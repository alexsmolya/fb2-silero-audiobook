"""
Тесты для проверки логирования текста TTS-сегментов и диагностических полей в JSONL.
"""

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from src.core.run_diagnostics import RunDiagnostics, DiagnosticsLimits


class TestTTSDiagnosticsJSONL(unittest.TestCase):
    """Тесты диагностики JSONL для TTS-сегментов."""

    def test_text_and_boundaries_appear_in_jsonl(self):
        with TemporaryDirectory() as tmp_dir:
            diag = RunDiagnostics(
                book_path=Path("test.fb2"),
                run_info={"backend": "silero"},
                logs_dir=Path(tmp_dir),
                limits=DiagnosticsLimits(),
            )

            test_text = "— Недаром её отец и ряд специалистов считали, что..."

            diag.record_tts_segment(
                chapter_index=1,
                segment_index=1,
                segment_total=5,
                segment_type="main",
                backend="silero",
                voice="xenia",
                language="ru",
                device="cpu",
                characters=len(test_text),
                wall_seconds=0.15,
                audio_path=Path("/tmp/fake.mp3"),
                audio_info={"duration_seconds": 2.5},
                status="success",
                text=test_text,
            )

            final_file = diag.finalize("success")

            lines = Path(final_file).read_text(encoding="utf-8").strip().splitlines()
            events = [json.loads(line) for line in lines]
            tts_events = [e for e in events if e.get("event") == "tts_segment"]

            self.assertEqual(len(tts_events), 1)
            event = tts_events[0]

            self.assertEqual(event["text"], test_text)
            self.assertEqual(event["characters"], len(test_text))
            self.assertEqual(event["boundary_before"], "start_of_chapter")
            self.assertEqual(event["boundary_after"], "...")
            self.assertEqual(event["audio_duration_seconds"], 2.5)

    def test_unicode_quotes_newlines_escaping_in_jsonl(self):
        with TemporaryDirectory() as tmp_dir:
            diag = RunDiagnostics(
                book_path=Path("test.fb2"),
                run_info={"backend": "silero"},
                logs_dir=Path(tmp_dir),
                limits=DiagnosticsLimits(),
            )

            complex_text = "— «Привет! — сказал он.\nВторой абзац: \"Цитата\" & special chars.»"

            diag.record_tts_segment(
                chapter_index=1,
                segment_index=2,
                segment_total=5,
                segment_type="main",
                backend="silero",
                voice="eugene",
                language="ru",
                device="cpu",
                characters=len(complex_text),
                wall_seconds=0.2,
                audio_path=None,
                audio_info={"duration_seconds": 3.0},
                status="success",
                text=complex_text,
            )

            final_file = diag.finalize("success")

            lines = Path(final_file).read_text(encoding="utf-8").strip().splitlines()
            events = [json.loads(line) for line in lines]
            tts_events = [e for e in events if e.get("event") == "tts_segment"]

            self.assertEqual(len(tts_events), 1)
            event = tts_events[0]
            self.assertEqual(event["text"], complex_text)
            self.assertEqual(event["boundary_before"], "dash")
            self.assertEqual(event["boundary_after"], ".")

    def test_boundary_detection_punctuation_variants(self):
        cases = [
            ("Простое предложение.", "."),
            ("Вопрос?", "?"),
            ("Восклицание!", "!"),
            ("Многоточие...", "..."),
            ("Кажется, запятая,", ","),
            ("Двоеточие:", ":"),
            ("Точка с запятой;", ";"),
            ("Тире —", "dash"),
            ("Без знаков на конце", "none"),
        ]

        for text, expected_boundary_after in cases:
            with TemporaryDirectory() as tmp_dir:
                d = RunDiagnostics(
                    book_path=Path("test.fb2"),
                    run_info={"backend": "mock"},
                    logs_dir=Path(tmp_dir),
                )
                d.record_tts_segment(
                    chapter_index=1, segment_index=2, segment_total=2,
                    segment_type="main", backend="mock", voice="v", language="ru",
                    device="cpu", characters=len(text), wall_seconds=0.1, audio_path=None,
                    text=text,
                )
                final_file = d.finalize("success")
                lines = Path(final_file).read_text(encoding="utf-8").strip().splitlines()
                events = [json.loads(l) for l in lines]
                tts_event = [e for e in events if e.get("event") == "tts_segment"][0]
                self.assertEqual(tts_event["boundary_after"], expected_boundary_after, f"Failed for '{text}'")


if __name__ == "__main__":
    unittest.main()
