# Text segmentation forensic fixes

## Task

Fix the first group of deterministic FB2-to-Silero text pipeline defects
proved by the Book 7 forensic analysis, without changing the global pause
policy, audio encoding, model/voice/device logic, or model-only prosody.

## Repository state

- Repository: `alexsmolya/fb2-silero-audiobook`
- Push remote: `origin`
- Remote URL: `https://github.com/alexsmolya/fb2-silero-audiobook.git`
- Remote default branch: `main`
- Base branch: `feat/pronunciation-corrections`
- Base SHA: `4694e66b0591a5028415bac243a5827434f7e072`
- Working/source branch: `fix/text-segmentation-forensic`
- Task commit: `345320389e2b9ee584ae4b81145e8dfa5a985947`
- Source branch pushed: yes, as `origin/fix/text-segmentation-forensic`

The task branch was intentionally based on the then-current verified HEAD,
which already contained the pronunciation and ellipsis work used by the
forensic run. It was not rebased onto the older `main`.

## Evidence used

- `analysis/REPORT.md`
- `analysis/segments.csv`
- Real source: `07 Гимн шута - 07.fb2`
- Existing parser, splitter, pipeline, Silero wrapper integration, and tests

The human audiobook had already been verified as the same book with minor
textual differences (21/21 chapters and 63/63 distributed anchors matched), so
the deterministic findings were accepted as a valid correction basis.

## Implementation

- Preserved FB2 title and paragraph structure through segmentation instead of
  joining chapter paragraphs with ordinary spaces before splitting.
- Made structural titles independent from the first body paragraph.
- Rejected fragments with no alphanumeric speech content before TTS inference.
- Added conservative boundaries for `?..`, `!..`, and clear next sentences
  after `⁈`; dialogue-attribution forms such as `Что⁈ — спросил он` stay intact.
- Canonicalized only heading comparison for insignificant whitespace, case,
  and proven leading decoration such as `.Глава 16`.
- Protected censored asterisk patterns before the Silero wrapper. Standalone
  masks become `пик`; masked letters become an ellipsis; literal `2 * 3` stays
  literal.
- Protected identifier suffixes with leading zero: `80−03` and `80-03` become
  `80 дефис ноль три` before wrapper digit conversion.
- Normalized clock-like dotted notation only with a leading-zero hour or an
  explicit time cue. `Выезд в 9.30` becomes `Выезд в 9 30`; ordinary `3.14`
  keeps prior decimal behavior.
- Normalized `⁈` to `?!` before Silero wrapper processing.
- Cached a failed spaCy model-load attempt so per-paragraph fallback does not
  repeatedly retry or flood logs.

## Changed files

- `src/core/fb2_parser.py`
- `src/core/pipeline.py`
- `src/core/sentence_splitter.py`
- `src/core/tts_silero.py`
- `tests/test_fb2_parser.py`
- `tests/test_sentence_splitter_characterization.py`
- `tests/test_silero_pronunciations.py`

## Verification

- Focused parser/splitter/Silero regression tests passed.
- Full suite: `268 passed`, `51 subtests passed`.
- `python -m compileall -q src tests`: passed.
- `git diff --check`: passed.
- No full-book synthesis and no model download were performed.

Dry structural validation against the real Book 7 FB2 and the original
forensic segment CSV:

| Metric | Before | After |
| --- | ---: | ---: |
| Paragraph-crossing speech segments | 134 | 0 |
| Merged chapter headings | 22 | 0 |
| Punctuation-only speech segments | 10 | 0 |
| Missed clear `?..` / `!..` boundaries | 13 | 0 |
| Missed clear `⁈` boundaries | 32 | 0 |
| Duplicate `.Глава 16` | 1 | 0 |
| Segments exposed to wrapper asterisk spelling | 15 | 0 |
| Lossy `80−03` occurrences | 2 | 0 |
| Decimalized clock `9.30` occurrences | 1 | 0 |

The deterministic speech-segment count changed from 6,906 to 7,051 because
structural and terminal boundaries are now retained.

## Limitations and unresolved findings

- The unconditional `0.3 s` inter-segment pause policy was deliberately not
  changed here.
- No claims were made about model-only stress, intonation, or listening quality.
- Mixed-script `Y-хромосомы` remained a follow-up candidate.
- Clock detection is intentionally conservative rather than a universal number
  parser.

## Recommended next task

Design and validate a target-final-silence pause policy using existing Silero
edge silence, boundary types, forensic pause artifacts, and a short A/B sample.
