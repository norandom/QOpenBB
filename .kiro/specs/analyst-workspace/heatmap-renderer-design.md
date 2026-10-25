# Heatmap renderer and controls

Build the replacement inside the existing chart host and editor. HM1 already supplies the wide matrix. This design adds appearance resolution, painting and editor intents without creating another capture, aggregation or storage owner. Application routing remains a later atomic join.

## Verified original behavior

The source pin and runtime qualification are recorded in the [data contract](heatmap-data-contract.md). Original runs 5 and 10 extend the finite-data observations; failed observer attempts remain local and are not passes. Complete probe source and runner copies accompany these later runs.

- A constant value of 5 renders with the default middle palette color `#e1cc00` and a single legend value 5. Pinned AG Charts selects `colorRange[floor(length/2)]` for a constant domain.
- No category produces row ordinals 1, 2, 3. No series exposes the native message "No data available to be charted"; an internal hidden canvas may remain in the DOM. No-series model serialization was not captured.
- Both axes are category axes. A horizontal thickness change writes `chartOptions.heatmap.axes.category.bottom.line` and `.top.line`; a vertical change writes `.left.line` and `.right.line`. Widths 4 and 7 remain distinct and visibly affect the corresponding plot edges. Do not substitute ordinary category/number identities.
- Gradient legend uses `heatmap.gradientLegend`, including `enabled`, `reverseOrder`, `position`, `spacing`, `gradient.thickness`, `gradient.preferredLength` and label styling. Observed positions are Top, Right, Bottom, Left. Default right-side dimensions are thickness 16, preferred length 200, spacing 20.
- Series controls expose labels, font, line color/width/opacity, tooltips and Single/Multiple/Compact modes. Titles include chart title, subtitle and both axis titles. The native axis sections expose line, ticks, labels and auto-rotation; no numeric/time conversion or grid section is offered for Heatmap.

Run 10 saved `heatmap.tooltip.enabled=false` while a new signed-cell hover still showed a tooltip. Its reversed legend displayed reversed numbers against an unchanged gradient, so color/value correspondence disagreed with the cells. The owner approved correcting both behaviors on 2026-10-25: disabling tooltips must suppress cell tooltips; reversing the legend must reverse its gradient and labels together while preserving the cell color/value mapping. Keep the existing controls and saved leaves.

## Palette and cell semantics

Pinned AG Charts 12.1.1 source uses evenly spaced palette stops with OKLCH interpolation over the finite extent. Built-in light and dark themes use `#ffa03a`, `#e1cc00`, `#459d55`. No automatic zero-centered domain is introduced.

A custom theme object alone does not change that default. Native palette-type selection depends on explicit fills/strokes or up/down/neutral colors. For a custom indexed/full palette, the Heatmap default range takes the first two fills circularly; one fill is repeated. Non-string fills such as gradients/patterns use the source's fallback fill. An explicit series color range overrides the palette-derived default. Preserve this precedence in a small stateless theme-paint adapter; do not reuse the hierarchy palette resolver's unconditional diverging range.

Use the accepted matrix's finite cells for value extent, labels, tooltips and provenance. A missing cell may need transient transparent rectangle geometry so configured borders remain visible, as established by pinned native source. Such geometry is not a numeric observation and must never become a zero, tooltip value, extent input or aggregate. All-missing domain appearance and public-grid undefined admission remain explicitly open before application acceptance.

Prefer one ECharts custom rectangle series through the existing SVG host. Numeric x/y category indices preserve repeated row labels. Compute cell rectangles through public Cartesian coordinates with source-equivalent floor/ceil bounds, clipping and zero category-band gaps. This permits transparent missing geometry and label fitting without a second renderer or state owner. Native ECharts Heatmap remains an alternative only if it satisfies the same missing-border, labeling and identity contract with less code.

Reuse pure color, gradient-layout and hover primitives where their contracts fit. Internal hierarchy-prefixed names do not require a separate rename/refactor task. Do not reuse hierarchy leaf/subtree weighting or its hover projection; Heatmap supplies finite cell identities. Existing host revision, resize, disposal and PNG export stay authoritative.

