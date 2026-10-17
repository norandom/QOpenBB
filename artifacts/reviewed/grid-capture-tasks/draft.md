## Approved design slice: ordinary displayed-grid capture

The owner approved [the bounded capture design](chart-grid-capture-design.md) after independent runtime/design review. This amendment proposes tasks 2.38-2.40; implementation approval remains separate. Tasks 2.34-2.37 and the complexity/checker foundations are already accepted. This branch depends on those tasks, not on unfinished earlier numerical renderer entries. A2 completion alone does not unblock mapper/editor/application activation, renderer-complete images or delivery.

The three leaves are sequential because the real-grid setup, adapter and integrated tests share a fixture and configuration. No (P) marker applies. A Sol worker handles each bounded implementation leaf; fresh independent review follows each leaf, with Astra for financial capture and the final join. Controller owns shared test configuration, inventory, source pins, evidence publication and commits. Disjoint appearance/editor research may overlap, with one heavy suite/browser/build at a time; it grants no implementation permission for those lanes.

All paths below are relative to vendor/workspace/terminalpro unless explicitly rooted. Frozen application/types.ts, accepted session/range/snapshot behavior, mapper, host, UI and flags remain read-only. No new package, enterprise module, renderer activation or saved-state owner is introduced.

- [ ] 2.38 Freeze the ordinary-grid fixture and exercise the real Community API
  - Foundation task, 1-3 hours. Own tests/unit/chart-application/gridCapture.fixtures.json and gridCapture.grid.test.ts; controller alone owns the narrowly scoped application tsconfig.json extension for resolveJsonModule. Reuse the existing jsdom/maxWorkers:1 configuration and existing actual Community grid test pattern; do not import root vitest.setup.ts or tests/mocks/ag-grid, which would replace the real API.
  - Translate only the admitted finite synthetic rows, expected financial arrays, selected IDs and range into the self-contained fixture. Record original reference source/image and per-input hashes separately from current candidate identity. Keep normalized-percent and getter experiments explicitly labelled; arbitrary getter configuration, mixed-unit mapping and category inference are not accepted by these fixtures.
  - Use the locked Community modules and typed real GridApi, with only necessary DOM environment shims. AllCommunityModule provides getCellValue and client-row-model/filter/sort/column APIs. Wait for observable model completion, assert actual IDs/order and unformatted values, then destroy the grid and remove the owned host. No GridApi mock or enterprise registration may satisfy this setup gate.
  - Done when executable fixture/setup checks pass for real flat rows, sorting/filtering, stable duplicate-label identities and raw-versus-unformatted getter/formatter values using the current locked environment. Tests must run without the not-yet-created capture adapter; there is no skipped or empty-suite acceptance. Freeze fixture/configuration hashes for 2.39 after independent review and fresh verification.
  - Complexity: tests/fixture and test-only configuration are documented exclusions. Reuse accepted inventory/checker tasks 1.3/1.4; any unexpected maintained production setup change returns to controller review and must meet 400 physical/300 logical/50 per function. No implicit dependency upgrade or broad compiler relaxation.
  - _Boundary: Actual Community grid verification environment and finite reference fixture_
  - _Depends: 1.4, 2.37_
  - _Requirements: 1.1, 4.8, 4.9, 10.4, 10.5, 10.6_

- [ ] 2.39 Capture resolved ordinary observations without changing their meaning
  - Core task, 1-3 hours. Own src/components/General/Table/Chart/application/gridCapture.ts, tests/unit/chart-application/gridCapture.test.ts and the adapter integration additions to gridCapture.grid.test.ts. Consume the accepted fixture/configuration and frozen CaptureDisplayedChart contract; request controller review rather than editing shared types or existing helpers.
  - Consume caller-resolved category/descriptors and ordered range unchanged. Read displayed indices within inclusive valid bounds and use unformatted public grid values. Preserve node IDs, duplicate category labels, numeric zero/negative/fraction/null, supplied units/scale and resolved series order. Never infer category roles, re-filter visibility, parse displayed percentage text, rescale observations or fall back to raw node.data. Test A1 visible-range resolution followed by A2 capture as an explicit seam.
  - Construct the existing flat snapshot from supplied address/data revision, model and original range provenance through the accepted snapshot validator. Preserve input and metadata immutability and return the original captured stamp. Caller pre/post current-stamp validation remains external; do not claim this input can detect a newer generation or caller-owned transpose metadata.
  - Cover destroyed/unready API versus ready-empty rows, malformed input, partial/reversed/out-of-count bounds, missing/duplicate IDs, undefined/nonfinite/unhandled values and bounded API failures. Detectable non-client-side/group/pivot/pinned cases receive diagnostics without importing enterprise modules. Bounds and unsupported-value policies are the approved conservative internal contract, not claims about unobserved original clipping or product behavior.
  - Write meaningful failing regressions before implementation without a feature flag. Done when focused unit and actual-grid integration tests match independent original fixture expectations, waiting/invalid/unresolved behavior and no-write/no-mutation guarantees, with both strict compilers and scoped lint passing. Numeric-only synthetic category, general multiple-category rules, transformed/aggregated/remote paths and UI invocation remain unverified.
  - Complexity: controller registers gridCapture.ts before its acceptance. Its whole maintained file passes 400 physical lines, 300 logical units and 50 per function using the implemented checker and actual current fork manifests. Tests/evidence are explicit exclusions; no new size exception or additional production helper ownership is assumed. Independent Astra review and fresh verification are required.
  - _Boundary: Pure ordinary GridApi-to-snapshot capture adapter_
  - _Depends: 2.38_
  - _Requirements: 1.1, 4.2, 4.7, 4.8, 4.9, 10.4, 10.5, 10.6_

