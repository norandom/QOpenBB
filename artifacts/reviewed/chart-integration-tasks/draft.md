# Proposed chart application task amendment

Draft for independent task-graph review. Merge only after PASS and retain a separate owner task-approval gate. Approved design input: `.kiro/specs/openbb-self-service/chart-application-integration-design.md`, SHA-256 `196b88811be7b637d21d4c1e37048d6091609942f4696f9a4bcdc5e90cbb5313`. This amendment adds four executable source-safe leaves; it does not authorize application activation. Existing accepted tasks and unrelated working-tree changes remain outside this amendment.

## Replace the entire Exclusive lanes and joins table

| Wave | Eligible work | Exclusive writable scope | Join and shared ownership |
| --- | --- | --- | --- |
| Foundation | Accepted 1.1-1.8 remain prerequisites | Existing checker, inventory and verification foundations | Reuse accepted checks; no new foundation implementation is implied |
| A: Workspace | Accepted packaging and renderer slices remain historical; 2.34, then 2.35 and 2.36, then 2.37 become eligible only after this task amendment is approved | Chart/application/types.ts and shared test setup belong to controller; A1 owns chartRange.ts/sessionState.ts and their units; B1 owns financialFormatting.ts and its units | 2.35/2.36 may overlap after independent acceptance of 2.34; 2.37 accepts only their joined source-safe boundary |
| A: Data | 3.1-3.7 keep their recorded status and within-lane prerequisites | Owned provider/data API paths and tests | No independent writes to shared locks, catalog bindings or source snapshots |
| A: blocked renderer/catalog join | Replacement renderer/catalog binding, A2/B2, mapper, C/D and real-app joins require their named frozen contracts and a separately reviewed/approved bounded task graph | Ownership in the application integration design; no dispatch from this table | Historical 2.8-2.11 and the superseded 2.9 binding are not executable replacement plans; 2.37 alone does not unblock this row |
| A: image and dashboard joins | 3.8 waits for the reviewed current renderer/catalog source join; 2.12 then waits for 3.8 and complete renderer source acceptance; 4.1-4.5 wait for 2.12/3.8 and their explicit prerequisites | Controller serializes catalog/source/image records and real-app verification | No renderer-complete, dashboard-baseline or release acceptance while original capability gaps remain; an identified unreleased milestone is separate |
| B: Agent | 5.1-5.5 retain their explicit prerequisites and within-lane order | Agent service and agent-specific tests; controller owns builder/origin integration | No Excel implementation before current-identity 5.5 acceptance |
| B: Delivery | 7.1-7.6 in order after 4.5 | Portable delivery commands/wrappers/tests and backup/restore | Shared schemas/build joins remain controller-owned |
| C: Excel | 6.1-6.6 in order after 5.5 | Owned add-in/generator and Excel-specific tests/assets | May overlap eligible delivery; controller owns builder/Compose join |
| Final join | 8.1-8.6 after Excel and Delivery prerequisites | Controller-owned candidate and acceptance records | Complete source/image identities, Office/server/recovery evidence and full capability set remain required |

Chart/application production paths above are relative to `vendor/workspace/terminalpro/src/components/General/Table/`; other lanes retain their concrete ownership paths from the approved design. At most controller plus two bounded Sol implementers and one independent reviewer; difficult state/financial joins receive Astra review. One heavy check at a time. Freeze interfaces before dispatch, stop affected lanes on drift, preserve unrelated dirty inventory/catalog/renderer work, and selectively stage only independently accepted changes. No existing menu, action or feature flag may be removed, hidden, disabled, made inert or given a reduced default.

## Append after the accepted 2.28-2.33 slice

