# Original chart option state boundary

## Overview

Owner-approved bounded amendment following accepted tasks 2.19-2.23. This slice preserves the original option baseline across initialization and partition changes, and translates the observed column-chart editor controls into original option patches. It prepares original-control integration without changing the Workspace interface or activating incomplete charts.

Baseline: Workspace `06fdb859bf426eb44dce13c54b21c494fcc244fd`. Original reference: `38dffc33389aca0e4a87e0e88d42f7067aa220df`. This supplements the parent design; all other requirement coverage remains there. The owner approved design and autonomous implementation. Tasks 2.24-2.27 passed independent task-graph review before execution.

## Boundary Commitments

### This slice owns

- Pure selection and transition of saved model/options baselines, with explicit prior state and captured partition address.
- Typed patches for title text, title enabled, legend position and stroke width in the observed `bar` namespace for grouped/stacked columns.
- Composition tests with the existing integrated and detached reducers, including preserved inactive-family settings.

### Out of Boundary

Effective theme resolution, generated formatter callbacks, palette/axis/tooltip mapping, line missing-data behavior, family-change range effects, actual grid capture, editor UI construction, application activation and SQLite persistence. These remain mandatory later compatibility work. No existing control, feature flag or caller changes. Family switches are exercised as supplied reducer inputs; this slice does not implement their grid side effects.

### Allowed Dependencies

Existing compatibility types and reducers, pinned `lodash/cloneDeep` and `lodash.merge`, and existing unit verification tooling. No new dependency. No imports from React, GridApi, ECharts, stores or providers. The original hook remains source evidence, not a runtime dependency.

### Revalidation Triggers

Changing selection precedence, empty-partition behavior, patch paths, accepted value domains, reducer contracts, source revision or clone/merge semantics requires the affected contract tests to rerun. Future theme resolution and actual application adoption require separately reviewed contracts and browser evidence.

## Architecture

Saved options and effective render options are different boundaries. The original hook selects stored references first; later it reconstructs common defaults and merges generated options containing functions. This slice handles the former. It must not advertise its returned baseline as an effective style or feed it directly to the current Cartesian mapper.

Flow: validated saved inputs plus optional previous baseline -> baseline transition; typed control event -> original patch; explicit reducer inputs -> existing storage reducer. Tests own composition. No new global state owner or alternative reducer is introduced.

Build versus adopt: reuse the installed clone and merge implementations and the accepted reducers. A small pure transition function is necessary because reference retention on empty partitions is application behavior. A typed patch mapper is necessary because original AG editor event objects will no longer be supplied by that library.

## Components and Interfaces

### Baseline transition

Intent: reproduce original reference values while keeping caller data immutable. Requirements: 4.8, 4.9. State contract; P0 dependencies are existing `JsonObject`, `RuntimeOptions` and `ChartModel` types.

Define `OptionBaseline` with readonly fields `stateAddress: string`, `model: ChartModel`, `options: RuntimeOptions` and `chartType: string`. Nested values use the existing mutable compatibility types so they can be passed to accepted reducers without unsafe casts. Independence is enforced through deep copying, not recursive freezing or a deep-readonly type claim. The captured address records the current input partition even when values were retained from the previous baseline.

`selectOptionBaseline(input: unknown): ValidationResult<OptionBaseline>` accepts a discriminated union:

- `kind: "initialize"`, `stateAddress: string`, optional/null `partitionModel: ChartModel`, optional/null `rootModel: ChartModel`, optional/null `rootOptions: RuntimeOptions`, and `initialChartType: string` already resolved by the original chart-type helper.
- `kind: "synchronize"`, `stateAddress: string`, optional/null `partitionModel: ChartModel`, and `previous: OptionBaseline`.

