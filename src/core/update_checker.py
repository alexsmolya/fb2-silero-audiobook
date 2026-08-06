"""
Модуль проверки обновлений официальных моделей Silero TTS (UpdateChecker).

Использует официальный манифест `models.yml` репозитория `snakers4/silero-models`.
Не выполняет скачивание моделей, обновление файлов или изменение метаданных.
"""

from __future__ import annotations

import argparse
import json
import logging
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import httpx
import yaml

from src.core.model_manager import ModelManager

logger = logging.getLogger(__name__)

OFFICIAL_MANIFEST_URL = (
    "https://raw.githubusercontent.com/snakers4/silero-models/master/models.yml"
)
DEFAULT_TIMEOUT = 10.0  # Секунды


@dataclass
class CheckUpdateResult:
    """Результат проверки обновлений модели."""

    status: str
    # Статусы: "up_to_date" | "update_available" | "same_version_remote_changed"
    #          "remote_unavailable" | "manifest_invalid" | "local_model_missing" | "error"

    local_model_id: Optional[str] = None
    local_sha256: Optional[str] = None
    local_size_bytes: Optional[int] = None
    local_installed_at: Optional[str] = None

    remote_model_id: Optional[str] = None
    remote_package_url: Optional[str] = None
    remote_size_bytes: Optional[int] = None
    remote_etag: Optional[str] = None
    remote_last_modified: Optional[str] = None

    message: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Преобразовать в словарь."""
        return asdict(self)


def parse_model_version(model_id: str) -> Tuple[int, int]:
    """Извлечь кортеж (major, minor) версии из ID модели (например v5_5_ru -> (5, 5))."""
    match = re.search(r"v(\d+)(?:_(\d+))?", model_id, re.IGNORECASE)
    if match:
        major = int(match.group(1))
        minor = int(match.group(2)) if match.group(2) else 0
        return (major, minor)
    return (0, 0)


class UpdateChecker:
    """Класс проверки наличия обновлений официальных моделей Silero."""

    def __init__(
        self,
        model_manager: Optional[ModelManager] = None,
        manifest_url: str = OFFICIAL_MANIFEST_URL,
        timeout: float = DEFAULT_TIMEOUT,
    ):
        self.model_manager = model_manager or ModelManager()
        self.manifest_url = manifest_url
        self.timeout = timeout

    def check_for_updates(self) -> CheckUpdateResult:
        """Выполнить проверку наличия обновлений.

        Возвращает объект CheckUpdateResult с результатами сравнения.
        Никогда не выбрасывает сетевые исключения наружу.
        """
        # 1. Запрос метаданных локальной активной модели
        local_meta = self.model_manager.get_active_model()
        if not local_meta or not local_meta.valid:
            return CheckUpdateResult(
                status="local_model_missing",
                message="Локальная активная модель не найдена или недействительна.",
            )

        local_installed_date = (
            local_meta.installed_at.split("T")[0]
            if local_meta.installed_at
            else "неизвестно"
        )

        # 2. Получение официального манифеста models.yml
        try:
            with httpx.Client(timeout=self.timeout, follow_redirects=True) as client:
                response = client.get(self.manifest_url)
                if response.status_code != 200:
                    return CheckUpdateResult(
                        status="remote_unavailable",
                        local_model_id=local_meta.model_id,
                        local_sha256=local_meta.sha256,
                        local_size_bytes=local_meta.size_bytes,
                        local_installed_at=local_installed_date,
                        message=f"Официальный манифест недоступен (HTTP {response.status_code}).",
                    )
                manifest_text = response.text
        except Exception as exc:
            logger.warning("Не удалось получить манифест с %s: %s", self.manifest_url, exc)
            return CheckUpdateResult(
                status="remote_unavailable",
                local_model_id=local_meta.model_id,
                local_sha256=local_meta.sha256,
                local_size_bytes=local_meta.size_bytes,
                local_installed_at=local_installed_date,
                message=f"Официальный источник недоступен: {exc}",
            )

        # 3. Парсинг YAML структуры манифеста
        try:
            manifest_data = yaml.safe_load(manifest_text)
            if not isinstance(manifest_data, dict):
                raise ValueError("Манифест не является словарь-объектом")

            tts_ru = manifest_data.get("tts_models", {}).get("ru", {})
            if not isinstance(tts_ru, dict) or not tts_ru:
                raise ValueError("В манифесте отсутствует секция tts_models.ru")
        except Exception as exc:
            logger.warning("Ошибка разбора манифеста: %s", exc)
            return CheckUpdateResult(
                status="manifest_invalid",
                local_model_id=local_meta.model_id,
                local_sha256=local_meta.sha256,
                local_size_bytes=local_meta.size_bytes,
                local_installed_at=local_installed_date,
                message=f"Не удалось разобрать официальный манифест: {exc}",
            )

        # 4. Поиск наиболее актуальной официальной русской модели
        ru_candidates = []
        for model_key, model_info in tts_ru.items():
            if not isinstance(model_info, dict):
                continue
            # Ищем модели для русской речи (ключи оканчиваются на _ru или русские модели)
            if model_key.endswith("_ru") or "ru" in model_key:
                v_tuple = parse_model_version(model_key)
                ru_candidates.append((v_tuple, model_key, model_info))

        if not ru_candidates:
            # Выбираем ключи, имеющие секцию latest с package url
            for model_key, model_info in tts_ru.items():
                if isinstance(model_info, dict) and "latest" in model_info:
                    v_tuple = parse_model_version(model_key)
                    ru_candidates.append((v_tuple, model_key, model_info))

        if not ru_candidates:
            return CheckUpdateResult(
                status="manifest_invalid",
                local_model_id=local_meta.model_id,
                local_sha256=local_meta.sha256,
                local_size_bytes=local_meta.size_bytes,
                local_installed_at=local_installed_date,
                message="В официальном манифесте не найдено подходящих моделей.",
            )

        # Сортируем кандидатов по номеру версии
        ru_candidates.sort(key=lambda item: item[0], reverse=True)
        _, remote_model_id, remote_info = ru_candidates[0]

        latest_data = remote_info.get("latest", {})
        if isinstance(latest_data, dict):
            remote_package_url = latest_data.get("package")
        else:
            remote_package_url = None

        local_version = parse_model_version(local_meta.model_id)
        remote_version = parse_model_version(remote_model_id)

        # 5. Сравнение локальной и удаленной версий
        if remote_version > local_version:
            # Доступна более новая версия
            remote_size = None
            if remote_package_url:
                remote_size = self._fetch_remote_file_size(remote_package_url)

            return CheckUpdateResult(
                status="update_available",
                local_model_id=local_meta.model_id,
                local_sha256=local_meta.sha256,
                local_size_bytes=local_meta.size_bytes,
                local_installed_at=local_installed_date,
                remote_model_id=remote_model_id,
                remote_package_url=remote_package_url,
                remote_size_bytes=remote_size,
                message=f"Доступна новая официальная модель: {remote_model_id}.",
            )

        # 6. Версии совпадают (например v5_5_ru == v5_5_ru). Проверяем изменение удаленного файла
        remote_size = None
        remote_etag = None
        remote_last_modified = None

        if remote_package_url:
            head_info = self._fetch_remote_head_info(remote_package_url)
            remote_size = head_info.get("size")
            remote_etag = head_info.get("etag")
            remote_last_modified = head_info.get("last_modified")

        if remote_size is not None and local_meta.size_bytes is not None:
            if remote_size != local_meta.size_bytes:
                return CheckUpdateResult(
                    status="same_version_remote_changed",
                    local_model_id=local_meta.model_id,
                    local_sha256=local_meta.sha256,
                    local_size_bytes=local_meta.size_bytes,
                    local_installed_at=local_installed_date,
                    remote_model_id=remote_model_id,
                    remote_package_url=remote_package_url,
                    remote_size_bytes=remote_size,
                    remote_etag=remote_etag,
                    remote_last_modified=remote_last_modified,
                    message=f"Файл модели {remote_model_id} на сервере изменён.",
                )

        return CheckUpdateResult(
            status="up_to_date",
            local_model_id=local_meta.model_id,
            local_sha256=local_meta.sha256,
            local_size_bytes=local_meta.size_bytes,
            local_installed_at=local_installed_date,
            remote_model_id=remote_model_id,
            remote_package_url=remote_package_url,
            remote_size_bytes=remote_size or local_meta.size_bytes,
            remote_etag=remote_etag,
            remote_last_modified=remote_last_modified,
            message="Обновлений не обнаружено.",
        )

    def _fetch_remote_head_info(self, url: str) -> Dict[str, Any]:
        """Получить размер, ETag и Last-Modified через HTTP HEAD запрос."""
        info: Dict[str, Any] = {}
        try:
            with httpx.Client(timeout=self.timeout, follow_redirects=True) as client:
                res = client.head(url)
                if res.status_code == 200:
                    if "Content-Length" in res.headers:
                        try:
                            info["size"] = int(res.headers["Content-Length"])
                        except ValueError:
                            pass
                    if "ETag" in res.headers:
                        info["etag"] = res.headers["ETag"].strip('"')
                    if "Last-Modified" in res.headers:
                        info["last_modified"] = res.headers["Last-Modified"]
        except Exception as exc:
            logger.debug("HEAD запрос к %s не удался: %s", url, exc)
        return info

    def _fetch_remote_file_size(self, url: str) -> Optional[int]:
        """Получить размер удаленного файла."""
        return self._fetch_remote_head_info(url).get("size")


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
        lines.append("Обновлений не обнаружено.")
    elif res.status == "update_available":
        lines.append("Доступна новая модель.")
    elif res.status == "same_version_remote_changed":
        lines.append("Файл модели изменён.")
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
        description="Проверка наличии обновлений официальных моделей Silero TTS"
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
