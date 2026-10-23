# Waterfall renderer and editor join

Freeze two new-file lanes, then perform the shared application join in the controller. Prefer an explicit `waterfall` member of `ApplicationChartFamily` over widening `CartesianFamily`: this costs explicit application routing but prevents the generic Cartesian translator from silently drawing ordinary bars. Both choices reuse the existing session owner; a family-specific projection is not a second session framework.

Read-only inspection on 2026-10-23 at Workspace HEAD `e2b87ed98cd5ef18fb9ca6ddf888802d71fc685e`, with W1 work in progress. The bounded W2 design is independently approved for lane dispatch; implementation acceptance remains open. No production edits, tests, builds, browser actions or provider requests ran. Core `product.md`, `tech.md`, `structure.md` steering files were absent; complexity, delegation, testing and documentation steering were read. Specification language is English.

Paths below are relative to `vendor/workspace/terminalpro/src/components/General/Table/Chart/`; test paths are relative to `vendor/workspace/terminalpro/`.

## Why these seams match current code

- `projectOrdinarySetup` already owns aggregation, displayed order, source IDs, value origins and witnesses. `applicationSessionSelection.ts` currently passes all selected fields to its single-axis admission. `applicationSessionSetup.ts` independently repeats that admission after a Set Up edit. Both calls need the same transient first-field selection; changing only the render selection leaves mixed-unit Set Up broken.
- `ApplicationSessionInputs/Context` already accept an `ApplicationChartFamily` generic. Range demonstrates a family projection/selection on the same capture, stamp, dispatch, persistence and host owners. Reuse that seam without copying lifecycle logic.
- `appearanceDefaults` already accepts `family: string`. `resolveCommonAppearance` has an explicit family union which can safely gain `waterfall` without activating callers. `appearanceLayers` currently maps every non-line/area family to `bar`; do not send Waterfall through that function unchanged.
- `ChartRenderRequest` already has `projectNavigationWindow(projected,current)` and `projectPointer(applied)`. `lifecycle.ts` invokes these generically. It must remain byte-for-byte unchanged.
- `cartesianNavigator` adds no zoom at all when both toggles are false, and its slider targets horizontal axes. Calling it alone does not satisfy hidden-navigator zoom or horizontal Waterfall. `rangeNavigator` demonstrates hidden carriers and generic host callbacks, but takes Range-specific composed geometry; it cannot simply accept a Waterfall object.
- `navigatorOverview` clones custom-series `renderItem` closures. Main-pixel coordinates captured in such a closure will draw the miniature incorrectly. Geometry must use `api.coord`, `api.size` and the current custom-series coordinate system.
- `ChartLabelsPanel` is directly reusable for item label fonts. `ChartSeriesStylePanel` is reusable for each sign's border/fill-opacity controls. The ordinary top-level series panel must be replaced for Waterfall, not shown alongside the sign controls.

## Controller-owned frozen type file

Create `application/waterfallTypes.ts` before dispatching both workers. These are proposed exact public exports; internal helper names are worker-owned. All fields are readonly. Import existing `ResolvedApplicationAppearance`, `ApplicationAxisRuntime`, `ApplicationThemeInput`, `AppearanceInput`, `ResolvedFontStyle`, `ChartLabelsState/Edit`, `ChartSeriesStylePanelProps`, `ChartLabelsPanelProps`, `ChartSnapshot`, `SnapshotDiagnostic`, `ChartDisplayPolicy`, `CartesianMappingContext`, `ChartRenderRequest`, and `ValidationResult` rather than recreating their contracts.

