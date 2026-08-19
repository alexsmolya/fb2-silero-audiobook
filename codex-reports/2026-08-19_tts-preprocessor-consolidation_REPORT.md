# TTS preprocessor consolidation — review handoff

## Status

Implementation complete locally. Engineering verdict: `READY_FOR_REVIEW`.

- Repository: `alexsmolya/fb2-silero-audiobook`
- Starting branch/SHA: `main` / `9fd35745ba294bd455307e90144b20169d52ee34`
- Resulting engineering branch/SHA: `feat/tts-preprocessor-consolidation` / `ca443da718cbacb85790f807a0e82acac3f685ba`
- Implementation commit: `34033a8 feat: consolidate deterministic TTS preprocessing`
- Source FB2 files are not modified.

## What changed

`src/core/tts_preprocessor.py` is now the explicit deterministic compiler for
structured FB2 chapters. It preserves source structure, applies the existing
Silero-safe rules and narrow confirmed contextual rules before segmentation,
and emits `ChangeRecord` entries. `pipeline.py` writes the normalized script
and machine-readable change log, then segments the normalized paragraphs.

The Silero backend retains compatibility imports, while the preprocessing
implementation is owned by the new stage. Non-Silero backends remain a no-op
at this stage. Pause policy, model silence handling, FFmpeg sample padding,
and segment ordering logic were not changed.

## Rule inventory summary

The canonical cross-source inventory is
`docs/tts-preprocessor/RULE_INVENTORY.md`; architecture is documented in
`docs/tts-preprocessor/ARCHITECTURE.md`.

| Group | Count/status |
|---|---:|
| Existing rule/structural families preserved and represented in the compiler | 36 |
| Existing families migrated to the explicit preprocessor | 36 |
| Newly implemented confirmed narrow rules | 18 |
| Intentionally unresolved/deferred classes or findings | 4 |

The 18 new rules cover the confirmed journal forms for `обречённо`,
`два с половиной часа`, `набралось`, negative `не было`, contextual `потом`,
`глаза`, day-of-week `среду`, lock `замок`, `статью`, `не с чем`, `высоты`,
`стрелку`, `хлопок`, `стены`, `нападавших`, `родов`, `лица`, and the explicit
book-profile `Галицын` forms. Existing `всё/все`, dictionary stress, censor,
identifiers, clock notation, interrobang, abbreviation hardening, heading
normalization, FB2 structure, and prior segmentation/pause/audio safeguards
are retained.

Deferred items are: expressive long-vowel production transformation,
acronym classification without an explicit lexicon, universal `Борисович`
handling, and global `какого хера` stress. The code has an experimental
elongation detector and explicit acronym resolver, but neither changes normal
production text. `Галицын` is a project/book profile override, not a universal
surname rule.

## Journal and prior evidence

The 2026-08-18 Drive journal was read directly, along with the three available
2026-08-14 Drive handoffs. The journal's architecture requirements and the
listed confirmed listening cases were found and incorporated where safe. The
journal did not provide a confirmed universal `Борисович` rule; the existing
repository also had no such implementation, so it remains explicit debt.
The journal's warnings against global `ALL_CAPS`, global `хЕра`, blanket
patronymic regexes, and long-vowel heuristics were honored.

## Validation

- Baseline focused suite before changes: 59 passed, 1 warning, 7 subtests.
- New preprocessor suite: 10 passed.
- Focused regression suite: **69 passed, 1 warning, 7 subtests passed**, exit 0.
- Full suite: **302 passed, 2 warnings, 51 subtests passed**, exit 0.
- `python -m compileall -q src tests`: exit 0.
- `uv lock --check`: exit 0 (`Resolved 123 packages`).
- `git diff --check`: exit 0.
- Local model availability check: `v5_5_ru` found at the existing local cache.

## Real book 09/10 forensic pass

The corpus paths were confirmed locally and were not copied into Git. The
row-level audit is `docs/tts-preprocessor/BOOK09_10_CORPUS_AUDIT.md` with JSON
sidecar `docs/tts-preprocessor/BOOK09_10_CORPUS_AUDIT.json`. It contains 1072
target rows: 533 from book 9 and 539 from book 10. The source and normalized
paragraph counts are unchanged: 2819/2819 and 2872/2872.

| Metric | Book 9 | Book 10 |
|---|---:|---:|
| Chapters | 23 | 28 |
| Segments | 6394 | 6387 |
| Paragraph crossings | 0 | 0 |
| Accidental title/body merges | 0 | 0 |
| Intended title/body boundary cases | 23 | 28 |
| Punctuation-only / empty segments | 0 / 0 | 0 / 0 |
| Very-short segments (<12 chars) | 291 | 305 |
| Very-long segments (>1200 chars) | 0 | 0 |
| Dialogue boundary samples | 14 | 14 |

The real corpus exposed and fixed two defects: the lock resolver previously
discarded modifiers (`дверной замок`), and the day-of-week resolver only
covered `в среду`, missing `проводишь свою среду`. The new rules preserve all
lexical tokens. A corpus-wide token audit found no non-heading, non-censor
lexical loss; remaining heading differences are the intentional chapter-number
normalization.

The local ignored forensic directory is `forensic-output/book09-10/` and
contains five approximate MP3 localization clips plus the real-context
long-vowel A/B directory. MP3 localization is paragraph-ratio based; it is
not reliable alignment and cannot establish stress.

## Artifact and audio smoke

A short pipeline smoke produced:

- `/tmp/audiobook-tts-smoke.pY6a0m/smoke-book.tts.md` (316 bytes)
- `/tmp/audiobook-tts-smoke.pY6a0m/smoke-book.tts-changes.json` (1764 bytes)
- 2 segment rows and 3 traceable change records.

The real-context long-vowel smoke used the existing local Silero model and
generated 16 MP3 fragments under `forensic-output/book09-10/long-vowel-real-context/`:
four actual FB2 phrases, each with original/3/4/5-vowel candidates. Examples
include `Да-а-а-ай`, `Но-о-ормально`, `о-о-очень`, and `да-а-а-а-а`. Synthesis
succeeded; automated output cannot establish perceptual quality, so the
production transform remains opt-in/unresolved. No FB2 or full-book MP3 was
added to Git.

## Limitations and review focus

- `source_offsets` are reserved in the change schema but are currently null;
  stable source and paragraph IDs are present.
- Resumed/partial chapter runs write artifact segment rows for processed
  chapters; the normalized book and changes remain available from the initial
  compiler write.
- The first live network check failed with DNS resolution, then the authorized
  normal push succeeded through the approved network path.

Suggested review focus: contextual-rule narrowness and negative controls,
paragraph provenance through `SentenceSplitter`, artifact traceability, and
the unchanged pause/audio paths.

## Git/publication

At handoff the worktree is clean and the feature branch is published at
`origin/feat/tts-preprocessor-consolidation` (`ca443da718cbacb85790f807a0e82acac3f685ba`).
No merge, rebase, force-push, or GitHub action was performed.
