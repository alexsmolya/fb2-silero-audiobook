"""Regression tests for target-final-silence pause adaptation."""

from __future__ import annotations

import asyncio
import struct
import wave
from pathlib import Path
from types import SimpleNamespace

import pytest

from src.core.pause_policy import (
    BoundaryType,
    CHAPTER_TARGET_FINAL_SILENCE,
    EDGE_MAX_MEASURED_SECONDS,
    EdgeSilence,
    classify_boundary,
    measure_wav_edge_silence,
    read_edge_silence,
    required_padding,
    target_pause,
    write_edge_silence,
)
from src.core.pipeline import Pipeline


def _write_wav(path: Path, sections: list[tuple[float, int]]) -> None:
    with wave.open(str(path), "wb") as stream:
        stream.setnchannels(1)
        stream.setsampwidth(2)
        stream.setframerate(22050)
        for seconds, value in sections:
            stream.writeframes(
                struct.pack("<h", value) * round(22050 * seconds)
            )


def test_enough_existing_silence_adds_nothing() -> None:
    padding = required_padding(
        0.30,
        EdgeSilence(0.0, 0.22),
        EdgeSilence(0.11, 0.0),
    )
    assert padding == 0.0


def test_only_silence_deficit_is_added() -> None:
    padding = required_padding(
        0.45,
        EdgeSilence(0.0, 0.12),
        EdgeSilence(0.08, 0.0),
    )
    assert padding == pytest.approx(0.25)


def test_padding_is_never_negative_and_missing_metadata_is_conservative() -> None:
    assert required_padding(-1.0, None, None) == 0.0
    assert required_padding(0.45, None, None) == 0.45
    assert required_padding(2.10, None, None, fallback_padding=1.5) == 1.5


@pytest.mark.parametrize(
    ("marker", "previous", "current", "expected"),
    [
        ("sentence", "Обычная фраза.", "Следующая.", BoundaryType.ORDINARY),
        ("sentence", "Вопрос?", "Ответ.", BoundaryType.QUESTION),
        ("sentence", "Возглас!", "Ответ.", BoundaryType.EXCLAMATION),
        ("sentence", "Он замолчал…", "Потом ответил.", BoundaryType.ELLIPSIS),
        ("sentence", "Он спросил.", "— Да.", BoundaryType.DIALOGUE),
        ("sentence", "— Да.", "Он кивнул.", BoundaryType.DIALOGUE),
        ("paragraph", "Конец.", "Новый абзац.", BoundaryType.PARAGRAPH),
        ("title_body", "Глава 1", "Первый абзац.", BoundaryType.TITLE_BODY),
        ("chapter_start", "", "Глава 1", BoundaryType.CHAPTER_START),
    ],
)
def test_boundary_classification(marker, previous, current, expected) -> None:
    assert classify_boundary(marker, previous, current) == expected


def test_policy_has_distinct_structural_and_punctuation_targets() -> None:
    assert target_pause(BoundaryType.ORDINARY) == 0.30
    assert target_pause(BoundaryType.QUESTION) > target_pause(BoundaryType.ORDINARY)
    assert target_pause(BoundaryType.EXCLAMATION) > target_pause(BoundaryType.ORDINARY)
    assert target_pause(BoundaryType.PARAGRAPH) > target_pause(BoundaryType.ORDINARY)
    assert target_pause(BoundaryType.TITLE_BODY) > target_pause(BoundaryType.PARAGRAPH)
    assert target_pause(BoundaryType.CHAPTER_START) == 0.0
    assert CHAPTER_TARGET_FINAL_SILENCE == 2.10
    assert target_pause(BoundaryType.ORDINARY, ordinary_target=0.4) == pytest.approx(0.4)
    assert target_pause(BoundaryType.PARAGRAPH, ordinary_target=0.4) == pytest.approx(0.55)


def test_wav_edge_measurement_is_read_only_and_does_not_clip_speech(
    tmp_path: Path,
) -> None:
    source = tmp_path / "segment.wav"
    _write_wav(source, [(0.10, 0), (0.20, 4000), (0.15, 0)])
    original = source.read_bytes()

    edge = measure_wav_edge_silence(source)

    assert edge is not None
    assert edge.leading_seconds == pytest.approx(0.10, abs=1 / 22050)
    assert edge.trailing_seconds == pytest.approx(0.15, abs=1 / 22050)
    assert source.read_bytes() == original


def test_detector_requires_minimum_silence_and_bounds_measurement(
    tmp_path: Path,
) -> None:
    source = tmp_path / "bounded.wav"
    _write_wav(source, [(0.02, 0), (0.10, 4000), (2.0, 0)])

    edge = measure_wav_edge_silence(source)

    assert edge is not None
    assert edge.leading_seconds == 0.0
    assert edge.trailing_seconds == EDGE_MAX_MEASURED_SECONDS


def test_edge_sidecar_round_trip_and_invalid_data(tmp_path: Path) -> None:
    audio = tmp_path / "segment.mp3"
    write_edge_silence(audio, EdgeSilence(0.12, 0.34))
    assert read_edge_silence(audio) == EdgeSilence(0.12, 0.34)

    sidecar = audio.with_suffix(".mp3.pause.json")
    sidecar.write_text('{"leading_seconds": -1, "trailing_seconds": 2}', encoding="utf-8")
    assert read_edge_silence(audio) is None


def test_pipeline_keeps_comment_before_and_after_targets_in_correct_order(
    tmp_path: Path,
) -> None:
    chapter_dir = tmp_path / "chapter"
    chapter_dir.mkdir()
    for index in range(3):
        (chapter_dir / f"seg_{index:06d}.mp3").write_bytes(b"audio")

    observed = {}

    class Assembler:
        def assemble_chapter(self, segments, output_path, cancel_event=None):
            observed["segments"] = segments
            return output_path

    pipeline = Pipeline.__new__(Pipeline)
    pipeline.config = SimpleNamespace(tts_config=SimpleNamespace(
        pause_between_sentences=0.3,
        pause_before_comment=1.0,
        pause_after_comment=0.7,
    ))
    pipeline._temp_dir = tmp_path
    pipeline.audio_assembler = Assembler()

    asyncio.run(pipeline._assemble_chapter_audio(
        ["Первое.", "Второе."],
        ["Комментарий.", None],
        chapter_dir,
        0,
        boundary_markers=["chapter_start", "sentence"],
    ))

    assert [target for _path, target in observed["segments"]] == [0.0, 1.0, 0.7]
