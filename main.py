#!/usr/bin/env python3
"""
Точка входа в приложение Audiobook Generator.
Десктопное приложение для озвучки FB2-книг с AI-комментариями.
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

# Добавляем src в путь для импорта
sys.path.insert(0, str(Path(__file__).parent))

from src.config.settings import load_settings, save_settings
from src.utils.logger import setup_logging
from src.ui.app import AudiobookApp


def main():
    """Главная функция запуска приложения."""
    if len(sys.argv) > 1 and sys.argv[1] in ("model-info", "--model-info"):
        from tools.model_info import main as model_info_main

        sys.argv.pop(1)
        model_info_main()
        return

    if len(sys.argv) > 1 and sys.argv[1] in ("models", "model-manager", "--models"):
        from tools.model_manager import main as model_manager_main

        sys.argv.pop(1)
        model_manager_main()
        return

    # Настройка логирования
    log_dir = Path.home() / ".audiobook-generator"
    log_file = log_dir / "audiobook-generator.log"
    setup_logging(log_file=log_file, level=logging.INFO)

    logger = logging.getLogger(__name__)
    logger.info("=" * 60)
    logger.info("Audiobook Generator v0.1.0")
    logger.info("=" * 60)

    # Загрузка настроек
    settings = load_settings()

    # Если первый запуск, помечаем что он был
    if settings.first_run:
        logger.info("Первый запуск приложения")
        settings.first_run = False
        save_settings(settings)

    # Запуск GUI
    try:
        app = AudiobookApp(settings)
        app.run()
    except Exception as e:
        logger.critical("Критическая ошибка: %s", e, exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