- [ ] 2.34 Freeze source-safe application contracts and executable test scope
  - Controller task, 1-3 hours. Reconcile exact current bytes with the approved design and original source pin `38dffc33389aca0e4a87e0e88d42f7067aa220df`; record actual HEAD plus explicit changed-file manifests and hashes, separating unrelated dirty changes from this slice.
  - Define the design's address/stamp/result, resolved range, column command and display-policy types in `Chart/application/types.ts`, importing accepted legacy/snapshot/option-state types. Keep canonical `CaptureDisplayedChart -> SessionResult<ResolvedSnapshotInput>` only; do not implement capture. Freeze explicit A1 range/session callable inputs/outputs against the source contracts and existing reducer, including ownership of range writes separately from option patches. Freeze B1 callback inputs against the formatting source contract. No guessed category, GridApi invocation, appearance, React session or editor API is admitted.
  - Add compile-time contracts in `tests/unit/chart-application/contracts.types.ts`, a strict `tsconfig.json` and one-worker `vitest.config.mjs` in that directory, reusing the accepted chart compatibility setup. Include both new application tests and existing compatibility tests in the explicit joined commands below. Do not edit the existing shared compatibility configurations during worker fan-out.
  - Controller adds only new owned maintained paths to `.kiro/complexity-budgets.json` and keeps new breadth checks planned/unverified. Reuse accepted 1.3/1.4 checker foundations. Preserve existing concurrent inventory/breadth edits and review their diff separately.
  - Done when independent review verifies source-supported callable contracts and exclusive ownership; strict compile and scoped lint pass, and the explicit current manifest gate measures whole modified maintained files at 400 physical lines/file, 300 logical units/file and 50/function. Record commands, exits, source hashes and config hashes before A1/B1 dispatch; tests/evidence are documented exclusions.
  - _Boundary: Controller shared contract freeze, new application test configuration and scope registration_
  - _Depends: 1.4, 2.33_
  - _Requirements: 1.1, 4.8, 4.9, 10.4, 10.5, 10.6_

- [ ] 2.35 (P) Preserve source range precedence and addressed chart session updates
  - A1 task, 1-3 hours; exclusive writes `Chart/application/chartRange.ts`, `sessionState.ts`, `tests/unit/chart-application/chartRange.test.ts` and `sessionState.test.ts`. Consume 2.34's frozen types/configuration; shared types, existing reducers, contexts, grid callers and mapper are read-only.
  - Resolve eligible stored range, configured columns and generated visible columns in original precedence, honoring ignoreCellRange, the stored more-than-one-column condition, configured empty fallback diagnostics, generated-column intersection and selected-ID order. Preserve ordinary stored row bounds and original JSON without mutation. Do not infer category, raw grid values, aggregation or detached transformations.
  - Validate address/stamps and use accepted option baseline/editor/reducer semantics against the latest supplied storage. Reject stale widget/key/generation/render revision without writes; keep ephemeral counters out of storage. Preserve inactive-family/unknown state, populated-to-empty baseline behavior and root-theme stripping. Keep range transition writes separate from options reduction. Counter overflow invalidates the session; no old token is reused.
  - Done when focused regressions assert exact outputs and input immutability for these transitions, including two widget IDs sharing a stateKey, delayed edits, partition changes, destination-model inputs and separately persisted cellRange. No React activation or chart guard removal occurs; D must later consume these modules before application acceptance.
  - Run focused units, strict compile and scoped lint using the commands below; independent review and fresh verification must pass. Whole owned production files pass 400 physical/300 logical/50 per-function with the actual current manifest; record measured counts and identities. Request controller contract review if work exceeds this boundary.
  - _Boundary: A1 pure source range and session state adapters_
  - _Depends: 2.34_
  - _Requirements: 4.2, 4.7, 4.8, 4.9, 10.5, 10.6_

