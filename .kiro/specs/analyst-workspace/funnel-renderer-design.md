# F2 renderer and controls interface proposal

Freeze one resolved appearance and render input, then implement custom shapes and controls in disjoint lanes. Reuse the current chart session, option reducer and ECharts host. Independent interface review approved this bounded inactive design on 2026-10-26. It introduces no UI feature delta beyond the approved [Funnel contract](funnel-contract.md). It preserves the exact [F1 data interface](funnel-data-design.md); neither F2 lane may change it.

## Minimal shared interface

Parent owns new `application/funnelRenderTypes.ts` before dispatch. Existing names imported below are actual project types: `ResolvedApplicationAppearance`, `ResolvedApplicationSeries` from `appearanceModel.ts`, `ChartDisplayPolicy` from `types.ts`, `ChartShadowState` from the existing Shadow panel and `FunnelMagnitudeData | PyramidData` from F1 contracts. Public render declarations:

```ts
type FunnelFont = ResolvedApplicationSeries["labels"];
type FunnelNumericLabel = FunnelFont & Readonly<{
  placement: "center" | "before" | "after";
  spacing: number;
}>;
type FunnelStageLabel = FunnelFont & Readonly<{
  placement: "before" | "after";
  spacing: number;
}>;
interface FunnelStroke {
  readonly strokeWidth: number;
  readonly strokeOpacity: number;
  readonly fillOpacity: number;
  readonly lineDash: readonly number[];
}
interface FunnelCommonStyle {
  readonly application: Readonly<Pick<ResolvedApplicationAppearance,
    "title" | "subtitle" | "padding" | "background" | "tooltip" | "palette">>;
  readonly direction: "vertical" | "horizontal";
  readonly label: FunnelNumericLabel;
  readonly stageLabel: FunnelStageLabel;
  readonly series: FunnelStroke;
  readonly paint: FunnelThemePaint;
  readonly seriesAreaPadding: Readonly<{
    top: number; right: number; bottom: number; left: number;
  }>;
}
type ResolvedFunnelStyle = FunnelCommonStyle & (
  | { readonly family: "funnel";
      readonly shadow: Readonly<ChartShadowState>;
      readonly dropOff: FunnelStroke & { readonly enabled: boolean;
        readonly fill: string; readonly stroke: string };
      readonly spacingRatio: number }
  | { readonly family: "coneFunnel" }
  | { readonly family: "pyramid";
      readonly shadow: Readonly<ChartShadowState>;
      readonly reverse: boolean; readonly spacing: number;
      readonly aspectRatio?: number }
);
interface FunnelRenderInput {
  readonly data: FunnelMagnitudeData | PyramidData;
  readonly style: ResolvedFunnelStyle;
  readonly context: Readonly<{
    display: ChartDisplayPolicy;
    viewport: Readonly<{ width: number; height: number }>;
  }>;
}
function translateFunnel(input: FunnelRenderInput): CartesianTranslationResult;
```

`CartesianTranslationResult` is the existing supported/unsupported/invalid ECharts-options result from `echarts/cartesianTypes.ts`; reuse its envelope without importing Cartesian axis semantics. Enforce data/style/paint family equality and finite resolved dimensions before producing options. F1 empty/invalid results are handled by the session before calling the renderer; no data re-admission or normalization in F2. `spacingRatio`, Pyramid spacing/aspect/reverse are effective native geometry settings, not new editor controls. Resolve stock defaults from retained themes; do not invent UI settings for them. Theme paint arrays must be nonempty, validated CSS colors. Stage paints use the explicit effective variant `paint` arrays, not application.palette. The appearance resolver applies saved native `series.fills` and `series.strokes` over caller theme-paint defaults through the existing composition precedence, validating the resulting arrays; caller theme defaults must never overwrite an explicit saved palette. Font retains native weight and style separately from the menu's combined weight key.

Keep geometry positions in viewport pixels and preserve F1 stage.index/rowId association in custom-series data. Each shape hit/tooltip must map to a real value stage; missing stages emit no numeric label, shape or fabricated tooltip. Connector shape belongs to its preceding value stage and exists only for adjacent present endpoints. For Funnel/Cone, keep visual connectors silent: their drawing identity does not override native category-aligned picking. Transparent per-stage axial nearest-neighbor strips provide tooltip hit areas, including zero and terminal cross-sections, without visible fabricated bars. Compute strip boundaries from all original stage positions, omit missing-stage strips without bridging gaps, clip to the plot and resolve midpoint ties deterministically. This clarification does not change Pyramid picking. Numeric formatting receives signed `value`, never magnitude/ratio. Stage labels use category formatting independently of numeric labels. Genuine zero may have degenerate geometry while its stage label remains; do not inflate zero into a positive-value bar. No axes, legend, navigator, miniature or crosshair interfaces are added.

