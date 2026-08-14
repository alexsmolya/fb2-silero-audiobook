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

## Finding 5: Un-yoified text corpus and context-dependent Russian homographs (`все ↔ всё`)

### Observed problem

In real-world Russian FB2 books, printed text is overwhelmingly un-yoified (e.g. 298 out of 298 instances of `все`/`всё` written as `все` with letter `е`). When passed directly to Silero TTS, errors occurred in both directions:
1. **Under-yoification**: Idioms like `все же` (meaning `всё же`), `все равно`, `все-таки`, `все время`, `все еще` remained un-yoified as `все же`, because Silero's accentor did not infer `всё` from plain `все`.
2. **Over-yoification**: Plural subjects before plural verbs in long sentences (e.g. `Убедившись, что все ознакомились...`) were mis-yoified by Silero's accentor (`put_yo_homo=True`) into `вс+ё ознакомились` instead of `вс+е`.

### Root cause and minimal reproduction

```python
from silero_tts.silero_tts import SileroTTS

tts = SileroTTS(model_id="v5_5_ru", language="ru", speaker="eugene", sample_rate=48000, device="cpu")
p_id = tts.tts_model.speaker_to_package.get("eugene")
pkg = tts.tts_model.packages[p_id]

# Mis-yoification bug in Silero homograph accentor for long plural sentences:
text = "Убедившись, что все ознакомились с посланием, Волконская открыла прикрепленное к нему фото."
result = pkg.accentor(text, put_stress=True, put_yo=True, put_yo_homo=True)
# Result: 'Убед+ившись, чт+о вс+ё ознак+омились...' (erroneously converts plural 'все' to 'вс+ё')
```

### Application resolution

The application implements a context-aware homograph preprocessor that:
- Resolves unambiguous adverbs and idioms (`всё же`, `всё равно`, `всё-таки`, `всё время`, `всё еще`, `всё больше`, `всё это`).
- Adds explicit protective stress `вс+е` for plural subjects before plural verbs (`все ознакомились`, `все пришли`, `все выпили`). Silero's accentor strictly respects explicit stress `вс+е` and preserves `вс+е`.
- Preserves explicit `всё` and plain `все` in non-matching contexts without performing a global replacement.

See the
[implementation](https://github.com/alexsmolya/fb2-silero-audiobook/blob/ae3da72cfc926153384ac2c762055a437c15120d/src/core/tts_silero.py#L162-L225)
and
[regression tests](https://github.com/alexsmolya/fb2-silero-audiobook/blob/ae3da72cfc926153384ac2c762055a437c15120d/tests/test_silero_pronunciations.py#L270-L294).

## Finding 6: Russian stress dictionary entries and proper names

### Observed problem and root cause analysis

Listening validation identified five specific stress anomalies:

1. **`туше`**: Silero accentor defaults to `т+уше` (1st syllable). Normative pronunciation is `туш+е` (2nd syllable). **(Upstream dictionary candidate)**
2. **`второй`**: Silero accentor defaults to `вт+орой` (1st vowel), which sounds like `втОрый`. Normative pronunciation is `втор+ой`. **(Upstream dictionary candidate)**
3. **`Валерыч`**: Silero accentor defaults nominative form to `В+алерыч` (1st syllable), while oblique forms (`Валерыча`, `Валерычу`) are accented on 2nd syllable (`Вал+ерыча`). Normative colloquial patronymic is `Вал+ерыч`. **(Upstream dictionary candidate)**
4. **`Максим`**: Silero accentor defaults to `Макс+им`, but standalone exclamations like `— Максим!` can receive falling pitch contour on `мАксим`. Adding explicit dictionary rule `"Максим" = "Макс+им"` ensures consistent stress across sentence positions. **(Application pitch contour control)**
5. **`один в один`**: The phrase `один в один` was synthesized without phrase-level stress on the second word, sounding like proper name `Один`. The application adds a phrase context rule `один в один` -> `один в од+ин` while protecting the proper name / Norse god `Один` (`Бог Один...` -> `Од+ин`) and single `один`. **(Application phrase context rule)**

See the
[dictionary rules](https://github.com/alexsmolya/fb2-silero-audiobook/blob/ae3da72cfc926153384ac2c762055a437c15120d/pronunciations.toml#L95-L125),
[phrase preprocessor implementation](https://github.com/alexsmolya/fb2-silero-audiobook/blob/ae3da72cfc926153384ac2c762055a437c15120d/src/core/tts_silero.py#L225-L228),
and
[regression tests](https://github.com/alexsmolya/fb2-silero-audiobook/blob/ae3da72cfc926153384ac2c762055a437c15120d/tests/test_silero_pronunciations.py#L295-L340).

## Verification

At publication time, `.venv/bin/python -m pytest -q` completed with **292 passed, 51 subtests passed**, and one non-failing warning. `git diff --check` also passed with zero errors. All pronunciation changes were accepted through human A/B listening validation.

## Relevant implementation

The implementation is committed in
[`ae3da72cfc926153384ac2c762055a437c15120d`](https://github.com/alexsmolya/fb2-silero-audiobook/commit/ae3da72cfc926153384ac2c762055a437c15120d)
(`fix(tts): resolve Russian homographs and pronunciation accenting`). The links above
are commit-pinned permalinks to the corresponding implementation and tests.

## Upstream usefulness

- **`silero-tts` wrapper maintainers:** unsafe abbreviation-regex reproduction,
  a boundary-safe literal-dot replacement, and a regression test.
- **Silero maintainers:** real context-dependent Russian stress examples for
  evaluating automatic stress and homograph handling (including `все ↔ всё` mis-yoification and default dictionary candidates `туше`, `второй`, `Валерыч`).
- **This application only:** conservative FB2 chapter-heading deduplication, FFmpeg command-line integration, and context-aware phrase rules (`один в один`).
