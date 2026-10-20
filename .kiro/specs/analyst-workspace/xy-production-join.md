# Scatter and bubble production join

Make the gallery's scatter and bubble choices usable in the existing Table/File chart journey. Use the accepted inactive mapper at Workspace `7e509d3`, specifically `echarts/xyTypes.ts`, and the existing widget session and editor dock. Completion means the user can configure, refresh, save, reopen and export these charts in both themes. More inactive helper acceptance alone does not complete this slice.

This X3/X4 implementation contract was independently reviewed and approved on 2026-10-20 against the current mapper, session, setup, editor and caller interfaces. [Source research](xy-chart-research.md) owns parity evidence; [X2 design](xy-mapper-design.md) explains numerical mapping. Paths below are relative to `vendor/workspace/terminalpro/src/components/General/Table/Chart/`.

## One cohesive join

Use one bounded implementer for this join. Session dispatch, ready-state unions, setup policy, caller defaults and editor routing touch shared contracts; their current seams do not justify two simultaneous writable lanes. Split work into cohesive `application/xy*.ts`, `editor/xy/*` and numeric navigator modules inside the same assignment. The controller owns final integration review and release verification.

Extend `ApplicationChartFamily` with `XyChartType` and add an explicit `isXyChartFamily` guard. Extend the ready-state union with `kind: "xy"` and XY-specific editor data; do not make a Cartesian appearance pretend to be XY. Reuse the common ready fields (stamp, options, revision, model, snapshot, legend scope/projection and setup props), but allow the XY branch its own editor projection type where the current Cartesian editor contract cannot represent it.

Use these minimal transient contracts:

```ts
type XyValueRole = "x" | "y" | "size";
interface XyEditorProjection {
  readonly chartType: XyChartType;
  readonly paired: boolean;
  readonly roles: readonly { readonly colId: string; readonly role: XyValueRole }[];
  readonly labels: "category" | "y";
  readonly style: ResolvedXyStyle;
}
type XyEditIntent =
  | { readonly panel: "xy"; readonly edit: { readonly kind: "paired"; readonly value: boolean } }
  | { readonly panel: "xy"; readonly edit:
      | { readonly kind: "shape"; readonly value: string }
      | { readonly kind: "size" | "maxSize" | "strokeWidth"; readonly value: number } };
interface XyEditCommand {
  readonly stamp: SessionStamp;
  readonly family: XyChartType;
  readonly intent: XyEditIntent;
}
```

Add this intent to the existing `ApplicationChartCommand`; route it through `executeApplicationChartCommand`. It is not another dispatcher or store. Existing common caption, legend, padding, background, tooltip, labels and axis commands remain in the same transaction path, with XY-specific bindings where needed. Numeric axis targeting uses explicit `"x" | "y"` direction plus option type `"number"`; retain both concrete axes' option siblings when editing a finite leaf. Do not reuse semantic category-axis type transitions for numeric X.

## Projection and persistence

The XY selection pipeline is: latest baseline and range, retained capture, setup projection, X1 assignments, resolved XY appearance, `translateXy`, navigator decoration, ready-state editor projection. `context.labels` is `"category"` only for a real Labels selection; `DEFAULT_SETUP_CATEGORY` means `"y"`. Retain original snapshot identity and aggregation provenance. Pairing is derived from the active family option, defaults true and never persists an assignment array.

Paired-mode edits write `chartOptions[family].paired`. Shape/size/maxSize/strokeWidth edits write `chartOptions[family].series[field]`, preserving the original top-level XY paths. They must not write Cartesian `series.marker.*`. `maxSize` is a bubble control; a stale scatter maxSize command is rejected. The renderer consumes top-level XY stroke width as `ResolvedXyStyle.series.markers.strokeWidth`; ordinary `series.strokeWidth` is not an alternate drawing authority.

Use the existing validated option baseline/reducer and exact latest-state stamp checks. Do not replace saved state with effective appearance. Preserve unknown options, inactive family branches and inactive marker fields. Family switching retains scatter and bubble pairing separately. Pairing and appearance edits advance render revision; category/range/data changes use the existing recapture and data revision rules. Changing Labels must recapture before projection. Commands captured before refresh, reorder, family change or widget replacement must not commit against a newer session.

Resolve appearance in explicit low-to-high layers: XY stock defaults, selected theme common, selected theme active family, composed caller/saved common, composed caller/saved active family. Reuse `composeAppearanceOptions` semantics: it validates detached copies, replaces saved common with generated common, and merges generated options with the selected saved baseline. Do not introduce a different saved-common precedence. Add scatter/bubble awareness where theme normalization currently visits only bar/line; do not feed XY into `appearanceLayers`, whose fallback is bar.

Resolve numeric X and Y explicitly, including finite optional bounds, positional title overrides, fonts, tick/grid settings and point-label settings. Shared number-axis options apply to both axes; concrete bottom/left options override their own axis. Preserve custom orientation titles; apply original caller-generated scatter title defaults only under the source range-size rule. Reuse X2's explicit palette/background/caption and marker override precedence. Default circle/7, bubble maxSize 30, fill opacity 0.8, stroke width 1 and disabled labels must remain effective unless the appropriate layer overrides them.