## Appearance and edit boundary

Controls lane owns new `application/funnelAppearanceTypes.ts` (input aliases) and `application/funnelEditorTypes.ts` (panel state/intents). Appearance input follows the actual Heatmap pattern: `{ baseline: OptionBaseline; generated: RuntimeOptions; theme: ApplicationThemeInput; themePaint: FunnelThemePaint; precision: number }`. Caller-supplied `themePaint` is mandatory: existing ApplicationThemeInput does not retain the native secondSequentialColors/custom-palette distinction. Avoid embedding engine or runtime instances. `resolveFunnelAppearance(input, family): ValidationResult<ResolvedFunnelStyle>` uses existing `composeAppearanceOptions` precedence and native-family baseline selection; do not write effective defaults back to storage.

Parent freezes this exact data-only paint contract in the shared render-types file:

```ts
interface FunnelThemePaint {
  readonly family: FunnelFamily;
  readonly fills: readonly string[];
  readonly strokes: readonly string[];
  readonly numericLabelColor: string;
  readonly stageLabelColor: string;
  readonly dropOffFill: string;
  readonly dropOffStroke: string;
}
```

`caller/funnelThemePaint.ts` is parent-owned F3 integration, not renderer work. It resolves selected native palette before generic ApplicationThemeInput discards its provenance: Funnel uses the single native fill/stroke; Cone uses inbuilt secondSequentialColors for both arrays, or the evaluated native SAFE_RANGE2_OPERATION result for custom palettes; Pyramid uses the complete native fills/strokes arrays. Native numeric label color is chartBackgroundColor for Funnel/Pyramid and textColor for Cone; stage-label color is textColor. Drop-off paints come from resolved native dropOff defaults/fallback paint, even when not applicable to the variant. All values are validated CSS strings and arrays are nonempty. Do not substitute generic palette fills for Cone or interpolate a new custom range in the renderer. Native derivation sources: Enterprise `FUNNEL_SERIES_THEME` at 27985, `CONE_FUNNEL_SERIES_THEME` at 28982 and `PYRAMID_SERIES_THEME` at 36873. Caller helper must receive/evaluate the actual selected native palette result, including SAFE_RANGE2_OPERATION, rather than guessing it from theme name. F2 contract tests supply explicit paint fixtures; F3 verifies the actual caller derivation for stock/custom themes.

Minimal public controls functions:

```ts
function projectFunnelEditorState(style: ResolvedFunnelStyle): FunnelEditorState;
function mapFunnelEditorIntent(
  style: ResolvedFunnelStyle, intent: FunnelEditIntent,
): ValidationResult<{ readonly eventOptions: RuntimeOptions }>;
```

`FunnelEditorState` contains only kind/family, existing padding/background/tooltips panel states, Titles state with availableCaptions restricted to title/subtitle, Series style controls, separate labels/stageLabels font panel states, direction, optional dropOff and optional shadow states by family capability. Build state from resolved style, not a second default model.

`FunnelEditIntent` reuses existing `ApplicationEditorIntent` variants for padding, background, tooltips, series, shadow and labels; restrict Titles edit caption to title/subtitle. Add `{panel:"stageLabels", edit: ChartLabelsEdit}`, `{panel:"funnelDirection", value:"vertical"|"horizontal"}` and `{panel:"funnelDropOff", edit: {field:"enabled",value:boolean} | {field:SeriesStyleField,value:number}}`. Reject capability-ineligible shadow/dropOff intents at runtime even if dispatched with a forged type. Reuse existing validators and `fontLeaf` to preserve weight/style. Reject nonfinite numbers, negative widths/dashes/font sizes and opacity outside [0,1]; validate paints. Retain saved dash arrays when untouched; a scalar slider edit follows the existing native-compatible one-element dash convention rather than flattening arrays on load.