- [ ] 2.36 (P) Preserve owned financial display callbacks without changing observations
  - B1 task, 1-3 hours; exclusive writes `Chart/application/financialFormatting.ts` and `tests/unit/chart-application/financialFormatting.test.ts`. Consume frozen 2.34 contracts and existing numeric/fiscal helpers. Existing source helpers, mapper, RuntimeOptions, shared configuration and A1 paths remain read-only.
  - Derive typed category, axis, crosshair, legend, series-label and tooltip-number display policies from explicit current period, widget/global precision, column definitions and the source Index formatter contract. Retain zero precision and callback regeneration; never persist functions or replace the data-only RuntimeOptions type.
  - Assert strict +/-1,000,000 boundaries and outside values, magnitude precisions 2/0, series precision 0, current tooltip precision, zero/negative/fractional values and existing nonfinite helper behavior. Preserve date-only/recognized datetime/Date-object, midnight/non-midnight, quarter/year and column-versus-line/legend differences. Expected strings follow the pinned source helpers, not new locale rules.
  - Keep integrated values unchanged; do not apply detached normalizedPercent rescaling or infer currency/prefix/suffix propagation. Test callbacks directly with explicit inputs. AG callback selection, invocation, multiple-tooltip ordering/layout/null behavior and mapper call-site replacement remain blocked joins.
  - Done when source-based expected-string regressions, input immutability, strict compile, scoped lint, independent financial review and fresh verification pass. Whole owned production file passes 400 physical/300 logical/50 per-function with actual manifest evidence; no invocation or application parity claim is made.
  - _Boundary: B1 pure financial display policies_
  - _Depends: 2.34_
  - _Requirements: 4.8, 4.9, 10.5, 10.6_

- [ ] 2.37 Verify and accept the joined source-safe application boundary
  - Explicit controller integration task, 1-3 hours. Freeze A1/B1 worker edits, inspect their combined diff and independently reproduce all new units plus existing chart compatibility units, strict checks, scoped lint and whole-file complexity against exact joined bytes. No browser/build/runtime activation is part of this gate.
  - Audit accepted reducer/mapper/snapshot/host behavior and original feature flags for unintended changes; prove A1/B1 share the frozen contracts without creating a second storage owner. Maintain source hashes and the explicit changed-file manifests, retaining unrelated dirty work outside accepted ownership.
  - Done when independent Astra review accepts only the source-safe contracts/helpers, with actual test IDs, commands/exits, size evidence and reviewed sanitized artifacts; controller updates breadth/inventory/source records selectively. Mark actual helper checks verified while application, capture, effective appearance, editor, export and save/restart remain unverified.
  - Whole modified maintained production scope, including shared types/configuration and controller helpers if any, passes 400 physical/300 logical/50 per-function; tests and evidence are documented exclusions. No release image promotion and no implicit permission for A2/B2/C/D follows acceptance.
  - _Boundary: Controller integration of A1/B1 contracts, identity and evidence_
  - _Depends: 2.35, 2.36_
  - _Requirements: 1.1, 4.8, 4.9, 10.4, 10.5, 10.6_

### Check commands and setup contract for 2.34-2.37

Run in an isolated WSL/Linux source stage with pinned Node 24.22.0 and the accepted locked dependency tree, following the exercised `artifacts/task-2.33/check.sh` staging pattern. Controller snapshots exact dirty source bytes into the stage and hashes them; never archive HEAD alone and silently omit dirty inputs. Serialize any dependency restoration; no new install is assumed. Resolve `$QBB_STAGE` and `$QBB_ROOT` explicitly before execution and record their real paths. The first task creates the new config files; these are planned checks until exercised, not currently passing commands.

From `$QBB_STAGE/terminalpro`:

```sh
node node_modules/typescript/bin/tsc --project tests/unit/chart-application/tsconfig.json --noEmit
node node_modules/typescript/bin/tsc --project tests/unit/chart-compatibility/tsconfig.json --noEmit
node node_modules/vitest/vitest.mjs run --config tests/unit/chart-application/vitest.config.mjs
node node_modules/vitest/vitest.mjs run --config tests/unit/chart-compatibility/vitest.config.mjs
node node_modules/@biomejs/biome/bin/biome check src/components/General/Table/Chart/application tests/unit/chart-application
```

For A1 or B1 focus, append the actual owned test paths to the new Vitest command. Its include pattern must discover the new tests and maxWorkers must be 1; strict config includes new application source/tests and imported accepted contracts. No write/fix lint option. No empty/skipped-suite acceptance. Before joins, inspect test counts and exact discovered test paths rather than treating exit 0 alone as evidence.

From `$QBB_ROOT`, using controller-produced current manifests for both forks:

```sh
pipeline/.venv/bin/python -m tools.quality.complexity --check --changes workspace=artifacts/chart-application-implementation/workspace-changes.json --changes data_api=artifacts/chart-application-implementation/data-api-changes.json --output artifacts/chart-application-implementation/complexity.json
```

