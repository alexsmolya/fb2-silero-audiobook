"""Tests for the structured deterministic TTS preprocessing compiler."""

from __future__ import annotations

import json
from pathlib import Path

from src.core.fb2_parser import BookMetadata, Chapter, ParsedBook
from src.core.sentence_splitter import SentenceSplitter
from src.core.tts_preprocessor import (
    TtsPreprocessor,
    detect_expressive_elongations,
    resolve_acronym,
    write_tts_artifacts,
)


def _book() -> ParsedBook:
    return ParsedBook(
        metadata=BookMetadata(title="Test book", lang="ru"),
        chapters=[Chapter(
            title="Глава 1",
            paragraphs=[
                "Глава 1",
                "Но все же события произошли. Вопросов не было.",
                "Дверной замок был закрыт.",
            ],
        )],
    )


def test_compile_preserves_structure_and_records_changes() -> None:
    original = _book()
    compiler = TtsPreprocessor(backend="silero")

    normalized = compiler.compile_book(original)

    assert original.chapters[0].title == "Глава 1"
    assert original.chapters[0].paragraphs[1] == "Но все же события произошли. Вопросов не было."
    assert normalized.chapters[0].title == "Глава первая"
    assert normalized.chapters[0].paragraphs[1].startswith("Но всё же")
    assert "н+е было" in normalized.chapters[0].paragraphs[1]
    assert normalized.chapters[0].paragraph_ids == [
        "ch-0001-p-0001", "ch-0001-p-0002", "ch-0001-p-0003",
    ]
    assert any(change.rule_id == "phrase.ne_bylo" for change in normalized.changes)


def test_artifacts_are_traceable_and_markdown_is_not_backend_input(tmp_path: Path) -> None:
    normalized = TtsPreprocessor(backend="silero").compile_book(_book())
    segments = [
        {
            "segment_id": "ch-0001-s-0001",
            "source_paragraph": "ch-0001-p-0002",
            "chapter": 1,
            "paragraph": 2,
            "boundary_before": "chapter_start",
            "text": "Но всё же события произошли.",
        },
    ]

    script_path, changes_path = write_tts_artifacts(
        normalized, tmp_path, "book", segments=segments,
    )

    script = script_path.read_text(encoding="utf-8")
    payload = json.loads(changes_path.read_text(encoding="utf-8"))
    assert "ch-0001-p-0002" in script
    assert "ch-0001-s-0001" in script
    assert payload["segments"][0]["source_paragraph"] == "ch-0001-p-0002"
    assert payload["changes"][0]["rule_id"]
    assert "<!-- generated" in script


def test_context_rules_keep_required_negative_controls() -> None:
    compiler = TtsPreprocessor(backend="silero")

    assert compiler.compile_book(ParsedBook(
        metadata=BookMetadata(lang="ru"),
        chapters=[Chapter(paragraphs=["Старый замок стоял на холме."])]
    )).chapters[0].paragraphs[0] == "Старый замок стоял на холме."
    assert compiler.compile_book(ParsedBook(
        metadata=BookMetadata(lang="ru"),
        chapters=[Chapter(paragraphs=["Дверной замок был закрыт."])]
    )).chapters[0].paragraphs[0] == "Дверной зам+ок был закрыт."
    assert compiler.compile_book(ParsedBook(
        metadata=BookMetadata(lang="ru"),
        chapters=[Chapter(paragraphs=["Замок явно не желал открываться."])]
    )).chapters[0].paragraphs[0] == "Зам+ок явно не желал открываться."
    assert compiler.compile_book(ParsedBook(
        metadata=BookMetadata(lang="ru"),
        chapters=[Chapter(paragraphs=["Ключ, но замок послушно отозвался."])]
    )).chapters[0].paragraphs[0] == "Ключ, но зам+ок послушно отозвался."
    assert compiler.compile_book(ParsedBook(
        metadata=BookMetadata(lang="ru"),
        chapters=[Chapter(paragraphs=["В сторону стены он не смотрел."])]
    )).chapters[0].paragraphs[0] == "В сторону стен+ы он не смотрел."