```ts
export type WaterfallSign = "positive" | "negative";
export type WaterfallDirection = "vertical" | "horizontal";
export interface WaterfallThemePaint {
  readonly positive: { readonly fill: string; readonly stroke: string };
  readonly negative: { readonly fill: string; readonly stroke: string };
  readonly total: { readonly fill: string; readonly stroke: string };
  readonly connectorStroke: string;
}
export interface WaterfallLabelStyle extends Readonly<ChartLabelsState>, ResolvedFontStyle {
  readonly placement: string;
  readonly spacing: number;
}
export interface WaterfallItemStyle {
  readonly name: string;
  readonly fill: string;
  readonly stroke: string;
  readonly strokeWidth: number;
  readonly strokeOpacity: number;
  readonly fillOpacity: number;
  readonly lineDash: readonly number[];
  readonly lineDashOffset: number;
  readonly label: WaterfallLabelStyle;
}
export interface WaterfallSeriesStyle {
  readonly direction: WaterfallDirection;
  readonly visible: boolean;
  readonly tooltipEnabled: boolean;
  readonly item: Readonly<Record<WaterfallSign | "total", WaterfallItemStyle>>;
  readonly line: {
    readonly enabled: boolean;
    readonly stroke: string;
    readonly strokeWidth: number;
    readonly strokeOpacity: number;
    readonly lineDash: readonly number[];
    readonly lineDashOffset: number;
  };
}
export interface WaterfallResolvedAppearance {
  readonly application: ResolvedApplicationAppearance;
  readonly axisRuntime: ApplicationAxisRuntime;
  readonly series: WaterfallSeriesStyle;
}
export type WaterfallAppearanceInput = Omit<AppearanceInput, "family"> & {
  readonly paint: WaterfallThemePaint;
  readonly legendEnabled?: boolean;
};
export type WaterfallAppearanceResult =
  | { readonly status: "resolved"; readonly value: WaterfallResolvedAppearance }
  | { readonly status: "invalid" | "unsupported"; readonly diagnostics: readonly SnapshotDiagnostic[] };

export type WaterfallEdit =
  | { readonly kind: "direction"; readonly value: WaterfallDirection }
  | { readonly kind: "connector"; readonly field: "stroke"; readonly value: string }
  | { readonly kind: "connector"; readonly field: "strokeWidth" | "strokeOpacity" | "lineDash"; readonly value: number }
  | { readonly kind: "item"; readonly sign: WaterfallSign; readonly field: "strokeWidth" | "strokeOpacity" | "fillOpacity" | "lineDash"; readonly value: number }
  | { readonly kind: "label"; readonly sign: WaterfallSign; readonly edit: ChartLabelsEdit };
export type WaterfallEditIntent = { readonly panel: "waterfall"; readonly edit: WaterfallEdit };
export interface WaterfallControlValues {
  readonly direction: WaterfallDirection;
  readonly connector: WaterfallSeriesStyle["line"];
  readonly items: Readonly<Record<WaterfallSign, {
    readonly series: Omit<ChartSeriesStylePanelProps, "onEdit">;
    readonly labels: Omit<ChartLabelsPanelProps, "onEdit">;
  }>>;
}
export interface WaterfallControlsProps {
  readonly value: WaterfallControlValues;
  readonly onEdit: (edit: WaterfallEdit) => void;
}

export interface WaterfallRenderInput {
  readonly snapshot: ChartSnapshot;
  readonly fieldId: string;
  readonly appearance: WaterfallResolvedAppearance;
  readonly context: CartesianMappingContext & {
    readonly viewport: { readonly width: number; readonly height: number };
  };
  readonly theme: ApplicationThemeInput;
  readonly navigatorEnabled: boolean;
  readonly miniChartEnabled: boolean;
  readonly navigation: WaterfallNavigationPolicy;
}
export type WaterfallRenderResult =
  | ({ readonly status: "supported" } & Pick<ChartRenderRequest,
      "options" | "projectNavigationWindow" | "projectPointer">)
  | { readonly status: "invalid" | "unsupported"; readonly diagnostics: readonly SnapshotDiagnostic[] };
```

`navigation` is resolved runtime policy from existing options, never a new stored flag or UI control. `WaterfallNavigationPolicy` contains pagination, showInMiniChart, outsideMinor, hoverRange/clickRange (exact, nearest or numeric), zoom (enabled, scaleX, scaleY, scrolling, panning), and autoScale (enabled, padding, minVisibleItems). The scale flags retain the existing Range policy convention after direction mapping. Preserve the normal default zoom-enabled route, horizontal direction, and hidden/visible navigator states. `context.legendSelection` is ignored for Waterfall because its sign legend is fixed. The type-only module is the authoritative compile-checked interface; names in this document must agree with it.

## Lane A: renderer, after W1 acceptance

Exclusive new production files: `echarts/waterfall.ts`, `echarts/waterfallSeries.ts`, `echarts/waterfallInteraction.ts`, `echarts/waterfallNavigator.ts`, and `echarts/waterfallCategory.ts` for continuous coordinate/domain planning. These responsibilities are translation/admission, engine-coordinate painting, source-identity pointer/window projection, and navigator composition. Do not add a file unless its responsibility warrants it; unused reserved paths need not be created.

Exclusive tests: `tests/unit/chart-compatibility/waterfall.render.test.ts`, `waterfall.navigation.test.ts`, `waterfall.pointer.test.ts`.

