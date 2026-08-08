"""
Модуль разбиения текста на предложения с учётом языка.
Поддерживает русский, английский, японский и китайский языки.
"""

from __future__ import annotations

import logging
import re
from typing import Dict, Callable, List

logger = logging.getLogger(__name__)


class SentenceSplitter:
    """Разбиение текста на предложения с учётом языка.

    Для русского и английского использует spacy (если модель загружена),
    для японского и китайского — кастомные правила на основе регулярных выражений.
    """

    def __init__(self):
        self._splitters: Dict[str, Callable[[str], List[str]]] = {
            "ru": self._split_ru,
            "en": self._split_en,
            "ja": self._split_ja,
            "zh": self._split_zh,
        }
        self._nlp_ru = None
        self._nlp_en = None
        self._nlp_ru_load_attempted = False
        self._nlp_en_load_attempted = False

    def split(self, text: str, lang: str = "ru") -> List[str]:
        """Разбиение текста на предложения.

        Args:
            text: Исходный текст.
            lang: Язык текста (ru, en, ja, zh).

        Returns:
            Список предложений.
        """
        if not text or not text.strip():
            return []

        splitter = self._splitters.get(lang, self._split_fallback)
        sentences = splitter(text)
        # Знаки пунктуации сами по себе задают границу/паузу, но не являются
        # речью и не должны запускать TTS inference.
        sentences = [
            sentence.strip()
            for sentence in sentences
            if self.has_speech_content(sentence)
        ]
        return sentences

    def split_paragraphs(
        self,
        paragraphs: List[str],
        lang: str = "ru",
    ) -> List[str]:
        """Split each structural paragraph independently.

        Keeping paragraphs separate until this point prevents an FB2 title or
        paragraph ending from being merged into the next TTS segment.
        """
        segments: List[str] = []
        for paragraph in paragraphs:
            segments.extend(self.split(paragraph, lang))
        return segments

    def split_chapter(
        self,
        title: str,
        paragraphs: List[str],
        lang: str = "ru",
    ) -> List[str]:
        """Keep a structural title separate, then split body paragraphs."""
        title_parts = [
            " ".join(part.split())
            for part in title.splitlines()
            if part.strip()
        ]
        leading = paragraphs[:len(title_parts)]
        has_structural_title = bool(title_parts) and len(leading) == len(title_parts) and all(
            " ".join(paragraph.split()).casefold() == part.casefold()
            for paragraph, part in zip(leading, title_parts)
        )
        if not has_structural_title:
            return self.split_paragraphs(paragraphs, lang)

        title_segments = self.split(" ".join(title_parts), lang)
        body_segments = self.split_paragraphs(paragraphs[len(title_parts):], lang)
        return title_segments + body_segments

    @staticmethod
    def has_speech_content(text: str) -> bool:
        """Return whether a fragment contains something pronounceable."""
        return any(character.isalnum() for character in text)

    def _load_spacy_ru(self):
        """Загрузка spacy модели для русского языка."""
        if self._nlp_ru_load_attempted:
            return self._nlp_ru is not None
        self._nlp_ru_load_attempted = True
        if self._nlp_ru is None:
            try:
                import spacy
                nlp = spacy.load("ru_core_news_sm")
                # Увеличиваем лимит длины текста: некоторые главы
                # "Братьев Карамазовых" >1M символов.
                # Для sentence-split'инга NER/parser не нужны,
                # поэтому высокий лимит безопасен.
                nlp.max_length = 10_000_000
                self._nlp_ru = nlp
                logger.info("Загружена spacy модель: ru_core_news_sm (max_length=10M)")
            except OSError:
                logger.warning(
                    "spacy модель ru_core_news_sm не найдена. "
                    "Установите: python -m spacy download ru_core_news_sm"
                )
                return False
        return True

    def _load_spacy_en(self):
        """Загрузка spacy модели для английского языка."""
        if self._nlp_en_load_attempted:
            return self._nlp_en is not None
        self._nlp_en_load_attempted = True
        if self._nlp_en is None:
            try:
                import spacy
                nlp = spacy.load("en_core_web_sm")
                nlp.max_length = 10_000_000
                self._nlp_en = nlp
                logger.info("Загружена spacy модель: en_core_web_sm (max_length=10M)")
            except OSError:
                logger.warning(
                    "spacy модель en_core_web_sm не найдена. "
                    "Установите: python -m spacy download en_core_web_sm"
                )
                return False
        return True

    def _split_ru(self, text: str) -> List[str]:
        """Разбиение русского текста на предложения."""
        if self._load_spacy_ru():
            doc = self._nlp_ru(text)
            return [sent.text for sent in doc.sents]
        return self._split_fallback(text)

    def _split_en(self, text: str) -> List[str]:
        """Разбиение английского текста на предложения."""
        if self._load_spacy_en():
            doc = self._nlp_en(text)
            return [sent.text for sent in doc.sents]
        return self._split_fallback(text)

    def _split_ja(self, text: str) -> List[str]:
        """Разбиение японского текста на предложения.

        Японские знаки конца предложения: 。！？
        """
        # Используем позитивный просмотр вперёд для сохранения знака
        pattern = r'[^。！？\n]+[。！？]?'
        sentences = re.findall(pattern, text)
        return [s.strip() for s in sentences if s.strip()]

    def _split_zh(self, text: str) -> List[str]:
        """Разбиение китайского текста на предложения.

        Китайские знаки конца предложения: 。！？
        Также поддерживаются полуширинные !?
        """
        pattern = r'[^。！？!?\n]+[。！？!?]?'
        sentences = re.findall(pattern, text)
        return [s.strip() for s in sentences if s.strip()]

    def _split_fallback(self, text: str) -> List[str]:
        """Универсальное разбиение на предложения (резервный алгоритм).

        Используется, если spacy модель не загружена.
        Поддерживает консервативную обработку Unicode (…)- и ASCII (...)-многоточий.
        """
        # 1. Первичное консервативное разбиение по многоточиям:
        # Режем по многоточию (… или ...) ТОЛЬКО если за ним через пробел(ы)
        # (и возможные тире/кавычки) следует Заглавная буква.
        #
        # Известное ограничение (Trade-off):
        # Внутреннее многоточие перед именем собственным (например, "посмотрел на… Павла")
        # без полного NLP-парсера будет разделено так же, как начало нового предложения
        # ("Он замолчал… Павел ушёл"), так как оба содержат заглавную букву.
        ellipsis_split_pattern = (
            r'(?<=[…])\s+(?=(?:[—–-]\s*)?[«"\'“”]?\s*[А-ЯЁA-Z])'
            r'|'
            r'(?<=\.\.\.)\s+(?=(?:[—–-]\s*)?[«"\'“”]?\s*[А-ЯЁA-Z])'
            r'|'
            r'(?<=[?!]\.\.)\s+(?=[А-ЯЁA-Z])'
            r'|'
            # Interrobang is a boundary only for an unambiguous next sentence.
            # A following dialogue dash is deliberately excluded so constructs
            # such as "Что⁈ — спросил он" remain intact.
            r'(?<=⁈)\s+(?=[«"\'“”]?\s*[А-ЯЁA-Z])'
        )
        chunks = re.split(ellipsis_split_pattern, text)

        # 2. Стандартное разбиение по одиночным знакам конца предложения [.!?。！？\n].
        # Используем (?<=(?<!\.)[.!?。！？\n])\s+, чтобы точка на конце многоточия (...) не вызывала ложного разрыва.
        std_pattern = r'(?<=(?<!\.)[.!?。！？\n])\s+'

        result = []
        for chunk in chunks:
            parts = re.split(std_pattern, chunk)
            for part in parts:
                sub_parts = [p.strip() for p in part.split("\n") if p.strip()]
                result.extend(sub_parts)
        return result
