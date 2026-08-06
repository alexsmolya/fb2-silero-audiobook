"""
Unit-тесты для модуля src.core.download_manager (DownloadManager).

Все сетевые обращения к HTTP / Silero полностью смокированы.
Все файлы создаются во временных папках pytest (tmp_path).
"""

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import httpx
import pytest
from src.core.download_manager import (
    DownloadManager,
    DownloadProgress,
    DownloadRequest,
    DownloadResult,
    validate_download_url,
)
from src.core.model_manager import ModelManager, ModelMetadata
from src.core.update_checker import CheckUpdateResult, UpdateChecker

DUMMY_URL = "https://models.silero.ai/models/tts/ru/v5_6_ru.pt"
DUMMY_MODEL_DATA = b"x" * (2 * 1024 * 1024)  # 2 МБ бинарных данных


def make_mock_client(status_code=200, url=DUMMY_URL, chunks=None, headers=None):
    """Вспомогательный хелпер для создания полностью настроенного mock httpx.Client."""
    mock_response = MagicMock()
    mock_response.status_code = status_code
    mock_response.url = httpx.URL(url)

    if chunks is None:
        chunks = [DUMMY_MODEL_DATA]

    total_len = sum(len(c) for c in chunks)
    default_headers = {"Content-Length": str(total_len)}
    if headers:
        default_headers.update(headers)

    mock_response.headers = default_headers
    mock_response.iter_bytes.return_value = chunks

    mock_client = MagicMock()
    mock_client.__enter__.return_value = mock_client
    mock_client.stream.return_value.__enter__.return_value = mock_response
    return mock_client


def test_validate_download_url():
    assert validate_download_url("https://models.silero.ai/models/tts/ru/v5_5_ru.pt")[0] is True
    assert validate_download_url("http://models.silero.ai/models/tts/ru/v5_5_ru.pt")[0] is False  # HTTP не разрешен
    assert validate_download_url("file:///etc/passwd")[0] is False  # file:// не разрешен
    assert validate_download_url("https://localhost/model.pt")[0] is False  # localhost не разрешен
    assert validate_download_url("https://192.168.1.1/model.pt")[0] is False  # Приватный IP не разрешен
    assert validate_download_url("https://user:pass@models.silero.ai/model.pt")[0] is False  # Логин/пароль


def test_dry_run_without_download(tmp_path: Path):
    mm = ModelManager(models_dir=tmp_path / "models")
    dl = DownloadManager(model_manager=mm)

    req = DownloadRequest(
        model_id="v5_6_ru",
        url=DUMMY_URL,
        expected_size_bytes=len(DUMMY_MODEL_DATA),
    )

    res = dl.download_model(req, dry_run=True)
    assert res.status == "ready"
    assert res.dry_run is True
    # Убеждаемся, что файлы не вылились на диск
    target_file = tmp_path / "models" / "v5_6_ru" / "v5_6_ru.pt"
    assert not target_file.exists()


def test_successful_streaming_download(tmp_path: Path):
    mm = ModelManager(models_dir=tmp_path / "models")
    dl = DownloadManager(model_manager=mm)

    req = DownloadRequest(
        model_id="v5_6_ru",
        url=DUMMY_URL,
        expected_size_bytes=len(DUMMY_MODEL_DATA),
    )

    mock_client = make_mock_client()

    with patch("httpx.Client", return_value=mock_client):
        res = dl.download_model(req)
        assert res.status == "success"
        assert res.downloaded_bytes == len(DUMMY_MODEL_DATA)

        target_file = tmp_path / "models" / "v5_6_ru" / "v5_6_ru.pt"
        assert target_file.is_file()

        meta_file = tmp_path / "models" / "v5_6_ru" / "metadata.json"
        assert meta_file.is_file()
        meta_data = json.loads(meta_file.read_text(encoding="utf-8"))
        assert meta_data["active"] is False  # КРИТИЧЕСКАЯ ПРОВЕРКА
        assert meta_data["model_id"] == "v5_6_ru"


