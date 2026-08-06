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


# --- 1. ВАЛИДАЦИЯ И АКТИВАЦИЯ ---

def test_dry_run_no_changes(tmp_path: Path):
    """Сценарии 38, 39: Dry-run в режиме read-only не изменяет файлы и активную модель."""
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
    """Сценарии 1, 27, 32: Валидная модель успешно активируется, создавая state.json."""
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


def test_already_active_model(tmp_path: Path):
    """Сценарий 2: Повторный запрос активации активной модели возвращает already_active."""
    models_dir = tmp_path / "models"
    create_mock_model_dir(models_dir, "v5_5_ru", active=True)

    mm = ModelManager(models_dir=models_dir)
    switcher = ModelSwitcher(model_manager=mm)

    res = switcher.activate_model("v5_5_ru")
    assert res.success is True
    assert res.status == "already_active"


def test_model_not_found(tmp_path: Path):
    """Сценарий 3: Активация несуществующей модели возвращает model_not_found."""
    models_dir = tmp_path / "models"
    models_dir.mkdir(parents=True)

    mm = ModelManager(models_dir=models_dir)
    switcher = ModelSwitcher(model_manager=mm)

    res = switcher.activate_model("non_existent_model")
    assert res.success is False
    assert res.status == "model_not_found"


def test_invalid_metadata(tmp_path: Path):
    """Сценарий 4: Поврежденный metadata.json возвращает metadata_invalid."""
    models_dir = tmp_path / "models"
    m_dir = models_dir / "v5_6_ru"
    m_dir.mkdir(parents=True)
    (m_dir / "metadata.json").write_text("{corrupted json", encoding="utf-8")

    mm = ModelManager(models_dir=models_dir)
    switcher = ModelSwitcher(model_manager=mm)

    res = switcher.activate_model("v5_6_ru")
    assert res.success is False
    assert res.status == "metadata_invalid"


def test_missing_model_file(tmp_path: Path):
    """Сценарий 5: Отсутствие бинарного .pt файла возвращает model_file_missing."""
    models_dir = tmp_path / "models"
    m_dir = models_dir / "v5_6_ru"
    m_dir.mkdir(parents=True)
    (m_dir / "metadata.json").write_text(
        json.dumps({"model_id": "v5_6_ru", "filename": "missing.pt"}), encoding="utf-8"
    )

    mm = ModelManager(models_dir=models_dir)
    switcher = ModelSwitcher(model_manager=mm)

    res = switcher.activate_model("v5_6_ru")
    assert res.success is False
    assert res.status in ("model_file_missing", "metadata_invalid")


def test_size_mismatch(tmp_path: Path):
    """Сценарий 6: Несовпадение размера файла с метаданными возвращает size_mismatch."""
    models_dir = tmp_path / "models"
    m_dir = models_dir / "v5_6_ru"
    m_dir.mkdir(parents=True)
    pt_file = m_dir / "v5_6_ru.pt"
    pt_file.write_bytes(b"data")

    (m_dir / "metadata.json").write_text(
        json.dumps({"model_id": "v5_6_ru", "filename": "v5_6_ru.pt", "size": 99999}), encoding="utf-8"
    )

    mm = ModelManager(models_dir=models_dir)
    switcher = ModelSwitcher(model_manager=mm)

    res = switcher.activate_model("v5_6_ru")
    assert res.success is False
    assert res.status == "size_mismatch"


def test_hash_mismatch(tmp_path: Path):
    """Сценарий 7: Несовпадение SHA-256 хеша с метаданными возвращает hash_mismatch."""
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


def test_path_traversal_blocked(tmp_path: Path):
    """Сценарий 8: Попытка вынести путь за пределы root блокируется."""
    models_dir = tmp_path / "models"
    m_dir = models_dir / "v5_6_ru"
    m_dir.mkdir(parents=True)
    outside_file = tmp_path / "outside.pt"
    outside_file.write_bytes(b"outside data")

    (m_dir / "metadata.json").write_text(
        json.dumps({"model_id": "v5_6_ru", "filename": "../../outside.pt"}), encoding="utf-8"
    )

    mm = ModelManager(models_dir=models_dir)
    switcher = ModelSwitcher(model_manager=mm)

    res = switcher.activate_model("v5_6_ru")
    assert res.success is False
    assert res.status in ("path_traversal", "metadata_invalid")


