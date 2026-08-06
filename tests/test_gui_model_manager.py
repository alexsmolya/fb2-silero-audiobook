"""Unit-тесты GUI-логики подсистемы управления моделями Silero TTS.

Проверяет controller/view-model без зависимости от открытого X11-дисплея.
Все 20 требуемых сценариев покрываются полностью с использованием моков.
"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.core.download_manager import DownloadProgress, DownloadRequest, DownloadResult
from src.core.model_manager import ModelManager, ModelMetadata
from src.core.model_migrator import MigrationResult, ModelMigrator
from src.core.model_switcher import ModelSwitcher, SmokeTestResult, SpeakerTestResult, SwitchResult
from src.core.update_checker import CheckUpdateResult, UpdateChecker
from src.gui.model_manager_controller import ActiveModelSummary, ModelManagerController


@pytest.fixture
def mock_mm(tmp_path: Path) -> MagicMock:
    mm = MagicMock(spec=ModelManager)
    info = ModelMetadata(
        model_id="v5_5_ru",
        filename="v5_5_ru_ru.pt",
        path=str(tmp_path / "v5_5_ru" / "v5_5_ru_ru.pt"),
        size_bytes=145420684,
        modified="2026-08-06T18:00:00",
        active=True,
        valid=True,
        sha256="50081637b602126ee06cb3bc8a744d25651d2da149ee8864b9a379bfdd934437",
        source="legacy_migration",
    )
    mm.get_active_model.return_value = info
    mm.list_local_models.return_value = [info]
    return mm


@pytest.fixture
def controller(mock_mm: MagicMock) -> ModelManagerController:
    uc = MagicMock(spec=UpdateChecker)
    dm = MagicMock()
    ms = MagicMock(spec=ModelSwitcher)
    mig = MagicMock(spec=ModelMigrator)
    ctrl = ModelManagerController(
        model_manager=mock_mm,
        update_checker=uc,
        download_manager=dm,
        model_switcher=ms,
        model_migrator=mig,
    )
    return ctrl


def test_1_active_model_summary(controller: ModelManagerController):
    """1. Отображение активной модели."""
    sum_info = controller.get_active_model_summary(current_voice="xenia")
    assert sum_info is not None
    assert sum_info.model_id == "v5_5_ru"
    assert sum_info.filename == "v5_5_ru_ru.pt"
    assert "138.7" in sum_info.size_str
    assert sum_info.short_sha256 == "50081637b602…"


def test_2_xenia_as_current_voice(controller: ModelManagerController):
    """2. Отображение xenia как текущего голоса."""
    sum_info = controller.get_active_model_summary(current_voice="xenia")
    assert sum_info is not None
    assert sum_info.current_voice == "xenia"


def test_3_update_check_success(controller: ModelManagerController):
    """3. Update check success (высокая уверенность)."""
    uc_res = CheckUpdateResult(
        status="up_to_date",
        local_model_id="v5_5_ru",
        remote_model_id="v5_5_ru",
        comparison_confidence="high",
        message="Модели совпадают по SHA256",
    )
    controller.update_checker.check_for_updates.return_value = uc_res

    res_box = []
    cb = lambda r: res_box.append(r)

    ok = controller.check_updates(on_success=cb, on_error=lambda e: None)
    assert ok is True

    if controller._active_worker:
        controller._active_worker.join(timeout=2.0)

    assert len(res_box) == 1
    assert res_box[0].status == "up_to_date"
    assert res_box[0].comparison_confidence == "high"


def test_4_update_check_low_confidence(controller: ModelManagerController):
    """4. Update check low confidence."""
    uc_res = CheckUpdateResult(
        status="up_to_date",
        local_model_id="v5_5_ru",
        remote_model_id="v5_5_ru",
        comparison_confidence="low",
        message="Идентичность подтверждена только по размеру",
    )
    controller.update_checker.check_for_updates.return_value = uc_res

    res_box = []
    controller.check_updates(on_success=lambda r: res_box.append(r), on_error=lambda e: None)
    if controller._active_worker:
        controller._active_worker.join(timeout=2.0)

    assert res_box[0].comparison_confidence == "low"


def test_5_update_available(controller: ModelManagerController):
    """5. Update available."""
    uc_res = CheckUpdateResult(
        status="update_available",
        local_model_id="v5_5_ru",
        remote_model_id="v5_6_ru",
        comparison_confidence="high",
        remote_size_bytes=145420684,
        message="Доступна новая версия v5_6_ru",
    )
    controller.update_checker.check_for_updates.return_value = uc_res

    res_box = []
    controller.check_updates(on_success=lambda r: res_box.append(r), on_error=lambda e: None)
    if controller._active_worker:
        controller._active_worker.join(timeout=2.0)

    assert res_box[0].status == "update_available"
    assert res_box[0].remote_model_id == "v5_6_ru"


def test_6_network_error(controller: ModelManagerController):
    """6. Network error при проверке обновлений."""
    controller.update_checker.check_for_updates.side_effect = OSError("Connection refused")

    err_box = []
    controller.check_updates(on_success=lambda r: None, on_error=lambda e: err_box.append(e))
    if controller._active_worker:
        controller._active_worker.join(timeout=2.0)

    assert len(err_box) == 1
    assert "Не удалось проверить обновления" in err_box[0]


def test_7_download_progress(controller: ModelManagerController):
    """7. Прогресс скачивания."""
    def fake_download(req, progress_callback=None):
        if progress_callback:
            progress_callback(DownloadProgress(downloaded_bytes=500, total_bytes=1000, percent=50.0))
        return DownloadResult(status="success", model_id=req.model_id, installed_path="/tmp/model.pt")

    controller.download_manager.download_model.side_effect = fake_download

    prog_box = []
    comp_box = []

    controller.download_model(
        model_id="v5_6_ru",
        on_progress=lambda p: prog_box.append(p),
        on_complete=lambda s, m: comp_box.append((s, m)),
    )
    if controller._active_worker:
        controller._active_worker.join(timeout=2.0)

    assert len(prog_box) == 1
    assert prog_box[0].percent == 50.0
    assert comp_box[0][0] is True


def test_8_cancel_download(controller: ModelManagerController):
    """8. Отмена скачивания."""
    controller.cancel_download()
    assert controller._cancel_requested is True


def test_9_downloaded_model_remains_inactive(controller: ModelManagerController):
    """9. Скачанная модель остаётся inactive."""
    controller.download_manager.download_model.return_value = DownloadResult(
        status="success", model_id="v5_6_ru", installed_path="/tmp/v5_6_ru.pt"
    )

    comp_box = []
    controller.download_model("v5_6_ru", on_progress=lambda p: None, on_complete=lambda s, m: comp_box.append((s, m)))
    if controller._active_worker:
        controller._active_worker.join(timeout=2.0)

    assert "ещё не активирована" in comp_box[0][1]


def test_10_smoke_test_both_voices(controller: ModelManagerController):
    """10. Smoke-test обоих голосов (eugene и xenia)."""
    sm_res = SmokeTestResult(
        success=True,
        status="success",
        model_id="v5_5_ru",
        available_speakers=["eugene", "xenia"],
        tested_speakers=["eugene", "xenia"],
        missing_required_speakers=[],
        failed_speakers=[],
        speaker_results={
            "eugene": SpeakerTestResult(speaker="eugene", status="success"),
            "xenia": SpeakerTestResult(speaker="xenia", status="success"),
        },
    )
    controller.model_switcher.run_smoke_test.return_value = sm_res

    res_box = []
    controller.run_smoke_test("v5_5_ru", all_speakers=False, on_complete=lambda r: res_box.append(r))
    if controller._active_worker:
        controller._active_worker.join(timeout=2.0)

    assert res_box[0].success is True
    assert "eugene" in res_box[0].speaker_results
    assert "xenia" in res_box[0].speaker_results


def test_11_missing_xenia_blocks_activation(controller: ModelManagerController):
    """11. Отсутствие xenia блокирует активацию."""
    sw_res = SwitchResult(
        success=False,
        status="voice_missing",
        model_id="v5_6_ru",
        message="Голос xenia отсутствует",
    )
    controller.model_switcher.activate_model.return_value = sw_res

    comp_box = []
    controller.activate_model("v5_6_ru", current_voice="xenia", on_complete=lambda s, m: comp_box.append((s, m)))
    if controller._active_worker:
        controller._active_worker.join(timeout=2.0)

    assert comp_box[0][0] is False
    assert "голос 'xenia' отсутствует" in comp_box[0][1]


def test_12_selected_xenia_passed_to_model_switcher(controller: ModelManagerController):
    """12. Выбранный xenia передаётся в ModelSwitcher."""
    controller.model_switcher.activate_model.return_value = SwitchResult(
        success=True, status="success", model_id="v5_6_ru"
    )

    controller.activate_model("v5_6_ru", current_voice="xenia", on_complete=lambda s, m: None)
    if controller._active_worker:
        controller._active_worker.join(timeout=2.0)

    controller.model_switcher.activate_model.assert_called_once_with(
        model_id="v5_6_ru", voice="xenia", force=False
    )


def test_13_successful_activation(controller: ModelManagerController):
    """13. Успешная активация."""
    controller.model_switcher.activate_model.return_value = SwitchResult(
        success=True, status="success", model_id="v5_6_ru"
    )

    comp_box = []
    controller.activate_model("v5_6_ru", current_voice="xenia", on_complete=lambda s, m: comp_box.append((s, m)))
    if controller._active_worker:
        controller._active_worker.join(timeout=2.0)

    assert comp_box[0][0] is True
    assert "успешно активирована" in comp_box[0][1]


def test_14_rollback(controller: ModelManagerController):
    """14. Rollback к предыдущей модели."""
    controller.model_switcher.rollback_active_model.return_value = SwitchResult(
        success=True, status="success", model_id="v5_5_ru"
    )

    comp_box = []
    controller.rollback_model(on_complete=lambda s, m: comp_box.append((s, m)))
    if controller._active_worker:
        controller._active_worker.join(timeout=2.0)

    assert comp_box[0][0] is True
    assert "восстановлена: v5_5_ru" in comp_box[0][1]


def test_15_dialog_closed_during_callback(controller: ModelManagerController):
    """15. Закрытие диалога во время callback (безопасный вызов)."""
    executed = []

    def buggy_dispatcher(cb):
        raise RuntimeError("Widget destroyed!")

    controller.set_ui_dispatcher(buggy_dispatcher)
    controller._dispatch_ui(lambda: executed.append(1))
    assert executed == []


def test_16_buttons_disabled_during_operation(controller: ModelManagerController):
    """16. Кнопки блокируются во время операции (is_busy = True)."""
    controller.is_busy = True
    assert controller.check_updates(on_success=lambda r: None, on_error=lambda e: None) is False
    assert controller.download_model("v5_6_ru", on_progress=lambda p: None, on_complete=lambda s, m: None) is False
    assert controller.run_smoke_test("v5_5_ru", all_speakers=False, on_complete=lambda r: None) is False
    assert controller.activate_model("v5_6_ru", current_voice="xenia", on_complete=lambda s, m: None) is False


def test_17_repeat_click_does_not_start_second_operation(controller: ModelManagerController):
    """17. Повторное нажатие не запускает вторую операцию."""
    controller.is_busy = True
    assert controller.rollback_model(on_complete=lambda s, m: None) is False
    assert controller.migrate_legacy_model(on_complete=lambda s, m: None) is False


def test_18_corrupted_state_does_not_break_gui(mock_mm: MagicMock):
    """18. Повреждённый state.json не ломает основной GUI."""
    mock_mm.get_active_model.side_effect = Exception("Corrupted state.json")
    ctrl = ModelManagerController(model_manager=mock_mm)

    summary = ctrl.get_active_model_summary()
    assert summary is None


def test_19_legacy_migration_not_triggered_automatically(controller: ModelManagerController):
    """19. Legacy migration не запускается автоматически."""
    controller.model_migrator.migrate_legacy_model.assert_not_called()


def test_20_exceptions_converted_to_user_messages(controller: ModelManagerController):
    """20. Исключения преобразуются в пользовательские сообщения."""
    controller.model_switcher.activate_model.side_effect = RuntimeError("Disk IO error")

    comp_box = []
    controller.activate_model("v5_6_ru", current_voice="xenia", on_complete=lambda s, m: comp_box.append((s, m)))
    if controller._active_worker:
        controller._active_worker.join(timeout=2.0)

    assert comp_box[0][0] is False
    assert "Не удалось активировать модель: Disk IO error" in comp_box[0][1]
