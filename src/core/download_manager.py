"""
Модуль асинхронной/потоковой загрузки официальных моделей Silero TTS (DownloadManager).

Выполняет безопасную потоковую загрузку файлов моделей во временный каталог,
проверку целостности (размер, SHA-256), защиту от SSRF, атомарную установку
и регистрацию в ModelManager с обязательным параметром active=False.
"""

from __future__ import annotations

import argparse
import ipaddress
import json
import logging
import os
import shutil
import sys
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple
from urllib.parse import urlparse
from uuid import uuid4

import httpx

from src.core.model_inspector import _calculate_sha256, _format_size
from src.core.model_manager import ModelManager, ModelMetadata

logger = logging.getLogger(__name__)

ALLOWED_SCHEMES = {"https"}
ALLOWED_HOSTNAMES = {
    "models.silero.ai",
    "raw.githubusercontent.com",
    "github.com",
    "objects.githubusercontent.com",
}
CHUNK_SIZE = 128 * 1024  # 128 KiB
DEFAULT_CONNECT_TIMEOUT = 3.0
DEFAULT_READ_TIMEOUT = 10.0


@dataclass
class DownloadRequest:
    """Параметры запроса на скачивание модели."""

    model_id: str
    url: str
    expected_size_bytes: Optional[int] = None
    remote_etag: Optional[str] = None
    remote_last_modified: Optional[str] = None
    remote_sha256: Optional[str] = None
    destination_root: Optional[Path] = None


@dataclass
class DownloadProgress:
    """Информация о текущем прогрессе скачивания."""

    downloaded_bytes: int
    total_bytes: Optional[int] = None
    percent: Optional[float] = None
    bytes_per_second: float = 0.0
    elapsed_seconds: float = 0.0


