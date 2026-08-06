"""
Модуль безопасного управляемого переключения моделей Silero TTS (ModelSwitcher).

Осуществляет валидацию метаданных/хешей, предварительный изолированный smoke-test
обязательных русских голосов (eugene, xenia), атомарное переключение active и поддержку отката (rollback).
"""

from __future__ import annotations

import argparse
import json
import logging
import math
import os
import sys
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from src.core.model_inspector import _calculate_sha256, _format_size
from src.core.model_manager import ModelManager, ModelMetadata

logger = logging.getLogger(__name__)

DEFAULT_SMOKE_TEST_PHRASE = "Это проверка новой речевой модели."
REQUIRED_RUSSIAN_SPEAKERS = ["eugene", "xenia"]
DEFAULT_SMOKE_TEST_TIMEOUT = 15.0


@dataclass
class SwitchRequest:
    """Параметры запроса на активацию модели."""

    model_id: str
    voice: Optional[str] = None
    force: bool = False
    skip_smoke_test: bool = False


@dataclass
class SpeakerTestResult:
    """Результат проверки отдельного диктора (speaker)."""

    speaker: str
    status: str  # "success" | "missing" | "synth_failed" | "empty_audio" | "nan_audio" | "timeout"
    sample_rate: Optional[int] = None
    audio_samples: int = 0
    duration_seconds: float = 0.0
    synthesis_seconds: float = 0.0
    message: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Преобразовать в словарь."""
        return asdict(self)


@dataclass
class SmokeTestResult:
    """Результат выполнения комплексного smoke-test модели."""

    success: bool
    status: str
    # Статусы: "success" | "load_failed" | "synth_failed" | "timeout" | "missing_required_speakers" | "error"

    model_id: str
    available_speakers: List[str]
    tested_speakers: List[str]
    missing_required_speakers: List[str]
    failed_speakers: List[str]
    speaker_results: Dict[str, SpeakerTestResult]
    load_time_sec: float = 0.0
    message: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Преобразовать в словарь."""
        d = {
            "success": self.success,
            "status": self.status,
            "model_id": self.model_id,
            "available_speakers": self.available_speakers,
            "tested_speakers": self.tested_speakers,
            "missing_required_speakers": self.missing_required_speakers,
            "failed_speakers": self.failed_speakers,
            "speaker_results": {
                k: v.to_dict() if hasattr(v, "to_dict") else v
                for k, v in self.speaker_results.items()
            },
            "load_time_sec": self.load_time_sec,
            "message": self.message,
        }
        return d


@dataclass
class SwitchResult:
    """Результат выполнения переключения активной модели."""

    success: bool
    status: str
    # Статусы: "success" | "already_active" | "model_not_found" | "metadata_invalid" |
    #          "model_file_missing" | "size_mismatch" | "hash_mismatch" | "smoke_test_failed" |
    #          "voice_missing" | "activation_conflict" | "rollback_unavailable" |
    #          "rollback_success" | "write_error" | "error" | "ready"

    model_id: Optional[str] = None
    previous_model_id: Optional[str] = None
    installed_path: Optional[str] = None
    active: bool = False
    smoke_test: Optional[SmokeTestResult] = None
    message: str = ""
    dry_run: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Преобразовать в словарь."""
        d = asdict(self)
        if self.smoke_test and hasattr(self.smoke_test, "to_dict"):
            d["smoke_test"] = self.smoke_test.to_dict()
        return d


@dataclass
class RollbackResult:
    """Результат выполнения операции rollback."""

    success: bool
    status: str
    restored_model_id: Optional[str] = None
    previous_model_id: Optional[str] = None
    smoke_test: Optional[SmokeTestResult] = None
    message: str = ""
    dry_run: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Преобразовать в словарь."""
        d = asdict(self)
        if self.smoke_test and hasattr(self.smoke_test, "to_dict"):
            d["smoke_test"] = self.smoke_test.to_dict()
        return d


