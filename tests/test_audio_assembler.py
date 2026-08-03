import struct
import tempfile
import threading
import unittest
import wave
from pathlib import Path
from unittest.mock import MagicMock, patch

from src.core.audio_assembler import AudioAssembler
from src.utils.exceptions import PipelineCanceledError


class AudioAssemblerTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.base = Path(self.temporary_directory.name)

    @staticmethod
    def _write_constant_wav(path: Path, value: int, seconds: float) -> None:
        frames = int(22050 * seconds)
        with wave.open(str(path), "wb") as stream:
            stream.setnchannels(1)
            stream.setsampwidth(2)
            stream.setframerate(22050)
            stream.writeframes(struct.pack("<h", value) * frames)

    def test_chapter_uses_one_ffmpeg_and_preserves_audio_pause_order(self):
        first = self.base / "first.wav"
        second = self.base / "second.wav"
        output = self.base / "chapter.wav"
        self._write_constant_wav(first, 1000, 0.1)
        self._write_constant_wav(second, -1000, 0.1)

        assembler = AudioAssembler(sample_rate=22050)
        with patch.object(
            assembler, "_run_ffmpeg", wraps=assembler._run_ffmpeg,
        ) as run:
            assembler.assemble_chapter(
                [(first, 0.1), (second, 0.2)], output,
            )

        self.assertEqual(run.call_count, 1)
        with wave.open(str(output), "rb") as stream:
            self.assertEqual(stream.getframerate(), 22050)
            self.assertEqual(stream.getnchannels(), 1)
            samples = struct.unpack(
                f"<{stream.getnframes()}h", stream.readframes(stream.getnframes()),
            )

        def mean(start: float, end: float) -> float:
            values = samples[int(start * 22050):int(end * 22050)]
            return sum(values) / len(values)

        self.assertAlmostEqual(len(samples) / 22050, 0.5, places=3)
        self.assertLess(abs(mean(0.02, 0.08)), 1)
        self.assertGreater(mean(0.12, 0.18), 900)
        self.assertLess(abs(mean(0.22, 0.38)), 1)
        self.assertLess(mean(0.42, 0.48), -900)

    def test_chapter_filter_graph_keeps_missing_file_pause_and_input_order(self):
        first = self.base / "first.mp3"
        second = self.base / "second.mp3"
        missing = self.base / "missing.mp3"
        output = self.base / "chapter.wav"
        first.write_bytes(b"first")
        second.write_bytes(b"second")
        observed = {}

        assembler = AudioAssembler.__new__(AudioAssembler)
        assembler.sample_rate = 22050

        def capture(args, cancel_event=None):
            script = Path(args[args.index("-filter_complex_script") + 1])
            observed["args"] = args
            observed["graph"] = script.read_text(encoding="utf-8")
            output.write_bytes(b"chapter")

        assembler._run_ffmpeg = capture
        assembler.get_audio_duration = lambda _path: 1.0
        assembler.assemble_chapter(
            [(first, 0.1), (missing, 0.2), (second, 0.3)], output,
        )

        args = observed["args"]
        self.assertEqual(
            [args[index + 1] for index, value in enumerate(args) if value == "-i"],
            [str(first), str(second)],
        )
        self.assertIn(
            "[pause_0][segment_0][pause_1][pause_2][segment_2]"
            "concat=n=5:v=0:a=1[chapter]",
            observed["graph"],
        )

    def test_chapter_cancellation_prevents_ffmpeg(self):
        audio = self.base / "audio.mp3"
        audio.write_bytes(b"audio")
        canceled = threading.Event()
        canceled.set()
        assembler = AudioAssembler.__new__(AudioAssembler)
        assembler.sample_rate = 22050
        assembler._run_ffmpeg = MagicMock()

        with self.assertRaises(PipelineCanceledError):
            assembler.assemble_chapter(
                [(audio, 0.3)], self.base / "chapter.wav", canceled,
            )
        assembler._run_ffmpeg.assert_not_called()


if __name__ == "__main__":
    unittest.main()
