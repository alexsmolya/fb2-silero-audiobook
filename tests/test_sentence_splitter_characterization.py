"""
Характеризационные тесты (Characterization tests) для текущего разбиения на предложения (SentenceSplitter).

Фиксируют существующее поведение модуля SentenceSplitter (включая неоптимальные разрывы
и особенности обработки сокращений, диалогов и т.д.) до проведения оптимизации алгоритма.
"""

import unittest
from src.core.sentence_splitter import SentenceSplitter


class TestSentenceSplitterCharacterization(unittest.TestCase):
    """Фиксация текущего поведения SentenceSplitter."""

    def setUp(self):
        self.splitter = SentenceSplitter()

    def test_01_short_sentence(self):
        """1. Короткое предложение."""
        text = "Да."
        result = self.splitter.split(text, lang="ru")
        self.assertEqual(result, ["Да."])

    def test_02_multiple_sentences(self):
        """2. Несколько простых предложений."""
        text = "Первое предложение. Второе предложение! Третье предложение?"
        result = self.splitter.split(text, lang="ru")
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], "Первое предложение.")
        self.assertEqual(result[1], "Второе предложение!")
        self.assertEqual(result[2], "Третье предложение?")

    def test_03_long_sentence(self):
        """3. Длинное предложение с несколькими придаточными частями."""
        text = (
            "Он долго шел по темному ночному лесу, прислушиваясь к каждому шороху веток, "
            "потому что где-то поблизости мог находиться опасный хищник."
        )
        result = self.splitter.split(text, lang="ru")
        # Текущий алгоритм сохраняет единое длинное предложение без разрывов по запятым
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], text)

    def test_04_sentence_exceeding_limit(self):
        """4. Очень длинное предложение (превышающее типичный комфортный TTS-лимит)."""
        text = (
            "В том далеком городе, где шум машин никогда не стихал даже глубокой ночью, "
            "жила одна пожилая женщина, которая каждый день выходила на балкон и смотрела на "
            "проплывающие облака, думая о своем далеком детстве и о людях, которых она когда-то любила."
        )
        result = self.splitter.split(text, lang="ru")
        # Фиксируем: текущий сегментатор не режет предложение без точек
        self.assertEqual(len(result), 1)

    def test_05_abbreviations(self):
        """5. Сокращения (и т.д., т.к., г., ул.)."""
        text = "Прибыли в г. Москва на ул. Арбат и т. д. Все прошло хорошо."
        result = self.splitter.split(text, lang="ru")
        # Фиксируем текущую разбивку на предложения
        self.assertTrue(len(result) >= 1)
        # Убеждаемся, что итоговый текст не потерян
        self.assertEqual(" ".join(result), text)

    def test_06_dialogue_with_dashes(self):
        """6. Диалог с тире."""
        text = "— Куда мы идем? — спросил Павел. — К реке, — ответил спутник."
        result = self.splitter.split(text, lang="ru")
        self.assertTrue(len(result) >= 2)
        # Фиксируем, что все части диалога присутствуют
        self.assertIn("— Куда мы идем?", result[0])

    def test_07_ellipsis(self):
        """7. Многоточие."""
        text = "Недаром её отец и ряд специалистов считали, что... это было ошибкой."
        result = self.splitter.split(text, lang="ru")
        self.assertTrue(len(result) >= 1)

    def test_08_dot_without_space(self):
        """8. Точка без пробела (числа, сайты, опечатки)."""
        text = "Версия 2.0.1 вышла на сайте booksnew.ru вчера."
        result = self.splitter.split(text, lang="ru")
        self.assertTrue(len(result) >= 1)

    def test_09_long_syntactic_construction(self):
        """9. Длинная синтаксическая конструкция (пример из задачи)."""
        text = (
            "Недаром её отец и ряд специалистов считали, что штурмовая группа при огневом "
            "контакте с противником в наступлении сохраняет свою боеспособность в течение нескольких часов."
        )
        result = self.splitter.split(text, lang="ru")
        # В текущей реализации целое предложение возвращается одним блоком
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], text)


if __name__ == "__main__":
    unittest.main()
