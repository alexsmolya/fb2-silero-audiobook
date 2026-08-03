import asyncio
import queue
import tempfile
import threading
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from audiobook_gui import AudiobookGeneratorGUI
from src.core.fb2_parser import BookMetadata, Chapter, ParsedBook
from src.core.pipeline import AppConfig, Pipeline
from src.core.tts_manager import TTSConfig, TTSManager
from src.utils.exceptions import PipelineCanceledError


class FakeButton:
    def __init__(self):
        self.text = ""
        self.disabled = False

    def configure(self, **kwargs):
        if "text" in kwargs:
            self.text = kwargs["text"]

    def state(self, states):
        for state in states:
            if state == "disabled":
                self.disabled = True
            elif state == "!disabled":
                self.disabled = False


class FakeVar:
    def __init__(self, value):
        self.value = value

    def get(self):
        return self.value


class FakeThread:
    def __init__(self, **kwargs):
        self.started = False

    def start(self):
        self.started = True

    def is_alive(self):
        return self.started


class FakeRoot:
    def __init__(self):
        self.destroyed = False
        self.after_calls = []

    def after(self, delay, callback, *args):
        self.after_calls.append((delay, callback, args))

    def destroy(self):
        self.destroyed = True

    def winfo_exists(self):
        return not self.destroyed


class FakeAssembler:
    def __init__(self):
        self.book_output = None

    def assemble_chapter(self, segments, output_path, cancel_event=None):
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(b"chapter")
        return output_path

    def assemble_book(
        self, chapter_paths, output_path, progress_callback=None,
        cancel_event=None,
    ):
        self.book_output = output_path
        if progress_callback:
            progress_callback(len(chapter_paths), len(chapter_paths))
        output_path.write_bytes(b"book")
        return output_path

    def cleanup_temp_files(self, temp_dir):
        import shutil

        shutil.rmtree(temp_dir)


