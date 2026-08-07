"""Структурированная диагностика одного запуска audiobook pipeline."""

from __future__ import annotations

import contextlib
import copy
import importlib.metadata
import json
import math
import os
import platform
import re
import shutil
import subprocess
import sys
import threading
import time
import uuid
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Iterator, Mapping, Optional

try:
    import fcntl
except ImportError:  # pragma: no cover - Linux is the supported target
    fcntl = None


SCHEMA_VERSION = 1
APP_NAME = "fb2-silero-audiobook"
LOG_PREFIX = f"{APP_NAME}-run-"
MIN_FILE_BYTES = 8 * 1024
MIN_TERMINAL_RESERVE_BYTES = 4 * 1024
TRUNCATION_EVENT_RESERVE_BYTES = 512
ERROR_LIKE_FIELDS = {
    "error", "message", "reason", "detail", "warning", "exception", "stderr",
}
SECRET_FIELD_NAMES = {
    "token", "apikey", "password", "authorization", "accesstoken",
    "refreshtoken", "secret", "clientsecret",
}


def state_logs_directory(
    env: Optional[Mapping[str, str]] = None,
    home: Optional[Path] = None,
) -> Path:
    environment = os.environ if env is None else env
    xdg_state_home = environment.get("XDG_STATE_HOME", "").strip()
    if xdg_state_home:
        return Path(xdg_state_home).expanduser() / APP_NAME / "logs"
    home_dir = Path.home() if home is None else Path(home)
    return home_dir / ".local" / "state" / APP_NAME / "logs"


def safe_book_slug(value: str, limit: int = 48) -> str:
    """Вернуть короткий Unicode slug без path traversal и control chars."""
    value = re.sub(r"[\x00-\x1f\x7f]", "", str(value))
    value = value.replace("/", " ").replace("\\", " ")
    value = re.sub(r"[<>:\"|?*]", " ", value)
    value = re.sub(r"\s+", "-", value.strip())
    value = re.sub(r"[^\w().\-]+", "-", value, flags=re.UNICODE)
    value = value.strip(" .-_")[:limit].strip(" .-_")
    return value or "book"


@dataclass(frozen=True)
class DiagnosticsLimits:
    max_files: int = 30
    max_total_bytes: int = 250 * 1024 * 1024
    max_file_bytes: int = 25 * 1024 * 1024
    terminal_reserve_bytes: int = 64 * 1024

    def validate(self) -> None:
        values = {
            "max_files": self.max_files,
            "max_total_bytes": self.max_total_bytes,
            "max_file_bytes": self.max_file_bytes,
            "terminal_reserve_bytes": self.terminal_reserve_bytes,
        }
        if any(isinstance(value, bool) or not isinstance(value, int) for value in values.values()):
            raise ValueError("Diagnostics limits must be integers")
        if self.max_files < 1:
            raise ValueError("max_files must be at least 1")
        if self.max_file_bytes < MIN_FILE_BYTES:
            raise ValueError(f"max_file_bytes must be at least {MIN_FILE_BYTES}")
        if self.terminal_reserve_bytes < MIN_TERMINAL_RESERVE_BYTES:
            raise ValueError(
                f"terminal_reserve_bytes must be at least {MIN_TERMINAL_RESERVE_BYTES}"
            )
        if self.terminal_reserve_bytes >= self.max_file_bytes:
            raise ValueError("terminal_reserve_bytes must be smaller than max_file_bytes")
        if self.max_total_bytes < self.max_file_bytes:
            raise ValueError("max_total_bytes must be at least max_file_bytes")