The controller creates these manifests before checking: exact inventory-approved repository/base, actual snapshot identity and complete changed-file entries; unchanged data API receives an explicit empty manifest only if the actual scope warrants it. Dirty inventory/catalog/renderer files may be measured by the repository gate but their unrelated work is not accepted by this slice. A cap failure outside the slice is reported to its owner, not repaired or excluded silently. Preserve source/stage hashes, commands, exits and exclusions with evidence. Review and publish only completed sanitized evidence under `artifacts/reviewed/` before selective commit/push.

## Insert explicit blocking annotations in existing tasks 2.12 and 4.1

Insert as the first detail bullet in 2.12:

  - BLOCKED: historical 2.11 completion cannot authorize this build. Require the separately reviewed/approved current renderer/catalog source-join graph, its complete source acceptance and 3.8 identity verification first. Source-safe 2.34-2.37 acceptance does not satisfy renderer-complete eligibility. Any smaller identified unreleased image milestone needs its own reviewed bounded task and cannot complete 2.12.

Replace 2.12's `_Depends: 2.11, 3.8_` with `_Depends: 3.8_`; the unnumbered current renderer/catalog source-acceptance prerequisite above is mandatory until a future reviewed task ID exists. Replace its stale instruction `retain notices and explicit unsupported states` with `retain notices and preserve every original capability; unresolved renderer parity blocks this renderer-complete gate`.

Insert as the first detail bullet in 4.1:

  - BLOCKED until current renderer-complete image acceptance in 2.12 and catalog identity in 3.8, including their separately reviewed replacement source-join prerequisites. Source-safe helper acceptance cannot satisfy either prerequisite or unlock dashboard/delivery acceptance. Keep `_Depends: 2.12, 3.8_` unchanged.

## Replace task 3.8 in place

- [ ] 3.8 Verify the served image and current catalog identity
  - BLOCKED pending a separately reviewed/approved current renderer/catalog source-join task graph and its acceptance; historical 2.9 Perspective bindings are superseded. Acceptance of 2.37 alone does not satisfy this prerequisite. This existing integration gate must be split into bounded leaves in that followup plan if needed; it is not dispatched from this amendment.
  - Compare the identified candidate data/Workspace served schema/catalog with installed generated snapshots and the accepted current renderer binding; ensure generated assets reference the actual preserved OpenBB behavior. Controller alone writes shared snapshots/source locks.
  - Inspect image layers/metadata for provider credentials. If generation changes embedded assets, rebuild the affected candidate through Dagger only and rerun portable reference checks against that exact loaded image; no prior image evidence is reused.
  - Done when independently reviewed loaded-image identities, served metadata and canonical contract hashes agree. This verifies catalog identity, not renderer parity, live-provider acceptance or publication readiness.
  - Complexity: maintained helpers pass 400 physical/300 logical/50 per-function using actual manifests; tests/evidence/generated output are documented exclusions.
  - _Boundary: Controller consumer contracts and data API integration_
  - _Depends: 3.7_
  - _Requirements: 1.1, 4.3, 4.5, 4.8, 4.9, 5.3, 5.9, 9.6, 11.1, 11.3_

## Replace task 4.3 in place

- [ ] 4.3 Verify original dashboard controls and their effects in the real frontend
  - BLOCKED until 4.2 and the separately reviewed current renderer/application join and complete original capability/flag mapping are accepted. Split the actual matrix into bounded verification leaves in the followup task graph before dispatch; source-safe 2.37 is insufficient.
  - Preserve real Playwright account/login/connector registration, absolute same-origin discovery, FMP/FRED add/arrange/resize/remove and observable widget values. Exercise original controls, menus, conditional actions and flag defaults with actual financial results, chart/table transitions, settings and exports under 4.8/4.9.
  - Compare original/candidate integrated light/dark shell, themes, typography, controls, focus and interactions; assert resulting observations and exact state changes. Native Perspective explorer behavior and unavailable legacy controls cannot substitute for the original UX.
  - Done when independently reviewed real-app regressions verify displayed outcomes and failure/recovery with isolated headless one-worker Playwright/CDP diagnostics. Missing controls or capability differences block acceptance and remain visible in the matrix.
  - Complexity: tests/evidence are exclusions; maintained runner/helpers pass whole-file 400 physical/300 logical/50 per-function with actual scope manifests.
  - _Boundary: Verification and Workspace integration_
  - _Depends: 4.2_
  - _Requirements: 4.1, 4.3, 4.5, 4.6, 4.8, 4.9, 10.1, 10.2, 10.3_

