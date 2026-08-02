"""Тесты глобального монотонного прогресса обработки книги."""

from __future__ import annotations

import asyncio
import queue
import tempfile
import threading
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

from audiobook_gui import AudiobookGeneratorGUI
from src.core.book_progress import BookProgressTracker
from src.core.checkpoint_manager import Checkpoint
from src.core.fb2_parser import BookMetadata, Chapter, ParsedBook
from src.core.pipeline import AppConfig, Pipeline
from src.utils.exceptions import PipelineCanceledError


class FakeAssembler:
    def assemble_chapter(self, _segments, output_path, cancel_event=None):
        if cancel_event and cancel_event.is_set():
            raise PipelineCanceledError("canceled")
        output_path.write_bytes(b"chapter")
        return output_path

    def assemble_book(
        self, chapter_paths, output_path, progress_callback=None,
        cancel_event=None,
    ):
        for index, _path in enumerate(chapter_paths, start=1):
            if cancel_event and cancel_event.is_set():
                raise PipelineCanceledError("canceled")
            if progress_callback:
                progress_callback(index, len(chapter_paths))
        output_path.write_bytes(b"final mp3")
        return output_path

    @staticmethod
    def cleanup_temp_files(temp_dir):
        import shutil
        shutil.rmtree(temp_dir)


class FakeTTS:
    def __init__(self, failure: str | None = None):
        self.failure = failure

    async def synthesize_chapter(
        self, text_segments, comment_segments, chapter_dir,
        progress_callback=None, detail_callback=None, cancel_event=None,
    ):
        chapter_dir.mkdir(parents=True, exist_ok=True)
        segments = []
        for index, text in enumerate(text_segments):
            segments.append(text)
            if index < len(comment_segments) and comment_segments[index]:
                segments.append(comment_segments[index])
        for index, text in enumerate(segments, start=1):
            if detail_callback:
                detail_callback(index, len(segments), text, "voice", "mock")
            (chapter_dir / f"seg_{index:06d}.mp3").write_bytes(b"segment")
            if progress_callback:
                progress_callback(index, len(segments))
            if self.failure == "cancel" and index == 1:
                raise PipelineCanceledError("canceled")
            if self.failure == "error" and index == 1:
                raise RuntimeError("tts failed")
        return chapter_dir