def test_external_symlink_blocked(tmp_path: Path):
    """Сценарий 9: Символическая ссылка за пределы root блокируется."""
    models_dir = tmp_path / "models"
    m_dir = models_dir / "v5_6_ru"
    m_dir.mkdir(parents=True)
    outside_file = tmp_path / "outside.pt"
    outside_file.write_bytes(b"outside data")
    symlink_file = m_dir / "v5_6_ru.pt"
    try:
        symlink_file.symlink_to(outside_file)
    except Exception:
        pytest.skip("Symlink creation not supported")

    (m_dir / "metadata.json").write_text(
        json.dumps({"model_id": "v5_6_ru", "filename": "v5_6_ru.pt"}), encoding="utf-8"
    )

    mm = ModelManager(models_dir=models_dir)
    switcher = ModelSwitcher(model_manager=mm)

    res = switcher.activate_model("v5_6_ru")
    assert res.success is False
    assert res.status in ("path_traversal", "metadata_invalid")


# --- 2. SMOKE-TEST И МНОГОГОЛОСАЯ ПРОВЕРКА ---

def test_eugene_and_xenia_present_and_working(tmp_path: Path):
    """Сценарии 10, 17, 22: eugene и xenia присутствуют и синтезируют; загрузка вызвана 1 раз."""
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
        res = switcher.run_smoke_test("v5_5_ru")
        assert res.success is True
        assert res.status == "success"
        assert "eugene" in res.speaker_results
        assert "xenia" in res.speaker_results
        assert res.speaker_results["eugene"].status == "success"
        assert res.speaker_results["xenia"].status == "success"
        assert mock_importer.load_pickle.call_count == 1  # КРИТИЧЕСКАЯ ПРОВЕРКА 1 ЗАГРУЗКИ


def test_smoke_test_load_failure(tmp_path: Path):
    """Сценарий 11: Ошибка загрузки модели возвращает load_failed."""
    models_dir = tmp_path / "models"
    create_mock_model_dir(models_dir, "v5_5_ru", active=True)

    mm = ModelManager(models_dir=models_dir)
    switcher = ModelSwitcher(model_manager=mm)

    with patch("torch.package.PackageImporter", side_effect=RuntimeError("Corrupted pt file")):
        res = switcher.run_smoke_test("v5_5_ru")
        assert res.success is False
        assert res.status == "load_failed"


def test_eugene_missing_fails_activation(tmp_path: Path):
    """Сценарий 18: Отсутствие eugene блокирует активацию."""
    models_dir = tmp_path / "models"
    create_mock_model_dir(models_dir, "v5_5_ru", active=True)

    mm = ModelManager(models_dir=models_dir)
    switcher = ModelSwitcher(model_manager=mm)

    mock_tts = MagicMock()
    mock_tts.speakers = ["xenia", "kseniya"]
    mock_tts.sample_rates = [24000]

    mock_importer = MagicMock()
    mock_importer.load_pickle.return_value = mock_tts

    with patch("torch.package.PackageImporter", return_value=mock_importer):
        res = switcher.run_smoke_test("v5_5_ru")
        assert res.success is False
        assert "eugene" in res.missing_required_speakers


def test_xenia_missing_fails_activation(tmp_path: Path):
    """Сценарий 19: Отсутствие xenia блокирует активацию."""
    models_dir = tmp_path / "models"
    create_mock_model_dir(models_dir, "v5_5_ru", active=True)

    mm = ModelManager(models_dir=models_dir)
    switcher = ModelSwitcher(model_manager=mm)

    mock_tts = MagicMock()
    mock_tts.speakers = ["eugene", "kseniya"]
    mock_tts.sample_rates = [24000]

    mock_importer = MagicMock()
    mock_importer.load_pickle.return_value = mock_tts

    with patch("torch.package.PackageImporter", return_value=mock_importer):
        res = switcher.run_smoke_test("v5_5_ru")
        assert res.success is False
        assert "xenia" in res.missing_required_speakers


def test_eugene_crashes_xenia_works(tmp_path: Path):
    """Сценарий 20: Падает eugene, xenia синтезирует -> активация блокируется."""
    models_dir = tmp_path / "models"
    create_mock_model_dir(models_dir, "v5_5_ru", active=True)

    mm = ModelManager(models_dir=models_dir)
    switcher = ModelSwitcher(model_manager=mm)

    mock_tts = MagicMock()
    mock_tts.speakers = ["eugene", "xenia"]
    mock_tts.sample_rates = [24000]

    def side_effect(text, speaker, sample_rate):
        if speaker == "eugene":
            raise RuntimeError("Eugene crash")
        return np.sin(np.linspace(0, 100, 24000 * 2))

    mock_tts.apply_tts.side_effect = side_effect

    mock_importer = MagicMock()
    mock_importer.load_pickle.return_value = mock_tts

    with patch("torch.package.PackageImporter", return_value=mock_importer):
        res = switcher.run_smoke_test("v5_5_ru")
        assert res.success is False
        assert res.speaker_results["eugene"].status == "synth_failed"
        assert res.speaker_results["xenia"].status == "success"


