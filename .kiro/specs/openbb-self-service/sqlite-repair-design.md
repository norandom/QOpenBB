# SQLite dashboard query compatibility

## Overview

Repair the existing application queries so dashboard and app reads work with the bundled SQLite runtime and entity-shared dashboards report their actual creator. No additional adapter, database service or schema migration is required. This bounded supplement supports 2.2, 4.2 and 4.7; the parent design retains all other requirements and full renderer parity remains mandatory.

Owner-approved design and narrow size exception, 2026-10-17. Astra returned APPROVE-for-owner-review in `artifacts/completion-path/sqlite-design-review.md` after settings-isolation clarifications; the owner then approved and requested task generation. Source: Workspace `b96d36d16ba87db2dd595d5796507d473dd0c0c6`. Source inspection and fresh complexity measurements are available; no database test has run for this repair. The inspected pipeline Python environment lacks the backend dependencies.

### Goals

- Execute all six populated dashboard/app read paths using actual mapped models and file-backed SQLite.
- Preserve names, permissions, shared-recipient filtering, existing return schemas and stored dashboard content.
- Prove bulk dashboard insert/update survives session closure and engine recreation, then retain the separate application restart acceptance gate.

### Non-Goals

Frontend activation, PostgreSQL, replacement persistence interfaces, API changes, unrelated CRUD refactoring, queue redesign, new deployment components and full browser persistence acceptance are outside this repair.

## Boundary Commitments

### This slice owns

Six name expressions and one missing creator join in `backend-api/backend/api/crud.py`; regression tests using the existing database models; a tightly scoped complexity exception; source/evidence registration. Existing callable signatures, result labels, CASE conditions and transaction boundaries remain unchanged.

### Out of Boundary

The `get_user_dashboards_entity_shared_noex` query intentionally joins the owner for its permissions-map filter. Preserve this join and attribution. The regular entity-shared query instead needs its selected creator relationship. Do not unify these queries or revise authorization policy. Bulk save commits before share-file enqueue; this repair does not promise atomicity across those operations.

### Allowed Dependencies

Use the existing backend Python 3.13 dependency lock, SQLAlchemy 2, SQLAlchemy-Utils, aiosqlite, Pydantic settings, pytest and pytest-asyncio. Restore the frozen backend environment through the established protected toolchain or reuse an identified backend image; do not resolve a new dependency set for this repair. No runtime package addition and no provider calls. Test transports may replace queue enqueue only; actual CRUD, models, storage decorators and share helper remain exercised.

### Revalidation Triggers

Any changed schema, owner/creator relation, permissions predicate, name fallback, saved content conversion, transaction boundary, storage decorator, backend lock or source revision requires revalidation. An unrelated edit to CRUD invalidates this exception's scope. Renderer and final image changes require the later application persistence join even after these tests pass.

## Architecture

Keep the existing dependency direction: mapped models and schemas feed CRUD; existing routes consume CRUD. Tests enter the same CRUD functions with a real asynchronous SQLAlchemy session. No helper service or second data model sits between them.

Replace `func.concat(User.first_name, " ", User.last_name)` with the typed SQLAlchemy string expression `User.first_name + " " + User.last_name`. SQLAlchemy compiles string addition for the selected dialect, including MySQL's concatenation function. [SQLAlchemy operator reference](https://docs.sqlalchemy.org/en/20/core/operators.html#string-alteration).

Preserve the existing CASE condition requiring both names to be non-null, email fallback, labels and result conversion. Empty strings are not NULL; final display trimming remains in the existing conversion. Add the explicit `User.uuid == DashboardItem.creator_uuid` join only in `get_user_dashboards_entity_shared`. Preserve filters and exclusions.

## File Structure Plan

Paths beginning `backend-api/` are relative to the Workspace fork.

| File | Responsibility |
| --- | --- |
| `backend-api/backend/api/crud.py` | Six expression replacements and one creator join |
| `backend-api/backend/tests_sqlite/conftest.py` | Synthetic settings before imports, disposable file database, real metadata and session fixtures |
| `backend-api/backend/tests_sqlite/fixtures.py` | Real model fixture builders for distinct owners, creators, recipients and entities |
| `backend-api/backend/tests_sqlite/test_dashboard_reads.py` | Four dashboard reads, name semantics, sharing membership and join cardinality |
| `backend-api/backend/tests_sqlite/test_app_reads.py` | Two app reads, names and active recipient membership |
| `backend-api/backend/tests_sqlite/test_dashboard_persistence.py` | Actual bulk insert/update, engine recreation, storage roundtrip and failure isolation |
| `.kiro/complexity-budgets.json` | Controller-owned maintained scope and exact revision-bound physical/logical exceptions |
| `.kiro/breadth.toml` | Actual test paths and honest query-layer evidence status |
| `.kiro/specs/openbb-self-service/sqlite-repair-verification.md` | Before/after evidence, measured exception review and remaining application gate |
| `sources.lock.json` | Accepted fork revision after independent implementation review |

Sibling `tests_sqlite` avoids inheriting the existing `tests/conftest.py` MySQL/testcontainers fixture graph. Tests and documentation are excluded from production caps. No new maintained production module is planned.

## Components and Interfaces

All six async functions retain their current inputs and `UserDashboards` or `UserApps` outputs:

| Function | Relationship and preserved contract |
| --- | --- |
| `get_user_dashboards_owned` | Requested owner set; creator display identity |
| `get_user_dashboards_shared` | Active individual shares; creator display identity |
| `get_user_dashboards_entity_shared_noex` | Existing owner permissions-map membership and display attribution |
| `get_user_dashboards_entity_shared` | Existing entity/exclusion filtering; exactly one joined creator per selected dashboard |
| `get_user_apps_shared` | Existing active share selection and app owner identity |
| `get_user_apps_owned` | Owner selection and existing active view-recipient projection |