Map each intent to an inner native patch, then explicitly scope it: `eventOptions = { [nativeFunnelType(style.family)]: patch }`, exactly as `mapHeatmapEditorIntent` returns `{heatmap: patch(...)}` in `application/heatmapEditor.ts`. Existing reducer only merges options; it does not add a family scope. Inner common patches remain `{padding:{[side]:value}}`, `{background:{[field]:value}}`, `{title:fontLeaf(...)}` or `{subtitle:fontLeaf(...)}`. Tooltip is `{tooltip:{[field]:value}}`; series style/direction/font/dropOff/shadow patches use `{series:{...}}` with native keys. Thus a Cone direction edit is `{"cone-funnel":{series:{direction:"horizontal"}}}` and a Pyramid title edit is `{pyramid:{title:{text:"..."}}}`. Never write unscoped root `series` or guess that camelCase `coneFunnel` is the saved option scope. Pass this explicit envelope to existing `reduceSessionOptions`; preserve unrelated/family options. Session stamp validation stays outside these pure mapping functions. Direction edits affect geometry and do not transpose saved capture or switch categories/series.

## Label layout and clipping ownership

Resolve numeric placement/spacing defaults to Funnel center/0, Cone before/4, Pyramid center/0. Cone numeric before/after offsets follow the stage progression axis: above/below in Vertical and left/right in Horizontal. Pyramid stage labels default before/12. Funnel/Cone stage placement defaults before for vertical (left) and after for horizontal (bottom), matching native axis selection at Enterprise 27941-27983; resolve their effective category-label padding into stageLabel.spacing using native axis/theme defaults rather than importing a visible Axis control. Saved explicit stageLabel.placement wins for each variant. For Funnel/Cone, native `series.stageLabel.padding` overrides the category-axis padding default and maps to resolved stageLabel.spacing (Enterprise 27935). For Pyramid, native `series.stageLabel.spacing` overrides its default 12 and maps to resolved stageLabel.spacing (Enterprise 36150 and 36873). Do not read Pyramid spacing from padding or persist an axis-backed Funnel padding edit as spacing. Source-backed Cone extra seriesArea padding is top/bottom20, left/right0; other variants inherit the effective native seriesArea padding. Pyramid interstage spacing is 2; Funnel spacingRatio is .25. These are resolved layout settings with no new UI controls. The controls lane resolves saved/theme inputs; geometry lane owns measurement, available label space and clipping.

Geometry computes a content rectangle after common background/title/subtitle/padding chrome using existing title/chrome layout helpers. Reserve stage-label area on the resolved before/after side using measured text extent plus stageLabel.spacing; reserve Cone numeric-label before/after spacing independently. Never reserve numeric-label space when disabled or for a missing value. The remaining nonnegative rectangle is the shape plot; if no positive shape area remains, emit no nonfinite/negative-size shape and return a supported blank plot while the common chrome/controls remain available. Stage labels are clipped to their reserved available area and value labels to the available plot/label area; long text must not expand outside the chart viewport. Measure with the ECharts/zrender text facilities already available to custom rendering, not CSS character-count guesses. Use the same font family/weight/style/size for measurement and drawing. Pure geometry output retains separate plot, stageLabelArea and numericLabelArea rectangles so tests can inspect bounds; these are geometry-lane internal types, not another lifecycle state. Defaults and measured extents must be verified for both directions at the first join; no area can change F1 normalized values.

## Source keys and panels

All project paths below start at `vendor/workspace/terminalpro/src/components/General/Table/Chart/`. Installed native source is AG Grid Enterprise 34.1.1 `/home/mc/.bun/install/cache/ag-grid-enterprise@34.1.1@@@1/dist/package/main.esm.mjs`.

| Visible control | Native option key | Reuse and source |
| --- | --- | --- |
| Chart Style | root `padding.{top,right,bottom,left}`, `background.{visible,fill}` | `ChartPaddingPanel`, `ChartBackgroundPanel`; composition exemplar `editor/heatmap/HeatmapCustomizeEditor.tsx:25-36`, mapping `application/heatmapEditor.ts` commonPatch. Native runtime confirms Chart Style section; detailed cosmetics effects remain acceptance work. |
| Titles | root `title`, `subtitle`: enabled/text/fontFamily/fontSize/fontWeight/fontStyle/color/spacing | `ChartTitlesPanel` and `CaptionFields`, pass `availableCaptions:["title","subtitle"]`; no axis titles. Exact native allowed properties follow existing `fontLeaf`/chrome resolution. |
| Tooltips | effective root `tooltip.enabled` resolved from native series tooltip scope | `ChartTooltipsPanel`; existing `heatmapEditor.ts` commonPatch maps tooltip leaves through current reducer. All three native series list tooltips at installed lines 49634-49636. Verify saved family scope at join rather than creating a new JSON schema. |
| Stroke Width, Line Dash, Stroke Opacity, Fill Opacity | `series.strokeWidth`, `series.lineDash`, `series.strokeOpacity`, `series.fillOpacity` | `ChartSeriesStylePanel.tsx:7-20`; native mapping 49634-49636 and opacity slider 49739-49743. No added fill/stroke color UI: palette/theme owns normal stage paints. |
| Labels | `series.label.{enabled,fontFamily,fontSize,fontWeight,fontStyle,color}` | `ChartLabelsPanel`; native initLabels 49770 onward. Signed numeric values through display.seriesLabel. |
| Stage Labels | `series.stageLabel` with separate enabled/font fields | Reuse `ChartLabelsPanel` with `label="Stage Labels"`; separate state/edit mapping, not a new font widget. Native initStageLabels 49815-49817. |
| Drop-Off, Funnel only | `series.dropOff.{enabled,strokeWidth,lineDash,strokeOpacity,fillOpacity}` | Small toggle wrapper plus `ChartSeriesStylePanel`; native initDropOff 49745-49765. Fill/stroke paints are resolved retained theme settings, not new color controls. |
| Shadow, Funnel/Pyramid | `series.shadow.{enabled,color,blur,xOffset,yOffset}` | Existing `ChartShadowPanel.tsx:7-22`; native capability list 49634-49636. Cone has no shadow controls or applied shadow. |
| Direction | `series.direction` | Existing Vertical/Horizontal choice inputs; native assessment records effects, source geometry confirms axis orientation. No category transpose. |