Public export:

```ts
export function projectWaterfall(input: WaterfallRenderInput): WaterfallRenderResult;
```

The parent supplies the first-field ordinary projection and its witness. Renderer validates that `fieldId` is the sole effective numeric field, calls frozen W1 `projectWaterfallTotals(snapshot.rows.map(row => row.values[fieldId]))` once on the full ordered data, and associates W1 indices with immutable `snapshot.rows[index].id` and category. Undefined observations must fail; missing values are explicit null. It does not choose fields, aggregate, rewrite capture, or synthesize totals.

Full cumulative points remain the authority for navigation. Window changes crop those points and recompute visible endpoint extent/pointer positions; never sum only the visible rows. The overview retains full points and engine coordinates. Zero points have no visible rectangle at the observed default width zero. Missing points have no bar and break connectors on both adjacent edges. A normal label `Total` stays a movement. Tooltip values are raw signed deltas with the supplied display callbacks and source identities; duplicate labels are not keys. Do not claim zero/missing hover parity beyond the observed evidence.

Legend entries represent positive/negative sign classes, not selected metric IDs. Match the observed negative-only empty legend defect; mixed data has Positive/Negative with configured names and theme paints. `selectedMode: false`; no `projectLegendSelection`. Presence must follow the retained predicate, including a focused zero-only case against source/reference, rather than assuming negative bars always imply a Negative legend entry. Legend visibility remains the existing editor setting.

Use existing layout/axes/grid/navigator helpers where their contracts fit. The controller can widen only shared layout/axis parameter unions to `waterfall`; orientation must follow resolved axis positions, not the string family predicate. Reserve measured main-axis label space before miniature placement. Reuse the rectangular spatial index/picker if suitable, and return the generic pointer plan; do not edit pointer lifecycle or native event bindings.

## Lane B: appearance and disconnected controls, independent of renderer

Exclusive new production files: `application/waterfallAppearance.ts`, `application/waterfallAppearanceOptions.ts`, `application/waterfallEditorControls.ts`, `editor/waterfall/WaterfallControls.tsx`. The first two own complete Waterfall layer resolution/validation and nested styles; the third owns control values and pure option-patch mapping; the TSX composes existing primitives. No shared editor/session file edits in this lane.

Exclusive tests: `tests/unit/chart-compatibility/waterfallAppearance.test.ts`, `waterfallEditorControls.test.tsx`.

Public exports:

```ts
export function resolveWaterfallAppearance(input: WaterfallAppearanceInput): WaterfallAppearanceResult;
export function waterfallControlValues(value: WaterfallResolvedAppearance): WaterfallControlValues;
export function mapWaterfallEdit(edit: WaterfallEdit, current: WaterfallResolvedAppearance): ValidationResult<RuntimeOptions>;
export function WaterfallControls(props: WaterfallControlsProps): React.ReactElement;
```

Yes, this lane can be completed independently: it consumes only the frozen style/control types and existing appearance/editor primitives. It does not depend on W1 output or renderer geometry. Parent first adds `waterfall` to the `resolveCommonAppearance` argument union, which is a type-only preparation, not caller activation.

Compose baseline/generated options with `composeAppearanceOptions`. Apply common and Waterfall theme/generated/saved layers with existing precedence; `bar` keys must never affect Waterfall. Start common chrome/axis defaults with `appearanceDefaults`, then Waterfall source defaults. Resolve direction to concrete axes while retaining applicable axis options. The result contains effective data only; patches contain only edited leaves and go through the existing reducer. Do not persist resolved defaults or overwrite unknown options.

Reachable controls: direction in existing Set Up direction group; tooltip through the existing panel mapped to chart-level `waterfall.tooltip`; connector stroke/width/opacity/dash; positive/negative item border width/dash/stroke opacity/fill opacity and label enabled/font/weight+style/size/color. `WaterfallControls` owns a local positive/negative selector only. No connector enabled checkbox, item fill/stroke color control, placement control, total selector, category/series inversion or axis ticks. Preserve stored unsupported/unknown keys including totals bags without inventing their effects or claiming parity. Original G14344 offers single/shared/compact modes; retain them. G10320/G13950 pass the outer chart-options proxy, so both tooltip enable and mode write waterfall.tooltip, independently of saved series.tooltip settings.

