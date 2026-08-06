#!/usr/bin/env python3
"""
CLI для инспекции и вывода информации о локальной модели Silero TTS.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Добавляем корень проекта в sys.path для корректных импортов
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.core.model_inspector import DEFAULT_SILERO_MODEL_ID, get_silero_model_info


def format_text_output(info) -> str:
    """Форматирование метаданных в текстовый вид."""
    lines = [
        "Silero model",
        "",
        f"ID: {info.model_id}",
    ]
    if info.exists:
        lines.extend(
            [
                f"Filename: {info.filename or ''}",
                f"Size: {info.size_formatted or info.size_bytes or ''}",
                f"SHA256: {info.sha256 or ''}",
                f"Modified: {info.modified or ''}",
                f"Path: {info.path or ''}",
            ]
        )
    else:
        lines.extend(
            [
                "Status: Not found",
                f"Error: {info.error or 'Model file not found'}",
            ]
        )
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Информация о локальной модели Silero TTS"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Вывод в формате JSON",
    )
    parser.add_argument(
        "--model-id",
        default=DEFAULT_SILERO_MODEL_ID,
        help="Идентификатор модели (по умолчанию: v5_5_ru)",
    )

    args, unknown = parser.parse_known_args()
    info = get_silero_model_info(model_id=args.model_id)

    if args.json:
        print(json.dumps(info.to_dict(), indent=2, ensure_ascii=False))
    else:
        print(format_text_output(info))

    if not info.exists:
        sys.exit(1)


if __name__ == "__main__":
    main()