## Replace task 4.5 in place

- [ ] 4.5 Accept actual dashboard persistence and the validated API baseline
  - BLOCKED until 4.4, accepted SQLite 4.9, current real-app renderer joins and full original capability checks pass. A separately reviewed followup graph sizes the restart/failure matrix before dispatch; helper acceptance or a smaller unreleased chart milestone cannot certify this baseline.
  - Explicitly save layout/widget parameters and original chart model, selected range, active/inactive-family options, theme and settings-open state through the existing action. Inspect successful response, close/reopen dashboard, restart the disposable environment, sign in again and assert stored state and refreshed observations under the same source/image set.
  - Preserve table column order/widths/selection ownership across chart return, refresh and family changes. Include failed-save recovery without false saved state or lost edits; outgoing POST/engine recreation alone is insufficient.
  - Join current clean-build, catalog, financial, integrated light/dark/control and persistence evidence. Done when independent review accepts the complete current baseline record and breadth distinguishes verified, failing and untested capabilities. Known original chart gaps block renderer/release acceptance; no unavailable-state exception is introduced.
  - Complexity: tests/evidence are excluded; any maintained runner/helper passes 400 physical/300 logical/50 per-function with actual scope manifests.
  - _Boundary: Verification and Workspace integration_
  - _Depends: 4.4, 4.9_
  - _Requirements: 2.2, 4.2, 4.4, 4.7, 4.8, 4.9, 8.1, 10.5, 10.6, 11.1_

## Blocked followups, outside this executable amendment

These are explicit return-to-design/task gates, not numbered implementation tasks or fulfilled design coverage:

| Component/join | Required frozen input before a bounded task can be approved |
| --- | --- |
| A2 gridCapture | Actual ordinary GridApi fixture category/series, range, raw/valueGetter and displayed-row contract; exact typed capture signature already canonical. Numeric-only, multiple-category, hidden/getter/remote cases each retain their own missing evidence. |
| B2 effectiveAppearance | Typed AppearanceInput/Result, finite admitted stock/custom leaves and explicit per-leaf precedence. Six stock defaults/two custom grouped-column observations do not establish arbitrary inheritance. |
| Mapper | Reviewed A2/B1/B2 outputs; actual formatter invocation, category binding, tooltip mode/null/order/layout and explicit effective-leaf projections. Unknown/mixed-unit semantics remain a separate reviewed parity join. |
| C docked editor | Flattened visible/conditional per-field ledger, value domains, exact namespaces/events/effects, props/events and bounded family/group ownership. Four column patches do not complete the editor. |
| D application composition | Exact ChartSessionInput/ChartSession/editor contracts; independently accepted A1/A2/B1/B2 and mapper; measured useUpdateColumnState.ts disposition. Exclusive paths from the design; actual A1/B1 consumption required. |
| Real-app milestone | Reviewed C/D and SQLite; actual financial rows/arrays, original docked journey, theme/export/table restoration and explicit save/reopen/restart, error recovery and cleanup. Unreleased milestone remains distinct from complete renderer parity. |
| Remaining release scope | Other families, detached/AI charts, entity theme preview, aggregated/pivot/transpose/remote and advanced table paths retain capability-matrix obligations and separately scoped joins. No product/menu/flag reduction. |

The completed runtime retry proves one finite initial projection and zero nested edits/saves; exit 1 and cleanup 0 remain recorded. It supplies no missing event, range or formatter seam. The controller must return affected boundaries to design/contract freeze and obtain bounded reviewed tasks before dispatch; no missing signature is invented here. Anthropic 5.5 acceptance still precedes every Excel implementation step.
