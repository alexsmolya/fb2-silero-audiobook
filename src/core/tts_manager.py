"""
Модуль управления синтезом речи.
Содержит TTSConfig и TTSManager — фабрику/диспетчер для выбора бэкенда.
"""

from __future__ import annotations

import logging
import os
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from src.core.tts_base import TTSBackend
from src.utils.exceptions import PipelineCanceledError

logger = logging.getLogger(__name__)


# Маппинг (движок, язык, пол) → имя голоса
BACKEND_VOICES = {
    "edge": {
        "ru": {"male": "ru-RU-DmitryNeural", "female": "ru-RU-SvetlanaNeural"},
        "en": {"male": "en-US-GuyNeural", "female": "en-US-JennyNeural"},
        "ja": {"male": "ja-JP-KeitaNeural", "female": "ja-JP-NanamiNeural"},
        "zh": {"male": "zh-CN-YunxiNeural", "female": "zh-CN-XiaoxiaoNeural"},
    },
    "silero": {
        "ru": {"male": "eugene", "female": "xenia"},
        "en": {"male": "random", "female": "en_0"},
    },
    "piper": {
        "ru": {"male": "ru_RU-dmitri-medium", "female": "ru_RU-irina-medium"},
        "en": {"male": "en_US-joe-medium", "female": "en_US-amy-medium"},
        # Для китайского в Piper только женские голоса
        "zh": {"male": "zh_CN-xiao_ya-medium", "female": "zh_CN-xiao_ya-medium"},
    },
    "supertonic": {
        "ru": {"male": "M1", "female": "F1"},
        "en": {"male": "M1", "female": "F1"},
        "ja": {"male": "M1", "female": "F1"},
        "zh": {"male": "M1", "female": "F1"},
    },
}
# Fallback: если язык не найден — берём английский
_FALLBACK_LANG = "en"


def resolve_voice(backend: str, book_lang: str, gender: str) -> str:
    """Преобразовать (движок, язык книги, пол) в конкретное имя голоса.

    Args:
        backend: Имя TTS-движка ("edge", "silero", "piper", "supertonic").
        book_lang: Код языка книги ("ru", "en", "ja", "zh").
        gender: Пол ("male" или "female").

    Returns:
        Имя голоса (например, "ru-RU-DmitryNeural" или "eugene").
    """
    voices_for_backend = BACKEND_VOICES.get(backend, BACKEND_VOICES["edge"])
    voices_for_lang = voices_for_backend.get(book_lang, voices_for_backend.get(_FALLBACK_LANG, {}))
    return voices_for_lang.get(gender, voices_for_lang.get("female", next(iter(voices_for_lang.values()))))


@dataclass
class TTSConfig:
    """Конфигурация синтеза речи."""
    backend: str = "edge"  # "edge" | "piper"
    main_voice: str = "ru-RU-SvetlanaNeural"
    comment_voice: str = "ru-RU-DmitryNeural"
    main_speed: float = 1.0  # 1.0 = нормальный темп
    comment_speed: float = 1.0
    pause_before_comment: float = 1.0  # секунд тишины перед комментарием
    pause_after_comment: float = 0.7  # секунд тишины после комментария
    pause_between_sentences: float = 0.3  # пауза между предложениями


# Словарь для обратной связи backend → читаемое название
BACKEND_NAMES = {
    "edge": "Edge TTS",
    "piper": "Piper (локальный)",
    "supertonic": "Supertonic 3 (локальный)",
    "silero": "Silero TTS (локальный)",
}


