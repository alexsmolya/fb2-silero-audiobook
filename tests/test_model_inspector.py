"""
Тесты для модуля инспекции моделей src.core.model_inspector и CLI tools.model_info.
"""

import json
from pathlib import Path
from unittest.mock import patch

from src.core.model_inspector import (
    ModelInfo,
    _calculate_sha256,
    _format_size,
    find_silero_model_path,
    get_silero_model_info,
)
from tools.model_info import format_text_output


def test_format_size():
    assert _format_size(1048576) == "1,048,576 bytes (1.0 MB)"


def test_calculate_sha256(tmp_path: Path):
    test_file = tmp_path / "sample.txt"
    test_file.write_bytes(b"hello silero")
    expected = "70c1c0f7ca273f589eef5ed78d0a8ad1e6daf9b3eb8b62d81bc40fe59a903909"
    assert _calculate_sha256(test_file) == expected


def test_get_silero_model_info_success():
    info = get_silero_model_info("v5_5_ru")
    assert info.exists is True
    assert info.model_id == "v5_5_ru"
    assert info.filename == "v5_5_ru_ru.pt"
    assert info.sha256 == "50081637b602126ee06cb3bc8a744d25651d2da149ee8864b9a379bfdd934437"
    assert info.path is not None
    assert info.size_bytes > 0
    assert info.error is None


def test_get_silero_model_info_missing():
    with patch("src.core.model_inspector.find_silero_model_path", return_value=None):
        info = get_silero_model_info("non_existent_model")
        assert info.exists is False
        assert info.model_id == "non_existent_model"
        assert info.error is not None
        assert info.filename is None
        assert info.sha256 is None


def test_format_text_output_success():
    info = ModelInfo(
        exists=True,
        model_id="v5_5_ru",
        filename="v5_5_ru_ru.pt",
        path="/path/to/model.pt",
        size_bytes=100,
        size_formatted="100 bytes (0.0 MB)",
        sha256="abc123hash",
        modified="2026-08-06T12:00:00+00:00",
    )
    output = format_text_output(info)
    assert "Silero model" in output
    assert "ID: v5_5_ru" in output
    assert "Filename: v5_5_ru_ru.pt" in output
    assert "SHA256: abc123hash" in output


def test_format_text_output_missing():
    info = ModelInfo(
        exists=False,
        model_id="v5_5_ru",
        error="Model file not found",
    )
    output = format_text_output(info)
    assert "Silero model" in output
    assert "Status: Not found" in output
    assert "Error: Model file not found" in output
