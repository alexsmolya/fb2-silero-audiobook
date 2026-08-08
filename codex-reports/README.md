# Codex reports

This directory is the durable handoff between repository work and a fresh
ChatGPT/Codex session. After every major task, Codex should:

1. create compact `YYYY-MM-DD_<task>_REPORT.md` with the goal, verified base
   and final SHAs, implementation decisions, changed files, checks, metrics,
   limitations, unresolved findings, and recommended next task;
2. create `logs/YYYY-MM-DD_<task>_RUNLOG.md` with significant commands, exit
   codes, failures/retries, warnings, intermediate checks, measurements, Git
   operations, and short reviewable decision summaries;
3. update `LATEST.md` to point at both files;
4. commit all report files and push the exact source branch named in the report.

Reports must be concise and self-contained. Run logs are diagnostic summaries,
not raw transcripts and never private chain-of-thought. Collapse repetitive
output with an explicit omission note, but retain every failed command and its
remediation. Do not include credentials, personal account data, secrets, giant
logs, or binary artifacts. Important claims should be verifiable from Git
history and the named test/analysis artifacts.

`LATEST.md` is the stable entry point for connectors. Open it first, then read
the compact report; consult the linked run log only when diagnostic detail is
needed.