def test_eugene_works_xenia_crashes(tmp_path: Path):
    """Сценарий 12, 21: eugene синтезирует, xenia падает -> активация блокируется."""
    models_dir = tmp_path / "models"
    create_mock_model_dir(models_dir, "v5_5_ru", active=True)

    mm = ModelManager(models_dir=models_dir)
    switcher = ModelSwitcher(model_manager=mm)

    mock_tts = MagicMock()
    mock_tts.speakers = ["eugene", "xenia"]
    mock_tts.sample_rates = [24000]

    def side_effect(text, speaker, sample_rate):
        if speaker == "xenia":
            raise RuntimeError("Xenia crash")
        return np.sin(np.linspace(0, 100, 24000 * 2))

    mock_tts.apply_tts.side_effect = side_effect

    mock_importer = MagicMock()
    mock_importer.load_pickle.return_value = mock_tts

    with patch("torch.package.PackageImporter", return_value=mock_importer):
        res = switcher.run_smoke_test("v5_5_ru")
        assert res.success is False
        assert res.speaker_results["eugene"].status == "success"
        assert res.speaker_results["xenia"].status == "synth_failed"


def test_smoke_test_empty_audio(tmp_path: Path):
    """Сценарий 14: Пустой аудио-тензор отклоняется."""
    models_dir = tmp_path / "models"
    create_mock_model_dir(models_dir, "v5_5_ru", active=True)

    mm = ModelManager(models_dir=models_dir)
    switcher = ModelSwitcher(model_manager=mm)

    mock_tts = MagicMock()
    mock_tts.speakers = ["eugene", "xenia"]
    mock_tts.sample_rates = [24000]
    mock_tts.apply_tts.return_value = np.array([])  # 0 сэмплов

    mock_importer = MagicMock()
    mock_importer.load_pickle.return_value = mock_tts

    with patch("torch.package.PackageImporter", return_value=mock_importer):
        res = switcher.run_smoke_test("v5_5_ru")
        assert res.success is False
        assert res.speaker_results["eugene"].status == "empty_audio"


def test_smoke_test_nan_audio(tmp_path: Path):
    """Сценарий 15: Аудио с NaN / Inf значениями отклоняется."""
    models_dir = tmp_path / "models"
    create_mock_model_dir(models_dir, "v5_5_ru", active=True)

    mm = ModelManager(models_dir=models_dir)
    switcher = ModelSwitcher(model_manager=mm)

    mock_tts = MagicMock()
    mock_tts.speakers = ["eugene", "xenia"]
    mock_tts.sample_rates = [24000]
    arr = np.sin(np.linspace(0, 100, 24000 * 2))
    arr[10] = np.nan
    mock_tts.apply_tts.return_value = arr

    mock_importer = MagicMock()
    mock_importer.load_pickle.return_value = mock_tts

    with patch("torch.package.PackageImporter", return_value=mock_importer):
        res = switcher.run_smoke_test("v5_5_ru")
        assert res.success is False
        assert res.speaker_results["eugene"].status == "nan_audio"


def test_smoke_test_silent_audio(tmp_path: Path):
    """Сценарий 16: Полностью молчаливое аудио (нули) отклоняется."""
    models_dir = tmp_path / "models"
    create_mock_model_dir(models_dir, "v5_5_ru", active=True)

    mm = ModelManager(models_dir=models_dir)
    switcher = ModelSwitcher(model_manager=mm)

    mock_tts = MagicMock()
    mock_tts.speakers = ["eugene", "xenia"]
    mock_tts.sample_rates = [24000]
    mock_tts.apply_tts.return_value = np.zeros(24000 * 2)

    mock_importer = MagicMock()
    mock_importer.load_pickle.return_value = mock_tts

    with patch("torch.package.PackageImporter", return_value=mock_importer):
        res = switcher.run_smoke_test("v5_5_ru")
        assert res.success is False
        assert res.speaker_results["eugene"].status == "empty_audio"


