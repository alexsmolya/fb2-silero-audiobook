"""
Оркестратор — координация всех модулей для создания аудиокниги.
Управляет потоком: парсинг → разбиение → комментарии → TTS → склейка.
"""

from __future__ import annotations

import asyncio
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

    def __init__(self, config: AppConfig):
        self.config = config
        self.fb2_parser = FB2Parser()
        self.sentence_splitter = SentenceSplitter()
        self.comment_manager = CommentManager(config.comment_config)
        self.tts_manager = TTSManager(config.tts_config)
        self.audio_assembler = AudioAssembler()
        self.book_input_preparer = BookInputPreparer()
        self.checkpoint_manager = CheckpointManager(config.work_dir)

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

        self._check_canceled(cancel_event)
        self._active_cancel_event = cancel_event

        self.config.work_dir.mkdir(parents=True, exist_ok=True)
        self._temp_dir = Path(tempfile.mkdtemp(
            prefix="audiobook-run-",
            dir=self.config.work_dir,
        ))
        self._chapter_audio_paths = []
        partial_output_path: Optional[Path] = None
        prepared_book: Optional[PreparedBook] = None
        progress = BookProgressTracker(
            lambda message, value: self._report(
                progress_callback, message, value,
            )
        )

        try:
            # Шаг 0: подготовка поддерживаемого формата к существующему FB2-пути
            source_format = detect_book_format(self.config.book_path)
            progress.publish("Подготовка входной книги...", 0.0)
            if source_format != ".fb2":
                progress.publish(
                    f"Подготовка книги: "
                    f"{source_format.removeprefix('.').upper()} → FB2 через Calibre…",
                    0.0,
                )
            prepared_book = self.book_input_preparer.prepare(
                self.config.book_path,
                cancel_event=cancel_event,
            )
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
            book = self.fb2_parser.parse(prepared_book.fb2_path)
            self._book = book
            self._check_canceled(cancel_event)

            if not book.chapters:
                raise ValueError("В книге нет глав")

            total_chapters = len(book.chapters)
            start_chapter = self.config.chapter_start or 0
            end_chapter = self.config.chapter_end or total_chapters
            chapters_to_process = book.chapters[start_chapter:end_chapter]
            chapter_texts = [
                " ".join(chapter.paragraphs)
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
                sentences = self.sentence_splitter.split(
                    " ".join(chapter.paragraphs),
                    book.metadata.lang,
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
                await self.tts_manager.synthesize_chapter(
                    text_segments=sentences,
                    comment_segments=comments,
                    chapter_dir=chapter_dir,
                    progress_callback=tts_progress,
                    detail_callback=detail_callback,
                    cancel_event=cancel_event,
                )

                # Склейка аудиофрагментов главы
                self._check_canceled(cancel_event)
                progress.publish(
                    f"Глава {chapter_num + 1}/{total_chapters}: склейка аудио...",
                    progress.chapter_tts(
                        idx, len(tts_segments), len(tts_segments), tts_segments,
                    ),
                )

                chapter_audio = await self._assemble_chapter_audio(
                    sentences, comments, chapter_dir, chapter_num, cancel_event,
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

                self.audio_assembler.assemble_book(
                    self._chapter_audio_paths,
                    partial_output_path,
                    progress_callback=assembly_progress,
                    cancel_event=cancel_event,
                )
                self._check_canceled(cancel_event)
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

                # Ошибка очистки Calibre-временных данных ещё должна считаться
                # ошибкой запуска, поэтому завершаем её до публикации 100%.
                prepared_book.cleanup()
                prepared_book = None

                # Очистка чекпоинта
                self.checkpoint_manager.clear()

                progress.complete(
                    f"Аудиокнига готова: {output_path}",
                )

                return output_path

            else:
                self._check_canceled(cancel_event)
                raise ValueError("Не удалось создать аудиокнигу: нет обработанных глав")

        finally:
            self._active_cancel_event = None
            if partial_output_path is not None and partial_output_path.exists():
                try:
                    partial_output_path.unlink()
                except OSError:
                    progress.publish(
                        f"Не удалось удалить временный файл: {partial_output_path}",
                        progress.last_value,
                    )
            # Очистка временных файлов
            if self._temp_dir and self._temp_dir.exists():
                try:
                    self.audio_assembler.cleanup_temp_files(self._temp_dir)
                except OSError:
                    progress.publish(
                        f"Не удалось удалить временный каталог: {self._temp_dir}",
                        progress.last_value,
                    )

            # Очищаем чекпоинт при любом прерывании (кроме успешного завершения):
            # временные файлы удалены, так что чекпоинт бесполезен.
            # Если дошли до return output_path в строке 245 — clear() уже вызван,
            # вызывать повторно безвредно (clear проверяет exists()).
            self.checkpoint_manager.clear()
            if prepared_book is not None:
                prepared_book.cleanup()

    async def _assemble_chapter_audio(
        self,
        sentences: List[str],
        comments: List[Optional[str]],
        chapter_dir: Path,
        chapter_num: int,
        cancel_event: Optional[threading.Event] = None,
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
                segments.append((audio_files[audio_idx], tts_cfg.pause_between_sentences))
                audio_idx += 1

            # Комментарий
            if i < len(comments) and comments[i] and audio_idx < len(audio_files):
                segments.append((audio_files[audio_idx], tts_cfg.pause_before_comment))
                audio_idx += 1
                # Добавляем паузу после комментария к последнему сегменту
                if segments:
                    segments[-1] = (segments[-1][0], tts_cfg.pause_after_comment)

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

    @staticmethod
    def _check_canceled(cancel_event: threading.Event) -> None:
        if cancel_event.is_set():
            raise PipelineCanceledError("Обработка отменена пользователем")

    async def close(self):
        """Освобождение ресурсов."""
        await self.comment_manager.close()
        await self.tts_manager.close()