## Frozen interface preparation

The exact proposed declarations are retained at `artifacts/chart-heatmap/heatmapTypes.proposed.ts`. Independent review accepted the materialized declarations at `application/heatmapTypes.ts`. Their frozen SHA-256 is `729ba59722dfae0bc315219aef8ce3f2c81edbc9ade32c572e0f185261f94bb1`; any interface change stops dependent lanes until reconciled.

The interface comprises `ResolvedHeatmapStyle`, categorical axis IDs `x|y`, `HeatmapMappingInput`, `HeatmapAppearanceInput`, `HeatmapEditorState`, `HeatmapEditIntent` and pure resolver/translator/editor function signatures. Styles keep application captions/padding/background/tooltip, two category-axis appearances, color range, gradient legend and cell line/label options. Editor intents retain all four title captions. Only edited original leaves are returned as `eventOptions`; resolved defaults must not be written back to storage. Unknown and inactive-family options remain preserved.

## Bounded implementation lanes

Paths below are relative to `terminalpro/src/components/General/Table/Chart/` in the owned Workspace fork. New files must be registered in the maintained inventory before acceptance.

- HM2a: controller-owned `application/heatmapTypes.ts` plus a compile-only contract fixture. Pure declarations only; do not activate routes.
- HM2b: appearance/control worker owns new `application/heatmapAppearance.ts`, `heatmapEditor.ts`, `caller/heatmapThemePaint.ts`, `editor/heatmap/HeatmapCustomizeEditor.tsx` and `HeatmapAxisEditor.tsx`, with focused appearance/editor tests. It resolves layers, emits original saved leaves and reuses existing input panels. It does not edit the shared session, host or public router.
- HM2c: renderer worker owns new `echarts/heatmap.ts`, `heatmapCells.ts`, `heatmapAxes.ts`, `heatmapChrome.ts` and focused numeric/native-ECharts rendering tests. It consumes the frozen interface and HM1 matrix, with no reducer or editor writes. Labels, tooltips, legend and clipping belong to the renderer boundary.
- HM3: the controller joins existing unions, appearance dispatch, recapture, caller/editor selection and session routes once both lanes are accepted. Any cohesive extraction from a near-cap shared owner is designed before editing it.

Two implementation lanes may overlap only after HM2a and the semantic decisions they depend on are accepted. Do not create all listed files mechanically; keep each responsibility cohesive and split only where caps or ownership require it. Changes outside these paths require a reviewed boundary amendment.

## Acceptance gates

Each behavioral task retains meaningful RED/GREEN evidence, exact-file lint, baseline-relative typing and the existing inventory-backed size check: 400 physical lines/file, 300 logical units/file, 50/function. Reuse focused test helpers; one heavy suite/build runs at a time. Independent review verifies source and actual results before a per-task commit.

Native renderer checks cover signed/zero/constant values, duplicate row identity, finite palette interpolation, transparent missing borders, label fitting, tooltip identity, both categorical axes and gradient layout. Control tests verify saved leaf effects and preservation of unrelated options. Both owner-approved corrections require behavioral regression tests; approval is not test evidence.

Full Heatmap acceptance still requires the retained-FMP application journey, light/dark original comparison, visible control effects, refresh, fresh reopen and export in an identified image. Publish selected financial screenshots and rebuild release images only when that functional milestone is accepted. The current alpha remains unchanged.

## Accepted shared interfaces

HM2a is accepted at Workspace `216e8a296391e64f8e069602332caa09aafa9943`. The compile-only fixture covers both category axes, four title captions and readonly contracts. The declarations occupy 168 physical lines and emit no runtime code. [Independent verification](../../../artifacts/reviewed/chart-heatmap/renderer-types-review.md) records lint, baseline-relative typing, AST parity and inventory checks. The owner approved both behavior corrections; HM2b and HM2c may now proceed in parallel. Application integration remains open.
