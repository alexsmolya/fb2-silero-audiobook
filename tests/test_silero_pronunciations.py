"""Тесты пользовательского словаря произношений Silero."""

from __future__ import annotations

import asyncio
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from src.core.tts_silero import (
    SILERO_RU_MODEL_ID,
    SileroTTSManager,
    apply_pronunciations,
    load_pronunciations,
)


class SileroPronunciationTests(unittest.TestCase):
    def _load(self, content: str):
        temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(temporary_directory.cleanup)
        path = Path(temporary_directory.name) / "pronunciations.toml"
        path.write_text(content, encoding="utf-8")
        return load_pronunciations(path)

    def test_backend_loads_dictionary_once_when_created(self):
        config = SimpleNamespace(main_voice="xenia", comment_voice="eugene")
        with patch(
            "src.core.tts_silero.load_pronunciations",
            return_value=[],
        ) as loader:
            SileroTTSManager(config)
        loader.assert_called_once_with()

    def test_russian_wrapper_uses_v5_5_with_eugene(self):
        config = SimpleNamespace(main_voice="eugene", comment_voice="xenia")
        with patch(
            "src.core.tts_silero.load_pronunciations",
            return_value=[],
        ), patch(
            "silero_tts.silero_tts.SileroTTS",
        ) as silero_tts:
            manager = SileroTTSManager(config)
            with patch.object(manager, "_get_device", return_value="cpu"):
                asyncio.run(manager._ensure_ru_initialized())

        silero_tts.assert_called_once_with(
            model_id="v5_5_ru",
            language="ru",
            speaker="eugene",
            sample_rate=48000,
            device="cpu",
        )
        self.assertEqual(SILERO_RU_MODEL_ID, "v5_5_ru")

    def test_english_wrapper_keeps_v3_en(self):
        config = SimpleNamespace(main_voice="en_0", comment_voice="random")
        with patch(
            "src.core.tts_silero.load_pronunciations",
            return_value=[],
        ), patch(
            "silero_tts.silero_tts.SileroTTS",
        ) as silero_tts:
            manager = SileroTTSManager(config)
            with patch.object(manager, "_get_device", return_value="cpu"):
                initialized = asyncio.run(manager._ensure_en_initialized())

        self.assertTrue(initialized)
        silero_tts.assert_called_once_with(
            model_id="v3_en",
            language="en",
            speaker="en_0",
            sample_rate=48000,
            device="cpu",
        )

    def test_replaces_russian_phrase(self):
        rules = self._load(
            '[ru]\n"открыла глаза" = "открыла глаз+а"\n'
        )
        self.assertEqual(
            apply_pronunciations("открыла глаза", rules),
            "открыла глаз+а",
        )

    def test_preserves_initial_capital(self):
        rules = self._load(
            '[ru]\n"открыла глаза" = "открыла глаз+а"\n'
        )
        self.assertEqual(
            apply_pronunciations("Открыла глаза", rules),
            "Открыла глаз+а",
        )

    def test_longer_phrase_has_priority(self):
        rules = self._load(
            '[ru]\n'
            '"глаза" = "глаз+а"\n'
            '"открыла глаза" = "раскрыла глаз+а"\n'
        )
        self.assertEqual(
            apply_pronunciations("Она открыла глаза.", rules),
            "Она раскрыла глаз+а.",
        )

    def test_does_not_replace_part_of_another_word(self):
        rules = self._load('[ru]\n"глаз" = "гл+аз"\n')
        self.assertEqual(
            apply_pronunciations("глазной и глаз", rules),
            "глазной и гл+аз",
        )

    def test_missing_file_returns_empty_rules(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "missing.toml"
            self.assertEqual(load_pronunciations(path), [])

    def test_invalid_toml_returns_empty_rules(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "pronunciations.toml"
            path.write_text('[ru\n"глаза" = "глаз+а"', encoding="utf-8")
            with self.assertLogs("src.core.tts_silero", level="WARNING") as logs:
                rules = load_pronunciations(path)
            self.assertEqual(rules, [])
            self.assertIn("не удалось загрузить словарь", " ".join(logs.output))


if __name__ == "__main__":
    unittest.main()