## Setup and controls

Keep the existing add/remove/reorder controls, Labels selector and Aggregate control. Show headings **Labels** and **X Y Values**, plus **Paired Mode**. Derive role annotations from the selected order and pairing, including incomplete trailing groups: paired scatter alternates X/Y; paired bubble cycles X/Y/size; unpaired uses first X followed by Y or Y/size. Roles are presentation only; X1 remains the assignment authority.

Introduce an explicit `xy-coordinates` policy in setup projection. It forbids Switch Category / Series, preserves each column's declared unit/scale, and removes the ordinary single-axis requirement that all selected columns share units. USD X/Y and USD/share size are valid. Do not apply the single-axis unit gate to X/Y/size together, infer conversion factors, or rescale raw observations. Original XY permits multiple coordinate series with different descriptors; retain their identities and tooltip labels without inventing a common unit title.

Aggregation remains available only with a real Labels category, with existing sum/first/last/min/max/count/avg behavior. Aggregate all selected numeric columns independently before assigning X/Y/size; never sum across different columns. Counts use existing observation-count descriptors and neutral number formatting for coordinates, size, labels and tooltips. Always project from the retained flat capture so repeated edits cannot aggregate an aggregate.

Zero selected numeric columns must be accepted by the XY setup path; existing `selectedColumns` rejects an empty list and must be narrowly adjusted for this policy. Empty/incomplete selections remain editable and show **No data available to be charted.**, rather than waiting forever or substituting points. Scatter requires two fields and bubble three. Retain incomplete selected fields and their annotations.

Customize exposes point tooltips, shape, size and stroke width, plus labels; bubble exposes Min Size and Max Size. Reuse the established controls and seven shape choices through XY bindings. Shared title/legend/background/padding/axis/navigation controls remain available. Do not expose line interpolation/connection controls or Switch Category / Series for XY; their saved values remain untouched.

## Caller, host and navigator join

Add XY to the ordinary caller admission/gallery gates, session projection/family transitions and dock editor mode. Update `caller/generatedOptions.ts`, theme normalization and any caller-family guard that currently recognizes only Cartesian/combo. Generate scatter/bubble series and numeric-axis options directly. Existing display callbacks remain outside persisted options. Table and File use the same session; standalone and AI callers retain their existing scope.

Use numeric X for main and overview axes. Navigator/mini-chart flags remain false by default and mutually exclusive; either enables navigation. Build the overview from full data and retain the same per-series bubble size domains, including sizes on missing-coordinate rows. Legend filtering and navigator windows must not renormalize bubble diameters or turn numeric X into row indexes.

Normalize the navigator range against the actual numeric X domain. Preserve minimum-visible-items 4, Y autoscale to the selected X window, wheel zoom, pan and double-click/reset behavior. Resolve those interactions through the existing host lifecycle with an explicit XY branch; do not replace previous-family interaction behavior. Reset restores the full numeric window. All-equal X, empty data and windows containing no points need finite empty/single-domain behavior and bounded event handling.

Before activation, replace X2's one-sided out-of-data bound diagnostic with the original empty-domain result. If supplied minimum exceeds observed maximum, or supplied maximum is below observed minimum, the affected axis and point geometry are empty; never reverse the extent or expand it with invented observations. `normalisedExtentWithMetadata` at retained Charts 30524-30543 establishes this rule. Keep the editor and original data available so changing the bound restores the chart.

Refresh must rebuild from current captured rows and retain valid saved options; save/reopen must restore family, pairing, field order, category, aggregate and appearance. Export uses the existing host's current visible chart, including numeric coordinates and configured point geometry. Existing transaction failure/diagnostic behavior remains observable.

## Acceptance and scope limits

Use the captured AAPL FMP CSV and provenance in `artifacts/chart-combo/fmp/`, without another provider request. Exercise revenue X, net income Y and EPS size, with fiscal period labels. Verify plotted raw coordinates, linear diameters, formatted tooltip values/units, both themes, controls, navigator interactions, refresh, save/reopen and export through the application. Add synthetic journey cases for pairing/reorder/incomplete groups, aggregation, missing coordinates/sizes, negative/equal sizes and empty-bound restoration.

Run focused transaction/editor tests and bounded mapper/host regressions, then isolated background Playwright at one worker. Prior Cartesian and combination journeys must still pass; no previous UI feature may be reduced to make XY pass. Record actual test evidence in breadth and the milestone record. After independent review and fresh acceptance, make the bounded commit and completed-milestone image release under the existing Dagger/publication policy.

All new or modified production files must satisfy whole-file caps of 400 physical lines, 300 logical units and 50 units per function. Inspect shared-file baselines before edits: session dispatch/projection unions, setup projection, editor assembly and host lifecycle are integration points, not permission to grow oversized files. Extract cohesive responsibilities into the owned XY modules first. Any unavoidable oversized shared file needs a narrowly documented measured design exception approved by the controller/reviewer; no implicit grandfathering or arbitrary forwarding extraction. Extend the maintained inventory and run its explicit fork-scope gate. This design creates no exception and authorizes no unrelated refactor.
