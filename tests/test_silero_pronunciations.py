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

    def test_book_7_pronunciation_rules(self):
        rules = load_pronunciations()

        # 1. Безопасные имена и термины
        self.assertEqual(apply_pronunciations("Лев Демидович", rules), "Лев Дем+идович")
        self.assertEqual(apply_pronunciations("мимо Льва Демидовича", rules), "мимо Льва Дем+идовича")
        self.assertEqual(apply_pronunciations("Паша", rules), "П+аша")
        self.assertEqual(apply_pronunciations("клановка", rules), "кл+ановка")
        self.assertEqual(apply_pronunciations("ястребами", rules), "+ястребами")

        # 2. Фразовые и контекстные правила
        self.assertEqual(apply_pronunciations("не слишком большая часть", rules), "не слишком больш+ая часть")
        self.assertEqual(apply_pronunciations("Никто не подаст руки", rules), "Никто не подаст рук+и")
        self.assertEqual(
            apply_pronunciations("без всяких эмоций предельно формально начала Юсупова", rules),
            "без всяких эмоций предельно формально начал+а Юсупова",
        )
        self.assertEqual(apply_pronunciations("в его словах", rules), "в его слов+ах")
        self.assertEqual(apply_pronunciations("приложил сил к тому, чтобы", rules), "приложил сил к том+у, чтобы")
        self.assertEqual(apply_pronunciations("так и малое дофига", rules), "так и м+алое дофига")
        self.assertEqual(apply_pronunciations("второй технический кандидат", rules), "втор+ой технический кандидат")

        # 3. Не должны изменяться (омографы, бренды, многоточия)
        self.assertEqual(apply_pronunciations("Стоит уточнить...", rules), "Стоит уточнить...")
        self.assertEqual(apply_pronunciations("— Стоит? — Стоит.", rules), "— Стоит? — Стоит.")
        self.assertEqual(apply_pronunciations("все", rules), "все")
        self.assertEqual(apply_pronunciations("всё", rules), "всё")
        self.assertEqual(apply_pronunciations("РитРос", rules), "РитРос")
        self.assertEqual(apply_pronunciations("ряд… специалистов", rules), "ряд… специалистов")

        # 4. Нумерация глав
        self.assertEqual(apply_pronunciations("Глава 1", rules), "Глава первая")
        self.assertEqual(apply_pronunciations("Глава 7", rules), "Глава седьмая")
        self.assertEqual(apply_pronunciations("Глава 22", rules), "Глава двадцать вторая")


if __name__ == "__main__":
    unittest.main()
