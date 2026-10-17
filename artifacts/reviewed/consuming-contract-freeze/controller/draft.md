# Consuming chart contracts: appearance, session and original controls

## Overview

This amendment defines the next application handoffs using the accepted composition, color, snapshot, reducer and host work. The user approved preparing these contracts after the readiness review. It does not authorize implementation or activate the existing chart entry guards.

The target remains the original table -> chart -> docked editor -> edit/theme -> fresh export -> table -> save/reopen/restart journey. Complete requirements and non-chart components remain owned by the main design. A reduced panel, partial chart options or an alternate persistence owner cannot satisfy this amendment.

Current candidate: Workspace `ea02ec15956dee8d2c8a06825387a570757db12d`. Original reference: `38dffc33389aca0e4a87e0e88d42f7067aa220df`. This package contains source inspection and offline evidence extraction, not new runtime observations. Proposed contracts remain a draft where the named evidence gates are open; no implementation-ready design is claimed.

## Boundary Commitments

### This amendment owns

- The explicit selected-theme/generated/baseline appearance input and extensions to the existing resolved Cartesian style and mapper.
- The React session's typed handoffs, existing-widget transactions, revision/lifetime rules, editor command envelope and host export-freshness seam.
- An evidence ledger linking original control observations and appearance leaves to required projection and interaction checks.
- A concrete dependency order for completing the consuming design without changing the original UX.

### Out of Boundary

No second renderer, generic theme resolver, per-leaf runtime provenance graph, partial-options host path, storage copy, persisted command log, capability flag, substitute editor, provider change or deployment change. Original unknown-unit/mixed-unit behavior, category inference, transformed snapshots and remaining chart families remain mandatory dependencies of their consuming paths, not removed product features.

### Allowed Dependencies

Use accepted `OptionBaseline`, `RuntimeOptions`, snapshot/range types, `ChartDisplayPolicy`, session helpers, original state reducers, the existing widget updater, public Community GridApi, locked ECharts 6.0.0 and the existing ECharts lifecycle/host. Use owned design-system inputs, colors, fonts, switches, tabs and spacing controls. Commercial editor internals are reference evidence only.

### Revalidation Triggers

Recheck this package when selected-theme semantics, generated defaults, saved precedence, field types, financial formatting, control predicates, widget-update behavior, host revision/export behavior or locked dependency versions change. Original-reference findings apply only to their recorded inputs and actions.

## Architecture

Dependency direction is existing data contracts and reducers -> appearance/display projection -> session and existing host -> original entry/editor integration. The reducer remains the sole chart-state reducer; the host remains the sole chart engine owner. Evidence statuses belong in the ledgers, not production rendering values.

The source-generated inputs and selected theme enter `resolveApplicationAppearance`. It calls the accepted composition/color helpers and returns either the extended existing `ResolvedCartesianStyle`, or invalid/unresolved diagnostics. Only a resolved style reaches the existing Cartesian mapper and host. Missing coverage cannot be disguised as an ECharts default or a partial render.

The session derives a display policy from explicit formatting inputs. Extend the existing mapper with a trusted display argument; keep old isolated three-argument callers compatible during migration, but require the application path to supply the policy. Do not add a second application mapper or formatting state owner. Public ECharts member existence establishes an available target, not visual equivalence.

## Components and Interfaces

### Appearance and mapper

The appearance lane's `proposed-types.ts` and `field-manifest.json` are the detailed draft inputs. The entry remains:

```typescript
type AppearanceResult =
  | { readonly status: "resolved"; readonly style: ResolvedCartesianStyle }
  | { readonly status: "invalid" | "unresolved";
      readonly diagnostics: readonly SnapshotDiagnostic[] };
type ResolveApplicationAppearance =
  (input: AppearanceInput) => AppearanceResult;
```