def test_progress_with_known_size(tmp_path: Path):
    mm = ModelManager(models_dir=tmp_path / "models")
    dl = DownloadManager(model_manager=mm)

    req = DownloadRequest(
        model_id="v5_6_ru",
        url=DUMMY_URL,
        expected_size_bytes=len(DUMMY_MODEL_DATA),
    )

    progress_reports = []

    def callback(prog: DownloadProgress):
        progress_reports.append(prog)

    mock_client = make_mock_client(chunks=[DUMMY_MODEL_DATA[:1024], DUMMY_MODEL_DATA[1024:]])

    with patch("httpx.Client", return_value=mock_client):
        res = dl.download_model(req, progress_callback=callback)
        assert res.status == "success"
        assert len(progress_reports) == 2
        assert progress_reports[-1].percent == 100.0


def test_progress_with_unknown_size(tmp_path: Path):
    mm = ModelManager(models_dir=tmp_path / "models")
    dl = DownloadManager(model_manager=mm)

    req = DownloadRequest(model_id="v5_6_ru", url=DUMMY_URL)

    progress_reports = []
    mock_client = make_mock_client(chunks=[DUMMY_MODEL_DATA])
    # Убираем Content-Length из ответа
    mock_client.stream.return_value.__enter__.return_value.headers = {}

    with patch("httpx.Client", return_value=mock_client):
        res = dl.download_model(req, progress_callback=lambda p: progress_reports.append(p))
        assert res.status == "success"
        assert progress_reports[-1].percent is None


def test_network_timeout(tmp_path: Path):
    mm = ModelManager(models_dir=tmp_path / "models")
    dl = DownloadManager(model_manager=mm)

    req = DownloadRequest(model_id="v5_6_ru", url=DUMMY_URL)

    mock_client = MagicMock()
    mock_client.__enter__.return_value = mock_client
    mock_client.stream.side_effect = httpx.ReadTimeout("Read timeout")

    with patch("httpx.Client", return_value=mock_client):
        res = dl.download_model(req)
        assert res.status == "timeout"
        temp_dir = tmp_path / "models" / ".tmp_downloads"
        assert len(list(temp_dir.glob("*.part"))) == 0


def test_http_404_error(tmp_path: Path):
    mm = ModelManager(models_dir=tmp_path / "models")
    dl = DownloadManager(model_manager=mm)

    req = DownloadRequest(model_id="v5_6_ru", url=DUMMY_URL)
    mock_client = make_mock_client(status_code=404)

    with patch("httpx.Client", return_value=mock_client):
        res = dl.download_model(req)
        assert res.status == "network_error"
        assert "404" in res.message


def test_redirect_to_localhost_blocked(tmp_path: Path):
    mm = ModelManager(models_dir=tmp_path / "models")
    dl = DownloadManager(model_manager=mm)

    req = DownloadRequest(model_id="v5_6_ru", url=DUMMY_URL)
    mock_client = make_mock_client(url="http://localhost/malicious.pt")

    with patch("httpx.Client", return_value=mock_client):
        res = dl.download_model(req)
        assert res.status == "ssrf_blocked"


def test_insufficient_space(tmp_path: Path):
    mm = ModelManager(models_dir=tmp_path / "models")
    dl = DownloadManager(model_manager=mm)

    req = DownloadRequest(
        model_id="v5_6_ru",
        url=DUMMY_URL,
        expected_size_bytes=100 * 1024 * 1024 * 1024,  # 100 ГБ
    )

    with patch("shutil.disk_usage", return_value=(1000, 900, 100)):  # Свободно 100 байт
        res = dl.download_model(req)
        assert res.status == "insufficient_space"


def test_cancellation_download(tmp_path: Path):
    mm = ModelManager(models_dir=tmp_path / "models")
    dl = DownloadManager(model_manager=mm)

    req = DownloadRequest(model_id="v5_6_ru", url=DUMMY_URL)
    mock_client = make_mock_client(chunks=[b"chunk1", b"chunk2"])

    with patch("httpx.Client", return_value=mock_client):
        res = dl.download_model(req, cancellation_check=lambda: True)
        assert res.status == "cancelled"
        temp_dir = tmp_path / "models" / ".tmp_downloads"
        assert len(list(temp_dir.glob("*.part"))) == 0


