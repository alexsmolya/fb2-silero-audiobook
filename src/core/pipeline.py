"""
Оркестратор — координация всех модулей для создания аудиокниги.
Управляет потоком: парсинг → разбиение → комментарии → TTS → склейка.
"""

from __future__ import annotations

import asyncio
import contextlib
import logging
import os
import tempfile
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, List, Optional, Tuple

from .fb2_parser import FB2Parser, ParsedBook
from .sentence_splitter import SentenceSplitter
from .tts_preprocessor import TtsPreprocessor, write_tts_artifacts
from .pause_policy import classify_boundary, target_pause
from .comment_manager import CommentManager, CommentConfig
from .tts_manager import TTSManager, TTSConfig
from .audio_assembler import AudioAssembler
from .book_input import BookInputPreparer, PreparedBook, detect_book_format
from .book_progress import BookProgressTracker
from .checkpoint_manager import CheckpointManager, Checkpoint
from src.utils.exceptions import PipelineCanceledError

logger = logging.getLogger(__name__)


@dataclass
class AppConfig:
    """Полная конфигурация приложения."""
    # Пути
    book_path: Path = Path("")
    output_dir: Path = Path.home() / "audiobooks"
    work_dir: Path = Path.home() / ".audiobook-generator"

    # Настройки книги
    lang: str = "ru"
    chapter_start: int = 0  # 0 = с начала
    chapter_end: int = 0    # 0 = до конца

    # Комментарии
    comment_config: CommentConfig = field(default_factory=CommentConfig)

    # TTS
    tts_config: TTSConfig = field(default_factory=TTSConfig)