- [ ] 2.40 Independently verify the joined ordinary capture boundary
  - Explicit controller integration task, 1-3 hours. Freeze worker edits and reproduce all chart-application and chart-compatibility units, both strict compilers, scoped lint, exact source/config/test identities and whole maintained complexity using current manifests for both forks. Compare the accepted fixture values to actual GridApi and capture outputs; no browser/build/application activation is part of this gate.
  - Audit the actual diff for unchanged frozen types, accepted range/session/reducer/snapshot/mapper/host behavior, UI and flags. Confirm the adapter owns no persisted storage or lifecycle and the A1/A2 visibility/ordering seam preserves exact financial observations. Keep unrelated dirty catalog/renderer work outside acceptance and selective staging.
  - Done when a fresh independent Astra review accepts tasks 2.38-2.40 only, with real-grid tests discovered and no skips, exact commands/exits/hashes, actual breadth test paths and inventory/source pins aligned. Publish only completed reviewed evidence with source/published hashes before explicit commit/push; do not reuse original-runtime research as candidate application proof.
  - Complexity: entire modified maintained scope passes 400 physical/300 logical/50 per function with unchanged-byte exception validation where applicable; tests/evidence/test-only configuration remain declared exclusions. Retain the actual maintained file count and test count rather than assuming the historical baseline counts are current.
  - No full application, effective appearance, editor, export, save/restart, renderer, image or release acceptance follows this helper gate. Blocked followups below remain binding; no hidden menu, flag or unavailable fallback is authorized.
  - _Boundary: Controller A2 verification, scope inventory and evidence join_
  - _Depends: 2.39_
  - _Requirements: 1.1, 4.2, 4.7, 4.8, 4.9, 10.4, 10.5, 10.6_

### Verification setup and commands for 2.38-2.40

Use a fresh isolated WSL/Linux stage, not a stale task237 archive. Existing pinned Node is 24.22.0, and the accepted dependency tree is /home/mc/qopenbb-work/appearance-deps/terminalpro/node_modules. Read-only prerequisite inspection found AG Grid Community/React 34.1.1, Vitest 4.1.11, jsdom 30.0.1 and application TypeScript 5.9.2; quality tooling separately uses TypeScript 6.0.3. No installation or upgrade is assumed. If the accepted tree is unavailable, restore only through the existing locked protected workflow and record actual identities before acceptance.

The application config already discovers gridCapture.grid.test.ts, uses jsdom and maxWorkers:1, and has no global setupFiles. The controller-owned resolveJsonModule setting is application-only; compatibility compiler settings remain unchanged. Reuse the environment pattern from tests/unit/communityRealGrid.test.tsx, not its broad any types or mocks. Keep any DOM shims local to the owned grid test, clean up global mutations, and never replace the public methods being verified. Unexpected setup scope returns to controller review.

Snapshot exact current fork bytes into the stage, including uncommitted owned inputs, and retain a source/stage hash manifest. Run from its terminalpro directory:

```sh
node node_modules/typescript/bin/tsc --project tests/unit/chart-application/tsconfig.json --noEmit
node node_modules/typescript/bin/tsc --project tests/unit/chart-compatibility/tsconfig.json --noEmit
node node_modules/vitest/vitest.mjs run --config tests/unit/chart-application/vitest.config.mjs
node node_modules/vitest/vitest.mjs run --config tests/unit/chart-compatibility/vitest.config.mjs
node node_modules/@biomejs/biome/bin/biome check src/components/General/Table/Chart/application tests/unit/chart-application
```

For focused setup/adapter verification, append the actual owned test paths to the application Vitest command; inspect discovered tests and skip counts. Before 2.39 there is no import of the absent adapter. The existing 36 application and 260 compatibility tests are a historical baseline, not proof that future tests passed.

The controller creates current workspace/data_api manifests with correct repository/base/head and complete changed-file entries, preserving unrelated dirty inputs measured by the full gate. From the root with pinned Node on PATH:

```sh
pipeline/.venv/bin/python -m tools.quality.complexity --check --changes workspace=artifacts/grid-capture-implementation/workspace-changes.json --changes data_api=artifacts/grid-capture-implementation/data-api-changes.json --output artifacts/grid-capture-implementation/complexity.json
```

These future manifest paths are task outputs, not existing evidence. Update inventory/source pins together and validate existing exception targets are unchanged before rebinding their revision. No new production-only environment or service is required. Core product.md/tech.md/structure.md remain absent as recorded in the parent specification; the specialized steering and approved requirements/design govern this plan.
