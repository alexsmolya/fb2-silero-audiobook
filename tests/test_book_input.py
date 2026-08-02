"""Тесты подготовки входных книг через системный Calibre."""

from __future__ import annotations

import asyncio
import shutil
import subprocess
import tempfile
import threading
import unittest
from pathlib import Path
from unittest.mock import AsyncMock

from audiobook_gui import BOOK_FILETYPES, AudiobookGeneratorGUI
from src.core.book_input import (
    CALIBRE_BOOK_EXTENSIONS,
    CALIBRE_REQUIRED_MESSAGE,
    SUPPORTED_BOOK_EXTENSIONS,
    BookInputPreparer,
    CalibreImportError,
    PreparedBook,
    UnsupportedBookFormatError,
    detect_book_format,
)
from src.core.fb2_parser import FB2Parser
from src.core.pipeline import AppConfig, Pipeline
from src.utils.exceptions import PipelineCanceledError


MINIMAL_FB2 = """<?xml version="1.0" encoding="utf-8"?>
<FictionBook xmlns="http://www.gribuser.ru/xml/fictionbook/2.0">
  <description><title-info>
    <book-title>Название из метаданных</book-title>
    <lang>ru</lang>
  </title-info></description>
  <body><section><title><p>Глава</p></title>
    <p>Первый русский абзац.</p>
    <p>Второй русский абзац.</p>
  </section></body>
</FictionBook>
"""


class SuccessfulProcess:
    def __init__(self, command, **kwargs):
        self.command = command
        self.kwargs = kwargs
        self.returncode = 0
        Path(command[2]).write_text(MINIMAL_FB2, encoding="utf-8")

    def communicate(self, timeout=None):
        return "", ""

    def poll(self):
        return self.returncode


class FailedProcess(SuccessfulProcess):
    def __init__(self, command, **kwargs):
        self.command = command
        self.kwargs = kwargs
        self.returncode = 7

    def communicate(self, timeout=None):
        return "", "подробная диагностическая ошибка Calibre"


class CancelingProcess:
    def __init__(self, command, cancel_event, require_kill):
        self.command = command
        self.cancel_event = cancel_event
        self.require_kill = require_kill
        self.returncode = None
        self.terminated = False
        self.killed = False
        self.calls = 0

    def communicate(self, timeout=None):
        self.calls += 1
        if self.calls == 1:
            self.cancel_event.set()
            raise subprocess.TimeoutExpired(self.command, timeout)
        if self.require_kill and not self.killed:
            raise subprocess.TimeoutExpired(self.command, timeout)
        self.returncode = -9 if self.killed else -15
        return "", ""

    def terminate(self):
        self.terminated = True

    def kill(self):
        self.killed = True

    def poll(self):
        return self.returncode

    def wait(self, timeout=None):
        self.returncode = -9 if self.killed else -15
        return self.returncode