class Pipeline:
    """Оркестратор процесса создания аудиокниги.

    Пример использования:
        config = AppConfig(
            book_path=Path("book.fb2"),
            output_dir=Path("./output"),
        )
        pipeline = Pipeline(config)
        result = await pipeline.run(
            progress_callback=lambda c, t: print(f"{c}/{t}"),
            cancel_event=threading.Event(),
        )
    """

    def __init__(self, config: AppConfig, diagnostics=None):
        self.config = config
        self.fb2_parser = FB2Parser()
        self.sentence_splitter = SentenceSplitter()
        self.comment_manager = CommentManager(config.comment_config)
        self.tts_manager = TTSManager(config.tts_config)
        self.audio_assembler = AudioAssembler()
        self.book_input_preparer = BookInputPreparer()
        self.checkpoint_manager = CheckpointManager(config.work_dir)
        self.diagnostics = diagnostics

        self._book: Optional[ParsedBook] = None
        self._temp_dir: Optional[Path] = None
        self._chapter_audio_paths: List[Path] = []
        self._paused = False
        self._pause_event = threading.Event()
        self._pause_event.set()  # не на паузе
        self._cancel_event = threading.Event()  # не отменён
        self._active_cancel_event: Optional[threading.Event] = None

    async def run(
        self,
        progress_callback: Optional[Callable[[str, float], None]] = None,
        cancel_event: Optional[threading.Event] = None,
        detail_callback: Optional[Callable[[int, int, str, str, str], None]] = None,
    ) -> Path:
        """Запуск полного процесса создания аудиокниги.

        Args:
            progress_callback: Колбэк прогресса (статус, процент 0.0-1.0).
            cancel_event: Событие отмены.
            detail_callback: Колбэк деталей синтеза (номер, всего, текст, голос, движок).

        Returns:
            Путь к финальному MP3-файлу.

        Raises:
            ValueError: Если книга не загружена.
        """
        if cancel_event is None:
            cancel_event = self._cancel_event

        self._active_cancel_event = cancel_event
        self._temp_dir = None
        self._chapter_audio_paths = []
        partial_output_path: Optional[Path] = None
        prepared_book: Optional[PreparedBook] = None
        terminal_status = "error"
        terminal_error: Optional[str] = None
        result_path: Optional[Path] = None
        primary_exception: Optional[BaseException] = None
        primary_traceback = None
        cleanup_exception: Optional[BaseException] = None
        progress = BookProgressTracker(
            lambda message, value: self._report(
                progress_callback, message, value,
            )
        )

        try:
            if self.diagnostics is not None:
                self.diagnostics.register_sensitive_paths(
                    self.config.book_path,
                    self.config.output_dir,
                    self.config.work_dir,
                )
            self._check_canceled(cancel_event)
            self.config.work_dir.mkdir(parents=True, exist_ok=True)
            self._temp_dir = Path(tempfile.mkdtemp(
                prefix="audiobook-run-",
                dir=self.config.work_dir,
            ))
            if self.diagnostics is not None:
                self.diagnostics.register_sensitive_paths(
                    self._temp_dir,
                )
                try:
                    self.diagnostics.start_sampler()
                except Exception as exc:
                    logger.warning("Не удалось запустить sampler диагностики: %s", exc)

            # Шаг 0: подготовка поддерживаемого формата к существующему FB2-пути
            with self._diagnostic_stage("input_preparation"):
                source_format = detect_book_format(self.config.book_path)
            progress.publish("Подготовка входной книги...", 0.0)
            if source_format != ".fb2":
                progress.publish(
                    f"Подготовка книги: "
                    f"{source_format.removeprefix('.').upper()} → FB2 через Calibre…",
                    0.0,
                )
            preparation_stage = (
                "calibre_conversion" if source_format != ".fb2"
                else "input_file_ready"
            )
            with self._diagnostic_stage(
                preparation_stage,
                input_size_bytes=self._file_size(self.config.book_path),
            ):
                prepared_book = self.book_input_preparer.prepare(
                    self.config.book_path,
                    cancel_event=cancel_event,
                )
            if self.diagnostics is not None:
                self.diagnostics.register_sensitive_paths(prepared_book.fb2_path)
            if prepared_book.converted:
                progress.publish(
                    "Книга подготовлена, запуск обработки…",
                    progress.PREPARATION_END,
                )

            # Шаг 1: Парсинг FB2
            self._check_canceled(cancel_event)
            progress.publish(
                "Парсинг FB2-файла...", progress.PREPARATION_END,
            )
            parsing_started = time.perf_counter()
            with self._diagnostic_stage("fb2_parsing"):
                book = self.fb2_parser.parse(prepared_book.fb2_path)
            if self.diagnostics is not None:
                self.diagnostics.book_parsed(
                    book,
                    time.perf_counter() - parsing_started,
                )
            self._book = book
            self._check_canceled(cancel_event)

            if not book.chapters:
                raise ValueError("В книге нет глав")

            preprocessor = TtsPreprocessor(
                backend=self.config.tts_config.backend,
                profile=(
                    self.config.tts_config.pronunciation_profile
                    or book.metadata.title
                ),
            )
            with self._diagnostic_stage("tts_preprocessing"):
                normalized_book = preprocessor.compile_book(book)
            artifact_stem = self.config.book_path.stem or "book"
            tts_script_path, tts_changes_path = write_tts_artifacts(
                normalized_book,
                self.config.output_dir,
                artifact_stem,
            )
            if self.diagnostics is not None:
                self.diagnostics.register_sensitive_paths(
                    tts_script_path,
                    tts_changes_path,
                )

            total_chapters = len(normalized_book.chapters)
            start_chapter = self.config.chapter_start or 0
            end_chapter = self.config.chapter_end or total_chapters
            chapters_to_process = normalized_book.chapters[start_chapter:end_chapter]
            chapter_texts = [
                "\n".join(chapter.paragraphs)
                for chapter in chapters_to_process
            ]
            progress.set_chapters(chapter_texts)

            progress.publish(
                f"Книга: '{book.metadata.title}', глав: {len(chapters_to_process)}",
                progress.PARSING_END,
            )

            # Проверка чекпоинта
            checkpoint = self.checkpoint_manager.load()
            resume_from = 0
            if checkpoint and checkpoint.book_path == str(self.config.book_path):
                resume_from = checkpoint.last_completed_chapter + 1

                # Если чекпоинт указывает на главу вне текущего диапазона — очищаем и начинаем сначала
                if resume_from >= end_chapter:
                    logger.warning(
                        "Чекпоинт (глава %d) вне диапазона [%d, %d), очищаю и начинаю сначала",
                        checkpoint.last_completed_chapter, start_chapter, end_chapter,
                    )
                    self.checkpoint_manager.clear()
                    resume_from = 0
                else:
                    completed_before_range = max(
                        0, min(resume_from - start_chapter, len(chapters_to_process)),
                    )
                    if completed_before_range:
                        progress.publish(
                            f"Восстановление с главы {resume_from + 1}...",
                            progress.chapter_complete(completed_before_range - 1),
                        )
                    else:
                        progress.publish(
                            f"Восстановление с главы {resume_from + 1}...",
                            progress.PARSING_END,
                        )

            # Шаг 2-4: Обработка каждой главы
            artifact_segments = []
            for idx, chapter in enumerate(chapters_to_process):
                self._check_canceled(cancel_event)

                # Ожидание снятия паузы
                self._pause_event.wait()

                chapter_num = start_chapter + idx
                if chapter_num < resume_from:
                    continue

                # Разбиение на предложения
                progress.publish(
                    f"Глава {chapter_num + 1}/{total_chapters}: разбиение на предложения...",
                    progress.chapter_bounds(idx)[0],
                )
                with self._diagnostic_stage(
                    "sentence_splitting",
                    chapter_index=chapter_num + 1,
                ):
                    structured_segments = self.sentence_splitter.split_chapter_segments(
                        chapter.title,
                        chapter.paragraphs,
                        book.metadata.lang,
                    )
                    sentences = [segment.text for segment in structured_segments]
                normalized_chapter = normalized_book.chapters[chapter_num]
                for segment_index, segment in enumerate(structured_segments, start=1):
                    paragraph_number = (
                        segment.source_paragraph_index
                        if segment.source_paragraph_index is not None
                        else 0
                    )
                    paragraph_id = (
                        normalized_chapter.paragraph_ids[paragraph_number - 1]
                        if 0 < paragraph_number <= len(normalized_chapter.paragraph_ids)
                        else f"ch-{chapter_num + 1:04d}-title"
                    )
                    artifact_segments.append({
                        "segment_id": f"ch-{chapter_num + 1:04d}-s-{segment_index:04d}",
                        "source_paragraph": paragraph_id,
                        "chapter": chapter_num + 1,
                        "paragraph": paragraph_number,
                        "boundary_before": segment.boundary_before,
                        "text": segment.text,
                    })
                write_tts_artifacts(
                    normalized_book,
                    self.config.output_dir,
                    artifact_stem,
                    segments=artifact_segments,
                )

                if not sentences:
                    logger.warning("Глава %d пуста, пропуск", chapter_num + 1)
                    progress.publish(
                        f"Глава {chapter_num + 1}/{total_chapters}: пуста, пропуск",
                        progress.chapter_complete(idx),
                    )
                    continue

                # Генерация комментариев (если включены)
                if self.config.comment_config.enabled:
                    progress.publish(
                        f"Глава {chapter_num + 1}/{total_chapters}: генерация комментариев...",
                        progress.chapter_preparation(idx),
                    )
                    comments = await self.comment_manager.generate_all(
                        sentences,
                        progress_callback=None,
                    )
                else:
                    comments = [None] * len(sentences)

                # Синтез речи
                progress.publish(
                    f"Глава {chapter_num + 1}/{total_chapters}: синтез речи...",
                    progress.chapter_preparation(idx),
                )

                tts_segments: List[str] = []
                for sentence_idx, sentence in enumerate(sentences):
                    tts_segments.append(sentence)
                    if (
                        sentence_idx < len(comments)
                        and comments[sentence_idx]
                    ):
                        tts_segments.append(comments[sentence_idx] or "")

                def tts_progress(completed: int, total: int) -> None:
                    progress.publish(
                        f"Глава {chapter_num + 1}/{total_chapters}: "
                        f"синтез речи {completed}/{total}...",
                        progress.chapter_tts(
                            idx, completed, total, tts_segments,
                        ),
                    )

                chapter_dir = self._temp_dir / f"chapter_{chapter_num:04d}"
                with self._diagnostic_stage(
                    "chapter_synthesis",
                    chapter_index=chapter_num + 1,
                    items=len(tts_segments),
                ):
                    synthesis_kwargs = dict(
                        text_segments=sentences,
                        comment_segments=comments,
                        chapter_dir=chapter_dir,
                        progress_callback=tts_progress,
                        detail_callback=detail_callback,
                        cancel_event=cancel_event,
                    )
                    if self.diagnostics is not None:
                        synthesis_kwargs.update(
                            diagnostics=self.diagnostics,
                            chapter_index=chapter_num + 1,
                            language=book.metadata.lang,
                            audio_probe=getattr(
                                self.audio_assembler, "get_audio_info", None,
                            ),
                        )
                    await self.tts_manager.synthesize_chapter(**synthesis_kwargs)

                # Склейка аудиофрагментов главы
                self._check_canceled(cancel_event)
                progress.publish(
                    f"Глава {chapter_num + 1}/{total_chapters}: склейка аудио...",
                    progress.chapter_tts(
                        idx, len(tts_segments), len(tts_segments), tts_segments,
                    ),
                )

                chapter_inputs = list(chapter_dir.glob("*.mp3"))
                assembly_started = time.perf_counter()
                with self._diagnostic_stage(
                    "chapter_assembly",
                    chapter_index=chapter_num + 1,
                    items=len(chapter_inputs),
                    input_size_bytes=sum(
                        self._file_size(path) or 0 for path in chapter_inputs
                    ),
                ):
                    chapter_audio = await self._assemble_chapter_audio(
                        sentences, comments, chapter_dir, chapter_num, cancel_event,
                        boundary_markers=[
                            segment.boundary_before for segment in structured_segments
                        ],
                    )
                if self.diagnostics is not None:
                    chapter_info = self._audio_info(chapter_audio)
                    self.diagnostics.emit(
                        "chapter_audio_assembled",
                        chapter_index=chapter_num + 1,
                        input_files=len(chapter_inputs),
                        input_size_bytes=sum(
                            self._file_size(path) or 0 for path in chapter_inputs
                        ),
                        duration_seconds=max(
                            0.0, time.perf_counter() - assembly_started,
                        ),
                        output_size_bytes=self._file_size(chapter_audio),
                        output_duration_seconds=chapter_info.get("duration_seconds"),
                    )
                self._chapter_audio_paths.append(chapter_audio)
                progress.publish(
                    f"Глава {chapter_num + 1}/{total_chapters}: обработана",
                    progress.chapter_complete(idx),
                )

                # Сохранение чекпоинта
                config_dict = {
                    "book_path": str(self.config.book_path),
                    "lang": self.config.lang,
                    "comment_frequency": self.config.comment_config.frequency,
                    "provider": self.config.comment_config.provider,
                }
                self.checkpoint_manager.save(Checkpoint(
                    book_path=str(self.config.book_path),
                    last_completed_chapter=chapter_num,
                    total_chapters=total_chapters,
                    config_hash=CheckpointManager.compute_config_hash(config_dict),
                    timestamp=time.time(),
                    output_dir=str(self._temp_dir),
                ))

            # Шаг 5: Склейка книги
            if self._chapter_audio_paths:
                self._check_canceled(cancel_event)
                progress.publish(
                    "Склейка всех глав в аудиокнигу...",
                    progress.CHAPTERS_END,
                )

                output_filename = f"{book.metadata.title}.mp3"
                # Очищаем имя файла от недопустимых символов
                output_filename = "".join(
                    c for c in output_filename
                    if c.isalnum() or c in " .-_()"
                ).strip()

                output_path = self.config.output_dir / output_filename
                self.config.output_dir.mkdir(parents=True, exist_ok=True)
                fd, partial_name = tempfile.mkstemp(
                    prefix=f".{output_filename}.",
                    suffix=".partial.mp3",
                    dir=self.config.output_dir,
                )
                os.close(fd)
                partial_output_path = Path(partial_name)

                def assembly_progress(completed: int, total: int) -> None:
                    progress.publish(
                        "Склейка всех глав в аудиокнигу...",
                        progress.final_assembly(completed, total),
                    )

                final_started = time.perf_counter()
                with self._diagnostic_stage(
                    "final_assembly",
                    items=len(self._chapter_audio_paths),
                    input_size_bytes=sum(
                        self._file_size(path) or 0
                        for path in self._chapter_audio_paths
                    ),
                ):
                    self.audio_assembler.assemble_book(
                        self._chapter_audio_paths,
                        partial_output_path,
                        progress_callback=assembly_progress,
                        cancel_event=cancel_event,
                    )
                final_ffmpeg_seconds = max(
                    0.0, time.perf_counter() - final_started,
                )
                self._check_canceled(cancel_event)
                verification_started = time.perf_counter()
                with self._diagnostic_stage("mp3_verification"):
                    if (
                        not partial_output_path.is_file()
                        or partial_output_path.stat().st_size <= 0
                    ):
                        raise RuntimeError(
                            "Финальная сборка не создала корректный MP3-файл"
                        )
                    progress.publish(
                        "Проверка готового MP3...",
                        progress.FINAL_ASSEMBLY_END,
                    )
                    os.replace(partial_output_path, output_path)
                    partial_output_path = None
                    if not output_path.is_file() or output_path.stat().st_size <= 0:
                        raise RuntimeError("Итоговый MP3-файл не найден после сборки")
                    final_info = self._audio_info(output_path)
                if self.diagnostics is not None:
                    self.diagnostics.set_mp3_result(
                        output_path, final_info.get("duration_seconds"),
                    )
                    self.diagnostics.emit(
                        "book_audio_assembled",
                        input_chapters=len(self._chapter_audio_paths),
                        input_size_bytes=sum(
                            self._file_size(path) or 0
                            for path in self._chapter_audio_paths
                        ),
                        ffmpeg_seconds=final_ffmpeg_seconds,
                        output_duration_seconds=final_info.get("duration_seconds"),
                        output_size_bytes=self._file_size(output_path),
                        bitrate_bps=final_info.get("bitrate_bps"),
                        verification_seconds=max(
                            0.0, time.perf_counter() - verification_started,
                        ),
                    )

                # Ошибка очистки Calibre-временных данных ещё должна считаться
                # ошибкой запуска, поэтому завершаем её до публикации 100%.
                prepared_book.cleanup()
                prepared_book = None

                # Очистка чекпоинта
                self.checkpoint_manager.clear()

                terminal_status = "success"
                result_path = output_path

            else:
                self._check_canceled(cancel_event)
                raise ValueError("Не удалось создать аудиокнигу: нет обработанных глав")

        except PipelineCanceledError as exc:
            terminal_status = "canceled"
            terminal_error = str(exc)
            primary_exception = exc
            primary_traceback = exc.__traceback__
        except BaseException as exc:
            terminal_status = "error"
            terminal_error = str(exc)
            primary_exception = exc
            primary_traceback = exc.__traceback__
        finally:
            self._active_cancel_event = None
            try:
                with self._diagnostic_stage("temporary_cleanup"):
                    cleanup_errors: List[BaseException] = []

                    def attempt_cleanup(action, warning: str) -> None:
                        try:
                            action()
                        except BaseException as exc:
                            cleanup_errors.append(exc)
                            progress.publish(warning, progress.last_value)

                    if partial_output_path is not None and partial_output_path.exists():
                        attempt_cleanup(
                            partial_output_path.unlink,
                            f"Не удалось удалить временный файл: {partial_output_path}",
                        )
                    if self._temp_dir and self._temp_dir.exists():
                        attempt_cleanup(
                            lambda: self.audio_assembler.cleanup_temp_files(self._temp_dir),
                            f"Не удалось удалить временный каталог: {self._temp_dir}",
                        )
                    attempt_cleanup(
                        self.checkpoint_manager.clear,
                        "Не удалось очистить checkpoint",
                    )
                    if prepared_book is not None:
                        attempt_cleanup(
                            prepared_book.cleanup,
                            "Не удалось очистить временные данные входной книги",
                        )
                    if cleanup_errors:
                        raise cleanup_errors[0]
            except BaseException as exc:
                cleanup_exception = exc
                if primary_exception is None:
                    terminal_status = "error"
                    terminal_error = str(exc)
            finally:
                if (
                    primary_exception is None
                    and cleanup_exception is None
                    and result_path is not None
                ):
                    try:
                        progress.complete(f"Аудиокнига готова: {result_path}")
                    except BaseException as exc:
                        primary_exception = exc
                        primary_traceback = exc.__traceback__
                        terminal_status = "error"
                        terminal_error = str(exc)
                if self.diagnostics is not None:
                    try:
                        self.diagnostics.finalize(
                            terminal_status,
                            error=terminal_error,
                            output_path=result_path,
                        )
                    except BaseException as exc:
                        has_pipeline_failure = (
                            primary_exception is not None
                            or cleanup_exception is not None
                        )
                        if not isinstance(exc, Exception) and not has_pipeline_failure:
                            primary_exception = exc
                            primary_traceback = exc.__traceback__
                        else:
                            logger.warning(
                                "Ошибка финализации diagnostics (%s) не изменяет "
                                "результат Pipeline",
                                type(exc).__name__,
                            )

        if primary_exception is not None:
            raise primary_exception.with_traceback(primary_traceback)
        if cleanup_exception is not None:
            raise cleanup_exception
        if result_path is None:
            raise RuntimeError("Pipeline завершился без результата")
        return result_path

    async def _assemble_chapter_audio(
        self,
        sentences: List[str],
        comments: List[Optional[str]],
        chapter_dir: Path,
        chapter_num: int,
        cancel_event: Optional[threading.Event] = None,
        boundary_markers: Optional[List[str]] = None,
    ) -> Path:
        """Сборка аудиофрагментов главы в один файл."""
        segments: List[Tuple[Path, float]] = []
        tts_cfg = self.config.tts_config

        # Собираем все mp3 файлы из директории главы
        # PiperTTSManager использует seg_*.mp3 (индексные имена),
        # EdgeTTSManager использует segment_*.mp3 (хеш-имена)
        audio_files = sorted(chapter_dir.glob("*.mp3"))

        # Формируем сегменты с паузами
        audio_idx = 0
        for i in range(len(sentences)):
            if audio_idx < len(audio_files):
                # Основной текст
                marker = (
                    boundary_markers[i]
                    if boundary_markers is not None and i < len(boundary_markers)
                    else "chapter_start" if i == 0 else "sentence"
                )
                previous_text = sentences[i - 1] if i > 0 else ""
                boundary = classify_boundary(marker, previous_text, sentences[i])
                main_target = (
                    tts_cfg.pause_after_comment
                    if i > 0 and i - 1 < len(comments) and comments[i - 1]
                    else target_pause(
                        boundary, tts_cfg.pause_between_sentences,
                    )
                )
                segments.append((
                    audio_files[audio_idx],
                    main_target,
                ))
                audio_idx += 1

            # Комментарий
            if i < len(comments) and comments[i] and audio_idx < len(audio_files):
                segments.append((audio_files[audio_idx], tts_cfg.pause_before_comment))
                audio_idx += 1

        chapter_output = self._temp_dir / f"chapter_{chapter_num:04d}_audio.wav"
        return self.audio_assembler.assemble_chapter(
            segments,
            chapter_output,
            cancel_event=cancel_event,
        )

    def pause(self):
        """Поставить процесс на паузу."""
        self._paused = True
        self._pause_event.clear()
        logger.info("Процесс поставлен на паузу")

    def resume(self):
        """Снять процесс с паузы."""
        self._paused = False
        self._pause_event.set()
        logger.info("Процесс возобновлён")

    def cancel(self):
        """Отменить процесс."""
        self._cancel_event.set()
        if self._active_cancel_event is not None:
            self._active_cancel_event.set()
        self._pause_event.set()  # снимаем с паузы, чтобы процесс завершился
        logger.info("Процесс отменён")

    def is_canceled(self) -> bool:
        """Проверка, был ли процесс отменён."""
        return self._cancel_event.is_set()

    def is_paused(self) -> bool:
        """Проверка, стоит ли процесс на паузе."""
        return self._paused

    def _report(
        self,
        callback: Optional[Callable[[str, float], None]],
        message: str,
        progress: float,
    ):
        """Отправка отчёта о прогрессе."""
        if callback:
            callback(message, progress)
        logger.info("[%.0f%%] %s", progress * 100, message)

    def _diagnostic_stage(self, stage: str, **fields):
        if self.diagnostics is None:
            return contextlib.nullcontext()
        return self.diagnostics.stage(stage, **fields)

    @staticmethod
    def _file_size(path: Path) -> Optional[int]:
        try:
            return Path(path).stat().st_size
        except OSError:
            return None

    def _audio_info(self, path: Path) -> dict:
        probe = getattr(self.audio_assembler, "get_audio_info", None)
        if probe is None:
            return {
                "duration_seconds": None,
                "bitrate_bps": None,
                "sample_rate": None,
            }
        return probe(path)

    @staticmethod
    def _check_canceled(cancel_event: threading.Event) -> None:
        if cancel_event.is_set():
            raise PipelineCanceledError("Обработка отменена пользователем")

    async def close(self):
        """Освобождение ресурсов."""
        await self.comment_manager.close()
        await self.tts_manager.close()
