# Pause policy forensic run log

Technical diagnostic summary for engineering commit
`8c56f34f7c2e1de5f63743a0ab5f3f48e18826c9`. Repetitive output is collapsed;
no credentials, secrets, raw transcript, or private chain-of-thought is stored.

## 1. GitHub handoff and branch setup

Initial local state:

```text
git status --short --branch
git branch --show-current
git rev-parse HEAD
git remote -v
```

Result: exit `0`; clean `fix/text-segmentation-forensic` at `3453203`.

First network preflight:

```text
git remote show origin && ...
```

Result: exit `128`:

```text
fatal: unable to access GitHub: Could not resolve host: github.com
```

Remediation: repeated the same read-only network checks with approved network
access. Result: exit `0`; `origin` was
`https://github.com/alexsmolya/fb2-silero-audiobook.git`, default branch `main`,
ordinary push dry-run succeeded, and `gh` authentication was valid. No token
value was recorded.

`gh repo view` without explicit repository resolved the configured upstream
`saabst/book-v2-audio`; decision: use the actual Git push remote `origin` as the
handoff repository.

Created and committed the first handoff infrastructure as `e9e2507`, then:

```text
git push -u origin fix/text-segmentation-forensic
```

Result: exit `0`; new remote branch created. No PR was opened.

After the user added the two-level reporting requirement, the retrospective
report was renamed to `_REPORT.md`, a diagnostic `_RUNLOG.md` was added, and
`LATEST.md`/README were updated in `7746c01`, then pushed successfully.

Pause branch setup:

```text
git switch -c fix/pause-policy-forensic
git cherry-pick 7746c016f14dc14b737c3485d53775dda466f67a
```

Result: exit `0`; equivalent protocol sync commit `8c29e85` on the pause branch.

## 2. Architecture and artifact inspection

Read relevant sections/files with grouped `sed`/`rg` commands:

- `analysis/REPORT.md`
- `analysis/analyze_silence.py`
- `analysis/silences.csv`, `segment_pauses.csv`, `silence_stats.json`,
  `segments.csv`, `chapters.csv`, `human_text_anchors.jsonl`
- `src/core/audio_assembler.py`, `pipeline.py`, TTS backends, and tests

Findings:

- chapter assembly uses one ffmpeg filter graph;
- every tuple was `(audio_path, additive_pause_before)`;
- old pipeline supplied `0.3 s` before every main segment, including the first;
- chapter WAV is PCM16 mono 22,050 Hz;
- final book assembly separately inserted `1.5 s` between chapter WAV files;
- Silero already had punctuation-dependent leading/trailing silence;
- paragraph/title boundary types were no longer available at assembly;
- before/after comment pause targets were applied on the wrong sides.

## 3. Cached pause analysis

A read-only Python aggregation joined `segments.csv` and
`segment_pauses.csv`. Exit `0`.

Exact old final / inferred natural adjacent-edge medians:

```text
ordinary:    0.596 / 0.296 (n=5727)
question:    0.789 / 0.489 (n=438)
exclamation: 0.664 / 0.364 (n=479)
ellipsis:    0.596 / 0.296 (n=240)
dialogue:    0.725 / 0.425 (n=3588, overlapping classification)
paragraph:   0.612 / 0.312 (n=3028, overlapping classification)
```

The inferred edge value is exact detected boundary duration minus the proven
`0.300 s` insertion.

Human cached evidence:

```text
all silences: n=15974, p25=0.147, median=0.261, p75=0.414
chapter boundary: n=20, p25=2.139, median=2.179, p75=2.231
```

A low-confidence three-ASR-anchor piecewise mapping selected nearest human
silences within `0.20 s`: 1,540 matches, median anchor distance `0.10 s`.
Ordinary/dialogue/paragraph medians were 0.267/0.255/0.275 s; punctuation
subclasses had only 11–13 samples. Decision: use these only as order-of-
magnitude evidence and not fabricate precise title/punctuation human targets.

## 4. Implementation decisions

- Preserve structural boundary markers via `StructuredSegment` until assembly.
- Classify structure before punctuation: chapter start, title-body, paragraph,
  then dialogue/question/exclamation/ellipsis/ordinary.
