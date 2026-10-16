# Chart adoption and SQLite findings

The next chart work can proceed through an isolated snapshot and Cartesian mapping boundary. Reconnecting the application requires additional editor and grid contracts. SQLite needs a query repair within the existing backend, not another adapter service.

These are source findings from 2026-10-16, independently investigated by two GPT-6.1 Sol agents. Workspace source is `042ba87e3208a51857da4ae2d1c3109a680716d9`; original behavior reference is `38dffc33389aca0e4a87e0e88d42f7067aa220df`. No runtime acceptance follows from this inspection.

## Preserve displayed observations

Original paths below are relative to `terminalpro/src/components/General/Table/`.

| Source | Observed contract | Consequence |
| --- | --- | --- |
| `Chart/AgChartView.tsx:24` | Range creation forwards type, selected columns, aggregation and combo metadata | These options are not a complete data snapshot |
| `Chart/utils.tsx:603` | Ordinary integrated charts return `rowData:null` | Capture actual displayed grid rows at the future grid adapter |
| `Chart/utils.tsx:413` | Transpose paths merge dates/field identities and preserve financial formatting rules | Do not replace this with generic provider-row normalization |
| `Chart/utils.tsx:628` | Transformed data traverses filtered/sorted nodes and applies date ordering | Raw provider ordering is insufficient |
| `hooks/useTableContext.tsx:273` | Resolves destination-family range, server page bounds and pivot columns | Preserve the resolved range and its provenance |
| `Chart/hooks/useChartOptions.tsx:431` | Generated common defaults replace common options before merge | Stored leaf values alone do not describe effective styling |
| Current `Chart/communityState.ts:3` | State address depends on grouping, period, transpose, sheet, ratio and pivot | Carry the captured address rather than re-resolving it after an asynchronous update |
| Current `Chart/echarts/lifecycle.ts` | Accepts strictly newer finite render revisions | Data revision cannot order theme-only, family or settings updates |

Three-family mapping should operate on immutable, already resolved values. That isolates numerical fidelity from grid capture and original editor parsing. ECharts supplies rendering; the accepted host supplies lifecycle. This avoids a general renderer framework or emulating the whole AG API.

Application adoption remains unverified. Current callers suppress chart view, the current chart view renders an unavailable boundary, and the community boundary rejects integrated charts. These are known outstanding parity defects, not acceptable final behavior. Restoring the toggle alone would expose incomplete controls. All existing enabled paths must have working mappings before final adoption acceptance.

## Observe saved editor fields before mapping them

The initial editor capture exercised title, legend, stroke and stacked-family controls, but captured no reliable outgoing saved widget payload. The capture waited eight seconds. Both inspected revisions of `LayoutAuth/useSyncItems.tsx` dispatch state every 30 seconds and save dashboards every 60 seconds; `api/dashboard.api.ts` sends `{items: dashboardData}` to `/pro/dash/sync`.

A subsequent capture used the verified Control+Shift+S save action and collected seven actual outgoing synthetic-dashboard payloads. Title, legend and stroke edits occupy the `bar` branch and remain stored across grouped, stacked and line selections. See [original option findings](chart-option-discovery.md). Outgoing payloads establish saved field paths, not effective styling or persistence after reopening. The earlier apparent title/legend reset must not be described as deleted stored state.

## Repair SQLite at the query boundary

All six `func.concat` sites are in `backend-api/backend/api/crud.py`. This file is unchanged between the inspected original and current revisions.

| Line | Function |
| --- | --- |
| 533 | `get_user_dashboards_owned` |
| 814 | `get_user_dashboards_shared` |
| 848 | `get_user_dashboards_entity_shared_noex` |
| 907 | `get_user_dashboards_entity_shared` |
| 1529 | `get_user_apps_shared` |
| 1562 | `get_user_apps_owned` |

Proposed change: use SQLAlchemy string addition for `User.first_name + " " + User.last_name`, preserving the enclosing CASE, both-names-non-null condition, email fallback, labels and joins. Empty strings must stay distinct from nulls; do not add normalization or coalesce. Existing result conversion strips strings.

The entity-shared dashboard query at lines 895-911 references User without a join, producing an implicit Cartesian product. Multiple-user tests must determine the correct creator and reject duplicate/leaked results. This is a separately reviewable query correctness defect; a six-expression patch alone does not establish sharing correctness.

The repository checker measures this file at 1599 physical lines and 582 logical units, with no function above 50. A six-line repair therefore still requires a reviewed, revision-bound physical/logical exception or a cohesive refactor. Extracting approximately 300 lines of dashboard/app reads would not bring the remaining file below 400. Do not claim that a small helper makes the whole file compliant.

## Persistence verification contract

Existing backend tests default to MySQL and depend on container/migration fixtures. They are not evidence of SQLite execution. A future repair should use a dedicated file-backed SQLite database with real mapped models and storage types.

- Execute all six actual CRUD functions with populated results, including shared paths; empty early returns must not disguise unexecuted SQL.
- Cover populated, first-null, last-null, both-null, empty and whitespace names; assert IDs, content, ownership and sharing filters. Seed unrelated users and inactive shares.
- Exercise the actual `bulk_dashboard_insert_update` path with `schemas.DashboardsCreate`, then read owned dashboards, update widget/layout state, dispose/recreate the engine and verify the saved content. Preserve on-prem share-file handling and test rollback/isolation.
- Compile for SQLite and supported non-SQLite dialects as supplementary checks.
- Finally exercise actual save, environment restart, sign-in and reopen in the browser. Engine recreation alone cannot close requirements 4.2 or 4.7.

## Synthesis and next boundary

Use one lossless snapshot contract for numerical mapping; keep original state reducers authoritative for original event semantics. Adopt existing ECharts and SQLAlchemy behavior rather than introduce additional services. Separate the chart render contract from SQLite repair because they have different inputs, owners and acceptance tests.

The next bounded chart design can be reviewed independently. Full editor, transformation, table parity and real persistence remain required before product acceptance. Implementation, tests and breadth statuses must continue to distinguish isolated evidence from an operable dashboard.
