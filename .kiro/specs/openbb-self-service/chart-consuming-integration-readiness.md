# Connect the accepted chart contracts to the original experience

The next design must connect effective appearance, the Cartesian mapper and the original editor/session flow. Tasks 2.41-2.45 are accepted, but their helpers have no application consumers at Workspace `ea02ec15956dee8d2c8a06825387a570757db12d`. This discovery record identifies the contracts to finish before implementation tasks can be generated. It does not approve activation or introduce another utility-only implementation wave.

## Target and current gap

The consuming application milestone remains table selection -> chart -> original docked settings -> edits and theme changes -> fresh export -> table return -> explicit save/reopen/restart. Preserve the original controls, conditional visibility, styling, focus behavior and feature flags. A reduced settings panel or a successful standalone chart is not acceptance of that journey.

The current replacement has no `Chart/editor/` implementation, `useApplicationChartSession`, `ChartSessionInput`, `ChartSession`, `AppearanceInput` or `AppearanceResult`. The existing chart entry, option hooks and table callbacks remain guarded or inert. Removing one guard cannot connect the lifecycle safely. These are existing unfinished replacement paths, not new restrictions introduced by this work.

Use the accepted [composition, colors and tooltip state contracts](chart-appearance-source-verification.md), [ordinary capture](chart-grid-capture-verification.md), formatting policy, reducers and ECharts host. Keep each existing owner: the session coordinates revisions and latest storage, the reducer writes original chart state, and the host owns the engine, export and disposal.

## Freeze these contracts next

Paths in the following table are relative to `vendor/workspace/terminalpro/src/components/General/Table/Chart/`. A proposed file is a responsibility boundary, not an instruction to create an empty module.

| Contract | Established evidence or code | Required design output |
| --- | --- | --- |
| Effective appearance inputs | Selected `baseline.options`, generated data-only options, stock/custom selection source, explicit color aliases, ordered stable series IDs | Concrete `AppearanceInput` and result, selected-theme palette ownership and admitted per-leaf precedence in `application/effectiveAppearance.ts`. Never treat the current loop-produced `themePalette` as an active-mode selector. |
| Captions and background | Background fills and separate title/legend/axis typography are observed; current style only represents a subset | Named fields for visibility, title/subtitle typography and spacing, four-sided padding, with exact evidence and public projection tests. Enabled background images need their own effect evidence. |
| Axes and grid | Captured category/number axis leaves and derived grid colors | Separate axis roles, titles, labels, positions, line/grid visibility and styles. Do not infer axis-line color from grid stroke. A cohesive `echarts/cartesianAxes.ts` may own projection once fields are frozen. |
| Legend and series | Finite legend geometry, fills/strokes, line width, marker channels and saved-family conflicts | Explicit legend geometry and per-stable-ID series fields; retain disabled marker shape/size. Opacity/dash, palette exhaustion/reorder and custom line/stacked behavior need their named evidence. Existing modulo allocation is not proof of original allocation. |
| Display and tooltip invocation | `ChartDisplayPolicy`; grouped single/shared/compact content and original saved `bar.tooltip.mode` | Mapper input for trusted display policy, hovered-series identity and content rules. Current axis-trigger/all-series output is insufficient. Freeze null/tie/order behavior and pointer/keyboard invocation before accepting those paths. |
| Original docked editor | Captured tabs/groups and finite event namespaces; owned design-system primitives | Complete visible/conditional field ledger: label, domain, namespace, effect, original predicate, geometry and interaction assertion. Concrete editor props/actions; no five-control substitute for the original panel. |
| React session and persistence | Address/revision helpers, latest-storage reducer orchestration, range helpers and host handle | Concrete session input/output, functional latest-storage transaction, theme/data/render revisions, panel state and export freshness. Composed rendering options must never become persisted original options. |
| Entry and table lifecycle | Original source defines pre-toggle column-state flush, range persistence and restoration | One coordinated join across chart entry, option hooks, table context, range callbacks, settings actions and all chart guards. Restore the original button primitives and original no-series predicate. |
| Aggregate and transpose | Finite Sum and transpose/restoration observations | Separate transformed-snapshot contract retaining observation identity, missing values, units and restoration order. Do not label transformed data as ordinary to pass an existing mapper. |

