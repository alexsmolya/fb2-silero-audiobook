# FFmpeg large-chapter regression fix

## Outcome

The released adaptive pause implementation could emit a positive, sub-sample
floating-point residue as an FFmpeg duration. FFmpeg 9 rejected the scientific
notation while parsing the filter graph, so chapter 2 never reached audio
processing. Padding is now expressed as an integer count of output samples and
FFmpeg failures expose the diagnostic stderr tail rather than the banner.

- Repository: `alexsmolya/fb2-silero-audiobook`
- Branch: `fix/large-chapter-ffmpeg-assembly`
- Engineering SHA: `bd58a2b77172a986de581ccc5cebfdc38eda33d7`
- Final functional `main` SHA: `bd58a2b77172a986de581ccc5cebfdc38eda33d7`
- Original `main`: `f50930e6b01dcb6423c25c8b44b606704cd97a76`
- Original run: `6d7ca90e`, chapter 2/22, 189 TTS segments

## Exact failure and root cause

The supplied JSONL recorded only the first 500 characters of stderr and then
successfully removed the temporary run directory. It therefore did not retain
the original command, filter graph, edge sidecars, or diagnostic tail. A
minimal reproduction of the exact released calculation and FFmpeg invocation
produced return code 234 and this useful stderr:

```text
[Parsed_atrim_3 @ ...] Unable to parse "duration" option value "5.551115123125783e-17" as duration
[fc#0 @ ...] Error applying option 'duration' to filter 'atrim': Invalid argument
Error : Invalid argument
```

The value comes from the semantically zero adaptive deficit
`0.45 - (0.15 + 0.30)`, represented by binary floating point as
`5.551115123125783e-17`. The old graph rendered it as
`atrim=duration=5.551115123125783e-17`; FFmpeg 9's duration parser does not
accept that notation.

The separate large-graph hypothesis was tested and rejected. The old code
successfully assembled a synthetic graph with 189 distinct MP3 inputs, 188
pause nodes, 377 concat elements, and a 38,896-character `filter_complex`.
Thus the count of inputs, pads, and graph size was not the failure trigger.

The real run proves 189 FFmpeg inputs totaling 5,101,410 bytes. Its exact pause
node count, concat item count, and filter length are not recoverable because
those values were neither logged nor retained after cleanup; no values are
invented here. A second run, `55a27342`, independently failed on the identical
189 inputs and byte count after about 0.05 seconds, consistent with
deterministic filter initialization failure.

## Fix

`AudioAssembler.assemble_chapter()` converts each calculated adaptive deficit
to `round(pause * sample_rate)` and emits `atrim=end_sample=N` only when `N` is
positive. Sub-sample residues become zero; real padding is bounded to the
nearest output sample. Segment order, adaptive target-final-silence semantics,
edge metadata, natural leading/trailing silence, and the no-trimming rule are
unchanged. No fixed 0.3-second policy or chunking architecture was introduced.

`_run_ffmpeg()` still writes full stderr through the existing error logger, but
the raised `RuntimeError` now contains the last 4 KiB and a truncation marker
when the banner/configuration prefix was omitted.

Changed files:

- `src/core/audio_assembler.py`
- `tests/test_audio_assembler.py`

## Regression coverage and verification

The new real-FFmpeg regression creates 189 distinct short WAV segments with
adaptive edge sidecars and targets, including the exact zero-deficit residue.
It validates output existence/format, every segment's sample order, exact total
frame count, and every inserted padding run. This directly detects lost or
duplicated boundary padding. A separate mocked-process test verifies that a
long FFmpeg banner cannot hide the diagnostic tail.

- Focused: `8 passed` in 0.84 s.
- Full suite: `290 passed`, 51 subtests, two non-fatal environment/package
  warnings, in 12.70 s.
- `python -m compileall -f audiobook_gui.py src tests`: passed.
- `git diff --check`: passed.
- Synthetic 189-segment acceptance `ffprobe`: PCM s16le, mono, 22050 Hz,
  duration 3.193741 s, size 140,922 bytes.

## Real chapter acceptance limitation

The 189 source MP3 files and `.pause.json` sidecars were not available. Both
failed pipelines used a run directory under `~/.audiobook-generator` and the
logged `temporary_cleanup` stage deleted it immediately after the exception.
A read-only search of the configured work directory, state/cache directories,
`/tmp`, `/var/tmp`, and user audio locations found no retained chapter-2
segments. Per task scope, no 189-segment TTS rerun or full-book synthesis was
started. The synthetic 189-file real-FFmpeg test is therefore the acceptance
substitute; the original chapter could not be rebuilt from cache.

## Installation and publication

`scripts/install_desktop.py` refreshed the managed desktop entry. Its `Exec`
and `Path` point to `/home/alex/Projects/audiobook-generator`. The real-display
GUI remained alive without output until the intentional five-second timeout
(exit 124); no book generation started.

An ordinary non-force push advanced `origin/main` from `f50930e` to `bd58a2b`.
The feature branch was retained. The documentation handoff is published by a
following ordinary `main` push.

## Remaining limitations

- The original full stderr and exact actual filter metrics cannot be recovered
  after the already-completed cleanup.
- No real chapter-2 source segments survived, so no real chapter assembly was
  possible without repeating TTS.
- No full-book synthesis, ASR, listening, pronunciation work, dependency
  upgrade, or model download was performed.
