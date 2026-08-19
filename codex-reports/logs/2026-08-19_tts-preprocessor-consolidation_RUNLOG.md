# Run log — TTS preprocessor consolidation (2026-08-19)

Commands and relevant outcomes; no hidden reasoning included.

| Command/action | Result |
|---|---|
| `pwd`, `git status --short`, branch/SHA/remotes/log preflight | clean `main` at `9fd35745ba294bd455307e90144b20169d52ee34`; origin/upstream recorded |
| `git ls-remote origin ...` | exit 128; DNS failure: `Could not resolve host: github.com` |
| Read CODEX bootstrap, bounty policy, project files/history/reports/docs | completed |
| Read Drive journal and three 2026-08-14 handoffs | completed via connected Drive |
| Baseline focused pytest | exit 0; 59 passed, 1 warning, 7 subtests |
| Created `feat/tts-preprocessor-consolidation` | exit 0 |
| Added compiler, artifacts, inventory, architecture, tests, pipeline wiring | completed |
| New preprocessor pytest | exit 0; 9 passed |
| Full `.venv/bin/python -m pytest -q` | exit 0; 301 passed, 2 warnings, 51 subtests |
| `.venv/bin/python -m compileall -q src tests` | exit 0 |
| `uv lock --check` | exit 0; 123 packages resolved |
| `git diff --check` | exit 0 |
| `uv run python main.py models info v5_5_ru` | exit 0; local model available |
| First long-vowel smoke command | exit 1; temporary one-line command had a Python `SyntaxError`; no repository effect |
| Retried long-vowel smoke via `/tmp/long_vowel_smoke.py` | exit 0; 16 MP3 fragments generated under `/tmp/audiobook-long-vowels.iHFhLA` |
| Short artifact smoke | exit 0; `.tts.md` and `.tts-changes.json` created under `/tmp/audiobook-tts-smoke.pY6a0m` |
| `git commit -m 'feat: consolidate deterministic TTS preprocessing'` | exit 0; `34033a887e797a7cc5a456d9cf589ab0e5b3b8be` |

## Corpus forensic extension

| Command/action | Result |
|---|---|
| Parse books 9/10 + compile + split without synthesis | exit 0; 23/28 chapters, 2819/2872 paragraphs, 6394/6387 segments |
| Target occurrence extraction | exit 0; 1072 rows, 533 book 9 and 539 book 10 |
| Real corpus token-preservation audit | exit 0; no non-heading, non-censor lexical loss |
| Fix lock modifier loss and bounded `проводишь свою среду` | implemented; focused tests passed |
| Real-context long-vowel Silero smoke | exit 0; 16 MP3 files, four phrases × original/3/4/5 |
| Focused post-fix pytest | exit 0; 69 passed, 1 warning, 7 subtests |
| Full post-fix pytest | exit 0; 302 passed, 2 warnings, 51 subtests |
| Rebuilt `BOOK09_10_CORPUS_AUDIT.md/.json` | exit 0; tracked audit artifacts |

## Expressive-vowel production extension

| Command/action | Result |
|---|---|
| Human A/B decision applied | v3 selected: exactly 3 contiguous vowels; v4 rejected as inconsistent |
| Dry-run over expressive audit rows | exit 0; 113 rows, 110 transformed, 3 skipped negative controls, 0 suspicious, 113 lexical-preservation passes |
| Production transform tests | exit 0; 12 preprocessor tests |
| Full post-transform pytest | exit 0; 304 passed, 2 warnings, 51 subtests |
| compileall / `uv lock --check` / `git diff --check` | exit 0 / 0 / 0 |

The standalone initial `О` in book10/chapter4/paragraph79 remains a documented
Silero model limitation and is not transformed.

## Local production pass

| Command/action | Result |
|---|---|
| Inspect launcher and settings | `.local/share/applications/fb2-silero-audiobook.desktop` targets current repository `.venv/bin/python audiobook_gui.py`; Silero backend configured; output directory `/home/alex/Загрузки/AudioBook` |
| `.venv/bin/python scripts/install_desktop.py` | exit 0; launcher refreshed; Calibre detected |
| `desktop-file-validate ~/.local/share/applications/fb2-silero-audiobook.desktop` | exit 0; category hint only |
| Local model/cache check | exit 0; `v5_5_ru_ru.pt` present, 145420684 bytes |
| Persistent short `Pipeline.run` smoke | exit 0; 7 segments synthesized; `.tts.md`, `.tts-changes.json`, MP3, and run log written under `/home/alex/Загрузки/AudioBook/_local-production-smoke/`; diagnostic errors 0 |
| Direct `timeout --signal=TERM 8 .venv/bin/python audiobook_gui.py` | exit 1 because `_tkinter.TclError: couldn't connect to display ":0"`; no `xvfb-run`/headless X server available; environment limitation |
| Real book 9/10 parse/preprocess/segment dry validation | exit 0; 23/28 chapters, 2819/2872 paragraphs, 6394/6387 segments; no paragraph crossings or accidental title/body merges |
| Expressive v3 dry-run | exit 0; 113 rows, 110 transformed, 3 skipped negative controls, 0 suspicious, 113 lexical preservation passes |
| `.venv/bin/python -m pytest -q tests/test_tts_preprocessor.py` | exit 0; 12 passed, 1 warning |
| Focused regression pytest | exit 0; 71 passed, 2 warnings, 7 subtests |
| Full `.venv/bin/python -m pytest -q` | exit 0; 304 passed, 2 warnings, 51 subtests |
| `.venv/bin/python -m compileall -q src tests` | exit 0 |
| `uv lock --check` | exit 0; 123 packages resolved |
| `git diff --check` | exit 0 |

Persistent artifact locations and final local validation are summarized in
`codex-reports/2026-08-19_tts-preprocessor-consolidation_FINAL_LOCAL_VALIDATION.md`.

Normal push completed after a DNS-related retry using the approved network
path: `origin/feat/tts-preprocessor-consolidation` at `c88785c043ea...`.
Drive bundle manifest and patch read-back succeeded; the first report upload
hit a Google Drive API quota limit, then the bounded retry succeeded and the
report checksum matched local content. The local-production documentation was
committed after that handoff as
`1d692b8f39bf7d6fbeaf77511999c0e7a055685f`. No merge or force-push is in scope.
Normal archival push then succeeded:
`bb36466..2770d96 feat/tts-preprocessor-consolidation -> feat/tts-preprocessor-consolidation`.
