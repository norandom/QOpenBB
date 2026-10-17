# Task 4.8 storage-layer regressions

The new tests exercise actual bulk dashboard CRUD and compressed SQLite storage. They establish engine-reopen persistence; application restart, browser save/reopen, refresh and renderer acceptance remain unverified. No production source, fixtures, dependencies or transaction behavior changed.

## Reproduce

Run as WSL Debian user `mc` with the frozen task 4.6 runtime:

```sh
/home/mc/qopenbb-work/sqlite-runtime/venv/bin/python /mnt/d/Source/QOpenBB/artifacts/task-4.8/verify.py focused
/home/mc/qopenbb-work/sqlite-runtime/venv/bin/python /mnt/d/Source/QOpenBB/artifacts/task-4.8/verify.py full
```

The script calls the existing isolated launcher serially, followed by Ruff lint and format checks for the new test file. Each JSON record includes exact commands, exits, source hashes, Workspace revision, Python/SQLite versions and installed distributions. The launcher prints its child command and removed sandbox path. Tests use real dependency-closed tables, enabled foreign keys and the original UUID/compressed-content decorators. No account configuration, keys or network access are needed.

Final evidence on 2026-10-17: the focused run passes seven tests with 53 deselected and zero skips; the full run passes all 60 tests with zero skips. Both runs and all four lint/format checks exit 0. `focused.json` and `full.json` bind these results to Workspace `4579cea149db29a592b28e4a2312c4348f4038dc` plus the new uncommitted test's SHA256. No source edits occurred between these two passing runs.

## Observable contracts

- `test_bulk_insert_update_engine_reopen` inserts and updates typed `DashboardsCreate` input with nested layout, widget parameters and chart state. It checks real gzip bytes, UUID/owner/creator/entity identity and dates; closes the session, disposes its engine, opens a new engine on the same file and checks both stored rows and the repaired owned-dashboard read.
- `test_real_share_helper_commit_before_enqueue` executes the original helper in on-prem mode. Only `rq_que.enqueue` is replaced. The recorder checks string UUIDs, actual worker target and timeout. An independent synchronous SQLite connection sees the updated bytes inside enqueue, proving commit preceded transport. Success and swallowed `JobTimeoutException` return normally; `RuntimeError` propagates. A fresh session proves the updated content remains committed in every case.
- `test_failed_bulk_save_preserves_other_owner` checks foreign update, foreign delete and an explicit duplicate ID insertion by a distinct same-entity owner. Existing foreign update/duplicate behavior is a database uniqueness failure, while foreign delete is HTTP 400. Explicit rollback follows failures; another owner's payload and dates remain exact. An existing ID submitted by its actual owner is an update by design, so the duplicate insertion uses a different owner.

This maps task 4.8 to requirements 2.2, 4.2, 4.7, 10.3, 10.5 and 10.6 within `sqlite-repair-design.md` Testing Strategy cases 3-5. The 4.7 reads run unchanged in the full suite. Tests are exempt from production size caps. Controller owns breadth registration, independent review and acceptance.

## Development evidence

This task adds regressions for accepted behavior and makes no production change. No pre-repair RED claim is made. `initial-0.log` records seven test failures because raw SQL bound hexadecimal strings instead of the actual binary UUID representation. `second-0.log` records six passes and one test failure from reading an expired fixture object's UUID after rollback. Binding UUID bytes and capturing identifiers before rollback corrected those test assumptions. The corresponding JSON files retain source identities and commands; their lint/format entries refer to the same zero-exit checks subsequently repeated in final evidence. Focused and full logs record the corrected suite.

Disproof conditions include changed nested state after reopening, unreadable gzip bytes, altered identity/dates, queue invocation before committed visibility, swallowed non-timeout failures, or foreign-owner state modification. Passing these tests establishes none of the outstanding application or browser acceptance gates.
