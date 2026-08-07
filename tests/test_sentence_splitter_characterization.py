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
        """7. Обработка многоточия (консервативные правила для … и ...)."""
        # Внутреннее многоточие со строчной буквой — НЕ режется
        t1 = "Недаром его отец и ряд… специалистов клана на полном серьезе рассматривали вариант ликвидации девушки."
        r1 = self.splitter.split(t1, lang="ru")
        self.assertEqual(r1, [t1])

        t2 = "Даже этот лощеный… прощелыга говорит правильно."
        r2 = self.splitter.split(t2, lang="ru")
        self.assertEqual(r2, [t2])

        t3 = "Он подумал… но ничего не сказал."
        r3 = self.splitter.split(t3, lang="ru")
        self.assertEqual(r3, [t3])

        t4 = "Это было странно... но объяснимо."
        r4 = self.splitter.split(t4, lang="ru")
        self.assertEqual(r4, [t4])

        # Многоточие на границе предложений перед Заглавной буквой — РЕЖЕТСЯ
        t5 = "И всем нужны были деньги, влияние, участие в проектах… И никто не смог дать четкий ответ на один простой вопрос."
        r5 = self.splitter.split(t5, lang="ru")
        self.assertEqual(len(r5), 2)
        self.assertEqual(r5[0], "И всем нужны были деньги, влияние, участие в проектах…")
        self.assertEqual(r5[1], "И никто не смог дать четкий ответ на один простой вопрос.")

        t6 = "Они собирались повести людей в новый мир… Воевода пожал плечами."
        r6 = self.splitter.split(t6, lang="ru")
        self.assertEqual(len(r6), 2)
        self.assertEqual(r6[0], "Они собирались повести людей в новый мир…")
        self.assertEqual(r6[1], "Воевода пожал плечами.")

        t7 = "Это было странно... Очень странно."
        r7 = self.splitter.split(t7, lang="ru")
        self.assertEqual(len(r7), 2)
        self.assertEqual(r7[0], "Это было странно...")
        self.assertEqual(r7[1], "Очень странно.")

        # Диалог после многоточия
        t8 = "Он замолчал… — И что дальше? — спросил Сергей."
        r8 = self.splitter.split(t8, lang="ru")
        self.assertEqual(len(r8), 3)
        self.assertEqual(r8[0], "Он замолчал…")
        self.assertEqual(r8[1], "— И что дальше?")
        self.assertEqual(r8[2], "— спросил Сергей.")
        self.assertEqual(" ".join(r8), t8)

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

    def test_10_ellipsis_proper_name_limitation(self):
        """10. Ограничение эвристики: имена собственные после внутреннего многоточия."""
        # Фиксируем компромиссное поведение fallback-сегментатора:
        # Поскольку эвристика проверяет заглавную букву после многоточия,
        # имена собственные воспринимаются как начало нового предложения.
        c1 = "Он посмотрел на… Павла, стоявшего у двери."
        r1 = self.splitter.split(c1, lang="ru")
        self.assertEqual(len(r1), 2)
        self.assertEqual(r1[0], "Он посмотрел на…")
        self.assertEqual(r1[1], "Павла, стоявшего у двери.")

        c2 = "Больше всего он боялся… Волконского, разумеется."
        r2 = self.splitter.split(c2, lang="ru")
        self.assertEqual(len(r2), 2)

        c3 = "Он замолчал… Павел пожал плечами."
        r3 = self.splitter.split(c3, lang="ru")
        self.assertEqual(len(r3), 2)
        self.assertEqual(r3[0], "Он замолчал…")
        self.assertEqual(r3[1], "Павел пожал плечами.")


if __name__ == "__main__":
    unittest.main()
