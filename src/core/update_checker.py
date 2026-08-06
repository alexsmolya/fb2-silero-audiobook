"""
Модуль проверки обновлений официальных моделей Silero TTS (UpdateChecker).

Использует официальный манифест `models.yml` репозитория `snakers4/silero-models` и HTTP HEAD метаданные.
Не выполняет скачивание моделей, замену файлов или автоматическую запись метаданных.
"""

from __future__ import annotations

import argparse
import json
import logging
import re
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import httpx
import yaml

from src.core.model_manager import ModelManager, ModelMetadata

logger = logging.getLogger(__name__)

OFFICIAL_MANIFEST_URL = (
    "https://raw.githubusercontent.com/snakers4/silero-models/master/models.yml"
)
DEFAULT_CONNECT_TIMEOUT = 3.0
DEFAULT_READ_TIMEOUT = 5.0


@dataclass
class RemoteArtifactMetadata:
    """Нормализованные метаданные удалённого артефакта модели."""

    url: Optional[str] = None
    size_bytes: Optional[int] = None
    etag: Optional[str] = None
    etag_is_weak: bool = False
    last_modified: Optional[str] = None
    sha256: Optional[str] = None
    content_md5: Optional[str] = None
    digest: Optional[str] = None
    checked_at: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Преобразовать в словарь."""
        return asdict(self)


@dataclass
class CheckUpdateResult:
    """Результат проверки обновлений модели."""

    status: str
    # Статусы: "up_to_date" | "update_available" | "same_version_remote_changed"
    #          "remote_unavailable" | "manifest_invalid" | "local_model_missing" | "error"

    comparison_confidence: str = "none"  # "high" | "medium" | "low" | "none"
    comparison_basis: List[str] = None  # e.g. ["sha256"], ["strong_etag"], ["last_modified", "content_length"], ["content_length"], ["version_comparison"]

    local_model_id: Optional[str] = None
    local_sha256: Optional[str] = None
    local_size_bytes: Optional[int] = None
    local_installed_at: Optional[str] = None

    remote_model_id: Optional[str] = None
    remote_package_url: Optional[str] = None
    remote_size_bytes: Optional[int] = None
    remote_etag: Optional[str] = None
    remote_etag_is_weak: bool = False
    remote_last_modified: Optional[str] = None
    remote_sha256: Optional[str] = None

    message: str = ""

    def __post_init__(self):
        if self.comparison_basis is None:
            self.comparison_basis = []

    def to_dict(self) -> Dict[str, Any]:
        """Преобразовать в словарь."""
        return asdict(self)


def normalize_etag(etag_str: Optional[str]) -> Tuple[Optional[str], bool]:
    """Нормализовать ETag заголовок и определить weak-признак."""
    if not etag_str or not isinstance(etag_str, str):
        return None, False

    clean_etag = etag_str.strip()
    is_weak = False

    if clean_etag.startswith("W/") or clean_etag.startswith("w/"):
        is_weak = True
        clean_etag = clean_etag[2:].strip()

    if clean_etag.startswith('"') and clean_etag.endswith('"') and len(clean_etag) >= 2:
        clean_etag = clean_etag[1:-1]

    return (clean_etag if clean_etag else None), is_weak


def normalize_sha256(sha_str: Optional[str]) -> Optional[str]:
    """Нормализовать SHA-256 строку."""
    if not sha_str or not isinstance(sha_str, str):
        return None
    cleaned = sha_str.strip().lower()
    return cleaned if len(cleaned) == 64 else None


def parse_model_version(model_id: str) -> Tuple[int, int]:
    """Извлечь кортеж (major, minor) версии из ID модели (например v5_5_ru -> (5, 5))."""
    match = re.search(r"v(\d+)(?:_(\d+))?", model_id, re.IGNORECASE)
    if match:
        major = int(match.group(1))
        minor = int(match.group(2)) if match.group(2) else 0
        return (major, minor)
    return (0, 0)


def evaluate_artifact_comparison(
    local_meta: ModelMetadata,
    remote_artifact: RemoteArtifactMetadata,
    remote_model_id: str,
) -> CheckUpdateResult:
    """Явная бизнес-логика сопоставления локальной модели и удалённого артефакта.

    Использует многоуровневую политику доверия:
      Уровень 1: Криптографический хеш (SHA-256)
      Уровень 2: Сильный ETag (strong ETag)
      Уровень 3: Last-Modified + Content-Length
      Уровень 4: Только Content-Length (low confidence)
    """
    local_version = parse_model_version(local_meta.model_id)
    remote_version = parse_model_version(remote_model_id)

    local_installed_date = (
        local_meta.installed_at.split("T")[0]
        if local_meta.installed_at
        else "неизвестно"
    )

    base_result_kwargs = dict(
        local_model_id=local_meta.model_id,
        local_sha256=local_meta.sha256,
        local_size_bytes=local_meta.size_bytes,
        local_installed_at=local_installed_date,
        remote_model_id=remote_model_id,
        remote_package_url=remote_artifact.url,
        remote_size_bytes=remote_artifact.size_bytes,
        remote_etag=remote_artifact.etag,
        remote_etag_is_weak=remote_artifact.etag_is_weak,
        remote_last_modified=remote_artifact.last_modified,
        remote_sha256=remote_artifact.sha256,
    )

    # 1. Сравнение номеров версий
    if remote_version > local_version:
        return CheckUpdateResult(
            status="update_available",
            comparison_confidence="high",
            comparison_basis=["version_comparison"],
            message=f"Доступна новая официальная модель: {remote_model_id}.",
            **base_result_kwargs,
        )

    # Изучаем историю привязанного удалённого снимка в локальных метаданных
    stored_remote = local_meta.remote_artifact or {}
    stored_etag, stored_weak = normalize_etag(stored_remote.get("etag"))
    stored_last_mod = stored_remote.get("last_modified")

    # 2. Уровень 1: Криптографический хеш SHA-256 (если доступен в манифесте)
    norm_local_sha = normalize_sha256(local_meta.sha256)
    norm_remote_sha = normalize_sha256(remote_artifact.sha256)

    if norm_local_sha and norm_remote_sha:
        if norm_local_sha != norm_remote_sha:
            return CheckUpdateResult(
                status="same_version_remote_changed",
                comparison_confidence="high",
                comparison_basis=["sha256"],
                message=f"Файл модели {remote_model_id} изменён (SHA-256 не совпадает).",
                **base_result_kwargs,
            )
        return CheckUpdateResult(
            status="up_to_date",
            comparison_confidence="high",
            comparison_basis=["sha256"],
            message="Обновлений не обнаружено (SHA-256 совпадает).",
            **base_result_kwargs,
        )

    # 3. Уровень 2: Strong ETag (если есть сохранённый ETag и удалённый ETag не weak)
    if stored_etag and remote_artifact.etag and not remote_artifact.etag_is_weak:
        if remote_artifact.etag != stored_etag:
            return CheckUpdateResult(
                status="same_version_remote_changed",
                comparison_confidence="high",
                comparison_basis=["strong_etag"],
                message=f"Файл модели {remote_model_id} изменён на сервере (изменился ETag).",
                **base_result_kwargs,
            )
        return CheckUpdateResult(
            status="up_to_date",
            comparison_confidence="high",
            comparison_basis=["strong_etag"],
            message="Обновлений не обнаружено (strong ETag совпадает).",
            **base_result_kwargs,
        )

    # 4. Уровень 3: Last-Modified + Content-Length (если есть сохранённый снимковый Last-Modified)
    if stored_last_mod and remote_artifact.last_modified:
        size_changed = (
            remote_artifact.size_bytes is not None
            and local_meta.size_bytes is not None
            and remote_artifact.size_bytes != local_meta.size_bytes
        )
        time_changed = remote_artifact.last_modified != stored_last_mod

        if time_changed or size_changed:
            return CheckUpdateResult(
                status="same_version_remote_changed",
                comparison_confidence="medium",
                comparison_basis=["last_modified", "content_length"],
                message=f"Файл модели {remote_model_id} на сервере изменён (дата/размер изменились).",
                **base_result_kwargs,
            )
        return CheckUpdateResult(
            status="up_to_date",
            comparison_confidence="medium",
            comparison_basis=["last_modified", "content_length"],
            message="Обновлений не обнаружено (дата Last-Modified и размер совпадают).",
            **base_result_kwargs,
        )

    # 5. Уровень 4: Только Content-Length
    if remote_artifact.size_bytes is not None and local_meta.size_bytes is not None:
        if remote_artifact.size_bytes != local_meta.size_bytes:
            return CheckUpdateResult(
                status="same_version_remote_changed",
                comparison_confidence="medium",
                comparison_basis=["content_length"],
                message=f"Файл модели {remote_model_id} на сервере изменён (размер отличается: локально {local_meta.size_bytes}, на сервере {remote_artifact.size_bytes}).",
                **base_result_kwargs,
            )
        # Размер совпадает, но исходной базовой точки ETag/Last-Modified в старых метаданных не сохранялось
        return CheckUpdateResult(
            status="up_to_date",
            comparison_confidence="low",
            comparison_basis=["content_length"],
            message="Новая версия не обнаружена, но идентичность файла нельзя доказать на 100% (совпадает только размер).",
            **base_result_kwargs,
        )

    # 6. Метаданных сервера недостаточно
    return CheckUpdateResult(
        status="up_to_date",
        comparison_confidence="none",
        comparison_basis=["none"],
        message="Официальный сервер не предоставляет метаданных для оценки изменений файла.",
        **base_result_kwargs,
    )


class UpdateChecker:
    """Класс проверки наличия обновлений официальных моделей Silero."""

    def __init__(
        self,
        model_manager: Optional[ModelManager] = None,
        manifest_url: str = OFFICIAL_MANIFEST_URL,
        connect_timeout: float = DEFAULT_CONNECT_TIMEOUT,
        read_timeout: float = DEFAULT_READ_TIMEOUT,
    ):
        self.model_manager = model_manager or ModelManager()
        self.manifest_url = manifest_url
        self.connect_timeout = connect_timeout
        self.read_timeout = read_timeout

    def _get_httpx_timeout(self) -> httpx.Timeout:
        """Сформировать объект таймаутов httpx."""
        return httpx.Timeout(
            connect=self.connect_timeout,
            read=self.read_timeout,
            write=self.read_timeout,
            pool=self.read_timeout,
        )

    def check_for_updates(self) -> CheckUpdateResult:
        """Выполнить проверку наличия обновлений.

        Не проводит запись/изменение metadata.json.
        Не выбрасывает сырые сетевые исключения наружу.
        """
        # 1. Запрос метаданных локальной активной модели
        local_meta = self.model_manager.get_active_model()
        if not local_meta or not local_meta.valid:
            return CheckUpdateResult(
                status="local_model_missing",
                comparison_confidence="none",
                message="Локальная активная модель не найдена или недействительна.",
            )

        local_installed_date = (
            local_meta.installed_at.split("T")[0]
            if local_meta.installed_at
            else "неизвестно"
        )

        # 2. Получение официального манифеста models.yml (с 1 ретраем при сбое сети)
        manifest_text = None
        last_error = None

        for attempt in (1, 2):
            try:
                with httpx.Client(timeout=self._get_httpx_timeout(), follow_redirects=True) as client:
                    response = client.get(self.manifest_url)
                    if response.status_code == 200:
                        manifest_text = response.text
                        break
                    else:
                        last_error = f"HTTP {response.status_code}"
                        break  # HTTP 404/500 не повторить
            except (httpx.ConnectTimeout, httpx.ReadTimeout, httpx.ConnectError) as exc:
                last_error = str(exc)
                if attempt == 1:
                    logger.debug("Повторная попытка запроса манифеста после ошибки: %s", exc)
                    continue
            except Exception as exc:
                last_error = str(exc)
                break

        if manifest_text is None:
            return CheckUpdateResult(
                status="remote_unavailable",
                comparison_confidence="none",
                local_model_id=local_meta.model_id,
                local_sha256=local_meta.sha256,
                local_size_bytes=local_meta.size_bytes,
                local_installed_at=local_installed_date,
                message=f"Официальный источник недоступен: {last_error or 'ошибка соединения'}",
            )

        # 3. Парсинг YAML манифеста
        try:
            manifest_data = yaml.safe_load(manifest_text)
            if not isinstance(manifest_data, dict):
                raise ValueError("Манифест не является JSON/YAML словарем")

            tts_ru = manifest_data.get("tts_models", {}).get("ru", {})
            if not isinstance(tts_ru, dict) or not tts_ru:
                raise ValueError("В манифесте отсутствует секция tts_models.ru")
        except Exception as exc:
            logger.warning("Ошибка разбора манифеста: %s", exc)
            return CheckUpdateResult(
                status="manifest_invalid",
                comparison_confidence="none",
                local_model_id=local_meta.model_id,
                local_sha256=local_meta.sha256,
                local_size_bytes=local_meta.size_bytes,
                local_installed_at=local_installed_date,
                message=f"Не удалось разобрать официальный манифест: {exc}",
            )

        # 4. Выбор наиболее актуальной официальной русской модели
        ru_candidates = []
        for model_key, model_info in tts_ru.items():
            if isinstance(model_info, dict) and (model_key.endswith("_ru") or "ru" in model_key or "latest" in model_info):
                v_tuple = parse_model_version(model_key)
                ru_candidates.append((v_tuple, model_key, model_info))

        if not ru_candidates:
            return CheckUpdateResult(
                status="manifest_invalid",
                comparison_confidence="none",
                local_model_id=local_meta.model_id,
                local_sha256=local_meta.sha256,
                local_size_bytes=local_meta.size_bytes,
                local_installed_at=local_installed_date,
                message="В официальном манифесте не найдено подходящих моделей.",
            )

        ru_candidates.sort(key=lambda item: item[0], reverse=True)
        _, remote_model_id, remote_info = ru_candidates[0]

        latest_data = remote_info.get("latest", {})
        if isinstance(latest_data, dict):
            remote_package_url = latest_data.get("package")
            remote_manifest_sha = normalize_sha256(latest_data.get("sha256"))
        else:
            remote_package_url = None
            remote_manifest_sha = None

        # 5. Запрос HTTP HEAD к серверу пакета для получения заголовков
        remote_artifact = self._fetch_remote_artifact_metadata(
            url=remote_package_url,
            manifest_sha256=remote_manifest_sha,
        )

        # 6. Запуск политики сравнения
        return evaluate_artifact_comparison(
            local_meta=local_meta,
            remote_artifact=remote_artifact,
            remote_model_id=remote_model_id,
        )

    def _fetch_remote_artifact_metadata(
        self,
        url: Optional[str],
        manifest_sha256: Optional[str] = None,
    ) -> RemoteArtifactMetadata:
        """Запрос HTTP HEAD для получения метаданных удалённого артефакта."""
        artifact = RemoteArtifactMetadata(
            url=url,
            sha256=manifest_sha256,
            checked_at=datetime.now(timezone.utc).isoformat(),
        )

        if not url:
            return artifact

        for attempt in (1, 2):
            try:
                with httpx.Client(timeout=self._get_httpx_timeout(), follow_redirects=True) as client:
                    res = client.head(url)
                    if res.status_code == 200:
                        raw_len = res.headers.get("Content-Length")
                        if raw_len:
                            try:
                                artifact.size_bytes = int(raw_len)
                            except ValueError:
                                logger.debug("Поврежденное значение Content-Length: %s", raw_len)

                        clean_etag, is_weak = normalize_etag(res.headers.get("ETag"))
                        artifact.etag = clean_etag
                        artifact.etag_is_weak = is_weak
                        artifact.last_modified = res.headers.get("Last-Modified")
                        artifact.content_md5 = res.headers.get("Content-MD5")
                        artifact.digest = res.headers.get("Digest")
                        break
            except (httpx.ConnectTimeout, httpx.ReadTimeout, httpx.ConnectError) as exc:
                if attempt == 1:
                    logger.debug("Повторный HEAD запрос к %s после ошибки: %s", url, exc)
                    continue
            except Exception as exc:
                logger.debug("HEAD запрос к %s не удался: %s", url, exc)
                break

        return artifact


def format_update_check_result(res: CheckUpdateResult) -> str:
    """Форматирование результата проверки обновлений в соответствии со спецификацией."""
    lines = []

    # 1. Секция локальной модели
    lines.append("Локальная модель")
    lines.append("")
    lines.append(res.local_model_id or "Отсутствует")
    if res.local_sha256:
        lines.append("")
        lines.append("SHA256:")
        lines.append(res.local_sha256)
    if res.local_installed_at:
        lines.append("")
        lines.append("Установлена:")
        lines.append(res.local_installed_at)

    lines.append("")
    lines.append("----------------")
    lines.append("")

    # 2. Секция официальной модели
    lines.append("Официальная модель")
    lines.append("")
    if res.status == "remote_unavailable":
        lines.append("Официальный источник недоступен.")
        return "\n".join(lines)

    lines.append(res.remote_model_id or "Неизвестно")

    lines.append("")
    lines.append("Результат")
    lines.append("")

    if res.status == "up_to_date":
        lines.append(res.message)
        lines.append("")
        lines.append("Основание:")
        if "content_length" in res.comparison_basis:
            lines.append("Совпадает только размер файла (Content-Length).")
        elif "strong_etag" in res.comparison_basis:
            lines.append("Совпадает ETag файла.")
        elif "sha256" in res.comparison_basis:
            lines.append("Совпадает SHA-256 хеш.")
        elif "last_modified" in res.comparison_basis:
            lines.append("Совпадают размер и дата Last-Modified.")
        else:
            lines.append("Версия соответствует официальной.")

        lines.append("")
        lines.append("Уровень уверенности:")
        if res.comparison_confidence == "high":
            lines.append("Высокий (подтверждено хешем/ETag).")
        elif res.comparison_confidence == "medium":
            lines.append("Средний (подтверждено датой и размером).")
        elif res.comparison_confidence == "low":
            lines.append("Низкий (локально отсутствует сохраняемый ETag/Last-Modified снимка).")
        else:
            lines.append("Не определен.")

    elif res.status == "update_available":
        lines.append("Доступна новая модель.")
    elif res.status == "same_version_remote_changed":
        lines.append("Версия имеет прежнее имя, но удалённый файл изменён.")
        lines.append("")
        lines.append("Основание:")
        if "sha256" in res.comparison_basis:
            lines.append("Изменился SHA-256 хеш.")
        elif "strong_etag" in res.comparison_basis:
            lines.append("Изменился ETag.")
        elif "last_modified" in res.comparison_basis:
            lines.append("Изменились дата Last-Modified или размер.")
        else:
            lines.append("Изменился размер файла.")
        lines.append("")
        lines.append("Рекомендуется проверить новую редакцию модели.")
    elif res.status == "local_model_missing":
        lines.append("Локальная модель отсутствует.")
    elif res.status == "manifest_invalid":
        lines.append(f"Ошибка манифеста: {res.message}")
    else:
        lines.append(res.message)

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Проверка наличия обновлений официальных моделей Silero TTS"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Вывод результатов в формате JSON",
    )
    args, unknown = parser.parse_known_args()
    is_json = args.json or ("--json" in sys.argv)

    checker = UpdateChecker()
    res = checker.check_for_updates()

    if is_json:
        print(json.dumps(res.to_dict(), indent=2, ensure_ascii=False))
    else:
        print(format_update_check_result(res))

    if res.status in ("remote_unavailable", "manifest_invalid", "error"):
        sys.exit(1)


if __name__ == "__main__":
    main()