def test_confirmed_journal_cases_are_narrow_and_deterministic() -> None:
    compiler = TtsPreprocessor(backend="silero")
    cases = {
        "обреченно": "обречённо",
        "два с половиной часа": "два с половиной час+а",
        "набралось": "набрал+ось",
        "никого не было": "никого н+е было",
        "вопросов не было": "вопросов н+е было",
        "А потом стало тихо.": "А пот+ом стало тихо.",
        "открывать глаза": "открывать глаз+а",
        "В среду встретимся.": "В ср+еду встретимся.",
        "дверной замок": "дверной зам+ок",
        "с королевской статью": "с королевской ст+атью",
        "не с чем": "н+е с чем",
        "Я высоты боюсь": "Я высот+ы боюсь",
        "пока стрелку не надоест": "пока стрелк+у не надоест",
        "хлопок вышибного заряда": "хлоп+ок вышибного заряда",
        "в сторону стены": "в сторону стен+ы",
        "четверо нападавших": "четверо напад+авших",
        "представители великих родов": "представители великих род+ов",
        "красноте лица": "красноте лиц+а",
    }
    for original, expected in cases.items():
        result = compiler.compile_book(ParsedBook(
            metadata=BookMetadata(lang="ru"),
            chapters=[Chapter(paragraphs=[original])],
        )).chapters[0].paragraphs[0]
        assert result == expected, original

    assert compiler.compile_book(ParsedBook(
        metadata=BookMetadata(lang="ru"),
        chapters=[Chapter(paragraphs=["холодным потом"])]
    )).chapters[0].paragraphs[0] == "холодным потом"
    assert compiler.compile_book(ParsedBook(
        metadata=BookMetadata(lang="ru"),
        chapters=[Chapter(paragraphs=["А как ты проводишь свою среду?"])]
    )).chapters[0].paragraphs[0] == "А как ты проводишь свою ср+еду?"


def test_context_rules_preserve_lexical_tokens() -> None:
    import re

    compiler = TtsPreprocessor(backend="silero")
    cases = [
        "Дверной замок был закрыт.",
        "А как ты проводишь свою среду?",
        "с королевской статью повернув голову",
        "четверо нападавших вошли",
        "красноте лица не придавали значения",
    ]
    for source in cases:
        normalized = compiler.compile_book(ParsedBook(
            metadata=BookMetadata(lang="ru"),
            chapters=[Chapter(paragraphs=[source])],
        )).chapters[0].paragraphs[0]
        tokens = lambda text: re.findall(r"[а-яё]+", text.casefold().replace("+", ""))
        assert tokens(normalized) == tokens(source), (source, normalized)


def test_galitsyn_is_an_explicit_book_profile_override() -> None:
    default = TtsPreprocessor(backend="silero")
    profile = TtsPreprocessor(backend="silero", profile="book9")
    source = ParsedBook(
        metadata=BookMetadata(lang="ru"),
        chapters=[Chapter(paragraphs=["Галицын и Галитын"])]
    )
    assert default.compile_book(source).chapters[0].paragraphs[0] == "Галицын и Галитын"
    assert profile.compile_book(source).chapters[0].paragraphs[0] == "Гал+ицын и Галитын"


def test_silero_compiler_does_not_apply_russian_rules_to_other_languages() -> None:
    book = ParsedBook(
        metadata=BookMetadata(lang="en"),
        chapters=[Chapter(paragraphs=["Chapter 1 and все"])]
    )
    normalized = TtsPreprocessor(backend="silero").compile_book(book)
    assert normalized.chapters[0].paragraphs[0] == "Chapter 1 and все"
    assert normalized.changes == []


def test_segment_ids_can_follow_compiled_paragraphs() -> None:
    normalized = TtsPreprocessor(backend="silero").compile_book(_book())
    segments = SentenceSplitter().split_chapter_segments(
        normalized.chapters[0].title,
        normalized.chapters[0].paragraphs,
        "ru",
    )

    assert segments
    assert all(segment.source_paragraph_index is not None for segment in segments)
    assert [segment.source_paragraph_index for segment in segments[:2]] == [0, 2]


def test_expressive_elongation_is_detected_but_not_transformed() -> None:
    assert [item["text"] for item in detect_expressive_elongations(
        "о-о-о ааа Не-е-ет слово"
    )] == ["о-о-о", "ааа", "е-е-е"]
    assert detect_expressive_elongations("слово") == []


def test_acronym_resolution_requires_explicit_entries() -> None:
    assert resolve_acronym("СВУ", spell_letters=("СВУ",)).output == "С В У"
    assert resolve_acronym("СИБ", lexicalized_words=("СИБ",)).mode == "lexicalized_word"
    unknown = resolve_acronym("НВП")
    assert unknown.mode == "unknown"
    assert unknown.output == "НВП"
