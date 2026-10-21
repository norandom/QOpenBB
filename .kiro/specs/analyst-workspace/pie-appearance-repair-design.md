# P4 pie appearance repair design

V1 source is independently accepted at `008fbd1`. The native selection proof and immutable metadata foundation are independently accepted at `ab50456`; V2-L/V2-H implementation is authorized under the reviewed interface below. V2 source is independently accepted at `e5e3e36`; P4 image/visual acceptance remains open. The accepted font repair `ff8878c` remains outside V2 ownership.

## Evidence and scope

Reference: [recorded reference evidence](../../../artifacts/reviewed/chart-pie/verification.md#p4-first-image-and-control-repair), source `38dffc33389aca0e4a87e0e88d42f7067aa220df`, original image `sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f`. Candidate: P3 source `2d91255`, existing `p4-browser-fmp-2` candidate run. The controller must retain its complete image digest in the final record rather than infer it from source. Inspected all eight light/dark default PNGs in `p4-reference/run-05/extracted/original-{pie,doughnut}-{light,dark}.png` and `p4-browser-fmp-2/browser-output/pie-fmp-captured-AAPL-quar-75ee9-s-refresh-and-reopen-export/default-{pie,donut}-{light,dark}.png`.

Both images are 619 by 284 CSS/bitmap pixels, DPR 1. Original Pie has no legend, a larger disc, and four callout/value pairs. Original Donut has square legend markers, six entries across two rows, a `1 / 2` pager, outer Revenue title, and outer callouts only. Candidate has circles, three unpaged rows, missing title, smaller geometry and overlapping inner callouts. The actual original saved model retains common `legend.maxHeight=50`, marker shape `square`, size 11, marker padding 5, item padding X/Y 32/8 and spacing 20. Both label toggles are enabled; absence of numeric labels in narrow rings is fitting behavior.

The financial input remains FY2025 AAPL quarterly revenue/gross profit in raw USD, with separate totals 416,161,000,000 and 195,201,000,000. No repair may change observations, normalized denominators, palette identity, setup aggregation or native slice-key identity.

## Source-backed contracts

Original bundled sources below are retained in `artifacts/task-2.1/frontend/terminalpro/node_modules/`. Line numbers refer to that retained bundle, not other builds.

| Contract | Inspected source | Repair consequence |
| --- | --- | --- |
| Theme legend limits and markers | Current original-derived `Chart/themes.tsx:80` | `pieLayout` currently hardcodes circles; common appearance drops maxHeight/shape. Carry effective values into pie layout without changing other chart defaults. |
| Donut field titles | `ag-grid-enterprise/dist/package/main.cjs.js:45763`, `PieChartProxy.getSeries` | Every named donut field generates `title.text=displayName`; `showInLegend` is true for multiple fields. Pie generates no series title. Do not hardcode Revenue or equate title visibility with legend visibility. |
| Title typography and placement | `ag-charts-community/dist/package/main.cjs.js:47129`, `donutTheme`; `:46242`, `getTitleTranslationY` | Default title is enabled, Verdana 14px, subtle theme text, spacing 5. Baseline is `-outerRadius-2-spacing`, centered, bottom aligned. Theme/saved series-title options retain precedence. |
| Surrounding-ring bounds | Same Charts bundle `:49354`, `PolarChart.computeCircle`; `:46509`, `bboxIntersectsSurroundingSeries`; `:46279`, title visibility | Sort rings by their effective inner radius. Each except the outermost uses the next larger inner radius as surrounding boundary. Reject a title box if any corner lies outside it. Collapsed radii and saved ratios are evaluated geometrically, not by ring index. |
| Callout suppression | Same bundle `:46755`, `computeLabelsBBox` | During hide-needed passes suppress vertical overflow, severely truncated labels and surrounding-ring overflow. Title exclusion area, collision offsets, min spacing and angle also participate. The stock two-ring sample hides inner callouts because their boxes exceed the surrounding hole; other dimensions/labels may fit. |
| Polar fitting | Same bundle `:49354-49465`, `computeCircle/refineCircle` | The original refines measured label bounds iteratively. Current fixed margins are an approximation. First correct legend reservation and compare: removing Pie's unexpected legend and Donut's extra row explains the observed radius deficits. A full refinement port is outside this repair unless a residual matched-image failure demonstrates the need. |
| Sector fit | Same bundle `:46780`, `updateSectorLabelNodes` | Existing four-corner sector containment and configured ratio/offset are the correct principle. Preserve enabled state when text cannot fit; recompute after toggles/resize. |
| Legend pages | Same bundle `:35025`, `gridLayout`; `:36245`, `calculatePagination` | Row/column packing uses measured boxes and maximum column widths, item padding, maximum available width/height and pager footprint. Paginate rather than silently exceed maxHeight or truncate entries. |

Installed ECharts 6.0.0 was inspected at `/home/mc/qopenbb-work/echarts-probe/node_modules/.pnpm/echarts@6.0.0/node_modules/echarts/lib/component/legend/ScrollableLegendView.js:164`. Horizontal scroll layout supplies no horizontal wrapping limit. Replacing `plain` with `scroll` would yield a single row and fails the observed original two-row contract.

## Task V1: effective default and retained appearance

One owner changes only `application/pieAppearance.ts`, `application/pieSessionSelection.ts`, `echarts/pieTypes.ts`, `echarts/pieAdmission.ts` and a new focused `tests/unit/chart-application/pieAppearanceDefaults.test.ts`. The reviewed V1 scope also included only the default-legend assertion and explicit-enabled one-field slice-legend/reprojection case in `tests/unit/chart-application/pieProductionJoin.test.ts`. Paths are relative to `vendor/workspace/terminalpro/src/components/General/Table/Chart/` unless prefixed `tests/`.

Pass the effective assignment count into `resolvePieAppearance`; use `assignment.assignments.length > 1` only as the fallback legend enabled value. Pie renders at most one assignment even when setup retains multiple numeric selections. Donut uses its actual resolved rings, including transpose. Explicit common/family theme and saved values continue to override this fallback. Do not patch persisted options during render or interpret selected numeric count as rendered count.

Resolve pie-specific legend layout additions (`maxHeight`, optional `maxWidth`, marker shape and pagination appearance) and series-title appearance from the existing composed layers. Keep these in the pie style extension rather than widening editor controls or changing all families' common defaults. Use finite admission checks and copied immutable values. Title text comes from each assignment's snapshot descriptor, including an assigned empty ring; do not obtain it from the first data observation. Source option precedence remains the existing composition's responsibility. The actual title appearance defaults are source-derived; no AAPL-specific values enter production.

Freeze V1's interface as follows. `resolvePieAppearance` receives a required `assignmentCount: number` alongside its existing input; `selectPieSession` supplies `assignment.assignments.length`. Reject noninteger/negative counts. `PieMappingInput.style.legendLayout` is a required `ResolvedPieLegendLayout` with `maxHeight?: number`, `maxWidth?: number` and `markerShape: string`. Undefined dimensions mean no explicit bound; defined dimensions must be finite nonnegative values. Resolve these from effective `legend.maxHeight`, `legend.maxWidth`, `legend.item.marker.shape`, with the original theme's 50/square values and source default square fallback. Do not add pager fields in V1.

`ResolvedPieSeries.title` is required and typed `PieFont & { readonly spacing: number }`. It resolves effective `series.title.enabled/fontFamily/fontSize/fontWeight/fontStyle/color/spacing`, with original default enabled, Verdana 14, weight 400, spacing 5 and the original subtle-text theme mix (38% toward chart background from theme text). It contains no field text. `PieFont` already carries enabled/font/size/color/weight/fontWeight/fontStyle. Title text will be derived per assignment in V2; no extra appearance state owner is introduced. Existing direct mapper fixtures must supply these required fields; include `tests/unit/chart-compatibility/pie.fixtures.ts` in V1 test ownership. `pieAdmission` validates and copies the additions using existing font/numeric rules, with focused `pie.test.ts` admission cases also owned by V1. V2 owns any pager presentation metadata; it is not a V1 prerequisite.

Completion: new/empty/one/two-assignment defaults; Pie with two setup fields; one/multiple transposed donut rings; `doughnut`; explicit true/false at common/family/saved layers; retained title and legend dimensions/shape through resolution. Whole modified production files pass 400 physical lines, 300 logical units and 50/function. This task alone does not close the visual defect.

## Task V2: original layout with the current renderer owner

Execute after V1 and freeze its types before editing. One integration owner handles the coupled geometry, legend and lifecycle work. Preserve every existing gallery/editor control and saved path. No feature flag, alternate chart owner, editor clone or provider work.

### Geometry and labels

Extract a cohesive pure helper `echarts/pieLabels.ts` for measured title/callout boxes and surrounding containment. Keep current common-radius/ring geometry in `pieLayout.ts` and native sector/label option emission in `pieSeries.ts`. Add per-ring title metadata in `pieData.ts`/`pieTypes.ts`, resolved from the assignment descriptor even for no observations.

Include actual visible legend height plus configured spacing in the existing geometry calculation. This is the first radius repair; do not implement the original iterative fitter speculatively. Compute surrounding radii from the resulting effective geometry. Emit silent title graphics inside the same ECharts canvas so export includes them. Reject overflowing title/callout boxes using the original surrounding-radius rule, including title exclusion where applicable. For constrained inner callouts, use native `labelLayout`/per-datum `label.show` with measured positions and prevent subsequent collision movement through the surrounding ring. Keep existing outer native layout unless a test demonstrates a defect. Native pie series and leaders retain sectors, tooltip hits and filtering; sector companions stay silent with shared geometry/keys. Preserve independent label enablement, raw values, leader length/width/offset, rotation and saved radii.

Default original geometry is an image acceptance target, not a hardcoded radius. Validate rotated, long-label and resized cases. Keep zero-total outlines and collapsed-ring handling. If residual fitting differs after legend/title/bounds repair, report the exact failed image and obtain a bounded design amendment for that case before expanding layout scope. Thick-stroke differences remain subject to matched original comparison; do not certify them from radius arithmetic.

### Multirow legend adapter

Add `echarts/pieLegendLayout.ts` for pure measured packing and `echarts/pieLegendBinding.ts` for renderer-local paging. Pack entries in assignment/observation order with source-derived maximum column widths, square markers, spacing and available maxHeight/maxWidth. Account for pager footprint until page count/footprint stabilizes within a bounded iteration count. Reserve the maximum page height so changing page does not resize the donut.

Use native plain legends positioned at computed cells (one item component per cell if row layout cannot preserve the measured columns). Keep the first hidden canonical legend's `data` equal to every stable item key; all native legends receive the same selected map. This is required because `lifecycle.legendOptions` currently reads the first legend. Visible items retain native legend click/hover behavior and painted main-series providers. Do not introduce a second selection map or make graphics fake slice toggles.

The pager uses canvas graphics for original arrows/counter and a lifecycle-bound event handler. Extend the supported pie translation result, pie ready value and `ChartRenderRequest` with optional immutable `legendPagination` metadata: page anchors/item keys, visible component IDs and pager graphic IDs/placement. Non-pie callers omit it. `projectLegendSelection` still returns options and retains its existing financial reprojection role; pagination metadata is independent of selected fractions and is replaced on a new ready revision. The binding decorates freshly projected options with current-page visibility immediately before `setOption`.

Only the existing renderer lifecycle owns the transient page anchor. Preserve it on same-scope refresh/resize by key, clamp when items disappear, reset on scope/family change, detach listeners on release/disposal, and reject stale-generation callbacks. Page clicks must neither write Widget storage nor advance render revision; export must include the currently drawn page. Route binding failure through existing error/export invalidation. All keys remain available on other pages and accessibility traversal; add keyboard-focusable pager/legend access through the same lifecycle/container if current native canvas access cannot supply equivalent controls. Such access dispatches native actions and shares the binding's page anchor, without another React state owner.

Before completing this adapter, prove in actual ECharts that a click in a visible component updates the canonical all-key selection and that reprojection keeps every component synchronized. If this fails, stop and review that seam; do not bypass it with a parallel selection store. Also prove that hidden page components neither paint nor steal hits and that the first provider remains the painted series.

### Frozen V2 metadata and lifecycle contract

These definitions supersede the provisional metadata description above. V1's approved types remain unchanged. The controller creates `echarts/pieLegendTypes.ts` after independent interface review and before any two-lane implementation. All rectangles are finite CSS-pixel coordinates in the chart container; width/height are nonnegative. All keys are existing `pie-item:` identities, never display text. IDs have a reserved `openbb-pie-legend-` prefix and are unique within options.

```ts
interface PieLegendRect {
  readonly x: number;
  readonly y: number;
  readonly width: number;
  readonly height: number;
}
interface PieLegendItem {
  readonly key: string;
  readonly label: string;
  readonly legendId: string;
  readonly bounds: PieLegendRect;
}
interface PieLegendPage {
  readonly anchorKey: string;
  readonly items: readonly PieLegendItem[];
}
interface PieLegendPagination {
  readonly canonicalLegendId: string;
  readonly pages: readonly PieLegendPage[];
  readonly pager: {
    readonly previousId: string;
    readonly nextId: string;
    readonly counterId: string;
    readonly previousBounds: PieLegendRect;
    readonly nextBounds: PieLegendRect;
  };
}
```

For insufficient layout space, match the original legend visibility rule: force a minimum cell only when both effective maxWidth and maxHeight are explicitly defined. Otherwise an unsatisfiable layout keeps the hidden canonical all-key legend but emits no visible items, pager, pagination descriptor or visible legend reservation. This does not change saved enabled state or native selection; a later fitting viewport or style projection restores normal layout.

Every eligible key occurs in exactly one page; each page is nonempty and its anchor is its first key. Bounds are the item's placement on its own page, not an accumulating offset. Include metadata for a visible one-page legend too, so keyboard slice access is consistent; hide/disable pager graphics for fewer than two pages. Omit metadata for a disabled or empty legend. Canonical legend is always array index zero, `show:false`, `selectedMode:true`, with every key exactly once. Each item has one native single-entry plain legend component, `selectedMode:true`, positioned by its measured cell. Every component receives the same full selection map. The pure mapper initially shows page zero and includes all page components, hiding the others. `legendPagination` is a rendering descriptor only: no selected map, current page, callback, provider data or revision is stored in it.

Extend the successful `TranslatePie` result in `echarts/pieTypes.ts` with optional `legendPagination?: PieLegendPagination`; keep invalid/unsupported variants unchanged. Do not widen `CartesianTranslationResult` globally. Pass the descriptor unchanged through the `kind: "pie"` ready member in `application/applicationChartSessionTypes.ts`, `application/pieSessionProjection.ts`, `application/useApplicationChartSession.ts` host props, and optional `ChartRenderRequest.legendPagination` in `echarts/lifecycle.ts`. `echarts/EChartsHost.tsx` includes it in latest refs, lifecycle update arguments and update-effect dependencies. Non-pie branches explicitly omit it. The existing `projectLegendSelection` callback still returns only ECharts options; all page packing and titles depend on unchanged observations/style/viewport, while selected fractions only change polar geometry. Fresh session projections replace metadata whenever those layout inputs change.

`echarts/pieLegendBinding.ts` exports this lifecycle-owned interface (types may be exported from the binding rather than duplicated in the pure metadata module):

```ts
interface PieLegendPorts {
  readonly container: HTMLDivElement;
  readonly isActive: () => boolean;
  readonly readSelected: () => Readonly<Record<string, boolean>>;
  readonly toggle: (key: string) => void;
  readonly repaint: () => void;
  readonly fail: (error: unknown) => void;
}
interface PieLegendBinding {
  project(options: EChartsOption, plan: PieLegendPagination | undefined,
    scope: string | undefined): EChartsOption;
  sync(): void;
  handleClick(event: unknown): void;
  dispose(): void;
}
declare function createPieLegendBinding(ports: PieLegendPorts): PieLegendBinding;
```

`project` returns a new options object with current-page visibility, pager counter/enabled paint, and pager event metadata; it must not mutate mapper options. It selects an anchor on first plan/scope, preserves it when a key still exists, or clamps the prior page ordinal when that key disappears. Changing page sets the anchor to the target page's first key. New scope resets page zero. Omitted plan clears paging/accessibility. `project` never calls `setOption`, `dispatchAction` or the session. `sync`, called only after successful `setOption`, updates DOM accessibility controls from the accepted plan and `readSelected`; failure releases the renderer through the existing lifecycle error path. If render fails, release/dispose removes the provisional binding and controls, so no unaccepted drawing can be exported.

The lifecycle creates one binding for each engine generation and disposes it in `release`. It registers one `instance.on("click", listener)` forwarding only current-generation events to `handleClick`, and unregisters the same listener on release. Binding `project` runs after `legendOptions(request)` and before the single existing `setOption(...,{notMerge:true})`; `sync` runs after that call succeeds. Canonical selection remains read from native legend zero. `toggle` dispatches native `legendToggleSelect` with the stable key and no legendId filter, causing the existing `legendselectchanged` listener to reproject financial geometry. `repaint` invokes the same forced render path as current legend refresh, for the current request, without advancing revision. `isActive` rejects disposed, applying, unsized or stale-generation work. One shared lifecycle interaction-error handler releases the renderer and calls the current request's `onError`, preserving export invalidation.

Pager graphics use supported `graphic.info` event data `{ kind: "pie-legend-page", direction: -1 | 1, token: number }`; `project` assigns a new binding-local draw token. `handleClick` requires `componentType === "graphic"`, the exact kind/direction and current token. Disabled boundary directions do nothing. It does not intercept legend clicks, chart pointer events or native hover. ECharts 6's inspected `component/graphic/GraphicView.js:setEventData` exposes `info` in graphic click events. A stale queued pager event cannot affect a newer drawing even within the same engine generation.

Add `echarts/pieLegendAccessibility.ts` only for DOM control projection/disposal, called by the binding; it owns no page or selection state. Use stable keyed buttons/switches inside the existing host container, retain focus across sync, and remove them on dispose. Visible item proxy bounds match the native item. Proxy controls pass pointer events through so mouse selection remains native; Enter/Space dispatch exactly one native action. Off-page items remain in accessible traversal; focusing one asks the same binding to reveal its page and places its focus outline over that item's new visible bounds. Pager controls are named Previous/Next legend page, have real disabled states, and Enter/Space use the same binding action as graphic clicks. Announce the current page with an accessible status. `aria-checked` is read from the native canonical map after render, never cached as another selected-state owner. Canvas pager/counter remains the exported visual, and accessibility DOM must not alter chart size or appear in PNG export.

### V2-P: mandatory native selection proof before adapter production

One worker owns only new `tests/unit/chart-compatibility/pieLegend.render.test.ts`. No production changes, image build, dependencies or browser run. After the controller grants the unit-test slot, reuse the existing P2 configuration and fake text measurement with actual SVG SSR ECharts:

```sh
node node_modules/vitest/vitest.mjs run \
  --config tests/unit/chart-compatibility/vitest.config.mjs \
  tests/unit/chart-compatibility/pieLegend.render.test.ts
```

Run from the staged `terminalpro` checkout with the existing pinned Node/dependencies; record that checkout/revision and command/exit. The configuration already supplies the bounded worker policy. This is a planned command until executed. The inherited `lifecycle.test.ts` mock omits ECharts `ComponentModel` and fails before collection, as recorded in the P3 evidence. Do not cite that suite as passing or use a full ECharts mock for this proof.

Build a tiny test-only option from existing pie fixtures: two independently keyed rings, painted series before transparent companions, a hidden full-key canonical legend and visible per-item components across two pages. Prove all four conditions:

1. Actual engine rendering retains every initially enabled sector despite other legend components having single-entry data. Hidden canonical/page components do not draw text or hit targets; visible swatches use painted main-series colors.
2. Invoke the visible legend's actual registered click target in the engine view (following its generated clickable hit rectangle, rather than manually calling the application's handler). Confirm exactly one native `legendselectchanged` event, canonical key becomes false, every legend component agrees for that key, and the equal-caption item in the other ring stays true. This exercises native click dispatch. A separate explicit `dispatchAction` is useful but is insufficient alone.
3. Reproject using canonical native selection and existing `translatePie`, then decorate test options with the same components. Assert correct ring-local remaining fractions, aligned companions, and retained off-page keys. Restore through the visible native click. Switch page by updating component visibility and repeat on page two, preserving page-one selection.
4. Disable every item in one ring, then restore a page-two key; check zero-total outlines/recovery, no other-ring filtering, and rendered SVG current-page text after a notMerge repaint. This proves native semantics/exportable drawing only, not production lifecycle/PNG export or keyboard behavior.