class ModelSwitcher:
    """Класс управления переключением активной модели Silero TTS."""

    def __init__(self, model_manager: Optional[ModelManager] = None):
        self.model_manager = model_manager or ModelManager()
        self.models_dir = self.model_manager.get_models_dir()
        self.state_file = self.models_dir / "state.json"

        # История переключений
        state_dir = Path.home() / ".local" / "share" / "fb2-silero-audiobook"
        state_dir.mkdir(parents=True, exist_ok=True)
        self.history_log_file = state_dir / "model_switches.jsonl"

    def get_state(self) -> Dict[str, Any]:
        """Прочитать единый файл состояния state.json."""
        if not self.state_file.is_file():
            return {}
        try:
            with self.state_file.open("r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, dict) else {}
        except Exception as exc:
            logger.warning("Ошибка чтения state.json: %s", exc)
            return {}

    def _write_state_atomic(self, active_model_id: str, previous_model_id: Optional[str]) -> bool:
        """Записать единый файл состояния state.json атомарно."""
        now_iso = datetime.now(timezone.utc).isoformat()
        state_data = {
            "active_model_id": active_model_id,
            "previous_model_id": previous_model_id,
            "switched_at": now_iso,
        }

        temp_state = self.models_dir / "state.json.tmp"
        try:
            with temp_state.open("w", encoding="utf-8") as f:
                json.dump(state_data, f, indent=2, ensure_ascii=False)
            temp_state.replace(self.state_file)
            return True
        except Exception as exc:
            logger.error("Ошибка атомарной записи state.json: %s", exc)
            if temp_state.exists():
                try:
                    temp_state.unlink()
                except Exception:
                    pass
            return False

    def log_switch_event(
        self,
        action: str,
        from_model_id: Optional[str],
        to_model_id: Optional[str],
        status: str,
        message: str = "",
        smoke_test: Optional[SmokeTestResult] = None,
    ):
        """Записать событие переключения в журнал model_switches.jsonl."""
        try:
            event = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "action": action,
                "from_model_id": from_model_id,
                "to_model_id": to_model_id,
                "status": status,
                "message": message,
                "smoke_test": smoke_test.to_dict() if smoke_test else None,
            }
            with self.history_log_file.open("a", encoding="utf-8") as f:
                f.write(json.dumps(event, ensure_ascii=False) + "\n")
        except Exception as exc:
            logger.warning("Не удалось записать событие в журнал переключений: %s", exc)

    def validate_model_for_switch(self, model_id: str) -> Tuple[bool, str, Optional[ModelMetadata]]:
        """Проверка модели на возможность использования до переключения."""
        model_info = self.model_manager.get_model_info(model_id)
        if not model_info:
            return False, "model_not_found", None

        if not model_info.valid:
            return False, "metadata_invalid", model_info

        if not model_info.path:
            return False, "model_file_missing", model_info

        target_file = Path(model_info.path)
        if not target_file.is_file():
            return False, "model_file_missing", model_info

        # Защита от Path Traversal и Symlink за пределы root
        try:
            resolved_target = target_file.resolve()
            resolved_models_dir = self.models_dir.resolve()
            if not str(resolved_target).startswith(str(resolved_models_dir)) and not model_info.is_legacy:
                return False, "path_traversal", model_info
        except Exception:
            return False, "path_traversal", model_info

        # Запрет использования временных и незавершенных файлов .part / .tmp
        file_str = str(target_file)
        if ".part" in file_str or ".tmp" in file_str or ".tmp_downloads" in file_str:
            return False, "invalid_file_type", model_info

        # Проверка размера файла
        stat = target_file.stat()
        if model_info.size_bytes and stat.st_size != model_info.size_bytes:
            return False, "size_mismatch", model_info

        # Проверка SHA-256 хеша
        if model_info.sha256:
            calc_sha = _calculate_sha256(target_file)
            if calc_sha.lower() != model_info.sha256.lower():
                return False, "hash_mismatch", model_info

        return True, "valid", model_info

    def run_smoke_test(
        self,
        model_id: str,
        phrase: str = DEFAULT_SMOKE_TEST_PHRASE,
        speakers_to_test: Optional[List[str]] = None,
        all_speakers: bool = False,
        timeout: float = DEFAULT_SMOKE_TEST_TIMEOUT,
    ) -> SmokeTestResult:
        """Выполнить изолированный smoke-test синтеза речи для обязательных и дополнительных голосов."""
        valid, err_status, model_info = self.validate_model_for_switch(model_id)
        if not valid:
            return SmokeTestResult(
                success=False,
                status=err_status,
                model_id=model_id,
                available_speakers=[],
                tested_speakers=[],
                missing_required_speakers=[],
                failed_speakers=[],
                speaker_results={},
                message=f"Валидация перед smoke-test не пройдена: {err_status}",
            )

        start_load = time.monotonic()
        try:
            # Изолированная загрузка модели ОДИН РАЗ
            from torch.package import PackageImporter
            import torch

            importer = PackageImporter(model_info.path)
            tts_model = importer.load_pickle("tts_models", "model")
            load_time = time.monotonic() - start_load

            available_speakers = list(getattr(tts_model, "speakers", []))
            sample_rates = getattr(tts_model, "sample_rates", [24000])
            target_sr = sample_rates[-1] if sample_rates else 24000

            # Определяем список дикторов для тестирования
            if all_speakers:
                target_speakers = list(available_speakers)
            elif speakers_to_test:
                target_speakers = list(speakers_to_test)
            else:
                target_speakers = list(REQUIRED_RUSSIAN_SPEAKERS)

            tested_speakers = []
            missing_required_speakers = []
            failed_speakers = []
            speaker_results: Dict[str, SpeakerTestResult] = {}

            import numpy as np

            for speaker in target_speakers:
                tested_speakers.append(speaker)

                # Проверка наличия голоса в модели
                if speaker not in available_speakers:
                    if speaker in REQUIRED_RUSSIAN_SPEAKERS:
                        missing_required_speakers.append(speaker)
                    failed_speakers.append(speaker)

                    speaker_results[speaker] = SpeakerTestResult(
                        speaker=speaker,
                        status="missing",
                        message=f"Голос '{speaker}' отсутствует в модели.",
                    )
                    continue

                # Тестирование синтеза отдельного голоса
                start_synth = time.monotonic()
                try:
                    audio_tensor = tts_model.apply_tts(text=phrase, speaker=speaker, sample_rate=target_sr)
                    synth_time = time.monotonic() - start_synth

                    if audio_tensor is None or (hasattr(audio_tensor, "__len__") and len(audio_tensor) == 0):
                        failed_speakers.append(speaker)
                        speaker_results[speaker] = SpeakerTestResult(
                            speaker=speaker,
                            status="empty_audio",
                            sample_rate=target_sr,
                            synthesis_seconds=round(synth_time, 3),
                            message="Модель вернула пустой аудио-тензор.",
                        )
                        continue

                    if hasattr(audio_tensor, "detach"):
                        samples = audio_tensor.detach().cpu().numpy()
                    elif hasattr(audio_tensor, "tolist"):
                        samples = audio_tensor.tolist()
                    else:
                        samples = audio_tensor

                    samples_arr = np.array(samples, dtype=float)
                    num_samples = len(samples_arr)
                    duration_sec = num_samples / float(target_sr)

                    if duration_sec < 0.2:
                        failed_speakers.append(speaker)
                        speaker_results[speaker] = SpeakerTestResult(
                            speaker=speaker,
                            status="empty_audio",
                            sample_rate=target_sr,
                            audio_samples=num_samples,
                            duration_seconds=round(duration_sec, 2),
                            synthesis_seconds=round(synth_time, 3),
                            message=f"Длительность аудио слишком мала ({duration_sec:.2f} сек).",
                        )
                        continue

                    if np.isnan(samples_arr).any() or np.isinf(samples_arr).any():
                        failed_speakers.append(speaker)
                        speaker_results[speaker] = SpeakerTestResult(
                            speaker=speaker,
                            status="nan_audio",
                            sample_rate=target_sr,
                            audio_samples=num_samples,
                            duration_seconds=round(duration_sec, 2),
                            synthesis_seconds=round(synth_time, 3),
                            message="Аудио содержит нечисловые значения (NaN / Inf).",
                        )
                        continue

                    max_amp = float(np.max(np.abs(samples_arr)))
                    if max_amp < 0.0001:
                        failed_speakers.append(speaker)
                        speaker_results[speaker] = SpeakerTestResult(
                            speaker=speaker,
                            status="empty_audio",
                            sample_rate=target_sr,
                            audio_samples=num_samples,
                            duration_seconds=round(duration_sec, 2),
                            synthesis_seconds=round(synth_time, 3),
                            message="Аудиосигнал полностью молчаливый (тишина).",
                        )
                        continue

                    # Успешная проверка данного голоса
                    speaker_results[speaker] = SpeakerTestResult(
                        speaker=speaker,
                        status="success",
                        sample_rate=target_sr,
                        audio_samples=num_samples,
                        duration_seconds=round(duration_sec, 2),
                        synthesis_seconds=round(synth_time, 3),
                        message="Голос успешно проверен.",
                    )

                except Exception as exc:
                    logger.warning("Ошибка синтеза для голоса %s: %s", speaker, exc)
                    failed_speakers.append(speaker)
                    speaker_results[speaker] = SpeakerTestResult(
                        speaker=speaker,
                        status="synth_failed",
                        message=f"Исключение при синтезе голоса: {exc}",
                    )

            # Оценка общего допуска модели: ВСЕ обязательные голосы (eugene, xenia) должны пройти!
            overall_success = True
            for req in REQUIRED_RUSSIAN_SPEAKERS:
                if req not in speaker_results or speaker_results[req].status != "success":
                    overall_success = False
                    if req not in missing_required_speakers and req in failed_speakers:
                        pass

            if overall_success:
                status = "success"
                msg = f"Smoke-test прошел успешно для обязательных голосов ({', '.join(REQUIRED_RUSSIAN_SPEAKERS)})."
            else:
                if missing_required_speakers:
                    status = "missing_required_speakers"
                    msg = f"Отсутствуют обязательные голоса: {', '.join(missing_required_speakers)}."
                else:
                    status = "synth_failed"
                    msg = f"Ошибки синтеза обязательных голосов: {', '.join(failed_speakers)}."

            return SmokeTestResult(
                success=overall_success,
                status=status,
                model_id=model_id,
                available_speakers=available_speakers,
                tested_speakers=tested_speakers,
                missing_required_speakers=missing_required_speakers,
                failed_speakers=failed_speakers,
                speaker_results=speaker_results,
                load_time_sec=round(load_time, 3),
                message=msg,
            )

        except Exception as exc:
            logger.warning("Ошибка загрузки модели %s для smoke-test: %s", model_id, exc)
            return SmokeTestResult(
                success=False,
                status="load_failed",
                model_id=model_id,
                available_speakers=[],
                tested_speakers=[],
                missing_required_speakers=REQUIRED_RUSSIAN_SPEAKERS,
                failed_speakers=REQUIRED_RUSSIAN_SPEAKERS,
                speaker_results={},
                load_time_sec=round(time.monotonic() - start_load, 3),
                message=f"Исключение при загрузке модели: {exc}",
            )

    def activate_model(
        self,
        model_id: str,
        voice: Optional[str] = None,
        dry_run: bool = False,
        force: bool = False,
        skip_smoke_test: bool = False,
    ) -> SwitchResult:
        """Активация модели с обязательным предварительным smoke-test всех обязательных голосов."""
        active_model = self.model_manager.get_active_model()
        current_active_id = active_model.model_id if active_model else None

        # 1. Валидация целевой модели
        valid, err_status, model_info = self.validate_model_for_switch(model_id)
        if not valid:
            self.log_switch_event(
                action="activate",
                from_model_id=current_active_id,
                to_model_id=model_id,
                status=err_status,
                message=f"Валидация не пройдена ({err_status})",
            )
            return SwitchResult(
                success=False,
                status=err_status,
                model_id=model_id,
                previous_model_id=current_active_id,
                active=False,
                message=f"Модель '{model_id}' не прошла валидацию ({err_status}).",
                dry_run=dry_run,
            )

        if current_active_id == model_id and not force:
            return SwitchResult(
                success=True,
                status="already_active",
                model_id=model_id,
                previous_model_id=current_active_id,
                installed_path=model_info.path if model_info else None,
                active=True,
                message=f"Модель '{model_id}' уже является активной.",
                dry_run=dry_run,
            )

        # 2. Изолированный smoke-test (eugene + xenia)
        smoke_res = None
        if not skip_smoke_test:
            smoke_res = self.run_smoke_test(model_id)
            if not smoke_res.success and not force:
                self.log_switch_event(
                    action="activate",
                    from_model_id=current_active_id,
                    to_model_id=model_id,
                    status="smoke_test_failed",
                    message=smoke_res.message,
                    smoke_test=smoke_res,
                )
                return SwitchResult(
                    success=False,
                    status="smoke_test_failed",
                    model_id=model_id,
                    previous_model_id=current_active_id,
                    installed_path=model_info.path,
                    active=False,
                    smoke_test=smoke_res,
                    message=f"Smoke-test модели '{model_id}' завершился ошибкой: {smoke_res.message}",
                    dry_run=dry_run,
                )

        # 3. Проверка выбранного пользователем голоса (не менять выбранный голос молча!)
        if voice and smoke_res and smoke_res.available_speakers:
            if voice not in smoke_res.available_speakers and not force:
                return SwitchResult(
                    success=False,
                    status="voice_missing",
                    model_id=model_id,
                    previous_model_id=current_active_id,
                    installed_path=model_info.path,
                    active=False,
                    smoke_test=smoke_res,
                    message=f"Выбранный пользователем голос '{voice}' отсутствует в новой модели '{model_id}'. Автоматическая подмена запрещена.",
                    dry_run=dry_run,
                )

        # 4. Dry-run режим
        if dry_run:
            return SwitchResult(
                success=True,
                status="ready",
                model_id=model_id,
                previous_model_id=current_active_id,
                installed_path=model_info.path,
                active=False,
                smoke_test=smoke_res,
                message="План активации проверен. Фактическое переключение будет выполнено при запуске с --yes.",
                dry_run=True,
            )

        # 5. Атомарное переключение метаданных
        if active_model and active_model.path and not active_model.is_legacy:
            try:
                old_dir = Path(active_model.path).parent
                old_meta_file = old_dir / "metadata.json"
                if old_meta_file.is_file():
                    with old_meta_file.open("r", encoding="utf-8") as f:
                        old_meta_data = json.load(f)
                    old_meta_data["active"] = False
                    old_tmp = old_dir / "metadata.json.tmp"
                    with old_tmp.open("w", encoding="utf-8") as f:
                        json.dump(old_meta_data, f, indent=2, ensure_ascii=False)
                    old_tmp.replace(old_meta_file)
            except Exception as exc:
                logger.warning("Ошибка обнуления флага active у старой модели: %s", exc)

        new_dir = Path(model_info.path).parent
        new_meta_file = new_dir / "metadata.json"
        try:
            new_meta_data = {}
            if new_meta_file.is_file():
                with new_meta_file.open("r", encoding="utf-8") as f:
                    new_meta_data = json.load(f)
            new_meta_data["model_id"] = model_id
            new_meta_data["active"] = True
            new_tmp = new_dir / "metadata.json.tmp"
            with new_tmp.open("w", encoding="utf-8") as f:
                json.dump(new_meta_data, f, indent=2, ensure_ascii=False)
            new_tmp.replace(new_meta_file)
        except Exception as exc:
            logger.error("Ошибка установки флага active у новой модели: %s", exc)
            return SwitchResult(
                success=False,
                status="write_error",
                model_id=model_id,
                previous_model_id=current_active_id,
                message=f"Не удалось обновить metadata.json новой модели: {exc}",
            )

        # Обновляем единый файл состояния state.json
        state_ok = self._write_state_atomic(active_model_id=model_id, previous_model_id=current_active_id)
        if not state_ok:
            logger.warning("state.json не записан, но metadata.json моделей обновлены.")

        # Запись в журнал событий
        self.log_switch_event(
            action="activate",
            from_model_id=current_active_id,
            to_model_id=model_id,
            status="success",
            message=f"Модель {model_id} успешно активирована.",
            smoke_test=smoke_res,
        )

        return SwitchResult(
            success=True,
            status="success",
            model_id=model_id,
            previous_model_id=current_active_id,
            installed_path=model_info.path,
            active=True,
            smoke_test=smoke_res,
            message=f"Модель '{model_id}' успешно активирована.",
        )

    def rollback_active_model(self, dry_run: bool = False) -> RollbackResult:
        """Откат к предыдущей заведомо рабочей модели."""
        state = self.get_state()
        current_active = self.model_manager.get_active_model()
        current_id = current_active.model_id if current_active else None

        previous_id = state.get("previous_model_id")
        if not previous_id:
            if self.history_log_file.is_file():
                try:
                    lines = self.history_log_file.read_text(encoding="utf-8").strip().splitlines()
                    for line in reversed(lines):
                        if not line:
                            continue
                        ev = json.loads(line)
                        if ev.get("action") == "activate" and ev.get("status") == "success":
                            if ev.get("from_model_id") and ev.get("from_model_id") != current_id:
                                previous_id = ev.get("from_model_id")
                                break
                except Exception as exc:
                    logger.debug("Ошибка чтения журнала переключений при rollback: %s", exc)

        if not previous_id:
            return RollbackResult(
                success=False,
                status="rollback_unavailable",
                previous_model_id=None,
                message="Предыдущая рабочая модель не найдена в истории или state.json.",
                dry_run=dry_run,
            )

        switch_res = self.activate_model(
            model_id=previous_id,
            dry_run=dry_run,
            force=True,
        )

        if switch_res.success:
            return RollbackResult(
                success=True,
                status="rollback_success" if not dry_run else "ready",
                restored_model_id=previous_id,
                previous_model_id=current_id,
                smoke_test=switch_res.smoke_test,
                message=f"Успешный откат на предыдущую модель '{previous_id}'.",
                dry_run=dry_run,
            )
        else:
            final_status = "rollback_unavailable" if switch_res.status in ("model_not_found", "model_file_missing") else switch_res.status
            return RollbackResult(
                success=False,
                status=final_status,
                restored_model_id=previous_id,
                previous_model_id=current_id,
                smoke_test=switch_res.smoke_test,
                message=f"Не удалось выполнить откат на '{previous_id}': {switch_res.message}",
                dry_run=dry_run,
            )