class RunDiagnostics:
    """Thread-safe, fail-open JSONL writer and lightweight system sampler."""

    def __init__(
        self,
        book_path: Path,
        run_info: Mapping[str, Any],
        *,
        logs_dir: Optional[Path] = None,
        limits: DiagnosticsLimits = DiagnosticsLimits(),
        sample_interval: float = 1.0,
        perf_counter: Callable[[], float] = time.perf_counter,
        now: Callable[[], datetime] = lambda: datetime.now().astimezone(),
        replace: Callable[[Path | str, Path | str], None] = os.replace,
    ) -> None:
        limits.validate()
        self.run_id = uuid.uuid4().hex[:8]
        self.logs_dir = state_logs_directory() if logs_dir is None else Path(logs_dir)
        self.limits = limits
        self.sample_interval = max(float(sample_interval), 0.01)
        self._perf_counter = perf_counter
        self._now = now
        self._replace = replace
        self._started = perf_counter()
        self._lock = threading.RLock()
        self._stream = None
        self._last_flush = self._started
        self._bytes_written = 0
        self._disabled = False
        self._closed = False
        self._finalizing = False
        self._finalized = threading.Event()
        self._final_result: Optional[Path] = None
        self._truncated = False
        self._diagnostic_errors = 0
        self._reported_errors: set[str] = set()
        self._sampler_stop = threading.Event()
        self._sampler_thread: Optional[threading.Thread] = None
        self._previous_cpu: Optional[tuple[int, int, list[tuple[int, int]]]] = None
        self._previous_process: Optional[tuple[float, int]] = None
        self._last_gpu_sample = 0.0
        self._nvml_attempted = False
        self._nvml_module = None
        self._nvml_handle = None
        self.warning: Optional[str] = None
        self._sensitive_paths: set[str] = {
            str(Path.home()),
            str(Path(book_path).expanduser().absolute()),
        }
        self._stats: dict[str, Any] = {
            "total_chapters": 0,
            "tts_segments": 0,
            "characters": 0,
            "tts_times": [],
            "tts_wall_seconds": 0.0,
            "audio_duration_seconds": 0.0,
            "stage_durations": {},
            "mp3_size_bytes": None,
        }

        stamp = now().strftime("%Y-%m-%d_%H-%M-%S")
        slug = safe_book_slug(Path(book_path).stem)
        base_name = f"{LOG_PREFIX}{stamp}_{slug}_{self.run_id}.jsonl"
        self.part_path = self.logs_dir / f"{base_name}.part"
        self.final_path = self.logs_dir / base_name

        try:
            self.logs_dir.mkdir(parents=True, exist_ok=True)
            self._recover_incomplete()
            self.rotate()
            self._stream = self.part_path.open(
                "x", encoding="utf-8", buffering=64 * 1024,
            )
            if fcntl is None:
                raise OSError("file locking is unavailable")
            fcntl.flock(self._stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            self.emit("run_start", **self._run_start_fields(book_path, run_info))
        except Exception as exc:
            self._disable(f"Не удалось создать диагностический журнал: {exc}")

    @property
    def available(self) -> bool:
        return (
            not self._disabled and not self._closed and not self._finalizing
            and self._stream is not None
        )

    @property
    def truncated(self) -> bool:
        return self._truncated

    @property
    def diagnostic_errors(self) -> int:
        return self._diagnostic_errors

    def _disable(self, warning: str) -> None:
        self.warning = self.warning or warning
        self._disabled = True
        try:
            if self._stream is not None:
                self._stream.close()
        except Exception:
            pass
        self._stream = None

    def register_sensitive_paths(self, *paths: Optional[Path]) -> None:
        """Register runtime paths that must be redacted from diagnostic errors."""
        with self._lock:
            for path in paths:
                if path is not None:
                    self._sensitive_paths.add(str(Path(path).expanduser().absolute()))

    def _base_event(self, event: str) -> dict[str, Any]:
        return {
            "schema_version": SCHEMA_VERSION,
            "run_id": self.run_id,
            "event": event,
            "timestamp": self._now().isoformat(),
            "elapsed_seconds": max(0.0, self._perf_counter() - self._started),
        }

    def emit(self, event: str, **fields: Any) -> bool:
        """Append one JSON object; diagnostics failures never escape."""
        with self._lock:
            if not self.available:
                return False
            try:
                payload = self._base_event(event)
                payload.update(self._sanitize_fields(fields))
                payload = _bounded_payload(payload)
                encoded = self._encode_line(payload)
                threshold = (
                    self.limits.max_file_bytes
                    - self.limits.terminal_reserve_bytes
                )
                event_limit = max(0, threshold - TRUNCATION_EVENT_RESERVE_BYTES)
                if self._bytes_written + len(encoded) > event_limit:
                    self._mark_truncated_locked(threshold)
                    return False
                self._write_encoded(encoded)
                now_value = self._perf_counter()
                if now_value - self._last_flush >= 1.0:
                    self._stream.flush()
                    self._last_flush = now_value
                return True
            except Exception as exc:
                self._diagnostic_errors += 1
                self._disable(f"Диагностический журнал недоступен: {exc}")
                return False

    def _encode_line(self, payload: Mapping[str, Any]) -> bytes:
        line = json.dumps(
            payload, ensure_ascii=False, separators=(",", ":"),
        ) + "\n"
        return line.encode("utf-8")

    def _write_encoded(self, encoded: bytes) -> None:
        self._stream.write(encoded.decode("utf-8"))
        self._bytes_written += len(encoded)

    def _mark_truncated_locked(self, threshold: int) -> None:
        if self._truncated:
            return
        self._truncated = True
        encoded = self._encode_line(self._base_event("diagnostics_truncated"))
        if self._bytes_written + len(encoded) <= threshold:
            self._write_encoded(encoded)

    def _sanitize_fields(self, fields: Mapping[str, Any]) -> dict[str, Any]:
        return {
            key: _sanitize_field_value(
                key, value, tuple(self._sensitive_paths),
            )
            for key, value in fields.items()
        }

    def diagnostic_error(self, source: str, exc: BaseException) -> None:
        key = f"{source}:{type(exc).__name__}:{exc}"
        with self._lock:
            if key in self._reported_errors:
                return
            self._reported_errors.add(key)
            self._diagnostic_errors += 1
        self.emit(
            "diagnostic_error",
            source=source,
            error_type=type(exc).__name__,
            error=str(exc)[:300],
        )

    @contextlib.contextmanager
    def stage(self, stage: str, **fields: Any) -> Iterator[None]:
        started = self._perf_counter()
        self.emit("stage_start", stage=stage, **fields)
        status = "success"
        error = None
        try:
            yield
        except BaseException as exc:
            status = "canceled" if type(exc).__name__ == "PipelineCanceledError" else "error"
            error = str(exc)[:300]
            raise
        finally:
            duration = max(0.0, self._perf_counter() - started)
            with self._lock:
                if not self._closed and not self._finalizing:
                    self._stats["stage_durations"][stage] = (
                        self._stats["stage_durations"].get(stage, 0.0) + duration
                    )
            self.emit(
                "stage_end",
                stage=stage,
                status=status,
                duration_seconds=duration,
                error=error,
                **fields,
            )

    def book_parsed(self, book: Any, duration_seconds: float) -> None:
        chapter_characters = [
            sum(len(paragraph) for paragraph in chapter.paragraphs)
            for chapter in book.chapters
        ]
        with self._lock:
            if self._closed or self._finalizing:
                return
            self._stats["total_chapters"] = len(book.chapters)
        self.emit(
            "book_parsed",
            title=book.metadata.title,
            author=book.metadata.author or None,
            chapters=len(book.chapters),
            paragraphs=sum(len(chapter.paragraphs) for chapter in book.chapters),
            total_characters=sum(chapter_characters),
            chapter_characters=chapter_characters,
            parsing_seconds=max(0.0, duration_seconds),
        )

    def record_tts_segment(
        self,
        *,
        chapter_index: int,
        segment_index: int,
        segment_total: int,
        segment_type: str,
        backend: str,
        voice: str,
        language: str,
        device: str,
        characters: int,
        wall_seconds: float,
        audio_path: Optional[Path],
        audio_info: Optional[Mapping[str, Any]] = None,
        status: str = "success",
        error: Optional[str] = None,
        text_excerpt: Optional[str] = None,
        text: Optional[str] = None,
        text_for_tts: Optional[str] = None,
        boundary_before: Optional[str] = None,
        boundary_after: Optional[str] = None,
    ) -> None:
        info = dict(audio_info or {})
        duration = _positive_float(info.get("duration_seconds"))
        wall = max(0.0, float(wall_seconds))
        chars = len(text) if text is not None else max(0, int(characters))

        if text is not None:
            if boundary_before is None:
                boundary_before = (
                    "start_of_chapter" if segment_index == 1
                    else "paragraph_break" if text.startswith("\n")
                    else "dash" if text.lstrip().startswith(("—", "-"))
                    else "sentence_continuation"
                )
            if boundary_after is None:
                t = text.rstrip().rstrip('»"\'”)]}')
                if not t:
                    boundary_after = "space" if text and text[-1].isspace() else "none"
                elif t.endswith("...") or t.endswith("…"):
                    boundary_after = "..."
                elif t.endswith("?!") or t.endswith("!?"):
                    boundary_after = "?!"
                elif t.endswith("?"):
                    boundary_after = "?"
                elif t.endswith("!"):
                    boundary_after = "!"
                elif t.endswith("."):
                    boundary_after = "."
                elif t.endswith(","):
                    boundary_after = ","
                elif t.endswith(";"):
                    boundary_after = ";"
                elif t.endswith(":"):
                    boundary_after = ":"
                elif t.endswith("—") or t.endswith("-"):
                    boundary_after = "dash"
                elif text.endswith("\n"):
                    boundary_after = "paragraph_break"
                elif text[-1].isspace():
                    boundary_after = "space"
                else:
                    boundary_after = "none"

        with self._lock:
            if self._closed or self._finalizing:
                return
            self._stats["tts_segments"] += 1
            self._stats["characters"] += chars
            self._stats["tts_times"].append(wall)
            self._stats["tts_wall_seconds"] += wall
            if duration is not None:
                self._stats["audio_duration_seconds"] += duration
        fields = {
            "chapter_index": chapter_index,
            "segment_index": segment_index,
            "segment_total": segment_total,
            "segment_type": segment_type,
            "backend": backend,
            "voice": voice,
            "language": language,
            "device": device,
            "characters": chars,
            "wall_seconds": wall,
            "audio_duration_seconds": duration,
            "audio_size_bytes": _file_size(audio_path),
            "sample_rate": info.get("sample_rate"),
            "characters_per_second": _safe_div(chars, wall),
            "realtime_factor": _safe_div(wall, duration),
            "audio_realtime_speed": _safe_div(duration, wall),
            "status": status,
            "outcome": status,
            "error": error,
        }
        if text is not None:
            fields["text"] = text
        if text_for_tts is not None and text_for_tts != text:
            fields["text_for_tts"] = text_for_tts
        if boundary_before is not None:
            fields["boundary_before"] = boundary_before
        if boundary_after is not None:
            fields["boundary_after"] = boundary_after
        if status != "success" and text_excerpt:
            fields["text_excerpt"] = text_excerpt[:80]
        self.emit("tts_segment", **fields)

    def set_mp3_result(self, path: Path, duration_seconds: Optional[float]) -> None:
        with self._lock:
            if self._closed or self._finalizing:
                return
            self._stats["mp3_size_bytes"] = _file_size(path)
            if duration_seconds is not None:
                self._stats["audio_duration_seconds"] = duration_seconds

    def start_sampler(self) -> None:
        with self._lock:
            if not self.available or self._sampler_thread is not None:
                return
            self._sampler_stop.clear()
            thread = threading.Thread(
                target=self._sample_loop,
                name=f"diagnostics-{self.run_id}",
                daemon=True,
            )
            self._sampler_thread = thread
        try:
            thread.start()
        except Exception as exc:
            with self._lock:
                if self._sampler_thread is thread:
                    self._sampler_thread = None
            self.diagnostic_error("system_sampler_start", exc)

    def stop_sampler(self, timeout: float = 5.0) -> None:
        with self._lock:
            thread = self._sampler_thread
        if thread is None:
            return
        self._sampler_stop.set()
        try:
            if thread is not threading.current_thread():
                thread.join(timeout=timeout)
        except Exception as exc:
            self.diagnostic_error("system_sampler_stop", exc)
        with self._lock:
            if self._sampler_thread is thread and not thread.is_alive():
                self._sampler_thread = None

    def _sample_loop(self) -> None:
        while not self._sampler_stop.is_set():
            sample_started = self._perf_counter()
            try:
                fields = self._system_metrics()
                fields["sampler_overhead_seconds"] = max(
                    0.0, self._perf_counter() - sample_started,
                )
                self.emit("system_sample", **fields)
            except Exception as exc:
                self.diagnostic_error("system_sampler", exc)
            remaining = self.sample_interval - (
                self._perf_counter() - sample_started
            )
            self._sampler_stop.wait(max(0.0, remaining))

    def _system_metrics(self) -> dict[str, Any]:
        cpu_percent, per_cpu = self._cpu_percentages()
        process_cpu = self._process_cpu_percent()
        mem = _read_meminfo()
        process = _read_process_status()
        gpu = self._gpu_metrics()
        cuda_allocated = cuda_reserved = None
        torch = sys.modules.get("torch")
        try:
            if torch is not None and torch.cuda.is_available():
                cuda_allocated = torch.cuda.memory_allocated()
                cuda_reserved = torch.cuda.memory_reserved()
        except Exception as exc:
            self.diagnostic_error("torch_cuda_memory", exc)
        return {
            "cpu_percent": cpu_percent,
            "cpu_logical_percent": per_cpu,
            "cpu_frequency_mhz": _cpu_frequency_mhz(),
            "cpu_temperature_c": _cpu_temperature_c(),
            "ram_used_bytes": mem.get("used"),
            "ram_available_bytes": mem.get("available"),
            "process_cpu_percent": process_cpu,
            "process_rss_bytes": process.get("rss"),
            "process_threads": process.get("threads"),
            **gpu,
            "torch_cuda_allocated_bytes": cuda_allocated,
            "torch_cuda_reserved_bytes": cuda_reserved,
        }

    def _cpu_percentages(self) -> tuple[Optional[float], Optional[list[float]]]:
        current = _read_cpu_times()
        previous = self._previous_cpu
        self._previous_cpu = current
        if previous is None or current is None:
            return None, None
        total = _cpu_delta_percent(previous[:2], current[:2])
        per_cpu = [
            _cpu_delta_percent(old, new)
            for old, new in zip(previous[2], current[2])
        ]
        return total, per_cpu

    def _process_cpu_percent(self) -> Optional[float]:
        current = _read_process_cpu()
        previous = self._previous_process
        self._previous_process = current
        if current is None or previous is None:
            return None
        wall_delta = current[0] - previous[0]
        ticks_per_second = os.sysconf("SC_CLK_TCK")
        cpu_seconds = (current[1] - previous[1]) / ticks_per_second
        return _safe_div(cpu_seconds * 100.0, wall_delta)

    def _gpu_metrics(self) -> dict[str, Any]:
        empty = {
            "gpu_utilization_percent": None,
            "gpu_memory_used_bytes": None,
            "gpu_memory_total_bytes": None,
            "gpu_temperature_c": None,
            "gpu_power_draw_watts": None,
        }
        now_value = self._perf_counter()
        if now_value - self._last_gpu_sample < max(1.0, self.sample_interval):
            return empty
        self._last_gpu_sample = now_value
        nvml_metrics = self._nvml_metrics()
        if nvml_metrics is not None:
            return nvml_metrics
        executable = shutil.which("nvidia-smi")
        if executable is None:
            return empty
        try:
            result = subprocess.run(
                [
                    executable,
                    "--query-gpu=utilization.gpu,memory.used,memory.total,"
                    "temperature.gpu,power.draw",
                    "--format=csv,noheader,nounits",
                ],
                capture_output=True,
                text=True,
                timeout=min(2.0, max(0.2, self.sample_interval)),
                check=False,
            )
            if result.returncode or not result.stdout.strip():
                return empty
            values = [part.strip() for part in result.stdout.splitlines()[0].split(",")]
            if len(values) < 5:
                return empty
            return {
                "gpu_utilization_percent": _number(values[0]),
                "gpu_memory_used_bytes": _mib_to_bytes(values[1]),
                "gpu_memory_total_bytes": _mib_to_bytes(values[2]),
                "gpu_temperature_c": _number(values[3]),
                "gpu_power_draw_watts": _number(values[4]),
            }
        except Exception as exc:
            self.diagnostic_error("nvidia_smi", exc)
            return empty

    def _nvml_metrics(self) -> Optional[dict[str, Any]]:
        if not self._nvml_attempted:
            self._nvml_attempted = True
            try:
                import pynvml
                pynvml.nvmlInit()
                self._nvml_module = pynvml
                self._nvml_handle = pynvml.nvmlDeviceGetHandleByIndex(0)
            except (ImportError, ModuleNotFoundError):
                return None
            except Exception as exc:
                self.diagnostic_error("nvml_init", exc)
                return None
        if self._nvml_module is None or self._nvml_handle is None:
            return None
        try:
            nvml = self._nvml_module
            memory = nvml.nvmlDeviceGetMemoryInfo(self._nvml_handle)
            utilization = nvml.nvmlDeviceGetUtilizationRates(self._nvml_handle)
            temperature = nvml.nvmlDeviceGetTemperature(
                self._nvml_handle, nvml.NVML_TEMPERATURE_GPU,
            )
            try:
                power = nvml.nvmlDeviceGetPowerUsage(self._nvml_handle) / 1000.0
            except Exception:
                power = None
            return {
                "gpu_utilization_percent": float(utilization.gpu),
                "gpu_memory_used_bytes": int(memory.used),
                "gpu_memory_total_bytes": int(memory.total),
                "gpu_temperature_c": float(temperature),
                "gpu_power_draw_watts": power,
            }
        except Exception as exc:
            self.diagnostic_error("nvml_sample", exc)
            return None

    def finalize(
        self,
        status: str,
        *,
        error: Optional[str] = None,
        output_path: Optional[Path] = None,
    ) -> Optional[Path]:
        """Stop sampler, append terminal+summary, close and atomically rename."""
        with self._lock:
            if self._closed:
                return self._final_result
            if self._finalizing:
                wait_for_other = True
            else:
                self._finalizing = True
                wait_for_other = False
        if wait_for_other:
            self._finalized.wait()
            with self._lock:
                return self._final_result

        result: Optional[Path] = None
        fatal_exception: Optional[BaseException] = None
        try:
            self.stop_sampler()
            if self._nvml_module is not None:
                try:
                    self._nvml_module.nvmlShutdown()
                except Exception as exc:
                    self.diagnostic_error("nvml_shutdown", exc)
                finally:
                    self._nvml_module = None
                    self._nvml_handle = None
            with self._lock:
                result = self._finalize_locked(status, error, output_path)
        except Exception as exc:
            with self._lock:
                self._diagnostic_errors += 1
                self.warning = self.warning or (
                    f"Не удалось завершить диагностический журнал: {exc}"
                )
        except BaseException as exc:
            fatal_exception = exc
            with self._lock:
                self._diagnostic_errors += 1
                self.warning = self.warning or (
                    "Завершение диагностического журнала было прервано: "
                    f"{type(exc).__name__}"
                )
        finally:
            with self._lock:
                stream = self._stream
                self._stream = None
                if stream is not None:
                    try:
                        stream.close()
                    except BaseException as close_exc:
                        self._diagnostic_errors += 1
                        self.warning = self.warning or (
                            "Не удалось закрыть диагностический журнал: "
                            f"{type(close_exc).__name__}"
                        )
                        if fatal_exception is None and not isinstance(
                            close_exc, Exception,
                        ):
                            fatal_exception = close_exc
                self._disabled = self._disabled or result is None
                self._closed = True
                self._final_result = result
                self._finalizing = False
                self._finalized.set()
        if fatal_exception is not None:
            raise fatal_exception
        return result

    def _finalize_locked(
        self,
        status: str,
        error: Optional[str],
        output_path: Optional[Path],
    ) -> Optional[Path]:
        if output_path is not None:
            self._stats["mp3_size_bytes"] = _file_size(output_path)
        stats = copy.deepcopy(self._stats)
        times = stats["tts_times"]
        audio_duration = _positive_float(stats["audio_duration_seconds"])
        tts_wall = stats["tts_wall_seconds"]
        stages = stats["stage_durations"]
        terminal = self._base_event("run_terminal")
        terminal.update(self._sanitize_fields({"status": status, "error": error}))
        summary = self._base_event("run_summary")
        summary.update({
            "terminal_status": status,
            "wall_seconds": max(0.0, self._perf_counter() - self._started),
            "total_chapters": stats["total_chapters"],
            "tts_segments": stats["tts_segments"],
            "characters": stats["characters"],
            "tts_wall_seconds": tts_wall,
            "tts_segment_mean_seconds": (sum(times) / len(times)) if times else None,
            "tts_segment_min_seconds": min(times) if times else None,
            "tts_segment_max_seconds": max(times) if times else None,
            "audio_duration_seconds": audio_duration,
            "realtime_factor": _safe_div(tts_wall, audio_duration),
            "calibre_seconds": stages.get("calibre_conversion"),
            "parsing_seconds": stages.get("fb2_parsing"),
            "splitting_seconds": stages.get("sentence_splitting"),
            "chapter_assembly_seconds": stages.get("chapter_assembly"),
            "final_assembly_seconds": stages.get("final_assembly"),
            "mp3_size_bytes": stats["mp3_size_bytes"],
            "diagnostic_errors": self._diagnostic_errors,
            "diagnostics_truncated": self._truncated,
        })
        terminal_bytes = self._encode_line(_bounded_payload(terminal))
        summary_bytes = self._encode_line(summary)
        pair_size = len(terminal_bytes) + len(summary_bytes)
        if pair_size > self.limits.terminal_reserve_bytes:
            raise ValueError("terminal event pair exceeds reserved space")
        if self._bytes_written + pair_size > self.limits.max_file_bytes:
            raise ValueError("terminal event pair exceeds file size limit")
        self._write_encoded(terminal_bytes)
        self._write_encoded(summary_bytes)
        if self._stream is not None:
            self._stream.flush()
            os.fsync(self._stream.fileno())
        if not self._disabled and self.part_path.exists():
            self._replace(self.part_path, self.final_path)
        if self._stream is not None:
            self._stream.close()
        self._stream = None
        self.rotate()
        return self.final_path if self.final_path.exists() else None

    def _recover_incomplete(self) -> None:
        for path in self.logs_dir.glob(f"{LOG_PREFIX}*.jsonl.part"):
            if not _is_owned_part(path.name):
                continue
            if fcntl is None:
                continue
            recovery_stream = None
            try:
                recovery_stream = path.open("r+", encoding="utf-8")
                fcntl.flock(
                    recovery_stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB,
                )
            except (BlockingIOError, OSError):
                if recovery_stream is not None:
                    recovery_stream.close()
                continue
            base = path.name.removesuffix(".jsonl.part")
            target = path.with_name(base + ".incomplete.jsonl")
            counter = 1
            while target.exists():
                target = path.with_name(
                    base + f".{counter}.incomplete.jsonl"
                )
                counter += 1
            try:
                self._replace(path, target)
            finally:
                recovery_stream.close()

    def rotate(self) -> None:
        try:
            candidates = [
                path for path in self.logs_dir.iterdir()
                if path.is_file()
                and _is_owned_final(path.name)
                and path != self.part_path
            ]
            candidates.sort(key=lambda path: (path.stat().st_mtime_ns, path.name))
            total = sum(path.stat().st_size for path in candidates)
            while candidates and (
                len(candidates) > self.limits.max_files
                or total > self.limits.max_total_bytes
            ):
                oldest = candidates.pop(0)
                size = oldest.stat().st_size
                oldest.unlink()
                total -= size
        except Exception as exc:
            self.diagnostic_error("rotation", exc)

    def _run_start_fields(
        self, book_path: Path, run_info: Mapping[str, Any],
    ) -> dict[str, Any]:
        torch_info = _torch_info()
        gpu_model = _gpu_model()
        source = Path(book_path)
        return {
            "app_version": _package_version(),
            "python_version": platform.python_version(),
            "os": platform.system(),
            "kernel": platform.release(),
            "architecture": platform.machine(),
            "cpu_model": _cpu_model(),
            "physical_cpu_count": _physical_cpu_count(),
            "logical_cpu_count": os.cpu_count(),
            "ram_total_bytes": _read_meminfo().get("total"),
            "backend": run_info.get("backend"),
            "voice": run_info.get("voice"),
            "language": run_info.get("language"),
            "device": run_info.get("device"),
            **torch_info,
            "gpu_model": gpu_model,
            "source_format": source.suffix.lower(),
            "source_size_bytes": _file_size(source),
            "source_filename": source.name,
            "calibre_import": source.suffix.lower() != ".fb2",
            "system_sample_interval_seconds": self.sample_interval,
        }


def _safe_div(numerator: Any, denominator: Any) -> Optional[float]:
    try:
        if numerator is None or denominator is None or float(denominator) <= 0:
            return None
        return float(numerator) / float(denominator)
    except (TypeError, ValueError, ZeroDivisionError):
        return None


def _is_owned_part(name: str) -> bool:
    return name.startswith(LOG_PREFIX) and name.endswith(".jsonl.part")


def _is_owned_final(name: str) -> bool:
    if not name.startswith(LOG_PREFIX):
        return False
    return (
        name.endswith(".jsonl") and not name.endswith(".jsonl.part")
    )


def _sanitize_field_value(
    key: str,
    value: Any,
    paths: tuple[str, ...],
    force_sensitive: bool = False,
) -> Any:
    if _normalize_field_name(key) in SECRET_FIELD_NAMES:
        return "<redacted>"
    sensitive = force_sensitive or key.lower() in ERROR_LIKE_FIELDS
    if sensitive and isinstance(value, str):
        return _sanitize_error(value, paths)
    if isinstance(value, Mapping):
        sanitized = {}
        for nested_key, nested_value in value.items():
            key_text = str(nested_key)
            sanitized[key_text] = _sanitize_field_value(
                key_text, nested_value, paths, sensitive,
            )
        return sanitized
    if isinstance(value, (list, tuple)):
        return [
            _sanitize_field_value(key, item, paths, sensitive)
            for item in value
        ]
    return value


def _normalize_field_name(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", str(value).lower())


def _sanitize_error(value: str, paths: tuple[str, ...] = ()) -> str:
    # Error fields are capped in the journal; cap before regex processing too,
    # so an exceptionally large exception cannot make sanitization quadratic.
    compact = " ".join(str(value)[:8192].split())
    compact = re.sub(
        r"(?i)([a-z][a-z0-9+.-]*://)[^/@\s:]+:[^@\s]+@",
        r"\1<redacted>@",
        compact,
    )
    compact = re.sub(
        r"(?i)\bBearer\s+(?:\"[^\"]*\"|'[^']*'|[^\s,;]+)",
        "Bearer <redacted>",
        compact,
    )
    compact = re.sub(
        r"(?i)\b(api[_-]?key|token|password)\b\s*[=:]\s*"
        r"(?:\"[^\"]*\"|'[^']*'|[^,;]+)",
        lambda match: f"{match.group(1)}=<redacted>",
        compact,
    )
    compact = re.sub(r"\bsk-[A-Za-z0-9_-]{8,}\b", "<redacted>", compact)
    for path in sorted((path for path in paths if path), key=len, reverse=True):
        marker = f"<path:{Path(path).name}>" if Path(path).suffix else "<path>"
        compact = compact.replace(path, marker)
    return compact[:300]


def _bounded_payload(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Bound attacker/user-controlled values before exact size accounting."""
    bounded: dict[str, Any] = {}
    truncated_fields = []
    for key, value in payload.items():
        if isinstance(value, str) and len(value) > 2048:
            bounded[key] = value[:2048]
            truncated_fields.append(key)
        elif isinstance(value, (list, tuple)) and len(value) > 1024:
            bounded[key] = list(value[:1024])
            truncated_fields.append(key)
        else:
            bounded[key] = value
    if truncated_fields:
        bounded["truncated_fields"] = truncated_fields
    return bounded


def _positive_float(value: Any) -> Optional[float]:
    try:
        number = float(value)
        return number if number > 0 and math.isfinite(number) else None
    except (TypeError, ValueError):
        return None


def _number(value: Any) -> Optional[float]:
    try:
        number = float(value)
        return number if math.isfinite(number) else None
    except (TypeError, ValueError):
        return None


def _mib_to_bytes(value: Any) -> Optional[int]:
    number = _number(value)
    return int(number * 1024 * 1024) if number is not None else None


def _file_size(path: Optional[Path]) -> Optional[int]:
    try:
        return Path(path).stat().st_size if path is not None else None
    except OSError:
        return None


def _package_version() -> Optional[str]:
    try:
        return importlib.metadata.version(APP_NAME)
    except importlib.metadata.PackageNotFoundError:
        return None


def _read_meminfo() -> dict[str, Optional[int]]:
    result = {"total": None, "available": None, "used": None}
    try:
        values = {}
        for line in Path("/proc/meminfo").read_text().splitlines():
            key, raw = line.split(":", 1)
            values[key] = int(raw.strip().split()[0]) * 1024
        result["total"] = values.get("MemTotal")
        result["available"] = values.get("MemAvailable")
        if result["total"] is not None and result["available"] is not None:
            result["used"] = result["total"] - result["available"]
    except Exception:
        pass
    return result


def _cpu_model() -> Optional[str]:
    try:
        for line in Path("/proc/cpuinfo").read_text().splitlines():
            if line.lower().startswith("model name"):
                return line.split(":", 1)[1].strip()
    except Exception:
        pass
    return platform.processor() or None


def _physical_cpu_count() -> Optional[int]:
    try:
        physical = set()
        current: dict[str, str] = {}
        for line in Path("/proc/cpuinfo").read_text().splitlines() + [""]:
            if not line:
                if "physical id" in current and "core id" in current:
                    physical.add((current["physical id"], current["core id"]))
                current = {}
            elif ":" in line:
                key, value = line.split(":", 1)
                current[key.strip()] = value.strip()
        return len(physical) or None
    except Exception:
        return None


def _read_cpu_times() -> Optional[tuple[int, int, list[tuple[int, int]]]]:
    try:
        rows = []
        for line in Path("/proc/stat").read_text().splitlines():
            if not re.match(r"^cpu(?:\d+)?\s", line):
                continue
            values = [int(value) for value in line.split()[1:]]
            idle = values[3] + (values[4] if len(values) > 4 else 0)
            rows.append((sum(values), idle))
        return rows[0][0], rows[0][1], rows[1:]
    except Exception:
        return None


def _cpu_delta_percent(old: tuple[int, int], new: tuple[int, int]) -> float:
    total = new[0] - old[0]
    idle = new[1] - old[1]
    return max(0.0, min(100.0, (1.0 - idle / total) * 100.0)) if total else 0.0


def _read_process_cpu() -> Optional[tuple[float, int]]:
    try:
        fields = Path("/proc/self/stat").read_text().split()
        ticks = int(fields[13]) + int(fields[14])
        return time.perf_counter(), ticks
    except Exception:
        return None


def _read_process_status() -> dict[str, Optional[int]]:
    result = {"rss": None, "threads": None}
    try:
        for line in Path("/proc/self/status").read_text().splitlines():
            if line.startswith("VmRSS:"):
                result["rss"] = int(line.split()[1]) * 1024
            elif line.startswith("Threads:"):
                result["threads"] = int(line.split()[1])
    except Exception:
        pass
    return result


def _cpu_frequency_mhz() -> Optional[float]:
    try:
        values = []
        for path in Path("/sys/devices/system/cpu").glob("cpu*/cpufreq/scaling_cur_freq"):
            values.append(float(path.read_text().strip()) / 1000.0)
        return sum(values) / len(values) if values else None
    except Exception:
        return None


def _cpu_temperature_c() -> Optional[float]:
    try:
        values = []
        for path in Path("/sys/class/thermal").glob("thermal_zone*/temp"):
            value = float(path.read_text().strip())
            values.append(value / 1000.0 if value > 1000 else value)
        return max(values) if values else None
    except Exception:
        return None


def _gpu_model() -> Optional[str]:
    executable = shutil.which("nvidia-smi")
    if executable is None:
        return None
    try:
        result = subprocess.run(
            [executable, "--query-gpu=name", "--format=csv,noheader"],
            capture_output=True, text=True, timeout=2.0, check=False,
        )
        return result.stdout.splitlines()[0].strip() if result.returncode == 0 else None
    except Exception:
        return None


def _torch_info() -> dict[str, Any]:
    result = {
        "pytorch_version": None,
        "cuda_build_version": None,
        "cuda_available": None,
    }
    try:
        result["pytorch_version"] = importlib.metadata.version("torch")
    except importlib.metadata.PackageNotFoundError:
        return result
    try:
        import torch
        result["cuda_build_version"] = torch.version.cuda
        result["cuda_available"] = bool(torch.cuda.is_available())
    except Exception:
        pass
    return result