class GlobalProgressTests(unittest.TestCase):
    def test_values_are_clamped_and_never_decrease(self):
        values = []
        tracker = BookProgressTracker(lambda _message, value: values.append(value))
        tracker.publish("negative", -1)
        tracker.publish("forward", 0.6)
        tracker.publish("backward", 0.2)
        tracker.publish("premature", 2)

        self.assertEqual(values[0], 0.0)
        self.assertEqual(values[1], values[2])
        self.assertEqual(values[-1], tracker.FINAL_ASSEMBLY_END)
        self.assertTrue(all(0.0 <= value <= 1.0 for value in values))
        self.assertEqual(values, sorted(values))

    def test_chapter_weight_uses_source_character_count(self):
        tracker = BookProgressTracker()
        tracker.set_chapters(["x" * 10, "x" * 100])
        small_start, small_end = tracker.chapter_bounds(0)
        large_start, large_end = tracker.chapter_bounds(1)

        self.assertGreater(large_end - large_start, small_end - small_start)
        self.assertAlmostEqual(small_end, large_start)

    def test_tts_progress_uses_completed_fragment_character_count(self):
        tracker = BookProgressTracker()
        tracker.set_chapters(["x" * 110])
        after_short = tracker.chapter_tts(0, 1, 2, ["x" * 10, "x" * 100])
        after_long = tracker.chapter_tts(0, 2, 2, ["x" * 10, "x" * 100])
        start, end = tracker.chapter_bounds(0)

        self.assertLess(after_short - start, (after_long - start) / 2)
        self.assertLess(after_long, end)

    def test_empty_book_and_chapters_have_safe_fallbacks(self):
        tracker = BookProgressTracker()
        tracker.set_chapters([])
        self.assertLess(tracker.chapter_tts(0, 0, 0), 1.0)
        tracker.set_chapters(["", ""])
        self.assertAlmostEqual(
            tracker.chapter_bounds(0)[1] - tracker.chapter_bounds(0)[0],
            tracker.chapter_bounds(1)[1] - tracker.chapter_bounds(1)[0],
        )

    def test_calibre_and_final_assembly_stay_in_reserved_ranges(self):
        tracker = BookProgressTracker()
        self.assertEqual(tracker.PREPARATION_END, 0.03)
        self.assertEqual(tracker.PARSING_END, 0.05)
        self.assertEqual(tracker.CHAPTERS_END, 0.92)
        self.assertLess(tracker.final_assembly(1, 1), 0.99)
        self.assertEqual(tracker.publish("verify", 0.99), 0.99)
        self.assertEqual(tracker.complete("done"), 1.0)

    def _make_pipeline(
        self, base: Path, failure: str | None = None,
        checkpoint: Checkpoint | None = None,
    ) -> Pipeline:
        source = base / "book.fb2"
        source.write_text("<mock/>", encoding="utf-8")
        pipeline = Pipeline(AppConfig(
            book_path=source,
            output_dir=base / "out",
            work_dir=base / "work",
        ))
        pipeline.fb2_parser.parse = MagicMock(return_value=ParsedBook(
            metadata=BookMetadata(title="Progress", lang="en"),
            chapters=[
                Chapter(title="Short", paragraphs=["a" * 10]),
                Chapter(title="Large", paragraphs=["b" * 100]),
            ],
        ))
        pipeline.sentence_splitter.split = MagicMock(
            side_effect=lambda text, _lang: [text[: max(1, len(text) // 3)],
                                             text[max(1, len(text) // 3):]]
        )
        pipeline.tts_manager = FakeTTS(failure)
        pipeline.audio_assembler = FakeAssembler()
        pipeline.checkpoint_manager.load = MagicMock(return_value=checkpoint)
        return pipeline

    def test_pipeline_is_monotonic_across_different_sized_chapters(self):
        with tempfile.TemporaryDirectory() as directory:
            pipeline = self._make_pipeline(Path(directory))
            events = []
            result = asyncio.run(pipeline.run(
                progress_callback=lambda message, value: events.append(
                    (message, value)
                )
            ))
            self.assertTrue(result.is_file())

        values = [value for _message, value in events]
        self.assertEqual(values[0], 0.0)
        self.assertEqual(values[-1], 1.0)
        self.assertEqual(values, sorted(values))
        first_complete = next(
            value for message, value in events if "Глава 1/2: обработана" in message
        )
        second_start = next(
            value for message, value in events
            if "Глава 2/2: разбиение" in message
        )
        self.assertEqual(first_complete, second_start)
        self.assertLess(first_complete - 0.05, 0.2)

    def test_calibre_import_is_confined_to_initial_range(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            pipeline = self._make_pipeline(base)
            source = base / "book.epub"
            converted = base / "converted.fb2"
            source.write_bytes(b"epub")
            converted.write_bytes(b"fb2")
            pipeline.config.book_path = source
            pipeline.book_input_preparer.prepare = MagicMock(return_value=SimpleNamespace(
                converted=True,
                fb2_path=converted,
                cleanup=lambda: None,
            ))
            events = []
            asyncio.run(pipeline.run(
                progress_callback=lambda message, value: events.append(
                    (message, value)
                )
            ))

        parsing_index = next(
            index for index, (message, _value) in enumerate(events)
            if message == "Парсинг FB2-файла..."
        )
        import_values = [value for _message, value in events[:parsing_index]]
        self.assertTrue(import_values)
        self.assertLessEqual(max(import_values), BookProgressTracker.PREPARATION_END)

    def test_cancellation_and_error_keep_last_value_below_100(self):
        for failure, exception in (
            ("cancel", PipelineCanceledError), ("error", RuntimeError),
        ):
            with self.subTest(failure=failure), tempfile.TemporaryDirectory() as directory:
                pipeline = self._make_pipeline(Path(directory), failure=failure)
                values = []
                with self.assertRaises(exception):
                    asyncio.run(pipeline.run(
                        progress_callback=lambda _message, value: values.append(value)
                    ))
                self.assertEqual(values, sorted(values))
                self.assertGreater(values[-1], 0.0)
                self.assertLess(values[-1], 1.0)

    def test_failed_final_assembly_never_reaches_100(self):
        class FailingAssembler(FakeAssembler):
            def assemble_book(
                self, chapter_paths, output_path, progress_callback=None,
                cancel_event=None,
            ):
                if progress_callback:
                    progress_callback(len(chapter_paths), len(chapter_paths))
                raise RuntimeError("assembly failed")

        with tempfile.TemporaryDirectory() as directory:
            pipeline = self._make_pipeline(Path(directory))
            pipeline.audio_assembler = FailingAssembler()
            values = []
            with self.assertRaisesRegex(RuntimeError, "assembly failed"):
                asyncio.run(pipeline.run(
                    progress_callback=lambda _message, value: values.append(value)
                ))

        self.assertEqual(values, sorted(values))
        self.assertLess(values[-1], 1.0)

    def test_resume_reports_completed_chapter_weight_immediately(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            source = base / "book.fb2"
            checkpoint = Checkpoint(
                book_path=str(source), last_completed_chapter=0,
                total_chapters=2, config_hash="unused", timestamp=0,
            )
            pipeline = self._make_pipeline(base, checkpoint=checkpoint)
            events = []
            asyncio.run(pipeline.run(
                progress_callback=lambda message, value: events.append(
                    (message, value)
                )
            ))
            resume_value = next(
                value for message, value in events if message.startswith("Восстановление")
            )
            self.assertGreater(resume_value, BookProgressTracker.PARSING_END)

    def test_gui_progress_is_monotonic_and_terminal_failures_preserve_it(self):
        gui = AudiobookGeneratorGUI.__new__(AudiobookGeneratorGUI)
        gui.progress = {"value": 0}
        gui._shown_progress = 0.0
        gui._append_log = lambda _message: None
        gui.terminal_handled = False

        gui._handle_event(("progress", "first", 0.7))
        gui._handle_event(("progress", "late old event", 0.2))
        self.assertEqual(gui.progress["value"], 70)

        gui.start_button = MagicMock()
        gui.cancel_button = MagicMock()
        gui.open_folder_button = MagicMock()
        gui.pipeline = object()
        gui.worker = object()
        gui.cancel_event = threading.Event()
        gui.worker_done_event = None
        gui.worker_outcome = None
        gui.cancel_requested = False
        gui.close_after_worker = False
        gui.started_at = 1.0
        gui.last_result_path = None
        gui._handle_event(("error", "failure", "traceback"))
        self.assertEqual(gui.progress["value"], 70)

    def test_gui_deduplicates_only_consecutive_status_log_lines(self):
        gui = AudiobookGeneratorGUI.__new__(AudiobookGeneratorGUI)
        gui.progress = {"value": 0}
        gui._shown_progress = 0.0
        gui._last_logged_worker_status = None
        gui.terminal_handled = False
        messages = []
        gui._append_log = messages.append

        for value in (0.92, 0.94, 0.96):
            gui._handle_event((
                "progress", "Склейка всех глав в аудиокнигу...", value,
            ))

        self.assertEqual(gui.progress["value"], 96)
        self.assertEqual(messages, ["Склейка всех глав в аудиокнигу..."])

        gui._reset_progress_state()
        messages.clear()
        statuses = (
            "Склейка",
            "Склейка",
            "Проверка",
            "Склейка",
        )
        for index, status in enumerate(statuses, start=1):
            gui._handle_event(("progress", status, index / 10))
        self.assertEqual(messages, ["Склейка", "Проверка", "Склейка"])

        gui._reset_progress_state()
        messages.clear()
        gui._handle_event(("progress", "Синтез речи 1/2...", 0.2))
        gui._handle_event(("progress", "Синтез речи 2/2...", 0.3))
        self.assertEqual(
            messages,
            ["Синтез речи 1/2...", "Синтез речи 2/2..."],
        )

    def test_gui_new_run_reset_allows_same_status_again(self):
        gui = AudiobookGeneratorGUI.__new__(AudiobookGeneratorGUI)
        gui.progress = {"value": 55}
        gui._shown_progress = 55.0
        gui._last_logged_worker_status = "Подготовка входной книги..."
        gui.terminal_handled = False
        messages = []
        gui._append_log = messages.append

        gui._reset_progress_state()
        gui._handle_event(("progress", "Подготовка входной книги...", 0.0))

        self.assertEqual(gui.progress["value"], 0)
        self.assertEqual(messages, ["Подготовка входной книги..."])

    def test_gui_terminal_messages_are_never_deduplicated(self):
        def make_gui():
            gui = AudiobookGeneratorGUI.__new__(AudiobookGeneratorGUI)
            gui.progress = {"value": 80}
            gui._shown_progress = 80.0
            gui._last_logged_worker_status = "Ошибка: failure"
            gui.start_button = MagicMock()
            gui.cancel_button = MagicMock()
            gui.open_folder_button = MagicMock()
            gui.pipeline = object()
            gui.worker = object()
            gui.cancel_event = threading.Event()
            gui.worker_done_event = None
            gui.worker_outcome = None
            gui.terminal_handled = False
            gui.cancel_requested = False
            gui.close_after_worker = False
            gui.started_at = None
            gui.last_result_path = None
            messages = []
            gui._append_log = messages.append
            return gui, messages

        with tempfile.TemporaryDirectory() as directory:
            result = Path(directory) / "result.mp3"
            result.write_bytes(b"mp3")
            success_gui, success_messages = make_gui()
            success_gui._handle_event(("success", result))
            self.assertTrue(success_messages[0].startswith("Готово за "))

        canceled_gui, canceled_messages = make_gui()
        canceled_gui._handle_event(("canceled",))
        self.assertEqual(canceled_messages, ["Обработка отменена пользователем"])

        error_gui, error_messages = make_gui()
        error_gui._handle_event(("error", "failure", "traceback"))
        self.assertEqual(error_messages, ["Ошибка: failure", "traceback"])

    def test_gui_callback_and_detail_events_keep_queue_contract(self):
        with tempfile.TemporaryDirectory() as directory:
            result = Path(directory) / "result.mp3"
            result.write_bytes(b"mp3")
            gui = AudiobookGeneratorGUI.__new__(AudiobookGeneratorGUI)
            gui.events = queue.Queue()
            gui.cancel_event = threading.Event()

            class QueuePipeline:
                async def run(self, progress_callback, detail_callback, **_kwargs):
                    progress_callback("global", 0.4)
                    detail_callback(1, 2, "text", "voice", "mock")
                    return result

            outcome = gui._run_pipeline(QueuePipeline())
            queued = [gui.events.get_nowait(), gui.events.get_nowait()]

        self.assertEqual(outcome, ("success", result))
        self.assertEqual(queued[0], ("progress", "global", 0.4))
        self.assertEqual(queued[1][0], "detail")


if __name__ == "__main__":
    unittest.main()