def test_size_mismatch(tmp_path: Path):
    mm = ModelManager(models_dir=tmp_path / "models")
    dl = DownloadManager(model_manager=mm)

    req = DownloadRequest(
        model_id="v5_6_ru",
        url=DUMMY_URL,
        expected_size_bytes=999999,  # Отличается от фактического
    )

    mock_client = make_mock_client()

    with patch("httpx.Client", return_value=mock_client):
        res = dl.download_model(req)
        assert res.status == "size_mismatch"


def test_official_sha256_mismatch(tmp_path: Path):
    mm = ModelManager(models_dir=tmp_path / "models")
    dl = DownloadManager(model_manager=mm)

    req = DownloadRequest(
        model_id="v5_6_ru",
        url=DUMMY_URL,
        remote_sha256="0000000000000000000000000000000000000000000000000000000000000000",
    )

    mock_client = make_mock_client()

    with patch("httpx.Client", return_value=mock_client):
        res = dl.download_model(req)
        assert res.status == "hash_mismatch"


def test_already_downloaded_identical_file(tmp_path: Path):
    mm = ModelManager(models_dir=tmp_path / "models")

    target_dir = tmp_path / "models" / "v5_6_ru"
    target_dir.mkdir(parents=True)
    target_file = target_dir / "v5_6_ru.pt"
    target_file.write_bytes(DUMMY_MODEL_DATA)

    import hashlib
    actual_sha = hashlib.sha256(DUMMY_MODEL_DATA).hexdigest()

    dl = DownloadManager(model_manager=mm)
    req = DownloadRequest(
        model_id="v5_6_ru",
        url=DUMMY_URL,
        expected_size_bytes=len(DUMMY_MODEL_DATA),
        remote_sha256=actual_sha,
    )

    res = dl.download_model(req)
    assert res.status == "already_downloaded"
    assert res.installed_path == str(target_file.resolve())


def test_target_conflict_different_file(tmp_path: Path):
    mm = ModelManager(models_dir=tmp_path / "models")

    target_dir = tmp_path / "models" / "v5_6_ru"
    target_dir.mkdir(parents=True)
    target_file = target_dir / "v5_6_ru.pt"
    target_file.write_bytes(b"different content")

    dl = DownloadManager(model_manager=mm)
    req = DownloadRequest(
        model_id="v5_6_ru",
        url=DUMMY_URL,
        expected_size_bytes=len(DUMMY_MODEL_DATA),
    )

    res = dl.download_model(req)
    assert res.status == "target_conflict"


def test_old_model_remains_active(tmp_path: Path):
    models_dir = tmp_path / "models"
    mm = ModelManager(models_dir=models_dir)

    # 1. Создаем существующую активную модель v5_5_ru
    v55_dir = models_dir / "v5_5_ru"
    v55_dir.mkdir(parents=True)
    (v55_dir / "v5_5_ru_ru.pt").write_bytes(b"active v55 model data")
    (v55_dir / "metadata.json").write_text(
        json.dumps({"model_id": "v5_5_ru", "active": True}), encoding="utf-8"
    )

    assert mm.get_active_model().model_id == "v5_5_ru"

    # 2. Скачиваем модель v5_6_ru
    dl = DownloadManager(model_manager=mm)
    req = DownloadRequest(model_id="v5_6_ru", url=DUMMY_URL)
    mock_client = make_mock_client()

    with patch("httpx.Client", return_value=mock_client):
        res = dl.download_model(req)
        assert res.status == "success"

        # КРИТИЧЕСКИЕ ПРОВЕРКИ:
        # Старая модель осталась активной
        assert mm.get_active_model().model_id == "v5_5_ru"

        # Новая модель имеет active=False
        new_info = mm.get_model_info("v5_6_ru")
        assert new_info.active is False


def test_progress_callback_error_handling(tmp_path: Path):
    mm = ModelManager(models_dir=tmp_path / "models")
    dl = DownloadManager(model_manager=mm)

    req = DownloadRequest(model_id="v5_6_ru", url=DUMMY_URL)

    def buggy_callback(prog):
        raise RuntimeError("Callback crashed!")

    mock_client = make_mock_client()

    with patch("httpx.Client", return_value=mock_client):
        # Скачивание должно завершиться с успехом несмотря на ошибку callback
        res = dl.download_model(req, progress_callback=buggy_callback)
        assert res.status == "success"
