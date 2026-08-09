# Run log: FFmpeg large-chapter regression

## Preflight

Read-only preflight found a clean `main` at
`f50930e6b01dcb6423c25c8b44b606704cd97a76`, equal to `origin/main`, and the
requested JSONL at
`~/.local/state/fb2-silero-audiobook/logs/fb2-silero-audiobook-run-2026-08-09_20-17-07_07-Гимн-шута---07_6d7ca90e.jsonl`.
There was no repository-root or `/home/alex/AGENTS.md`; the user-supplied
instructions were authoritative. `codex-reports/LATEST.md`, the linked release
REPORT, and RUNLOG were read before edits.

The branch `fix/large-chapter-ffmpeg-assembly` was created from unchanged main.
No files were deleted.

## Original run evidence

JSONL extraction showed:

```text
chapter 2 synthesis: success, 189/189
chapter assembly start: 189 inputs, 5,101,410 bytes
chapter assembly end: error after 0.051876651 s
reported exception: Ошибка ffmpeg (код 234): <500-character banner prefix>
temporary_cleanup: success after 0.022262573 s
```

The file has 378 records and 279,790 bytes. It contains no FFmpeg command,
filter graph, full stderr, edge silence values, pause count, or concat count.
The adjacent run `55a27342` repeated the same chapter-2 failure with 189 inputs,
5,101,410 bytes, and a 0.054335065-second assembly attempt.

A read-only search found no retained WAV, MP3, or pause sidecar from either
run. Pipeline inspection confirmed creation under
`~/.audiobook-generator/audiobook-run-*` and unconditional temporary cleanup.

## Reproduction and rejected hypothesis

First scale probe, using the unmodified implementation:

```text
189 MP3 inputs
188 pause nodes
377 concat elements
filter_complex: 38,896 characters
result: success
```

This rejected input count, concat pad count, and filter size as sufficient
causes. A second probe used the adaptive values `target=0.45`, previous trailing
edge `0.15`, and current leading edge `0.30`:

```text
required_padding repr: 5.551115123125783e-17
ffmpeg exit: 234
```

Full useful stderr from the reproduction:

```text
[Parsed_atrim_3 @ 0x55f9a361e580] Unable to parse "duration" option value "5.551115123125783e-17" as duration
[fc#0 @ 0x55f9a361cd80] Error applying option 'duration' to filter 'atrim': Invalid argument
Error : Invalid argument
```

The complete reproduction stderr was 2,677 bytes; its preceding content was
the FFmpeg banner/configuration. The old RuntimeError exposed only that prefix.

## Implementation and tests

Applied the following bounded changes:

```text
pause_samples = max(0, round(pause * sample_rate))
atrim=end_sample=<integer>
RuntimeError stderr payload = last 4096 characters
```

Commands and results:

```text
.venv/bin/python -m pytest -q tests/test_audio_assembler.py
8 passed in 0.84s

.venv/bin/python -m pytest -q
290 passed, 51 subtests passed in 12.70s; exit 0

.venv/bin/python -m compileall -f audiobook_gui.py src tests
exit 0

git diff --check
exit 0
```

The synthetic acceptance created 189 distinct constant-value WAV files and
adaptive sidecars. The test checked all samples in sequence and an exact
expected frame total. Standalone `ffprobe` reported:

```json
{"codec_name":"pcm_s16le","sample_rate":"22050","channels":1,
 "duration":"3.193741","size":"140922"}
```

Real chapter-2 assembly was not attempted because its source audio was absent;
repeating Silero synthesis was explicitly out of scope.

## Failed/non-fatal attempts

- The supplied JSONL could not yield full stderr because the old exception had
  already truncated it; no retry could restore discarded bytes.
- A broad file search found no surviving chapter segments after successful
  cleanup.
- The first GUI smoke inside the restricted sandbox exited with Tk
  `couldn't connect to display ":0"`. The authorized real-display retry stayed
  in the Tk event loop until intentional timeout, exit 124, with empty output.
- `gh auth status` reported an invalid CLI token. No token was exposed or
  modified. The requested direct Git operation used the repository's working
  Git credentials successfully; no PR was required.

## Git, installation, publication

```text
git commit -m "fix: make adaptive chapter padding sample-accurate"
bd58a2b77172a986de581ccc5cebfdc38eda33d7

git fetch origin
origin/main remained f50930e6b01dcb6423c25c8b44b606704cd97a76

git switch main
git merge --ff-only fix/large-chapter-ffmpeg-assembly
fast-forward to bd58a2b

.venv/bin/python scripts/install_desktop.py
managed launcher refreshed; clone path confirmed

git push origin main
f50930e..bd58a2b main -> main; exit 0
```

No force push, rebase, reset, branch deletion, full synthesis, ASR, dependency
upgrade, or model download occurred.