class BookInputTests(unittest.TestCase):
    def _recording_temp_factory(self, created):
        def factory(**kwargs):
            temporary_directory = tempfile.TemporaryDirectory(**kwargs)
            created.append(Path(temporary_directory.name))
            return temporary_directory

        return factory

    def test_fb2_passes_without_calibre(self):
        def unexpected_lookup(_name):
            raise AssertionError("Для FB2 нельзя искать ebook-convert")

        preparer = BookInputPreparer(executable_finder=unexpected_lookup)
        source = Path("Книга с пробелами.fb2")

        prepared = preparer.prepare(source)

        self.assertEqual(prepared.fb2_path, source)
        self.assertFalse(prepared.converted)

    def test_all_allowed_extensions_are_recognized(self):
        expected = {
            ".fb2", ".epub", ".mobi", ".azw", ".azw3", ".txt",
            ".txtz", ".docx", ".odt", ".rtf", ".html", ".htm",
            ".htmlz", ".fbz",
        }
        self.assertEqual(SUPPORTED_BOOK_EXTENSIONS, expected)
        self.assertEqual(CALIBRE_BOOK_EXTENSIONS, expected - {".fb2"})
        for extension in expected:
            with self.subTest(extension=extension):
                self.assertEqual(detect_book_format(f"book{extension}"), extension)

    def test_extension_case_is_ignored_and_kepub_is_epub(self):
        self.assertEqual(detect_book_format("BOOK.EPUB"), ".epub")
        self.assertEqual(detect_book_format("book.kepub.epub"), ".epub")
        self.assertEqual(detect_book_format("BOOK.FB2"), ".fb2")

    def test_gui_file_dialog_has_required_groups_without_unsupported_formats(self):
        labels = [label for label, _patterns in BOOK_FILETYPES]
        self.assertEqual(labels, [
            "Поддерживаемые книги",
            "FB2",
            "EPUB",
            "MOBI / AZW",
            "Текст и документы",
            "HTML",
            "Все файлы",
        ])
        patterns = {
            pattern
            for _label, group_patterns in BOOK_FILETYPES
            for pattern in group_patterns
        }
        patterns = {pattern.lower() for pattern in patterns}
        for extension in SUPPORTED_BOOK_EXTENSIONS:
            self.assertIn(f"*{extension}", patterns)
        for extension in (".pdf", ".djvu", ".cbz", ".cbr", ".azw4", ".doc"):
            self.assertNotIn(f"*{extension}", patterns)

    def test_unsupported_formats_are_rejected(self):
        extensions = (
            ".pdf", ".djvu", ".cbz", ".cbr", ".cb7", ".azw4",
            ".doc", ".zip", ".chm", ".lit", ".pdb", "",
        )
        for extension in extensions:
            with self.subTest(extension=extension):
                with self.assertRaises(UnsupportedBookFormatError):
                    detect_book_format(f"book{extension}")

    def test_missing_ebook_convert_only_breaks_non_native_formats(self):
        preparer = BookInputPreparer(executable_finder=lambda _name: None)
        self.assertEqual(preparer.prepare("book.fb2").fb2_path, Path("book.fb2"))

        with self.assertRaisesRegex(CalibreImportError, "sudo pacman -S calibre"):
            preparer.prepare("book.epub")
        self.assertIn("требуется Calibre", CALIBRE_REQUIRED_MESSAGE)

    def test_command_is_argument_list_without_shell_and_handles_unicode(self):
        calls = []

        def popen(command, **kwargs):
            process = SuccessfulProcess(command, **kwargs)
            calls.append(process)
            return process

        preparer = BookInputPreparer(
            executable_finder=lambda _name: "/usr/bin/ebook-convert",
            popen_factory=popen,
        )
        source = Path("/tmp/Русская книга с пробелами.epub")
        prepared = preparer.prepare(source)
        try:
            self.assertEqual(
                calls[0].command,
                ["/usr/bin/ebook-convert", str(source), str(prepared.fb2_path)],
            )
            self.assertIsInstance(calls[0].command, list)
            self.assertIs(calls[0].kwargs["shell"], False)
        finally:
            prepared.cleanup()

    def test_calibre_error_is_bounded_and_temporary_directory_is_removed(self):
        created = []
        preparer = BookInputPreparer(
            executable_finder=lambda _name: "/usr/bin/ebook-convert",
            popen_factory=FailedProcess,
            temporary_directory_factory=self._recording_temp_factory(created),
        )

        with self.assertRaisesRegex(
            CalibreImportError,
            "подробная диагностическая ошибка Calibre",
        ):
            preparer.prepare("broken.epub")

        self.assertEqual(len(created), 1)
        self.assertFalse(created[0].exists())

    def test_calibre_error_is_reported_as_regular_gui_error(self):
        gui = AudiobookGeneratorGUI.__new__(AudiobookGeneratorGUI)
        gui.cancel_event = threading.Event()

        class FailedPipeline:
            async def run(self, **_kwargs):
                raise CalibreImportError("Краткая ошибка Calibre: stderr")

        outcome = gui._run_pipeline(FailedPipeline())

        self.assertEqual(outcome[0], "error")
        self.assertEqual(outcome[1], "Краткая ошибка Calibre: stderr")
        self.assertNotIn("success", outcome)

    def test_temporary_directory_is_removed_after_success_cleanup(self):
        created = []
        preparer = BookInputPreparer(
            executable_finder=lambda _name: "/usr/bin/ebook-convert",
            popen_factory=SuccessfulProcess,
            temporary_directory_factory=self._recording_temp_factory(created),
        )

        prepared = preparer.prepare("book.epub")
        self.assertTrue(prepared.fb2_path.is_file())
        self.assertTrue(created[0].exists())
        prepared.cleanup()
        self.assertFalse(created[0].exists())

    def test_cancel_terminates_process_and_removes_temporary_directory(self):
        self._assert_cancel_cleanup(require_kill=False)

    def test_cancel_kills_unresponsive_process_and_removes_temporary_directory(self):
        self._assert_cancel_cleanup(require_kill=True)

    def _assert_cancel_cleanup(self, require_kill):
        created = []
        cancel_event = threading.Event()
        processes = []

        def popen(command, **_kwargs):
            process = CancelingProcess(command, cancel_event, require_kill)
            processes.append(process)
            return process

        preparer = BookInputPreparer(
            executable_finder=lambda _name: "/usr/bin/ebook-convert",
            popen_factory=popen,
            temporary_directory_factory=self._recording_temp_factory(created),
        )

        with self.assertRaises(PipelineCanceledError):
            preparer.prepare("book.epub", cancel_event=cancel_event)

        self.assertTrue(processes[0].terminated)
        self.assertEqual(processes[0].killed, require_kill)
        self.assertFalse(created[0].exists())

    def test_converted_fb2_lives_through_pipeline_and_metadata_names_result(self):
        with tempfile.TemporaryDirectory() as base_dir:
            base = Path(base_dir)
            converted_dir = tempfile.TemporaryDirectory(
                prefix="converted-",
                dir=base,
            )
            converted_path = Path(converted_dir.name) / "random-name.fb2"
            converted_path.write_text(MINIMAL_FB2, encoding="utf-8")
            prepared = PreparedBook(
                source_path=base / "source.epub",
                fb2_path=converted_path,
                source_format=".epub",
                _temporary_directory=converted_dir,
            )

            class Preparer:
                def prepare(self, _path, cancel_event=None):
                    self.cancel_event = cancel_event
                    return prepared

            config = AppConfig(
                book_path=base / "source.epub",
                output_dir=base / "out",
                work_dir=base / "work",
            )
            pipeline = Pipeline(config)
            pipeline.book_input_preparer = Preparer()
            pipeline.tts_manager.synthesize_chapter = AsyncMock()

            async def assemble_chapter(*_args, **_kwargs):
                chapter_path = pipeline._temp_dir / "chapter.wav"
                chapter_path.write_bytes(b"chapter")
                return chapter_path

            pipeline._assemble_chapter_audio = assemble_chapter

            def assemble_book(
                _chapters, output_path, progress_callback=None,
                cancel_event=None,
            ):
                self.assertTrue(converted_path.is_file())
                self.assertIsNotNone(cancel_event)
                if progress_callback:
                    progress_callback(len(_chapters), len(_chapters))
                output_path.write_bytes(b"book")
                return output_path

            pipeline.audio_assembler.assemble_book = assemble_book

            messages = []
            result = asyncio.run(pipeline.run(
                cancel_event=threading.Event(),
                progress_callback=lambda message, _progress: messages.append(message),
            ))

            self.assertEqual(result.name, "Название из метаданных.mp3")
            self.assertTrue(result.is_file())
            self.assertFalse(converted_path.exists())
            self.assertFalse(Path(converted_dir.name).exists())
            self.assertIn(
                "Подготовка книги: EPUB → FB2 через Calibre…",
                messages,
            )
            self.assertIn("Книга подготовлена, запуск обработки…", messages)


