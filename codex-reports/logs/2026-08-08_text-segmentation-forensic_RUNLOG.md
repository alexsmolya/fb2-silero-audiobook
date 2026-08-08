# Text segmentation forensic run log

Diagnostic summary for task commit
`345320389e2b9ee584ae4b81145e8dfa5a985947`. This is not a raw terminal
transcript and contains no credentials or internal chain-of-thought.

## Execution sequence

1. Verified the checkout was clean on `feat/pronunciation-corrections` at
   `4694e66b0591a5028415bac243a5827434f7e072`; inspected local branches,
   `origin`, `upstream`, parser/splitter/pipeline/Silero code, tests, and the
   forensic report.
2. Confirmed that the current HEAD contained the pronunciation and ellipsis
   commits used by the forensic run and created
   `fix/text-segmentation-forensic` from that HEAD.
3. Implemented structural splitting, punctuation filtering, terminal-mark
   handling, heading deduplication, and Silero input protection.
4. Added focused regression tests and iterated on dialogue conservatism,
   asterisk patterns, and failed spaCy-load caching.
5. Ran focused, pipeline-related, and full tests; performed a no-TTS dry
   validation against the real FB2 and existing forensic CSV.
6. Reviewed the scoped diff, committed once, and later added the GitHub handoff
   documents in a separate documentation commit.

## Significant commands and results

### Preflight and inspection

```text
git status --short --branch
git branch --show-current
git rev-parse HEAD
git remote -v
git branch -vv
git log --oneline --decorate --graph --max-count=18 --all
rg --files ...
sed -n ... analysis/REPORT.md and relevant source/test files
```

Result: exit `0`; worktree clean. `origin` was
`alexsmolya/fb2-silero-audiobook`, `upstream` was
`saabst/book-v2-audio`, and remote default was later verified as `main`.

Branch creation:

```text
git switch -c fix/text-segmentation-forensic
```

Result: exit `0`.

### Failed test attempt 1

```text
pytest -q tests/test_fb2_parser.py \
  tests/test_sentence_splitter_characterization.py \
  tests/test_silero_pronunciations.py
```

Result: exit `127`.

```text
/usr/bin/bash: pytest: command not found
```

Remediation: located the existing `.venv` and used its Python; no dependency
installation or model download was performed.

### Failed test attempt 2

```text
.venv/bin/pytest -q tests/test_fb2_parser.py \
  tests/test_sentence_splitter_characterization.py \
  tests/test_silero_pronunciations.py
```

Result: exit `2`; collection failed because invoking the venv's `pytest`
entrypoint did not put the repository root on `sys.path`:

```text
ModuleNotFoundError: No module named 'src'
```

Remediation: used the project-compatible form `.venv/bin/python -m pytest`.

### Focused and integration checks

```text
.venv/bin/python -m pytest -q \
  tests/test_fb2_parser.py \
  tests/test_sentence_splitter_characterization.py \
  tests/test_silero_pronunciations.py
```

Intermediate result: exit `0`, `33 passed`, 7 subtests. After final regression
additions, the focused splitter/Silero subset passed `32 tests`, 7 subtests.

```text
.venv/bin/python -m pytest -q \
  tests/test_global_progress.py tests/test_cancellation.py \
  tests/test_book_input.py tests/test_run_diagnostics.py
```

Result: exit `0`, `89 passed`, 44 subtests.

### First real-FB2 dry validation and warning issue

The first per-paragraph dry run succeeded but repeatedly attempted to load the
absent `ru_core_news_sm` model, producing thousands of identical warnings and
large collapsed output.

```text
[repeated warning omitted: absent spaCy Russian model retried once per paragraph]
```

Decision: cache failed spaCy model-load attempts. This was required by the new
per-paragraph execution path and avoided both repeated work and log flooding.

The same run exposed metric-definition differences:

- a contiguous-run regex counted 13 segments, while all 15 forensic segments
  contained censored asterisk forms, including `*-*-*` and one embedded `*`;
- a broad mixed-terminal regex counted one quoted repetition that the forensic
  classification intentionally excluded.

Decision: protect obvious literary masks including repeated hyphenated and
embedded-in-word forms while preserving spaced literal `*`; keep `?..`/`!..`
splitting conservative around quotes and dialogue dashes.

### Final real-FB2 dry validation

Input artifacts:

- `07 Гимн шута - 07.fb2`
- `analysis/segments.csv`

No audio synthesis was run. Final result:

```text
segments: 6906 -> 7051
paragraph crossings: 134 -> 0
merged chapter headings: 22 -> 0
punctuation-only speech segments: 10 -> 0
missed ?../!.. boundaries: 13 -> 0
clear ⁈ missed boundaries: 32 -> 0
duplicate .Глава 16: 1 -> 0
asterisk-to-звёздочка segments: 15 -> 0
lossy 80−03 occurrences: 2 -> 0
decimalized 9.30 occurrences: 1 -> 0
```

Normalization samples:

```text
группа 80−03 => группа 80 дефис ноль три
группа 80-03 => группа 80 дефис ноль три
Выезд в 9.30. => Выезд в 9 30.
Число 3.14. => Число 3.14.
— ******! => — пик!
```

### Final verification

```text
.venv/bin/python -m pytest -q
.venv/bin/python -m compileall -q src tests
git diff --check
```

Result: exit `0`; `268 passed`, 51 subtests. Two non-fatal environment warnings
were retained in the test summary: CUDA NVML initialization was unavailable,
and an installed packaged Torch module emitted a `SyntaxWarning` for an escape
sequence. Neither affected test outcomes.

### Git operations

```text
git add <four scoped core files> <three scoped test files>
git commit -m "fix: preserve book structure and normalize TTS text"
```

Result: exit `0`; task commit
`345320389e2b9ee584ae4b81145e8dfa5a985947`, 7 files changed, 268 insertions,
9 deletions.

Reporting infrastructure was added as commit
`e9e25071574e91639e1b05cce837c7581278f139` and pushed normally:

```text
git push -u origin fix/text-segmentation-forensic
```

Result: exit `0`; new remote branch
`origin/fix/text-segmentation-forensic`. No PR, merge, rebase, force-push, or
remote-history rewrite was performed.

## Files changed by the engineering task

- `src/core/fb2_parser.py`
- `src/core/pipeline.py`
- `src/core/sentence_splitter.py`
- `src/core/tts_silero.py`
- `tests/test_fb2_parser.py`
- `tests/test_sentence_splitter_characterization.py`
- `tests/test_silero_pronunciations.py`

## Outcome and follow-up

The deterministic text defects were eliminated structurally before expensive
TTS. The global `0.3 s` pause policy was explicitly left unchanged. The next
recommended task is target-final-silence pause adaptation using existing edge
silence and boundary-type evidence.