`AppearanceInput` supplies mode, family, selected `OptionBaseline`, original generated data-only options, shared `ThemeSelection`, ordered stable series identities, category column ID and original category-fill state. Mode is dark/light evidence identity, not the selected theme name. `ThemeSelection` carries the actual selected name/base/params/overrides/palette and explicit color tokens. The caller must resolve their source provenance; it cannot pass captured effective output, another mode's loop-produced palette or guessed aliases. Restoring original option generation and token selection is an explicit predecessor of resolver integration.

The style extensions name background visibility, four-sided padding, title/subtitle typography and spacing, separate category/number axes, grid/axis lines, legend geometry, retained disabled marker values, independent series colors/opacity/dash/labels and tooltip mode. Keep one canonical value for each existing field; merge extensions into `cartesianTypes.ts` rather than keeping duplicate old/new style owners. Unknown existing saved properties remain preserved by the storage owner.

The canonical path replaces overlapping legacy fields: per-series nested marker owns marker enabled/shape/size/fill/stroke/width; each typography role owns its font/color/size/weight. Global marker and global/axis typography aliases cannot coexist on this path, even with equal or own-undefined values. The appearance draft's migration table specifies every removed alias. Existing isolated three-argument mapper callers retain an explicit legacy validation/projection branch in the same mapper; the application supplies display policy and canonical style. No second normalizer or runtime flag selects a different product feature set. Migrate constructors, validation and projections together and test duplicate aliases before acceptance.

The manifest records 127 observed pointer groups covering 908 historical observations, plus four supplemental gates: 131 rows total. Every row retains exact reference provenance and distinguishes observed values, source rules, proposed public targets and missing parity evidence. The four saved-composition cases do not establish arbitrary common/family/position inheritance. All applicable fields must have established resolution and projection before a configuration produces resolved options. No fixture-ID or fixed-series-count gate is permitted.

### Session and latest storage

The session lane's draft supplies the full proposed interfaces. Shared names must resolve to one production declaration during the consuming design; no duplicate `ThemeSelection` or style definition is created. Its key input boundaries are:

```typescript
type SessionSelectionResult =
  | { readonly status: "ready"; readonly value: SessionSelection }
  | { readonly status: "waiting" }
  | { readonly status: "invalid" | "unresolved";
      readonly diagnostics: readonly SnapshotDiagnostic[] };
interface SessionRenderInputs {
  readonly mode: "light" | "dark";
  readonly selectedTheme: ThemeSelection;
  readonly generated: RuntimeOptions;
  readonly formatting: FinancialFormattingInput;
  readonly chartBarFillEnabled: boolean;
}
type BuildSessionRender =
  (input: SessionRenderInput) => SessionResult<ChartRenderRequest>;
type UseApplicationChartSession =
  (input: ChartSessionInput) => ChartSession;
```

Selection is unstamped: the hook owns generation/revisions and stamps validated capture. Explicit immutable mode/theme/generated/formatting inputs drive invalidation; callback identity alone does not. `buildRender` is an internal composition seam with explicit inputs and no store/GridApi reads. It consumes snapshot validation, appearance resolution, trusted display and the existing mapper. A ready request retains the supplied stamp and uses its render revision.

Root `chartBarFillEnabled` is also an explicit immutable input and invalidates rendering. Data-only theme projection omits the original item-styler closure, so theme values alone cannot convey this dependency; enabled category-fill effects remain gated. For ordinary captured numeric bindings, construct ordered series identities with `id = sourceKey = SnapshotColumn.id` and the descriptor label, matching public grid capture and `row.values[id]`. Different source-key or transformed bindings require an explicit reviewed immutable map, never a hidden store lookup or label-based guess.

Commands carry the displayed stamp. Validate it before accepting work, then derive the address, baseline, original model and storage again from the functional `updateWidget(previous => next)` transaction. The callback must be replay-safe: no engine calls, downloads, revision publication or success effects inside it. Rendering-derived options never replace selected `baseline.options` in the persistence reducer. Invalid, stale and unresolved commands return the identical previous widget.

