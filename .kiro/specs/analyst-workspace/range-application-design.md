# R4f composed application mapping contract

Implement `composeRangeApplication` as the next cohesive consumer: captured/projection inputs and saved appearance become measured axes, a final plot rectangle and the existing Bar/Area mapper output. Calendar and numerical category planning may run beside appearance/layout composition against the interface below. Join and test the real composed output before accepting either lane as R4f. Live session gates remain unchanged until the subsequent control/navigation/pointer join is complete; this is a dependency, not a feature flag or permission checkpoint.

Source-reviewed implementation contract, 2026-10-22, Workspace baseline `5e85724`. Local source research remains in `artifacts/chart-range/r4f-category-planning-source.md`, `r4f-calendar-reuse.md`, `r4e-caller-map.md` and `r4e-interaction-map.md`. Production caps are 400 physical lines/file, 300 logical units/file and 50/function, including every modified shared file.

## Frozen shared boundary

Controller owns a new `echarts/rangeApplicationTypes.ts` before fan-out. Imports refer to the existing application appearance, display, snapshot, Range mapping/projection and linear-density types. All paths below are relative to `src/components/General/Table/Chart/`.

```ts
type RangeFamily = "rangeBar" | "rangeArea";
type Extent = readonly [] | readonly [number, number];
type Window = readonly [number, number];
type CalendarStep = number | string | {
  readonly unit: string;
  readonly step?: number;
  readonly epoch?: number;
  readonly utc?: boolean;
};
interface RangeAxisPolicy {
  readonly min?: number;
  readonly max?: number;
  readonly nice: boolean;
  readonly reverse: boolean;
  readonly interval: {
    readonly step?: CalendarStep;
    readonly values?: readonly number[];
    readonly minSpacing?: number;
    readonly maxSpacing?: number;
  };
}
interface RangeContinuousCategoryInput {
  readonly kind: "number" | "time";
  readonly domain:
    | { readonly mode: "full"; readonly dataExtent: Extent }
    | { readonly mode: "window"; readonly fullExtent: Extent };
  readonly policy: RangeAxisPolicy;
  readonly span: number;
  readonly visibleRange: Window;
  readonly density?: LinearTickDensity;
  readonly labelFormat?: string;
}
interface RangeContinuousCategoryResult {
  readonly category: RangeCategoryInput;
  readonly rawTicks: readonly number[];
  readonly density: LinearTickDensity;
  readonly reverse: boolean;
}
function planRangeContinuousCategory(
  input: RangeContinuousCategoryInput,
): RangeContinuousCategoryResult;

interface RangeNumericAxisPolicy {
  readonly min?: number;
  readonly max?: number;
  readonly nice: boolean;
  readonly reverse: boolean;
  readonly interval: {
    readonly step?: number;
    readonly values?: readonly number[];
    readonly minSpacing?: number;
    readonly maxSpacing?: number;
  };
}
interface RangeNumericAxisInput {
  readonly domain: RangeContinuousCategoryInput["domain"];
  readonly policy: RangeNumericAxisPolicy;
  readonly span: number;
  readonly visibleRange: Window;
  readonly density?: LinearTickDensity;
  readonly preserveConstant: boolean;
}
interface RangeNumericAxisResult {
  readonly semanticExtent: Extent;
  readonly fullExtent: Extent;
  readonly visibleExtent: Extent;
  readonly rawTicks: readonly number[];
  readonly density: LinearTickDensity;
}
function planRangeNumericAxis(input: RangeNumericAxisInput): RangeNumericAxisResult;

interface RangeApplicationInput {
  readonly family: RangeFamily;
  readonly snapshot: ChartSnapshot;
  readonly baseline: OptionBaseline;
  readonly generated: RuntimeOptions;
  readonly theme: ApplicationThemeInput;
  readonly axisRuntime: ApplicationAxisRuntime;
  readonly display: ChartDisplayPolicy;
  readonly precision: number;
  readonly viewport: { readonly width: number; readonly height: number };
  readonly legendSelection?: Readonly<Record<string, boolean>>;
  readonly legendEnabled?: boolean;
  readonly visibleRange?: Window;
  // A navigation re-projection retains this accepted full-domain plan.
  readonly categoryFullExtent?: Extent;
}
type RangeApplicationResult =
  | {
      readonly status: "supported";
      readonly options: EChartsOption;
      readonly projection: RangeBarProjection;
      readonly appearance: ResolvedApplicationAppearance;
      readonly axisRuntime: ApplicationAxisRuntime;
      readonly category: RangeCategoryPlan;
      readonly valueAxis: RangeValueAxisPlan;
      readonly plot: RangeBarMappingInput["context"]["plot"];
      readonly mapping: RangeBarMappingInput | RangeAreaMappingInput;
    }
  | { readonly status: "invalid" | "unsupported";
      readonly diagnostics: readonly SnapshotDiagnostic[] };
function composeRangeApplication(input: RangeApplicationInput): RangeApplicationResult;
```