- Add only final-silence deficit; never trim audio.
- Measure Silero PCM16 WAV edges once before existing MP3 conversion and store
  validated JSON sidecars.
- Use `-45 dB`, minimum `0.04 s`, maximum recorded edge `1.50 s`.
- Preserve the user ordinary-pause setting as baseline; differentiate other
  targets by fixed evidence-based offsets.
- Adapt chapter WAV edges to a separate `2.10 s` final target; retain `1.5 s`
  fallback padding when metadata is unavailable.
- Missing/invalid segment sidecar uses full target padding.

## 5. Tests and intermediate issue

Initial focused integration after implementation:

```text
.venv/bin/python -m pytest -q tests/test_audio_assembler.py \
  tests/test_sentence_splitter_characterization.py \
  tests/test_silero_pronunciations.py tests/test_global_progress.py \
  tests/test_cancellation.py
```

Result: exit `0`, `57 passed`, 9 subtests.

Expanded pause/pipeline suite result: exit `0`, `125 passed`, 51 subtests.

While selecting the real fixture, splitter output showed standalone
`******!` had disappeared because punctuation-only filtering ran before Silero
normalization. This was a functional regression from the prior task, not a
pause-policy choice. Decision: treat only obvious 2+ asterisk mask patterns as
speech-bearing; retain the `— …` filter. Regression test added.

Real-FB2 structural recheck after the fix:

```text
segments: 6906 -> 7053
punctuation-only: 0
mixed-terminal misses: 0
interrobang misses: 0
duplicate heading: 0
raw asterisks after Silero preprocessing: 0
censor segments preserved: 15
identifier/clock regressions: 0
```

## 6. CUDA/model checks and short A/B

Initial restricted checks reported `torch.cuda.is_available() == False` and
`nvidia-smi` could not communicate with the driver. This was an environment
restriction, not a missing GPU. Approved host checks then returned:

```text
NVIDIA GeForce RTX 3050 Laptop GPU
torch.cuda.is_available() == True
```

The active local model was valid `v5_5_ru` (145,420,684 bytes), and the wrapper
already contained the same model file. No download or network model access was
needed.

One approved local GPU command synthesized 24 segments once and assembled the
same MP3s twice. Result: exit `0`. Repetitive per-segment wrapper logs were
omitted:

```text
[full repetitive Silero progress omitted; 24/24 segments synthesized]
model=v5_5_ru voice=xenia device=cuda
legacy duration=80.201043 s
adaptive duration=75.469252 s
```

Artifacts outside Git:

```text
analysis/pause_ab_2026-08-08/before_legacy_0.3.wav
analysis/pause_ab_2026-08-08/after_adaptive.wav
analysis/pause_ab_2026-08-08/manifest.json
```

Cached `silencedetect=-45dB:d=0.04` matched 23/23 boundaries:

```text
digital padding: 7.200 -> 2.468 s
median boundary: 0.594 -> 0.450 s
p25/p75: 0.571/0.609 -> 0.339/0.477 s
boundaries >=0.5 s: 22/23 -> 4/23
```

Dialogue adaptive median remained `0.558 s` because existing natural silence
already exceeded the `0.38 s` target. No trim/clipping was applied.

## 7. Final verification and Git

Final full check:

```text
.venv/bin/python -m pytest -q
.venv/bin/python -m compileall -q src tests
git diff --check
```

Result: exit `0`; `288 passed`, 51 subtests. Two non-fatal existing environment
warnings remained: restricted NVML initialization during sandbox tests and an
installed packaged Torch `SyntaxWarning`. Focused final tests passed `55`, plus
7 subtests.

Code commit:

```text
git commit -m "fix: adapt pauses to existing TTS silence"
```

Result: exit `0`; `8c56f34f7c2e1de5f63743a0ab5f3f48e18826c9`, 8 files,
553 insertions, 14 deletions.

The compact report, this run log, and `LATEST.md` were committed afterward and
pushed with `fix/pause-policy-forensic`. No full-book synthesis, PR, merge,
force-push, remote-history rewrite, dependency change, or binary Git artifact
was created.
