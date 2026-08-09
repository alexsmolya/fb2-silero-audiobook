"""
Модуль склейки аудиофайлов.
Объединяет аудиофрагменты в главы и главы в финальный MP3-файл.
Использует прямой вызов ffmpeg вместо pydub (pydub требует audioop,
который удалён из стандартной библиотеки Python 3.13+).
"""

from __future__ import annotations

import json
import logging
import math
import os
import shutil
import subprocess as sp
import tempfile
import threading
from pathlib import Path
from typing import Callable, List, Optional, Tuple

from src.utils.exceptions import PipelineCanceledError
from src.core.pause_policy import (
    CHAPTER_TARGET_FINAL_SILENCE,
    measure_wav_edge_silence,
    read_edge_silence,
    required_padding,
    write_edge_silence,
)

logger = logging.getLogger(__name__)

_FFMPEG_ERROR_TAIL_CHARS = 4096


class AudioAssembler:
    """Склейка аудиофрагментов в главы и книгу через ffmpeg.

    Пример использования:
        assembler = AudioAssembler()
        # Склейка главы
        chapter_path = assembler.assemble_chapter(
            segments=[("path1.wav", 0.3), ("path2.wav", 1.0)],
            output_path=Path("chapter1.wav"),
        )
        # Склейка книги
        book_path = assembler.assemble_book(
            chapter_paths=[Path("chapter1.wav"), Path("chapter2.wav")],
            output_path=Path("book.mp3"),
        )
    """

    def __init__(self, sample_rate: int = 22050):
        """Инициализация AudioAssembler.

        Args:
            sample_rate: Частота дискретизации для выходных WAV-файлов.
                По умолчанию 22050 Гц — стандартная частота моделей Piper TTS.
                Edge TTS (через ffmpeg) будет передискретизирован под эту частоту
                при склейке, что обеспечивает консистентность всех аудиофрагментов
                и предотвращает белый шум из-за mismatch в ffmpeg concat demuxer.
        """
        self.sample_rate = sample_rate
        self._ffmpeg = self._find_ffmpeg()
        self._audio_probe_warnings: set[str] = set()

    # ── helpers ────────────────────────────────────────────────

    @staticmethod
    def _find_ffmpeg() -> str:
        """Поиск ffmpeg в PATH."""
        exe = shutil.which("ffmpeg")
        if exe is None:
            raise RuntimeError(
                "ffmpeg не найден. Установите ffmpeg:\n"
                "  sudo apt install ffmpeg          # Debian/Ubuntu\n"
                "  sudo dnf install ffmpeg          # Fedora\n"
                "  brew install ffmpeg              # macOS\n"
                "  winget install ffmpeg            # Windows"
            )
        return exe

    @staticmethod
    def _check_canceled(cancel_event: Optional[threading.Event]) -> None:
        if cancel_event is not None and cancel_event.is_set():
            raise PipelineCanceledError("Обработка отменена пользователем")

    def _run_ffmpeg(
        self,
        args: List[str],
        cancel_event: Optional[threading.Event] = None,
        **kwargs,
    ) -> None:
        """Запуск ffmpeg с логированием."""
        self._check_canceled(cancel_event)
        cmd = [self._ffmpeg] + args
        logger.debug("ffmpeg: %s", " ".join(str(a) for a in cmd))
        process = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE, **kwargs)
        try:
            while True:
                try:
                    _, stderr_bytes = process.communicate(timeout=0.1)
                    break
                except sp.TimeoutExpired:
                    if cancel_event is None or not cancel_event.is_set():
                        continue
                    process.terminate()
                    try:
                        _, stderr_bytes = process.communicate(timeout=2.0)
                    except sp.TimeoutExpired:
                        process.kill()
                        _, stderr_bytes = process.communicate()
                    raise PipelineCanceledError(
                        "Обработка отменена пользователем"
                    )
        except BaseException:
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=2.0)
                except sp.TimeoutExpired:
                    process.kill()
                    process.wait()
            raise

        if process.returncode:
            stderr = stderr_bytes.decode("utf-8", errors="replace") if stderr_bytes else ""
            logger.error("ffmpeg error (code %d): %s", process.returncode, stderr)
            stderr_tail = stderr[-_FFMPEG_ERROR_TAIL_CHARS:]
            if len(stderr) > len(stderr_tail):
                stderr_tail = (
                    "[начало stderr опущено; показан диагностический хвост]\n"
                    + stderr_tail
                )
            raise RuntimeError(
                f"Ошибка ffmpeg (код {process.returncode}): {stderr_tail}"
            )

    def _make_silence(
        self,
        path: Path,
        duration_sec: float,
        cancel_event: Optional[threading.Event] = None,
    ) -> Path:
        """Создание WAV-файла с тишиной заданной длительности."""
        duration_ms = int(duration_sec * 1000)
        self._run_ffmpeg([
            "-f", "lavfi",
            "-i", f"anullsrc=r={self.sample_rate}:cl=mono",
            "-t", str(duration_sec),
            "-acodec", "pcm_s16le",
            str(path),
        ], cancel_event=cancel_event)
        return path

    # ── public API ─────────────────────────────────────────────

    def assemble_chapter(
        self,
        segments: List[Tuple[Path, float]],
        output_path: Path,
        cancel_event: Optional[threading.Event] = None,
    ) -> Path:
        """Склейка аудиофрагментов в главу.

        Все входные файлы и паузы декодируются/создаются в одном filter graph
        ffmpeg и склеиваются в WAV (PCM s16le, 1ch, sample_rate Гц). Это сохраняет
        нормализацию кодеков без отдельного запуска ffmpeg для каждого сегмента
        и каждой паузы.

        Args:
            segments: Список кортежей (путь_к_аудио, пауза_перед_в_сек).
            output_path: Путь для сохранения готовой главы.

        Returns:
            Путь к готовому аудиофайлу главы.
        """
        logger.info("Склейка главы: %d фрагментов", len(segments))
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with tempfile.TemporaryDirectory(prefix="chapter_") as tmp_dir:
            tmp_root = Path(tmp_dir)
            input_args: List[str] = []
            filters: List[str] = []
            concat_inputs: List[str] = []
            input_index = 0

            previous_edge = None
            for idx, (audio_path, target) in enumerate(segments):
                self._check_canceled(cancel_event)
                current_edge = read_edge_silence(audio_path)
                pause = required_padding(target, previous_edge, current_edge)
                # Express padding as an integer number of output samples. Besides
                # making boundaries sample-accurate, this removes sub-sample
                # floating-point residues such as 5.55e-17. FFmpeg's duration
                # parser rejects that scientific notation during filter setup.
                pause_samples = max(0, round(pause * self.sample_rate))
                if pause_samples > 0:
                    pause_label = f"pause_{idx}"
                    filters.append(
                        f"anullsrc=r={self.sample_rate}:cl=mono,"
                        f"atrim=end_sample={pause_samples},asetpts=PTS-STARTPTS"
                        f"[{pause_label}]"
                    )
                    concat_inputs.append(f"[{pause_label}]")

                if not audio_path.exists():
                    logger.warning("Файл не найден: %s", audio_path)
                    continue

                input_args.extend(["-i", str(audio_path)])
                audio_label = f"segment_{idx}"
                filters.append(
                    f"[{input_index}:a:0]"
                    f"aformat=sample_fmts=s16:sample_rates={self.sample_rate}:"
                    f"channel_layouts=mono,asetpts=PTS-STARTPTS[{audio_label}]"
                )
                concat_inputs.append(f"[{audio_label}]")
                input_index += 1
                previous_edge = current_edge

            if not concat_inputs:
                raise FileNotFoundError("Нет ни одного валидного аудиофайла для склейки главы")

            filters.append(
                "".join(concat_inputs)
                + f"concat=n={len(concat_inputs)}:v=0:a=1[chapter]"
            )
            filter_graph = ";\n".join(filters)

            self._check_canceled(cancel_event)
            self._run_ffmpeg([
                *input_args,
                "-filter_complex", filter_graph,
                "-map", "[chapter]",
                "-acodec", "pcm_s16le",
                "-ac", "1",
                "-ar", str(self.sample_rate),
                "-y", str(output_path),
            ], cancel_event=cancel_event)

        self._check_canceled(cancel_event)
        # Получаем длительность через ffprobe
        duration = self.get_audio_duration(output_path)
        chapter_edge = measure_wav_edge_silence(output_path)
        if chapter_edge is not None:
            write_edge_silence(output_path, chapter_edge)
        logger.info("Глава сохранена: %s (%.1f сек)", output_path, duration)
        return output_path

    def assemble_book(
        self,
        chapter_paths: List[Path],
        output_path: Path,
        chapter_pause: float = CHAPTER_TARGET_FINAL_SILENCE,
        progress_callback: Optional[Callable[[int, int], None]] = None,
        cancel_event: Optional[threading.Event] = None,
    ) -> Path:
        """Склейка глав в финальную аудиокнигу.

        Args:
            chapter_paths: Список путей к аудиофайлам глав.
            output_path: Путь для сохранения финального MP3.
            chapter_pause: Целевая итоговая пауза между главами в секундах.
            progress_callback: Колбэк прогресса (текущая глава, всего).

        Returns:
            Путь к финальному MP3-файлу.
        """
        logger.info(
            "Склейка книги: %d глав -> %s",
            len(chapter_paths), output_path,
        )
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with tempfile.TemporaryDirectory(prefix="book_") as tmp_dir:
            tmp_root = Path(tmp_dir)
            file_list_paths: List[Path] = []
            total = len(chapter_paths)
            previous_edge = None

            for i, chapter_path in enumerate(chapter_paths):
                self._check_canceled(cancel_event)
                current_edge = read_edge_silence(chapter_path)
                pause = required_padding(
                    chapter_pause,
                    previous_edge,
                    current_edge,
                    fallback_padding=1.5,
                )
                if i > 0 and pause > 0:
                    silence_path = tmp_root / f"pause_{i}.wav"
                    self._make_silence(silence_path, pause, cancel_event)
                    file_list_paths.append(silence_path)

                if not chapter_path.exists():
                    logger.warning("Глава не найдена: %s", chapter_path)
                    continue

                file_list_paths.append(chapter_path)
                previous_edge = current_edge

                if progress_callback:
                    progress_callback(i + 1, total)

            if not file_list_paths:
                raise FileNotFoundError("Нет ни одной валидной главы для склейки книги")

            # Создаём файл-список для ffmpeg concat demuxer
            list_file = tmp_root / "filelist.txt"
            with open(list_file, "w", encoding="utf-8") as f:
                for p in file_list_paths:
                    f.write(f"file '{p.resolve()}'\n")

            # Конвертируем всё в WAV (чтобы concat работал с одинаковым кодеком)
            merged_wav = tmp_root / "merged.wav"
            self._check_canceled(cancel_event)
            self._run_ffmpeg([
                "-f", "concat",
                "-safe", "0",
                "-i", str(list_file),
                "-acodec", "pcm_s16le",
                "-ac", "1",
                "-ar", str(self.sample_rate),
                "-y", str(merged_wav),
            ], cancel_event=cancel_event)

            # Финальное кодирование в MP3
            self._check_canceled(cancel_event)
            self._run_ffmpeg([
                "-i", str(merged_wav),
                "-codec:a", "libmp3lame",
                "-b:a", "192k",
                "-q:a", "0",
                "-y", str(output_path),
            ], cancel_event=cancel_event)

        self._check_canceled(cancel_event)
        duration_min = self.get_audio_duration(output_path) / 60
        logger.info(
            "Аудиокнига сохранена: %s (%.1f мин)",
            output_path, duration_min,
        )

        return output_path

    def cleanup_temp_files(self, temp_dir: Path):
        """Удаление временных файлов.

        Args:
            temp_dir: Директория с временными файлами.
        """
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
            logger.debug("Временные файлы удалены: %s", temp_dir)

    def get_audio_duration(self, audio_path: Path) -> float:
        """Получение длительности аудиофайла в секундах через ffprobe.

        Args:
            audio_path: Путь к аудиофайлу.

        Returns:
            Длительность в секундах.
        """
        info = self.get_audio_info(audio_path)
        return float(info.get("duration_seconds") or 0.0)

    def get_audio_info(self, audio_path: Path) -> dict:
        """Получить длительность, bitrate и sample rate через общий ffprobe."""
        empty = {
            "duration_seconds": None,
            "bitrate_bps": None,
            "sample_rate": None,
        }
        if not audio_path.exists():
            return empty
        ffprobe = shutil.which("ffprobe")
        if ffprobe is None:
            self._warn_audio_probe_once("missing", "ffprobe не найден")
            return empty
        try:
            result = sp.run(
                [
                    ffprobe, "-v", "quiet", "-print_format", "json",
                    "-show_format", "-show_streams", str(audio_path),
                ],
                capture_output=True,
                check=True,
                timeout=10.0,
            )
            data = json.loads(result.stdout)
            audio_stream = next(
                (
                    stream for stream in data.get("streams", [])
                    if stream.get("codec_type") == "audio"
                ),
                {},
            )
            format_data = data.get("format", {})
            return {
                "duration_seconds": _first_positive_number(
                    format_data.get("duration"), audio_stream.get("duration"),
                ),
                "bitrate_bps": _first_positive_number(
                    format_data.get("bit_rate"), audio_stream.get("bit_rate"),
                ),
                "sample_rate": _optional_number(audio_stream.get("sample_rate")),
            }
        except sp.TimeoutExpired:
            self._warn_audio_probe_once(
                "timeout", "ffprobe превысил лимит времени",
            )
            return empty
        except OSError:
            self._warn_audio_probe_once("missing", "ffprobe не найден")
            return empty
        except (
            sp.CalledProcessError, json.JSONDecodeError,
            AttributeError, TypeError, ValueError,
        ) as exc:
            self._warn_audio_probe_once(
                type(exc).__name__, "ffprobe вернул некорректные данные",
            )
            return empty

    def _warn_audio_probe_once(self, key: str, message: str) -> None:
        warnings = getattr(self, "_audio_probe_warnings", None)
        if warnings is None:
            warnings = self._audio_probe_warnings = set()
        if key not in warnings:
            warnings.add(key)
            logger.warning("%s", message)


def _optional_number(value):
    if isinstance(value, bool):
        return None
    try:
        number = float(value)
        if not math.isfinite(number) or number <= 0:
            return None
        return int(number) if number.is_integer() else number
    except (TypeError, ValueError):
        return None


def _first_positive_number(*values):
    for value in values:
        number = _optional_number(value)
        if number is not None:
            return number
    return None