`mapping` is the exact immutable mapper input used to produce `options`; it is retained for the interaction/navigation join, not a second state owner. Its discriminant is `family` on the composition input; a discriminated mapping wrapper may be used if typing requires one. The existing Bar/Area projection shapes are compatible. Do not generalize `CartesianFamily` by casting Range into it. Common appearance/layout helpers can accept an explicit structural input or the appropriate additional family type in a controller-owned edit.

The category planner only accepts number/time; ordinal wrapping, collision selection and full band extent remain composition responsibilities using `resolveRangeCategory`. It receives `rangeCategoryData(...).paddedExtent` once. `mode: window` bypasses bound replacement and nicing, retaining the full-domain decision. Output extents and tick coordinates stay ascending; reverse is a pixel-transform property. Throwing planner admission is contained by the composed public result boundary. No category numeric label uses the financial value formatter: number categories retain raw numeric identity; time labels use the source automatic calendar formatter or the supported explicit date format.

`planRangeNumericAxis` is exported from new `echarts/rangeNumericAxis.ts`, exclusively owned by lane A. It owns numerical endpoint replacement, density/spacing, optional nicing, explicit step/value tick selection, visible cropping, finite arithmetic admission and deduplication exactly once. It imports the accepted neutral `linearTicks` defaults. Number-category planning calls it with `preserveConstant: false`; the controller adapts existing `planRangeValueAxis` to call it with `preserveConstant: true`. That flag bypasses singleton domain expansion only; it does not suppress applicable explicit tick filtering or labels. In full mode `semanticExtent` is the endpoint-replaced, pre-nice extent. In window mode `semanticExtent` equals the supplied full extent because the original observed semantic extent is deliberately unavailable; no bounds or nicing is reapplied. Existing value-axis calls always use full mode and therefore preserve their established semanticExtent result. `reverse` is retained policy metadata and never changes numeric sorting or extents.

The controller extends `RangeValueAxisInput` with optional `policy?: RangeNumericAxisPolicy`. Existing `bounds`, `density` and `visibleRange` remain source-compatible: absent policy means nice true, reverse false and an empty interval; `bounds.min/max`, when supplied, take precedence over the corresponding policy bounds. Application composition supplies matching bounds or leaves them absent rather than passing conflicting state. The controller leaves public value-axis admission, zero-width-window behavior and `valueScale` construction in its existing owner, replacing only duplicated numerical planning with this call. A temporary controller adapter is not another interval implementation. Tests must prove old default outputs, constant midpoint transport and zero-width-window behavior are unchanged. No shared neutral-file edits belong to lane A during fan-out.

The numeric helper permits `0 <= start <= end <= 1` to preserve existing value-axis zero-width windows. The category planner enforces its stricter `start < end` boundary before calling it. This difference is independent of `preserveConstant`. Lane A owns focused `rangeNumericAxis.test.ts` alongside its category/calendar tests; controller owns existing `rangeValueAxis` regression updates.

## Two disjoint implementation lanes

| Lane | Exclusive writable production files | Concrete output |
| --- | --- | --- |
| A: continuous categories | New `echarts/rangeCategoryAxis.ts`, `rangeNumericAxis.ts`, `rangeCalendarAdapter.ts`, `rangeCalendarLabels.ts`, `rangeAxisValidation.ts` | `planRangeContinuousCategory` and `planRangeNumericAxis` implement the frozen boundaries. Reuse `linearTicks.ts` by import; do not edit it during fan-out. The isolated calendar adapter uses the already-declared MIT `ag-charts-community` 12.1.1 pure scale/interval helpers and is consumed by the planner. |
| B: application composition | New `application/rangeAppearance.ts`, `rangeAxisAppearance.ts`; new `echarts/rangeApplication.ts`, `rangeAxisLayout.ts`, `rangeApplicationAxes.ts`, and `rangeLabelLayout.ts` | `composeRangeApplication` consumes A, accepted `resolveRangeSeriesAppearance`, actual Range projection, `rangeValueAxis`, and both existing translate functions. No duplicate min/max or calendar algorithms. |

