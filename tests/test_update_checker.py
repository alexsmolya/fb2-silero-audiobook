"""
Unit-тесты для расширенного модуля src.core.update_checker (UpdateChecker).

Все сетевые обращения к GitHub / silero.ai полностью смокированы.
"""

from pathlib import Path
from unittest.mock import MagicMock, patch

import httpx
import pytest
from src.core.model_manager import ModelManager, ModelMetadata
from src.core.update_checker import (
    CheckUpdateResult,
    RemoteArtifactMetadata,
    UpdateChecker,
    evaluate_artifact_comparison,
    format_update_check_result,
    normalize_etag,
    normalize_sha256,
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


def test_normalize_etag():
    etag, is_weak = normalize_etag('W/"123456789"')
    assert etag == "123456789"
    assert is_weak is True

    etag2, is_weak2 = normalize_etag('"abcdef"')
    assert etag2 == "abcdef"
    assert is_weak2 is False

    etag3, is_weak3 = normalize_etag(None)
    assert etag3 is None
    assert is_weak3 is False


def test_normalize_sha256():
    valid_sha = "50081637b602126ee06cb3bc8a744d25651d2da149ee8864b9a379bfdd934437"
    assert normalize_sha256(valid_sha.upper()) == valid_sha
    assert normalize_sha256("short_invalid_sha") is None


def test_parse_model_version():
    assert parse_model_version("v5_5_ru") == (5, 5)
    assert parse_model_version("v5_6_ru") == (5, 6)
    assert parse_model_version("v6_0_ru") == (6, 0)
    assert parse_model_version("v5_ru") == (5, 0)


# 1. Одинаковый официальный SHA-256
def test_identical_official_sha256():
    local_meta = ModelMetadata(
        model_id="v5_5_ru",
        sha256="50081637b602126ee06cb3bc8a744d25651d2da149ee8864b9a379bfdd934437",
        valid=True,
    )
    remote = RemoteArtifactMetadata(
        url="https://models.silero.ai/models/tts/ru/v5_5_ru.pt",
        sha256="50081637b602126ee06cb3bc8a744d25651d2da149ee8864b9a379bfdd934437",
    )
    res = evaluate_artifact_comparison(local_meta, remote, "v5_5_ru")
    assert res.status == "up_to_date"
    assert res.comparison_confidence == "high"
    assert "sha256" in res.comparison_basis


# 2. Различный официальный SHA-256
def test_different_official_sha256():
    local_meta = ModelMetadata(
        model_id="v5_5_ru",
        sha256="50081637b602126ee06cb3bc8a744d25651d2da149ee8864b9a379bfdd934437",
        valid=True,
    )
    remote = RemoteArtifactMetadata(
        url="https://models.silero.ai/models/tts/ru/v5_5_ru.pt",
        sha256="1111111111111111111111111111111111111111111111111111111111111111",
    )
    res = evaluate_artifact_comparison(local_meta, remote, "v5_5_ru")
    assert res.status == "same_version_remote_changed"
    assert res.comparison_confidence == "high"
    assert "sha256" in res.comparison_basis


# 3. Одинаковый strong ETag
def test_identical_strong_etag():
    local_meta = ModelMetadata(
        model_id="v5_5_ru",
        remote_artifact={"etag": "etag_abc_123"},
        valid=True,
    )
    remote = RemoteArtifactMetadata(
        url="https://models.silero.ai/models/tts/ru/v5_5_ru.pt",
        etag="etag_abc_123",
        etag_is_weak=False,
    )
    res = evaluate_artifact_comparison(local_meta, remote, "v5_5_ru")
    assert res.status == "up_to_date"
    assert res.comparison_confidence == "high"
    assert "strong_etag" in res.comparison_basis


# 4. Различный strong ETag
def test_different_strong_etag():
    local_meta = ModelMetadata(
        model_id="v5_5_ru",
        remote_artifact={"etag": "etag_old"},
        valid=True,
    )
    remote = RemoteArtifactMetadata(
        url="https://models.silero.ai/models/tts/ru/v5_5_ru.pt",
        etag="etag_new",
        etag_is_weak=False,
    )
    res = evaluate_artifact_comparison(local_meta, remote, "v5_5_ru")
    assert res.status == "same_version_remote_changed"
    assert res.comparison_confidence == "high"
    assert "strong_etag" in res.comparison_basis


# 5. Weak ETag (не используется как единственный high proof)
def test_weak_etag_handling():
    etag, is_weak = normalize_etag('W/"weak_123"')
    assert is_weak is True
    assert etag == "weak_123"


# 6. Одинаковые Last-Modified и размер
def test_identical_last_modified_and_size():
    local_meta = ModelMetadata(
        model_id="v5_5_ru",
        size_bytes=1000,
        remote_artifact={"last_modified": "Thu, 16 Apr 2026 10:03:41 GMT"},
        valid=True,
    )
    remote = RemoteArtifactMetadata(
        url="https://models.silero.ai/models/tts/ru/v5_5_ru.pt",
        size_bytes=1000,
        last_modified="Thu, 16 Apr 2026 10:03:41 GMT",
    )
    res = evaluate_artifact_comparison(local_meta, remote, "v5_5_ru")
    assert res.status == "up_to_date"
    assert res.comparison_confidence == "medium"
    assert "last_modified" in res.comparison_basis


# 7. Изменённый Last-Modified
def test_changed_last_modified():
    local_meta = ModelMetadata(
        model_id="v5_5_ru",
        size_bytes=1000,
        remote_artifact={"last_modified": "Thu, 16 Apr 2026 10:03:41 GMT"},
        valid=True,
    )
    remote = RemoteArtifactMetadata(
        url="https://models.silero.ai/models/tts/ru/v5_5_ru.pt",
        size_bytes=1000,
        last_modified="Fri, 17 Apr 2026 12:00:00 GMT",
    )
    res = evaluate_artifact_comparison(local_meta, remote, "v5_5_ru")
    assert res.status == "same_version_remote_changed"
    assert res.comparison_confidence == "medium"
    assert "last_modified" in res.comparison_basis


# 8. Изменённый размер
def test_changed_size():
    local_meta = ModelMetadata(
        model_id="v5_5_ru",
        size_bytes=1000,
        valid=True,
    )
    remote = RemoteArtifactMetadata(
        url="https://models.silero.ai/models/tts/ru/v5_5_ru.pt",
        size_bytes=2000,
    )
    res = evaluate_artifact_comparison(local_meta, remote, "v5_5_ru")
    assert res.status == "same_version_remote_changed"
    assert res.comparison_confidence == "medium"
    assert "content_length" in res.comparison_basis


# 9. Совпадает только размер (без базовых метаданных)
def test_size_matches_only_no_baseline():
    local_meta = ModelMetadata(
        model_id="v5_5_ru",
        size_bytes=1000,
        valid=True,
    )
    remote = RemoteArtifactMetadata(
        url="https://models.silero.ai/models/tts/ru/v5_5_ru.pt",
        size_bytes=1000,
    )
    res = evaluate_artifact_comparison(local_meta, remote, "v5_5_ru")
    assert res.status == "up_to_date"
    assert res.comparison_confidence == "low"
    assert res.comparison_basis == ["content_length"]


# 10 & 16. Обратная совместимость старого metadata без remote_artifact
def test_backward_compatibility_old_metadata():
    local_meta = ModelMetadata(
        model_id="v5_5_ru",
        size_bytes=1000,
        remote_artifact=None,
        valid=True,
    )
    remote = RemoteArtifactMetadata(
        url="https://models.silero.ai/models/tts/ru/v5_5_ru.pt",
        size_bytes=1000,
        last_modified="Thu, 16 Apr 2026 10:03:41 GMT",
    )
    res = evaluate_artifact_comparison(local_meta, remote, "v5_5_ru")
    # Так как локально remote_artifact был None, ETag/Last-Modified снимка нет.
    # Результат должен объявлять low confidence up_to_date, а не ошибочный same_version_remote_changed
    assert res.status == "up_to_date"
    assert res.comparison_confidence == "low"
    assert res.comparison_basis == ["content_length"]


# 11. Удалённый сервер не отдаёт необязательные заголовки
def test_remote_server_no_optional_headers():
    local_meta = ModelMetadata(model_id="v5_5_ru", size_bytes=1000, valid=True)
    remote = RemoteArtifactMetadata(url="http://example.com/model.pt", size_bytes=1000)
    res = evaluate_artifact_comparison(local_meta, remote, "v5_5_ru")
    assert res.status == "up_to_date"
    assert res.comparison_confidence == "low"


# 12. HEAD не поддерживается / падает
def test_head_not_supported():
    local_meta = ModelMetadata(model_id="v5_5_ru", size_bytes=1000, valid=True)
    mm = MagicMock(spec=ModelManager)
    mm.get_active_model.return_value = local_meta

    checker = UpdateChecker(model_manager=mm)
    mock_manifest = MagicMock()
    mock_manifest.status_code = 200
    mock_manifest.text = SAMPLE_OFFICIAL_MANIFEST

    with patch("httpx.Client.get", return_value=mock_manifest):
        with patch.object(checker, "_fetch_remote_artifact_metadata") as mock_fetch:
            mock_fetch.return_value = RemoteArtifactMetadata(url="http://test.url")
            res = checker.check_for_updates()
            assert res.status == "up_to_date"
            assert res.comparison_confidence == "none"


# 13. Connect timeout
def test_connect_timeout():
    local_meta = ModelMetadata(model_id="v5_5_ru", valid=True)
    mm = MagicMock(spec=ModelManager)
    mm.get_active_model.return_value = local_meta

    checker = UpdateChecker(model_manager=mm)
    with patch("httpx.Client.get", side_effect=httpx.ConnectTimeout("Connect timed out")):
        res = checker.check_for_updates()
        assert res.status == "remote_unavailable"
        assert "Connect timed out" in res.message


# 14. Read timeout
def test_read_timeout():
    local_meta = ModelMetadata(model_id="v5_5_ru", valid=True)
    mm = MagicMock(spec=ModelManager)
    mm.get_active_model.return_value = local_meta

    checker = UpdateChecker(model_manager=mm)
    with patch("httpx.Client.get", side_effect=httpx.ReadTimeout("Read timed out")):
        res = checker.check_for_updates()
        assert res.status == "remote_unavailable"
        assert "Read timed out" in res.message


# 15. Повреждённое значение Content-Length
def test_corrupted_content_length():
    local_meta = ModelMetadata(model_id="v5_5_ru", valid=True)
    mm = MagicMock(spec=ModelManager)
    mm.get_active_model.return_value = local_meta

    checker = UpdateChecker(model_manager=mm)
    mock_res = MagicMock()
    mock_res.status_code = 200
    mock_res.headers = {"Content-Length": "not_an_integer"}

    with patch("httpx.Client.head", return_value=mock_res):
        meta = checker._fetch_remote_artifact_metadata("http://test.url")
        assert meta.size_bytes is None


# 17. Команда проверки НЕ изменяет metadata.json
def test_check_updates_does_not_modify_metadata(tmp_path: Path):
    model_dir = tmp_path / "models" / "v5_5_ru"
    model_dir.mkdir(parents=True)
    pt_file = model_dir / "v5_5_ru_ru.pt"
    pt_file.write_bytes(b"model data")

    meta_file = model_dir / "metadata.json"
    initial_content = '{\n  "model_id": "v5_5_ru",\n  "active": true\n}'
    meta_file.write_text(initial_content, encoding="utf-8")

    mm = ModelManager(models_dir=tmp_path / "models")
    checker = UpdateChecker(model_manager=mm)

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = SAMPLE_OFFICIAL_MANIFEST

    with patch("httpx.Client.get", return_value=mock_response):
        with patch.object(checker, "_fetch_remote_artifact_metadata", return_value=RemoteArtifactMetadata(size_bytes=10)):
            res = checker.check_for_updates()
            assert res.status == "up_to_date"
            # Убеждаемся, что metadata.json НЕ изменился
            assert meta_file.read_text(encoding="utf-8") == initial_content


def test_format_update_check_result():
    res1 = CheckUpdateResult(
        status="up_to_date",
        comparison_confidence="low",
        comparison_basis=["content_length"],
        local_model_id="v5_5_ru",
        local_sha256="50081637b602126ee06cb3bc8a744d25651d2da149ee8864b9a379bfdd934437",
        local_installed_at="2026-08-06",
        remote_model_id="v5_5_ru",
        message="Новая версия не обнаружена, но идентичность файла нельзя доказать на 100% (совпадает только размер).",
    )
    formatted1 = format_update_check_result(res1)
    assert "Локальная модель" in formatted1
    assert "v5_5_ru" in formatted1
    assert "Уровень уверенности:" in formatted1
    assert "Низкий" in formatted1

    res2 = CheckUpdateResult(
        status="same_version_remote_changed",
        comparison_confidence="high",
        comparison_basis=["strong_etag"],
        local_model_id="v5_5_ru",
        remote_model_id="v5_5_ru",
    )
    formatted2 = format_update_check_result(res2)
    assert "Версия имеет прежнее имя, но удалённый файл изменён." in formatted2
    assert "Изменился ETag." in formatted2
