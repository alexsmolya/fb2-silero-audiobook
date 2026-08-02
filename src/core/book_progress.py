"""Централизованный расчёт глобального прогресса обработки книги."""

from __future__ import annotations

from typing import Callable, Optional, Sequence


ProgressCallback = Callable[[str, float], None]


class BookProgressTracker:
    """Преобразует прогресс этапов и глав в монотонный диапазон 0.0..1.0."""

    PREPARATION_END = 0.03
    PARSING_END = 0.05
    CHAPTERS_END = 0.92
    FINAL_ASSEMBLY_END = 0.99

    CHAPTER_PREPARATION_SHARE = 0.03
    CHAPTER_TTS_END_SHARE = 0.93

    def __init__(self, callback: Optional[ProgressCallback] = None):
        self.callback = callback
        self.last_value = 0.0
        self._chapter_weights: tuple[float, ...] = ()
        self._chapter_offsets: tuple[float, ...] = (0.0,)

    def publish(self, message: str, value: float) -> float:
        """Опубликовать ограниченное монотонное значение ниже 100%."""
        value = min(self.FINAL_ASSEMBLY_END, max(0.0, float(value)))
        value = max(self.last_value, value)
        self.last_value = value
        if self.callback:
            self.callback(message, value)
        return value

    def complete(self, message: str) -> float:
        """Опубликовать 100%; вызывается только после проверки результата."""
        self.last_value = 1.0
        if self.callback:
            self.callback(message, 1.0)
        return 1.0

    def set_chapters(self, chapter_texts: Sequence[str]) -> None:
        """Распределить диапазон глав пропорционально объёму исходного текста."""
        lengths = [len(text.strip()) for text in chapter_texts]
        positive = [length for length in lengths if length > 0]
        fallback = (sum(positive) / len(positive)) if positive else 1.0
        weights = tuple(float(length or fallback) for length in lengths)
        total = sum(weights)
        if not weights:
            self._chapter_weights = ()
            self._chapter_offsets = (0.0,)
            return
        if total <= 0:
            weights = tuple(1.0 for _ in weights)
            total = float(len(weights))

        offsets = [0.0]
        accumulated = 0.0
        for weight in weights:
            accumulated += weight / total
            offsets.append(min(1.0, accumulated))
        offsets[-1] = 1.0
        self._chapter_weights = weights
        self._chapter_offsets = tuple(offsets)

    def chapter_bounds(self, chapter_index: int) -> tuple[float, float]:
        """Вернуть глобальные границы главы внутри диапазона обработки."""
        if not self._chapter_weights:
            return self.PARSING_END, self.CHAPTERS_END
        index = min(max(int(chapter_index), 0), len(self._chapter_weights) - 1)
        span = self.CHAPTERS_END - self.PARSING_END
        return (
            self.PARSING_END + self._chapter_offsets[index] * span,
            self.PARSING_END + self._chapter_offsets[index + 1] * span,
        )

    def chapter_preparation(self, chapter_index: int) -> float:
        start, end = self.chapter_bounds(chapter_index)
        return start + (end - start) * self.CHAPTER_PREPARATION_SHARE

    def chapter_tts(
        self,
        chapter_index: int,
        completed: int,
        total: int,
        segment_texts: Sequence[str] = (),
    ) -> float:
        """Учесть завершённые TTS-фрагменты по их фактическому объёму."""
        reported_total = max(int(total), 0)
        weights = [max(len(text.strip()), 1) for text in segment_texts]
        if reported_total > len(weights):
            fallback = (sum(weights) / len(weights)) if weights else 1.0
            weights.extend([fallback] * (reported_total - len(weights)))
        effective_total = max(reported_total, len(weights), 1)
        if len(weights) < effective_total:
            weights.extend([1.0] * (effective_total - len(weights)))

        done = min(max(int(completed), 0), effective_total)
        fraction = sum(weights[:done]) / max(sum(weights), 1.0)
        start, end = self.chapter_bounds(chapter_index)
        chapter_span = end - start
        tts_start = start + chapter_span * self.CHAPTER_PREPARATION_SHARE
        tts_end = start + chapter_span * self.CHAPTER_TTS_END_SHARE
        return tts_start + (tts_end - tts_start) * fraction

    def chapter_complete(self, chapter_index: int) -> float:
        return self.chapter_bounds(chapter_index)[1]

    def final_assembly(self, completed: int = 0, total: int = 1) -> float:
        """Отобразить подготовку входов финальной склейки, не достигая 99%."""
        fraction = min(1.0, max(0.0, completed / max(total, 1)))
        preparation_end = self.CHAPTERS_END + (
            self.FINAL_ASSEMBLY_END - self.CHAPTERS_END
        ) * 0.45
        return self.CHAPTERS_END + (
            preparation_end - self.CHAPTERS_END
        ) * fraction
