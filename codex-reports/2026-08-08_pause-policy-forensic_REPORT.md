# Forensic target-final-silence pause policy

## Task and initial state

Replace blindly added per-segment `0.3 s` silence with a measured
target-final-silence policy, while preserving punctuation prosody, structural
FB2 boundaries, chapter separation, and the completed text-segmentation fixes.

- Repository: `alexsmolya/fb2-silero-audiobook`
- Base branch: `fix/text-segmentation-forensic`
- Engineering base SHA: `e9e25071574e91639e1b05cce837c7581278f139`
- Required text-fix ancestor: `345320389e2b9ee584ae4b81145e8dfa5a985947`
- Protocol sync commit on this branch: `8c29e85`
- Working branch: `fix/pause-policy-forensic`
- Final engineering commit: `8c56f34f7c2e1de5f63743a0ab5f3f48e18826c9`
- Push target: `origin/fix/pause-policy-forensic`
- Push status: pushed normally; no PR, merge, rebase, or force-push

The original forensic run had 6,906 TTS segments. Every segment received
`0.300 s` digital silence before its audio. Detected final boundary silence was
median `0.598 s`; 6,900/6,906 boundaries were at least `0.5 s`. Human detected
silence was median `0.261 s` across 15,974 intervals.

## Evidence and human reference

Reused without repeating ASR:

- `analysis/REPORT.md`
- `analysis/silences.csv`
- `analysis/segment_pauses.csv`
- `analysis/silence_stats.json`
- `analysis/segments.csv`
- `analysis/chapters.csv`
- `analysis/human_text_anchors.jsonl`

Exact cached distributions:

| Source/class | n | p25 | median | p75 | Confidence |
| --- | ---: | ---: | ---: | ---: | --- |
| Human, all detected silences | 15,974 | 0.147 | 0.261 | 0.414 | high |
| Human, inter-track chapter boundary | 20 | 2.139 | 2.179 | 2.231 | high |
| Old Silero final ordinary boundary | 5,727 | 0.579 | 0.596 | 0.682 | high |
| Old Silero inferred natural ordinary edges | 5,727 | 0.279 | 0.296 | 0.382 | high |
| Old Silero inferred natural question edges | 438 | 0.301 | 0.489 | 0.555 | high |
| Old Silero inferred natural exclamation edges | 479 | 0.288 | 0.364 | 0.517 | high |
| Old Silero inferred natural ellipsis edges | 240 | 0.261 | 0.296 | 0.439 | high |

The Silero natural-edge values are exact arithmetic from detected final silence
minus the proven `0.300 s` digital insertion.

Human class-specific alignment is not word-level. A conservative piecewise
three-anchor/nearest-silence subset gave ordinary `n=556, median=0.267`,
dialogue `n=271, median=0.255`, and paragraph `n=677, median=0.275`; question,
exclamation, and ellipsis samples were only 13/12/11. These are low-confidence
order-of-magnitude checks and were not treated as exact optimization targets.
Title-to-body human timing was not sufficiently aligned to claim a measured
distribution.

## Implemented policy

For adjacent generated segments:

```text
added_padding = max(0, target_final_silence
                       - previous_trailing_silence
                       - current_leading_silence)
```

No audio is trimmed. A read-only PCM16 WAV detector uses `-45 dB`, requires at
least `0.04 s`, and bounds recorded edge silence at `1.50 s`. Silero measures
its WAV once before MP3 conversion and writes a small validated sidecar; this
avoids thousands of extra ffmpeg probe processes. Missing/invalid metadata
falls back conservatively to full target padding.

Default final targets:

| Boundary | Target seconds |
| --- | ---: |
| Ordinary sentence | 0.30 |
| Question | 0.45 |
| Exclamation | 0.38 |
| Ellipsis | 0.45 |
| Dialogue transition | 0.38 |
| Paragraph | 0.45 |
| Title → body | 0.75 |
| Chapter boundary | 2.10 |

The existing `pause_between_sentences` setting remains the ordinary baseline;
changing it shifts non-chapter targets by the same delta. Chapter separation is
independent and adapts measured chapter WAV edges to the `2.10 s` final target.

Structural boundary metadata is retained from the splitter through assembly.
The pre-existing comment pause order bug was corrected: before-comment and
after-comment targets now apply on the correct sides.

## Changed files

- `src/core/pause_policy.py`
- `src/core/audio_assembler.py`
- `src/core/pipeline.py`
- `src/core/sentence_splitter.py`
- `src/core/tts_silero.py`
- `tests/test_pause_policy.py`
- `tests/test_audio_assembler.py`
- `tests/test_sentence_splitter_characterization.py`

## Verification

- Focused final tests: `55 passed`, 7 subtests.
- Full final suite: `288 passed`, 51 subtests.
- `python -m compileall -q src tests`: passed.
- `git diff --check`: passed.
- No full-book generation and no model download.

Regression coverage includes enough-existing-silence, exact deficit, no
negative padding, all required boundary classes, separate chapter policy,
minimum/maximum detector bounds, source-byte preservation/no clipping,
sidecar validation, comment ordering, punctuation-only filtering, preserved
censor sound, and previous text segmentation behavior.

## Real short A/B

One 24-segment, 1,160-character, 80-second fixture was synthesized once with
installed `v5_5_ru`, voice `xenia`, CUDA. The same MP3 segments were assembled
with legacy and adaptive policies. Samples and manifest are outside Git at:

`analysis/pause_ab_2026-08-08/`

| Metric | Legacy | Adaptive |
| --- | ---: | ---: |
| Duration | 80.201 s | 75.469 s |
| Added digital padding | 7.200 s | 2.468 s |
| Boundary silence p25 | 0.571 s | 0.339 s |
| Boundary silence median | 0.594 s | 0.450 s |
| Boundary silence p75 | 0.609 s | 0.477 s |
| Boundaries ≥ 0.5 s | 22/23 | 4/23 |

All 23 boundaries matched cached `silencedetect` intervals. Adaptive medians by
class were ordinary `0.306 s` (`n=7`), paragraph `0.451 s` (`n=8`), question
`0.451 s`, exclamation `0.380 s` (`n=2`), ellipsis `0.487 s`, title-body
`0.752 s`, and dialogue `0.558 s` (`n=3`). Dialogue remained above its target
where Silero already produced longer natural silence; it was not trimmed.

## Failures, limitations, unresolved issues

- No blocking failure remains. CUDA visibility required running the local A/B
  outside the restricted sandbox; the model and GPU were already installed.
- Edge metadata is currently produced by Silero. Other backends safely fall
  back to adding the full target and are not yet edge-adaptive.
- Detector support is deliberately limited to generated PCM16 WAV input.
- Human per-class distributions remain low confidence without forced word
  alignment; title-body has no defensible human distribution.
- The A/B covers one voice/model and 24 segments, not subjective listening or a
  full book.
- Model-only stress/intonation and mixed-script `Y-хромосомы` remain separate.

During validation, standalone `******!` was found to be dropped before Silero
normalization. The narrow regression was fixed: obvious 2+ asterisk masks are
speech-bearing and become a censor sound, while punctuation-only `— …` remains
filtered. Current structural validation retains 15 censor segments and sends
zero raw asterisks to the Silero wrapper.

## Recommended next step

Perform a listening review of the two short samples, then consider extending
edge metadata to other backends. Keep model-only pronunciation/prosody as a
separate task.
