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

from src.core.model_inspector import _format_size
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

    # Subcommand: download
    parser_download = subparsers.add_parser("download", help="Загрузка новой официальной модели Silero TTS")
    parser_download.add_argument("--dry-run", action="store_true", help="Режим проверки плана загрузки без скачивания файла")
    parser_download.add_argument("--yes", action="store_true", help="Подтверждение реального скачивания файла")
    parser_download.add_argument("--force", action="store_true", help="Принудительное скачивание, даже если локальная модель актуальна")
    parser_download.add_argument("--json", action="store_true", help="Вывод в JSON")

    args, unknown = parser.parse_known_args()

    # Проверяем флаги --json, --dry-run, --yes, --force
    is_json = args.json or ("--json" in sys.argv)
    is_dry_run = getattr(args, "dry_run", False) or ("--dry-run" in sys.argv)
    is_yes = getattr(args, "yes", False) or ("--yes" in sys.argv)
    is_force = getattr(args, "force", False) or ("--force" in sys.argv)

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

    elif cmd == "download":
        from src.core.download_manager import DownloadManager, DownloadRequest, DownloadResult
        from src.core.update_checker import UpdateChecker

        checker = UpdateChecker(model_manager=mm)
        update_res = checker.check_for_updates()

        if update_res.status == "up_to_date" and not is_force:
            res = DownloadResult(
                status="no_update_available",
                model_id=update_res.local_model_id,
                url=update_res.remote_package_url,
                message="Обновлений не обнаружено. Локальная модель актуальна.",
                dry_run=is_dry_run,
            )
            if is_json:
                print(json.dumps(res.to_dict(), indent=2, ensure_ascii=False))
            else:
                print("План скачивания модели Silero:")
                print("----------------------------")
                print(f"Текущая модель: {update_res.local_model_id}")
                print("Результат: Обновлений не обнаружено. Скачивание не требуется.")
            return

        if not update_res.remote_model_id or not update_res.remote_package_url:
            res = DownloadResult(
                status="manifest_error",
                message=f"Не удалось определить параметры скачивания ({update_res.message}).",
                dry_run=is_dry_run,
            )
            if is_json:
                print(json.dumps(res.to_dict(), indent=2, ensure_ascii=False))
            else:
                print(f"Ошибка: {res.message}")
            sys.exit(1)

        req = DownloadRequest(
            model_id=update_res.remote_model_id,
            url=update_res.remote_package_url,
            expected_size_bytes=update_res.remote_size_bytes,
            remote_etag=update_res.remote_etag,
            remote_last_modified=update_res.remote_last_modified,
            remote_sha256=update_res.remote_sha256,
        )

        dl_manager = DownloadManager(model_manager=mm)

        if is_dry_run or not is_yes:
            res = dl_manager.download_model(req, dry_run=True)
            if is_json:
                print(json.dumps(res.to_dict(), indent=2, ensure_ascii=False))
            else:
                print("План скачивания модели Silero (Dry Run):")
                print("---------------------------------------")
                print(f"Локальная модель:      {update_res.local_model_id}")
                print(f"Удалённая модель:      {req.model_id}")
                print(f"URL источника:         {req.url}")
                print(f"Ожидаемый размер:      {_format_size(req.expected_size_bytes) if req.expected_size_bytes else 'неизвестно'}")
                print(f"Целевой путь:          {res.installed_path}")
                print(f"Автоматическая активация: НЕТ (active=False)")
                print("")
                if not is_yes and not is_dry_run:
                    print("Для выполнения реального скачивания передайте флаг --yes.")
        else:
            res = dl_manager.download_model(req, dry_run=False)
            if is_json:
                print(json.dumps(res.to_dict(), indent=2, ensure_ascii=False))
            else:
                print(f"Результат скачивания модели {req.model_id}:")
                print(f"Статус:      {res.status.upper()}")
                print(f"Путь:        {res.installed_path or 'N/A'}")
                print(f"Сообщение:   {res.message}")

            if res.status not in ("success", "already_downloaded"):
                sys.exit(1)


if __name__ == "__main__":
    main()