Keep `item.total`, sign names/fills/strokes, label placement/spacing and `line.enabled` in effective resolution where supported, even without controls. Font weight edits must preserve the paired fontStyle semantics via existing mapping helpers. Connector and item opacity/width/dash are separate paths. Explicit stroke behavior should use retained source defaults, not generic bar fallback.

## Parent-owned join and exact shared paths

The controller owns `application/waterfallTypes.ts`, new `application/waterfallSessionSelection.ts`, `application/waterfallSessionProjection.ts`, `application/waterfallEditorTransaction.ts`, and all modifications listed below. Workers do not edit these paths.

| Exact existing path | Required join |
| --- | --- |
| `application/comboSessionTypes.ts` | Add `"waterfall"` only to `ApplicationChartFamily`. Leave `CartesianFamily` and `isCartesianFamily` unchanged. |
| `application/applicationChartSessionTypes.ts` | Add Waterfall ready/control projection and specialized intent union. |
| `application/useApplicationChartSession.ts` | Route Waterfall to its projection on the same owner; expose specialized edit callback. |
| `application/applicationSessionDispatch.ts` | Route Waterfall edits through the existing stamped dispatch; reject Waterfall-only intents for other families. |
| `application/applicationSetupSelection.ts` | Route current Waterfall selection for Set Up. |
| `application/applicationSessionSelection.ts` | Exclude Waterfall from `canSwitchCategorySeries`; retain all saved series in sessionSetup. |
| `application/applicationSessionSetup.ts` | First-field transient selection before post-edit unit admission; retain full transition model/range/selection. Avoid distractor-count legend override. |
| `application/effectiveAppearance.ts` | Add `waterfall` only to `resolveCommonAppearance` accepted union. |
| `compatibility/editorBindings/types.ts` | Permit Waterfall in common editor selection/mapping family unions. |
| `compatibility/editorBindings/eligibility.ts` | Waterfall-specific eligibility: no generic labels/shadow/markers/connect-missing/ticks/inversion. Retain original numeric first-datum category/number/time selector eligibility: G12554 excludes no Waterfall family. |
| `compatibility/editorBindings/selectApplicationEditorState.ts` | Explicit Waterfall admission to common editor projection. |
| `compatibility/editorBindings/mapApplicationEditorEvent.ts` | Explicit `waterfall` namespace; reject unreachable generic series controls; tooltip patch goes under waterfall.tooltip. |
| `caller/themeInputs.ts` | Preserve Waterfall-specific theme overrides and original default zoom policy. Resolve `WaterfallThemePaint` from selected theme provenance. |
| `application/appearanceModel.ts` | Only if storing resolved Waterfall paint on existing theme input is chosen; optional data property, not state/UI. |
| `echarts/cartesianLayout.ts` | Accept Waterfall layout kind; fixed sign legend supplied by renderer. |
| `echarts/cartesianAxes.ts` | Accept Waterfall kind; horizontal order and extent use concrete orientation and cumulative endpoints. |
| `caller/useCallerDock.ts`, `AgChartView.tsx` | Explicit Waterfall caller activation only after both workers and join pass; mode props only. |
| `editor/combo/comboEditorMode.ts` | Add Waterfall mode with controls/onEdit. |
| `editor/ApplicationSeriesEditor.tsx` | Render Waterfall controls in place of ordinary series styles/labels. |
| `editor/setup/ChartSetupPanel.tsx` | Reuse existing direction group, suppress inversion for Waterfall. |

`application/waterfallSessionSelection.ts` calls `sessionBaseline`, `sessionRange`, `sessionSetup`; retains returned full setup; constructs `{...setup, seriesIds: setup.seriesIds.slice(0,1), switchCategorySeries:false}` only for `projectOrdinarySetup`; passes only effective field IDs into appearance and numerical admission. The helper policy should be reused at the Set Up transaction validation call, not duplicated with subtly different filtering. No `setupProjection.ts` algorithm changes are needed.

Common editor transactions may use Range's current pattern of rehydration + map + `reduceSessionOptions`, but retain the generic stamp/address/freshness checks and unknown keys. Update local concrete axes when direction changes so saved reopen and subsequent axis edits agree. Do not route specialized direction edits through Bar family changes.

