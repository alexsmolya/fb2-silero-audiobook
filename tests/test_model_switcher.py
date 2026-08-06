"""
Unit-тесты для модуля src.core.model_switcher (ModelSwitcher).

Все вызовы PyTorch / PackageImporter полностью смокированы.
Все файлы создаются во временных папках pytest (tmp_path).
"""

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from src.core.model_manager import ModelManager, ModelMetadata
from src.core.model_switcher import (
    ModelSwitcher,
    RollbackResult,
    SmokeTestResult,
    SwitchResult,
)


def create_mock_model_dir(base_dir: Path, model_id: str, active: bool = False, filename: str = None) -> Path:
    """Хелпер создания структуры модели с metadata.json и .pt файлом."""
    m_dir = base_dir / model_id
    m_dir.mkdir(parents=True, exist_ok=True)
    pt_name = filename or f"{model_id}.pt"
    pt_file = m_dir / pt_name
    pt_file.write_bytes(b"mock pt data " + model_id.encode())

    import hashlib
    sha = hashlib.sha256(pt_file.read_bytes()).hexdigest()

    meta = {
        "model_id": model_id,
        "filename": pt_name,
        "sha256": sha,
        "size": len(pt_file.read_bytes()),
        "active": active,
        "installed_at": "2026-08-06T12:00:00+00:00",
    }
    (m_dir / "metadata.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    return m_dir


def test_dry_run_no_changes(tmp_path: Path):
    models_dir = tmp_path / "models"
    create_mock_model_dir(models_dir, "v5_5_ru", active=True)
    create_mock_model_dir(models_dir, "v5_6_ru", active=False)

    mm = ModelManager(models_dir=models_dir)
    switcher = ModelSwitcher(model_manager=mm)

    with patch.object(switcher, "run_smoke_test") as mock_smoke:
        mock_smoke.return_value = SmokeTestResult(success=True, status="success", model_id="v5_6_ru")
        res = switcher.activate_model("v5_6_ru", dry_run=True)

        assert res.success is True
        assert res.dry_run is True
        assert res.status == "ready"

        # Проверяем, что активной осталась v5_5_ru
        assert mm.get_active_model().model_id == "v5_5_ru"


def test_activate_valid_model(tmp_path: Path):
    models_dir = tmp_path / "models"
    create_mock_model_dir(models_dir, "v5_5_ru", active=True)
    create_mock_model_dir(models_dir, "v5_6_ru", active=False)

    mm = ModelManager(models_dir=models_dir)
    switcher = ModelSwitcher(model_manager=mm)

    with patch.object(switcher, "run_smoke_test") as mock_smoke:
        mock_smoke.return_value = SmokeTestResult(success=True, status="success", model_id="v5_6_ru")
        res = switcher.activate_model("v5_6_ru", dry_run=False)

        assert res.success is True
        assert res.status == "success"
        assert res.model_id == "v5_6_ru"
        assert res.previous_model_id == "v5_5_ru"

        # КРИТИЧЕСКАЯ ПРОВЕРКА: Активной стала v5_6_ru
        assert mm.get_active_model().model_id == "v5_6_ru"
        assert (models_dir / "state.json").is_file()


def test_already_active_model(tmp_path: Path):
    models_dir = tmp_path / "models"
    create_mock_model_dir(models_dir, "v5_5_ru", active=True)

    mm = ModelManager(models_dir=models_dir)
    switcher = ModelSwitcher(model_manager=mm)

    res = switcher.activate_model("v5_5_ru")
    assert res.success is True
    assert res.status == "already_active"


def test_model_not_found(tmp_path: Path):
    models_dir = tmp_path / "models"
    models_dir.mkdir(parents=True)

    mm = ModelManager(models_dir=models_dir)
    switcher = ModelSwitcher(model_manager=mm)

    res = switcher.activate_model("non_existent_model")
    assert res.success is False
    assert res.status == "model_not_found"


def test_missing_model_file(tmp_path: Path):
    models_dir = tmp_path / "models"
    m_dir = models_dir / "v5_6_ru"
    m_dir.mkdir(parents=True)
    # metadata без .pt файла
    (m_dir / "metadata.json").write_text(json.dumps({"model_id": "v5_6_ru", "filename": "missing.pt"}), encoding="utf-8")

    mm = ModelManager(models_dir=models_dir)
    switcher = ModelSwitcher(model_manager=mm)

    res = switcher.activate_model("v5_6_ru")
    assert res.success is False
    assert res.status in ("model_file_missing", "metadata_invalid")


def test_size_mismatch(tmp_path: Path):
    models_dir = tmp_path / "models"
    m_dir = models_dir / "v5_6_ru"
    m_dir.mkdir(parents=True)
    pt_file = m_dir / "v5_6_ru.pt"
    pt_file.write_bytes(b"data")

    # Неверный размер в metadata
    (m_dir / "metadata.json").write_text(
        json.dumps({"model_id": "v5_6_ru", "filename": "v5_6_ru.pt", "size": 99999}), encoding="utf-8"
    )

    mm = ModelManager(models_dir=models_dir)
    switcher = ModelSwitcher(model_manager=mm)

    res = switcher.activate_model("v5_6_ru")
    assert res.success is False
    assert res.status == "size_mismatch"


def test_hash_mismatch(tmp_path: Path):
    models_dir = tmp_path / "models"
    m_dir = models_dir / "v5_6_ru"
    m_dir.mkdir(parents=True)
    pt_file = m_dir / "v5_6_ru.pt"
    pt_file.write_bytes(b"data")

    (m_dir / "metadata.json").write_text(
        json.dumps({
            "model_id": "v5_6_ru",
            "filename": "v5_6_ru.pt",
            "size": 4,
            "sha256": "0000000000000000000000000000000000000000000000000000000000000000"
        }), encoding="utf-8"
    )

    mm = ModelManager(models_dir=models_dir)
    switcher = ModelSwitcher(model_manager=mm)

    res = switcher.activate_model("v5_6_ru")
    assert res.success is False
    assert res.status == "hash_mismatch"


def test_smoke_test_failure_blocks_activation(tmp_path: Path):
    models_dir = tmp_path / "models"
    create_mock_model_dir(models_dir, "v5_5_ru", active=True)
    create_mock_model_dir(models_dir, "v5_6_ru", active=False)

    mm = ModelManager(models_dir=models_dir)
    switcher = ModelSwitcher(model_manager=mm)

    with patch.object(switcher, "run_smoke_test") as mock_smoke:
        mock_smoke.return_value = SmokeTestResult(
            success=False, status="nan_audio", model_id="v5_6_ru", message="NaN detected"
        )

        res = switcher.activate_model("v5_6_ru", dry_run=False)
        assert res.success is False
        assert res.status == "smoke_test_failed"

        # КРИТИЧЕСКАЯ ПРОВЕРКА: Модель v5_6_ru НЕ стала активной!
        assert mm.get_active_model().model_id == "v5_5_ru"


def test_successful_rollback(tmp_path: Path):
    models_dir = tmp_path / "models"
    create_mock_model_dir(models_dir, "v5_5_ru", active=False)
    create_mock_model_dir(models_dir, "v5_6_ru", active=True)

    # Записываем state.json
    state_file = models_dir / "state.json"
    state_file.write_text(
        json.dumps({"active_model_id": "v5_6_ru", "previous_model_id": "v5_5_ru"}), encoding="utf-8"
    )

    mm = ModelManager(models_dir=models_dir)
    switcher = ModelSwitcher(model_manager=mm)

    with patch.object(switcher, "run_smoke_test") as mock_smoke:
        mock_smoke.return_value = SmokeTestResult(success=True, status="success", model_id="v5_5_ru")
        res = switcher.rollback_active_model(dry_run=False)

        assert res.success is True
        assert res.status == "rollback_success"
        assert res.restored_model_id == "v5_5_ru"

        # Активной снова стала v5_5_ru
        assert mm.get_active_model().model_id == "v5_5_ru"


def test_rollback_unavailable_no_previous(tmp_path: Path):
    models_dir = tmp_path / "models"
    create_mock_model_dir(models_dir, "v5_5_ru", active=True)

    mm = ModelManager(models_dir=models_dir)
    switcher = ModelSwitcher(model_manager=mm)

    res = switcher.rollback_active_model(dry_run=False)
    assert res.success is False
    assert res.status == "rollback_unavailable"


def test_no_two_active_models(tmp_path: Path):
    models_dir = tmp_path / "models"
    create_mock_model_dir(models_dir, "v5_5_ru", active=True)
    create_mock_model_dir(models_dir, "v5_6_ru", active=False)
    create_mock_model_dir(models_dir, "v5_7_ru", active=False)

    mm = ModelManager(models_dir=models_dir)
    switcher = ModelSwitcher(model_manager=mm)

    with patch.object(switcher, "run_smoke_test") as mock_smoke:
        mock_smoke.return_value = SmokeTestResult(success=True, status="success", model_id="v5_7_ru")
        switcher.activate_model("v5_7_ru", dry_run=False)

        models = mm.list_local_models()
        active_count = sum(1 for m in models if m.active)
        assert active_count == 1
        assert mm.get_active_model().model_id == "v5_7_ru"


def test_switch_history_log_written(tmp_path: Path):
    models_dir = tmp_path / "models"
    create_mock_model_dir(models_dir, "v5_5_ru", active=True)
    create_mock_model_dir(models_dir, "v5_6_ru", active=False)

    mm = ModelManager(models_dir=models_dir)
    switcher = ModelSwitcher(model_manager=mm)
    switcher.history_log_file = tmp_path / "history.jsonl"

    with patch.object(switcher, "run_smoke_test") as mock_smoke:
        mock_smoke.return_value = SmokeTestResult(success=True, status="success", model_id="v5_6_ru")
        switcher.activate_model("v5_6_ru", dry_run=False)

        assert switcher.history_log_file.is_file()
        lines = switcher.history_log_file.read_text(encoding="utf-8").strip().splitlines()
        assert len(lines) >= 1
        event = json.loads(lines[-1])
        assert event["action"] == "activate"
        assert event["to_model_id"] == "v5_6_ru"
        assert event["status"] == "success"


def test_run_smoke_test_mocked_synth(tmp_path: Path):
    models_dir = tmp_path / "models"
    create_mock_model_dir(models_dir, "v5_5_ru", active=True)

    mm = ModelManager(models_dir=models_dir)
    switcher = ModelSwitcher(model_manager=mm)

    mock_tts = MagicMock()
    mock_tts.speakers = ["eugene", "kseniya"]
    mock_tts.sample_rates = [24000]

    import numpy as np
    fake_audio = np.sin(np.linspace(0, 100, 24000 * 2))  # 2 секунды синусоиды
    mock_tts.apply_tts.return_value = fake_audio

    mock_importer = MagicMock()
    mock_importer.load_pickle.return_value = mock_tts

    with patch("torch.package.PackageImporter", return_value=mock_importer):
        res = switcher.run_smoke_test("v5_5_ru")
        assert res.success is True
        assert res.status == "success"
        assert res.voice == "eugene"
        assert res.audio_duration_sec == 2.0
