"""
Модель управления локальным хранилищем моделей Silero TTS (ModelManager).

Отделяет хранение локальных моделей от пакетов виртуального окружения (.venv),
предоставляя функции поиска, учета, чтения метаданных и управления несколькими
моделями одновременно.
"""

from __future__ import annotations

import json
import logging
import os
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.core.model_inspector import (
    DEFAULT_SILERO_MODEL_ID,
    _calculate_sha256,
    _format_size,
    find_silero_model_path,
)

logger = logging.getLogger(__name__)


def get_default_models_dir() -> Path:
    """Получить системный каталог пользовательского хранения моделей."""
    xdg_data = os.environ.get("XDG_DATA_HOME")
    if xdg_data:
        base_dir = Path(xdg_data)
    else:
        base_dir = Path.home() / ".local" / "share"

    return base_dir / "fb2-silero-audiobook" / "models"


@dataclass
class ModelMetadata:
    """Метаданные модели TTS."""

    model_id: str
    filename: Optional[str] = None
    path: Optional[str] = None
    size_bytes: Optional[int] = None
    size_formatted: Optional[str] = None
    sha256: Optional[str] = None
    modified: Optional[str] = None
    installed_at: Optional[str] = None
    source: str = "user_models"  # "user_models" | "legacy_venv" | "unknown"
    active: bool = False
    is_legacy: bool = False
    valid: bool = True
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Преобразовать в словарь."""
        return asdict(self)


class ModelManager:
    """Менеджер для управления локальным хранилищем моделей."""

    def __init__(self, models_dir: Optional[Path] = None):
        self.models_dir = models_dir or get_default_models_dir()

    def get_models_dir(self) -> Path:
        """Получить рабочий каталог моделей (создается при необходимости)."""
        self.models_dir.mkdir(parents=True, exist_ok=True)
        return self.models_dir

    def _read_metadata_file(self, metadata_path: Path) -> Optional[Dict[str, Any]]:
        """Безопасное чтение metadata.json."""
        if not metadata_path.is_file():
            return None
        try:
            with metadata_path.open("r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    return data
                logger.warning("Файл %s не содержит JSON-объект", metadata_path)
                return None
        except Exception as exc:
            logger.warning("Ошибка чтения метаданных из %s: %s", metadata_path, exc)
            return None

    def _inspect_model_dir(self, model_dir: Path) -> ModelMetadata:
        """Инспекция отдельной папки модели в хранилище."""
        model_id = model_dir.name
        metadata_file = model_dir / "metadata.json"
        raw_meta = self._read_metadata_file(metadata_file)

        # Ищем файл .pt в директории
        pt_files = list(model_dir.glob("*.pt"))
        pt_file: Optional[Path] = pt_files[0] if pt_files else None

        if raw_meta is None and metadata_file.exists():
            # Метаданные есть, но повреждены
            if pt_file and pt_file.is_file():
                stat = pt_file.stat()
                size_bytes = stat.st_size
                sha256_hex = _calculate_sha256(pt_file)
                mtime = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat()
                return ModelMetadata(
                    model_id=model_id,
                    filename=pt_file.name,
                    path=str(pt_file.resolve()),
                    size_bytes=size_bytes,
                    size_formatted=_format_size(size_bytes),
                    sha256=sha256_hex,
                    modified=mtime,
                    installed_at=mtime,
                    source="user_models",
                    active=False,
                    is_legacy=False,
                    valid=False,
                    error="Файл metadata.json поврежден. Восстановлены базовые данные из файла модели.",
                )
            return ModelMetadata(
                model_id=model_id,
                valid=False,
                error="Файл metadata.json поврежден, а файл модели (.pt) отсутствует.",
            )

        if raw_meta is not None:
            filename = raw_meta.get("filename")
            target_pt = model_dir / filename if filename else pt_file

            if target_pt and target_pt.is_file():
                stat = target_pt.stat()
                size_bytes = raw_meta.get("size", stat.st_size)
                sha256_hex = raw_meta.get("sha256") or _calculate_sha256(target_pt)
                mtime = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat()
                installed_at = raw_meta.get("installed_at", mtime)
                active = bool(raw_meta.get("active", False))

                return ModelMetadata(
                    model_id=raw_meta.get("model_id", model_id),
                    filename=target_pt.name,
                    path=str(target_pt.resolve()),
                    size_bytes=size_bytes,
                    size_formatted=_format_size(size_bytes),
                    sha256=sha256_hex,
                    modified=mtime,
                    installed_at=installed_at,
                    source=raw_meta.get("source", "user_models"),
                    active=active,
                    is_legacy=False,
                    valid=True,
                )
            else:
                return ModelMetadata(
                    model_id=raw_meta.get("model_id", model_id),
                    filename=filename,
                    size_bytes=raw_meta.get("size"),
                    sha256=raw_meta.get("sha256"),
                    installed_at=raw_meta.get("installed_at"),
                    active=bool(raw_meta.get("active", False)),
                    valid=False,
                    error=f"Файл модели '{filename or '*.pt'}' отсутствует в директории.",
                )

        # Если нет metadata.json, но есть .pt
        if pt_file and pt_file.is_file():
            stat = pt_file.stat()
            size_bytes = stat.st_size
            sha256_hex = _calculate_sha256(pt_file)
            mtime = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat()
            return ModelMetadata(
                model_id=model_id,
                filename=pt_file.name,
                path=str(pt_file.resolve()),
                size_bytes=size_bytes,
                size_formatted=_format_size(size_bytes),
                sha256=sha256_hex,
                modified=mtime,
                installed_at=mtime,
                source="user_models",
                active=False,
                is_legacy=False,
                valid=True,
            )

        return ModelMetadata(
            model_id=model_id,
            valid=False,
            error="В папки модели нет файла .pt и метаданных.",
        )

    def detect_legacy_models(self) -> List[ModelMetadata]:
        """Обнаружить модели, находящиеся в устаревшем расположении (.venv)."""
        legacy_models: List[ModelMetadata] = []
        legacy_path = find_silero_model_path(DEFAULT_SILERO_MODEL_ID)

        if legacy_path and legacy_path.is_file():
            # Проверяем, не вынесен ли он уже в пользовательские модели
            stat = legacy_path.stat()
            size_bytes = stat.st_size
            sha256_hex = _calculate_sha256(legacy_path)
            mtime = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat()

            legacy_models.append(
                ModelMetadata(
                    model_id=DEFAULT_SILERO_MODEL_ID,
                    filename=legacy_path.name,
                    path=str(legacy_path.resolve()),
                    size_bytes=size_bytes,
                    size_formatted=_format_size(size_bytes),
                    sha256=sha256_hex,
                    modified=mtime,
                    installed_at=mtime,
                    source="legacy_venv",
                    active=False,
                    is_legacy=True,
                    valid=True,
                    error="Модель находится в устаревшем расположении (.venv). Требуется подготовка к миграции.",
                )
            )

        return legacy_models

    def list_local_models(self, include_legacy: bool = True) -> List[ModelMetadata]:
        """Получить список всех доступных локальных моделей."""
        models: List[ModelMetadata] = []
        user_dir = self.models_dir

        if user_dir.exists() and user_dir.is_dir():
            for child in sorted(user_dir.iterdir()):
                if child.is_dir():
                    models.append(self._inspect_model_dir(child))

        # Если в пользовательском каталоге моделей нет, проверяем legacy
        user_model_ids = {m.model_id for m in models if m.valid}

        if include_legacy:
            for legacy in self.detect_legacy_models():
                if legacy.model_id not in user_model_ids:
                    models.append(legacy)

        # Если ни одна модель не помечена как active, но есть хотя бы одна валидная — первая считается активной
        has_active = any(m.active for m in models if m.valid)
        if not has_active:
            for m in models:
                if m.valid:
                    m.active = True
                    break

        return models

    def get_active_model(self) -> Optional[ModelMetadata]:
        """Получить метаданные активной модели."""
        models = self.list_local_models(include_legacy=True)
        for m in models:
            if m.active and m.valid:
                return m
        return models[0] if models else None

    def get_model_info(self, model_id: str) -> Optional[ModelMetadata]:
        """Получить информацию по конкретному model_id."""
        models = self.list_local_models(include_legacy=True)
        for m in models:
            if m.model_id == model_id:
                return m
        return None

    def create_model_metadata(
        self,
        model_id: str,
        filename: str,
        sha256: str,
        size_bytes: int,
        source: str = "user_models",
        active: bool = False,
    ) -> ModelMetadata:
        """Создать запись метаданных для новой модели в user_models_dir."""
        model_dir = self.get_models_dir() / model_id
        model_dir.mkdir(parents=True, exist_ok=True)

        now_iso = datetime.now(timezone.utc).isoformat()
        meta_dict = {
            "model_id": model_id,
            "filename": filename,
            "sha256": sha256,
            "size": size_bytes,
            "installed_at": now_iso,
            "source": source,
            "active": active,
        }

        metadata_path = model_dir / "metadata.json"
        with metadata_path.open("w", encoding="utf-8") as f:
            json.dump(meta_dict, f, indent=2, ensure_ascii=False)

        return self._inspect_model_dir(model_dir)
