"""Минимальный одностраничный GUI для создания аудиокниги из FB2."""

from __future__ import annotations

import asyncio
import os
import queue
import subprocess
import threading
import time
import traceback
import tkinter as tk
import tkinter.font as tkfont
from pathlib import Path
from tkinter import filedialog, messagebox, scrolledtext, ttk
from typing import Optional

from src.config.settings import Settings, load_settings, save_settings
from src.core.comment_manager import CommentConfig
from src.core.pipeline import AppConfig, Pipeline
from src.core.tts_manager import BACKEND_NAMES, BACKEND_VOICES, TTSConfig
from src.utils.exceptions import PipelineCanceledError


LANGUAGES = {
    "Русский": "ru",
    "English": "en",
    "日本語": "ja",
    "中文": "zh",
}
LANGUAGE_NAMES = {code: name for name, code in LANGUAGES.items()}
BACKENDS = {
    BACKEND_NAMES.get(code, code): code
    for code in ("edge", "piper", "supertonic", "silero")
}
GENDER_NAMES = {
    "female": "женский",
    "male": "мужской",
}
UI_FONT_FAMILY = "Noto Sans"
MONO_FONT_FAMILY = "DejaVu Sans Mono"
UI_FONT_NAMES = (
    "TkDefaultFont",
    "TkTextFont",
    "TkMenuFont",
    "TkHeadingFont",
    "TkCaptionFont",
    "TkSmallCaptionFont",
    "TkIconFont",
)


def available_voices(backend: str, language: str) -> list[tuple[str, str]]:
    """Вернуть пары (подпись, имя голоса) для выбранных движка и языка."""
    backend_voices = BACKEND_VOICES.get(backend, BACKEND_VOICES["edge"])
    language_voices = backend_voices.get(language)
    fallback_used = language_voices is None
    if language_voices is None:
        language_voices = backend_voices.get("en", {})

    result: list[tuple[str, str]] = []
    seen: set[str] = set()
    for gender, voice in language_voices.items():
        if voice in seen:
            continue
        seen.add(voice)
        gender_name = GENDER_NAMES.get(gender, gender)
        suffix = ", fallback English" if fallback_used else ""
        result.append((f"{voice} ({gender_name}{suffix})", voice))
    return result


def voice_gender(backend: str, language: str, voice: str) -> str:
    """Определить пол выбранного голоса по существующему BACKEND_VOICES."""
    backend_voices = BACKEND_VOICES.get(backend, {})
    language_voices = backend_voices.get(language, {})
    for gender, candidate in language_voices.items():
        if candidate == voice:
            return gender

    for voices in backend_voices.values():
        for gender, candidate in voices.items():
            if candidate == voice:
                return gender
    return "female"


def format_duration(elapsed: float) -> str:
    """Отформатировать длительность обработки для итогового сообщения."""
    total_seconds = max(0, int(round(elapsed)))
    if total_seconds < 60:
        return f"{total_seconds} сек"
    if total_seconds < 3600:
        minutes, seconds = divmod(total_seconds, 60)
        return f"{minutes} мин {seconds} сек"
    hours, remainder = divmod(total_seconds, 3600)
    minutes = remainder // 60
    return f"{hours} ч {minutes} мин"


def format_file_size(path: Path) -> str:
    """Вернуть размер файла в мебибайтах."""
    return f"{path.stat().st_size / (1024 * 1024):.2f} МиБ"


def build_pipeline_config(
    settings: Settings,
    book_path: Path,
    output_dir: Path,
    language: str,
    backend: str,
    voice: str,
) -> AppConfig:
    """Собрать конфигурацию существующего backend для минимального GUI."""
    comment_config = CommentConfig(
        enabled=False,
        provider=settings.ai_provider,
        api_key="",
        system_prompt=settings.system_prompt,
        frequency=settings.comment_frequency,
        max_concurrent=settings.max_concurrent,
    )
    tts_config = TTSConfig(
        backend=backend,
        main_voice=voice,
        comment_voice=voice,
        main_speed=settings.main_speed,
        comment_speed=settings.comment_speed,
        pause_before_comment=settings.pause_before_comment,
        pause_after_comment=settings.pause_after_comment,
        pause_between_sentences=settings.pause_between_sentences,
    )
    return AppConfig(
        book_path=book_path,
        output_dir=output_dir,
        lang=language,
        chapter_start=0,
        chapter_end=0,
        comment_config=comment_config,
        tts_config=tts_config,
    )


