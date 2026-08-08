# Release: text segmentation and adaptive pauses

## Task and initial state

Promote the already implemented and accepted text-segmentation and adaptive
pause-policy work to the primary `main` branch, verify it, and refresh the
existing user-local launcher without redesigning either subsystem.

- Repository: `alexsmolya/fb2-silero-audiobook`
- Initial `main`: `514e331d8e3001c469db15ac7b80a368b31ecf04`
- Accepted feature branch: `fix/pause-policy-forensic`
- Accepted feature head: `1eaaf00026eea7aecb8da8d8afab86908637914b`
- Text-segmentation engineering commit: `345320389e2b9ee584ae4b81145e8dfa5a985947`
- Pause-policy engineering commit: `8c56f34f7c2e1de5f63743a0ab5f3f48e18826c9`
- Integration branch: `main`
- Integration result: fast-forward `514e331` to `1eaaf00`; no conflicts,
  merge commit, rebase, reset, or history rewrite
- Release documentation commit: recorded in `codex-reports/LATEST.md`

Preflight proved that `main` was the direct ancestor of the accepted feature
head (`main...feature = 0/17`) and that both engineering commits were in the
feature history. The worktree was clean. A fresh `git fetch origin` confirmed
that `origin/main` was still `514e331` before integration.

## Released functionality

- FB2 title and paragraph structure remains explicit through segmentation;
  headings cannot merge into the first body paragraph.
- Context-aware handling covers `?..`, `!..`, Unicode `⁈`, dialogue
  continuations, malformed duplicate headings, and punctuation-only fragments.
- Literary censor masks remain speech-bearing and are normalized before the
  Silero wrapper; raw repeated asterisks are not spoken as repeated
  “звёздочка”.
- Identifier `80−03`/`80-03` keeps its significant zero and clock-like
  `9.30` is normalized conservatively without changing ordinary decimals.
- Boundary metadata distinguishes ordinary, question, exclamation, ellipsis,
  dialogue, paragraph, title/body, and chapter transitions.
- Assembly uses target-final-silence deficit padding based on measured adjacent
  Silero edges. It never trims source TTS audio. Chapter padding adapts to an
  independent `2.10 s` target.

Principal implementation and regression files promoted by this release:

- `src/core/fb2_parser.py`
- `src/core/sentence_splitter.py`
- `src/core/tts_silero.py`
- `src/core/pause_policy.py`
- `src/core/audio_assembler.py`
- `src/core/pipeline.py`
- `src/core/run_diagnostics.py`
- `tests/test_fb2_parser.py`
- `tests/test_sentence_splitter_characterization.py`
- `tests/test_silero_pronunciations.py`
- `tests/test_pause_policy.py`
- `tests/test_audio_assembler.py`
- `tests/test_tts_diagnostics_jsonl.py`

The fast-forward also preserves the feature branch's already reviewed GUI
model-manager, pronunciation dictionary, diagnostics, documentation, and their
tests; no new functional source edit was made during this release task.

## Verification

- Full pytest: `288 passed`, 51 subtests; one non-fatal packaged-Torch
  `SyntaxWarning`.
- Focused structure/Silero/pause/assembly tests: `58 passed`, 7 subtests; two
  non-fatal environment/package warnings (NVML unavailable in the restricted
  test process and the same packaged-Torch warning).
- `python -m compileall -f audiobook_gui.py src tests`: passed.
- `uv lock --check --python .venv/bin/python`: passed, 123 packages resolved
  from the existing lock.
- `git diff --check`: passed.
- No full-book synthesis, ASR, model download, or additional A/B was run.

The unchanged accepted engineering commits retain the real-book dry results:

| Regression metric | Before | Released |
| --- | ---: | ---: |
| Paragraph crossings | 134 | 0 |
| Merged chapter headings | 22 | 0 |
| Punctuation-only speech segments | 10 | 0 |
| Missed `?..` / `!..` boundaries | 13 | 0 |
| Clear missed `⁈` boundaries | 32 | 0 |
| Duplicate `.Глава 16` | 1 | 0 |
| Asterisk-to-`звёздочка` cases | 15 | 0 |
| Lossy `80−03` cases | 2 | 0 |
| Decimalized `9.30` cases | 1 | 0 |

The accepted short A/B changed median detected boundary silence from
`0.594 s` to `0.450 s` and added padding from `7.200 s` to `2.468 s` across
23 boundaries. The user heard no regression and accepted the adaptive result.

## Local installation and smoke check

The documented installation is a managed desktop entry that runs this clone
directly; it does not copy the application. Running
`.venv/bin/python scripts/install_desktop.py` atomically refreshed the existing
entry at `~/.local/share/applications/fb2-silero-audiobook.desktop`.

- Exactly one matching desktop entry was found.
- It points to this repository's `.venv/bin/python` and `audiobook_gui.py`, with
  `Path=/home/alex/Projects/audiobook-generator`.
- The runtime import resolved `src/core/pause_policy.py` from this same clone
  and exposed the released target values.
- A real-display GUI smoke process remained alive in its event loop until the
  intentional five-second timeout; no TTS was started.
- `desktop-file-validate` accepted the entry with one informational category
  hint that an application may appear more than once in a menu.

## Limitations and next step

- Edge metadata remains Silero-specific; other backends retain the conservative
  full-target fallback.
- Model-only stress and prosody errors are intentionally not addressed here.
- No full audiobook was regenerated.

Recommended next step: use the updated launcher for normal listening and log
specific pronunciation/prosody cases for a later evidence-based task. Do not
replace them globally without accumulated examples.

Push target: `origin/main` by ordinary non-force push. The first publication
advanced it from `514e331` to `3ff15eb` successfully; the final report status
and exact documentation pointer are recorded in `codex-reports/LATEST.md`.
