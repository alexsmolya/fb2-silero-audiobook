"""Тесты JSONL-диагностики запуска без реального TTS и домашнего каталога."""

from __future__ import annotations

import asyncio
import fcntl
import json
import os
import subprocess
import tempfile
import threading
import time
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

from audiobook_gui import AudiobookGeneratorGUI
from src.core.run_diagnostics import (
    DiagnosticsLimits,
    LOG_PREFIX,
    RunDiagnostics,
    safe_book_slug,
    state_logs_directory,
)
from src.core.tts_manager import TTSConfig, TTSManager
from src.core.tts_silero import SileroTTSManager
from src.core.audio_assembler import AudioAssembler
from src.utils.exceptions import PipelineCanceledError
from tests import test_global_progress as global_progress_tests


class RunDiagnosticsTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.base = Path(self.temporary_directory.name)
        self.logs = self.base / "state" / "fb2-silero-audiobook" / "logs"
        self.book = self.base / "Книга опасная.fb2"
        self.book.write_text("book", encoding="utf-8")
        self.patches = (
            patch("src.core.run_diagnostics._gpu_model", return_value=None),
            patch("src.core.run_diagnostics._torch_info", return_value={
                "pytorch_version": "test",
                "cuda_build_version": None,
                "cuda_available": False,
            }),
        )
        for active_patch in self.patches:
            active_patch.start()

    def tearDown(self):
        for active_patch in reversed(self.patches):
            active_patch.stop()
        self.temporary_directory.cleanup()

    def make_diagnostics(self, **kwargs):
        return RunDiagnostics(
            self.book,
            {
                "backend": "mock",
                "voice": "voice",
                "language": "ru",
                "device": "cpu",
            },
            logs_dir=kwargs.pop("logs_dir", self.logs),
            sample_interval=kwargs.pop("sample_interval", 0.02),
            **kwargs,
        )

    @staticmethod
    def read_events(path: Path):
        return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]

    def test_state_directory_uses_xdg_then_home_fallback(self):
        self.assertEqual(
            state_logs_directory(
                env={"XDG_STATE_HOME": str(self.base / "custom")},
                home=self.base / "ignored",
            ),
            self.base / "custom" / "fb2-silero-audiobook" / "logs",
        )
        self.assertEqual(
            state_logs_directory(env={}, home=self.base / "home"),
            self.base / "home/.local/state/fb2-silero-audiobook/logs",
        )

    def test_safe_unique_cyrillic_name_cannot_escape_directory(self):
        first = self.make_diagnostics()
        second = self.make_diagnostics()
        self.assertTrue(first.part_path.is_relative_to(self.logs))
        self.assertTrue(second.part_path.is_relative_to(self.logs))
        self.assertNotEqual(first.part_path, second.part_path)
        self.assertIn("Книга", first.part_path.name)
        self.assertNotIn("..", first.part_path.name)
        self.assertNotIn("/", first.part_path.name)
        malicious = safe_book_slug("../../Каталог\\секрет\x00:*?")
        self.assertNotIn("..", malicious)
        self.assertNotIn("/", malicious)
        self.assertNotIn("\\", malicious)
        first.finalize("canceled")
        second.finalize("canceled")

    def test_part_creation_and_atomic_success_finalization(self):
        diagnostics = self.make_diagnostics()
        self.assertTrue(diagnostics.logs_dir.is_dir())
        self.assertTrue(diagnostics.part_path.is_file())
        self.assertFalse(diagnostics.final_path.exists())
        result = diagnostics.finalize("success")
        self.assertEqual(result, diagnostics.final_path)
        self.assertFalse(diagnostics.part_path.exists())
        self.assertTrue(diagnostics.final_path.is_file())

    def test_atomic_replace_happens_while_part_lock_is_still_held(self):
        observed = []

        def replace_while_locked(source, target):
            observed.append((source, target, diagnostics._stream.closed))
            os.replace(source, target)

        diagnostics = self.make_diagnostics(replace=replace_while_locked)
        diagnostics.finalize("success")
        self.assertEqual(observed, [
            (diagnostics.part_path, diagnostics.final_path, False),
        ])

    def test_owner_base_exception_releases_waiter_stream_and_file_lock(self):
        diagnostics = self.make_diagnostics()
        entered = threading.Event()
        release = threading.Event()
        owner_errors = []
        waiter_results = []

        def interrupted_stop():
            entered.set()
            self.assertTrue(release.wait(timeout=2))
            raise KeyboardInterrupt()

        diagnostics.stop_sampler = interrupted_stop

        def owner():
            try:
                diagnostics.finalize("error")
            except BaseException as exc:
                owner_errors.append(type(exc))

        owner_thread = threading.Thread(target=owner)
        owner_thread.start()
        self.assertTrue(entered.wait(timeout=2))
        waiter_thread = threading.Thread(
            target=lambda: waiter_results.append(diagnostics.finalize("error")),
        )
        waiter_thread.start()
        release.set()
        owner_thread.join(timeout=2)
        waiter_thread.join(timeout=2)

        self.assertFalse(owner_thread.is_alive())
        self.assertFalse(waiter_thread.is_alive())
        self.assertEqual(owner_errors, [KeyboardInterrupt])
        self.assertEqual(waiter_results, [None])
        self.assertTrue(diagnostics._finalized.is_set())
        self.assertTrue(diagnostics._closed)
        self.assertFalse(diagnostics._finalizing)
        self.assertIsNone(diagnostics._stream)

        with diagnostics.part_path.open("r+", encoding="utf-8") as stream:
            fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            fcntl.flock(stream.fileno(), fcntl.LOCK_UN)

    def test_nvml_base_exception_still_completes_finalizer_state(self):
        diagnostics = self.make_diagnostics()
        diagnostics._nvml_module = MagicMock()
        diagnostics._nvml_module.nvmlShutdown.side_effect = SystemExit(7)
        diagnostics._nvml_handle = object()
        with self.assertRaises(SystemExit):
            diagnostics.finalize("error")
        self.assertTrue(diagnostics._finalized.is_set())
        self.assertTrue(diagnostics._closed)
        self.assertFalse(diagnostics._finalizing)
        self.assertIsNone(diagnostics._stream)
        self.assertIsNone(diagnostics.finalize("error"))

    def test_replace_exception_is_fail_open_and_releases_lock(self):
        diagnostics = self.make_diagnostics(
            replace=MagicMock(side_effect=OSError("replace failed")),
        )
        self.assertIsNone(diagnostics.finalize("success"))
        self.assertTrue(diagnostics._finalized.is_set())
        self.assertTrue(diagnostics._closed)
        self.assertIsNone(diagnostics._stream)
        self.assertTrue(diagnostics.part_path.exists())
        with diagnostics.part_path.open("r+", encoding="utf-8") as stream:
            fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            fcntl.flock(stream.fileno(), fcntl.LOCK_UN)

    def test_old_part_is_recovered_as_incomplete(self):
        self.logs.mkdir(parents=True)
        stale = self.logs / f"{LOG_PREFIX}2026-01-01_00-00-00_old_deadbeef.jsonl.part"
        stale.write_text('{"event":"run_start"}\n', encoding="utf-8")
        diagnostics = self.make_diagnostics()
        recovered = stale.with_name(
            stale.name.removesuffix(".jsonl.part") + ".incomplete.jsonl"
        )
        self.assertTrue(recovered.is_file())
        self.assertFalse(stale.exists())
        diagnostics.finalize("canceled")

    def test_all_terminal_lifecycles_end_with_valid_summary(self):
        for status in ("success", "canceled", "error"):
            with self.subTest(status=status):
                diagnostics = self.make_diagnostics()
                path = diagnostics.finalize(
                    status,
                    error="expected" if status == "error" else None,
                )
                events = self.read_events(path)
                self.assertEqual(events[-2]["event"], "run_terminal")
                self.assertEqual(events[-2]["status"], status)
                self.assertEqual(events[-1]["event"], "run_summary")
                self.assertEqual(events[-1]["terminal_status"], status)

    def test_json_lines_have_common_fields_and_monotonic_elapsed(self):
        diagnostics = self.make_diagnostics()
        diagnostics.emit("custom", value=1)
        time.sleep(0.002)
        diagnostics.emit("custom", value=2)
        events = self.read_events(diagnostics.finalize("success"))
        elapsed = [event["elapsed_seconds"] for event in events]
        self.assertEqual(elapsed, sorted(elapsed))
        for event in events:
            self.assertEqual(event["schema_version"], 1)
            self.assertEqual(event["run_id"], diagnostics.run_id)
            self.assertIn("timestamp", event)
            self.assertIn("event", event)

    def test_run_start_excludes_paths_text_and_secrets(self):
        diagnostics = RunDiagnostics(
            self.book,
            {
                "backend": "mock", "voice": "voice", "language": "ru",
                "device": "cpu", "api_key": "SECRET", "text": "FULL TEXT",
            },
            logs_dir=self.logs,
        )
        path = diagnostics.finalize("success")
        contents = path.read_text(encoding="utf-8")
        self.assertNotIn("SECRET", contents)
        self.assertNotIn("FULL TEXT", contents)
        self.assertNotIn(str(self.base), contents)
        self.assertIn(self.book.name, contents)

    def test_tts_segment_math_and_zero_division(self):
        audio = self.base / "segment.wav"
        audio.write_bytes(b"audio")
        diagnostics = self.make_diagnostics()
        diagnostics.record_tts_segment(
            chapter_index=1, segment_index=1, segment_total=2,
            segment_type="main", backend="mock", voice="voice",
            language="ru", device="cpu", characters=100,
            wall_seconds=2.0, audio_path=audio,
            audio_info={"duration_seconds": 4.0, "sample_rate": 22050},
        )
        diagnostics.record_tts_segment(
            chapter_index=1, segment_index=2, segment_total=2,
            segment_type="comment", backend="mock", voice="comment",
            language="ru", device="cpu", characters=0,
            wall_seconds=0.0, audio_path=None,
            audio_info={"duration_seconds": 0.0},
        )
        events = self.read_events(diagnostics.finalize("success"))
        segments = [event for event in events if event["event"] == "tts_segment"]
        self.assertEqual(segments[0]["characters_per_second"], 50.0)
        self.assertEqual(segments[0]["realtime_factor"], 0.5)
        self.assertEqual(segments[0]["audio_realtime_speed"], 2.0)
        self.assertIsNone(segments[1]["characters_per_second"])
        self.assertIsNone(segments[1]["realtime_factor"])

    def test_tts_manager_records_each_actual_mock_fragment(self):
        class Backend:
            async def synthesize_chapter(
                self, text_segments, comment_segments, chapter_dir,
                progress_callback=None, detail_callback=None,
            ):
                segments = [(text_segments[0], "main", "main-voice")]
                segments.append((comment_segments[0], "comment", "comment-voice"))
                chapter_dir.mkdir(parents=True)
                for index, (text, _kind, voice) in enumerate(segments, start=1):
                    detail_callback(index, len(segments), text, voice, "mock")
                    (chapter_dir / f"seg_{index}.wav").write_bytes(b"audio")
                    progress_callback(index, len(segments))
                return chapter_dir

        diagnostics = self.make_diagnostics()
        manager = TTSManager(TTSConfig(backend="edge"))
        manager._backend = Backend()
        asyncio.run(manager.synthesize_chapter(
            ["основной текст"], ["комментарий"], self.base / "segments",
            diagnostics=diagnostics, chapter_index=2, language="ru",
            audio_probe=lambda _path: {
                "duration_seconds": 1.0, "sample_rate": 22050,
            },
        ))
        events = self.read_events(diagnostics.finalize("success"))
        segments = [event for event in events if event["event"] == "tts_segment"]
        self.assertEqual(len(segments), 2)
        self.assertEqual([event["segment_type"] for event in segments], ["main", "comment"])
        self.assertNotIn("основной текст", json.dumps(segments, ensure_ascii=False))
        initialization = next(
            event for event in events
            if event["event"] == "stage_end"
            and event.get("stage") == "tts_model_initialization"
        )
        self.assertEqual(initialization["status"], "success")
        self.assertEqual(initialization["outcome"], "success")
        self.assertEqual(sum(
            event["event"] == "stage_start"
            and event.get("stage") == "tts_model_initialization"
            for event in events
        ), 1)
        self.assertEqual(sum(
            event["event"] == "stage_end"
            and event.get("stage") == "tts_model_initialization"
            for event in events
        ), 1)

    def test_progress_only_backend_without_audio_does_not_record_success(self):
        class Backend:
            async def synthesize_chapter(
                self, text_segments, comment_segments, chapter_dir,
                progress_callback=None,
            ):
                progress_callback(1, 1)
                return chapter_dir

        diagnostics = self.make_diagnostics()
        manager = TTSManager(TTSConfig(backend="edge"))
        manager._backend = Backend()
        progress = []
        asyncio.run(manager.synthesize_chapter(
            ["текст"], [None], self.base / "legacy-no-audio",
            progress_callback=lambda completed, total: progress.append(
                (completed, total)
            ),
            diagnostics=diagnostics,
        ))
        events = self.read_events(diagnostics.finalize("success"))

        self.assertEqual(progress, [(1, 1)])
        self.assertFalse(any(event["event"] == "tts_segment" for event in events))
        self.assertFalse(any(
            event["event"] == "stage_end"
            and event.get("stage") == "tts_model_initialization"
            and event.get("status") == "success"
            for event in events
        ))
        self.assertEqual(events[-1]["tts_segments"], 0)

    def test_progress_only_backend_with_created_audio_records_once(self):
        class Backend:
            async def synthesize_chapter(
                self, text_segments, comment_segments, chapter_dir,
                progress_callback=None,
            ):
                chapter_dir.mkdir(parents=True)
                (chapter_dir / "seg_000000.wav").write_bytes(b"audio")
                progress_callback(1, 1)
                return chapter_dir

        diagnostics = self.make_diagnostics()
        manager = TTSManager(TTSConfig(backend="edge"))
        manager._backend = Backend()
        progress = []
        with patch.object(
            diagnostics,
            "record_tts_segment",
            wraps=diagnostics.record_tts_segment,
        ) as record_segment:
            asyncio.run(manager.synthesize_chapter(
                ["текст"], [None], self.base / "legacy-with-audio",
                progress_callback=lambda completed, total: progress.append(
                    (completed, total)
                ),
                diagnostics=diagnostics,
            ))
        events = self.read_events(diagnostics.finalize("success"))
        initialization = [
            event for event in events
            if event.get("stage") == "tts_model_initialization"
        ]

        self.assertEqual(progress, [(1, 1)])
        self.assertEqual(record_segment.call_count, 1)
        audio_path = record_segment.call_args.kwargs["audio_path"]
        self.assertTrue(audio_path.is_file())
        self.assertEqual(record_segment.call_args.kwargs["status"], "success")
        self.assertEqual(sum(event["event"] == "tts_segment" for event in events), 1)
        self.assertEqual(
            [(event["event"], event.get("status"), event.get("outcome"))
             for event in initialization],
            [("stage_start", None, None), ("stage_end", "success", "success")],
        )
        self.assertEqual(events[-1]["tts_segments"], 1)

    def test_progress_only_backend_does_not_reuse_one_file(self):
        class Backend:
            async def synthesize_chapter(
                self, text_segments, comment_segments, chapter_dir,
                progress_callback=None,
            ):
                chapter_dir.mkdir(parents=True)
                (chapter_dir / "one.wav").write_bytes(b"one")
                progress_callback(1, 2)
                progress_callback(2, 2)
                return chapter_dir

        diagnostics = self.make_diagnostics()
        manager = TTSManager(TTSConfig(backend="edge"))
        manager._backend = Backend()
        progress = []
        with patch.object(
            diagnostics,
            "record_tts_segment",
            wraps=diagnostics.record_tts_segment,
        ) as record_segment:
            asyncio.run(manager.synthesize_chapter(
                ["первый", "второй"], [None, None],
                self.base / "legacy-one-file-two-callbacks",
                progress_callback=lambda completed, total: progress.append(
                    (completed, total)
                ),
                diagnostics=diagnostics,
            ))
        events = self.read_events(diagnostics.finalize("success"))

        self.assertEqual(progress, [(1, 2), (2, 2)])
        self.assertEqual(record_segment.call_count, 1)
        self.assertEqual(
            record_segment.call_args.kwargs["audio_path"].name,
            "one.wav",
        )
        self.assertEqual(events[-1]["tts_segments"], 1)

    def test_progress_only_backend_claims_distinct_files_deterministically(self):
        class Backend:
            def __init__(self, create_ahead):
                self.create_ahead = create_ahead

            async def synthesize_chapter(
                self, text_segments, comment_segments, chapter_dir,
                progress_callback=None,
            ):
                chapter_dir.mkdir(parents=True)
                (chapter_dir / "one.wav").write_bytes(b"one")
                if self.create_ahead:
                    (chapter_dir / "two.wav").write_bytes(b"two")
                progress_callback(1, 2)
                if not self.create_ahead:
                    (chapter_dir / "two.wav").write_bytes(b"two")
                progress_callback(2, 2)
                return chapter_dir

        for create_ahead, expected_names in (
            (False, ["one.wav", "two.wav"]),
            (True, ["two.wav", "one.wav"]),
        ):
            with self.subTest(create_ahead=create_ahead):
                diagnostics = self.make_diagnostics(
                    logs_dir=self.logs / f"distinct-{create_ahead}",
                )
                manager = TTSManager(TTSConfig(backend="edge"))
                manager._backend = Backend(create_ahead)
                progress = []
                with patch.object(
                    diagnostics,
                    "record_tts_segment",
                    wraps=diagnostics.record_tts_segment,
                ) as record_segment:
                    asyncio.run(manager.synthesize_chapter(
                        ["первый", "второй"], [None, None],
                        self.base / f"legacy-distinct-{create_ahead}",
                        progress_callback=lambda completed, total: progress.append(
                            (completed, total)
                        ),
                        diagnostics=diagnostics,
                    ))
                events = self.read_events(diagnostics.finalize("success"))
                paths = [
                    call.kwargs["audio_path"]
                    for call in record_segment.call_args_list
                ]

                self.assertEqual(progress, [(1, 2), (2, 2)])
                self.assertEqual([path.name for path in paths], expected_names)
                self.assertEqual(len(set(paths)), 2)
                self.assertTrue(all(path.is_file() for path in paths))
                self.assertEqual(events[-1]["tts_segments"], 2)

    def test_progress_only_backend_ignores_preexisting_audio(self):
        chapter_dir = self.base / "legacy-old-files"
        chapter_dir.mkdir()
        (chapter_dir / "old.wav").write_bytes(b"old-wav")
        (chapter_dir / "old.mp3").write_bytes(b"old-mp3")

        class Backend:
            async def synthesize_chapter(
                self, text_segments, comment_segments, chapter_dir,
                progress_callback=None,
            ):
                (chapter_dir / "new.wav").write_bytes(b"new")
                progress_callback(1, 2)
                progress_callback(2, 2)
                return chapter_dir

        diagnostics = self.make_diagnostics()
        manager = TTSManager(TTSConfig(backend="edge"))
        manager._backend = Backend()
        progress = []
        with patch.object(
            diagnostics,
            "record_tts_segment",
            wraps=diagnostics.record_tts_segment,
        ) as record_segment:
            asyncio.run(manager.synthesize_chapter(
                ["первый", "второй"], [None, None], chapter_dir,
                progress_callback=lambda completed, total: progress.append(
                    (completed, total)
                ),
                diagnostics=diagnostics,
            ))
        events = self.read_events(diagnostics.finalize("success"))

        self.assertEqual(progress, [(1, 2), (2, 2)])
        self.assertEqual(record_segment.call_count, 1)
        self.assertEqual(
            record_segment.call_args.kwargs["audio_path"].name,
            "new.wav",
        )
        self.assertEqual(events[-1]["tts_segments"], 1)

    def test_modern_success_before_file_has_no_orphaned_stage(self):
        class Backend:
            async def synthesize_chapter(
                self, text_segments, comment_segments, chapter_dir,
                progress_callback=None, detail_callback=None,
                outcome_callback=None,
            ):
                detail_callback(1, 1, text_segments[0], "voice", "mock")
                path = chapter_dir / "one.wav"
                outcome_callback(1, 1, "success", None, path)
                progress_callback(1, 1)
                chapter_dir.mkdir(parents=True)
                path.write_bytes(b"audio")
                return chapter_dir

        diagnostics = self.make_diagnostics()
        manager = TTSManager(TTSConfig(backend="edge"))
        manager._backend = Backend()
        progress = []
        asyncio.run(manager.synthesize_chapter(
            ["текст"], [None], self.base / "modern-before-file",
            progress_callback=lambda completed, total: progress.append(
                (completed, total)
            ),
            diagnostics=diagnostics,
        ))
        events = self.read_events(diagnostics.finalize("success"))
        initialization = [
            event for event in events
            if event.get("stage") == "tts_model_initialization"
        ]

        self.assertEqual(progress, [(1, 1)])
        self.assertFalse(any(event["event"] == "tts_segment" for event in events))
        self.assertEqual(initialization, [])
        self.assertEqual(events[-1]["tts_segments"], 0)

    def test_modern_outcomes_publish_one_complete_initialization_pair(self):
        expected_stage_status = {
            "success": "success",
            "fallback_silence": "error",
            "error": "error",
            "canceled": "canceled",
        }

        for outcome, stage_status in expected_stage_status.items():
            with self.subTest(outcome=outcome):
                class Backend:
                    async def synthesize_chapter(
                        self, text_segments, comment_segments, chapter_dir,
                        progress_callback=None, detail_callback=None,
                        outcome_callback=None,
                    ):
                        detail_callback(
                            1, 1, text_segments[0], "voice", "mock",
                        )
                        chapter_dir.mkdir(parents=True)
                        path = chapter_dir / "one.wav"
                        path.write_bytes(b"audio")
                        outcome_callback(
                            1, 1, outcome,
                            None if outcome == "success" else "reported",
                            path,
                        )
                        progress_callback(1, 1)
                        return chapter_dir

                diagnostics = self.make_diagnostics(
                    logs_dir=self.logs / f"modern-{outcome}",
                )
                manager = TTSManager(TTSConfig(backend="edge"))
                manager._backend = Backend()
                progress = []
                asyncio.run(manager.synthesize_chapter(
                    ["текст"], [None], self.base / f"modern-{outcome}",
                    progress_callback=lambda completed, total: progress.append(
                        (completed, total)
                    ),
                    diagnostics=diagnostics,
                ))
                events = self.read_events(diagnostics.finalize("success"))
                segments = [
                    event for event in events
                    if event["event"] == "tts_segment"
                ]
                initialization = [
                    event for event in events
                    if event.get("stage") == "tts_model_initialization"
                ]

                self.assertEqual(progress, [(1, 1)])
                self.assertEqual(len(segments), 1)
                self.assertEqual(segments[0]["status"], outcome)
                self.assertEqual(
                    [(event["event"], event.get("status"), event.get("outcome"))
                     for event in initialization],
                    [("stage_start", None, None),
                     ("stage_end", stage_status, outcome)],
                )
                self.assertEqual(events[-1]["tts_segments"], 1)

    def test_modern_exception_publishes_one_complete_initialization_pair(self):
        class Backend:
            async def synthesize_chapter(
                self, text_segments, comment_segments, chapter_dir,
                progress_callback=None, detail_callback=None,
                outcome_callback=None,
            ):
                detail_callback(1, 1, text_segments[0], "voice", "mock")
                raise RuntimeError("synthesis failed")

        diagnostics = self.make_diagnostics()
        manager = TTSManager(TTSConfig(backend="edge"))
        manager._backend = Backend()
        with self.assertRaisesRegex(RuntimeError, "synthesis failed"):
            asyncio.run(manager.synthesize_chapter(
                ["текст"], [None], self.base / "modern-exception",
                diagnostics=diagnostics,
            ))
        events = self.read_events(diagnostics.finalize("error"))
        segments = [
            event for event in events if event["event"] == "tts_segment"
        ]
        initialization = [
            event for event in events
            if event.get("stage") == "tts_model_initialization"
        ]

        self.assertEqual(len(segments), 1)
        self.assertEqual(segments[0]["status"], "error")
        self.assertEqual(
            [(event["event"], event.get("status"), event.get("outcome"))
             for event in initialization],
            [("stage_start", None, None), ("stage_end", "error", "error")],
        )
        self.assertEqual(events[-1]["tts_segments"], 1)

    def test_stage_timing_uses_monotonic_counter(self):
        diagnostics = self.make_diagnostics()
        with diagnostics.stage("work", items=3):
            time.sleep(0.002)
        events = self.read_events(diagnostics.finalize("success"))
        end = next(
            event for event in events
            if event["event"] == "stage_end" and event["stage"] == "work"
        )
        self.assertGreater(end["duration_seconds"], 0)
        self.assertEqual(end["status"], "success")

    def test_sampler_starts_stops_joins_and_emits_samples(self):
        diagnostics = self.make_diagnostics(sample_interval=0.01)
        diagnostics._system_metrics = MagicMock(return_value={"cpu_percent": 1.0})
        diagnostics.start_sampler()
        thread = diagnostics._sampler_thread
        time.sleep(0.035)
        diagnostics.stop_sampler()
        self.assertFalse(thread.is_alive())
        path = diagnostics.finalize("success")
        samples = [
            event for event in self.read_events(path)
            if event["event"] == "system_sample"
        ]
        self.assertGreaterEqual(len(samples), 2)

    def test_absent_nvidia_returns_nulls(self):
        diagnostics = self.make_diagnostics()
        diagnostics._last_gpu_sample = -10
        with patch("src.core.run_diagnostics.shutil.which", return_value=None):
            metrics = diagnostics._gpu_metrics()
        self.assertTrue(all(value is None for value in metrics.values()))
        diagnostics.finalize("success")

    def test_nvidia_smi_fallback_parses_metrics(self):
        diagnostics = self.make_diagnostics()
        diagnostics._last_gpu_sample = -10
        completed = MagicMock(
            returncode=0,
            stdout="77, 1024, 8192, 65, 123.5\n",
        )
        with (
            patch("src.core.run_diagnostics.shutil.which", return_value="nvidia-smi"),
            patch("src.core.run_diagnostics.subprocess.run", return_value=completed),
        ):
            metrics = diagnostics._gpu_metrics()
        self.assertEqual(metrics["gpu_utilization_percent"], 77.0)
        self.assertEqual(metrics["gpu_memory_used_bytes"], 1024 * 1024 * 1024)
        diagnostics.finalize("success")

    def test_sampler_error_is_deduplicated_and_does_not_escape(self):
        diagnostics = self.make_diagnostics(sample_interval=0.01)
        diagnostics._system_metrics = MagicMock(side_effect=OSError("metrics"))
        diagnostics.start_sampler()
        time.sleep(0.035)
        diagnostics.stop_sampler()
        path = diagnostics.finalize("error", error="pipeline")
        errors = [
            event for event in self.read_events(path)
            if event["event"] == "diagnostic_error"
        ]
        self.assertEqual(len(errors), 1)

    def test_write_error_is_fail_open(self):
        diagnostics = self.make_diagnostics()
        diagnostics._stream.close()
        self.assertFalse(diagnostics.emit("custom"))
        self.assertFalse(diagnostics.available)
        self.assertIsNotNone(diagnostics.warning)

    def _create_old_log(self, name: str, size: int, mtime: int) -> Path:
        self.logs.mkdir(parents=True, exist_ok=True)
        path = self.logs / name
        path.write_bytes(b"x" * size)
        os.utime(path, ns=(mtime, mtime))
        return path

    def test_rotation_by_count_and_total_size_ignores_foreign_and_active(self):
        old = self._create_old_log(f"{LOG_PREFIX}old.jsonl", 30, 1)
        middle = self._create_old_log(f"{LOG_PREFIX}middle.incomplete.jsonl", 30, 2)
        newest = self._create_old_log(f"{LOG_PREFIX}new.jsonl", 30, 3)
        foreign = self._create_old_log("foreign.jsonl", 100, 0)
        diagnostics = self.make_diagnostics(limits=DiagnosticsLimits(
            max_files=2, max_total_bytes=100_000, max_file_bytes=10_000,
            terminal_reserve_bytes=4_096,
        ))
        self.assertFalse(old.exists())
        self.assertTrue(foreign.exists())
        self.assertTrue(diagnostics.part_path.exists())
        diagnostics.finalize("success")
        remaining = list(self.logs.glob(f"{LOG_PREFIX}*.jsonl"))
        self.assertLessEqual(len(remaining), 2)

    def test_rotation_by_total_size_removes_oldest(self):
        old = self._create_old_log(f"{LOG_PREFIX}old.jsonl", 6_000, 1)
        newest = self._create_old_log(f"{LOG_PREFIX}new.jsonl", 6_000, 2)
        foreign = self._create_old_log("foreign.jsonl", 20_000, 0)
        diagnostics = self.make_diagnostics(limits=DiagnosticsLimits(
            max_files=30, max_total_bytes=10_000, max_file_bytes=8_192,
            terminal_reserve_bytes=4_096,
        ))
        self.assertFalse(old.exists())
        self.assertTrue(newest.exists())
        self.assertTrue(foreign.exists())
        self.assertTrue(diagnostics.part_path.exists())
        diagnostics.finalize("success")

    def test_file_limit_truncates_samples_but_preserves_summary(self):
        diagnostics = self.make_diagnostics(limits=DiagnosticsLimits(
            max_files=30, max_total_bytes=100_000,
            max_file_bytes=8_192, terminal_reserve_bytes=4_096,
        ))
        for _ in range(100):
            diagnostics.emit("system_sample", payload="x" * 200)
        path = diagnostics.finalize("canceled")
        events = self.read_events(path)
        self.assertEqual(
            sum(event["event"] == "diagnostics_truncated" for event in events),
            1,
        )
        self.assertEqual(events[-1]["event"], "run_summary")
        self.assertTrue(events[-1]["diagnostics_truncated"])
        self.assertLessEqual(path.stat().st_size, diagnostics.limits.max_file_bytes)
        self.assertEqual(sum(e["event"] == "run_terminal" for e in events), 1)
        self.assertEqual(sum(e["event"] == "run_summary" for e in events), 1)

    def test_active_part_is_not_recovered_by_second_writer(self):
        first = self.make_diagnostics()
        first_part = first.part_path
        second = self.make_diagnostics()
        self.assertTrue(first_part.exists())
        self.assertFalse(first_part.with_name(
            first_part.name.removesuffix(".jsonl.part") + ".incomplete.jsonl"
        ).exists())
        second.finalize("canceled")
        first.finalize("canceled")

    def test_foreign_part_is_not_recovered(self):
        self.logs.mkdir(parents=True, exist_ok=True)
        foreign = self.logs / "foreign.jsonl.part"
        foreign.write_text("{}\n", encoding="utf-8")
        diagnostics = self.make_diagnostics()
        self.assertTrue(foreign.exists())
        diagnostics.finalize("success")

    def test_invalid_file_limit_combinations_are_rejected(self):
        invalid = (
            DiagnosticsLimits(max_files=0),
            DiagnosticsLimits(max_total_bytes=1),
            DiagnosticsLimits(max_file_bytes=0),
            DiagnosticsLimits(max_file_bytes=8_192, terminal_reserve_bytes=8_192),
            DiagnosticsLimits(max_file_bytes=8_192, terminal_reserve_bytes=-1),
        )
        for limits in invalid:
            with self.assertRaises(ValueError):
                self.make_diagnostics(limits=limits)

    def test_large_events_and_terminal_error_stay_within_limit(self):
        limits = DiagnosticsLimits(
            max_files=30, max_total_bytes=100_000,
            max_file_bytes=8_192, terminal_reserve_bytes=4_096,
        )
        diagnostics = self.make_diagnostics(limits=limits)
        diagnostics.emit("book_parsed", title="Ж" * 20_000, values=list(range(20_000)))
        path = diagnostics.finalize("error", error="failure " + "x" * 100_000)
        events = self.read_events(path)
        self.assertLessEqual(path.stat().st_size, limits.max_file_bytes)
        self.assertEqual([event["event"] for event in events[-2:]], [
            "run_terminal", "run_summary",
        ])
        self.assertEqual(sum(e["event"] == "run_terminal" for e in events), 1)
        self.assertEqual(sum(e["event"] == "run_summary" for e in events), 1)

    def test_error_like_fields_are_sanitized_centrally(self):
        diagnostics = self.make_diagnostics()
        secret_values = [
            "Authorization: Bearer very-secret-token",
            "api_key='secret with spaces'",
            'password="another secret value"',
            "https://alice:secret-password@example.invalid/path",
            f"failed at {self.book} then\nreason token=hidden-value",
        ]
        keys = ("error", "message", "reason", "detail", "warning", "exception", "stderr")
        for index, key in enumerate(keys):
            diagnostics.emit("failure_detail", **{key: secret_values[index % len(secret_values)]})
        contents = diagnostics.finalize("error", error=secret_values[0]).read_text(
            encoding="utf-8",
        )
        forbidden = (
            "very-secret-token", "secret with spaces", "another secret value",
            "secret-password", "hidden-value", str(self.book), str(self.base),
        )
        self.assertFalse(any(value in contents for value in forbidden))
        self.assertIn("<redacted>", contents)

    def test_secret_field_names_are_redacted_at_every_depth(self):
        diagnostics = self.make_diagnostics()
        diagnostics.emit(
            "secret_fields",
            TOKEN="FIXTURE_PRIVATE_STRING",
            api_key=["FIXTURE_PRIVATE_LIST"],
            **{
                "api-key": {"value": "FIXTURE_PRIVATE_DICT"},
                "apiKey": "FIXTURE_PRIVATE_CAMEL",
                "Password": 123456,
                "authorization": "Bearer FIXTURE_PRIVATE_AUTH",
                "access_token": "FIXTURE_PRIVATE_ACCESS",
                "nested": {
                    "refreshToken": "FIXTURE_PRIVATE_REFRESH",
                    "items": [
                        {"client_secret": "FIXTURE_PRIVATE_CLIENT"},
                        {"secret": "FIXTURE_PRIVATE_DEEP"},
                    ],
                },
                "title": "Безопасное название",
                "value": 42,
                "message": (
                    f"failed at {self.book}; token=FIXTURE_PRIVATE_ERROR"
                ),
            },
        )
        path = diagnostics.finalize("error")
        contents = path.read_text(encoding="utf-8")
        event = next(
            item for item in self.read_events(path)
            if item["event"] == "secret_fields"
        )
        redacted_values = [
            event["TOKEN"], event["api_key"], event["api-key"],
            event["apiKey"], event["Password"], event["authorization"],
            event["access_token"], event["nested"]["refreshToken"],
            event["nested"]["items"][0]["client_secret"],
            event["nested"]["items"][1]["secret"],
        ]
        self.assertTrue(all(value == "<redacted>" for value in redacted_values))
        self.assertFalse("FIXTURE_PRIVATE_" in contents)
        self.assertFalse(str(self.book) in contents)
        self.assertEqual(event["title"], "Безопасное название")
        self.assertEqual(event["value"], 42)

    def test_unusual_nested_mapping_keys_are_stringified_safely(self):
        class ObjectKey:
            def __init__(self, value):
                self.value = value

            def __str__(self):
                return self.value

        diagnostics = self.make_diagnostics()
        diagnostics.emit(
            "odd_keys",
            nested={
                (1, 2): "tuple-value",
                7: "numeric-value",
                ObjectKey("object-key"): "object-value",
                "deeper": {
                    (3, 4): [{ObjectKey("clientSecret"): "PRIVATE_VALUE"}],
                },
                1: "numeric-collision",
                "1": "string-collision",
            },
        )
        self.assertFalse(diagnostics._disabled)
        self.assertTrue(diagnostics.emit("after_odd_keys", value=42))
        path = diagnostics.finalize("success")
        events = self.read_events(path)
        event = next(item for item in events if item["event"] == "odd_keys")

        self.assertEqual(event["nested"]["(1, 2)"], "tuple-value")
        self.assertEqual(event["nested"]["7"], "numeric-value")
        self.assertEqual(event["nested"]["object-key"], "object-value")
        self.assertTrue(
            event["nested"]["deeper"]["(3, 4)"][0]["clientSecret"]
            == "<redacted>",
            "secret-like value was not redacted",
        )
        self.assertEqual(event["nested"]["1"], "string-collision")
        self.assertFalse(
            "PRIVATE_VALUE" in path.read_text(encoding="utf-8"),
            "secret-like value leaked from an unusual mapping key",
        )
        self.assertTrue(any(item["event"] == "after_odd_keys" for item in events))
        self.assertEqual(events[-2]["event"], "run_terminal")
        self.assertEqual(events[-1]["event"], "run_summary")

    def test_two_concurrent_finalize_calls_write_one_consistent_pair(self):
        diagnostics = self.make_diagnostics()
        update_barrier = threading.Barrier(3)

        def add_segments(offset):
            update_barrier.wait()
            for index in range(10):
                diagnostics.record_tts_segment(
                    chapter_index=1, segment_index=offset + index,
                    segment_total=20, segment_type="main", backend="mock",
                    voice="voice", language="ru", device="cpu", characters=10,
                    wall_seconds=0.1, audio_path=None,
                )

        update_threads = [
            threading.Thread(target=add_segments, args=(1,)),
            threading.Thread(target=add_segments, args=(11,)),
        ]
        for thread in update_threads:
            thread.start()
        update_barrier.wait()
        for thread in update_threads:
            thread.join(timeout=2)
        self.assertTrue(all(not thread.is_alive() for thread in update_threads))
        barrier = threading.Barrier(3)
        results = []

        def finish():
            barrier.wait()
            results.append(diagnostics.finalize("success"))

        threads = [threading.Thread(target=finish) for _ in range(2)]
        for thread in threads:
            thread.start()
        barrier.wait()
        for thread in threads:
            thread.join(timeout=2)
        self.assertTrue(all(not thread.is_alive() for thread in threads))
        self.assertEqual(results, [diagnostics.final_path, diagnostics.final_path])
        events = self.read_events(diagnostics.final_path)
        self.assertEqual(sum(e["event"] == "run_terminal" for e in events), 1)
        self.assertEqual(sum(e["event"] == "run_summary" for e in events), 1)
        self.assertEqual(events[-1]["tts_segments"], 20)
        self.assertEqual(events[-1]["characters"], 200)

    def test_ffprobe_failures_and_non_finite_values_are_safe(self):
        assembler = AudioAssembler.__new__(AudioAssembler)
        assembler._audio_probe_warnings = set()
        audio = self.base / "audio.mp3"
        audio.write_bytes(b"audio")
        empty = {"duration_seconds": None, "bitrate_bps": None, "sample_rate": None}
        with (
            patch("src.core.audio_assembler.shutil.which", return_value="ffprobe"),
            patch("src.core.audio_assembler.sp.run", side_effect=subprocess.TimeoutExpired("ffprobe", 10)),
        ):
            self.assertEqual(assembler.get_audio_info(audio), empty)
        for failure in (
            FileNotFoundError("ffprobe"),
            subprocess.CalledProcessError(1, ["ffprobe"]),
        ):
            with (
                patch("src.core.audio_assembler.shutil.which", return_value="ffprobe"),
                patch("src.core.audio_assembler.sp.run", side_effect=failure),
            ):
                self.assertEqual(assembler.get_audio_info(audio), empty)
        with (
            patch("src.core.audio_assembler.shutil.which", return_value="ffprobe"),
            patch("src.core.audio_assembler.sp.run", return_value=MagicMock(stdout=b"not-json")),
        ):
            self.assertEqual(assembler.get_audio_info(audio), empty)
        data = json.dumps({
            "format": {"duration": "NaN", "bit_rate": "Infinity"},
            "streams": [{"codec_type": "audio", "sample_rate": "-Infinity"}],
        }).encode()
        with (
            patch("src.core.audio_assembler.shutil.which", return_value="ffprobe"),
            patch("src.core.audio_assembler.sp.run", return_value=MagicMock(stdout=data)),
        ):
            self.assertEqual(assembler.get_audio_info(audio), empty)
            self.assertEqual(assembler.get_audio_duration(audio), 0.0)
        with patch("src.core.audio_assembler.shutil.which", return_value=None):
            self.assertEqual(assembler.get_audio_info(audio), empty)

    def test_ffprobe_uses_first_valid_format_or_stream_metric(self):
        assembler = AudioAssembler.__new__(AudioAssembler)
        assembler._audio_probe_warnings = set()
        audio = self.base / "metrics.mp3"
        audio.write_bytes(b"audio")

        def probe(format_duration, stream_duration, format_bitrate, stream_bitrate):
            stdout = json.dumps({
                "format": {
                    "duration": format_duration,
                    "bit_rate": format_bitrate,
                },
                "streams": [{
                    "codec_type": "audio",
                    "duration": stream_duration,
                    "bit_rate": stream_bitrate,
                    "sample_rate": "22050",
                }],
            }).encode()
            with (
                patch("src.core.audio_assembler.shutil.which", return_value="ffprobe"),
                patch(
                    "src.core.audio_assembler.sp.run",
                    return_value=MagicMock(stdout=stdout),
                ) as run,
            ):
                result = assembler.get_audio_info(audio)
            self.assertTrue(run.call_args.kwargs["check"])
            self.assertEqual(run.call_args.kwargs["timeout"], 10.0)
            return result

        for invalid in ("0", "NaN", "Infinity", "-Infinity", "N/A", "", "bad"):
            result = probe(invalid, "12.5", invalid, "128000")
            self.assertEqual(result["duration_seconds"], 12.5)
            self.assertEqual(result["bitrate_bps"], 128000)
        invalid = probe("NaN", "0", "N/A", "-1")
        self.assertIsNone(invalid["duration_seconds"])
        self.assertIsNone(invalid["bitrate_bps"])
        preferred = probe("7.25", "12.5", "192000", "128000")
        self.assertEqual(preferred["duration_seconds"], 7.25)
        self.assertEqual(preferred["bitrate_bps"], 192000)
        self.assertEqual(preferred["sample_rate"], 22050)

    def test_ffprobe_rejects_boolean_metrics_for_bytes_and_text_stdout(self):
        assembler = AudioAssembler.__new__(AudioAssembler)
        assembler._audio_probe_warnings = set()
        audio = self.base / "boolean-metrics.mp3"
        audio.write_bytes(b"audio")

        def probe(payload, as_bytes):
            stdout = json.dumps(payload)
            if as_bytes:
                stdout = stdout.encode()
            with (
                patch("src.core.audio_assembler.shutil.which", return_value="ffprobe"),
                patch(
                    "src.core.audio_assembler.sp.run",
                    return_value=MagicMock(stdout=stdout),
                ) as run,
            ):
                result = assembler.get_audio_info(audio)
            self.assertTrue(run.call_args.kwargs["capture_output"])
            self.assertTrue(run.call_args.kwargs["check"])
            self.assertEqual(run.call_args.kwargs["timeout"], 10.0)
            return result

        fallback_payload = {
            "format": {"duration": True, "bit_rate": False},
            "streams": [{
                "codec_type": "audio",
                "duration": "12.5",
                "bit_rate": 128000,
                "sample_rate": True,
            }],
        }
        invalid_payload = {
            "format": {"duration": True, "bit_rate": False},
            "streams": [{
                "codec_type": "audio",
                "duration": False,
                "bit_rate": True,
                "sample_rate": False,
            }],
        }
        for as_bytes in (True, False):
            with self.subTest(as_bytes=as_bytes, fallback=True):
                result = probe(fallback_payload, as_bytes)
                self.assertEqual(result["duration_seconds"], 12.5)
                self.assertEqual(result["bitrate_bps"], 128000)
                self.assertIsNone(result["sample_rate"])
                with patch.object(assembler, "get_audio_info", return_value=result):
                    self.assertEqual(assembler.get_audio_duration(audio), 12.5)
            with self.subTest(as_bytes=as_bytes, fallback=False):
                result = probe(invalid_payload, as_bytes)
                self.assertIsNone(result["duration_seconds"])
                self.assertIsNone(result["bitrate_bps"])
                self.assertIsNone(result["sample_rate"])
                with patch.object(assembler, "get_audio_info", return_value=result):
                    self.assertEqual(assembler.get_audio_duration(audio), 0.0)

    def test_silero_fallback_silence_is_not_recorded_as_success(self):
        backend = SileroTTSManager.__new__(SileroTTSManager)
        backend._main_voice = "xenia"
        backend._comment_voice = "xenia"
        backend.config = SimpleNamespace(main_speed=1.0, comment_speed=1.0)
        backend.synthesize_segment = AsyncMock(
            side_effect=RuntimeError("password='private value'"),
        )

        async def create_silence(path, duration_sec):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"silence")

        backend._generate_silence_mp3 = AsyncMock(side_effect=create_silence)
        diagnostics = self.make_diagnostics()
        manager = TTSManager(TTSConfig(backend="silero"))
        manager._backend = backend
        with patch("src.core.tts_silero.logger.error"):
            asyncio.run(manager.synthesize_chapter(
                ["короткий текст"], [None], self.base / "fallback",
                diagnostics=diagnostics, chapter_index=1, language="ru",
                audio_probe=lambda _path: {"duration_seconds": 0.5},
            ))
        events = self.read_events(diagnostics.finalize("success"))
        segment = next(event for event in events if event["event"] == "tts_segment")
        self.assertEqual(segment["status"], "fallback_silence")
        self.assertEqual(segment["outcome"], "fallback_silence")
        self.assertEqual(segment["audio_size_bytes"], len(b"silence"))
        self.assertNotIn("private value", json.dumps(segment, ensure_ascii=False))
        initialization = next(
            event for event in events
            if event["event"] == "stage_end"
            and event.get("stage") == "tts_model_initialization"
        )
        self.assertEqual(initialization["status"], "error")
        self.assertEqual(initialization["outcome"], "fallback_silence")
        self.assertNotIn(
            "private value", json.dumps(initialization, ensure_ascii=False),
        )
        summary = events[-1]
        self.assertEqual(summary["tts_segments"], 1)

    def _run_mock_pipeline(self, outcome: str):
        pipeline_base = self.base / outcome
        pipeline_base.mkdir(parents=True, exist_ok=True)
        pipeline = global_progress_tests.GlobalProgressTests()._make_pipeline(
            pipeline_base
        )
        diagnostics = self.make_diagnostics(logs_dir=self.logs / outcome)
        pipeline.diagnostics = diagnostics
        if outcome in {"canceled", "error"}:
            pipeline.tts_manager.failure = "cancel" if outcome == "canceled" else "error"
        exception = None
        try:
            asyncio.run(pipeline.run())
        except BaseException as exc:
            exception = exc
        return diagnostics, exception

    def test_pipeline_cancel_before_setup_finalizes_canceled_log(self):
        (self.base / "early-cancel").mkdir()
        pipeline = global_progress_tests.GlobalProgressTests()._make_pipeline(
            self.base / "early-cancel",
        )
        diagnostics = self.make_diagnostics(logs_dir=self.logs / "early-cancel")
        pipeline.diagnostics = diagnostics
        canceled = threading.Event()
        canceled.set()
        with self.assertRaises(PipelineCanceledError):
            asyncio.run(pipeline.run(cancel_event=canceled))
        events = self.read_events(diagnostics.final_path)
        self.assertEqual(events[-2]["status"], "canceled")
        self.assertEqual(events[-1]["terminal_status"], "canceled")
        self.assertFalse(diagnostics.part_path.exists())

    def test_pipeline_mkdtemp_failure_finalizes_error_log(self):
        (self.base / "setup-error").mkdir()
        pipeline = global_progress_tests.GlobalProgressTests()._make_pipeline(
            self.base / "setup-error",
        )
        diagnostics = self.make_diagnostics(logs_dir=self.logs / "setup-error")
        pipeline.diagnostics = diagnostics
        with patch("src.core.pipeline.tempfile.mkdtemp", side_effect=OSError("setup failed")):
            with self.assertRaisesRegex(OSError, "setup failed"):
                asyncio.run(pipeline.run())
        events = self.read_events(diagnostics.final_path)
        self.assertEqual(events[-1]["terminal_status"], "error")
        self.assertFalse(diagnostics.part_path.exists())

    def test_sampler_start_failure_is_fail_open(self):
        (self.base / "sampler-start").mkdir()
        pipeline = global_progress_tests.GlobalProgressTests()._make_pipeline(
            self.base / "sampler-start",
        )
        diagnostics = self.make_diagnostics(logs_dir=self.logs / "sampler-start")
        pipeline.diagnostics = diagnostics
        with patch("src.core.run_diagnostics.threading.Thread.start", side_effect=RuntimeError("thread failed")):
            result = asyncio.run(pipeline.run())
        self.assertTrue(result.is_file())
        events = self.read_events(diagnostics.final_path)
        self.assertEqual(events[-1]["terminal_status"], "success")
        self.assertEqual(
            sum(e.get("source") == "system_sampler_start" for e in events), 1,
        )

    def test_cleanup_failure_does_not_hide_primary_pipeline_error(self):
        (self.base / "primary-and-cleanup").mkdir()
        pipeline = global_progress_tests.GlobalProgressTests()._make_pipeline(
            self.base / "primary-and-cleanup", failure="error",
        )
        diagnostics = self.make_diagnostics(logs_dir=self.logs / "primary-and-cleanup")
        pipeline.diagnostics = diagnostics
        pipeline.audio_assembler.cleanup_temp_files = MagicMock(
            side_effect=OSError("cleanup failed"),
        )
        with self.assertRaisesRegex(RuntimeError, "tts failed"):
            asyncio.run(pipeline.run())
        events = self.read_events(diagnostics.final_path)
        terminal = events[-2]
        self.assertEqual(terminal["status"], "error")
        self.assertIn("tts failed", terminal["error"])
        cleanup_end = [
            e for e in events
            if e["event"] == "stage_end" and e.get("stage") == "temporary_cleanup"
        ][-1]
        self.assertEqual(cleanup_end["status"], "error")

    def test_cleanup_failure_after_success_changes_terminal_status(self):
        (self.base / "cleanup-only").mkdir()
        pipeline = global_progress_tests.GlobalProgressTests()._make_pipeline(
            self.base / "cleanup-only",
        )
        diagnostics = self.make_diagnostics(logs_dir=self.logs / "cleanup-only")
        pipeline.diagnostics = diagnostics
        pipeline.audio_assembler.cleanup_temp_files = MagicMock(
            side_effect=OSError("cleanup failed"),
        )
        with self.assertRaisesRegex(OSError, "cleanup failed"):
            asyncio.run(pipeline.run())
        events = self.read_events(diagnostics.final_path)
        self.assertEqual(events[-2]["status"], "error")
        self.assertEqual(events[-1]["terminal_status"], "error")

    def test_diagnostics_finalize_error_does_not_mask_pipeline_error(self):
        base = self.base / "pipeline-and-diagnostics-error"
        base.mkdir()
        pipeline = global_progress_tests.GlobalProgressTests()._make_pipeline(
            base, failure="error",
        )
        diagnostics = self.make_diagnostics(logs_dir=self.logs / "finalize-primary")
        pipeline.diagnostics = diagnostics
        original_finalize = diagnostics.finalize

        def fail_after_finalize(*args, **kwargs):
            original_finalize(*args, **kwargs)
            raise RuntimeError("diagnostics finalize failed")

        diagnostics.finalize = fail_after_finalize
        with self.assertRaisesRegex(RuntimeError, "tts failed"):
            asyncio.run(pipeline.run())
        self.assertTrue(diagnostics.final_path.is_file())

    def test_ordinary_diagnostics_finalize_error_is_fail_open_after_success(self):
        base = self.base / "successful-pipeline-finalize-error"
        base.mkdir()
        pipeline = global_progress_tests.GlobalProgressTests()._make_pipeline(base)
        diagnostics = self.make_diagnostics(logs_dir=self.logs / "finalize-success")
        pipeline.diagnostics = diagnostics
        original_finalize = diagnostics.finalize

        def fail_after_finalize(*args, **kwargs):
            original_finalize(*args, **kwargs)
            raise RuntimeError("diagnostics finalize failed")

        diagnostics.finalize = fail_after_finalize
        result = asyncio.run(pipeline.run())
        self.assertTrue(result.is_file())
        self.assertTrue(diagnostics.final_path.is_file())

    def test_base_exception_from_finalize_propagates_without_pipeline_error(self):
        base = self.base / "successful-pipeline-finalize-interrupt"
        base.mkdir()
        pipeline = global_progress_tests.GlobalProgressTests()._make_pipeline(base)
        diagnostics = self.make_diagnostics(logs_dir=self.logs / "finalize-interrupt")
        pipeline.diagnostics = diagnostics
        original_finalize = diagnostics.finalize

        def interrupt_after_finalize(*args, **kwargs):
            original_finalize(*args, **kwargs)
            raise KeyboardInterrupt()

        diagnostics.finalize = interrupt_after_finalize
        with self.assertRaises(KeyboardInterrupt):
            asyncio.run(pipeline.run())
        self.assertTrue(diagnostics.final_path.is_file())

    def test_mock_pipeline_success_cancellation_and_error_close_resources(self):
        for outcome, exception_type in (
            ("success", None),
            ("canceled", PipelineCanceledError),
            ("error", RuntimeError),
        ):
            with self.subTest(outcome=outcome):
                diagnostics, exception = self._run_mock_pipeline(outcome)
                if exception_type is None:
                    self.assertIsNone(exception)
                else:
                    self.assertIsInstance(exception, exception_type)
                self.assertTrue(diagnostics.final_path.is_file())
                self.assertFalse(diagnostics.part_path.exists())
                self.assertIsNone(diagnostics._stream)
                self.assertIsNone(diagnostics._sampler_thread)
                events = self.read_events(diagnostics.final_path)
                self.assertEqual(events[-1]["terminal_status"], outcome)

    def test_gui_saved_path_message_excludes_system_samples(self):
        diagnostics = self.make_diagnostics()
        gui = AudiobookGeneratorGUI.__new__(AudiobookGeneratorGUI)
        messages = []
        gui._append_log = messages.append
        gui._append_diagnostics_start(diagnostics)
        diagnostics.emit("system_sample", cpu_percent=1)
        diagnostics.finalize("success")
        gui.pipeline = MagicMock(diagnostics=diagnostics)
        gui._append_saved_diagnostics_path()
        self.assertEqual(messages, [
            f"Диагностический журнал: {diagnostics.part_path}",
            f"Журнал сохранён: {diagnostics.final_path}",
        ])
        self.assertNotIn("system_sample", " ".join(messages))

    def test_gui_diagnostics_warning_is_shown_once(self):
        gui = AudiobookGeneratorGUI.__new__(AudiobookGeneratorGUI)
        gui.progress = {"value": 0}
        gui._reset_progress_state()
        messages = []
        gui._append_log = messages.append
        diagnostics = MagicMock(
            available=False,
            warning="запись недоступна",
            final_path=self.base / "missing.jsonl",
        )
        gui._append_diagnostics_start(diagnostics)
        gui.pipeline = MagicMock(diagnostics=diagnostics)
        gui._append_saved_diagnostics_path()
        self.assertEqual(len(messages), 1)
        self.assertIn("запись недоступна", messages[0])


if __name__ == "__main__":
    unittest.main()