Models contain JSON outside the known `chartOptions` runtime slot. Options may contain own undefined values under the existing runtime contract. Validate every supplied model and options object, including fallback inputs that are not selected. Reject malformed option slots and malformed model chartType values. A model chartType accepts string or null; a missing key is absent, null is treated as absent, and an own undefined chartType is rejected because it lies outside the accepted runtime-option slot. Optional input model/options properties may be omitted or null; an own undefined optional input property is treated as omitted. The previous baseline must satisfy the same complete model/options validation. Reject accessors, cycles, nonfinite numbers, nonplain objects and throwing inspection. Inputs are inspected without invoking property getters. Return an error result rather than throwing. Validation must not silently coerce a malformed object into an empty baseline.

Initialization rules mirror `useChartOptions.tsx:307-323`: options are `partitionModel.chartOptions ?? rootOptions ?? {}`; model is `partitionModel ?? rootModel ?? {}`; chart type is `initialChartType`, not inferred from model. An empty partition model therefore wins model selection while still permitting the root-options fallback.

Synchronization mirrors lines 326-339: when the partition model has at least one own enumerable key, copy it into the next model and set options to its `chartOptions ?? {}`. Otherwise retain previous model/options values. A nonempty string chartType from the partition updates the previous type; absent, null or empty string retains it. Structural equality optimizations need not preserve object identity: outputs are independent deep copies with equivalent values. There is no root fallback during synchronization.

Model options and selected options are independent copies; mutating a returned nested object must not mutate input or a sibling returned field. Preserve unknown JSON model/options values, array order, null and own undefined. Do not introduce persisted envelope fields; `stateAddress` and transition metadata remain internal.

### Editor patch mapper

Intent: encode observed UI meanings as original stored fields. Requirements: 4.8, 4.9. Event contract; P0 dependency is `RuntimeOptions`.

`mapColumnEditorEvent(input: unknown): ValidationResult<RuntimeOptions>` accepts `{chartType: "groupedColumn" | "stackedColumn", event: ColumnEditorEvent}`. Each union member has exactly named fields `kind` and `value`: for example `{kind: "title-text", value: string}`. The discriminators and value types are:

| Discriminator | Value | Exact patch |
| --- | --- | --- |
| `title-text` | string, including empty | `{bar:{title:{text:value}}}` |
| `title-enabled` | boolean | `{bar:{title:{enabled:value}}}` |
| `legend-position` | `top`, `bottom`, `left` or `right` | `{bar:{legend:{position:value}}}` |
| `stroke-width` | finite nonnegative number | `{bar:{series:{strokeWidth:value}}}` |

Value domains are typed adapter contracts, not claims that every value was exercised in the original UI. Capture proves combined title text/enabled, bottom legend and width four. Remaining valid values require focused source-backed fixtures during implementation; invalid inputs yield errors and no partial patch. The mapper does not infer enabled from text, rewrite colors, select a new family or generate default settings. Line and all other chart families return an explicit unsupported-family error; no production guard is added.

### Composition with existing reducers

Integrated path: caller supplies the selected baseline as `resolvedOptions`, patch as `eventOptions`, original captured state key, current model, resolved chartType, totalSeries and isPivotMode to `reduceIntegratedState`. Existing reducer owns merge, root-theme stripping and storage write ordering. The baseline must already reflect any generated-common replacement in a future application caller; this slice's fixture composition is a stored-state contract only.

Detached path: the reducer replaces event options, so a patch alone is insufficient. The fixture caller constructs a complete event-options object using `merge(cloneDeep(currentCompleteEventOptions), patch)` and passes it to `reduceDetachedState`. `currentCompleteEventOptions` is an explicit supplied runtime object, not inferred from integrated state. This models the event producer's responsibility and does not alter the detached reducer. Future UI integration must supply the same complete-object contract.

Family-switch fixtures supply the existing reducer with already resolved destination model/range and type. They assert retained `bar` fields when selecting stacked/grouped/line, without claiming that bar settings style a line chart or that grid range updates occurred.

## File Structure Plan

All frontend paths are relative to `vendor/workspace/terminalpro/`.

