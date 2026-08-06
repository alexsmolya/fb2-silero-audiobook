"""
Модуль безопасной миграции локальных моделей Silero TTS (ModelMigrator).

Выполняет перенос моделей из устаревшего расположения (.venv) в пользовательское
хранилище ~/.local/share/fb2-silero-audiobook/models/ с проверкой целостности (SHA-256),
атомарной записью метаданных и гарантией сохранности исходного файла.
"""

from __future__ import annotations

import json
import logging
import os
import shutil
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

from src.core.model_inspector import _calculate_sha256, _format_size
from src.core.model_manager import ModelManager, ModelMetadata

logger = logging.getLogger(__name__)


@dataclass
class MigrationResult:
    """Результат выполнения операции миграции."""

    success: bool
    status: str  # "success" | "already_migrated" | "target_conflict" | "source_missing" | "disk_full" | "sha256_mismatch" | "size_mismatch" | "error"
    source_path: Optional[str] = None
    target_path: Optional[str] = None
    size_bytes: Optional[int] = None
    size_formatted: Optional[str] = None
    sha256: Optional[str] = None
    message: str = ""
    dry_run: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Преобразовать результат в словарь."""
        return asdict(self)


class ModelMigrator:
    """Класс безаварийной миграции моделей Silero TTS."""

    def __init__(self, model_manager: Optional[ModelManager] = None):
        self.model_manager = model_manager or ModelManager()

    def migrate_legacy_model(
        self,
        model_id: str = "v5_5_ru",
        dry_run: bool = False,
    ) -> MigrationResult:
        """Перенести legacy-модель в пользовательское хранилище.

        Параметры:
            model_id: Идентификатор модели (по умолчанию v5_5_ru)
            dry_run: Если True, выполнять только проверку без физического копирования
        """
        # 1. Поиск legacy-модели
        legacy_models = self.model_manager.detect_legacy_models()
        target_legacy = next(
            (m for m in legacy_models if m.model_id == model_id and m.valid),
            None,
        )

        if not target_legacy or not target_legacy.path:
            return MigrationResult(
                success=False,
                status="source_missing",
                message=f"Legacy-модель '{model_id}' не найдена в устаревшем расположении (.venv).",
                dry_run=dry_run,
            )

        source_file = Path(target_legacy.path)
        if not source_file.is_file():
            return MigrationResult(
                success=False,
                status="source_missing",
                message=f"Исходный файл legacy-модели не существует по пути {source_file}.",
                dry_run=dry_run,
            )

        filename = target_legacy.filename or source_file.name
        source_size = target_legacy.size_bytes if target_legacy.size_bytes is not None else source_file.stat().st_size
        source_sha256 = target_legacy.sha256 or _calculate_sha256(source_file)

        # 2. Определение целевых путей
        models_dir = self.model_manager.get_models_dir()
        target_dir = models_dir / model_id
        target_file = target_dir / filename
        metadata_file = target_dir / "metadata.json"

        # 3. Идемпотентность: Проверка уже существующего целевого файла
        if target_file.is_file():
            stat = target_file.stat()
            target_size = stat.st_size
            target_sha256 = _calculate_sha256(target_file)

            if target_size == source_size and target_sha256 == source_sha256:
                # Файл уже скопирован корректно. Проверяем/восстанавливаем metadata.json
                if not metadata_file.is_file():
                    self._write_metadata(
                        target_dir=target_dir,
                        metadata_file=metadata_file,
                        model_id=model_id,
                        filename=target_file.name,
                        sha256=source_sha256,
                        size_bytes=source_size,
                        source_path=str(source_file.resolve()),
                    )
                # Помечаем модель активной
                self._set_active_model(model_id)

                return MigrationResult(
                    success=True,
                    status="already_migrated",
                    source_path=str(source_file.resolve()),
                    target_path=str(target_file.resolve()),
                    size_bytes=source_size,
                    size_formatted=_format_size(source_size),
                    sha256=source_sha256,
                    message="Модель уже мигрирована в пользовательское хранилище и активна.",
                    dry_run=dry_run,
                )
            else:
                return MigrationResult(
                    success=False,
                    status="target_conflict",
                    source_path=str(source_file.resolve()),
                    target_path=str(target_file.resolve()),
                    size_bytes=target_size,
                    sha256=target_sha256,
                    message=f"Целевой файл {target_file} уже существует, но отличается по размеру или SHA-256.",
                    dry_run=dry_run,
                )

        # 4. Проверка свободного места (если доступно)
        try:
            total, used, free = shutil.disk_usage(models_dir.parent if models_dir.exists() else models_dir.parent.parent)
            required_space = source_size + 10 * 1024 * 1024  # размер + 10 МБ буфер
            if free < required_space:
                return MigrationResult(
                    success=False,
                    status="disk_full",
                    source_path=str(source_file.resolve()),
                    target_path=str(target_file.resolve()),
                    size_bytes=source_size,
                    sha256=source_sha256,
                    message=f"Недостаточно свободного места на диске ({_format_size(free)} свободно, требуется {_format_size(required_space)}).",
                    dry_run=dry_run,
                )
        except Exception as exc:
            logger.debug("Не удалось проверить свободное место: %s", exc)

        # 5. Если dry-run — завершаем с описанием действий
        if dry_run:
            return MigrationResult(
                success=True,
                status="ready",
                source_path=str(source_file.resolve()),
                target_path=str(target_file.resolve()),
                size_bytes=source_size,
                size_formatted=_format_size(source_size),
                sha256=source_sha256,
                message="Модель готова к миграции. Физическое копирование будет выполнено при запуске без --dry-run.",
                dry_run=True,
            )

        # 6. Физическая миграция
        target_dir.mkdir(parents=True, exist_ok=True)
        temp_file = target_dir / f"{filename}.tmp"

        if temp_file.exists():
            try:
                temp_file.unlink()
            except Exception as e:
                logger.warning("Не удалось удалить старый временный файл %s: %s", temp_file, e)

        try:
            # Поблочное копирование
            logger.info("Миграция: копирование %s -> %s ...", source_file, temp_file)
            with source_file.open("rb") as src, temp_file.open("wb") as dst:
                while chunk := src.read(65536):
                    dst.write(chunk)

            # Проверка размера и SHA-256 временного файла
            copied_size = temp_file.stat().st_size
            if copied_size != source_size:
                self._safe_remove(temp_file)
                return MigrationResult(
                    success=False,
                    status="size_mismatch",
                    source_path=str(source_file.resolve()),
                    target_path=str(target_file.resolve()),
                    message=f"Ошибка миграции: размер скопированного файла ({copied_size}) не совпадает с исходным ({source_size}).",
                )

            copied_sha256 = _calculate_sha256(temp_file)
            if copied_sha256.lower() != source_sha256.lower():
                self._safe_remove(temp_file)
                return MigrationResult(
                    success=False,
                    status="sha256_mismatch",
                    source_path=str(source_file.resolve()),
                    target_path=str(target_file.resolve()),
                    message=f"Ошибка миграции: SHA-256 не совпадает (исходный: {source_sha256}, скопированный: {copied_sha256}).",
                )

            # Атомарное переименование файла модели
            temp_file.replace(target_file)

            # Атомарная запись metadata.json
            self._write_metadata(
                target_dir=target_dir,
                metadata_file=metadata_file,
                model_id=model_id,
                filename=target_file.name,
                sha256=source_sha256,
                size_bytes=source_size,
                source_path=str(source_file.resolve()),
            )

            # Назначаем модель активной
            self._set_active_model(model_id)

            logger.info("Миграция модели %s успешно завершена.", model_id)
            return MigrationResult(
                success=True,
                status="success",
                source_path=str(source_file.resolve()),
                target_path=str(target_file.resolve()),
                size_bytes=source_size,
                size_formatted=_format_size(source_size),
                sha256=source_sha256,
                message="Миграция модели успешно завершена. Исходный файл в .venv сохранён.",
            )

        except Exception as exc:
            logger.error("Критическая ошибка при миграции модели: %s", exc, exc_info=True)
            self._safe_remove(temp_file)
            return MigrationResult(
                success=False,
                status="error",
                source_path=str(source_file.resolve()),
                target_path=str(target_file.resolve()),
                message=f"Ошибка в процессе миграции: {exc}",
            )

    def _safe_remove(self, path: Path):
        """Безопасное удаление временного файла."""
        if path.exists():
            try:
                path.unlink()
            except Exception as e:
                logger.warning("Не удалось удалить временный файл %s: %s", path, e)

    def _write_metadata(
        self,
        target_dir: Path,
        metadata_file: Path,
        model_id: str,
        filename: str,
        sha256: str,
        size_bytes: int,
        source_path: str,
    ):
        """Запись метаданных с использованием временного файла."""
        now_iso = datetime.now(timezone.utc).isoformat()
        meta_data = {
            "model_id": model_id,
            "filename": filename,
            "sha256": sha256,
            "size": size_bytes,
            "installed_at": now_iso,
            "source": "legacy_migration",
            "source_path": source_path,
            "active": True,
        }

        meta_temp = target_dir / "metadata.json.tmp"
        with meta_temp.open("w", encoding="utf-8") as f:
            json.dump(meta_data, f, indent=2, ensure_ascii=False)
        meta_temp.replace(metadata_file)

    def _set_active_model(self, active_model_id: str):
        """Отметить указанную модель как активную в метаданных всех пользовательских моделей."""
        models_dir = self.model_manager.get_models_dir()
        if not models_dir.exists():
            return

        for child in models_dir.iterdir():
            if child.is_dir():
                meta_file = child / "metadata.json"
                if meta_file.is_file():
                    try:
                        with meta_file.open("r", encoding="utf-8") as f:
                            data = json.load(f)
                        if isinstance(data, dict):
                            is_target = child.name == active_model_id
                            if data.get("active") != is_target:
                                data["active"] = is_target
                                tmp_meta = child / "metadata.json.tmp"
                                with tmp_meta.open("w", encoding="utf-8") as f:
                                    json.dump(data, f, indent=2, ensure_ascii=False)
                                tmp_meta.replace(meta_file)
                    except Exception as e:
                        logger.warning("Не удалось обновить статус active в %s: %s", meta_file, e)