def test_all_speakers_flag(tmp_path: Path):
    """Сценарий 23: --all-speakers проверяет все доступные голосы модели."""
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
    """Сценарии 24, 25, 26: Выбранный голос проверяется при активации без молчаливой подмены."""
    models_dir = tmp_path / "models"
    create_mock_model_dir(models_dir, "v5_5_ru", active=True)
    create_mock_model_dir(models_dir, "v5_6_ru", active=False)

    mm = ModelManager(models_dir=models_dir)
    switcher = ModelSwitcher(model_manager=mm)

    mock_smoke = MagicMock()
    mock_smoke.success = True
    mock_smoke.available_speakers = ["eugene"]  # xenia отсутствует в v5_6_ru

    with patch.object(switcher, "run_smoke_test", return_value=mock_smoke):
        res = switcher.activate_model("v5_6_ru", voice="xenia")
        assert res.success is False
        assert res.status == "voice_missing"
        assert "xenia" in res.message


# --- 3. СОСТОЯНИЕ, ROLLBACK И ИСТОРИЯ ---

def test_no_two_active_models(tmp_path: Path):
    """Сценарий 31: Только одна модель имеет active=True в системе."""
    models_dir = tmp_path / "models"
    create_mock_model_dir(models_dir, "v5_5_ru", active=True)
    create_mock_model_dir(models_dir, "v5_6_ru", active=False)
    create_mock_model_dir(models_dir, "v5_7_ru", active=False)

    mm = ModelManager(models_dir=models_dir)
    switcher = ModelSwitcher(model_manager=mm)

    mock_smoke = MagicMock()
    mock_smoke.success = True
    mock_smoke.status = "success"

    with patch.object(switcher, "run_smoke_test", return_value=mock_smoke):
        switcher.activate_model("v5_7_ru", dry_run=False)

        models = mm.list_local_models()
        active_count = sum(1 for m in models if m.active)
        assert active_count == 1
        assert mm.get_active_model().model_id == "v5_7_ru"


def test_successful_rollback(tmp_path: Path):
    """Сценарий 33: Успешный откат к предыдущей рабочей модели."""
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
    """Сценарий 34: Откат невозможно выполнить при отсутствии информации о предыдущей модели."""
    models_dir = tmp_path / "models"
    create_mock_model_dir(models_dir, "v5_5_ru", active=True)

    mm = ModelManager(models_dir=models_dir)
    switcher = ModelSwitcher(model_manager=mm)

    res = switcher.rollback_active_model(dry_run=False)
    assert res.success is False
    assert res.status == "rollback_unavailable"


def test_damaged_previous_model_blocks_rollback(tmp_path: Path):
    """Сценарий 35: Откат блокируется, если предыдущая модель повреждена."""
    models_dir = tmp_path / "models"
    # Создаем предыдущую модель без файла .pt
    m_dir = models_dir / "v5_5_ru"
    m_dir.mkdir(parents=True)
    (m_dir / "metadata.json").write_text(json.dumps({"model_id": "v5_5_ru", "filename": "missing.pt"}), encoding="utf-8")

    create_mock_model_dir(models_dir, "v5_6_ru", active=True)

    state_file = models_dir / "state.json"
    state_file.write_text(
        json.dumps({"active_model_id": "v5_6_ru", "previous_model_id": "v5_5_ru"}), encoding="utf-8"
    )

    mm = ModelManager(models_dir=models_dir)
    switcher = ModelSwitcher(model_manager=mm)

    res = switcher.rollback_active_model(dry_run=False)
    assert res.success is False
    assert res.status == "rollback_unavailable"


def test_switch_history_log_written(tmp_path: Path):
    """Сценарий 36: Запись событий переключения в model_switches.jsonl."""
    models_dir = tmp_path / "models"
    create_mock_model_dir(models_dir, "v5_5_ru", active=True)
    create_mock_model_dir(models_dir, "v5_6_ru", active=False)

    mm = ModelManager(models_dir=models_dir)
    switcher = ModelSwitcher(model_manager=mm)
    switcher.history_log_file = tmp_path / "history.jsonl"

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
        switcher.activate_model("v5_6_ru", dry_run=False)

        assert switcher.history_log_file.is_file()
        lines = switcher.history_log_file.read_text(encoding="utf-8").strip().splitlines()
        assert len(lines) >= 1
        event = json.loads(lines[-1])
        assert event["action"] == "activate"
        assert event["to_model_id"] == "v5_6_ru"
        assert event["status"] == "success"


