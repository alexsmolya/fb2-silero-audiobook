"""
Unit-тесты для модуля src.core.model_migrator (ModelMigrator) и интеграции с TTS.
"""

import json
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from src.core.model_inspector import _calculate_sha256
from src.core.model_manager import ModelManager, ModelMetadata
from src.core.model_migrator import MigrationResult, ModelMigrator
from src.core.tts_silero import SileroTTSManager
from tools.model_manager import format_migration_result


@pytest.fixture
def temp_dirs(tmp_path: Path):
    user_models_dir = tmp_path / "user_models"
    user_models_dir.mkdir()
    legacy_file = tmp_path / "legacy_v5_5_ru_ru.pt"
    legacy_file.write_bytes(b"dummy legacy model binary content 123456789")

    return {
        "user_models_dir": user_models_dir,
        "legacy_file": legacy_file,
    }


def test_migration_dry_run(temp_dirs: dict):
    user_dir = temp_dirs["user_models_dir"]
    legacy_file = temp_dirs["legacy_file"]

    mm = ModelManager(models_dir=user_dir)
    legacy_meta = ModelMetadata(
        model_id="v5_5_ru",
        filename="v5_5_ru_ru.pt",
        path=str(legacy_file),
        size_bytes=legacy_file.stat().st_size,
        sha256=_calculate_sha256(legacy_file),
        source="legacy_venv",
        is_legacy=True,
        valid=True,
    )

    with patch.object(mm, "detect_legacy_models", return_value=[legacy_meta]):
        migrator = ModelMigrator(model_manager=mm)
        res = migrator.migrate_legacy_model(model_id="v5_5_ru", dry_run=True)

        assert res.success is True
        assert res.status == "ready"
        assert res.dry_run is True
        assert res.sha256 == legacy_meta.sha256
        # Проверяем, что физические файлы НЕ создались
        assert not (user_dir / "v5_5_ru").exists()


def test_successful_migration(temp_dirs: dict):
    user_dir = temp_dirs["user_models_dir"]
    legacy_file = temp_dirs["legacy_file"]

    mm = ModelManager(models_dir=user_dir)
    legacy_sha256 = _calculate_sha256(legacy_file)
    legacy_size = legacy_file.stat().st_size
    legacy_meta = ModelMetadata(
        model_id="v5_5_ru",
        filename="v5_5_ru_ru.pt",
        path=str(legacy_file),
        size_bytes=legacy_size,
        sha256=legacy_sha256,
        source="legacy_venv",
        is_legacy=True,
        valid=True,
    )

    with patch.object(mm, "detect_legacy_models", return_value=[legacy_meta]):
        migrator = ModelMigrator(model_manager=mm)
        res = migrator.migrate_legacy_model(model_id="v5_5_ru", dry_run=False)

        assert res.success is True
        assert res.status == "success"
        assert res.sha256 == legacy_sha256

        # Проверяем файлы
        target_dir = user_dir / "v5_5_ru"
        target_pt = target_dir / "v5_5_ru_ru.pt"
        meta_json = target_dir / "metadata.json"

        assert target_pt.is_file()
        assert meta_json.is_file()

        assert _calculate_sha256(target_pt) == legacy_sha256
        assert target_pt.stat().st_size == legacy_size

        # Проверяем метаданные
        data = json.loads(meta_json.read_text(encoding="utf-8"))
        assert data["model_id"] == "v5_5_ru"
        assert data["sha256"] == legacy_sha256
        assert data["active"] is True

        # Проверяем сохранность legacy файла
        assert legacy_file.is_file()


def test_idempotent_migration(temp_dirs: dict):
    user_dir = temp_dirs["user_models_dir"]
    legacy_file = temp_dirs["legacy_file"]

    mm = ModelManager(models_dir=user_dir)
    legacy_sha256 = _calculate_sha256(legacy_file)
    legacy_meta = ModelMetadata(
        model_id="v5_5_ru",
        filename="v5_5_ru_ru.pt",
        path=str(legacy_file),
        size_bytes=legacy_file.stat().st_size,
        sha256=legacy_sha256,
        source="legacy_venv",
        is_legacy=True,
        valid=True,
    )

    with patch.object(mm, "detect_legacy_models", return_value=[legacy_meta]):
        migrator = ModelMigrator(model_manager=mm)
        # Первая миграция
        migrator.migrate_legacy_model(model_id="v5_5_ru", dry_run=False)

        # Вторая миграция (повторный запуск)
        res2 = migrator.migrate_legacy_model(model_id="v5_5_ru", dry_run=False)

        assert res2.success is True
        assert res2.status == "already_migrated"