class TTSManager:
    """Фабрика/диспетчер для TTS-бэкендов.

    Создаёт нужный бэкенд (EdgeTTSManager, PiperTTSManager) на основе
    config.backend и делегирует ему все вызовы.
    """

    def __init__(self, config: TTSConfig):
        self.config = config
        self._backend: Optional[TTSBackend] = None
        self._diagnostics_backend_reported = False
        self._diagnostics_backend_started: Optional[float] = None

    async def _get_backend(self) -> TTSBackend:
        """Ленивая инициализация бэкенда."""
        if self._backend is not None:
            return self._backend

        if self.config.backend == "edge":
            from src.core.tts_edge import EdgeTTSManager
            self._backend = EdgeTTSManager(self.config)
        elif self.config.backend == "piper":
            from src.core.tts_piper import PiperTTSManager
            self._backend = PiperTTSManager(self.config)
        elif self.config.backend == "supertonic":
            from src.core.tts_supertonic import SupertonicTTSManager
            self._backend = SupertonicTTSManager(self.config)
        elif self.config.backend == "silero":
            from src.core.tts_silero import SileroTTSManager
            self._backend = SileroTTSManager(self.config)
        else:
            raise ValueError(f"Неизвестный TTS-бэкенд: {self.config.backend}")

        logger.info("TTS бэкенд: %s", BACKEND_NAMES.get(self.config.backend, self.config.backend))
        return self._backend

    async def synthesize_segment(
        self,
        text: str,
        voice: str,
        speed: float = 1.0,
        output_dir: Optional[Path] = None,
    ) -> Path:
        """Синтез одного текстового сегмента в аудиофайл.

        Args:
            text: Текст для озвучки.
            voice: Имя голоса.
            speed: Темп речи.
            output_dir: Директория для временного файла.

        Returns:
            Путь к аудиофайлу.
        """
        backend = await self._get_backend()
        return await backend.synthesize_segment(text, voice, speed, output_dir)

    async def synthesize_chapter(
        self,
        text_segments: List[str],
        comment_segments: List[Optional[str]],
        chapter_dir: Path,
        progress_callback: Optional[Callable[[int, int], None]] = None,
        detail_callback: Optional[Callable[[int, int, str, str, str], None]] = None,
        cancel_event: Optional[threading.Event] = None,
        diagnostics=None,
        chapter_index: int = 0,
        language: str = "",
        audio_probe: Optional[Callable[[Path], Dict[str, Any]]] = None,
    ) -> Path:
        """Синтез целой главы с комментариями.

        Args:
            text_segments: Сегменты основного текста.
            comment_segments: Сегменты комментариев (None если нет).
            chapter_dir: Директория для временных файлов главы.
            progress_callback: Колбэк прогресса (текущий, всего).
            detail_callback: Колбэк с деталями (текущий, всего, текст, голос, бэкенд).

        Returns:
            Путь к директории с аудиофайлами главы.
        """
        backend = await self._get_backend()

        planned_segments = []
        for index, text in enumerate(text_segments):
            planned_segments.append((text, "main"))
            if index < len(comment_segments) and comment_segments[index]:
                planned_segments.append((comment_segments[index] or "", "comment"))
        pending: Dict[str, Any] = {}
        synthesis_started = time.perf_counter()
        supports_detail_callback = False
        legacy_files_before = (
            set(chapter_dir.glob("*.mp3")) | set(chapter_dir.glob("*.wav"))
        )
        legacy_claimed_paths: set[Path] = set()

        def check_canceled() -> None:
            if cancel_event is not None and cancel_event.is_set():
                raise PipelineCanceledError("Обработка отменена пользователем")

        def checked_progress(completed: int, total: int) -> None:
            # Backend вызывает этот callback сразу после атомарного TTS-вызова.
            if diagnostics is not None:
                started = pending.get("started", time.perf_counter())
                before = pending.get("files_before", legacy_files_before)
                files = set(chapter_dir.glob("*.mp3")) | set(chapter_dir.glob("*.wav"))
                created = sorted(files - before - legacy_claimed_paths)
                audio_path = pending.get("audio_path")
                if audio_path is None:
                    audio_path = created[-1] if created else (
                        max(files, key=lambda p: p.stat().st_mtime_ns)
                        if pending and files else None
                    )
                confirmed_audio = (
                    audio_path is not None and Path(audio_path).is_file()
                )
                segment_outcome = pending.get("outcome", "success")
                if segment_outcome == "success" and not confirmed_audio:
                    pending.clear()
                    if not self._diagnostics_backend_reported:
                        self._diagnostics_backend_started = None
                    check_canceled()
                    if progress_callback:
                        progress_callback(completed, total)
                    return
                info = None
                if audio_path is not None and audio_probe is not None:
                    try:
                        info = audio_probe(audio_path)
                    except Exception as exc:
                        diagnostics.diagnostic_error("tts_audio_probe", exc)
                planned_text, segment_type = (
                    planned_segments[completed - 1]
                    if 0 < completed <= len(planned_segments)
                    else (pending.get("text", ""), pending.get("segment_type", "main"))
                )
                device = getattr(backend, "_device", None) or (
                    "cuda" if self.config.backend == "silero" and os.environ.get("CUDA_VISIBLE_DEVICES", "") != "" else "cpu"
                )
                segment_error = pending.get("outcome_error")
                if (
                    not supports_detail_callback
                    and completed == 1
                    and not self._diagnostics_backend_reported
                    and self._diagnostics_backend_started is None
                ):
                    self._diagnostics_backend_started = synthesis_started
                if not supports_detail_callback and audio_path in created:
                    legacy_claimed_paths.add(audio_path)
                publish_initialization = (
                    not self._diagnostics_backend_reported
                    and self._diagnostics_backend_started is not None
                )
                if publish_initialization:
                    diagnostics.emit(
                        "stage_start",
                        stage="tts_model_initialization",
                        includes_first_segment=True,
                    )
                diagnostics.record_tts_segment(
                    chapter_index=chapter_index,
                    segment_index=completed,
                    segment_total=total,
                    segment_type=segment_type,
                    backend=pending.get("backend", self.config.backend),
                    voice=pending.get("voice", self.config.main_voice),
                    language=language,
                    device=str(device),
                    characters=len(planned_text),
                    wall_seconds=max(0.0, time.perf_counter() - started),
                    audio_path=audio_path,
                    audio_info=info,
                    status=segment_outcome,
                    error=segment_error,
                    text_excerpt=(
                        planned_text[:80]
                        if segment_outcome != "success"
                        else None
                    ),
                    text=planned_text,
                )
                if publish_initialization:
                    diagnostics.emit(
                        "stage_end",
                        stage="tts_model_initialization",
                        status=(
                            "success" if segment_outcome == "success"
                            else "canceled" if segment_outcome == "canceled"
                            else "error"
                        ),
                        outcome=segment_outcome,
                        duration_seconds=max(
                            0.0,
                            time.perf_counter()
                            - self._diagnostics_backend_started,
                        ),
                        includes_first_segment=True,
                        error=segment_error,
                    )
                    self._diagnostics_backend_reported = True
                pending.clear()
            check_canceled()
            if progress_callback:
                progress_callback(completed, total)

        def checked_detail(
            completed: int,
            total: int,
            text: str,
            voice: str,
            backend_name: str,
        ) -> None:
            # Backend вызывает этот callback непосредственно перед фрагментом.
            check_canceled()
            segment_type = (
                planned_segments[completed - 1][1]
                if 0 < completed <= len(planned_segments)
                else "main"
            )
            pending.clear()
            if (
                diagnostics is not None
                and not self._diagnostics_backend_reported
                and self._diagnostics_backend_started is None
            ):
                self._diagnostics_backend_started = time.perf_counter()
            pending.update({
                "completed": completed,
                "started": time.perf_counter(),
                "files_before": set(chapter_dir.glob("*.mp3")) | set(chapter_dir.glob("*.wav")),
                "text": text,
                "segment_type": segment_type,
                "voice": voice,
                "backend": backend_name,
            })
            if detail_callback:
                detail_callback(completed, total, text, voice, backend_name)

        def checked_outcome(
            completed: int,
            total: int,
            outcome: str,
            error: Optional[str],
            audio_path: Optional[Path],
        ) -> None:
            if diagnostics is None:
                return
            pending["outcome"] = outcome
            pending["outcome_error"] = error
            pending["audio_path"] = audio_path

        check_canceled()

        def record_pending_failure(exc: BaseException) -> None:
            if diagnostics is None or not pending:
                return
            failure_outcome = (
                "canceled" if isinstance(exc, PipelineCanceledError) else "error"
            )
            completed = int(pending.get("completed", 1))
            planned_text, segment_type = (
                planned_segments[completed - 1]
                if 0 < completed <= len(planned_segments)
                else (pending.get("text", ""), pending.get("segment_type", "main"))
            )
            publish_initialization = (
                not self._diagnostics_backend_reported
                and self._diagnostics_backend_started is not None
            )
            if publish_initialization:
                diagnostics.emit(
                    "stage_start",
                    stage="tts_model_initialization",
                    includes_first_segment=True,
                )
            diagnostics.record_tts_segment(
                chapter_index=chapter_index,
                segment_index=completed,
                segment_total=len(planned_segments),
                segment_type=segment_type,
                backend=pending.get("backend", self.config.backend),
                voice=pending.get("voice", self.config.main_voice),
                language=language,
                device=str(getattr(backend, "_device", None) or "cpu"),
                characters=len(planned_text),
                wall_seconds=max(
                    0.0,
                    time.perf_counter()
                    - pending.get("started", time.perf_counter()),
                ),
                audio_path=None,
                status=failure_outcome,
                error=str(exc)[:300],
                text_excerpt=planned_text[:80],
                text=planned_text,
            )
            if publish_initialization:
                diagnostics.emit(
                    "stage_end",
                    stage="tts_model_initialization",
                    status=failure_outcome,
                    outcome=failure_outcome,
                    duration_seconds=max(
                        0.0,
                        time.perf_counter()
                        - self._diagnostics_backend_started,
                    ),
                    includes_first_segment=True,
                    error=str(exc)[:300],
                )
                self._diagnostics_backend_reported = True
            pending.clear()

        if hasattr(backend, 'synthesize_chapter'):
            import inspect
            sig = inspect.signature(backend.synthesize_chapter)
            callback_kwargs = {"progress_callback": checked_progress}
            if 'detail_callback' in sig.parameters:
                supports_detail_callback = True
                callback_kwargs["detail_callback"] = checked_detail
            if diagnostics is not None and 'outcome_callback' in sig.parameters:
                callback_kwargs["outcome_callback"] = checked_outcome
            try:
                return await backend.synthesize_chapter(
                    text_segments, comment_segments, chapter_dir,
                    **callback_kwargs,
                )
            except BaseException as exc:
                record_pending_failure(exc)
                raise

        raise RuntimeError("TTS backend does not support chapter synthesis")

    async def get_available_voices(self, lang: str = "") -> List[Dict[str, Any]]:
        """Получение списка доступных голосов.

        Args:
            lang: Код языка для фильтрации (например, "ru"). Если пусто — все голоса.

        Returns:
            Список словарей с информацией о голосах.
        """
        backend = await self._get_backend()
        return await backend.get_available_voices(lang)

    async def close(self):
        """Освобождение ресурсов бэкенда."""
        if self._backend is not None:
            await self._backend.close()
