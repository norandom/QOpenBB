# Task 2.75 caller integration review

The ordinary Table and File callers are ready for the task 2.76 action join. This approval covers the production caller/session integration and focused component evidence. It does not accept browser, backend persistence, visual or full renderer parity.

## Review Verdict

- VERDICT: APPROVED
- TASK: openbb-self-service 2.75
- MECHANICAL_RESULTS:
  - Tests: PASS. Independent runs establish 108 distinct passing tests: caller/session/range 39, displayed-grid capture 43, Community components 22, and saved-state boundary 4. Commands below exited 0 after the documented correction.
  - TBD/TODO grep: CLEAN across all 21 maintained production paths.
  - Secrets grep: CLEAN for concrete private-key and credential patterns.
  - Static checks: PASS for scoped lint on 26 owned paths and affected diagnostic comparison; SPOT_CHECKED runtime imports and ownership. The strict comparison reports 42 baseline diagnostics and 39 current diagnostics, with none added. Existing broad graph errors remain; this is not a clean application-wide typecheck claim.
  - Boundary: WITHIN the frozen caller manifest and controller-authorized range-selection repair in the existing session owner.
  - Boundary audit: CLEAN. No additional grid capture, chart store, persistence envelope or toolbar was introduced.
  - RED phase: VERIFIED. The range regression expected [500, 1000] but received stale saved-range values [50, 100] before repair.
  - Complexity: PASS. The controller's combined gate exited 0; all 21 production paths were measured, with maxima of 347 physical lines, 110 logical units and 40 units per function. No violations or exceptions apply.
- FINDINGS:
  1. Important, resolved: the session reread a stored range after the caller had applied ignoreCellRange, configured selection and visibility rules. The repaired session reuses the existing range resolver against latest Widget state. A transient frame witness preserves accepted live Set Up changes, including final-series removal, without changing initial saved-range precedence. Tests cover subsequent ignore changes, external ranges, and queued configuration replacement/deletion.
  2. Important, resolved: custom and transposed callers could enter the ordinary capture path. Source-backed orientation classification now keeps those callers explicitly pending while preserving their entry controls and table return. Other chart families remain visible without fallback.
  3. Verification correction: the first independent 82-test run had one test failure because its second edit queried a collapsed Titles section. The test now reopens the real section before issuing that edit; the affected 39-test rerun passes. No failed assertion was removed.
- REMEDIATION: None for this bounded task.
- SUMMARY: The existing Table/File controls reach the real Widget owner, chart session and dock with preserved raw values, saved leaves and range rules; actions and actual application acceptance remain separate gates.

## Source and evidence

Reviewed against Workspace HEAD c3639dc96e0b59212d08e638e7a807b93dd74cc5 plus the uncommitted 21-production/26-owned-path change set. All 26 file hashes were independently checked against current bytes. The source-hashes.json inventory has SHA-256 ef55ee52cada29adab14a83bb58e2f0a14c4ba5009e919a9468e5c48835dc7d3. The original capability source is Workspace 38dffc33389aca0e4a87e0e88d42f7067aa220df. The retained AG Grid 34.1.1 source confirms that AG-GRID-DEFAULT-CATEGORY numbers rows from one within the selected displayed range.

The review read task 2.75, the live integration design/contracts and requirements 4.2, 4.7-4.9 and 10.1, 10.3-10.6. It checked original navbar predicates, hierarchical column roles, hidden mounted grid, table return, unchanged Plotly routing, selected stock/custom theme inputs, mode-specific palette, raw observations with undefined units, and preservation of unknown/inactive saved branches. Generated appearance values remain outside persistence.

Independent commands ran serially in WSL Debian as mc, from vendor/workspace/terminalpro, using Node 24.22.0 at /mnt/d/Source/QOpenBB/artifacts/task-1.2/node-v24.22.0-linux-x64/bin/node:

```sh
node node_modules/vitest/vitest.mjs run --config tests/unit/chart-application/vitest.config.mjs tests/unit/chart-application/callerRoute.test.tsx tests/unit/chart-application/callerInputs.test.ts tests/unit/chart-application/applicationSessionTransactions.test.ts tests/unit/chart-application/applicationSession.test.tsx tests/unit/chart-application/chartRange.test.ts
node node_modules/vitest/vitest.mjs run --config tests/unit/chart-application/vitest.config.mjs tests/unit/chart-application/gridCapture.test.ts
node node_modules/vitest/vitest.mjs run --config tests/unit/communityBoundary.config.mjs
node --experimental-strip-types --test tests/unit/communityBoundary.test.mjs
```

The capture suite ran in the initial combined six-file invocation and passed 43 tests; its unchanged source was hash-verified after the affected rerun. Scoped lint used Biome with the 26 owned paths. The diagnostic comparison used the existing session.tsconfig.json, all 21 production files, and an overlay of existing files from c3639dc. git diff --check and the final hash/count comparison were clean. Raw logs, RED output and intermediate inventories remain local.

The controller ran this combined gate from the repository root in the same WSL environment, exiting 0. The reviewer verified that its 21 measured paths and physical counts match the final hash inventory:

```sh
PATH="$PWD/artifacts/task-1.2/node-v24.22.0-linux-x64/bin:$PATH" /home/mc/qopenbb-work/sqlite-runtime/venv/bin/python -m tools.quality.complexity --check --changes workspace=artifacts/live-editor/callers/workspace-changes.json --changes data_api=artifacts/live-editor/checks/data_api-changes.json --output artifacts/live-editor/callers/complexity-final.json
```

## Acceptance limits

The caller tests execute actual AgGridTable/AgGridFile, the production session, dock and useWidgetUpdates transaction owner, while stubbing transport, grid public methods and the canvas host. They prove caller wiring, mapped values and saved fields, not actual browser drawing or backend restart. Task 2.76 still owns quick actions, dock menu activation, navigator/mini-chart and current-image export. Task 2.77 owns the Full application route, save/reopen/restart, failure recovery, console/network diagnostics and matched light/dark visual review. Advanced callers and other families remain unreleased parity obligations. The original structural-axis and numeric-rotation/Auto Rotate reopen limitations remain disclosed and unchanged.