For each admitted appearance leaf, the manifest must record its input path, reference case/hash, exact precedence, retained disabled value, typed field, public ECharts target and expected option/visible assertion. An observed value does not establish arbitrary theme inheritance. The eight-case ledger's empty-saved-model limitation is superseded only for the four named saved-composition fixtures.

## Execution order and bounded parallel work

1. Freeze the appearance field manifest and the display/tooltip invocation contract. Reuse the existing reference ledger and source findings; run targeted original captures only where a named row lacks evidence. A finite candidate rendering fixture can verify projections during development, but remains preparatory to the application journey.
2. In parallel, freeze the original editor field/event ledger and concrete session/editor interfaces. Resolve transformation and enabled-effect prerequisites for the controls that consume them. Do not infer complete UI coverage from the previously captured nested actions.
3. Synthesize one consuming integration design with exclusive file ownership and dependency joins. Reconcile the parent task graph and remaining renderer/catalog dependencies at that point. Obtain design review and the required human phase approval before generating implementation tasks.
4. Generate bounded tasks only for frozen contracts. Appearance resolution and editor field components may run concurrently after their shared types are frozen. Serialize shared mapper changes, session/context wiring and guard removal. Every task needs independent review and meaningful failure evidence.
5. Run the full original/candidate application journey with isolated browser state, matched light/dark captures, financial-value assertions, export freshness and actual backend save/reopen/restart. Complete remaining family/capability obligations before building and promoting a renderer-complete image.

Use Sol for bounded source/capture work, Astra for appearance/state/financial contract review, and Luna for mechanical mapping. Retain at most four active agents and one heavy suite/build at a time. No new package, service, store, feature flag or generic theme interpreter is proposed.

## File ownership and complexity planning

Fresh physical counts from the two read-only source inspections are below. Logical/function counts were not recomputed; these counts are planning inputs, not checker acceptance.

| Owner | Current files and physical lines | Planning constraint |
| --- | --- | --- |
| Appearance and mapper | `application/types.ts` 181; `echarts/cartesianTypes.ts` 108; `cartesianStyle.ts` 278; `cartesian.ts` 223 | Freeze shared types first. Split cohesive axis/caption/tooltip projection or validation responsibilities before growth reaches the caps. |
| Session and chart entry | `application/sessionState.ts` 195; `AgChartView.tsx` 47; `hooks/useChartOptions.tsx` 143 | Reuse existing reducer/host owners. New React lifetime hook must not duplicate storage or chart ownership. |
| Table integration, paths relative to General/Table | `hooks/useTableContext.tsx` 256; `hooks/types.d.ts` 146; `hooks/useUpdateColumnState.ts` 168; `AgGridTable.tsx` 333; `AgGridFile.tsx` 279; `communityBoundary.ts` 155; `hooks/communityActions.ts` 67 | One integration owner serializes caller/guard edits. Measure whole files, including existing code, before accepting modifications. |

All maintained production changes require inventory registration and the executable 400 physical lines/file, 300 logical units/file and 50/function gate. Do not add a size exception or silently grandfather a large modified file. Tests/reference fixtures remain explicit exclusions. Preserve unrelated catalog and financial-widget work.

## Evidence and status

This is local, read-only discovery on 2026-10-17. Two independent Sol lanes inspected current source and original source at `38dffc33389aca0e4a87e0e88d42f7067aa220df`. No runtime, test suite, browser, image build, dependency installation or provider call ran. No new implementation or visual-parity claim follows from it.

Authoritative inputs are the [application integration design](chart-application-integration-design.md), [appearance/editor amendment](chart-appearance-editor-integration-design.md), [finite appearance ledger](../../../artifacts/reviewed/appearance-next-audit/leaf-ledger.json), [saved composition findings](chart-appearance-saved-composition.md), [tooltip/transpose findings](chart-editor-contract-close.md), and [accepted joined source review](../../../artifacts/reviewed/task-2.45/review/report.md). The synthesis follows Kiro extension discovery and the project's COBESY documentation policy: explicit evidence, concrete next action and scoped claims.

The existing blocked integration rows in `tasks.md` remain in force. This document identifies their prerequisites; it does not mark them ready. The deployment target, Dagger-only builds, image-pull installation, Anthropic-before-Excel dependency, external Jupyter and deferred PostgreSQL are unchanged.