The existing `Widget.hooks.tsx:260` mutates its captured functional request into the first resulting object inside React's updater. A replay can therefore reuse stale state, and the surrounding updater schedules persistence/context effects during state calculation. Supplying a pure session callback alone does not establish the contract above. Adapt the existing owner before activating session writes: retain the immutable request for every evaluation, move effects outside replayable calculation and define exactly-once owner completion. This is a prerequisite with its own focused replay/rebase/effect checks, not a claim that the existing API is safe.

The write scheduler remains blocked until that completion port and its admission/rebase types are concrete. Preserve continuous title/slider edits and complete unchanged, rejected, stale and cancelled operations without waiting for a commit that may never occur. A one-pending-command lock would lose original interactions. No optimistic widget copy or persisted command log may stand in for owner acknowledgement.

After a committed change, recapture/rebuild and publish the appropriate revision. A generation change invalidates late work and remounts the existing host keyed by address/generation so reset counters cannot collide with its previous lifetime. Theme/options/formatting change render revision; observations/ranges/filter/sort/bindings change data and render. Panel-only state does not change financial data. Do not introduce an optimistic storage mirror.

The exact supported event union remains title text/enabled, legend position, stroke width and grouped tooltip mode. Root settings/view/range writes remain distinct from option patches. Their existing source ordering is recorded in the session draft. Family change, Set Up/transform commands and complete docked props remain gated by their exact reference contracts. Five supported commands do not define the final panel.

### Host and export

The current lifecycle tracks applied/deferred/stale/disposed work internally; the React host discards those results. Its image export returns a data URL without a revision receipt. Add any freshness mechanism to that same lifecycle/host, preserving existing callers.

The proposed additive receipt reports the actual applied revision after mount/update/resize; a revision-checked export requires current pending and applied revisions to agree in the same host lifetime. Hidden/zero-size, failed, disposed, deferred or superseded work cannot produce a current export. The session validates its command and host stamp before and after export. The external owner retains filename, download and menu behavior.

An applied receipt is not proof that animation pixels have settled. The exact settled-frame acknowledgement and public ECharts event correlation must be established before export tasks are generated. Do not disable original animation or treat a matching revision alone as image parity.

### Original editor

The editor ledger contains 295 rows: 202 runtime capture rows, 88 inventory capture rows and five supported-command rows, with 13 capture-query groups. These are finite evidence rows, not 295 independent control observations or a complete inventory. It distinguishes inventory, source predicates, observed edit payloads, effective changes and the five implemented event paths. Preserve original tabs, order, control geometry, conditional predicates, labels and local interaction state. The draft's column props describe an internal field group, not a complete `DockedChartEditorProps` contract ready to ship.

Do not infer focus, active-tab, scroll or prior selection restoration merely from root `chartSettingsOpen` or a saved outgoing payload. Capture the actual close/reopen/theme/family/table transitions. Preserve the original pre-toggle column-state flush and root view update. Chart entry, context, table/file callers, range callbacks, settings actions and guards must be joined together under one integration owner.

## File Structure Plan and Complexity

Paths below are relative to `terminalpro/src/components/General/Table/Chart/` unless stated otherwise. This is proposed responsibility allocation, not generated implementation tasks.

| Owner | Files | Boundary |
| --- | --- | --- |
| Shared contract controller | new `application/appearanceTypes.ts`; existing `application/types.ts`, `echarts/cartesianTypes.ts` | Source inputs, one resolved style contract, session/editor command interfaces; freeze before parallel implementation. |
| Appearance | new `application/effectiveAppearance.ts`; original `themes.tsx`/`hooks/useChartOptions.tsx` only for explicitly reviewed source-input extraction | Call existing helpers, resolve named leaves, preserve unknown storage, return diagnostics rather than defaults. |
| Mapper join | existing `echarts/cartesian.ts`, `cartesianStyle.ts`; cohesive `cartesianAxes.ts`, `cartesianCaptions.ts`, `cartesianTooltip.ts` where needed | One mapper and explicit public projections; no second implementation. |
| Session/host | new `application/useApplicationChartSession.ts`; existing `sessionState.ts`, `echarts/lifecycle.ts`, `EChartsHost.tsx` | Revisions, existing updater coordination and additive freshness on the current engine owner. |
| Existing widget owner | `terminalpro/src/components/Widget.hooks.tsx` and a cohesive extraction if required | Replay-safe evaluation and once-only completion/persistence/context effects; exact transaction port must be settled before session write tasks. No second store. |
| Original editor | `editor/ChartSettingsPanel.tsx`, `ColumnFields.tsx`, `LineFields.tsx`, `AxisFields.tsx`, `SetupFields.tsx` | Compose owned primitives only after each field/event/predicate contract is complete. |
| Serialized application integration | `AgChartView.tsx`, `hooks/useChartOptions.tsx`; General/Table `hooks/useTableContext.tsx`, `types.d.ts`, `useUpdateColumnState.ts`, `communityActions.ts`, `AgGridTable.tsx`, `AgGridFile.tsx`, `communityBoundary.ts` | Restore original entry/action/range/table lifecycle and remove guards only at the complete join. |

