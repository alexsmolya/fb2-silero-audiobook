"""Подготовка входных книг для существующего FB2-пайплайна."""

from __future__ import annotations

import logging
import shutil
import subprocess
import tempfile
import threading
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Optional

from src.utils.exceptions import AudiobookError, PipelineCanceledError

logger = logging.getLogger(__name__)


NATIVE_BOOK_EXTENSIONS = frozenset({".fb2"})
CALIBRE_BOOK_EXTENSIONS = frozenset({
    ".epub",
    ".mobi",
    ".azw",
    ".azw3",
    ".txt",
    ".txtz",
    ".docx",
    ".odt",
    ".rtf",
    ".html",
    ".htm",
    ".htmlz",
    ".fbz",
})
SUPPORTED_BOOK_EXTENSIONS = NATIVE_BOOK_EXTENSIONS | CALIBRE_BOOK_EXTENSIONS

CALIBRE_REQUIRED_MESSAGE = (
    "Для импорта EPUB, MOBI, AZW/AZW3, TXT/TXTZ, DOCX, ODT, RTF, "
    "HTML/HTM/HTMLZ и FBZ требуется Calibre. В CachyOS установите его "
    "командой: sudo pacman -S calibre"
)


class UnsupportedBookFormatError(AudiobookError):
    """Выбранный формат книги не входит в разрешённый список."""


class CalibreImportError(AudiobookError):
    """Calibre не смог подготовить входную книгу."""


def detect_book_format(path: Path | str) -> str:
    """Вернуть нормализованное расширение поддерживаемой книги."""
    source_path = Path(path)
    extension = source_path.suffix.lower()
    if extension not in SUPPORTED_BOOK_EXTENSIONS:
        shown = extension or "без расширения"
        raise UnsupportedBookFormatError(
            f"Формат {shown} не поддерживается. Выберите FB2, EPUB, MOBI, "
            "AZW/AZW3, TXT/TXTZ, DOCX, ODT, RTF, HTML/HTM/HTMLZ или FBZ."
        )
    return extension


@dataclass
class PreparedBook:
    """FB2-путь и владелец временных данных входной конвертации."""

    source_path: Path
    fb2_path: Path
    source_format: str
    _temporary_directory: Optional[tempfile.TemporaryDirectory] = field(
        default=None,
        repr=False,
    )

    @property
    def converted(self) -> bool:
        return self._temporary_directory is not None

    def cleanup(self) -> None:
        if self._temporary_directory is not None:
            self._temporary_directory.cleanup()
            self._temporary_directory = None

    def __enter__(self) -> "PreparedBook":
        return self

    def __exit__(self, _exc_type, _exc, _traceback) -> None:
        self.cleanup()


class BookInputPreparer:
    """Конвертировать разрешённые форматы в FB2 через системный Calibre."""

    def __init__(
        self,
        executable_finder: Callable[[str], Optional[str]] = shutil.which,
        popen_factory: Callable[..., subprocess.Popen] = subprocess.Popen,
        temporary_directory_factory: Callable[..., tempfile.TemporaryDirectory] = (
            tempfile.TemporaryDirectory
        ),
    ) -> None:
        self._executable_finder = executable_finder
        self._popen_factory = popen_factory
        self._temporary_directory_factory = temporary_directory_factory

    @staticmethod
    def _check_canceled(cancel_event: Optional[threading.Event]) -> None:
        if cancel_event is not None and cancel_event.is_set():
            raise PipelineCanceledError("Обработка отменена пользователем")

    @staticmethod
    def _stderr_excerpt(stderr: str | bytes | None, limit: int = 1200) -> str:
        if isinstance(stderr, bytes):
            stderr = stderr.decode("utf-8", errors="replace")
        compact = " ".join((stderr or "").split())
        if not compact:
            return "Calibre не сообщил подробностей"
        return compact[-limit:]

    def prepare(
        self,
        source_path: Path | str,
        cancel_event: Optional[threading.Event] = None,
    ) -> PreparedBook:
        """Подготовить FB2 и сохранить временные данные за вызывающим кодом."""
        source_path = Path(source_path)
        source_format = detect_book_format(source_path)
        if source_format in NATIVE_BOOK_EXTENSIONS:
            return PreparedBook(source_path, source_path, source_format)

        self._check_canceled(cancel_event)
        executable = self._executable_finder("ebook-convert")
        if executable is None:
            raise CalibreImportError(CALIBRE_REQUIRED_MESSAGE)

        temporary_directory = self._temporary_directory_factory(
            prefix="audiobook-calibre-"
        )
        output_path = Path(temporary_directory.name) / "converted.fb2"
        command = [executable, str(source_path), str(output_path)]
        logger.info(
            "Calibre: %s → FB2 (%s)",
            source_format.removeprefix(".").upper(),
            source_path,
        )

        process: Optional[subprocess.Popen] = None
        try:
            process = self._popen_factory(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                shell=False,
            )
            while True:
                try:
                    _stdout, stderr = process.communicate(timeout=0.1)
                    break
                except subprocess.TimeoutExpired:
                    if cancel_event is None or not cancel_event.is_set():
                        continue
                    process.terminate()
                    try:
                        process.communicate(timeout=2.0)
                    except subprocess.TimeoutExpired:
                        process.kill()
                        process.communicate()
                    raise PipelineCanceledError(
                        "Обработка отменена пользователем"
                    )

            if process.returncode:
                excerpt = self._stderr_excerpt(stderr)
                logger.error(
                    "ebook-convert завершился с кодом %s: %s",
                    process.returncode,
                    excerpt,
                )
                raise CalibreImportError(
                    f"Calibre не смог преобразовать книгу (код "
                    f"{process.returncode}): {excerpt}"
                )
            if not output_path.is_file() or output_path.stat().st_size == 0:
                raise CalibreImportError(
                    "Calibre завершил работу, но не создал корректный FB2-файл"
                )

            self._check_canceled(cancel_event)
            return PreparedBook(
                source_path=source_path,
                fb2_path=output_path,
                source_format=source_format,
                _temporary_directory=temporary_directory,
            )
        except BaseException:
            if process is not None and process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=2.0)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()
            temporary_directory.cleanup()
            raise
