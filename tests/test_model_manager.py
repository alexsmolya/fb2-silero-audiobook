"""
Тесты для модуля src.core.model_manager (ModelManager) и CLI tools.model_manager.
"""

import json
from pathlib import Path
from unittest.mock import patch

import pytest
from src.core.model_manager import ModelManager, ModelMetadata
from tools.model_manager import format_model_entry, format_models_list


@pytest.fixture
def temp_models_dir(tmp_path: Path) -> Path:
    models_dir = tmp_path / "models"
    models_dir.mkdir()
    return models_dir


def test_empty_models_directory(temp_models_dir: Path):
    with patch("src.core.model_manager.find_silero_model_path", return_value=None):
        mm = ModelManager(models_dir=temp_models_dir)
        models = mm.list_local_models(include_legacy=False)
        assert models == []
        assert mm.get_active_model() is None
        assert mm.get_model_info("v5_5_ru") is None


def test_single_model_present(temp_models_dir: Path):
    mm = ModelManager(models_dir=temp_models_dir)
    # Создаем папку модели с metadata.json и dummy .pt файлом
    m1_dir = temp_models_dir / "v5_5_ru"
    m1_dir.mkdir()
    pt_file = m1_dir / "v5_5_ru_ru.pt"
    pt_file.write_bytes(b"dummy model binary data")

    meta = mm.create_model_metadata(
        model_id="v5_5_ru",
        filename="v5_5_ru_ru.pt",
        sha256="dummyhash123",
        size_bytes=pt_file.stat().st_size,
        source="user_models",
        active=True,
    )

    assert meta.valid is True
    assert meta.model_id == "v5_5_ru"
    assert meta.filename == "v5_5_ru_ru.pt"
    assert meta.active is True

    models = mm.list_local_models(include_legacy=False)
    assert len(models) == 1
    assert models[0].model_id == "v5_5_ru"
    assert models[0].active is True

    active = mm.get_active_model()
    assert active is not None
    assert active.model_id == "v5_5_ru"


def test_multiple_models_present(temp_models_dir: Path):
    mm = ModelManager(models_dir=temp_models_dir)

    # Модель 1 (v5_5_ru)
    m1_dir = temp_models_dir / "v5_5_ru"
    m1_dir.mkdir()
    (m1_dir / "model.pt").write_bytes(b"model 1 binary")
    mm.create_model_metadata(
        model_id="v5_5_ru",
        filename="model.pt",
        sha256="hash1",
        size_bytes=14,
        active=False,
    )

    # Модель 2 (v5_6_ru)
    m2_dir = temp_models_dir / "v5_6_ru"
    m2_dir.mkdir()
    (m2_dir / "model.pt").write_bytes(b"model 2 binary")
    mm.create_model_metadata(
        model_id="v5_6_ru",
        filename="model.pt",
        sha256="hash2",
        size_bytes=14,
        active=True,
    )

    models = mm.list_local_models(include_legacy=False)
    assert len(models) == 2

    model_ids = {m.model_id for m in models}
    assert model_ids == {"v5_5_ru", "v5_6_ru"}

    active = mm.get_active_model()
    assert active is not None
    assert active.model_id == "v5_6_ru"


def test_corrupted_metadata_with_pt_file(temp_models_dir: Path):
    mm = ModelManager(models_dir=temp_models_dir)
    m_dir = temp_models_dir / "v5_5_ru"
    m_dir.mkdir()
    (m_dir / "v5_5_ru_ru.pt").write_bytes(b"some audio model data")

    # Пишем битый JSON
    (m_dir / "metadata.json").write_text("{corrupted json string", encoding="utf-8")

    models = mm.list_local_models(include_legacy=False)
    assert len(models) == 1
    m = models[0]
    assert m.model_id == "v5_5_ru"
    assert m.valid is False
    assert "поврежден" in m.error
    assert m.filename == "v5_5_ru_ru.pt"
    assert m.sha256 is not None  # Восстановлено из файла .pt


def test_corrupted_metadata_missing_pt_file(temp_models_dir: Path):
    mm = ModelManager(models_dir=temp_models_dir)
    m_dir = temp_models_dir / "v5_5_ru"
    m_dir.mkdir()
    (m_dir / "metadata.json").write_text("{corrupted json", encoding="utf-8")

    models = mm.list_local_models(include_legacy=False)
    assert len(models) == 1
    m = models[0]
    assert m.valid is False
    assert "отсутствует" in m.error


def test_missing_pt_file(temp_models_dir: Path):
    mm = ModelManager(models_dir=temp_models_dir)
    m_dir = temp_models_dir / "v5_5_ru"
    m_dir.mkdir()

    # metadata.json ссылается на небудущий файл
    meta_dict = {
        "model_id": "v5_5_ru",
        "filename": "missing.pt",
        "sha256": "abc",
        "size": 100,
        "active": True,
    }
    (m_dir / "metadata.json").write_text(json.dumps(meta_dict), encoding="utf-8")

    models = mm.list_local_models(include_legacy=False)
    assert len(models) == 1
    m = models[0]
    assert m.valid is False
    assert "отсутствует" in m.error


def test_detect_legacy_models(temp_models_dir: Path, tmp_path: Path):
    dummy_legacy_pt = tmp_path / "v5_5_ru_ru.pt"
    dummy_legacy_pt.write_bytes(b"legacy silero model content")

    with patch(
        "src.core.model_manager.find_silero_model_path",
        return_value=dummy_legacy_pt,
    ):
        mm = ModelManager(models_dir=temp_models_dir)
        legacy = mm.detect_legacy_models()
        assert len(legacy) == 1
        assert legacy[0].is_legacy is True
        assert legacy[0].source == "legacy_venv"
        assert legacy[0].model_id == "v5_5_ru"

        all_models = mm.list_local_models(include_legacy=True)
        assert len(all_models) == 1
        assert all_models[0].is_legacy is True


def test_cli_formatters():
    m = ModelMetadata(
        model_id="v5_5_ru",
        filename="v5_5_ru_ru.pt",
        path="/path/to/model",
        size_bytes=1000,
        size_formatted="1,000 bytes",
        sha256="hash123",
        source="user_models",
        active=True,
    )
    formatted_entry = format_model_entry(m)
    assert "[Active]" in formatted_entry
    assert "ID: v5_5_ru" in formatted_entry
    assert "SHA256: hash123" in formatted_entry

    formatted_list = format_models_list([m])
    assert "Local Silero Models (1 found):" in formatted_list