Read-only source support: ECharts 6 `component/legend/LegendModel.js:_updateData` builds `_availableNames` from all raw series independently of each component's displayed `data`; `legendAction.js:legendSelectActionHandler` synchronizes selection across components; `processor/dataFilter.js` nevertheless requires every legend to select each datum. That last interaction makes this proof a hard prerequisite. If it fails, stop V2 adapter implementation and revise the seam; no parallel selection map is authorized. The proof file becomes a retained regression and is handed to the layout owner after its reviewed acceptance.

### Bounded ownership and execution waves

Default to one V2 implementer after V2-P. Two implementation lanes are allowed only after the controller lands the exact `echarts/pieLegendTypes.ts` interface above and the proof passes; all production files listed here are explicitly under `src/components/General/Table/Chart/`.

| Wave/owner | Exclusive writable production paths | Tests/output |
| --- | --- | --- |
| V2-P proof owner | None | New `tests/unit/chart-compatibility/pieLegend.render.test.ts`; real-engine selection proof |
| Controller interface foundation | New `echarts/pieLegendTypes.ts` only | Reviewed types and ownership/inventory entry |
| V2-L pure layout owner | `echarts/pieTypes.ts`, `echarts/pie.ts`, `echarts/pieData.ts`, `echarts/pieLayout.ts`, `echarts/pieSeries.ts`; new `echarts/pieLabels.ts`, `echarts/pieLegendLayout.ts` | `pie.render.test.ts`, new `pieLayout.test.ts`, accepted proof file; mapper metadata/default pages, bounded geometry/title fit |
| V2-H lifecycle owner | `echarts/lifecycle.ts`, `echarts/EChartsHost.tsx`; new `echarts/pieLegendBinding.ts`, `echarts/pieLegendAccessibility.ts` | New `pieLegendBinding.test.ts`; `lifecycle.test.ts` mock repair and lifecycle regressions; no pure layout edits |
| Controller integration after both reviews | `application/pieSessionProjection.ts`, `application/applicationChartSessionTypes.ts`, `application/useApplicationChartSession.ts` | `pieSessionOwner.test.tsx`; existing application/browser scenarios and join checks |

