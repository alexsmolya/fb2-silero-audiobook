"""Tkinter-диалог "Модели Silero TTS".

Предоставляет интерфейс управления моделями Silero:
- Просмотр активной модели, ее параметров и сокращенного SHA-256
- Просмотр списка локально установленных моделей
- Проверка обновлений
- Скачивание новых моделей с прогресс-баром
- Smoke-test обязательных голосов (eugene, xenia)
- Безопасная активация с подтверждением и поддержкой выбранного голоса
- Откат к предыдущей модели с подтверждением
- Миграция legacy-модели из .venv
"""

from __future__ import annotations

import logging
import tkinter as tk
from tkinter import messagebox, ttk
from typing import Optional

from src.core.download_manager import DownloadProgress
from src.core.model_manager import ModelMetadata
from src.core.model_switcher import SmokeTestResult
from src.core.update_checker import CheckUpdateResult
from src.gui.model_manager_controller import ModelManagerController

logger = logging.getLogger(__name__)


class ModelManagerDialog(tk.Toplevel):
    """Диалоговое окно управления моделями Silero TTS."""

    def __init__(
        self,
        parent: tk.Tk,
        controller: Optional[ModelManagerController] = None,
        current_voice: str = "xenia",
    ):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller or ModelManagerController()
        self.current_voice = current_voice
        self._closed = False

        # Настройка безопасной диспетчеризации вызовов из фоновых потоков
        self.controller.set_ui_dispatcher(self._safe_dispatch)

        self.title("Модели Silero TTS")
        self.geometry("740x580")
        self.minsize(640, 480)
        self.transient(parent)
        self.grab_set()

        self.protocol("WM_DELETE_WINDOW", self._on_close)

        self._create_widgets()
        self._refresh_ui()

    def _safe_dispatch(self, callback) -> None:
        """Безопасный вызов callback в главном потоке GUI через after."""
        if not self._closed and self.winfo_exists():
            try:
                self.after(0, callback)
            except Exception:
                pass

    def _on_close(self) -> None:
        """Безопасное закрытие окна."""
        self._closed = True
        self.grab_release()
        self.destroy()

    def _create_widgets(self) -> None:
        main_frame = ttk.Frame(self, padding=14)
        main_frame.pack(fill="both", expand=True)

        # 1. Сводка по активной модели
        active_frame = ttk.LabelFrame(main_frame, text="Текущая активная модель", padding=10)
        active_frame.pack(fill="x", pady=(0, 10))

        self.lbl_active_id = ttk.Label(active_frame, text="Активная модель: —", font=("Noto Sans", 10, "bold"))
        self.lbl_active_id.grid(row=0, column=0, sticky="w", padx=5, pady=2)

        self.lbl_active_voice = ttk.Label(active_frame, text="Текущий голос: —")
        self.lbl_active_voice.grid(row=0, column=1, sticky="w", padx=15, pady=2)

        self.lbl_active_details = ttk.Label(active_frame, text="Файл: — | Размер: — | Источник: —")
        self.lbl_active_details.grid(row=1, column=0, columnspan=2, sticky="w", padx=5, pady=2)

        sha_frame = ttk.Frame(active_frame)
        sha_frame.grid(row=2, column=0, columnspan=2, sticky="w", padx=5, pady=2)

        self.lbl_active_sha = ttk.Label(sha_frame, text="SHA-256: —")
        self.lbl_active_sha.pack(side="left")

        self.btn_copy_sha = ttk.Button(sha_frame, text="Скопировать SHA-256", command=self._copy_full_sha)
        self.btn_copy_sha.pack(side="left", padx=(10, 0))

        self.lbl_update_status = ttk.Label(active_frame, text="Статус обновлений: не проверялись")
        self.lbl_update_status.grid(row=3, column=0, columnspan=2, sticky="w", padx=5, pady=2)

        # 2. Список локальных моделей
        list_frame = ttk.LabelFrame(main_frame, text="Установленные локальные модели", padding=10)
        list_frame.pack(fill="both", expand=True, pady=(0, 10))

        columns = ("model_id", "status", "size", "date", "source")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", selectmode="browse")
        self.tree.heading("model_id", text="Model ID")
        self.tree.heading("status", text="Статус")
        self.tree.heading("size", text="Размер")
        self.tree.heading("date", text="Дата")
        self.tree.heading("source", text="Источник")

        self.tree.column("model_id", width=120)
        self.tree.column("status", width=110)
        self.tree.column("size", width=90)
        self.tree.column("date", width=100)
        self.tree.column("source", width=140)

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self._on_tree_select)

        # 3. Индикатор скачивания / выполнения
        self.progress_frame = ttk.LabelFrame(main_frame, text="Прогресс операции", padding=8)
        self.lbl_progress_info = ttk.Label(self.progress_frame, text="")
        self.lbl_progress_info.pack(anchor="w")

        self.progress_bar = ttk.Progressbar(self.progress_frame, mode="determinate", maximum=100)
        self.progress_bar.pack(fill="x", pady=4)

        self.btn_cancel_op = ttk.Button(self.progress_frame, text="Отменить", command=self._cancel_download)
        self.btn_cancel_op.pack(anchor="e")

        # 4. Панель кнопок управления
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill="x", pady=(5, 0))

        self.btn_check_updates = ttk.Button(btn_frame, text="Проверить обновления", command=self._check_updates)
        self.btn_check_updates.pack(side="left", padx=(0, 5))

        self.btn_download = ttk.Button(btn_frame, text="Скачать", command=self._download_model, state="disabled")
        self.btn_download.pack(side="left", padx=5)

        self.btn_test = ttk.Button(btn_frame, text="Проверить модель", command=self._smoke_test, state="disabled")
        self.btn_test.pack(side="left", padx=5)

        self.btn_activate = ttk.Button(btn_frame, text="Активировать", command=self._activate_model, state="disabled")
        self.btn_activate.pack(side="left", padx=5)

        self.btn_rollback = ttk.Button(btn_frame, text="Откатить", command=self._rollback_model, state="disabled")
        self.btn_rollback.pack(side="left", padx=5)

        self.btn_migrate = ttk.Button(btn_frame, text="Перенести модель", command=self._migrate_legacy, state="disabled")
        self.btn_migrate.pack(side="left", padx=5)

        self.btn_close = ttk.Button(btn_frame, text="Закрыть", command=self._on_close)
        self.btn_close.pack(side="right")

        self._full_sha256 = ""

    def _refresh_ui(self) -> None:
        """Обновить все данные в графическом интерфейсе."""
        if self._closed:
            return

        summary = self.controller.get_active_model_summary(current_voice=self.current_voice)
        if summary:
            self.lbl_active_id.config(text=f"Активная модель: {summary.model_id}")
            self.lbl_active_voice.config(text=f"Текущий голос: {summary.current_voice}")
            self.lbl_active_details.config(
                text=f"Файл: {summary.filename} | Размер: {summary.size_str} | Источник: {summary.source}"
            )
            self.lbl_active_sha.config(text=f"SHA-256: {summary.short_sha256}")
            self.lbl_update_status.config(text=f"Статус обновлений: {summary.update_status}")
            self._full_sha256 = summary.full_sha256
            self.btn_copy_sha.state(["!disabled"])
        else:
            self.lbl_active_id.config(text="Активная модель: Не найдена")
            self.lbl_active_voice.config(text=f"Текущий голос: {self.current_voice}")
            self.lbl_active_details.config(text="Файл: — | Размер: — | Источник: —")
            self.lbl_active_sha.config(text="SHA-256: —")
            self.btn_copy_sha.state(["disabled"])

        # Обновление таблицы моделей
        for item in self.tree.get_children():
            self.tree.delete(item)

        models = self.controller.list_local_models()
        for info in models:
            size_mb = (info.size_bytes or 0) / (1024 * 1024)
            size_str = f"{size_mb:.1f} MB"
            date_str = info.modified[:10] if info.modified else "—"

            status = "Активна" if info.active else "Неактивна"
            if not info.valid:
                status = "Невалидна"

            self.tree.insert(
                "",
                "end",
                iid=info.model_id,
                values=(info.model_id, status, size_str, date_str, info.source or "хранилище"),
            )

        # Проверка кнопки отката
        can_rb = self.controller.can_rollback()
        if can_rb and not self.controller.is_busy:
            self.btn_rollback.state(["!disabled"])
        else:
            self.btn_rollback.state(["disabled"])

        # Проверка кнопки миграции
        can_mig = self.controller.is_legacy_available_for_migration()
        if can_mig and not self.controller.is_busy:
            self.btn_migrate.state(["!disabled"])
        else:
            self.btn_migrate.state(["disabled"])

        self._update_button_states()

    def _update_button_states(self) -> None:
        """Обновить активность кнопок в зависимости от выбранного элемента и статуса."""
        if self._closed:
            return

        is_busy = self.controller.is_busy

        if is_busy:
            self.btn_check_updates.state(["disabled"])
            self.btn_download.state(["disabled"])
            self.btn_test.state(["disabled"])
            self.btn_activate.state(["disabled"])
            self.btn_rollback.state(["disabled"])
            self.btn_migrate.state(["disabled"])
            return

        self.btn_check_updates.state(["!disabled"])

        # Проверяем, есть ли обновление для скачивания
        if self.controller.last_update_check and self.controller.last_update_check.status == "update_available":
            self.btn_download.state(["!disabled"])
        else:
            self.btn_download.state(["disabled"])

        # Проверяем выбор в дереве
        selected = self.tree.selection()
        if selected:
            sel_id = selected[0]
            models = {m.model_id: m for m in self.controller.list_local_models()}
            model_info = models.get(sel_id)

            if model_info and model_info.valid:
                self.btn_test.state(["!disabled"])
                if not model_info.active:
                    self.btn_activate.state(["!disabled"])
                else:
                    self.btn_activate.state(["disabled"])
            else:
                self.btn_test.state(["disabled"])
                self.btn_activate.state(["disabled"])
        else:
            self.btn_test.state(["disabled"])
            self.btn_activate.state(["disabled"])

    def _on_tree_select(self, _event=None) -> None:
        self._update_button_states()

    def _copy_full_sha(self) -> None:
        """Скопировать полный SHA-256 в буфер обмена."""
        if self._full_sha256:
            self.clipboard_clear()
            self.clipboard_append(self._full_sha256)
            messagebox.showinfo("Скопировано", "SHA-256 скопирован в буфер обмена.", parent=self)

    def _check_updates(self) -> None:
        """Обработчик кнопки "Проверить обновления"."""
        self.controller.is_busy = True
        self._update_button_states()
        self.lbl_update_status.config(text="Статус обновлений: идет проверка…")

        def _on_success(res: CheckUpdateResult):
            if self._closed:
                return
            if res.status == "update_available":
                size_mb = (res.remote_size_bytes or 0) / (1024 * 1024)
                msg = (
                    f"Доступна новая версия модели: {res.remote_model_id}\n"
                    f"Размер: {size_mb:.1f} MB\n"
                    f"Уверенность: {res.comparison_confidence}\n\n"
                    f"{res.message}"
                )
                messagebox.showinfo("Доступно обновление", msg, parent=self)
            else:
                conf_text = f"Уровень уверенности: {res.comparison_confidence}."
                if res.comparison_confidence == "low":
                    msg = f"Новая версия не обнаружена, но идентичность файла подтверждена только по размеру.\n({conf_text})"
                else:
                    msg = f"Установлена последняя версия: {res.local_model_id}.\n({conf_text})"
                messagebox.showinfo("Проверка обновлений", msg, parent=self)

            self._refresh_ui()

        def _on_error(err_msg: str):
            if self._closed:
                return
            messagebox.showerror("Ошибка проверки", err_msg, parent=self)
            self._refresh_ui()

        self.controller.check_updates(on_success=_on_success, on_error=_on_error)

    def _download_model(self) -> None:
        """Обработчик кнопки "Скачать"."""
        target_id = None
        if self.controller.last_update_check and self.controller.last_update_check.remote_model_id:
            target_id = self.controller.last_update_check.remote_model_id

        if not target_id:
            return

        self.progress_frame.pack(fill="x", pady=10)
        self.lbl_progress_info.config(text=f"Подготовка к скачиванию {target_id}…")
        self.progress_bar.config(value=0, mode="determinate")
        self.controller.is_busy = True
        self._update_button_states()

        def _on_prog(p: DownloadProgress):
            if self._closed:
                return
            if p.total_bytes:
                cur_mb = p.downloaded_bytes / (1024 * 1024)
                tot_mb = p.total_bytes / (1024 * 1024)
                speed_mb = p.bytes_per_second / (1024 * 1024)
                pct = p.percent or 0.0
                text = f"{cur_mb:.1f} MB / {tot_mb:.1f} MB ({pct:.1f}%) - {speed_mb:.1f} MB/s"
                self.progress_bar.config(mode="determinate", value=pct)
            else:
                cur_mb = p.downloaded_bytes / (1024 * 1024)
                speed_mb = p.bytes_per_second / (1024 * 1024)
                text = f"Скачано: {cur_mb:.1f} MB ({speed_mb:.1f} MB/s)"
                self.progress_bar.config(mode="indeterminate")
                self.progress_bar.step(2)

            self.lbl_progress_info.config(text=text)

        def _on_comp(success: bool, msg: str):
            if self._closed:
                return
            self.progress_frame.pack_forget()
            if success:
                messagebox.showinfo("Скачивание завершено", msg, parent=self)
            else:
                messagebox.showwarning("Результат скачивания", msg, parent=self)
            self._refresh_ui()

        self.controller.download_model(model_id=target_id, on_progress=_on_prog, on_complete=_on_comp)

    def _cancel_download(self) -> None:
        """Отмена скачивания."""
        self.controller.cancel_download()

    def _smoke_test(self) -> None:
        """Обработчик кнопки "Проверить модель"."""
        selected = self.tree.selection()
        if not selected:
            return
        model_id = selected[0]

        self.controller.is_busy = True
        self._update_button_states()

        def _on_comp(res: SmokeTestResult):
            if self._closed:
                return
            if res.success:
                e_res = res.speaker_results.get("eugene")
                x_res = res.speaker_results.get("xenia")
                e_status = "успешно" if e_res and e_res.status == "success" else "ошибка"
                x_status = "успешно" if x_res and x_res.status == "success" else "ошибка"

                avail_str = ", ".join(res.available_speakers) if res.available_speakers else "нет данных"

                msg = (
                    f"Результаты smoke-test модели {model_id}:\n\n"
                    f"eugene — {e_status}\n"
                    f"xenia — {x_status}\n\n"
                    f"Доступные голоса в модели:\n{avail_str}"
                )
                messagebox.showinfo("Smoke-test пройден", msg, parent=self)
            else:
                messagebox.showerror("Smoke-test не пройден", f"Ошибка проверки модели {model_id}:\n\n{res.message}", parent=self)

            self._refresh_ui()

        self.controller.run_smoke_test(model_id=model_id, all_speakers=False, on_complete=_on_comp)

    def _activate_model(self) -> None:
        """Обработчик кнопки "Активировать"."""
        selected = self.tree.selection()
        if not selected:
            return
        model_id = selected[0]

        active_sum = self.controller.get_active_model_summary()
        active_id = active_sum.model_id if active_sum else "—"

        confirm_msg = (
            f"Будет активирована модель {model_id}.\n\n"
            f"Текущая модель {active_id} останется на диске и будет доступна для отката.\n\n"
            f"Перед переключением будут проверены голоса eugene и xenia."
        )
        if not messagebox.askyesno("Подтверждение активации", confirm_msg, parent=self):
            return

        self.controller.is_busy = True
        self._update_button_states()

        def _on_comp(success: bool, msg: str):
            if self._closed:
                return
            if success:
                messagebox.showinfo("Успешная активация", msg, parent=self)
            else:
                messagebox.showerror("Ошибка активации", msg, parent=self)
            self._refresh_ui()

        self.controller.activate_model(model_id=model_id, current_voice=self.current_voice, on_complete=_on_comp)

    def _rollback_model(self) -> None:
        """Обработчик кнопки "Откатить"."""
        active_sum = self.controller.get_active_model_summary()
        active_id = active_sum.model_id if active_sum else "—"

        if not messagebox.askyesno("Подтверждение отката", f"Вернуться с модели {active_id} на предыдущую заведомо рабочую модель?", parent=self):
            return

        self.controller.is_busy = True
        self._update_button_states()

        def _on_comp(success: bool, msg: str):
            if self._closed:
                return
            if success:
                messagebox.showinfo("Успешный откат", msg, parent=self)
            else:
                messagebox.showerror("Ошибка отката", msg, parent=self)
            self._refresh_ui()

        self.controller.rollback_model(on_complete=_on_comp)

    def _migrate_legacy(self) -> None:
        """Обработчик кнопки "Перенести модель"."""
        confirm_msg = (
            "Обнаружена модель Silero внутри виртуального окружения (.venv).\n\n"
            "Перенести её в постоянное хранилище (~/.local/share/fb2-silero-audiobook/models/)?\n\n"
            "Исходная модель не будет удалена."
        )
        if not messagebox.askyesno("Перенос модели", confirm_msg, parent=self):
            return

        self.controller.is_busy = True
        self._update_button_states()

        def _on_comp(success: bool, msg: str):
            if self._closed:
                return
            if success:
                messagebox.showinfo("Перенос завершен", msg, parent=self)
            else:
                messagebox.showerror("Ошибка переноса", msg, parent=self)
            self._refresh_ui()

        self.controller.migrate_legacy_model(on_complete=_on_comp)