Modified production files are checked whole against 400 physical lines, 300 logical units and 50/function. Current `cartesianStyle.ts` is 278 physical lines, `AgGridTable.tsx` is 333 and `Widget.hooks.tsx` is 307; plan cohesive extraction before adding responsibilities. The widget-owner logical/function counts have not been run. Add inventory ownership before accepting new files. No new exception, lockfile update or runtime dependency is proposed. Contract artifacts and fixtures are nonproduction; this cannot exempt later maintained logic.

## Testing Strategy and Remaining Gates

| Gate | Discriminating check before dependent implementation |
| --- | --- |
| Source resolution | Selected stock/custom theme and nonempty saved family/common collisions; unequal alias tokens; explicit grid/subtitle overrides; original generated and combined inputs alongside effective leaves. |
| Layout | Independently enabled titles/subtitles, asymmetric padding, distinct axis roles and line/grid colors/widths, legend positions and overflow. Capture settled geometry, not only option names. |
| Series and tooltip | Selection/palette boundary and reorder, independent line/marker values, opacity/dash/shapes; hovered stable series IDs, null/missing/ties/order and pointer/keyboard behavior. Preserve numeric observations and units. |
| Complete controls | Flatten missing nested fields, domains, predicates and patch/effect paths; close/reopen/focus/tab/scroll and original entry/exit behavior. No capability predicate or generic arbitrary-path event. |
| Transform and data parity | Separate destination family range/model, category inference, aggregate/transpose, unknown/mixed units and source modes. Never coerce a transform to ordinary or unknown units to guessed currency. |
| Transaction/export | React updater replay, intervening address/data/theme change, old generation callbacks, hidden/deferred host updates, failed update/retry and settled current image. No stale event writes or stale download. |
| Application acceptance | Real original/candidate light/dark journey, actual values, original controls, fresh export, table return, backend save/reopen/restart. A candidate fixture or successful outgoing POST is insufficient. |

Use at most four agents, with two disjoint Sol lanes and an Astra reviewer; serialize heavy captures/builds/suites and shared joins. Browser work uses owned headless contexts and disposable data. Reference evidence must retain source/image/fixture/action identities, failures and cleanup; no owner credentials or live state enter artifacts.

## Requirements Traceability and Phase Decision

The main design retains all 69 criteria. This amendment addresses 1.1/1.4 through pinned source and adaptation boundaries; 4.2/4.7 through original transactions and real persistence checks; 4.8/4.9 through named appearance/control contracts and the complete original journey; 10.1-10.4 through future isolated numerical/browser/concurrency checks; and 10.5/10.6 through actual evidence identities and honest readiness status. No browser or runtime requirement is claimed passed by this contract package.

The immediate output is a concrete draft and evidence/capture manifest. Original resolution/layout/control gaps and settled export acknowledgement remain open. Therefore this package must not be recorded as an implementation-ready consuming design or used to generate activation tasks. Complete the named reference and host contracts, obtain independent design review and human design approval, then generate bounded tasks. Existing accepted tasks, phase approvals and the 1:1 product obligation remain intact.