| Path | Responsibility |
| --- | --- |
| `src/components/General/Table/Chart/compatibility/optionStateTypes.ts` | Baseline, transition and typed event contracts |
| `src/components/General/Table/Chart/compatibility/optionState.ts` | Validate and copy baseline initialization/synchronization |
| `src/components/General/Table/Chart/compatibility/editorEvents.ts` | Validate column editor events and produce original patches |
| `tests/unit/chart-compatibility/optionState.test.ts` | Precedence, transitions, validation and immutable copies |
| `tests/unit/chart-compatibility/editorEvents.test.ts` | Patch semantics and reducer composition |
| `tests/unit/chart-compatibility/editorPayload.fixtures.ts` | Minimal synthetic payload projections with source/digest provenance |

The controller owns root complexity inventory, breadth mapping and design/verification records. Existing reducers, legacy types, snapshots, Cartesian mapper, host, application callers and dependency locks remain unchanged. The inspected TypeScript configuration includes `compatibility/**/*.ts` and all local test `.ts` files; Vitest includes `chart-compatibility/**/*.test.{ts,tsx}` with one worker. New files use those existing patterns; no configuration change is required.

Every production module must pass the existing checker at 400 physical lines/file, 300 logical units/file and 50/function. Check whole files and the registered shared-module inventory. Validation and copying stay cohesive in `optionState.ts`; splitting requires a real responsibility boundary, not line-count evasion.

## Requirements Traceability and Testing Strategy

This slice contributes to 4.8-4.9 through saved-state fidelity only. It cannot complete either criterion. Requirements 10.4-10.6 govern bounded verification, actual path/evidence mapping and explicit unverified parity. Requirements 10.1-10.3 continue to govern later browser work; no new browser journey is claimed here. Requirements 4.2 and 4.7 remain separately blocked on real persistence verification. All remaining requirements retain parent design ownership.

- Baseline: every partition/root fallback; empty partition at initialization; nonempty model with missing/null options; populated-to-empty and populated-to-absent transitions; return to populated partition; empty/null/missing type and rejected own undefined type; initial chart type differing from model type; unknown fields and independent nested copies.
- Input safety: accessors not invoked, cycles, nonfinite values, throwing proxy, malformed option slots, nonplain objects, own undefined, nested arrays/null and prototype-sensitive property names. Errors must not mutate prior state.
- Editor: exact leaf paths, separate text/enabled edits, empty title, all accepted legend values, zero/fractional widths, invalid and unsupported events, no shared mutable output.
- Composition: integrated deep merge including null/undefined/array behavior and root-only theme removal; detached full-event replacement retaining unrelated settings; destination supplied model/range retention; bar edits preserved through grouped/stacked/line state changes; state-key collisions retain accepted reducer ordering.
- Import minimal synthetic expected fields from the actual seven-payload capture, with SHA-256 provenance. Do not copy disposable auth/state or treat an expected fixture generated by the implementation as an independent oracle.
- Run the full existing chart unit suite plus new cases, strict TypeScript, scoped lint and the maintained complexity checker. No renderer code changes occur, so this slice does not rerun or claim fresh browser/render acceptance. Prior 124 units/three browser cases remain historical evidence for their original revision.

## Error Handling and Migration

Validation errors contain field-specific descriptions without dumping full state. No store write occurs on invalid input. Retained unknown fields do not imply semantic renderer support. Future unsupported-setting diagnostics must be designed with effective style resolution; this slice only diagnoses malformed boundary input and unsupported event families.

There is no storage migration, service change or release promotion. The helpers remain unconnected until original rendering/editor integration has the necessary coverage. This restriction is an implementation boundary, not permission to ship disabled original features.

## Delivery Sequence

After design approval, generate tasks with explicit owned paths and acceptance criteria. Controller freezes shared types and captured fixtures first. Sol workers can then implement baseline transition and editor mapping concurrently in disjoint files. Astra independently reviews the reference-retention and detached-composition contracts; controller joins unit verification and the final complexity/inventory audit. Design approval does not authorize implementation before task approval.

## Supporting References

[Discovery](chart-option-discovery.md) records the source and actual outgoing-payload evidence. [Snapshot design](chart-snapshot-design.md) and [verification](chart-snapshot-verification.md) retain the previous accepted scope. Complete effective theme/editor behavior, destination grid effects, financial formatting and application-level persistence remain subsequent design boundaries.
