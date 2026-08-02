"""Установка пользовательского Desktop Entry для существующего клона."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Mapping, Optional, Sequence


DESKTOP_FILENAME = "fb2-silero-audiobook.desktop"
MANAGED_KEY = "X-FB2-Silero-Audiobook-Managed"
MANAGED_VALUE = "true"
DEFAULT_ICON = "audio-x-generic"


class DesktopInstallError(RuntimeError):
    """Безопасная установка или удаление ярлыка невозможны."""


@dataclass(frozen=True)
class InstallResult:
    entry_path: Path
    calibre_available: bool
    warnings: tuple[str, ...] = ()


@dataclass(frozen=True)
class UninstallResult:
    entry_path: Path
    removed: bool
    warnings: tuple[str, ...] = ()


def project_root() -> Path:
    """Определить корень проекта независимо от текущего каталога."""
    return Path(__file__).resolve().parents[1]


def applications_directory(
    env: Optional[Mapping[str, str]] = None,
    home: Optional[Path] = None,
) -> Path:
    """Вернуть пользовательский XDG-каталог Desktop Entry."""
    environment = os.environ if env is None else env
    xdg_data_home = environment.get("XDG_DATA_HOME", "").strip()
    if xdg_data_home:
        return Path(xdg_data_home).expanduser() / "applications"
    home_directory = Path.home() if home is None else Path(home)
    return home_directory / ".local" / "share" / "applications"


def _escape_exec_argument(value: Path | str) -> str:
    """Экранировать один аргумент поля Exec по Desktop Entry Specification."""
    escaped = []
    for character in str(value):
        if character == "%":
            escaped.append("%%")
        elif character in {'\\', '"', '`', '$'}:
            escaped.append(f"\\{character}")
        else:
            escaped.append(character)
    return f'"{"".join(escaped)}"'


def _escape_desktop_string(value: Path | str) -> str:
    """Экранировать обычное строковое значение Desktop Entry."""
    text = str(value)
    text = text.replace("\\", "\\\\")
    text = text.replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t")
    while text.startswith(" "):
        text = "\\s" + text[1:]
    while text.endswith(" "):
        text = text[:-1] + "\\s"
    return text


def build_desktop_entry(root: Path, icon: str = DEFAULT_ICON) -> str:
    """Сформировать Desktop Entry для конкретного абсолютного корня."""
    root = Path(root).resolve()
    python_path = root / ".venv" / "bin" / "python"
    gui_path = root / "audiobook_gui.py"
    exec_value = " ".join((
        _escape_exec_argument(python_path),
        _escape_exec_argument(gui_path),
    ))
    return "\n".join((
        "[Desktop Entry]",
        "Type=Application",
        "Name=Генератор аудиокниг Silero",
        "Comment=Локальная озвучка русских электронных книг",
        f"Exec={exec_value}",
        f"Path={_escape_desktop_string(root)}",
        f"Icon={_escape_desktop_string(icon)}",
        "Terminal=false",
        "Categories=AudioVideo;Audio;Utility;",
        "Keywords=аудиокнига;озвучка;книги;FB2;EPUB;Silero;TTS;audiobook;",
        "StartupNotify=true",
        f"{MANAGED_KEY}={MANAGED_VALUE}",
        "",
    ))


def is_managed_entry(path: Path) -> bool:
    """Проверить точный управляющий маркер без доверия имени файла."""
    try:
        contents = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise DesktopInstallError(
            f"Не удалось безопасно прочитать существующий ярлык: {path}: {exc}"
        ) from exc
    for line in contents.splitlines():
        key, separator, value = line.partition("=")
        if separator and key.strip() == MANAGED_KEY:
            return value.strip().lower() == MANAGED_VALUE
    return False


def _check_project_requirements(
    root: Path,
    which: Callable[[str], Optional[str]],
) -> bool:
    python_path = root / ".venv" / "bin" / "python"
    gui_path = root / "audiobook_gui.py"
    if not python_path.is_file() or not os.access(python_path, os.X_OK):
        raise DesktopInstallError(
            f"Не найден проектный Python: {python_path}. "
            "Сначала подготовьте существующее окружение .venv."
        )
    if not gui_path.is_file():
        raise DesktopInstallError(f"Не найден GUI приложения: {gui_path}")
    for command in ("ffmpeg", "ffprobe"):
        if which(command) is None:
            raise DesktopInstallError(
                f"Не найден обязательный системный инструмент: {command}"
            )
    return which("ebook-convert") is not None


def _run_command(
    command: Sequence[str],
    run: Callable[..., subprocess.CompletedProcess],
) -> subprocess.CompletedProcess:
    return run(
        list(command),
        capture_output=True,
        text=True,
        check=False,
    )


def _validate_entry(
    path: Path,
    which: Callable[[str], Optional[str]],
    run: Callable[..., subprocess.CompletedProcess],
) -> None:
    validator = which("desktop-file-validate")
    if validator is None:
        return
    result = _run_command((validator, str(path)), run)
    if result.returncode:
        details = " ".join((result.stderr or result.stdout or "").split())
        raise DesktopInstallError(
            f"desktop-file-validate отклонил ярлык: "
            f"{details or f'код {result.returncode}'}"
        )


def _refresh_database(
    directory: Path,
    which: Callable[[str], Optional[str]],
    run: Callable[..., subprocess.CompletedProcess],
) -> tuple[str, ...]:
    updater = which("update-desktop-database")
    if updater is None:
        return ()
    result = _run_command((updater, str(directory)), run)
    if not result.returncode:
        return ()
    details = " ".join((result.stderr or result.stdout or "").split())
    return (
        "Не удалось обновить пользовательскую desktop-базу: "
        f"{details or f'код {result.returncode}'}",
    )


def install(
    root: Optional[Path] = None,
    destination: Optional[Path] = None,
    which: Callable[[str], Optional[str]] = shutil.which,
    run: Callable[..., subprocess.CompletedProcess] = subprocess.run,
    replace: Callable[[Path | str, Path | str], None] = os.replace,
) -> InstallResult:
    """Атомарно установить или обновить принадлежащий проекту ярлык."""
    root = project_root() if root is None else Path(root).resolve()
    calibre_available = _check_project_requirements(root, which)
    applications_dir = (
        applications_directory() if destination is None else Path(destination)
    )
    applications_dir.mkdir(parents=True, exist_ok=True)
    entry_path = applications_dir / DESKTOP_FILENAME
    if entry_path.exists() and not is_managed_entry(entry_path):
        raise DesktopInstallError(
            f"Отказ от перезаписи чужого файла без маркера {MANAGED_KEY}=true: "
            f"{entry_path}"
        )

    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{DESKTOP_FILENAME}.",
        suffix=".desktop",
        dir=applications_dir,
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(build_desktop_entry(root))
            stream.flush()
            os.fsync(stream.fileno())
        temporary_path.chmod(0o644)
        _validate_entry(temporary_path, which, run)
        replace(temporary_path, entry_path)
        entry_path.chmod(0o644)
    except BaseException:
        temporary_path.unlink(missing_ok=True)
        raise

    warnings = _refresh_database(applications_dir, which, run)
    return InstallResult(entry_path, calibre_available, warnings)


def uninstall(
    destination: Optional[Path] = None,
    which: Callable[[str], Optional[str]] = shutil.which,
    run: Callable[..., subprocess.CompletedProcess] = subprocess.run,
) -> UninstallResult:
    """Удалить только управляемый Desktop Entry, не затрагивая проект."""
    applications_dir = (
        applications_directory() if destination is None else Path(destination)
    )
    entry_path = applications_dir / DESKTOP_FILENAME
    if not entry_path.exists():
        return UninstallResult(entry_path, removed=False)
    if not is_managed_entry(entry_path):
        raise DesktopInstallError(
            f"Отказ от удаления чужого файла без маркера {MANAGED_KEY}=true: "
            f"{entry_path}"
        )
    entry_path.unlink()
    warnings = _refresh_database(applications_dir, which, run)
    return UninstallResult(entry_path, removed=True, warnings=warnings)


def _print_warnings(warnings: Sequence[str]) -> None:
    for warning in warnings:
        print(f"Предупреждение: {warning}")


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Регистрация существующего клона в меню приложений",
    )
    parser.add_argument(
        "--uninstall",
        action="store_true",
        help="удалить только управляемый пользовательский ярлык",
    )
    args = parser.parse_args(argv)

    try:
        if args.uninstall:
            result = uninstall()
            if result.removed:
                print(f"Ярлык удалён: {result.entry_path}")
            else:
                print(f"Ярлык уже отсутствует: {result.entry_path}")
            _print_warnings(result.warnings)
            return 0

        result = install()
        print(f"Ярлык установлен: {result.entry_path}")
        if result.calibre_available:
            print("Calibre найден: дополнительные книжные форматы доступны.")
        else:
            print(
                "Calibre не найден: FB2 доступен, для дополнительных форматов "
                "установите calibre."
            )
        _print_warnings(result.warnings)
        return 0
    except DesktopInstallError as exc:
        parser.exit(1, f"Ошибка: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
