# TTS preprocessor consolidation — review handoff

## Status

Implementation complete locally. Engineering verdict: `READY_FOR_REVIEW`.

- Repository: `alexsmolya/fb2-silero-audiobook`
- Starting branch/SHA: `main` / `9fd35745ba294bd455307e90144b20169d52ee34`
- Resulting engineering branch/SHA: `feat/tts-preprocessor-consolidation` / `34033a887e797a7cc5a456d9cf589ab0e5b3b8be`
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
- New preprocessor suite: 9 passed.
- Full suite: **301 passed, 2 warnings, 51 subtests passed**, exit 0.
- `python -m compileall -q src tests`: exit 0.
- `uv lock --check`: exit 0 (`Resolved 123 packages`).
- `git diff --check`: exit 0.
- Local model availability check: `v5_5_ru` found at the existing local cache.

## Artifact and audio smoke

A short pipeline smoke produced:

- `/tmp/audiobook-tts-smoke.pY6a0m/smoke-book.tts.md` (316 bytes)
- `/tmp/audiobook-tts-smoke.pY6a0m/smoke-book.tts-changes.json` (1764 bytes)
- 2 segment rows and 3 traceable change records.

The controlled long-vowel smoke used the existing local Silero model and
generated 16 MP3 fragments (2/3/5 repeats for `о`, `а`, `у`, plus seven
expressive phrases) under `/tmp/audiobook-long-vowels.iHFhLA`; its result JSON
is `/tmp/audiobook-long-vowels.iHFhLA/results.json`. Synthesis succeeded, but
there was no automated perceptual evidence of a continuous vowel in this
environment and no human listening step was available. Therefore the result
is `MODEL_LIMITATION/UNRESOLVED`, and no production transform was introduced.

## Limitations and review focus

- `source_offsets` are reserved in the change schema but are currently null;
  stable source and paragraph IDs are present.
- Resumed/partial chapter runs write artifact segment rows for processed
  chapters; the normalized book and changes remain available from the initial
  compiler write.
- A live `git ls-remote origin` check failed with DNS resolution
  (`Could not resolve host: github.com`); local Git is the source of truth.

Suggested review focus: contextual-rule narrowness and negative controls,
paragraph provenance through `SentenceSplitter`, artifact traceability, and
the unchanged pause/audio paths.

## Git/publication

At report creation the worktree contains the implementation commit plus this
report/runlog/LATEST update. No merge, rebase, force-push, or GitHub action was
performed.

