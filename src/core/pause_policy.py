"""Boundary-aware target-final-silence policy and lightweight edge analysis."""

from __future__ import annotations

import array
import json
import math
import re
import sys
import wave
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Optional


class BoundaryType(StrEnum):
    CHAPTER_START = "chapter_start"
    ORDINARY = "ordinary"
    QUESTION = "question"
    EXCLAMATION = "exclamation"
    ELLIPSIS = "ellipsis"
    DIALOGUE = "dialogue"
    PARAGRAPH = "paragraph"
    TITLE_BODY = "title_body"


TARGET_FINAL_SILENCE = {
    BoundaryType.CHAPTER_START: 0.0,
    BoundaryType.ORDINARY: 0.30,
    BoundaryType.QUESTION: 0.45,
    BoundaryType.EXCLAMATION: 0.38,
    BoundaryType.ELLIPSIS: 0.45,
    BoundaryType.DIALOGUE: 0.38,
    BoundaryType.PARAGRAPH: 0.45,
    BoundaryType.TITLE_BODY: 0.75,
}

CHAPTER_TARGET_FINAL_SILENCE = 2.10
EDGE_THRESHOLD_DB = -45.0
EDGE_MIN_DURATION_SECONDS = 0.04
EDGE_MAX_MEASURED_SECONDS = 1.50
_CLOSING_PUNCTUATION_RE = re.compile(r"[\s»”\"')\]]+$")


@dataclass(frozen=True)
class EdgeSilence:
    """Measured leading and trailing digital/near-digital silence."""

    leading_seconds: float
    trailing_seconds: float

    def scaled_for_speed(self, speed: float) -> "EdgeSilence":
        safe_speed = speed if math.isfinite(speed) and speed > 0 else 1.0
        return EdgeSilence(
            leading_seconds=self.leading_seconds / safe_speed,
            trailing_seconds=self.trailing_seconds / safe_speed,
        )


def classify_boundary(
    structural_boundary: str,
    previous_text: str,
    current_text: str,
) -> BoundaryType:
    """Classify a boundary, giving FB2 structure priority over punctuation."""
    if structural_boundary == BoundaryType.CHAPTER_START:
        return BoundaryType.CHAPTER_START
    if structural_boundary == BoundaryType.TITLE_BODY:
        return BoundaryType.TITLE_BODY
    if structural_boundary == BoundaryType.PARAGRAPH:
        return BoundaryType.PARAGRAPH

    if current_text.lstrip().startswith(("—", "–")) or previous_text.lstrip().startswith(
        ("—", "–"),
    ):
        return BoundaryType.DIALOGUE

    terminal = _CLOSING_PUNCTUATION_RE.sub("", previous_text)
    if terminal.endswith(("?..", "!..", "...", "…")):
        return BoundaryType.ELLIPSIS
    if terminal.endswith(("⁈", "?!", "!?", "?")):
        return BoundaryType.QUESTION
    if terminal.endswith("!"):
        return BoundaryType.EXCLAMATION
    return BoundaryType.ORDINARY


def target_pause(
    boundary: BoundaryType,
    ordinary_target: float = TARGET_FINAL_SILENCE[BoundaryType.ORDINARY],
) -> float:
    """Return final-silence target, preserving the user's ordinary baseline."""
    if boundary == BoundaryType.CHAPTER_START:
        return 0.0
    if not math.isfinite(ordinary_target):
        ordinary_target = TARGET_FINAL_SILENCE[BoundaryType.ORDINARY]
    baseline_delta = ordinary_target - TARGET_FINAL_SILENCE[BoundaryType.ORDINARY]
    return max(0.0, TARGET_FINAL_SILENCE[boundary] + baseline_delta)


def required_padding(
    target_seconds: float,
    previous_edge: Optional[EdgeSilence],
    current_edge: Optional[EdgeSilence],
    *,
    fallback_padding: Optional[float] = None,
) -> float:
    """Return only the non-negative silence deficit between adjacent audio."""
    target = max(0.0, target_seconds) if math.isfinite(target_seconds) else 0.0
    if previous_edge is None or current_edge is None:
        fallback = target if fallback_padding is None else fallback_padding
        return max(0.0, fallback) if math.isfinite(fallback) else 0.0
    existing = max(0.0, previous_edge.trailing_seconds) + max(
        0.0, current_edge.leading_seconds,
    )
    return max(0.0, target - existing)


def measure_wav_edge_silence(
    path: Path,
    *,
    threshold_db: float = EDGE_THRESHOLD_DB,
    minimum_duration: float = EDGE_MIN_DURATION_SECONDS,
    maximum_edge: float = EDGE_MAX_MEASURED_SECONDS,
) -> Optional[EdgeSilence]:
    """Measure PCM WAV edges without trimming or modifying the source audio."""
    try:
        with wave.open(str(path), "rb") as stream:
            channels = stream.getnchannels()
            sample_width = stream.getsampwidth()
            sample_rate = stream.getframerate()
            frame_count = stream.getnframes()
            frames = stream.readframes(frame_count)
    except (OSError, EOFError, wave.Error):
        return None

    if channels < 1 or sample_width != 2 or sample_rate <= 0 or not frames:
        return None

    samples = array.array("h")
    samples.frombytes(frames)
    if sys.byteorder != "little":
        samples.byteswap()
    threshold = 32767 * (10 ** (threshold_db / 20.0))
    minimum_frames = max(1, round(minimum_duration * sample_rate))
    decoded_frames = len(samples) // channels

    def frame_is_silent(frame_index: int) -> bool:
        start = frame_index * channels
        return all(
            abs(value) <= threshold
            for value in samples[start:start + channels]
        )

    leading_frames = 0
    for frame_index in range(decoded_frames):
        if not frame_is_silent(frame_index):
            break
        leading_frames += 1

    trailing_frames = 0
    for frame_index in range(decoded_frames - 1, -1, -1):
        if not frame_is_silent(frame_index):
            break
        trailing_frames += 1

    def seconds(frames_at_edge: int) -> float:
        if frames_at_edge < minimum_frames:
            return 0.0
        return min(maximum_edge, frames_at_edge / sample_rate)

    return EdgeSilence(seconds(leading_frames), seconds(trailing_frames))


def pause_metadata_path(audio_path: Path) -> Path:
    return audio_path.with_suffix(audio_path.suffix + ".pause.json")


def write_edge_silence(audio_path: Path, edge: EdgeSilence) -> Path:
    """Write small sidecar metadata next to a generated audio segment."""
    path = pause_metadata_path(audio_path)
    path.write_text(
        json.dumps({
            "version": 1,
            "leading_seconds": round(max(0.0, edge.leading_seconds), 6),
            "trailing_seconds": round(max(0.0, edge.trailing_seconds), 6),
            "threshold_db": EDGE_THRESHOLD_DB,
            "minimum_duration_seconds": EDGE_MIN_DURATION_SECONDS,
        }, ensure_ascii=False),
        encoding="utf-8",
    )
    return path


def read_edge_silence(audio_path: Path) -> Optional[EdgeSilence]:
    """Read and validate edge metadata, returning None for unsafe sidecars."""
    try:
        data = json.loads(pause_metadata_path(audio_path).read_text(encoding="utf-8"))
        leading = float(data["leading_seconds"])
        trailing = float(data["trailing_seconds"])
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError):
        return None
    if not all(math.isfinite(value) and value >= 0 for value in (leading, trailing)):
        return None
    return EdgeSilence(
        min(leading, EDGE_MAX_MEASURED_SECONDS),
        min(trailing, EDGE_MAX_MEASURED_SECONDS),
    )