`bulk_dashboard_insert_update` remains unchanged and is exercised as the persistence boundary. Tests construct its actual `schemas.DashboardsCreate(items={uuid: content})` input, retain nested widget/layout/chart state and verify the stored result through the repaired read function.

## Complexity Disposition

The measured CRUD baseline is 1599 physical lines, 582 logical units and maximum function size 36. File SHA-256: `51fc65e7cea5938a8654f90671fd8180f81a0fea6fcd955f20d991ad6053c411`. A broad extraction would change substantially more code than this compatibility repair.

Propose two exact-path exceptions for this seven-site patch, physical and logical only, expiring 2026-11-17. Post-patch allowance is at most 1600 physical lines and 582 logical units, subject to actual measurement and independent review. If the patch exceeds these bounds, revise the design rather than inflate the exception. The 50-unit function cap remains enforced. All other modified production files retain 400/300/50 caps.

The controller binds exceptions to the final fork revision and a review recording before/after file hashes, exact diff and measured counts. Rebinding after later fork commits requires verifying the exempt file is unchanged. Do not register prospective values as measured evidence. Combined checker execution must use the actual fork changed-file manifest and preserve unrelated inventory edits. No exception is approved by the existence of this draft.

## Requirements Traceability

| Requirement | Contribution | Remaining acceptance |
| --- | --- | --- |
| 1.1, 1.4 | Recorded source, adaptation and exact reviewed patch | Final source/image release identity |
| 2.2, 4.2, 4.7 | File-backed stored dashboard content survives engine recreation | Real application save, environment restart, sign-in, reopen and refresh |
| 10.3, 10.5, 10.6 | Reproducible tests, breadth links and explicit evidence limits | Integrated Playwright regression against rebuilt images |

This is a bounded supplement, not a replacement for the parent's complete requirement mapping. No provider or renderer acceptance is inferred from query tests.

## Testing Strategy

### Isolation and environment

Run in a fresh backend test process. Before importing settings or API modules, prevent dotenv loading at settings-source construction and supply synthetic required settings, on-prem mode and temporary database/storage paths. Settings explicitly points at a backend env file, so changing the working directory alone is insufficient. Patching only the dotenv source's call method is too late because construction can read the file. Verify the interception with a synthetic sentinel env file and a denied-read assertion before loading real settings. Never read the owner's env. Reject outbound network activity; replace only queue transport where required.

The bootstrap also changes to an empty temporary working directory before the first settings import, retaining the backend's absolute import path. `ProSettings` reads `user_create.json` from the working directory; the test must neither read nor inherit operator account configuration. Start the child with an explicit minimal environment plus synthetic test settings, excluding inherited cloud, TLS and provider configuration. The parent test entry may start in the backend directory, but collection and imports that initialize settings must occur only after this isolation is established.

Use actual mapped tables and dependency-closed metadata, foreign keys enabled, UUID and compressed JSON storage types intact. Do not register a concat UDF, mock database execution, substitute tables or replace storage types. Each test owns its file because bulk save commits internally. Use at most two xdist workers when installed; start focused verification serially.

### Required cases

1. Execute all six populated projections with full, partially null, fully null, empty, whitespace and asymmetric empty/nonempty names. Assert exact output identity and display values after existing conversion. Keep source queries and emitted SQL as evidence.
2. Use distinct owner/creator/recipient/unrelated users and multiple entities/permissions maps. Check exact membership, active versus inactive shares, recipient boundaries, entity exclusions and empty paths. Preserve the noex permissions-map behavior. Assert entity query raw cardinality as well as returned dictionaries so dictionary overwrites cannot hide Cartesian rows; treat Cartesian-product warnings as failures.
3. Insert then update actual dashboard content through bulk save, read it, close sessions, dispose the engine, recreate it at the same filename and compare nested state exactly. Exercise actual compressed storage. Record UUID/date/creator semantics.
4. Exercise on-prem share-file handling through the real helper, replacing only queue enqueue with a deterministic recorder. Check arguments and retain current commit-before-enqueue behavior. Queue failure does not imply rollback of the already committed dashboard.
5. Attempt unauthorized foreign-dashboard modification and duplicate-ID insertion. Assert actual existing error behavior, explicitly roll back failed transactions and prove another owner's content is unchanged. Do not invent a new common HTTP error or transaction contract.
6. Compile captured real selects for SQLite and MySQL to verify dialect output and preserved predicates; execute SQLite. Compilation is not live MySQL acceptance. Capture RED/GREEN evidence against original and repaired source, without altering the tracked source for the reference run.

Proposed focused entry point from `backend-api/backend`: `<backend-python> -m pytest -c pyproject.toml tests_sqlite --confcutdir=tests_sqlite -o addopts='' -o asyncio_mode=auto -q`. Confirm available plugins and exact runtime before execution. Preserve the exercised command, revision, source hashes, exit status and artifacts in the verification record. No passing result is claimed yet.

## Implementation and Integration Gates

After design approval, generate a bounded backend repair/test task and an independent acceptance task. The backend worker owns only CRUD and sibling tests; the controller owns inventory, source pins, breadth and acceptance records. It can run independently of chart research, with the shared heavy-check queue serialized. An Astra reviewer checks sharing semantics, actual test execution and the size exception before acceptance.

Passing this repair permits the persistence layer to join application work; it does not bypass renderer-complete image, Compose, dashboard, Anthropic or Excel dependencies. A later isolated browser test must save via the actual route, restart the environment, sign in and reopen the same dashboard using rebuilt recorded images.