The lifecycle owner fixes the known test mock narrowly by retaining actual module exports and overriding only `init`, or by a reviewed equivalent mock boundary; it must independently show the suite collects and executes. Do not count this repair as native engine evidence. A meaningful failing lifecycle assertion must fail under an intentionally broken page/release/selection path. New accessibility helper tests verify native dispatch ports and focus behavior; actual UI keyboard interaction remains P4.

Neither lane edits `application/pieAppearance.ts`, `application/pieSessionSelection.ts`, `echarts/pieAdmission.ts`, shared fixtures or V1 tests after V1 acceptance unless the controller reviews a necessary contract correction. No lane edits the other's tests, the font transaction, production-join tests, inventories, specs or commits. Workers are not alone in the checkout and must preserve concurrent changes. The controller handles inventory/breadth updates and serializes shared propagation, heavy checks and commits. Every lane passes whole-file 400 physical/300 logical/50-function checks, including shared lifecycle/host files; the accessibility extraction has a real DOM projection responsibility, not a cap workaround.

### Remaining joined checks

`AgChartView` already spreads `session.hostProps`; no second mount is needed. Shared type seams carry only the optional immutable descriptor. The table above is the complete V2 writable production scope; further paths require controller ownership review. Current radius calculation remains in place, corrected for the actual maximum visible-page legend footprint. Full iterative polar layout remains deferred unless a matched comparison or meaningful fitting case demonstrates a residual failure.