The existing `ChartBackgroundState` uses `visible` and `fill` directly (`ChartBackgroundPanel.tsx:6-12`). `ChartTooltipsState` also retains `mode`; preserve its resolved/saved value through existing tooltip mapping and expose only modes already supported by the native/common control contract. Numeric typography uses existing native `fontFamily/fontSize` leaves while editor state uses `font/size` aliases. Full arrays, saved typography and unsupported unrelated options remain preserved by baseline/reducer composition.

Retained native characterization is [native assessment](../../../artifacts/reviewed/chart-funnel/native-assessment.md). Its observed common sections are Chart Style, Titles, Series; axes/legend/navigator were absent. Native options equality after reload did not prove Cone/Pyramid numeric labels remained visible. Candidate join must test label effects and visual persistence rather than copying that loss.

## Disjoint lanes and first join

After parent freezes this interface and F1 is independently accepted:

- Geometry owns new `echarts/funnel.ts`, `funnelGeometry.ts`, `funnelSeries.ts`, `funnelLabels.ts`, `funnelTooltip.ts` and geometry/renderer tests. It consumes only F1 output plus resolved style/context. It must not edit application/editor/shared host files or F1 contracts.
- Controls owns new `application/funnelAppearance.ts`, `funnelAppearanceTypes.ts`, `funnelEditor.ts`, `funnelEditorTypes.ts`, `editor/funnel/FunnelCustomizeEditor.tsx`, `editor/funnel/FunnelDropOffPanel.tsx` and their tests. Reuse existing panels directly; no new stage-label panel is needed. It must not edit geometry, F1 contracts or shared routing.
- Parent owns render contract file, `caller/funnelThemePaint.ts` and actual family session selection/projection/transaction wiring, caller theme routing, setup mode, ready/intent unions, `LiveChartEditor`, `AgChartView`, inventory and breadth. Those shared changes belong to F3. No lane edits `echarts/lifecycle.ts` (394 lines) or creates another lifecycle.

First join is an inactive contract test (before full application routing): actual ordinary `SetupProjection` -> accepted F1 adapter -> resolved appearance -> translateFunnel, then map an editor intent through the existing option reducer and re-resolve/retranslate. Assert numeric-label and stage-label toggles act independently; horizontal geometry changes orientation; Funnel dropOff toggle removes only connectors; Cone rejects shadow/dropOff; Pyramid uses F1 axial ranges. Include signed values and missing middle stage; tooltip raw value/row identity must survive changes, and missing endpoints must not bridge. This test proposal has not run. Browser visible effects, themes, fresh save/reopen, resize and export remain F4 acceptance.

All new/modified maintained files require 400 physical/300 logical units per file and 50 per function under the current inventory gate. Modules above are responsibility boundaries, not a requirement to create unnecessary files. Parent serializes shared joins, independent review and the heavy test/build queue. No implementation, runtime or tests were executed for this proposal.

## Dependency boundary

F3 must derive equivalent stock/custom paint data from owned theme inputs and compatible pure logic; it must not import commercial AG Charts runtime packages or its evaluator. The native operation names above describe observed palette semantics, not a required dependency. Inactive F2 joins use explicit paint fixtures. Actual caller derivation and stock/custom equivalence remain a separate F3 prerequisite.
