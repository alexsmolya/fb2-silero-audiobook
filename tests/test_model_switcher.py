"""
Unit-тесты для модуля src.core.model_switcher (ModelSwitcher).

Все вызовы PyTorch / PackageImporter полностью смокированы.
Все файлы создаются во временных папках pytest (tmp_path).
"""

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import numpy as np
import pytest
from src.core.model_manager import ModelManager, ModelMetadata
from src.core.model_switcher import (
    ModelSwitcher,
    REQUIRED_RUSSIAN_SPEAKERS,
    RollbackResult,
    SmokeTestResult,
    SpeakerTestResult,
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
        mock_smoke.return_value = SmokeTestResult(
            success=True,
            status="success",
            model_id="v5_6_ru",
            available_speakers=["eugene", "xenia"],
            tested_speakers=["eugene", "xenia"],
            missing_required_speakers=[],
            failed_speakers=[],
            speaker_results={},
        )
        res = switcher.activate_model("v5_6_ru", dry_run=True)

        assert res.success is True
        assert res.dry_run is True
        assert res.status == "ready"
        assert mm.get_active_model().model_id == "v5_5_ru"


def test_activate_valid_model(tmp_path: Path):
    models_dir = tmp_path / "models"
    create_mock_model_dir(models_dir, "v5_5_ru", active=True)
    create_mock_model_dir(models_dir, "v5_6_ru", active=False)

    mm = ModelManager(models_dir=models_dir)
    switcher = ModelSwitcher(model_manager=mm)

    with patch.object(switcher, "run_smoke_test") as mock_smoke:
        mock_smoke.return_value = SmokeTestResult(
            success=True,
            status="success",
            model_id="v5_6_ru",
            available_speakers=["eugene", "xenia"],
            tested_speakers=["eugene", "xenia"],
            missing_required_speakers=[],
            failed_speakers=[],
            speaker_results={},
        )
        res = switcher.activate_model("v5_6_ru", dry_run=False)

        assert res.success is True
        assert res.status == "success"
        assert res.model_id == "v5_6_ru"
        assert res.previous_model_id == "v5_5_ru"
        assert mm.get_active_model().model_id == "v5_6_ru"
        assert (models_dir / "state.json").is_file()


def test_eugene_and_xenia_present_and_working(tmp_path: Path):
    """Сценарий 1: eugene и xenia присутствуют и работают -> УСПЕХ."""
    models_dir = tmp_path / "models"
    create_mock_model_dir(models_dir, "v5_5_ru", active=True)

    mm = ModelManager(models_dir=models_dir)
    switcher = ModelSwitcher(model_manager=mm)

    mock_tts = MagicMock()
    mock_tts.speakers = ["aidar", "baya", "kseniya", "xenia", "eugene"]
    mock_tts.sample_rates = [24000]

    fake_audio = np.sin(np.linspace(0, 100, 24000 * 2))  # 2 сек
    mock_tts.apply_tts.return_value = fake_audio

    mock_importer = MagicMock()
    mock_importer.load_pickle.return_value = mock_tts

    with patch("torch.package.PackageImporter", return_value=mock_importer):
        res = switcher.run_smoke_test("v5_5_ru")
        assert res.success is True
        assert res.status == "success"
        assert "eugene" in res.speaker_results
        assert "xenia" in res.speaker_results
        assert res.speaker_results["eugene"].status == "success"
        assert res.speaker_results["xenia"].status == "success"
        # Загрузка модели выполняется ровно ОДИН РАЗ
        assert mock_importer.load_pickle.call_count == 1


def test_eugene_missing_fails_activation(tmp_path: Path):
    """Сценарий 2: Отсутствует eugene -> smoke test фейлится."""
    models_dir = tmp_path / "models"
    create_mock_model_dir(models_dir, "v5_5_ru", active=True)

    mm = ModelManager(models_dir=models_dir)
    switcher = ModelSwitcher(model_manager=mm)

    mock_tts = MagicMock()
    mock_tts.speakers = ["xenia", "kseniya"]  # eugene отсутствует
    mock_tts.sample_rates = [24000]
    mock_tts.apply_tts.return_value = np.sin(np.linspace(0, 100, 24000 * 2))

    mock_importer = MagicMock()
    mock_importer.load_pickle.return_value = mock_tts

    with patch("torch.package.PackageImporter", return_value=mock_importer):
        res = switcher.run_smoke_test("v5_5_ru")
        assert res.success is False
        assert "eugene" in res.missing_required_speakers
        assert res.speaker_results["eugene"].status == "missing"


def test_xenia_missing_fails_activation(tmp_path: Path):
    """Сценарий 3: Отсутствует xenia -> smoke test фейлится."""
    models_dir = tmp_path / "models"
    create_mock_model_dir(models_dir, "v5_5_ru", active=True)

    mm = ModelManager(models_dir=models_dir)
    switcher = ModelSwitcher(model_manager=mm)

    mock_tts = MagicMock()
    mock_tts.speakers = ["eugene", "kseniya"]  # xenia отсутствует
    mock_tts.sample_rates = [24000]
    mock_tts.apply_tts.return_value = np.sin(np.linspace(0, 100, 24000 * 2))

    mock_importer = MagicMock()
    mock_importer.load_pickle.return_value = mock_tts

    with patch("torch.package.PackageImporter", return_value=mock_importer):
        res = switcher.run_smoke_test("v5_5_ru")
        assert res.success is False
        assert "xenia" in res.missing_required_speakers
        assert res.speaker_results["xenia"].status == "missing"


def test_eugene_works_xenia_crashes(tmp_path: Path):
    """Сценарий 4: eugene синтезирует, xenia падает -> smoke test фейлится."""
    models_dir = tmp_path / "models"
    create_mock_model_dir(models_dir, "v5_5_ru", active=True)

    mm = ModelManager(models_dir=models_dir)
    switcher = ModelSwitcher(model_manager=mm)

    mock_tts = MagicMock()
    mock_tts.speakers = ["eugene", "xenia"]
    mock_tts.sample_rates = [24000]

    def side_effect(text, speaker, sample_rate):
        if speaker == "xenia":
            raise RuntimeError("Xenia synthesis crash")
        return np.sin(np.linspace(0, 100, 24000 * 2))

    mock_tts.apply_tts.side_effect = side_effect

    mock_importer = MagicMock()
    mock_importer.load_pickle.return_value = mock_tts

    with patch("torch.package.PackageImporter", return_value=mock_importer):
        res = switcher.run_smoke_test("v5_5_ru")
        assert res.success is False
        assert res.speaker_results["eugene"].status == "success"
        assert res.speaker_results["xenia"].status == "synth_failed"


def test_all_speakers_flag(tmp_path: Path):
    """Сценарий 9: --all-speakers проверяет все доступные голоса."""
    models_dir = tmp_path / "models"
    create_mock_model_dir(models_dir, "v5_5_ru", active=True)

    mm = ModelManager(models_dir=models_dir)
    switcher = ModelSwitcher(model_manager=mm)

    mock_tts = MagicMock()
    mock_tts.speakers = ["aidar", "baya", "kseniya", "xenia", "eugene"]
    mock_tts.sample_rates = [24000]
    mock_tts.apply_tts.return_value = np.sin(np.linspace(0, 100, 24000 * 2))

    mock_importer = MagicMock()
    mock_importer.load_pickle.return_value = mock_tts

    with patch("torch.package.PackageImporter", return_value=mock_importer):
        res = switcher.run_smoke_test("v5_5_ru", all_speakers=True)
        assert res.success is True
        assert len(res.tested_speakers) == 5
        assert set(res.tested_speakers) == set(mock_tts.speakers)


def test_user_selected_voice_preserved_or_warned(tmp_path: Path):
    """Сценарий 10-12: Выбранный голос проверяется при активации без молчаливой подмены."""
    models_dir = tmp_path / "models"
    create_mock_model_dir(models_dir, "v5_5_ru", active=True)
    create_mock_model_dir(models_dir, "v5_6_ru", active=False)

    mm = ModelManager(models_dir=models_dir)
    switcher = ModelSwitcher(model_manager=mm)

    mock_smoke = MagicMock()
    mock_smoke.success = True
    mock_smoke.available_speakers = ["eugene"]  # xenia отсутствует в v5_6_ru

    with patch.object(switcher, "run_smoke_test", return_value=mock_smoke):
        # Пользователь выбрал xenia, но xenia отсутствует в новой модели v5_6_ru
        res = switcher.activate_model("v5_6_ru", voice="xenia")
        assert res.success is False
        assert res.status == "voice_missing"
        assert "xenia" in res.message


def test_successful_rollback(tmp_path: Path):
    models_dir = tmp_path / "models"
    create_mock_model_dir(models_dir, "v5_5_ru", active=False)
    create_mock_model_dir(models_dir, "v5_6_ru", active=True)

    state_file = models_dir / "state.json"
    state_file.write_text(
        json.dumps({"active_model_id": "v5_6_ru", "previous_model_id": "v5_5_ru"}), encoding="utf-8"
    )

    mm = ModelManager(models_dir=models_dir)
    switcher = ModelSwitcher(model_manager=mm)

    mock_smoke = MagicMock()
    mock_smoke.success = True
    mock_smoke.status = "success"

    with patch.object(switcher, "run_smoke_test", return_value=mock_smoke):
        res = switcher.rollback_active_model(dry_run=False)

        assert res.success is True
        assert res.status == "rollback_success"
        assert res.restored_model_id == "v5_5_ru"
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

    mock_smoke = MagicMock()
    mock_smoke.success = True
    mock_smoke.status = "success"
    mock_smoke.available_speakers = ["eugene", "xenia"]

    with patch.object(switcher, "run_smoke_test", return_value=mock_smoke):
        switcher.activate_model("v5_7_ru", dry_run=False)

        models = mm.list_local_models()
        active_count = sum(1 for m in models if m.active)
        assert active_count == 1
        assert mm.get_active_model().model_id == "v5_7_ru"