Extend existing `tests/unit/chart-compatibility/pie.test.ts`, `pie.render.test.ts`, `lifecycle.test.ts` and add focused `pieLayout.test.ts`/`pieLegendBinding.test.ts`. Exercise real ECharts click/actions, duplicate category names across rings, page 2 selection/restore, all disabled/zero outlines, page changes followed by export, same-scope refresh, resize reflow, stale/disposed handlers and family reset. Geometry checks cover dynamic field titles, surrounding-ring suppression and a fitting inner-label case, narrow-ring numeric suppression, wider/single rings that fit, disabled labels reclaiming room, saved typography/rotation/radii and long categories. Prior-family lifecycle regressions must pass.

Use existing unit configurations with one worker and scoped strict TypeScript/lint. The controller supplies exact current check commands from the accepted P3 harness and explicit fork manifests for the portable complexity command in `docs/complexity.md`; do not invent a runner. Update `.kiro/complexity-budgets.json` ownership and `.kiro/breadth.toml` with actual paths before acceptance. Every new/modified production file as a whole must pass 400/300/50; measure shared lifecycle/session seams and extract a cohesive binding before growth breaches a cap. The accepted checker foundation is reused, not replaced by policy text.

## P4 closing gate

Independent review checks source contracts and native interaction evidence before one serialized Dagger candidate build. Reuse the existing isolated, headless one-worker application scenario and captured CSV; no new provider request. Record full source SHA, image digest, command/exit and artifact hashes. Capture both themes at the original 619 by 284/DPR 1 with editor closed, fonts settled, pointer out and fresh stable drawing. Compare Pie no-legend disc/callouts/values and Donut marker geometry, two rows/page counter, Revenue title, ring bounds and fitted labels against the original PNGs. Default and explicit legend override must both work.