@dataclass
class DownloadResult:
    """Результат операции скачивания и установки модели."""

    status: str
    # Статусы: "success" | "already_downloaded" | "no_update_available" | "cancelled" |
    #          "network_error" | "timeout" | "size_mismatch" | "hash_mismatch" |
    #          "target_conflict" | "manifest_error" | "insufficient_space" | "write_error" |
    #          "validation_error" | "ssrf_blocked" | "error"

    model_id: Optional[str] = None
    url: Optional[str] = None
    temporary_path: Optional[str] = None
    installed_path: Optional[str] = None
    downloaded_bytes: Optional[int] = None
    sha256: Optional[str] = None
    expected_size_bytes: Optional[int] = None
    remote_etag: Optional[str] = None
    remote_last_modified: Optional[str] = None
    message: str = ""
    dry_run: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Преобразовать в словарь."""
        return asdict(self)


def validate_download_url(url: str, allowed_hostnames: Optional[set[str]] = None) -> Tuple[bool, str]:
    """Проверка URL на безопасность и SSRF уязвимости."""
    if not url or not isinstance(url, str):
        return False, "URL скачивания не указан или имеет неверный тип."

    try:
        parsed = urlparse(url.strip())
    except Exception as exc:
        return False, f"Некорректный синтаксис URL: {exc}"

    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        return False, f"Недопустимая схема URL '{parsed.scheme}'. Разрешена только HTTPS."

    if not parsed.hostname:
        return False, "URL не содержит имя хоста."

    if parsed.username or parsed.password:
        return False, "Запрещено передавать учетные данные в URL."

    host = parsed.hostname.lower()

    # Проверка на локальные и приватные IP-адреса
    try:
        ip = ipaddress.ip_address(host)
        if ip.is_loopback or ip.is_private or ip.is_link_local or ip.is_unspecified:
            return False, f"Запрещен скачивание с приватного или локального IP-адреса '{host}'."
    except ValueError:
        # Не IP, а доменное имя — проверяем стандартные блокировки
        if host in ("localhost", "localhost.localdomain") or host.endswith(".local"):
            return False, f"Запрещен скачивание с локального хоста '{host}'."

    # Проверка списка доверенных хостов (если передан)
    hosts_to_check = allowed_hostnames or ALLOWED_HOSTNAMES
    if hosts_to_check:
        matched = False
        for allowed in hosts_to_check:
            if host == allowed or host.endswith("." + allowed):
                matched = True
                break
        if not matched:
            return False, f"Хост '{host}' не входит в список доверенных источников официальных моделей."

    return True, "OK"


class DownloadManager:
    """Класс управления асинхронной/потоковой загрузкой официальных моделей."""

    def __init__(
        self,
        model_manager: Optional[ModelManager] = None,
        connect_timeout: float = DEFAULT_CONNECT_TIMEOUT,
        read_timeout: float = DEFAULT_READ_TIMEOUT,
    ):
        self.model_manager = model_manager or ModelManager()
        self.connect_timeout = connect_timeout
        self.read_timeout = read_timeout

    def get_temp_dir(self) -> Path:
        """Получить временную папку загрузок .tmp_downloads/."""
        temp_dir = self.model_manager.get_models_dir() / ".tmp_downloads"
        temp_dir.mkdir(parents=True, exist_ok=True)
        return temp_dir

    def download_model(
        self,
        request: DownloadRequest,
        progress_callback: Optional[Callable[[DownloadProgress], None]] = None,
        cancellation_check: Optional[Callable[[], bool]] = None,
        dry_run: bool = False,
    ) -> DownloadResult:
        """Потоковая загрузка модели в пользовательское хранилище."""
        # 1. Валидация URL и SSRF защита
        valid_url, url_err = validate_download_url(request.url)
        if not valid_url:
            return DownloadResult(
                status="ssrf_blocked",
                model_id=request.model_id,
                url=request.url,
                message=f"Ошибка безопасности URL: {url_err}",
                dry_run=dry_run,
            )

        # 2. Определение целевого пути и проверка конфликта
        models_dir = request.destination_root or self.model_manager.get_models_dir()
        target_dir = models_dir / request.model_id
        target_filename = f"{request.model_id}.pt"
        target_file = target_dir / target_filename

        # Если целевой файл уже существует — проверяем идентичность
        if target_file.is_file():
            stat = target_file.stat()
            existing_size = stat.st_size
            existing_sha256 = _calculate_sha256(target_file)

            size_matches = (request.expected_size_bytes is None) or (existing_size == request.expected_size_bytes)
            hash_matches = (request.remote_sha256 is None) or (existing_sha256.lower() == request.remote_sha256.lower())

            if size_matches and hash_matches:
                return DownloadResult(
                    status="already_downloaded",
                    model_id=request.model_id,
                    url=request.url,
                    installed_path=str(target_file.resolve()),
                    downloaded_bytes=existing_size,
                    sha256=existing_sha256,
                    message="Модель уже скачана и зарегистрирована в хранилище.",
                    dry_run=dry_run,
                )
            else:
                return DownloadResult(
                    status="target_conflict",
                    model_id=request.model_id,
                    url=request.url,
                    installed_path=str(target_file.resolve()),
                    downloaded_bytes=existing_size,
                    sha256=existing_sha256,
                    message=f"Целевой файл {target_file} существует, но отличается по размеру или хешу.",
                    dry_run=dry_run,
                )

        # 3. Проверка свободного места на диске
        if request.expected_size_bytes:
            try:
                total, used, free = shutil.disk_usage(models_dir)
                required = request.expected_size_bytes + 20 * 1024 * 1024  # размер + 20 МБ
                if free < required:
                    return DownloadResult(
                        status="insufficient_space",
                        model_id=request.model_id,
                        url=request.url,
                        expected_size_bytes=request.expected_size_bytes,
                        message=f"Недостаточно свободного места на диске ({_format_size(free)} свободно, требуется {_format_size(required)}).",
                        dry_run=dry_run,
                    )
            except Exception as exc:
                logger.debug("Не удалось проверить свободное место: %s", exc)

        # 4. Dry-run режим
        if dry_run:
            return DownloadResult(
                status="ready",
                model_id=request.model_id,
                url=request.url,
                installed_path=str(target_file.resolve()),
                expected_size_bytes=request.expected_size_bytes,
                message="Готово к скачиванию. Физическая загрузка будет выполнена при запуске с --yes.",
                dry_run=True,
            )

        # 5. Подготовка временного файла
        temp_dir = self.get_temp_dir()
        temp_filename = f"{request.model_id}_{uuid4().hex[:8]}.pt.part"
        temp_file = temp_dir / temp_filename

        # 6. Потоковая загрузка с отслеживанием прогресса и таймаутами
        timeout = httpx.Timeout(
            connect=self.connect_timeout,
            read=self.read_timeout,
            write=self.read_timeout,
            pool=self.read_timeout,
        )

        import hashlib

        hasher = hashlib.sha256()
        downloaded_bytes = 0
        start_time = time.monotonic()

        try:
            with httpx.Client(timeout=timeout, follow_redirects=True) as client:
                with client.stream("GET", request.url) as response:
                    # Повторная валидация после возможного редиректа
                    final_url = str(response.url)
                    valid_final, final_err = validate_download_url(final_url)
                    if not valid_final:
                        self._safe_remove(temp_file)
                        return DownloadResult(
                            status="ssrf_blocked",
                            model_id=request.model_id,
                            url=final_url,
                            message=f"Ошибка безопасности после перенаправления: {final_err}",
                        )

                    if response.status_code != 200:
                        self._safe_remove(temp_file)
                        status_name = "timeout" if response.status_code == 408 else "network_error"
                        return DownloadResult(
                            status=status_name,
                            model_id=request.model_id,
                            url=final_url,
                            message=f"Сервер вернул ошибку HTTP {response.status_code}.",
                        )

                    # Определяем точный размер из заголовка, если был не известен
                    total_bytes = request.expected_size_bytes
                    if total_bytes is None and "Content-Length" in response.headers:
                        try:
                            total_bytes = int(response.headers["Content-Length"])
                        except ValueError:
                            pass

                    with temp_file.open("wb") as f_out:
                        for chunk in response.iter_bytes(chunk_size=CHUNK_SIZE):
                            # Проверка отмены
                            if cancellation_check and cancellation_check():
                                f_out.close()
                                self._safe_remove(temp_file)
                                return DownloadResult(
                                    status="cancelled",
                                    model_id=request.model_id,
                                    url=final_url,
                                    temporary_path=str(temp_file),
                                    message="Загрузка модели отменена пользователем.",
                                )

                            f_out.write(chunk)
                            hasher.update(chunk)
                            downloaded_bytes += len(chunk)

                            # Обновление прогресса
                            if progress_callback:
                                elapsed = time.monotonic() - start_time
                                bps = downloaded_bytes / elapsed if elapsed > 0 else 0.0
                                percent = (
                                    (downloaded_bytes / total_bytes * 100.0)
                                    if total_bytes and total_bytes > 0
                                    else None
                                )
                                prog = DownloadProgress(
                                    downloaded_bytes=downloaded_bytes,
                                    total_bytes=total_bytes,
                                    percent=percent,
                                    bytes_per_second=bps,
                                    elapsed_seconds=elapsed,
                                )
                                try:
                                    progress_callback(prog)
                                except Exception as exc:
                                    logger.warning("Ошибка в progress_callback: %s", exc)

        except (httpx.ConnectTimeout, httpx.ReadTimeout) as exc:
            self._safe_remove(temp_file)
            return DownloadResult(
                status="timeout",
                model_id=request.model_id,
                url=request.url,
                message=f"Превышено время ожидания сети (таймаут): {exc}",
            )
        except (httpx.ConnectError, httpx.HTTPError) as exc:
            self._safe_remove(temp_file)
            return DownloadResult(
                status="network_error",
                model_id=request.model_id,
                url=request.url,
                message=f"Сетевая ошибка при скачивании: {exc}",
            )
        except OSError as exc:
            self._safe_remove(temp_file)
            return DownloadResult(
                status="write_error",
                model_id=request.model_id,
                url=request.url,
                message=f"Ошибка записи на диск: {exc}",
            )
        except Exception as exc:
            self._safe_remove(temp_file)
            return DownloadResult(
                status="error",
                model_id=request.model_id,
                url=request.url,
                message=f"Критическая ошибка загрузки: {exc}",
            )

        # 7. Проверка целостности загруженного файла
        calculated_sha256 = hasher.hexdigest().lower()

        # Валидация размера
        if request.expected_size_bytes and downloaded_bytes != request.expected_size_bytes:
            self._safe_remove(temp_file)
            return DownloadResult(
                status="size_mismatch",
                model_id=request.model_id,
                url=request.url,
                downloaded_bytes=downloaded_bytes,
                expected_size_bytes=request.expected_size_bytes,
                sha256=calculated_sha256,
                message=f"Размер файла ({downloaded_bytes}) не совпадает с ожидаемым ({request.expected_size_bytes}).",
            )

        # Валидация SHA-256 (если присутствовал в манифесте)
        if request.remote_sha256 and calculated_sha256 != request.remote_sha256.lower():
            self._safe_remove(temp_file)
            return DownloadResult(
                status="hash_mismatch",
                model_id=request.model_id,
                url=request.url,
                downloaded_bytes=downloaded_bytes,
                sha256=calculated_sha256,
                message=f"SHA-256 ({calculated_sha256}) не совпадает с официальным хешем ({request.remote_sha256}).",
            )

        # Безопасная проверка: размер не менее 1 МБ
        if downloaded_bytes < 1024 * 1024:
            self._safe_remove(temp_file)
            return DownloadResult(
                status="validation_error",
                model_id=request.model_id,
                url=request.url,
                downloaded_bytes=downloaded_bytes,
                message="Скачанный файл слишком мал (менее 1 МБ) и не является корректной моделью.",
            )

        # 8. Атомарная установка и регистрация в ModelManager (active=False)
        target_dir.mkdir(parents=True, exist_ok=True)
        try:
            temp_file.replace(target_file)
        except Exception as exc:
            self._safe_remove(temp_file)
            return DownloadResult(
                status="write_error",
                model_id=request.model_id,
                url=request.url,
                message=f"Не удалось переместить файл модели в {target_file}: {exc}",
            )

        now_iso = datetime.now(timezone.utc).isoformat()
        remote_artifact_dict = {
            "url": request.url,
            "size_bytes": downloaded_bytes,
            "etag": request.remote_etag,
            "last_modified": request.remote_last_modified,
            "sha256": request.remote_sha256,
            "checked_at": now_iso,
        }

        # Регистрация новой модели с active=False!
        meta_dict = {
            "model_id": request.model_id,
            "filename": target_filename,
            "sha256": calculated_sha256,
            "size": downloaded_bytes,
            "installed_at": now_iso,
            "source": "official_download",
            "active": False,  # НЕ АКТИВИРОВАТЬ АВТОМАТИЧЕСКИ
            "remote_artifact": remote_artifact_dict,
        }

        meta_file = target_dir / "metadata.json"
        meta_temp = target_dir / "metadata.json.tmp"
        try:
            with meta_temp.open("w", encoding="utf-8") as f:
                json.dump(meta_dict, f, indent=2, ensure_ascii=False)
            meta_temp.replace(meta_file)
        except Exception as exc:
            logger.warning("Ошибка записи metadata.json для %s: %s", request.model_id, exc)

        logger.info("Модель %s успешно скачана и зарегистрирована (active=False)", request.model_id)

        return DownloadResult(
            status="success",
            model_id=request.model_id,
            url=request.url,
            installed_path=str(target_file.resolve()),
            downloaded_bytes=downloaded_bytes,
            sha256=calculated_sha256,
            expected_size_bytes=request.expected_size_bytes or downloaded_bytes,
            remote_etag=request.remote_etag,
            remote_last_modified=request.remote_last_modified,
            message="Модель успешно скачана и зарегистрирована (не активирована).",
        )

    def _safe_remove(self, path: Path):
        """Удаление временного файла."""
        if path.exists():
            try:
                path.unlink()
            except Exception as e:
                logger.warning("Не удалось удалить временный файл %s: %s", path, e)
