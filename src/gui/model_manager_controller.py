"""Controller (ViewModel) для GUI-интерфейса управления моделями Silero TTS.

Обеспечивает разделение бизнес-логики и Tkinter-виджетов:
- Безопасное управление состояниями операций (busy/idle)
- Выполнение сетевых и тяжелых операций (UpdateChecker, DownloadManager, ModelSwitcher) в фоновых потоках
- Безопасная диспетчеризация сообщений в главный поток GUI
- Проверка доступности обязательных голосов (eugene, xenia) и сохранение выбранного голоса
- Обработка исключений и перевод их в понятные пользователю сообщения
"""

from __future__ import annotations

import logging
import threading
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional

from src.core.download_manager import DownloadManager, DownloadProgress, DownloadRequest, DownloadResult
from src.core.model_manager import ModelManager, ModelMetadata
from src.core.model_migrator import ModelMigrator
from src.core.model_switcher import REQUIRED_RUSSIAN_SPEAKERS, ModelSwitcher, SmokeTestResult, SwitchResult
from src.core.update_checker import CheckUpdateResult, UpdateChecker

logger = logging.getLogger(__name__)


@dataclass
class ActiveModelSummary:
    model_id: str
    filename: str
    size_str: str
    install_date_str: str
    source: str
    short_sha256: str
    full_sha256: str
    path: str
    current_voice: str
    update_status: str