Tests are disjoint: A owns new `rangeCategoryAxis*.test.ts` / `rangeCalendar*.test.ts` / `rangeNumericAxis.test.ts`; B owns new `rangeApplication*.test.ts` / `rangeApplication*.render.test.ts`. Both use existing one-worker configurations. Shared types, appearance helper generalization, value-axis policy extension, core reverse/title/grid changes and inventory belong to the controller serial join. Workers may write tests against those frozen contracts but must not race on shared files. They are not alone in the checkout; preserve all other edits and stop only the affected lane if a shared interface must change.

Composition must call the real planners and cores in the joined revision. Test stubs may unblock B's local development; no mocked planner acceptance, unused appearance resolver or new helper-only milestone counts as this slice.

## Saved option and geometry contract

Resolve generated, selected theme/common/family, saved common/family and concrete physical axis layers with the established precedence. Read current `baseline.model.categoryAxisType` through the accepted provenance resolver, rather than trusting captured `rangeCategory.kind` after an edit. Snapshot provenance is required at the actual session boundary. Explicit category suppresses Date inference; numeric epochs never infer time. Category recapture changes the facts; aggregation retains them.

Preserve `axis.interval.{step,values,minSpacing,maxSpacing}`, `nice`, `reverse`, min/max, axis position and all appearance siblings. `tick` remains paint. Number interval step must be a positive number; time accepts the retained admitted unit strings/objects and numeric steps. Calendar epoch is a finite valid Date-range number. String-unit validation must follow retained source, not accept arbitrary strings merely because the transport type is `string`. Callback `every` is outside the existing JSON storage contract and must produce an explicit unsupported diagnostic if encountered, never a silent approximation.

Render explicit values by finite validation, domain filtering, numeric sorting and deduplication; retain the saved array unchanged. This is the explicit adaptation to the core's strictly increasing tick contract. Explicit step/value collision handling must not replace those ticks with an automatic sequence. The source too-dense explicit-step fallback remains automatic when it would produce at least one tick per pixel. Source min/max admission requires min < max when both explicitly supplied, while internal observed singleton extents retain their existing semantics.

For numerical category axes, use neutral linear arithmetic with optional density/interval policy. Preserve the accepted value planner's raw-singleton rule; add optional policy support to that planner at the controller join with defaults exactly matching existing tests. `nice:false` bypasses nicing for either continuous axis. Do not silently route saved value interval policies through the existing default-only value planner. Use raw counts for count aggregation display, existing financial display for values, and independent category formatting.

Calendar selection follows the retained candidates, tie-to-coarser rule, local/UTC interval encoding, Sunday weekly epoch and domain-start alignment. Month/year advancement uses calendar fields; DST days can be 23/25 hours. Automatic labels must vary with interval and hierarchy rather than always applying one fixed date string. Controller authorizes an isolated adapter around the existing MIT community 12.1.1 `_ModuleSupport.TimeScale` and needed pure interval/format helpers, subject to the calendar explorer's pure-instantiation check. This avoids a second calendar engine. No AG chart/scene instance, enterprise import or copied commercial bundle code is permitted. Convert JSON epoch options to native Date only inside the adapter and return numeric ticks. Pin the exact helper API/version contract and test that importing/calling the adapter has no renderer initialization. Internal API dependence stays contained in this adapter; ECharts remains the renderer. Do not replace the accepted default numerical algorithm merely because LinearScale is available from the same package.

Composition reserves title/subtitle, legend and padding using existing common chrome, then bounds label/tick/title feedback to measured final category/value spans. Auto collision retries may lower the proposed tick density; both axes must be replanned from the same final plot, with a finite pass limit and deterministic conservative reservation when space does not converge. Tiny viewports return a finite empty plot/no glyphs instead of negative geometry. Explicit ticks do not enter the automatic retry sequence. Final options must retain the core's exact grid/plot geometry; do not spread common `grid` over it afterward.

Axis paint includes title text/style/spacing, labels, line, ticks and alternating grid styles from `ResolvedApplicationAxis`. A composed axis decorator may add these settings to core axis options, but the tick table and title reservation must agree with the measured layout. Common caption, legend names/field IDs, theme background and legend selection remain observable in returned options. Direction swaps physical axes and their option bindings, without swapping semantic category/value policy.

