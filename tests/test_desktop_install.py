"""Тесты безопасной пользовательской установки Desktop Entry."""

from __future__ import annotations

import os
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import install_desktop as desktop


class CommandRunner:
    def __init__(self, validator_returncode: int = 0):
        self.calls = []
        self.validator_returncode = validator_returncode

    def __call__(self, command, **kwargs):
        self.calls.append((command, kwargs))
        returncode = (
            self.validator_returncode
            if Path(command[0]).name == "desktop-file-validate"
            else 0
        )
        return subprocess.CompletedProcess(
            command,
            returncode,
            stdout="",
            stderr="invalid desktop entry" if returncode else "",
        )


class DesktopInstallTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.base = Path(self.temporary_directory.name)
        self.root = self.base / "project"
        python_path = self.root / ".venv" / "bin" / "python"
        python_path.parent.mkdir(parents=True)
        python_path.write_text("python", encoding="utf-8")
        python_path.chmod(0o755)
        (self.root / "audiobook_gui.py").write_text("# gui\n", encoding="utf-8")
        self.applications = self.base / "xdg" / "applications"
        self.runner = CommandRunner()

    def tearDown(self):
        self.temporary_directory.cleanup()

    @staticmethod
    def which(command: str):
        available = {
            "ffmpeg",
            "ffprobe",
            "ebook-convert",
            "desktop-file-validate",
            "update-desktop-database",
        }
        return f"/usr/bin/{command}" if command in available else None

    def install(self, **kwargs):
        return desktop.install(
            root=self.root,
            destination=self.applications,
            which=kwargs.pop("which", self.which),
            run=kwargs.pop("run", self.runner),
            **kwargs,
        )

    def test_xdg_directory_uses_environment_then_home_fallback(self):
        xdg_root = self.base / "custom data"
        self.assertEqual(
            desktop.applications_directory(
                env={"XDG_DATA_HOME": str(xdg_root)},
                home=self.base / "ignored",
            ),
            xdg_root / "applications",
        )
        self.assertEqual(
            desktop.applications_directory(env={}, home=self.base / "home"),
            self.base / "home" / ".local" / "share" / "applications",
        )

    def test_install_creates_entry_with_required_fields_and_permissions(self):
        result = self.install()
        contents = result.entry_path.read_text(encoding="utf-8")

        self.assertEqual(result.entry_path, self.applications / desktop.DESKTOP_FILENAME)
        self.assertIn("[Desktop Entry]\n", contents)
        self.assertIn("Type=Application\n", contents)
        self.assertIn("Name=Генератор аудиокниг Silero\n", contents)
        self.assertIn("Terminal=false\n", contents)
        self.assertIn("Icon=audio-x-generic\n", contents)
        self.assertIn("Categories=AudioVideo;Audio;Utility;\n", contents)
        self.assertIn(f"{desktop.MANAGED_KEY}=true\n", contents)
        self.assertEqual(stat.S_IMODE(result.entry_path.stat().st_mode), 0o644)

    def test_exec_and_path_are_absolute_and_use_project_python(self):
        entry = desktop.build_desktop_entry(self.root)
        resolved_root = self.root.resolve()
        self.assertIn(
            f'Exec="{resolved_root / ".venv/bin/python"}" '
            f'"{resolved_root / "audiobook_gui.py"}"',
            entry,
        )
        self.assertIn(f"Path={resolved_root}\n", entry)
        self.assertNotIn("sh -c", entry)
        self.assertNotIn("bash", entry)

    def test_exec_escapes_spaces_quotes_cyrillic_and_reserved_characters(self):
        unusual_root = self.base / 'Проект "книга" $цена % `тест`'
        python_path = unusual_root / ".venv" / "bin" / "python"
        python_path.parent.mkdir(parents=True)
        python_path.write_text("python", encoding="utf-8")
        python_path.chmod(0o755)
        (unusual_root / "audiobook_gui.py").write_text("# gui\n", encoding="utf-8")

        result = desktop.install(
            root=unusual_root,
            destination=self.applications,
            which=self.which,
            run=self.runner,
        )
        exec_line = next(
            line for line in result.entry_path.read_text(encoding="utf-8").splitlines()
            if line.startswith("Exec=")
        )
        self.assertIn("Проект", exec_line)
        self.assertIn('\\"книга\\"', exec_line)
        self.assertIn("\\$цена", exec_line)
        self.assertIn("%%", exec_line)
        self.assertIn("\\`тест\\`", exec_line)
        self.assertIn('Exec="', exec_line)

    def test_reinstall_replaces_own_entry(self):
        first = self.install()
        first.entry_path.write_text(
            first.entry_path.read_text(encoding="utf-8") + "Comment=old\n",
            encoding="utf-8",
        )

        second = self.install()

        contents = second.entry_path.read_text(encoding="utf-8")
        self.assertNotIn("Comment=old", contents)
        self.assertTrue(desktop.is_managed_entry(second.entry_path))

    def test_install_refuses_to_overwrite_foreign_entry(self):
        self.applications.mkdir(parents=True)
        entry = self.applications / desktop.DESKTOP_FILENAME
        original = "[Desktop Entry]\nName=Чужой ярлык\n"
        entry.write_text(original, encoding="utf-8")

        with self.assertRaisesRegex(desktop.DesktopInstallError, "чужого файла"):
            self.install()

        self.assertEqual(entry.read_text(encoding="utf-8"), original)

    def test_uninstall_removes_only_managed_entry(self):
        entry = self.install().entry_path

        result = desktop.uninstall(
            destination=self.applications,
            which=self.which,
            run=self.runner,
        )

        self.assertTrue(result.removed)
        self.assertFalse(entry.exists())
        self.assertTrue(self.root.exists())
        self.assertTrue((self.root / ".venv" / "bin" / "python").exists())

    def test_uninstall_refuses_to_remove_foreign_entry(self):
        self.applications.mkdir(parents=True)
        entry = self.applications / desktop.DESKTOP_FILENAME
        entry.write_text("[Desktop Entry]\nName=Чужой ярлык\n", encoding="utf-8")

        with self.assertRaisesRegex(desktop.DesktopInstallError, "чужого файла"):
            desktop.uninstall(
                destination=self.applications,
                which=self.which,
                run=self.runner,
            )

        self.assertTrue(entry.exists())

    def test_repeated_uninstall_of_missing_entry_is_calm(self):
        result = desktop.uninstall(
            destination=self.applications,
            which=self.which,
            run=self.runner,
        )
        self.assertFalse(result.removed)

    def test_default_install_honors_temporary_xdg_and_not_real_home(self):
        temporary_xdg = self.base / "isolated-xdg"
        real_entry = desktop.applications_directory() / desktop.DESKTOP_FILENAME
        existed_before = real_entry.exists()
        mtime_before = real_entry.stat().st_mtime_ns if existed_before else None

        with patch.dict(os.environ, {"XDG_DATA_HOME": str(temporary_xdg)}):
            result = desktop.install(
                root=self.root,
                which=self.which,
                run=self.runner,
            )

        self.assertTrue(result.entry_path.is_relative_to(temporary_xdg))
        self.assertEqual(real_entry.exists(), existed_before)
        if existed_before:
            self.assertEqual(real_entry.stat().st_mtime_ns, mtime_before)

    def test_missing_ebook_convert_is_nonfatal(self):
        def without_calibre(command):
            if command == "ebook-convert":
                return None
            return self.which(command)

        result = self.install(which=without_calibre)

        self.assertFalse(result.calibre_available)
        self.assertTrue(result.entry_path.is_file())

    def test_missing_ffmpeg_is_fatal_without_writing_entry(self):
        def without_ffmpeg(command):
            if command == "ffmpeg":
                return None
            return self.which(command)

        with self.assertRaisesRegex(desktop.DesktopInstallError, "ffmpeg"):
            self.install(which=without_ffmpeg)
        self.assertFalse((self.applications / desktop.DESKTOP_FILENAME).exists())

    def test_missing_project_python_is_fatal_without_writing_entry(self):
        (self.root / ".venv" / "bin" / "python").unlink()

        with self.assertRaisesRegex(desktop.DesktopInstallError, "проектный Python"):
            self.install()
        self.assertFalse((self.applications / desktop.DESKTOP_FILENAME).exists())

    def test_install_uses_atomic_replace_in_same_directory(self):
        calls = []

        def recording_replace(source, destination):
            source = Path(source)
            destination = Path(destination)
            calls.append((source, destination))
            self.assertEqual(source.parent, destination.parent)
            self.assertTrue(source.is_file())
            os.replace(source, destination)

        result = self.install(replace=recording_replace)

        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0][1], result.entry_path)
        self.assertTrue(result.entry_path.is_file())

    def test_validator_failure_preserves_existing_managed_entry(self):
        existing = self.install().entry_path
        original = existing.read_text(encoding="utf-8")
        failing_runner = CommandRunner(validator_returncode=1)

        with self.assertRaisesRegex(
            desktop.DesktopInstallError,
            "desktop-file-validate",
        ):
            self.install(run=failing_runner)

        self.assertEqual(existing.read_text(encoding="utf-8"), original)
        leftovers = list(self.applications.glob(f".{desktop.DESKTOP_FILENAME}.*"))
        self.assertEqual(leftovers, [])


if __name__ == "__main__":
    unittest.main()
