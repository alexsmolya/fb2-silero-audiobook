#!/usr/bin/env python3
"""
CLI для управления, просмотра и миграции локальных моделей Silero TTS (ModelManager & ModelMigrator).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Добавляем корень проекта в sys.path
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.core.model_manager import ModelManager, ModelMetadata
from src.core.model_migrator import MigrationResult, ModelMigrator


def format_model_entry(m: ModelMetadata) -> str:
    """Форматирование метаданных единичной модели в текстовый вид."""
    status_tag = "[Active] " if m.active else "         "
    lines = [
        f"{status_tag}ID: {m.model_id}",
        f"  Source: {m.source}{' (legacy storage)' if m.is_legacy else ''}",
        f"  Filename: {m.filename or 'N/A'}",
        f"  Size: {m.size_formatted or m.size_bytes or 'N/A'}",
        f"  SHA256: {m.sha256 or 'N/A'}",
        f"  Modified: {m.modified or 'N/A'}",
        f"  Path: {m.path or 'N/A'}",
    ]
    if m.error:
        lines.append(f"  Note: {m.error}")
    return "\n".join(lines)


def format_models_list(models: list[ModelMetadata]) -> str:
    """Форматирование списка моделей в текстовый вид."""
    if not models:
        return "No local models found."

    header = f"Local Silero Models ({len(models)} found):\n"
    entries = [format_model_entry(m) for m in models]
    return header + "\n\n".join(entries)


def format_migration_result(res: MigrationResult) -> str:
    """Форматирование результата миграции в текстовый вид."""
    mode_str = " (Dry Run)" if res.dry_run else ""
    lines = [
        f"Silero Model Migration{mode_str}:",
        "",
        f"Status: {res.status.upper() if res.success else 'FAILED (' + res.status + ')'}",
        f"Source path: {res.source_path or 'N/A'}",
        f"Target path: {res.target_path or 'N/A'}",
        f"Size: {res.size_formatted or res.size_bytes or 'N/A'}",
        f"SHA256: {res.sha256 or 'N/A'}",
        f"Message: {res.message}",
    ]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Управление и просмотр локальных моделей Silero TTS"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Вывод результатов в формате JSON",
    )
    subparsers = parser.add_subparsers(dest="subcommand", help="Команды")

    # Subcommand: list
    parser_list = subparsers.add_parser("list", help="Показать все локальные модели")
    parser_list.add_argument("--json", action="store_true", help="Вывод в JSON")

    # Subcommand: active
    parser_active = subparsers.add_parser("active", help="Показать активную модель")
    parser_active.add_argument("--json", action="store_true", help="Вывод в JSON")

    # Subcommand: info
    parser_info = subparsers.add_parser("info", help="Показать информацию о конкретной модели")
    parser_info.add_argument("model_id", help="Идентификатор модели (напр. v5_5_ru)")
    parser_info.add_argument("--json", action="store_true", help="Вывод в JSON")

    # Subcommand: migrate
    parser_migrate = subparsers.add_parser("migrate", help="Миграция legacy-модели из .venv в пользовательское хранилище")
    parser_migrate.add_argument("--dry-run", action="store_true", help="Режим проверки без копирования файлов")
    parser_migrate.add_argument("--model-id", default="v5_5_ru", help="Идентификатор модели (по умолчанию v5_5_ru)")
    parser_migrate.add_argument("--json", action="store_true", help="Вывод в JSON")

    args, unknown = parser.parse_known_args()

    # Проверяем флаги --json и --dry-run
    is_json = args.json or ("--json" in sys.argv)
    is_dry_run = getattr(args, "dry_run", False) or ("--dry-run" in sys.argv)

    mm = ModelManager()
    cmd = args.subcommand or "list"

    if cmd == "list":
        models = mm.list_local_models(include_legacy=True)
        if is_json:
            print(json.dumps([m.to_dict() for m in models], indent=2, ensure_ascii=False))
        else:
            print(format_models_list(models))

    elif cmd == "active":
        active_model = mm.get_active_model()
        if is_json:
            print(
                json.dumps(
                    active_model.to_dict() if active_model else None,
                    indent=2,
                    ensure_ascii=False,
                )
            )
        else:
            if active_model:
                print("Active Silero Model:\n")
                print(format_model_entry(active_model))
            else:
                print("No active Silero model found.")
                sys.exit(1)

    elif cmd == "info":
        model_id = getattr(args, "model_id", None)
        if not model_id:
            print("Error: model_id required for info command", file=sys.stderr)
            sys.exit(1)
        info = mm.get_model_info(model_id)
        if is_json:
            print(
                json.dumps(
                    info.to_dict() if info else None,
                    indent=2,
                    ensure_ascii=False,
                )
            )
        else:
            if info:
                print(f"Model Info ({model_id}):\n")
                print(format_model_entry(info))
            else:
                print(f"Model '{model_id}' not found.")
                sys.exit(1)

    elif cmd == "migrate":
        model_id = getattr(args, "model_id", "v5_5_ru")
        migrator = ModelMigrator(model_manager=mm)
        result = migrator.migrate_legacy_model(model_id=model_id, dry_run=is_dry_run)

        if is_json:
            print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
        else:
            print(format_migration_result(result))

        if not result.success:
            sys.exit(1)


if __name__ == "__main__":
    main()