Controller-owned reverse join adds an optional `reverse?: boolean` to category input/plan and value scale, default false. This changes neither raw identity nor ascending extents. Bar category inverse is `horizontal XOR categoryReverse`; vertical Bar value inverse is `valueReverse`, horizontal value inverse likewise. Area x/y inverse each follows its corresponding reverse. All hand-written preflight/pointer coordinate transforms mirror those engine inversions. Area hit-cell pixel endpoints must be sorted before rectangle clipping; current `rangeAreaHit` assumes ascending x. Reversed Bar endpoint labels must stay attached to min/max identity rather than whichever screen edge becomes lower. Merely setting ECharts `inverse` fails this contract.

## Controller join and visible activation dependency

First join A/B and the shared extensions into one composed render test using captured setup data. This demonstrates application chrome, category ticks and final geometry together, but does not claim a visible session yet. Keep this as one active delivery slice continuing toward activation, without publishing a foundation-only image.

Actual activation then adds `rangeSessionSelection`/`rangeSessionProjection` and Range editor state to existing session/setup/storage dispatch. Widen `ApplicationChartFamily`, ready union, hook forwarding, `AgChartView` and caller dock only in that joined change. Include caller descriptor/initial-axis propagation and refresh/recapture synchronization: `sessionDataKey` currently omits `initialAxes`, so an initial inference patch alone cannot preserve changed category facts and local saved preferences.

Use existing editor panels and transactions: setup aggregation/order, both Bar directions, Area interpolation/markers/missing-data/shadow, labels/tooltips, semantic and physical axes, title/subtitle, grid, legend, padding/background and all existing navigator controls. Bar's original hidden category type/tick selectors are retained original eligibility, not new removals. Saved advanced axis options still apply. Do not borrow Box's category-only eligibility or tick-extension rejection.

The full live join requires navigator slider/miniature/wheel/pan/reset adapters and the accepted pointer bridge. Navigation consumes the exact full-domain plan and current enabled fields, preserves window across legend replans, and regenerates geometry/candidates after viewport changes. Common lifecycle forwarding must carry the final interaction projection. Source-exact hover, zero-distance paging and exact-category shared rows cannot be replaced by engine snap. These are coupled activation work, not reasons to disable controls or expose a reduced Range family early. Grouped Grid hierarchy remains outside currently admitted capture; do not reinterpret statistical `sourceMode: grouped` as hierarchy support.

## Planned checks and acceptance

- A: independently expected number ticks/bounds/nice false and both explicit interval forms; epoch irregular spacing; month-end/leap-year and DST spring/fall ticks under pinned local timezone plus UTC; multi-month domain-start alignment and Sunday weeks; empty/singleton/invalid-Date-range boundaries; cropped window retaining the same full extent; duplicate explicit values preserved in saved state and unique in rendered ticks.
- B/join: actual SVG/custom geometry from `composeRangeApplication` for category, `[0,100,1]` number categories and irregular native-Date capture; both Bar directions and both axis reversals; min/max labels and Area hit cells after reverse; explicit bounds and interval controls; title/subtitle/axis title/grid/legend/theme changing measured plot and actual output. Assert ticks and glyph positions against independent values, not snapshots of the planner's output.
- Session activation: category editor override, selected-category recapture, refresh, direction switch, legend reflow, resize, navigation/miniature/reset, save/reopen and export through existing application paths. Retain existing Box/ordinary regressions at every shared boundary. All previously reachable controls remain reachable and effective.
- Controller: focused one-worker tests, strict typing with parent-baseline comparison where necessary, scoped formatting, explicit current changed-file manifests and existing complexity checker. Register new owned production files in inventory; review final shared-module caps. One heavy gate at a time; no installs/builds during parallel implementation.
- Independent review challenges both algorithm semantics and real consumers before acceptance. Reconcile owning tasks, breadth and README/docs checkboxes to actual evidence. Full visible milestone still needs application/browser verification and real FMP range extrema, dates, units and transformations using recorded source/image provenance and selected reviewed chart samples. No synthetic helper tests establish that milestone.

This design is disproved if saved nice/interval/reverse options disappear, captions/grid change only editor state, navigation renices the crop, category ticks do not use final plot span, or `composeRangeApplication` remains absent from the eventual active session projection.

## Task acceptance

- [x] R4f.A: continuous category and shared numerical planning, consumed by composition.
- [x] R4f.B: effective appearance and measured application composition.
- [x] R4f.join: reverse/value policy integration, actual composed rendering, independent review and shared gates.
