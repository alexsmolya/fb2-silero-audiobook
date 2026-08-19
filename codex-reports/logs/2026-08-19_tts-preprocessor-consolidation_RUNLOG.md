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

Normal push completed after a DNS-related retry using the approved network
path: `origin/feat/tts-preprocessor-consolidation` at `c88785c043ea...`.
No merge or force-push is in scope.
