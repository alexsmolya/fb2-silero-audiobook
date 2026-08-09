# Latest Codex report

- Report: `codex-reports/2026-08-09_ffmpeg-large-chapter-regression_REPORT.md`
- Run log: `codex-reports/logs/2026-08-09_ffmpeg-large-chapter-regression_RUNLOG.md`
- Task: fix FFmpeg failure during adaptive assembly of a 189-segment chapter
- Engineering branch: `fix/large-chapter-ffmpeg-assembly`
- Engineering and final functional main SHA: `bd58a2b77172a986de581ccc5cebfdc38eda33d7`
- Root cause: a semantically zero adaptive deficit became
  `5.551115123125783e-17`, which FFmpeg rejected as an `atrim` duration
- Fix: integer-sample padding plus a 4-KiB diagnostic stderr tail
- Verification: focused 8 passed; full 290 passed plus 51 subtests; compileall,
  diff check, synthetic 189-file sample-order test, and ffprobe passed
- Real chapter: unavailable because the failed run's temporary MP3/sidecar
  directory had already been cleaned; no TTS rerun was performed
- Installation: managed launcher refreshed and real-display GUI smoke passed
- Publication: functional main `bd58a2b` pushed normally to `origin/main`
- Status: complete
- Timestamp: 2026-08-09 (Europe/Stockholm)