@unittest.skipUnless(shutil.which("ebook-convert"), "Calibre не установлен")
class CalibreIntegrationTests(unittest.TestCase):
    def test_txt_to_epub_to_fb2_preserves_russian_text_and_metadata(self):
        ebook_convert = shutil.which("ebook-convert")
        with tempfile.TemporaryDirectory() as base_dir:
            base = Path(base_dir)
            source = base / "Русская книга.txt"
            epub = base / "Русская книга.epub"
            source.write_text(
                "Глава первая\n\nПервый абзац по-русски.\n\n"
                "Второй абзац сохраняет кириллицу.",
                encoding="utf-8",
            )
            subprocess.run(
                [
                    ebook_convert,
                    str(source),
                    str(epub),
                    "--title",
                    "Интеграционная книга",
                    "--authors",
                    "Тестовый Автор",
                ],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            prepared = BookInputPreparer().prepare(epub)
            try:
                book = FB2Parser().parse(prepared.fb2_path)
                text = "\n".join(
                    paragraph
                    for chapter in book.chapters
                    for paragraph in chapter.paragraphs
                )
                self.assertEqual(book.metadata.title, "Интеграционная книга")
                self.assertIn("Первый абзац по-русски", text)
                self.assertIn("Второй абзац сохраняет кириллицу", text)
                self.assertGreaterEqual(len(book.chapters), 1)
                self.assertTrue(prepared.fb2_path.is_file())
            finally:
                converted_path = prepared.fb2_path
                prepared.cleanup()
            self.assertFalse(converted_path.exists())


if __name__ == "__main__":
    unittest.main()
