import struct
import tempfile
import threading
import unittest
import wave
from pathlib import Path
from unittest.mock import MagicMock, patch

from src.core.audio_assembler import AudioAssembler
from src.core.pause_policy import EdgeSilence, write_edge_silence
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
            observed["args"] = args
            observed["graph"] = args[args.index("-filter_complex") + 1]
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

    def test_chapter_adds_only_target_silence_deficit(self):
        first = self.base / "first.wav"
        second = self.base / "second.wav"
        output = self.base / "adaptive.wav"
        self._write_constant_wav(first, 1000, 0.3)
        self._write_constant_wav(second, -1000, 0.2)
        write_edge_silence(first, EdgeSilence(0.0, 0.12))
        write_edge_silence(second, EdgeSilence(0.08, 0.0))

        assembler = AudioAssembler(sample_rate=22050)
        assembler.assemble_chapter([(first, 0.0), (second, 0.45)], output)

        # Input audio is 0.5 s; only the 0.25 s target deficit is inserted.
        self.assertAlmostEqual(assembler.get_audio_duration(output), 0.75, places=3)

    def test_real_scale_adaptive_chapter_is_sample_accurate(self):
        sample_rate = 22050
        segment_frames = 220
        segment_seconds = segment_frames / sample_rate
        paths = []
        for index in range(189):
            path = self.base / f"segment_{index:03d}.wav"
            self._write_constant_wav(path, 1000 + index, segment_seconds)
            edge = (
                EdgeSilence(0.30, 0.0)
                if index == 1
                else EdgeSilence(0.001, 0.002)
            )
            write_edge_silence(path, edge)
            paths.append(path)

        # Boundary 1 has an exact semantic deficit of zero, but binary float
        # arithmetic produces 5.551115123125783e-17. The old duration-based
        # filter graph passed that scientific notation to ffmpeg and failed.
        write_edge_silence(paths[0], EdgeSilence(0.001, 0.15))
        targets = [0.0, 0.45] + [0.010] * 187
        output = self.base / "large-adaptive-chapter.wav"

        assembler = AudioAssembler(sample_rate=sample_rate)
        assembler.assemble_chapter(list(zip(paths, targets)), output)

        padding_frames = [
            0,
            0,
            round(0.009 * sample_rate),
            *([round(0.007 * sample_rate)] * 186),
        ]
        expected_frames = 189 * segment_frames + sum(padding_frames)
        with wave.open(str(output), "rb") as stream:
            self.assertEqual(stream.getframerate(), sample_rate)
            self.assertEqual(stream.getnchannels(), 1)
            self.assertEqual(stream.getnframes(), expected_frames)
            samples = struct.unpack(
                f"<{stream.getnframes()}h",
                stream.readframes(stream.getnframes()),
            )

        cursor = 0
        for index, padding in enumerate(padding_frames):
            self.assertTrue(all(value == 0 for value in samples[cursor:cursor + padding]))
            cursor += padding
            self.assertTrue(
                all(
                    value == 1000 + index
                    for value in samples[cursor:cursor + segment_frames]
                )
            )
            cursor += segment_frames
        self.assertEqual(cursor, len(samples))

    def test_chapter_skips_padding_when_edges_already_meet_target(self):
        first = self.base / "first.wav"
        second = self.base / "second.wav"
        output = self.base / "enough.wav"
        self._write_constant_wav(first, 1000, 0.2)
        self._write_constant_wav(second, -1000, 0.2)
        write_edge_silence(first, EdgeSilence(0.0, 0.25))
        write_edge_silence(second, EdgeSilence(0.15, 0.0))

        assembler = AudioAssembler(sample_rate=22050)
        assembler.assemble_chapter([(first, 0.0), (second, 0.30)], output)

        self.assertAlmostEqual(assembler.get_audio_duration(output), 0.4, places=3)

    def test_book_chapter_pause_is_a_separate_final_target(self):
        first = self.base / "chapter_1.wav"
        second = self.base / "chapter_2.wav"
        output = self.base / "book.mp3"
        self._write_constant_wav(first, 1000, 0.1)
        self._write_constant_wav(second, -1000, 0.1)
        write_edge_silence(first, EdgeSilence(0.0, 0.30))
        write_edge_silence(second, EdgeSilence(0.20, 0.0))

        assembler = AudioAssembler(sample_rate=22050)
        with patch.object(
            assembler, "_make_silence", wraps=assembler._make_silence,
        ) as make_silence:
            assembler.assemble_book([first, second], output)

        self.assertEqual(make_silence.call_count, 1)
        self.assertAlmostEqual(make_silence.call_args.args[1], 1.60, places=6)

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

    def test_ffmpeg_error_reports_diagnostic_tail_instead_of_banner(self):
        assembler = AudioAssembler.__new__(AudioAssembler)
        assembler._ffmpeg = "ffmpeg"
        banner = "configuration: " + ("feature " * 1000)
        diagnostic = (
            '[Parsed_atrim_3] Unable to parse "duration" option value '
            '"5.551115123125783e-17" as duration\nError: Invalid argument\n'
        )
        process = MagicMock()
        process.communicate.return_value = (b"", (banner + diagnostic).encode())
        process.returncode = 234

        with patch("src.core.audio_assembler.sp.Popen", return_value=process):
            with self.assertRaisesRegex(RuntimeError, "Unable to parse") as raised:
                assembler._run_ffmpeg(["-version"])

        message = str(raised.exception)
        self.assertIn("код 234", message)
        self.assertIn("5.551115123125783e-17", message)
        self.assertIn("начало stderr опущено", message)
        self.assertNotIn(banner, message)


if __name__ == "__main__":
    unittest.main()
