# Codex reports

This directory is the durable handoff between repository work and a fresh
ChatGPT/Codex session. After every major task, Codex should:

1. create `YYYY-MM-DD_<short-task-name>.md` with the task goal, verified base
   and final SHAs, implementation decisions, changed files, checks, metrics,
   limitations, unresolved findings, and recommended next task;
2. update `LATEST.md` to point at that report;
3. commit both files and push the exact source branch named in the report.

Reports must be concise and self-contained. Do not include credentials,
personal account data, raw terminal transcripts, giant logs, or binary
artifacts. A reader should verify important claims from Git history and the
named test/analysis artifacts.

`LATEST.md` is the stable entry point for connectors. Open it first, then open
the linked report.