Verify page 2 exposes the remaining Gross Profit items; toggling Gross Profit Q3 must leave Revenue Q3 unchanged and recompute only its ring denominator. Repeat meaningful callout/sector control edits, title/legend styling, refresh, save/reopen, theme switch and export; compare the original styled reference where applicable. Check console/network failures. Numeric labels absent solely because they do not fit must not be classified as disabled controls. Acceptance requires the actual images and effects, not visible buttons or unit options. Publish only the reviewed concise record and representative financial screenshots after controller acceptance; keep this diagnosis and intermediate runs local.

Core steering `product.md`, `tech.md` and `structure.md` were absent at inspection. Applicable complexity, testing, delegation and documentation steering plus the pie milestone/integration/renderer designs were read. This read-only design did not change implementation, dependencies, providers, browser runtimes or commits.

Controller join ownership includes `tests/unit/chart-compatibility/pie.test.ts` only if a concrete V2 output/admission regression requires it. No additional matrix is required.

## P4 side-legend correction

The identified `e5e3e36` image exposes a side-legend sizing defect: after moving the legend right, the mapper allocates almost the entire plot width to legend columns and leaves no drawable rings. This is separate from the default appearance accepted by the owner on 2026-10-21.

Restore the original orientation-aware available-width rule from `Legend.calculateLegendDimensions`: for side legends without an explicit maximum width, use the original aspect-ratio coefficient rather than the full padded viewport width. Preserve explicit dimensions, the accepted top/bottom layout, stable keys, selection and all reachable pages. The layout owner may modify only `echarts/pieLegendLayout.ts` and its existing `pieLayout.test.ts`; the controller owns records and image verification. Require a failing regression before the fix, positive drawable rings and reachable keys for the reported side layout, explicit-bound behavior, whole-file 400/300/50 caps and independent review. Verify the actual right-legend control in the rebuilt FMP journey before closing P4.

## P4 tooltip replacement correction

The rebuilt side-legend image passes the right-legend, control, native paging, selection and refresh checks, but reports a tooltip exception before reopen. A real-engine reproduction isolates the sequence: a visible native legend tooltip, resize scheduling a refresh, then `notMerge` replacing the tooltip view while the engine remains active. The old pending callback targets disposed tooltip content.

Use the public `hideTip` action within the existing applying guard immediately before every existing notMerge option replacement, including transitions whose next options omit a tooltip. It clears the old view's saved hover target so its pending callback has no content to show. Retain normal subsequent tooltips and existing release/export invalidation on failure; do not suppress errors, access private engine state or introduce a second tooltip owner. The lifecycle owner may modify `echarts/lifecycle.ts`, its existing unit tests and a cohesive actual-engine timer regression. Require meaningful timer reproduction, action ordering, failure handling, restored tooltip operation, whole-file 400/300/50 caps and independent review. Rebuild and pass the unfiltered FMP diagnostics before P4 acceptance.
