# TTS preprocessing/compiler architecture

The pipeline now has an explicit deterministic text stage between FB2 parsing
and final sentence segmentation:

```text
FB2Parser
  -> ParsedBook (chapters + paragraphs)
  -> TtsPreprocessor.compile_book()
  -> NormalizedBook + ChangeRecord[]
  -> SentenceSplitter.split_chapter_segments()
  -> backend input / audio
```

`TtsPreprocessor` is intentionally offline and deterministic. It owns the
Silero-oriented lexical, phrase, homograph, punctuation, number, censor, and
project-profile rules. It receives whole structured paragraphs, so contextual
rules do not need to cross paragraph boundaries or flatten chapter structure.

The compiler produces stable source IDs (`ch-0001-p-0001`) and records each
transformation with its rule ID, original/normalized text, chapter, paragraph,
source ID, category, and reason. `StructuredSegment` carries the source
paragraph index so the pipeline can extend the trace with stable segment IDs
after segmentation.

For every run, the pipeline writes two persistent artifacts beside the selected
output directory:

- `<input-stem>.tts.md`: readable normalized text grouped by chapter and source
  paragraph, with segment IDs when segmentation has run;
- `<input-stem>.tts-changes.json`: schema-versioned change and segment records.

The Markdown file is diagnostic only; its markup is never sent to a TTS backend.
The original FB2 is parsed read-only and is never rewritten.

Non-Silero backends receive their existing source text unchanged. The current
Silero backend keeps compatibility imports for callers that use its historical
helper functions, while the pipeline owns the stage invocation. Backend-level
Silero wrapper hardening remains isolated from book-level rules.

Project-specific pronunciation is opt-in through an explicit profile. The
pipeline uses the book title as the default profile selector, so the known
`Гимн шута` project override is not a universal surname rule. Long-vowel and
acronym classes are represented in the rule inventory and test architecture,
but have no speculative production transform.

Pause policy, measured edge-silence metadata, diagnostics, and FFmpeg assembly
remain downstream layers. The compiler only adds identity and text traceability;
it does not change pause targets or audio sample arithmetic.
