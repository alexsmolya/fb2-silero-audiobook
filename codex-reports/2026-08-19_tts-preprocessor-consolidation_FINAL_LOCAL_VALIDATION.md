# Final local validation — TTS preprocessor consolidation

Date: 2026-08-19 (Europe/Stockholm)
Branch: `feat/tts-preprocessor-consolidation`

## Local production result

The normal local runtime is the repository virtualenv entrypoint
`.venv/bin/python audiobook_gui.py`. The installed desktop entry
`~/.local/share/applications/fb2-silero-audiobook.desktop` points directly to
that working copy and was refreshed with `scripts/install_desktop.py`.

`TtsPreprocessor` is active in `src.core.pipeline` before final sentence
segmentation. A short real pipeline run used the cached local Silero model
`/home/alex/.local/share/fb2-silero-audiobook/models/v5_5_ru/v5_5_ru_ru.pt`.
It parsed FB2, wrote normalized artifacts, produced seven segments, synthesized
all seven through Silero, and assembled the final MP3 without diagnostics.

Persistent smoke output:

- `/home/alex/Загрузки/AudioBook/_local-production-smoke/local-production-smoke.tts.md`
- `/home/alex/Загрузки/AudioBook/_local-production-smoke/local-production-smoke.tts-changes.json`
- `/home/alex/Загрузки/AudioBook/_local-production-smoke/Local Production Smoke.mp3`
- `/home/alex/Загрузки/AudioBook/_local-production-smoke/run-logs/`

Normal GUI runs use the configured output directory (`/home/alex/Загрузки/AudioBook`
on this machine) for `.tts.md` and `.tts-changes.json`, and
`~/.local/state/fb2-silero-audiobook/logs/` for diagnostic run logs.

## Validation

- Books 9/10 parse and dry segmentation: 23/28 chapters, 2819/2872 source and
  normalized paragraphs, 6394/6387 segments.
- Paragraph crossings, accidental title/body merges, punctuation-only segments,
  and empty segments: 0 for both books.
- Expressive-vowel audit: 113 rows, 110 transformed, 3 skipped negative
  controls, 0 suspicious, 113 lexical-preservation passes.
- Focused tests: 71 passed, 2 warnings, 7 subtests.
- Full pytest: 304 passed, 2 warnings, 51 subtests.
- `compileall`: exit 0; `uv lock --check`: exit 0; `git diff --check`: exit 0.
- Desktop file validation: exit 0. Direct GUI launch could not connect to the
  unavailable `:0` display (`_tkinter.TclError`); no headless X server is
  installed. This is an environment limitation, not a launcher-path failure.

## Known limitations

Production v3 long-vowel handling is a best-effort deterministic workaround,
not a true Silero prosody fix. The standalone initial `О` in book 10 chapter 4
paragraph 79 may still be heard as `А`; it is deliberately not changed by the
expressive-vowel rule. Adaptive pause policy and FFmpeg assembly semantics were
not modified.

## Handoff state

Google Drive handoff is the primary review artifact. Git is only the secondary
archive after this local validation and Drive read-back. No merge, force-push,
or upstream Silero publication is part of this pass.