def test_history_write_failure_non_fatal(tmp_path: Path):
    """Сценарий 37: Ошибка записи истории не отменяет успешную активацию."""
    models_dir = tmp_path / "models"
    create_mock_model_dir(models_dir, "v5_5_ru", active=True)
    create_mock_model_dir(models_dir, "v5_6_ru", active=False)

    mm = ModelManager(models_dir=models_dir)
    switcher = ModelSwitcher(model_manager=mm)
    switcher.history_log_file = tmp_path / "non_existent_folder" / "history.jsonl"

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
        assert mm.get_active_model().model_id == "v5_6_ru"


def test_models_test_read_only(tmp_path: Path):
    """Сценарий 40: Выполнение models test не изменяет metadata и state.json."""
    models_dir = tmp_path / "models"
    create_mock_model_dir(models_dir, "v5_5_ru", active=True)

    mm = ModelManager(models_dir=models_dir)
    switcher = ModelSwitcher(model_manager=mm)

    mock_tts = MagicMock()
    mock_tts.speakers = ["eugene", "xenia"]
    mock_tts.sample_rates = [24000]
    mock_tts.apply_tts.return_value = np.sin(np.linspace(0, 100, 24000 * 2))

    mock_importer = MagicMock()
    mock_importer.load_pickle.return_value = mock_tts

    with patch("torch.package.PackageImporter", return_value=mock_importer):
        res = switcher.run_smoke_test("v5_5_ru")
        assert res.success is True
        # Проверяем, что state.json не создался
        assert not (models_dir / "state.json").exists()


def test_tts_session_active_model_resolution(tmp_path: Path):
    """Сценарии 41, 42: Новый TTS сеанс считывает новую активную модель."""
    models_dir = tmp_path / "models"
    create_mock_model_dir(models_dir, "v5_5_ru", active=False)
    create_mock_model_dir(models_dir, "v5_6_ru", active=True)

    mm = ModelManager(models_dir=models_dir)
    active_m = mm.get_active_model()
    assert active_m.model_id == "v5_6_ru"


def test_smoke_test_timeout(tmp_path: Path):
    """Сценарий 13: Превышение timeout при smoke-test возвращает статус timeout и не сменяет active."""
    models_dir = tmp_path / "models"
    create_mock_model_dir(models_dir, "v5_5_ru", active=True)

    mm = ModelManager(models_dir=models_dir)
    switcher = ModelSwitcher(model_manager=mm)

    with patch("torch.package.PackageImporter", side_effect=TimeoutError("Worker timed out")):
        res = switcher.run_smoke_test("v5_5_ru")
        assert res.success is False
        assert res.status == "timeout"
        assert "Превышено допустимое время" in res.message


def test_metadata_write_failure_rollback(tmp_path: Path):
    """Сценарий 28: Ошибка записи metadata.json возвращает write_error и сохраняет старую модель активной."""
    models_dir = tmp_path / "models"
    create_mock_model_dir(models_dir, "v5_5_ru", active=True)
    create_mock_model_dir(models_dir, "v5_6_ru", active=False)

    mm = ModelManager(models_dir=models_dir)
    switcher = ModelSwitcher(model_manager=mm)

    mock_smoke = MagicMock()
    mock_smoke.success = True

    with patch.object(switcher, "run_smoke_test", return_value=mock_smoke):
        # Смокируем ошибку при отмене/записи new metadata.json.tmp -> replace
        with patch("pathlib.Path.replace", side_effect=OSError("Disk write error")):
            res = switcher.activate_model("v5_6_ru", dry_run=False)
            assert res.success is False
            assert res.status == "write_error"
            # Старая модель v5_5_ru остается активной
            assert mm.get_active_model().model_id == "v5_5_ru"


def test_state_write_failure_rollback(tmp_path: Path):
    """Сценарий 29: Ошибка записи state.json откатывает metadata.json и сохраняет старую модель активной."""
    models_dir = tmp_path / "models"
    create_mock_model_dir(models_dir, "v5_5_ru", active=True)
    create_mock_model_dir(models_dir, "v5_6_ru", active=False)

    mm = ModelManager(models_dir=models_dir)
    switcher = ModelSwitcher(model_manager=mm)

    mock_smoke = MagicMock()
    mock_smoke.success = True

    with patch.object(switcher, "run_smoke_test", return_value=mock_smoke):
        # state.json не записывается
        with patch.object(switcher, "_write_state_atomic", return_value=False):
            res = switcher.activate_model("v5_6_ru", dry_run=False)
            assert res.success is False
            assert res.status == "write_error"
            assert mm.get_active_model().model_id == "v5_5_ru"
