"""
Модуль инспекции локальных моделей Silero TTS.

Предоставляет функции для обнаружения файлов моделей Silero на диске,
извлечения метаданных (размер, SHA-256, дата изменения) и безопасной обработки
случаев, когда модель отсутствует.
"""

from __future__ import annotations

import hashlib
import logging
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

DEFAULT_SILERO_MODEL_ID = "v5_5_ru"


@dataclass
class ModelInfo:
    """Метаданные локальной модели TTS."""

    exists: bool
    model_id: str
    filename: Optional[str] = None
    path: Optional[str] = None
    size_bytes: Optional[int] = None
    size_formatted: Optional[str] = None
    sha256: Optional[str] = None
    modified: Optional[str] = None
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Преобразовать инспекцию в словарь."""
        return asdict(self)


def _format_size(size_bytes: int) -> str:
    """Форматирование размера файла в читаемый вид."""
    mb = size_bytes / (1024 * 1024)
    return f"{size_bytes:,} bytes ({mb:.1f} MB)"


def _calculate_sha256(file_path: Path, chunk_size: int = 65536) -> str:
    """Вычисление SHA-256 хеша файла по блокам."""
    sha256_hash = hashlib.sha256()
    with file_path.open("rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest().lower()


def find_silero_model_path(
    model_id: str = DEFAULT_SILERO_MODEL_ID,
    language: str = "ru",
) -> Optional[Path]:
    """Программно определить путь к файлу модели Silero TTS.

    Поиск выполняется по логическим каталогам (пользовательское хранилище ModelManager,
    установленный silero-tts, torch hub cache) без жестко завязанных путей.
    """
    # 0. Проверяем активную модель в пользовательском хранилище ModelManager
    try:
        from src.core.model_manager import ModelManager

        mm = ModelManager()
        user_models = mm.list_local_models(include_legacy=False)
        for m in user_models:
            if m.model_id == model_id and m.active and m.valid and m.path:
                p = Path(m.path)
                if p.is_file():
                    return p.resolve()
    except Exception as e:
        logger.debug("Не удалось получить активную модель из ModelManager: %s", e)

    candidates: list[Path] = []

    # 1. Пакет silero_tts (silero_models/)
    try:
        import silero_tts

        pkg_dirs: list[Path] = []
        if hasattr(silero_tts, "__path__"):
            for p in silero_tts.__path__:
                pkg_dirs.append(Path(p))
        if getattr(silero_tts, "__file__", None):
            pkg_dirs.append(Path(silero_tts.__file__).parent)

        try:
            import silero_tts.silero_tts as stts

            if getattr(stts, "__file__", None):
                pkg_dirs.append(Path(stts.__file__).parent)
        except ImportError:
            pass

        for pkg_dir in pkg_dirs:
            pkg_models_dir = pkg_dir / "silero_models"
            if pkg_models_dir.exists():
                candidates.extend(
                    [
                        pkg_models_dir / f"{model_id}_{language}.pt",
                        pkg_models_dir / f"{model_id}.pt",
                    ]
                )
                for p in pkg_models_dir.glob("*.pt"):
                    if model_id in p.name and p not in candidates:
                        candidates.append(p)
    except Exception as e:
        logger.debug("Не удалось получить путь пакета silero_tts: %s", e)

    # 2. Кэш torch hub (~/.cache/torch/hub/ или TORCH_HOME)
    try:
        import os

        torch_home = os.environ.get("TORCH_HOME")
        if torch_home:
            torch_cache = Path(torch_home) / "hub" / "checkpoints"
        else:
            torch_cache = Path.home() / ".cache" / "torch" / "hub" / "checkpoints"

        if torch_cache.exists():
            candidates.extend(
                [
                    torch_cache / f"{model_id}_{language}.pt",
                    torch_cache / f"{model_id}.pt",
                ]
            )
            for p in torch_cache.glob("*.pt"):
                if model_id in p.name and p not in candidates:
                    candidates.append(p)
    except Exception as e:
        logger.debug("Не удалось проверить torch cache: %s", e)

    # Проверяем существование кандидатов
    for path in candidates:
        if path.is_file():
            return path.resolve()

    return None


def get_silero_model_info(
    model_id: str = DEFAULT_SILERO_MODEL_ID,
    language: str = "ru",
) -> ModelInfo:
    """Получить подробные метаданные локальной модели Silero.

    Возвращает объект ModelInfo. В случае отсутствия модели возвращает
    структуру с exists=False и описанием ошибки без генерации исключений.
    """
    try:
        model_path = find_silero_model_path(model_id=model_id, language=language)
        if not model_path or not model_path.is_file():
            return ModelInfo(
                exists=False,
                model_id=model_id,
                error=f"Модель Silero '{model_id}' не найдена локально.",
            )

        stat = model_path.stat()
        size_bytes = stat.st_size
        size_formatted = _format_size(size_bytes)
        sha256_hex = _calculate_sha256(model_path)

        mtime = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc)
        modified_iso = mtime.isoformat()

        return ModelInfo(
            exists=True,
            model_id=model_id,
            filename=model_path.name,
            path=str(model_path),
            size_bytes=size_bytes,
            size_formatted=size_formatted,
            sha256=sha256_hex,
            modified=modified_iso,
        )
    except Exception as exc:
        logger.warning("Ошибка при получении метаданных модели %s: %s", model_id, exc)
        return ModelInfo(
            exists=False,
            model_id=model_id,
            error=f"Ошибка инспекции модели: {exc}",
        )
