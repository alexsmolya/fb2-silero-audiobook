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

Remaining publication action: normal push of the feature branch, subject to
network availability. No merge or force-push is in scope.

