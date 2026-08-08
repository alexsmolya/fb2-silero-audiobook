# Run log: release text segmentation and adaptive pauses

## Scope

Release-only task. No redesign, full-book synthesis, ASR, model download, or
new pronunciation rule was authorized or performed.

## Preflight and integration

Grouped read-only preflight included:

```text
pwd
git status --short --branch
git branch --show-current
git rev-parse HEAD
git rev-parse main
git log --oneline --decorate --graph -n 20 --all
git remote -v
git branch -vv
git merge-base main fix/pause-policy-forensic
git rev-list --left-right --count main...fix/pause-policy-forensic
git cat-file -t 8c56f34f7c2e1de5f63743a0ab5f3f48e18826c9
git merge-base 345320389e2b9ee584ae4b81145e8dfa5a985947 fix/pause-policy-forensic
```

Result: exit `0`. The repository was clean on
`fix/pause-policy-forensic@1eaaf000`; `main` and `origin/main` were `514e331`.
The merge base was `514e331`, divergence was `0 17`, the pause commit existed,
and the text commit was the merge base of itself and the feature branch.

`git fetch origin` completed with exit `0`; follow-up comparison still showed
`origin/main@514e331` and divergence `0 17`.

Integration commands:

```text
git switch main
git merge --ff-only fix/pause-policy-forensic
```

Result: exit `0`; fast-forward `514e331..1eaaf00`, 29 files changed, 3,918
insertions and 74 deletions. No conflict, merge commit, rebase, reset, or
history rewrite occurred.

## Tests and checks

```text
.venv/bin/python -m pytest -q
```

Exit `0`: `288 passed`, 51 subtests in 12.60 seconds. One packaged Torch
`SyntaxWarning: invalid escape sequence` was retained.

```text
.venv/bin/python -m pytest -q \
  tests/test_fb2_parser.py \
  tests/test_sentence_splitter_characterization.py \
  tests/test_silero_pronunciations.py \
  tests/test_pause_policy.py \
  tests/test_audio_assembler.py
```

Exit `0`: `58 passed`, 7 subtests in 3.26 seconds. Warnings: NVML could not be
initialized in the restricted test process, and the same packaged Torch
syntax warning. Neither changed the test result.

```text
.venv/bin/python -m compileall -f audiobook_gui.py src tests
uv lock --check --python .venv/bin/python
git diff --check
```

All exited `0`; compileall covered the GUI, source, and tests; the lock check
resolved 123 existing packages in 2 ms. No dependency or model download ran.

The real-FB2 structural metrics were not recomputed with ASR. They were reused
from the existing REPORT/RUNLOG because `main` now contains the exact accepted
engineering commits and the complete regression suite passed. The retained
dry validation is 134→0 paragraph crossings, 22→0 merged headings, 10→0
punctuation-only segments, 13→0 mixed-terminal misses, 32→0 clear interrobang
misses, and zero remaining heading/censor/identifier/clock regressions.

## Installation and runtime checks

Inspection of README and `scripts/install_desktop.py` established that the
official user-local mechanism registers the existing clone; it does not copy
source or create a second environment. The pre-existing managed entry already
pointed to this clone.

```text
.venv/bin/python scripts/install_desktop.py
desktop-file-validate ~/.local/share/applications/fb2-silero-audiobook.desktop
```

Installer exit `0`: the managed entry was atomically refreshed and Calibre was
found. Validation exit `0` with an informational hint that its multiple main
categories may make it appear more than once in an application menu.

Checks of `Exec`, `Path`, and the management marker confirmed this repository,
its `.venv`, and `audiobook_gui.py`. A filename/content search found one
matching desktop entry and no competing launcher.

```text
timeout 5 .venv/bin/python audiobook_gui.py
```

Exit `124` was expected: the process produced no error and remained alive in
the Tk event loop until the intentional five-second timeout. No TTS or book
processing was started.

Two diagnostic probes failed after the focused tests because they referenced
nonexistent convenience names `DEFAULT_TARGETS` and then `PauseTargets` in the
functional `pause_policy` module. Each exited `1` with `AttributeError`; no
file was modified. The corrected probe used the actual API:

```text
.venv/bin/python -c "import src.core.pause_policy as p; ... \
  p.TARGET_FINAL_SILENCE ... p.CHAPTER_TARGET_FINAL_SILENCE"
```

Exit `0`; import path was this clone's `src/core/pause_policy.py`, targets were
ordinary `0.30`, question `0.45`, exclamation `0.38`, ellipsis `0.45`, dialogue
`0.38`, paragraph `0.45`, title/body `0.75`, and chapter `2.10` seconds.

## Git publication

Release REPORT, RUNLOG, and `LATEST.md` were added on `main` after functional
verification.

```text
git push origin main
```

Exit `0`; GitHub reported `514e331..3ff15eb main -> main`. The REPORT/RUNLOG
were then updated with that observed result. Their exact documentation commit
and the final pointer commit are recorded in `LATEST.md`. Publication uses only
ordinary pushes to `origin/main`; no PR, force-push, branch deletion, or
automatic merge operation is involved.