class AudiobookGeneratorGUI:
    """Один экран: книга, язык, движок, голос, папка и запуск."""

    def __init__(self, root: tk.Tk, settings: Optional[Settings] = None):
        self.root = root
        self.settings = settings or load_settings()
        self.pipeline: Optional[Pipeline] = None
        self.worker: Optional[threading.Thread] = None
        self.events: queue.Queue[tuple] = queue.Queue()
        self.voice_values: dict[str, str] = {}
        self.started_at: Optional[float] = None
        self.last_result_path: Optional[Path] = None
        self.cancel_event: Optional[threading.Event] = None
        self.worker_done_event: Optional[threading.Event] = None
        self.worker_outcome: Optional[tuple] = None
        self.terminal_handled = False
        self.cancel_requested = False
        self.close_after_worker = False
        self.cuda_visible_devices_was_set = "CUDA_VISIBLE_DEVICES" in os.environ
        self.initial_cuda_visible_devices = os.environ.get("CUDA_VISIBLE_DEVICES")

        self.root.title("Audiobook Generator")
        self.root.geometry("860x650")
        self.root.minsize(760, 580)
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self._configure_fonts()

        self.book_var = tk.StringVar(value=self.settings.book_path)
        self.output_var = tk.StringVar(value=self.settings.output_dir)
        self.language_var = tk.StringVar(
            value=LANGUAGE_NAMES.get(self.settings.book_lang, "Русский")
        )
        self.backend_var = tk.StringVar(
            value=next(
                (
                    name
                    for name, code in BACKENDS.items()
                    if code == self.settings.tts_backend
                ),
                "Edge TTS",
            )
        )
        self.voice_var = tk.StringVar()
        self.use_gpu_var = tk.BooleanVar(value=self.settings.use_gpu)

        self._create_widgets()
        self._refresh_voices()
        self._refresh_gpu_state()
        self.root.after(100, self._poll_events)

    def _configure_fonts(self) -> None:
        """Использовать шрифты с гарантированной поддержкой кириллицы."""
        available_fonts = set(tkfont.names(root=self.root))
        for font_name in UI_FONT_NAMES:
            if font_name not in available_fonts:
                continue
            tkfont.nametofont(font_name, root=self.root).configure(
                family=UI_FONT_FAMILY,
                size=11,
            )
        if "TkFixedFont" in available_fonts:
            tkfont.nametofont("TkFixedFont", root=self.root).configure(
                family=MONO_FONT_FAMILY,
                size=10,
            )
        if "TkTooltipFont" in available_fonts:
            tkfont.nametofont("TkTooltipFont", root=self.root).configure(
                family=UI_FONT_FAMILY,
                size=10,
            )

    def _create_widgets(self) -> None:
        main = ttk.Frame(self.root, padding=20)
        main.pack(fill="both", expand=True)
        main.columnconfigure(1, weight=1)
        main.rowconfigure(7, weight=1)

        ttk.Label(
            main,
            text="Создание аудиокниги",
            font=(UI_FONT_FAMILY, 18, "bold"),
        ).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 18))

        ttk.Label(main, text="FB2-файл:").grid(
            row=1, column=0, sticky="w", padx=(0, 12), pady=6
        )
        ttk.Entry(main, textvariable=self.book_var).grid(
            row=1, column=1, sticky="ew", pady=6
        )
        ttk.Button(main, text="Выбрать файл…", command=self._choose_book).grid(
            row=1, column=2, padx=(10, 0), pady=6
        )

        ttk.Label(main, text="Язык книги:").grid(
            row=2, column=0, sticky="w", padx=(0, 12), pady=6
        )
        language_box = ttk.Combobox(
            main,
            textvariable=self.language_var,
            values=list(LANGUAGES),
            state="readonly",
        )
        language_box.grid(row=2, column=1, columnspan=2, sticky="ew", pady=6)
        language_box.bind("<<ComboboxSelected>>", self._on_voice_source_changed)

        ttk.Label(main, text="TTS-движок:").grid(
            row=3, column=0, sticky="w", padx=(0, 12), pady=6
        )
        backend_box = ttk.Combobox(
            main,
            textvariable=self.backend_var,
            values=list(BACKENDS),
            state="readonly",
        )
        backend_box.grid(row=3, column=1, columnspan=2, sticky="ew", pady=6)
        backend_box.bind("<<ComboboxSelected>>", self._on_voice_source_changed)

        ttk.Label(main, text="Голос:").grid(
            row=4, column=0, sticky="w", padx=(0, 12), pady=6
        )
        self.voice_box = ttk.Combobox(
            main,
            textvariable=self.voice_var,
            state="readonly",
        )
        self.voice_box.grid(
            row=4, column=1, columnspan=2, sticky="ew", pady=6
        )

        ttk.Label(main, text="Выходная папка:").grid(
            row=5, column=0, sticky="w", padx=(0, 12), pady=6
        )
        ttk.Entry(main, textvariable=self.output_var).grid(
            row=5, column=1, sticky="ew", pady=6
        )
        ttk.Button(main, text="Выбрать папку…", command=self._choose_output).grid(
            row=5, column=2, padx=(10, 0), pady=6
        )

        self.gpu_check = ttk.Checkbutton(
            main,
            text="Использовать GPU для Silero, если доступна CUDA",
            variable=self.use_gpu_var,
        )
        self.gpu_check.grid(
            row=6, column=0, columnspan=3, sticky="w", pady=(8, 12)
        )

        log_frame = ttk.LabelFrame(main, text="Статус / лог", padding=8)
        log_frame.grid(
            row=7, column=0, columnspan=3, sticky="nsew", pady=(0, 12)
        )
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        self.log = scrolledtext.ScrolledText(
            log_frame,
            height=12,
            wrap="word",
            state="disabled",
            font=(MONO_FONT_FAMILY, 10),
        )
        self.log.grid(row=0, column=0, sticky="nsew")

        self.progress = ttk.Progressbar(
            main,
            mode="determinate",
            maximum=100,
        )
        self.progress.grid(
            row=8, column=0, columnspan=3, sticky="ew", pady=(0, 12)
        )

        button_frame = ttk.Frame(main)
        button_frame.grid(
            row=9, column=0, columnspan=3, sticky="ew"
        )
        button_frame.columnconfigure(0, weight=1)

        self.start_button = ttk.Button(
            button_frame,
            text="Создать аудиокнигу",
            command=self._start,
        )
        self.start_button.grid(
            row=0, column=0, sticky="ew", ipady=7
        )
        self.cancel_button = ttk.Button(
            button_frame,
            text="Прервать",
            command=self._request_cancel,
            state="disabled",
        )
        self.cancel_button.grid(
            row=0, column=1, padx=(10, 0), ipady=7
        )
        self.open_folder_button = ttk.Button(
            button_frame,
            text="Открыть папку",
            command=self._open_result_folder,
            state="disabled",
        )
        self.open_folder_button.grid(
            row=0, column=2, padx=(10, 0), ipady=7
        )

        self._append_log(
            "Выберите книгу, язык, движок, голос и выходную папку."
        )
        self._append_log("Проверка кириллицы: русский текст")

    def _choose_book(self) -> None:
        filename = filedialog.askopenfilename(
            parent=self.root,
            title="Выберите FB2-файл",
            filetypes=[("Книги FB2", "*.fb2"), ("Все файлы", "*.*")],
        )
        if filename:
            self.book_var.set(filename)

    def _choose_output(self) -> None:
        directory = filedialog.askdirectory(
            parent=self.root,
            title="Выберите выходную папку",
            initialdir=self.output_var.get() or str(Path.home()),
        )
        if directory:
            self.output_var.set(directory)

    def _on_voice_source_changed(self, _event=None) -> None:
        self._refresh_voices()
        self._refresh_gpu_state()

    def _refresh_voices(self) -> None:
        backend = BACKENDS.get(self.backend_var.get(), "edge")
        language = LANGUAGES.get(self.language_var.get(), "ru")
        options = available_voices(backend, language)
        self.voice_values = dict(options)
        labels = list(self.voice_values)
        self.voice_box.configure(values=labels)

        preferred_voice = BACKEND_VOICES.get(backend, {}).get(language, {}).get(
            self.settings.main_gender
        )
        preferred_label = next(
            (
                label
                for label, voice in options
                if voice == preferred_voice
            ),
            labels[0] if labels else "",
        )
        self.voice_var.set(preferred_label)

    def _refresh_gpu_state(self) -> None:
        backend = BACKENDS.get(self.backend_var.get(), "edge")
        if backend == "silero":
            self.gpu_check.state(["!disabled"])
        else:
            self.gpu_check.state(["disabled"])

    def _validate(self) -> Optional[tuple[Path, Path, str, str, str]]:
        book_path = Path(self.book_var.get().strip()).expanduser()
        if not book_path.is_file():
            messagebox.showerror(
                "Ошибка",
                "Выберите существующий FB2-файл.",
                parent=self.root,
            )
            return None
        if book_path.suffix.lower() != ".fb2":
            messagebox.showerror(
                "Ошибка",
                "Выбранный файл должен иметь расширение .fb2.",
                parent=self.root,
            )
            return None

        output_text = self.output_var.get().strip()
        if not output_text:
            messagebox.showerror(
                "Ошибка",
                "Выберите выходную папку.",
                parent=self.root,
            )
            return None
        output_dir = Path(output_text).expanduser()
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            messagebox.showerror(
                "Ошибка",
                f"Не удалось создать выходную папку:\n{exc}",
                parent=self.root,
            )
            return None

        language = LANGUAGES.get(self.language_var.get(), "ru")
        backend = BACKENDS.get(self.backend_var.get(), "edge")
        voice = self.voice_values.get(self.voice_var.get(), "")
        if not voice:
            messagebox.showerror(
                "Ошибка",
                "Для выбранных языка и движка нет доступного голоса.",
                parent=self.root,
            )
            return None
        return book_path, output_dir, language, backend, voice

    def _start(self) -> None:
        if self.worker and self.worker.is_alive():
            return

        selection = self._validate()
        if selection is None:
            return
        book_path, output_dir, language, backend, voice = selection
        self.last_result_path = None
        self.open_folder_button.state(["disabled"])
        self.start_button.configure(text="Создать аудиокнигу")

        gender = voice_gender(backend, language, voice)
        self.settings.book_path = str(book_path)
        self.settings.output_dir = str(output_dir)
        self.settings.book_lang = language
        self.settings.tts_backend = backend
        self.settings.main_gender = gender
        self.settings.comment_gender = gender
        self.settings.use_gpu = self.use_gpu_var.get()
        save_settings(self.settings)

        if backend == "silero":
            if not self.use_gpu_var.get():
                os.environ["CUDA_VISIBLE_DEVICES"] = ""
            elif self.cuda_visible_devices_was_set:
                os.environ["CUDA_VISIBLE_DEVICES"] = (
                    self.initial_cuda_visible_devices or ""
                )
            else:
                os.environ.pop("CUDA_VISIBLE_DEVICES", None)

        config = build_pipeline_config(
            self.settings,
            book_path,
            output_dir,
            language,
            backend,
            voice,
        )
        self.pipeline = Pipeline(config)
        self.cancel_event = threading.Event()
        self.worker_done_event = threading.Event()
        self.worker_outcome = None
        self.terminal_handled = False
        self.cancel_requested = False
        self.started_at = time.monotonic()
        self.last_result_path = None
        self.progress["value"] = 0
        self.start_button.configure(text="Идёт обработка…")
        self.start_button.state(["disabled"])
        self.cancel_button.configure(text="Прервать")
        self.cancel_button.state(["!disabled"])
        self.open_folder_button.state(["disabled"])
        self._append_log(
            f"Запуск: {book_path.name}; движок: {backend}; голос: {voice}"
        )

        self.worker = threading.Thread(
            target=self._worker_entry,
            args=(self.pipeline, self.worker_done_event),
            daemon=True,
        )
        self.worker.start()

    def _worker_entry(
        self,
        pipeline: Pipeline,
        done_event: threading.Event,
    ) -> None:
        try:
            self.worker_outcome = self._run_pipeline(pipeline)
        finally:
            done_event.set()

    def _run_pipeline(self, pipeline: Pipeline) -> tuple:
        def progress_callback(status: str, progress: float, **_details) -> None:
            self.events.put(("progress", status, progress))

        def detail_callback(
            completed: int,
            total: int,
            text_preview: str,
            voice: str,
            backend_name: str,
        ) -> None:
            progress = 0.2 + (completed / max(total, 1)) * 0.2
            detail = (
                f"Синтез {completed}/{total}: "
                f"{text_preview[:90]} [{backend_name}, {voice}]"
            )
            self.events.put(("progress", detail, progress))

        try:
            result = asyncio.run(
                pipeline.run(
                    progress_callback=progress_callback,
                    detail_callback=detail_callback,
                    cancel_event=self.cancel_event,
                )
            )
            if not result or not result.is_file():
                raise RuntimeError("Pipeline не вернул созданный аудиофайл")
            return ("success", result)
        except PipelineCanceledError:
            return ("canceled",)
        except Exception as exc:
            return ("error", str(exc), traceback.format_exc())

    def _request_cancel(self) -> None:
        """Запросить кооперативную остановку активного запуска."""
        if self.cancel_requested or not self.worker:
            return
        self.cancel_requested = True
        self.cancel_button.configure(text="Останавливаем…")
        self.cancel_button.state(["disabled"])
        if self.cancel_event is not None:
            self.cancel_event.set()
        if self.pipeline is not None:
            self.pipeline.cancel()

    def _poll_events(self) -> None:
        try:
            while True:
                event = self.events.get_nowait()
                self._handle_event(event)
        except queue.Empty:
            pass

        if self._poll_worker_completion():
            return

        if self.root.winfo_exists():
            self.root.after(100, self._poll_events)

    def _poll_worker_completion(self) -> bool:
        """Применить единственный итог только после завершения worker-thread."""
        if (
            self.worker is None
            or self.worker_done_event is None
            or not self.worker_done_event.is_set()
            or self.worker.is_alive()
            or self.worker_outcome is None
        ):
            return False
        will_close = self.close_after_worker
        self._handle_event(self.worker_outcome)
        return will_close

    def _handle_event(self, event: tuple) -> None:
        """Обработать одно worker-событие в GUI-потоке."""
        kind = event[0]
        if kind in {"success", "canceled", "error"}:
            if self.terminal_handled:
                return
            self.terminal_handled = True
        if kind == "progress":
            _, status, progress = event
            self.progress["value"] = max(0, min(100, progress * 100))
            if not status.startswith("Аудиокнига готова:"):
                self._append_log(status)
        elif kind == "success":
            if self.cancel_requested:
                self._finish_canceled()
                return
            _, result = event
            result_path = Path(result)
            started_at = self.started_at or time.monotonic()
            elapsed = time.monotonic() - started_at
            self.progress["value"] = 100
            self._append_log(
                f"Готово за {format_duration(elapsed)} · "
                f"{format_file_size(result_path)}: {result_path}"
            )
            self.started_at = None
            self.last_result_path = result_path
            self.start_button.configure(text="Создать ещё одну")
            self.start_button.state(["!disabled"])
            self.open_folder_button.state(["!disabled"])
            self._finish_worker()
        elif kind == "canceled":
            self._finish_canceled()
        elif kind == "error":
            _, error, details = event
            self._append_log(f"Ошибка: {error}")
            self._append_log(details)
            self.started_at = None
            self.last_result_path = None
            self.start_button.configure(text="Создать аудиокнигу")
            self.start_button.state(["!disabled"])
            self.open_folder_button.state(["disabled"])
            self._finish_worker()
        elif kind == "open_error":
            _, error = event
            messagebox.showerror(
                "Ошибка",
                f"Не удалось открыть папку:\n{error}",
                parent=self.root,
            )

    def _finish_canceled(self) -> None:
        self._append_log("Обработка отменена пользователем")
        self.progress["value"] = 0
        self.started_at = None
        self.last_result_path = None
        self.start_button.configure(text="Создать аудиокнигу")
        self.start_button.state(["!disabled"])
        self.open_folder_button.state(["disabled"])
        self._finish_worker()

    def _finish_worker(self) -> None:
        self.cancel_button.configure(text="Прервать")
        self.cancel_button.state(["disabled"])
        self.pipeline = None
        self.worker = None
        self.cancel_event = None
        self.worker_done_event = None
        self.worker_outcome = None
        self.cancel_requested = False
        if self.close_after_worker:
            self.root.destroy()

    def _append_log(self, message: str) -> None:
        self.log.configure(state="normal")
        self.log.insert("end", message.rstrip() + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    def _open_result_folder(self) -> None:
        """Открыть папку созданного файла, не блокируя главный поток GUI."""
        if self.last_result_path is None:
            return
        try:
            process = subprocess.Popen(
                ["xdg-open", str(self.last_result_path.parent)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                text=True,
                start_new_session=True,
            )
            threading.Thread(
                target=self._watch_folder_opener,
                args=(process,),
                daemon=True,
            ).start()
        except OSError as exc:
            messagebox.showerror(
                "Ошибка",
                f"Не удалось открыть папку:\n{exc}",
                parent=self.root,
            )

    def _watch_folder_opener(self, process: subprocess.Popen) -> None:
        """Дождаться xdg-open вне GUI-потока и передать возможную ошибку."""
        _, stderr = process.communicate()
        if process.returncode:
            error = (stderr or "xdg-open завершился с ошибкой").strip()
            self.events.put(("open_error", error))

    def _on_close(self) -> None:
        if self.worker and self.worker.is_alive():
            if not messagebox.askyesno(
                "Выход",
                "Прервать обработку и выйти?",
                parent=self.root,
            ):
                return
            self.close_after_worker = True
            self._request_cancel()
            return
        self.root.destroy()


def main() -> None:
    root = tk.Tk()
    AudiobookGeneratorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