class ModelManagerController:
    """Контроллер подсистемы управления моделями для GUI."""

    def __init__(
        self,
        model_manager: Optional[ModelManager] = None,
        update_checker: Optional[UpdateChecker] = None,
        download_manager: Optional[DownloadManager] = None,
        model_switcher: Optional[ModelSwitcher] = None,
        model_migrator: Optional[ModelMigrator] = None,
    ):
        self.model_manager = model_manager or ModelManager()
        self.update_checker = update_checker or UpdateChecker()
        self.download_manager = download_manager or DownloadManager(model_manager=self.model_manager)
        self.model_switcher = model_switcher or ModelSwitcher(model_manager=self.model_manager)
        self.model_migrator = model_migrator or ModelMigrator(model_manager=self.model_manager)

        self._active_worker: Optional[threading.Thread] = None
        self._cancel_requested = False
        self.is_busy = False
        self.last_update_check: Optional[CheckUpdateResult] = None
        self._ui_dispatcher: Optional[Callable[[Callable[[], None]], None]] = None

    def set_ui_dispatcher(self, dispatcher: Callable[[Callable[[], None]], None]) -> None:
        """Установить функцию безопасного вызова в GUI-потоке (например, root.after)."""
        self._ui_dispatcher = dispatcher

    def _dispatch_ui(self, callback: Callable[[], None]) -> None:
        """Выполнить callback в GUI-потоке, если задан диспетчер."""
        if self._ui_dispatcher:
            try:
                self._ui_dispatcher(callback)
            except Exception as exc:
                logger.warning("Не удалось диспетчеризовать вызов GUI: %s", exc)
        else:
            callback()

    def get_active_model_summary(self, current_voice: str = "xenia") -> Optional[ActiveModelSummary]:
        """Получить сводку об активной модели для отображения в GUI."""
        try:
            active_info = self.model_manager.get_active_model()
            if not active_info or not active_info.path or not active_info.valid:
                return None

            size_mb = (active_info.size_bytes or 0) / (1024 * 1024)
            size_str = f"{size_mb:.1f} MB"
            date_str = active_info.modified[:10] if active_info.modified else "Неизвестно"
            full_sha = active_info.sha256 or ""
            short_sha = f"{full_sha[:12]}…" if len(full_sha) >= 12 else full_sha

            update_status = "Не проверялись"
            if self.last_update_check:
                if self.last_update_check.status == "update_available":
                    update_status = f"Доступно обновление ({self.last_update_check.remote_model_id})"
                else:
                    update_status = "Установлена последняя версия"

            return ActiveModelSummary(
                model_id=active_info.model_id,
                filename=active_info.filename or "—",
                size_str=size_str,
                install_date_str=date_str,
                source=active_info.source or "хранилище",
                short_sha256=short_sha,
                full_sha256=full_sha,
                path=active_info.path or "—",
                current_voice=current_voice,
                update_status=update_status,
            )
        except Exception as exc:
            logger.error("Ошибка получения информации об активной модели: %s", exc)
            return None

    def list_local_models(self) -> List[ModelMetadata]:
        """Получить список локальных моделей."""
        try:
            return self.model_manager.list_local_models()
        except Exception as exc:
            logger.error("Ошибка получения списка моделей: %s", exc)
            return []

    def can_rollback(self) -> bool:
        """Проверить, доступен ли откат к предыдущей модели."""
        try:
            return self.model_switcher.can_rollback()
        except Exception as exc:
            logger.error("Ошибка проверки возможности отката: %s", exc)
            return False

    def is_legacy_available_for_migration(self) -> bool:
        """Проверить, доступна ли legacy-модель в .venv для миграции."""
        try:
            legacies = self.model_migrator.model_manager.detect_legacy_models()
            return len(legacies) > 0
        except Exception as exc:
            logger.error("Ошибка поиска legacy-модели: %s", exc)
            return False

    def check_updates(
        self,
        on_success: Callable[[CheckUpdateResult], None],
        on_error: Callable[[str], None],
    ) -> bool:
        """Запустить неблокирующую проверку обновлений через UpdateChecker."""
        if self.is_busy:
            return False

        self.is_busy = True

        def _worker():
            try:
                res = self.update_checker.check_for_updates()
                self.last_update_check = res

                def _ui():
                    self.is_busy = False
                    on_success(res)

                self._dispatch_ui(_ui)
            except Exception as exc:
                logger.error("Ошибка в фоновой проверке обновлений: %s", exc, exc_info=True)
                msg = "Не удалось проверить обновления. Проверьте подключение к интернету."

                def _ui_err():
                    self.is_busy = False
                    on_error(msg)

                self._dispatch_ui(_ui_err)

        self._active_worker = threading.Thread(target=_worker, daemon=True)
        self._active_worker.start()
        return True

    def download_model(
        self,
        model_id: str,
        on_progress: Callable[[DownloadProgress], None],
        on_complete: Callable[[bool, str], None],
    ) -> bool:
        """Запустить неблокирующее скачивание модели через DownloadManager."""
        if self.is_busy:
            return False

        self.is_busy = True
        self._cancel_requested = False

        url = f"https://models.silero.ai/models/tts/ru/{model_id}.pt"
        expected_size = None
        expected_sha = None

        if self.last_update_check and self.last_update_check.remote_model_id == model_id:
            url = self.last_update_check.remote_package_url or url
            expected_size = self.last_update_check.remote_size_bytes
            expected_sha = self.last_update_check.remote_sha256

        req = DownloadRequest(
            model_id=model_id,
            url=url,
            expected_size_bytes=expected_size,
            remote_sha256=expected_sha,
        )

        def _prog_callback(prog: DownloadProgress):
            if self._cancel_requested:
                raise RuntimeError("Download canceled by user")
            def _ui_p():
                on_progress(prog)
            self._dispatch_ui(_ui_p)

        def _worker():
            try:
                res: DownloadResult = self.download_manager.download_model(
                    req, progress_callback=_prog_callback
                )
                success = res.status in ("success", "already_downloaded")
                if success:
                    msg = f"Модель {model_id} успешно скачана.\n\nОна ещё не активирована."
                elif res.status == "canceled":
                    msg = "Загрузка отменена."
                else:
                    msg = f"Ошибка скачивания: {res.message}"

                def _ui_comp():
                    self.is_busy = False
                    on_complete(success, msg)

                self._dispatch_ui(_ui_comp)
            except Exception as exc:
                logger.error("Ошибка фонового скачивания: %s", exc)
                if "canceled" in str(exc).lower():
                    msg = "Загрузка отменена."
                    success = False
                else:
                    msg = f"Не удалось скачать модель: {exc}"
                    success = False

                def _ui_err():
                    self.is_busy = False
                    on_complete(success, msg)

                self._dispatch_ui(_ui_err)

        self._active_worker = threading.Thread(target=_worker, daemon=True)
        self._active_worker.start()
        return True

    def cancel_download(self) -> None:
        """Запросить отмену текущего скачивания."""
        self._cancel_requested = True

    def run_smoke_test(
        self,
        model_id: str,
        all_speakers: bool,
        on_complete: Callable[[SmokeTestResult], None],
    ) -> bool:
        """Запустить неблокирующий smoke-test модели через ModelSwitcher."""
        if self.is_busy:
            return False

        self.is_busy = True

        def _worker():
            try:
                res = self.model_switcher.run_smoke_test(
                    model_id=model_id, test_all_speakers=all_speakers
                )

                def _ui_comp():
                    self.is_busy = False
                    on_complete(res)

                self._dispatch_ui(_ui_comp)
            except Exception as exc:
                logger.error("Ошибка smoke-test в контроллере: %s", exc)
                err_res = SmokeTestResult(
                    success=False,
                    status="error",
                    model_id=model_id,
                    available_speakers=[],
                    tested_speakers=[],
                    missing_required_speakers=REQUIRED_RUSSIAN_SPEAKERS,
                    failed_speakers=REQUIRED_RUSSIAN_SPEAKERS,
                    speaker_results={},
                    message=f"Ошибка выполнения проверки: {exc}",
                )

                def _ui_err():
                    self.is_busy = False
                    on_complete(err_res)

                self._dispatch_ui(_ui_err)

        self._active_worker = threading.Thread(target=_worker, daemon=True)
        self._active_worker.start()
        return True

    def activate_model(
        self,
        model_id: str,
        current_voice: str,
        on_complete: Callable[[bool, str], None],
    ) -> bool:
        """Запустить неблокирующую активацию модели через ModelSwitcher."""
        if self.is_busy:
            return False

        self.is_busy = True

        def _worker():
            try:
                res: SwitchResult = self.model_switcher.activate_model(
                    model_id=model_id, voice=current_voice, force=False
                )
                success = res.success
                if success:
                    msg = f"Модель {model_id} успешно активирована.\n\nОна будет использована при следующем запуске синтеза."
                else:
                    if res.status == "voice_missing":
                        msg = f"Невозможно активировать модель: голос '{current_voice}' отсутствует в модели {model_id}."
                    else:
                        msg = f"Ошибка активации модели: {res.message}"

                def _ui_comp():
                    self.is_busy = False
                    on_complete(success, msg)

                self._dispatch_ui(_ui_comp)
            except Exception as exc:
                logger.error("Ошибка активации модели: %s", exc)
                msg = f"Не удалось активировать модель: {exc}"

                def _ui_err():
                    self.is_busy = False
                    on_complete(False, msg)

                self._dispatch_ui(_ui_err)

        self._active_worker = threading.Thread(target=_worker, daemon=True)
        self._active_worker.start()
        return True

    def rollback_model(
        self,
        on_complete: Callable[[bool, str], None],
    ) -> bool:
        """Запустить неблокирующий откат к предыдущей модели."""
        if self.is_busy:
            return False

        self.is_busy = True

        def _worker():
            try:
                res: SwitchResult = self.model_switcher.rollback_active_model()
                success = res.success
                if success:
                    msg = f"Активная модель восстановлена: {res.model_id}."
                else:
                    msg = f"Не удалось выполнить откат: {res.message}"

                def _ui_comp():
                    self.is_busy = False
                    on_complete(success, msg)

                self._dispatch_ui(_ui_comp)
            except Exception as exc:
                logger.error("Ошибка отката модели: %s", exc)
                msg = f"Ошибка отката: {exc}"

                def _ui_err():
                    self.is_busy = False
                    on_complete(False, msg)

                self._dispatch_ui(_ui_err)

        self._active_worker = threading.Thread(target=_worker, daemon=True)
        self._active_worker.start()
        return True

    def migrate_legacy_model(
        self,
        on_complete: Callable[[bool, str], None],
    ) -> bool:
        """Запустить неблокирующую миграцию legacy-модели."""
        if self.is_busy:
            return False

        self.is_busy = True

        def _worker():
            try:
                res = self.model_migrator.migrate_legacy_model()
                success = res.success
                if success:
                    msg = "Модель успешно перенесена в постоянное хранилище."
                else:
                    msg = f"Ошибка миграции: {res.message}"

                def _ui_comp():
                    self.is_busy = False
                    on_complete(success, msg)

                self._dispatch_ui(_ui_comp)
            except Exception as exc:
                logger.error("Ошибка миграции: %s", exc)
                msg = f"Не удалось перенести модель: {exc}"

                def _ui_err():
                    self.is_busy = False
                    on_complete(False, msg)

                self._dispatch_ui(_ui_err)

        self._active_worker = threading.Thread(target=_worker, daemon=True)
        self._active_worker.start()
        return True
