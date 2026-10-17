# SQLite repair verification

The isolated backend test runtime, seven-site query repair and bulk-storage regression boundary are independently accepted through task 4.9. The final review returns scoped GO for tasks 4.6-4.9. No application, renderer or deployment acceptance follows from this record.

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

## Accepted bulk storage: task 4.8

Independent Astra review (`artifacts/task-4.8/review/review.md`) reproduced 60 passing tests with zero skips, plus scoped Ruff and formatting checks. Seven additional cases exercise typed bulk insert/update, exact nested widget/layout/chart state and compressed content across SQLite engine recreation, and actual share-helper behavior. Only queue transport is replaced; a separate SQLite connection observes committed bytes during enqueue. Successful enqueue and caught job timeout return normally; other queue errors propagate while the prior commit remains stored, matching existing behavior.

Foreign update and duplicate insertion fail with the existing uniqueness error; foreign deletion raises the existing HTTP 400. Explicit rollback preserves the other owner's data and dates. These tests change no production transaction logic. Initial test failures concerned binary UUID binding and expired ORM access after rollback; corrected test assumptions and final identities are retained in `artifacts/task-4.8/README.md` and execution records. No new production-bug RED claim is made for this test-only task.

## Remaining integration gates

Independent final Astra review reproduced 60 passing tests with zero skips in 46.73 seconds, scoped Ruff checks and formatting of all eight test files. Its combined checker exits 0 with 168 measured files, nine exact exceptions, 38 excluded paths and no errors or violations, including the actual CRUD measurements and both exact exceptions at Workspace `f23cb786a946a6a996deedbe87be9c7ca86b221e`. Evidence: `artifacts/task-4.9/review/review.md`, `full.json` and `maintained-quality.json` in that directory. Explicit acceptance manifests include every maintained fork path, the committed SQLite tests and unrelated working changes; they are declared audit inputs, not a claim that all paths differ from the pinned HEAD. This avoids omitting the repair merely because it was already committed. The earlier working-diff-only report did not measure CRUD and is not the closing evidence.

The sibling `backend-api/backend/tests_sqlite/**` exclusion explicitly covers only its test launcher, fixtures and regressions. Production CRUD remains inventoried and measured. Working inventory additions for unrelated catalog/Perspective work are preserved; selective index construction excludes those additions from this slice's commits. Final review confirms source hashes, scope, sandbox cleanup, actual suite results and exception binding. Passing the combined audit does not accept the behavior of unrelated work included in its measurement scope.

Requirements 2.2, 4.2 and 4.7 still need the real application journey: save through the route, restart the environment, sign in, reopen layout/parameters and refresh data against recorded rebuilt images. Full original renderer parity, Anthropic, Excel and image-pull deployment remain separate open work.
