# SQLite repair verification

The isolated backend test runtime and seven-site query repair are accepted. Bulk-save verification and the joined SQLite gate are in progress. No application, renderer or deployment acceptance follows from this record.

## Scope and identity

The owner approved the [design and narrow size exception](sqlite-repair-design.md), then tasks 4.6-4.9. The repair owns six name projections and one creator join in the existing backend. It adds no database service, schema migration or feature flag. The original CRUD source hash is `51fc65e7cea5938a8654f90671fd8180f81a0fea6fcd955f20d991ad6053c411` at Workspace `b96d36d16ba87db2dd595d5796507d473dd0c0c6`.

## Accepted test runtime: task 4.6

Workspace `693954f43aac8af888cfe6e7bfed6d9dcb72d2f5` adds the sibling SQLite launcher, bootstrap, real-model builders and two infrastructure tests. The unchanged backend lock was exported with its development group and installed through Safe Chain uv into Python 3.13.15. Source, lock and installed dependency identities are recorded in `artifacts/task-4.6/evidence.json`.

Independent Astra re-review reproduced two passing tests with zero skips, Ruff and formatting checks, and cleanup after both success and expected nonzero exit. Evidence: `artifacts/task-4.6/review/review-round2.md`. The first review found that pytest retained its database outside the launcher directory. The repair places pytest's temporary root inside the disposable sandbox; a regression asserts database containment. The three confirmed leftover databases were removed without deleting shared pytest parents. The original rejection remains recorded.

The bootstrap intercepts dotenv source construction before application imports, proves denied sentinel/account reads, uses an empty temporary working directory and explicit synthetic environment, and denies network access. Actual model tables retain foreign keys, UUID types and compressed JSON. Tests verify compressed bytes, stored identities, foreign-key rejection and a fresh engine reading the same file. They do not call bulk dashboard save or accept the six read paths.

Exercised launcher, from the backend directory with the restored interpreter:

```sh
/home/mc/qopenbb-work/sqlite-runtime/venv/bin/python tests_sqlite/run.py
```

The path identifies this WSL development environment; a fresh host must restore the pinned runtime first. The launcher prints its exact child command and owns temporary state. It is a test command, not an installation procedure.

## Accepted read repair and measured exception: task 4.7

Independent Astra review (`artifacts/task-4.7/review/verdict.md`) reproduced 53 passing tests with zero skips and verified the exact seven-site diff. Matching baseline tests produced 10 failures and 43 passes: one entity-shared dashboard produced four raw rows with unrelated users present. Current SQLite 3.53.1 already supports the old concat function, so the six string changes are portability corrections, not six reproduced execution failures. The joined creator repair fixes the observed pre-existing upstream defect. No database is being ported.

Eight name combinations across all six read paths, distinct owner/creator identities, sharing membership and captured SQLite/MySQL select compilation are exercised. Existing noex owner attribution and permission-map semantics remain unchanged. Baseline and repaired runs have matching tests, fixtures, dependency locks and runtime manifests. MySQL compilation is not live MySQL acceptance.

The independently measured whole-file exception is approved at 1599 physical lines and 582 logical units, with maximum callable size 36 and expiry 2026-11-17. Repaired CRUD SHA-256 is `575b2cdeb0f04aab81af60b34074e4b9c2c6e21cfb6559c695e502361defc6e9`; the original hash is recorded above. Controller registration binds these exact measured baselines to the accepted fork revision. The function cap remains 50 and unrelated CRUD edits require renewed review. Test lint/format and CRUD lint pass. Whole-file CRUD formatting fails on both original and repaired source; unrelated formatting was deliberately left unchanged.

## Remaining integration gates

Task 4.8 must exercise real bulk save/update, compressed storage, engine recreation and failure isolation. Task 4.9 must independently accept the joined suite, verify exact revision-bound exceptions and run the combined maintained-code checker.

Even after those gates pass, requirements 2.2, 4.2 and 4.7 still need the real application journey: save through the route, restart the environment, sign in, reopen layout/parameters and refresh data against recorded rebuilt images. Full original renderer parity, Anthropic, Excel and image-pull deployment remain separate open work.