class CancellationTests(unittest.TestCase):
    def test_cancel_before_work(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            config = AppConfig(
                book_path=base / "book.fb2",
                output_dir=base / "out",
                work_dir=base / "work",
            )
            assembler = FakeAssembler()
            with patch("src.core.pipeline.AudioAssembler", return_value=assembler):
                pipeline = Pipeline(config)
            pipeline.fb2_parser.parse = MagicMock()
            canceled = threading.Event()
            canceled.set()

            with self.assertRaises(PipelineCanceledError):
                asyncio.run(pipeline.run(cancel_event=canceled))

            pipeline.fb2_parser.parse.assert_not_called()
            self.assertFalse(config.work_dir.exists())

    def test_cancel_between_tts_segments(self):
        event = threading.Event()
        synthesized = []

        class Backend:
            async def synthesize_chapter(
                self,
                text_segments,
                comment_segments,
                chapter_dir,
                progress_callback=None,
                detail_callback=None,
            ):
                for index, text in enumerate(text_segments):
                    detail_callback(index + 1, len(text_segments), text, "voice", "fake")
                    synthesized.append(text)
                    progress_callback(index + 1, len(text_segments))
                return chapter_dir

        manager = TTSManager(TTSConfig())
        manager._backend = Backend()

        def cancel_after_first(completed, total):
            event.set()

        with self.assertRaises(PipelineCanceledError):
            asyncio.run(manager.synthesize_chapter(
                ["one", "two"],
                [None, None],
                Path("unused"),
                progress_callback=cancel_after_first,
                cancel_event=event,
            ))

        self.assertEqual(synthesized, ["one"])

    def test_pipeline_without_cancel_signal_keeps_previous_behavior(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            config = AppConfig(
                book_path=base / "book.fb2",
                output_dir=base / "out",
                work_dir=base / "work",
            )
            assembler = FakeAssembler()
            with patch("src.core.pipeline.AudioAssembler", return_value=assembler):
                pipeline = Pipeline(config)
            pipeline.fb2_parser.parse = MagicMock(return_value=ParsedBook(
                metadata=BookMetadata(title="Test", lang="en"),
                chapters=[Chapter(title="One", paragraphs=["Sentence."])],
            ))
            pipeline.sentence_splitter.split = MagicMock(return_value=["Sentence."])

            async def synthesize(**kwargs):
                chapter_dir = kwargs["chapter_dir"]
                chapter_dir.mkdir(parents=True, exist_ok=True)
                (chapter_dir / "seg_000000.mp3").write_bytes(b"segment")
                return chapter_dir

            pipeline.tts_manager.synthesize_chapter = synthesize
            pipeline.checkpoint_manager.load = MagicMock(return_value=None)
            progress = []

            result = asyncio.run(pipeline.run(
                progress_callback=lambda status, value: progress.append((status, value))
            ))

            self.assertEqual(result, config.output_dir / "Test.mp3")
            self.assertTrue(result.is_file())
            self.assertTrue(assembler.book_output.name.endswith(".partial.mp3"))
            self.assertEqual(progress[-1][1], 1.0)

    def test_canceled_gui_is_not_success_and_can_start_again(self):
        gui = AudiobookGeneratorGUI.__new__(AudiobookGeneratorGUI)
        gui.progress = {"value": 73}
        gui.start_button = FakeButton()
        gui.cancel_button = FakeButton()
        gui.open_folder_button = FakeButton()
        gui.pipeline = object()
        gui.worker = object()
        gui.cancel_event = threading.Event()
        gui.worker_done_event = None
        gui.worker_outcome = None
        gui.terminal_handled = False
        gui.cancel_requested = True
        gui.close_after_worker = False
        gui.started_at = 1.0
        gui.last_result_path = Path("old.mp3")
        messages = []
        gui._append_log = messages.append

        gui._handle_event(("canceled",))

        self.assertEqual(messages, ["Обработка отменена пользователем"])
        self.assertNotIn("Готово", " ".join(messages))
        self.assertEqual(gui.progress["value"], 73)
        self.assertFalse(gui.start_button.disabled)
        self.assertTrue(gui.cancel_button.disabled)
        self.assertTrue(gui.open_folder_button.disabled)
        self.assertIsNone(gui.last_result_path)
        self.assertIsNone(gui.worker)

        gui._validate = MagicMock(return_value=(
            Path("book.fb2"), Path("out"), "ru", "edge", "voice"
        ))
        gui.settings = SimpleNamespace(
            book_path="", output_dir="", book_lang="ru", tts_backend="edge",
            main_gender="female", comment_gender="female", use_gpu=False,
            ai_provider="", system_prompt="", comment_frequency=0,
            max_concurrent=1, main_speed=1.0, comment_speed=1.0,
            pause_before_comment=1.0, pause_after_comment=0.7,
            pause_between_sentences=0.3,
        )
        gui.use_gpu_var = FakeVar(False)
        gui.cuda_visible_devices_was_set = False
        gui.initial_cuda_visible_devices = None

        with (
            patch("audiobook_gui.save_settings"),
            patch("audiobook_gui.Pipeline", return_value=MagicMock()),
            patch("audiobook_gui.RunDiagnostics") as diagnostics_class,
            patch("audiobook_gui.threading.Thread", FakeThread),
        ):
            diagnostics_class.return_value.available = False
            diagnostics_class.return_value.warning = None
            gui._start()

        self.assertIsNotNone(gui.worker)
        self.assertTrue(gui.worker.started)
        self.assertEqual(gui.progress["value"], 0)
        self.assertTrue(gui.start_button.disabled)
        self.assertFalse(gui.cancel_button.disabled)

    def test_worker_reports_cancellation_without_success(self):
        gui = AudiobookGeneratorGUI.__new__(AudiobookGeneratorGUI)
        gui.events = queue.Queue()
        gui.cancel_event = threading.Event()
        gui.worker_done_event = None
        gui.worker_outcome = None
        gui.terminal_handled = False

        class CanceledPipeline:
            async def run(self, **kwargs):
                raise PipelineCanceledError("expected cancellation")

        outcome = gui._run_pipeline(CanceledPipeline())

        self.assertEqual(outcome, ("canceled",))
        self.assertTrue(gui.events.empty())

    def test_duplicate_terminal_events_are_ignored(self):
        gui = AudiobookGeneratorGUI.__new__(AudiobookGeneratorGUI)
        gui.progress = {"value": 40}
        gui.start_button = FakeButton()
        gui.cancel_button = FakeButton()
        gui.open_folder_button = FakeButton()
        gui.pipeline = object()
        gui.worker = object()
        gui.cancel_event = threading.Event()
        gui.worker_done_event = None
        gui.worker_outcome = None
        gui.terminal_handled = False
        gui.cancel_requested = True
        gui.close_after_worker = False
        gui.started_at = 1.0
        gui.last_result_path = None
        messages = []
        gui._append_log = messages.append

        gui._handle_event(("canceled",))
        gui._handle_event(("error", "late error", "traceback"))
        gui._handle_event(("success", Path("late.mp3")))

        self.assertEqual(messages, ["Обработка отменена пользователем"])
        self.assertEqual(gui.progress["value"], 40)

    def test_close_waits_for_active_worker(self):
        gui = AudiobookGeneratorGUI.__new__(AudiobookGeneratorGUI)
        gui.root = FakeRoot()
        gui.progress = {"value": 35}
        gui.start_button = FakeButton()
        gui.cancel_button = FakeButton()
        gui.open_folder_button = FakeButton()
        gui.events = queue.Queue()
        gui.cancel_event = threading.Event()
        gui.worker_done_event = threading.Event()
        gui.worker_outcome = None
        gui.terminal_handled = False
        gui.cancel_requested = False
        gui.close_after_worker = False
        gui.started_at = 1.0
        gui.last_result_path = None
        messages = []
        gui._append_log = messages.append
        release_worker = threading.Event()

        class Pipeline:
            def cancel(self):
                release_worker.set()

        gui.pipeline = Pipeline()

        def run_pipeline(_pipeline):
            release_worker.wait(timeout=2.0)
            return ("canceled",)

        gui._run_pipeline = run_pipeline
        gui.worker = threading.Thread(
            target=gui._worker_entry,
            args=(gui.pipeline, gui.worker_done_event),
        )
        gui.worker.start()

        with patch("audiobook_gui.messagebox.askyesno", return_value=True):
            gui._on_close()

        self.assertFalse(gui.root.destroyed)
        self.assertTrue(gui.close_after_worker)
        gui.worker.join(timeout=2.0)
        self.assertFalse(gui.worker.is_alive())

        closed = gui._poll_worker_completion()

        self.assertTrue(closed)
        self.assertTrue(gui.root.destroyed)
        self.assertEqual(messages, ["Обработка отменена пользователем"])


if __name__ == "__main__":
    unittest.main()