Theme paint contract, checked against retained engine source on 2026-10-23: `itemTheme2` (enterprise E21861 onward) selects indexed fills 0/1/2 only when the palette type is user-indexed. Item strokes always use named altUp/altDown/neutral stroke values; connector stroke always uses neutral.stroke. The community theme merges named palette overrides over stock defaults (C26633). Palette classification is user-full when up/down/neutral exists, otherwise user-indexed when fills/strokes exists (C25838). Therefore an indexed custom stroke array alone does not replace Waterfall sign outlines or connector stroke. Named overrides remain effective. Stock OpenBB uses default light/dark blue and orange signs, gray neutral; do not derive neutral from indexed position 2, which is green. Parent resolves these facts where selected palette/base-theme provenance is still visible and passes explicit WaterfallThemePaint. No new conventional red/green palette. Existing explicit series fill/stroke overrides apply later in appearance resolution.

Controller also owns `.kiro/complexity-budgets.json`, `.kiro/breadth.toml`, the actual fork changed-file manifests and source/evidence pins. `echarts/lifecycle.ts`, `EChartsHost.tsx`, gallery/catalog/thumbnail, capture, persistence schema, standalone/AI/theme-preview callers, dependencies and unrelated catalog/Perspective work are excluded from both worker write scopes.

## Order, checks and stopping conditions

1. Parent reviews this contract, uses the frozen theme-paint and navigation-policy inputs, creates type file and any nonactivating type-only prerequisite. Record actual measured baselines for all shared files before changes.
2. Lane B may start immediately after that freeze. Lane A starts after W1 has independent numerical acceptance. Both get fresh contexts, exact writable paths and 400 physical lines/file, 300 logical units/file, 50 units/function caps. They are not alone and must preserve others' edits.
3. Parent joins shared paths, including both first-field admission sites, then admits Waterfall at existing caller guards. No flag or extra button. If a worker needs a shared edit, stop that dependency and return it to parent.
4. Independent Astra review checks financial identity, prefix/window invariants, unchanged selection, saved unknown keys, style precedence, control paths, miniature coordinate behavior and regression boundaries. One heavy check/build at a time; no production acceptance from source review alone.

Future commands, not run in this task, from terminalpro with the existing pinned Node on PATH:

```sh
node node_modules/vitest/vitest.mjs run --config tests/unit/chart-compatibility/vitest.config.mjs tests/unit/chart-compatibility/waterfallTotals.test.ts tests/unit/chart-compatibility/waterfallAppearance.test.ts tests/unit/chart-compatibility/waterfallEditorControls.test.tsx tests/unit/chart-compatibility/waterfall.render.test.ts tests/unit/chart-compatibility/waterfall.navigation.test.ts tests/unit/chart-compatibility/waterfall.pointer.test.ts --maxWorkers=1
node node_modules/vitest/vitest.mjs run --config tests/unit/chart-compatibility/vitest.config.mjs tests/unit/chart-compatibility/cartesian.navigator.test.ts tests/unit/chart-compatibility/cartesian.application.test.ts --maxWorkers=1
```

Parent adds actual session/Set Up regression test paths after creating them: mixed-unit distractor initial load and edits; reordering first field; aggregation/count; retained selection on family round trip; saved reopen; direction+axis edits; stale command rejection; tooltip edits use waterfall.tooltip. Original Table/File journey then checks default hidden navigation, miniature, cropping, refresh, ordinary controls, save/fresh reopen and PNG against retained FMP bridge. Positive/negative/mixed/zero/missing fixture comparisons are separate from financial arithmetic evidence. Existing standalone/AI rejection checks must remain unchanged.

Portable complexity command from repository root, with controller-generated current manifests (not historical heads):

```sh
pipeline/.venv/bin/python -m tools.quality.complexity --check --changes workspace=artifacts/chart-waterfall/workspace-changes.json --changes data_api=artifacts/chart-waterfall/data-api-changes.json --output artifacts/chart-waterfall/w2-complexity.json
```

Use the repository's exercised strict-type diagnostic comparison rather than claiming a globally clean `typecheck` against inherited failures. Run scoped format/type checks and combined caps on actual modified paths. Tests and documentation are outside production caps, but their presence does not excuse an oversized production file. A passing future command must be recorded with actual revision, exit and evidence. This proposal has no completed-test claims.

## Source correction before implementation acceptance

Original category-type selection is reachable for numeric first-datum dimensions when not grouped or category/series-switched (G12554-12578). Support category, number and time on the concrete category axis, including its horizontal Y-axis placement; the renderer must use continuous category coordinates where selected. Tooltip enable and single/shared/compact mode are chart-level Waterfall options (G10320, G13950, G14344, G18694/G18909). Preserve separate saved series tooltip options. This corrects the earlier provisional integration notes before acceptance; no control may be hidden to avoid the join.