def test_target_conflict(temp_dirs: dict):
    user_dir = temp_dirs["user_models_dir"]
    legacy_file = temp_dirs["legacy_file"]

    # Создаём целевой файл с другим содержимым
    target_dir = user_dir / "v5_5_ru"
    target_dir.mkdir(parents=True)
    target_pt = target_dir / "v5_5_ru_ru.pt"
    target_pt.write_bytes(b"completely different conflicting data")

    mm = ModelManager(models_dir=user_dir)
    legacy_meta = ModelMetadata(
        model_id="v5_5_ru",
        filename="v5_5_ru_ru.pt",
        path=str(legacy_file),
        size_bytes=legacy_file.stat().st_size,
        sha256=_calculate_sha256(legacy_file),
        source="legacy_venv",
        is_legacy=True,
        valid=True,
    )

    with patch.object(mm, "detect_legacy_models", return_value=[legacy_meta]):
        migrator = ModelMigrator(model_manager=mm)
        res = migrator.migrate_legacy_model(model_id="v5_5_ru", dry_run=False)

        assert res.success is False
        assert res.status == "target_conflict"


def test_missing_legacy_model(temp_dirs: dict):
    user_dir = temp_dirs["user_models_dir"]

    mm = ModelManager(models_dir=user_dir)
    with patch.object(mm, "detect_legacy_models", return_value=[]):
        migrator = ModelMigrator(model_manager=mm)
        res = migrator.migrate_legacy_model(model_id="v5_5_ru", dry_run=False)

        assert res.success is False
        assert res.status == "source_missing"


def test_sha256_mismatch_and_temp_cleanup(temp_dirs: dict):
    user_dir = temp_dirs["user_models_dir"]
    legacy_file = temp_dirs["legacy_file"]

    mm = ModelManager(models_dir=user_dir)
    legacy_meta = ModelMetadata(
        model_id="v5_5_ru",
        filename="v5_5_ru_ru.pt",
        path=str(legacy_file),
        size_bytes=legacy_file.stat().st_size,
        sha256=_calculate_sha256(legacy_file),
        source="legacy_venv",
        is_legacy=True,
        valid=True,
    )

    with patch.object(mm, "detect_legacy_models", return_value=[legacy_meta]):
        with patch("src.core.model_migrator._calculate_sha256", return_value="wrong_mismatched_hash"):
            migrator = ModelMigrator(model_manager=mm)
            res = migrator.migrate_legacy_model(model_id="v5_5_ru", dry_run=False)

            assert res.success is False
            assert res.status == "sha256_mismatch"

            # Проверяем, что временный файл .tmp удалён
            target_dir = user_dir / "v5_5_ru"
            assert not (target_dir / "v5_5_ru_ru.pt.tmp").exists()
            assert not (target_dir / "v5_5_ru_ru.pt").exists()


def test_cli_format_migration_result():
    res = MigrationResult(
        success=True,
        status="success",
        source_path="/src/path.pt",
        target_path="/dst/path.pt",
        size_bytes=100,
        size_formatted="100 bytes",
        sha256="abc123hash",
        message="OK",
    )
    formatted = format_migration_result(res)
    assert "Status: SUCCESS" in formatted
    assert "Source path: /src/path.pt" in formatted
    assert "SHA256: abc123hash" in formatted


@pytest.mark.asyncio
async def test_silero_tts_manager_loads_user_model(temp_dirs: dict):
    user_dir = temp_dirs["user_models_dir"]

    # Создаем пользовательскую модель
    m_dir = user_dir / "v5_5_ru"
    m_dir.mkdir()
    pt_file = m_dir / "v5_5_ru_ru.pt"
    pt_file.write_bytes(b"dummy pt content")

    meta = ModelMetadata(
        model_id="v5_5_ru",
        filename="v5_5_ru_ru.pt",
        path=str(pt_file),
        size_bytes=16,
        sha256="dummyhash",
        source="user_models",
        active=True,
        valid=True,
    )

    dummy_config = MagicMock()
    dummy_config.main_voice = "xenia"
    dummy_config.comment_voice = "eugene"

    manager = SileroTTSManager(config=dummy_config)
    mock_loaded_model = MagicMock()
    mock_importer = MagicMock()
    mock_importer.load_pickle.return_value = mock_loaded_model

    with patch("src.core.model_manager.ModelManager.get_active_model", return_value=meta):
        with patch("silero_tts.silero_tts.SileroTTS.__init__", return_value=None):
            with patch("torch.package.PackageImporter", return_value=mock_importer):
                await manager._ensure_ru_initialized()
                assert manager._tts_ru is not None
                assert manager._tts_ru.tts_model == mock_loaded_model
                mock_importer.load_pickle.assert_called_once_with("tts_models", "model")


@pytest.mark.asyncio
async def test_silero_tts_manager_fallback_to_legacy(temp_dirs: dict):
    dummy_config = MagicMock()
    dummy_config.main_voice = "xenia"
    dummy_config.comment_voice = "eugene"

    manager = SileroTTSManager(config=dummy_config)

    # Нет пользовательской модели -> fallback
    with patch("src.core.model_manager.ModelManager.get_active_model", return_value=None):
        with patch("silero_tts.silero_tts.SileroTTS.__init__", return_value=None) as mock_init:
            await manager._ensure_ru_initialized()
            assert manager._tts_ru is not None
            mock_init.assert_called_once()
