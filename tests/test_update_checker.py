"""
Unit-тесты для модуля src.core.update_checker (UpdateChecker).

Все сетевые обращения к GitHub / silero.ai полностью смокированы.
"""

from unittest.mock import MagicMock, patch

import pytest
from src.core.model_manager import ModelManager, ModelMetadata
from src.core.update_checker import (
    CheckUpdateResult,
    UpdateChecker,
    format_update_check_result,
    parse_model_version,
)

SAMPLE_OFFICIAL_MANIFEST = """
tts_models:
  ru:
    v5_5_ru:
      latest:
        package: 'https://models.silero.ai/models/tts/ru/v5_5_ru.pt'
        sample_rate: [8000, 24000, 48000]
    v5_4_ru:
      latest:
        package: 'https://models.silero.ai/models/tts/ru/v5_4_ru.pt'
"""

SAMPLE_NEWER_MANIFEST = """
tts_models:
  ru:
    v5_6_ru:
      latest:
        package: 'https://models.silero.ai/models/tts/ru/v5_6_ru.pt'
    v5_5_ru:
      latest:
        package: 'https://models.silero.ai/models/tts/ru/v5_5_ru.pt'
"""


def test_parse_model_version():
    assert parse_model_version("v5_5_ru") == (5, 5)
    assert parse_model_version("v5_6_ru") == (5, 6)
    assert parse_model_version("v6_0_ru") == (6, 0)
    assert parse_model_version("v5_ru") == (5, 0)
    assert parse_model_version("custom_model") == (0, 0)


def test_up_to_date():
    local_meta = ModelMetadata(
        model_id="v5_5_ru",
        filename="v5_5_ru_ru.pt",
        path="/path/v5_5_ru_ru.pt",
        size_bytes=1000,
        sha256="hash123",
        installed_at="2026-08-06T12:00:00+00:00",
        valid=True,
    )

    mm = MagicMock(spec=ModelManager)
    mm.get_active_model.return_value = local_meta

    checker = UpdateChecker(model_manager=mm)

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = SAMPLE_OFFICIAL_MANIFEST

    with patch("httpx.Client.get", return_value=mock_response):
        with patch.object(checker, "_fetch_remote_head_info", return_value={"size": 1000}):
            res = checker.check_for_updates()
            assert res.status == "up_to_date"
            assert res.local_model_id == "v5_5_ru"
            assert res.remote_model_id == "v5_5_ru"


def test_update_available():
    local_meta = ModelMetadata(
        model_id="v5_5_ru",
        filename="v5_5_ru_ru.pt",
        path="/path/v5_5_ru_ru.pt",
        size_bytes=1000,
        sha256="hash123",
        installed_at="2026-08-06T12:00:00+00:00",
        valid=True,
    )

    mm = MagicMock(spec=ModelManager)
    mm.get_active_model.return_value = local_meta

    checker = UpdateChecker(model_manager=mm)

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = SAMPLE_NEWER_MANIFEST

    with patch("httpx.Client.get", return_value=mock_response):
        with patch.object(checker, "_fetch_remote_file_size", return_value=1200):
            res = checker.check_for_updates()
            assert res.status == "update_available"
            assert res.local_model_id == "v5_5_ru"
            assert res.remote_model_id == "v5_6_ru"


def test_same_version_remote_changed():
    local_meta = ModelMetadata(
        model_id="v5_5_ru",
        filename="v5_5_ru_ru.pt",
        path="/path/v5_5_ru_ru.pt",
        size_bytes=1000,
        sha256="hash123",
        installed_at="2026-08-06T12:00:00+00:00",
        valid=True,
    )

    mm = MagicMock(spec=ModelManager)
    mm.get_active_model.return_value = local_meta

    checker = UpdateChecker(model_manager=mm)

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = SAMPLE_OFFICIAL_MANIFEST

    with patch("httpx.Client.get", return_value=mock_response):
        # Удаленный файл имеет другой размер
        with patch.object(checker, "_fetch_remote_head_info", return_value={"size": 1500}):
            res = checker.check_for_updates()
            assert res.status == "same_version_remote_changed"
            assert res.local_model_id == "v5_5_ru"
            assert res.remote_model_id == "v5_5_ru"


def test_remote_unavailable_http_error():
    local_meta = ModelMetadata(
        model_id="v5_5_ru",
        size_bytes=1000,
        valid=True,
    )

    mm = MagicMock(spec=ModelManager)
    mm.get_active_model.return_value = local_meta

    checker = UpdateChecker(model_manager=mm)

    with patch("httpx.Client.get", side_effect=Exception("Connection refused")):
        res = checker.check_for_updates()
        assert res.status == "remote_unavailable"
        assert "Официальный источник недоступен" in res.message


def test_manifest_invalid_structure():
    local_meta = ModelMetadata(model_id="v5_5_ru", valid=True)

    mm = MagicMock(spec=ModelManager)
    mm.get_active_model.return_value = local_meta

    checker = UpdateChecker(model_manager=mm)

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "invalid_yaml: [unclosed list"

    with patch("httpx.Client.get", return_value=mock_response):
        res = checker.check_for_updates()
        assert res.status == "manifest_invalid"


def test_local_model_missing():
    mm = MagicMock(spec=ModelManager)
    mm.get_active_model.return_value = None

    checker = UpdateChecker(model_manager=mm)
    res = checker.check_for_updates()
    assert res.status == "local_model_missing"


def test_unexpected_fields_in_manifest():
    manifest_with_extra = """
unexpected_global_key: "some_value"
tts_models:
  ru:
    v5_5_ru:
      latest:
        package: 'https://models.silero.ai/models/tts/ru/v5_5_ru.pt'
        extra_unknown_field: 12345
"""
    local_meta = ModelMetadata(model_id="v5_5_ru", size_bytes=1000, valid=True)
    mm = MagicMock(spec=ModelManager)
    mm.get_active_model.return_value = local_meta

    checker = UpdateChecker(model_manager=mm)
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = manifest_with_extra

    with patch("httpx.Client.get", return_value=mock_response):
        with patch.object(checker, "_fetch_remote_head_info", return_value={"size": 1000}):
            res = checker.check_for_updates()
            assert res.status == "up_to_date"


def test_format_update_check_result():
    res1 = CheckUpdateResult(
        status="up_to_date",
        local_model_id="v5_5_ru",
        local_sha256="50081637b602126ee06cb3bc8a744d25651d2da149ee8864b9a379bfdd934437",
        local_installed_at="2026-08-06",
        remote_model_id="v5_5_ru",
    )
    formatted1 = format_update_check_result(res1)
    assert "Локальная модель" in formatted1
    assert "v5_5_ru" in formatted1
    assert "Обновлений не обнаружено." in formatted1

    res2 = CheckUpdateResult(
        status="update_available",
        local_model_id="v5_5_ru",
        remote_model_id="v5_6_ru",
    )
    formatted2 = format_update_check_result(res2)
    assert "v5_6_ru" in formatted2
    assert "Доступна новая модель." in formatted2

    res3 = CheckUpdateResult(
        status="same_version_remote_changed",
        local_model_id="v5_5_ru",
        remote_model_id="v5_5_ru",
    )
    formatted3 = format_update_check_result(res3)
    assert "Файл модели изменён." in formatted3
