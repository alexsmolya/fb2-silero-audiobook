"""Regression tests for FB2 chapter structure."""

from __future__ import annotations

from pathlib import Path

from src.core.fb2_parser import FB2Parser


def test_structural_title_repeated_as_first_body_paragraph_is_spoken_once(
    tmp_path: Path,
) -> None:
    source = tmp_path / "duplicate-title.fb2"
    source.write_text(
        """<?xml version="1.0" encoding="utf-8"?>
<FictionBook xmlns="http://www.gribuser.ru/xml/fictionbook/2.0">
  <description><title-info><book-title>Test</book-title><lang>ru</lang></title-info></description>
  <body><section>
    <title><p>Глава 7</p></title>
    <p>  глава   7  </p>
    <p>Первый абзац.</p>
    <p>Глава 7</p>
  </section></body>
</FictionBook>
""",
        encoding="utf-8",
    )

    chapter = FB2Parser().parse(source).chapters[0]

    assert chapter.title == "Глава 7"
    assert chapter.paragraphs == ["Глава 7", "Первый абзац.", "Глава 7"]
