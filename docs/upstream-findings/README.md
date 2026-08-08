# Russian TTS findings from real-world audiobook generation

## Scope

These findings came from using
[fb2-silero-audiobook](https://github.com/alexsmolya/fb2-silero-audiobook)
to generate Russian audiobooks. Output anomalies were first found by listening,
then investigated in the text-processing and audio-assembly pipeline. The fixes
have regression coverage; pronunciation changes were also checked by human A/B
listening. No book title, source text, generated audio, or diagnostic log is
needed to reproduce the technical cases below.

## Project and attribution

The findings originate from the public `fb2-silero-audiobook` project maintained
by its repository owner. The maintainer discovered the pronunciation defects and
other output anomalies through real-world listening and testing. Technical
investigation, code analysis, implementation, and regression-test development
were performed with assistance from ChatGPT and OpenAI Codex. The resulting fixes
were validated with automated regression tests and, for pronunciation or output
quality, human A/B listening.

The provenance is therefore: human real-world observation and listening,
AI-assisted technical investigation and implementation, automated regression
testing, and human listening validation.

## Environment

The repository pins `silero-tts==0.0.5` and uses the Russian Silero model ID
`v5_5_ru`. Its verified Russian voices are `xenia` and `eugene`. Python, PyTorch,
and torchaudio are pinned elsewhere in the project, but they are not material to
the preprocessing findings below. FFmpeg is a system dependency and its version
is not pinned by the repository.

## Finding 1: unsafe Russian abbreviation regex in `silero-tts` preprocessing

### Observed problem

Ordinary Russian input such as `на этот вопрос` and `на эшафот` could be changed
before it reached the neural TTS model.

### Root cause and minimal reproduction

In `silero-tts==0.0.5`, the Russian abbreviation patterns for `н. э.` and
`д. н. э.` used unescaped dots:

```python
r"н.\s*э."
r"д.\s*н.\s*э."
```

In a regular expression, `.` matches any character. Consequently, the shorter
pattern matches the ordinary prefix `на эт` in `на этот вопрос`; applying the
wrapper's expansion leaves a corrupted result beginning `нашей эрыот ...`.
It similarly matches the beginning of `на эшафот`.

The application hardens only those known wrapper patterns by replacing them with
literal dots and word boundaries:

```python
r"(?<!\w)н\.\s*э\.(?!\w)"
r"(?<!\w)д\.\s*н\.\s*э\.(?!\w)"
```

This preserves ordinary words while retaining both spaced and unspaced forms of
the abbreviations. See the
[implementation](https://github.com/alexsmolya/fb2-silero-audiobook/blob/6be1d04f34ad5649b6e80c6b4d0599723c624b3a/src/core/tts_silero.py#L52-L78)
and the
[regression test](https://github.com/alexsmolya/fb2-silero-audiobook/blob/6be1d04f34ad5649b6e80c6b4d0599723c624b3a/tests/test_silero_pronunciations.py#L39-L59).

**This is a wrapper preprocessing defect. It is not evidence of a Silero neural
model pronunciation failure.**

## Finding 2: reproducible context-dependent Russian stress cases

Several listening failures were reproducible in context and corrected with
explicit Silero stress marks:

| Minimal context | Applied form | Why the override is contextual |
| --- | --- | --- |
| `под это определение не попадало` | `попад+ало` | `попадало` can represent different lexical/grammatical readings. |
| `испугался он явно не боли` | `б+оли` | `боли` can be a noun or an imperative, with different stress. |
| `глотнув воды`, `глотнуть воды`, `вкусной воды` | `вод+ы` | `воды` has different normative stress depending on form and meaning. |
| `заморозки` | `замор+озки` | The observed noun form needed an explicit stress mark. |

These are observed, context-specific cases, not a universal Russian stress
dictionary. The application uses phrase-level overrides and word boundaries;
tests also verify that unrelated readings such as `яблоко попадало с дерева`,
`Боли сильнее!`, and `минеральные воды` remain unchanged. The
[rules](https://github.com/alexsmolya/fb2-silero-audiobook/blob/6be1d04f34ad5649b6e80c6b4d0599723c624b3a/pronunciations.toml#L83-L93)
and
[regression assertions](https://github.com/alexsmolya/fb2-silero-audiobook/blob/6be1d04f34ad5649b6e80c6b4d0599723c624b3a/tests/test_silero_pronunciations.py#L161-L188)
show the exact scope. These examples may be useful to Silero maintainers when
evaluating automatic stress and homograph handling.

## Finding 3: duplicate FB2 chapter headings

Some FB2 documents contain a structural title such as
`<title><p>Chapter N</p></title>` and repeat the same text in the first body
paragraph. Because the parser's descendant paragraph search also includes the
paragraph inside `<title>`, the old path could send both copies to TTS.

The application now removes only consecutive copies of the structural title at
the very start of a chapter. Comparison ignores case and insignificant whitespace;
the same paragraph later in the chapter remains intact. See the
[parser implementation](https://github.com/alexsmolya/fb2-silero-audiobook/blob/6be1d04f34ad5649b6e80c6b4d0599723c624b3a/src/core/fb2_parser.py#L178-L197)
and its
[regression test](https://github.com/alexsmolya/fb2-silero-audiobook/blob/6be1d04f34ad5649b6e80c6b4d0599723c624b3a/tests/test_fb2_parser.py#L8-L32).

**This is an application/FB2 parser issue, not a Silero issue.**

## Finding 4: FFmpeg 9 integration compatibility

The real-world validation environment exposed an incompatibility in the
application's chapter-assembly invocation. The application previously passed the
filter graph through `-filter_complex_script`; it now passes the same generated
graph directly with `-filter_complex`. The regression test checks the exact
argument and graph supplied to FFmpeg. See the
[implementation](https://github.com/alexsmolya/fb2-silero-audiobook/blob/6be1d04f34ad5649b6e80c6b4d0599723c624b3a/src/core/audio_assembler.py#L200-L215)
and
[test](https://github.com/alexsmolya/fb2-silero-audiobook/blob/6be1d04f34ad5649b6e80c6b4d0599723c624b3a/tests/test_audio_assembler.py#L61-L93).

Because FFmpeg is system-provided rather than pinned, this is evidence for the
tested FFmpeg 9 environment, not a claim about every FFmpeg 9 installation.

**This is application/FFmpeg integration, not a Silero issue.**

## Verification

At publication time, `.venv/bin/python -m pytest -q` completed with **256 passed,
44 subtests passed**, and two non-failing warnings. `git diff --check` also passed.
The pronunciation changes were additionally accepted through human A/B listening;
local audio and JSONL diagnostics are intentionally not published as evidence.

## Relevant implementation

All four changes are collected in
[`6be1d04f34ad5649b6e80c6b4d0599723c624b3a`](https://github.com/alexsmolya/fb2-silero-audiobook/commit/6be1d04f34ad5649b6e80c6b4d0599723c624b3a)
(`fix: improve Russian TTS preprocessing and chapter handling`). The links above
are commit-pinned permalinks to the corresponding implementation and tests.

## Upstream usefulness

- **`silero-tts` wrapper maintainers:** unsafe abbreviation-regex reproduction,
  a boundary-safe literal-dot replacement, and a regression test.
- **Silero maintainers:** real context-dependent Russian stress examples for
  evaluating automatic stress and homograph handling. The report does not claim
  that the application overrides form a general-purpose dictionary.
- **This application only:** conservative FB2 chapter-heading deduplication and
  the FFmpeg command-line integration change.
