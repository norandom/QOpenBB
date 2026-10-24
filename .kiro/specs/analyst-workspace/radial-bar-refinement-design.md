# Radial Bar appearance refinement design

Add category-boundary grids, source-default radial-line visibility, measured fixed-label circle fitting, and explicit native legend spacing. Preserve the frozen Column density/numerical-grid change. The owner requested this closer appearance on 2026-10-24. This is a proposed implementation contract; no Bar refinement has been implemented or verified. Source provenance and screenshot bounds are in ../../../artifacts/reviewed/chart-radial/bar-visual-analysis.md; those visual estimates are not acceptance tolerances.

## Ownership and exports

New production owner `echarts/radialBarLayout.ts` owns only rectangle fitting and fixed angular label alignment. Its exact public contract is:

```ts
export interface BarMeasuredAngularLabel {
  readonly value: number;
  readonly angle: number; // canvas radians from right, top=-pi/2
  readonly width: number;
  readonly height: number;
}
export interface BarMeasuredCategoryLabel {
  readonly value: string | number;
  readonly radiusFraction: number; // existing category-band center / R
  readonly width: number;
  readonly height: number;
}
export interface BarCircleFitInput {
  readonly rect: { readonly x: number; readonly y: number;
    readonly width: number; readonly height: number };
  readonly innerRadiusRatio: number;
  readonly angularOffset: number; // source-resolved default spacing5+tick6=11
  readonly angular: readonly BarMeasuredAngularLabel[];
  readonly category: readonly BarMeasuredCategoryLabel[];
}
export interface BarFittedAnchor {
  readonly value: string | number;
  readonly x: number;
  readonly y: number;
  readonly angle?: number; // angular orientation metadata only
  readonly align: "left" | "center" | "right";
  readonly verticalAlign: "top" | "middle" | "bottom";
}
export interface BarCircleFit {
  readonly center: readonly [number, number];
  readonly radius: number;
  readonly hole: number;
  readonly numericalLabels: readonly BarFittedAnchor[];
  readonly categoryLabels: readonly BarFittedAnchor[];
}
export function fitRadialBarCircle(input: BarCircleFitInput): BarCircleFit | null;
```

All arguments/results must be finite, dimensions nonnegative, ratio in [0,1], measured dimensions nonnegative. Reject malformed bounds; do not hide labels or emit nonfinite pixels. Helper consumes measured/formatted labels, and does not read application state, format values, calculate domains/ticks/groups, or mutate inputs. The fixed-label helper has no font dependency. The parent uses measureText(actual formatted string, actual resolved font), already implemented with ECharts graphic.Text.getBoundingRect. Domain/tick preparation remains in radialLayout/radialScale.

For fixed labels, let A/B be rect halfwidth/halfheight, c/s cosine/sine with near-zero values normalized at 1e-10, d angularOffset. Start R=min(A,B). For each nonzero c bound R by (A-W)/abs(c)-d; at c=0 require W/2<=A. For each nonzero s bound R by (B-H)/abs(s)-d; at s=0 require H/2<=B. Clamp R to >=0 after intersecting bounds. If even R=0 with offset/text cannot fit, return null. The caller then preserves the existing layout path; large labels or a valid narrow viewport must not newly turn the entire chart into an invalid result. Do not claim that fallback labels are in bounds. Angular anchors are ((R+d)c,(R+d)s); alignment left/right/center by sign(c), baseline top/bottom/middle by sign(s). Exact vertical/horizontal directions use their centered coordinate axis. Center remains rect center. H=R*ratio.

Category labels use current source-matched top-ray anchor x=-10, y=-radiusFraction*R, align=right, verticalAlign=middle. Check their actual boxes too: horizontal constraint width+10<=A; vertical constraint radiusFraction*R+height/2<=B. Reduce R when needed; return null for physically impossible label widths and preserve the existing layout fallback without silently hiding labels. This is a bounded fixed-label approximation, not AG's full collision/minimum-radius solver. For saved Parallel/Perpendicular orientations, retain the existing geometry/anchor path in this slice. State that scope explicitly in evidence; no implicit orientation migration.

## Exact shared edits

- `compatibility/radialContracts.ts`: retain numericalGrid unchanged. Add optional categoryGrid using the same readonly enabled/width/styles shape. Add optional lineEnabled on ResolvedRadialAxisPaint; undefined for direct old renderer callers means enabled, preserving old calls. No new controls or persistence fields. Angular offset may be fixed source-default11 in the numerical lane because label.spacing/tick.size are outside the current public style; do not promise newly supported saved spacing/tick edits.
- `application/radialAppearance.ts`: defaults explicitly resolve line.enabled=true for Column axes and Bar angle-number, false for Bar radius-category; project bool into lineEnabled. Bar radius-category defaults enabled grid,width1,applicationColors(tokens).grid,solid dash. Generalize local grid-style resolver and premerge style guard by axis key without changing Column precedence/empty-array/partial-entry semantics. Only Column emits numericalGrid; only Bar emits categoryGrid. Malformed styles reject through existing selection envelope.
- `echarts/radialModel.ts`: add categoryGridRadii readonly array, empty for Column; keep numericalGridRadii. Add optional align/verticalAlign to RadialAxisAnchor, default paint center/middle for existing Column/other anchors. Do not change stable IDs, raw values, mark geometry contracts or existing model center ownership.
- `echarts/radialScale.ts`: add pure categoryGridRadii(R,H,count,paddingInner,paddingOuter) helper beside bands. For N=0 return []; N=1 return [H]. Otherwise use the same signed [R,H] band step/inset/bandwidth as marks. Emit source reverse-tick order: for k=0..N-1, radius is H if k=0, otherwise inset+step*(k-.5)+bandwidth/2. At default N=4 the style-order array is [H,.8R,.6R,.4R], NOT sorted ascending. Group padding does not enter this formula.
- `echarts/radialLayout.ts`: retain current Column branch byte-for-byte where possible. For Bar fixed labels, prepare the existing domain/ticks first (Bar density is independent of R), format/measure labels, compute category radius fractions with existing bands, then call fitRadialBarCircle on the padded rectangle. Reuse returned geometry for every mark/grid/label. Bar nonfixed orientation keeps old path. Emit category grids from the pure scale helper and leave numericalGridRadii empty. Filter axisStrokes by resolved lineEnabled!==false so the default Bar category ray disappears while explicit enabled=true restores it. Extract cohesive rectangle preparation or Bar-specific anchor construction into the new helper if radialLayout reaches400 physical lines; do not compress statements.
- `echarts/radialChrome.ts`: paint categoryGrid/categoryGridRadii analogously to frozen Column grids, preserving their order/style cycling below series. Labels consume optional alignment/baseline. Make Bar legend mapping explicit: icon=rect, native marker dimensions, itemGap=horizontalSpacing (horizontal) or verticalSpacing (vertical), remove horizontalSpacing from text padding. Keep native legend IDs/formatter/click selection. Column legend is unchanged.

## Legend marker gap and reservation

Fresh ECharts source read: installed LegendView.js line319 sets textX=itemWidth+5 for left-aligned items (or -5 for right); the native gap is5. The plain label's old padding translation is insufficiently proven by the retained screenshot. Default marker.padding5 therefore needs no adjustment. Use plain textStyle.padding=[0,0,0,itemSpacing-5] for Bar and explicitly align legend items left. This preserves literal displayed braces/pipes without introducing rich-text syntax. Fresh labelStyle.js lines440-447 forwards padding unless disableBox; LegendView calls createTextStyle without disableBox. Keep itemGap independent and remove all previous right/vertical outer text padding. Test actual visual marker-to-text origins at itemSpacing0,5,13; if the installed renderer clamps negative plain padding or otherwise fails this mapping, stop for a reviewed adjustment rather than claiming option-level spacing. No rich formatter is necessary in the proposed path.

Painting and fit reservation must use the same resulting item bounds. For the default one-row horizontal legend: item width=markerSize+itemSpacing+actualTextWidth; total width=sum(item widths)+(N-1)*horizontalSpacing, height=max(markerSize,actualTextHeight). Reserve height+legend.spacing; no trailing item padding. For vertical legend reserve max(item widths)+legend.spacing and use verticalSpacing only between entries. Keep existing reservation for wrapping/scroll cases unless its complete measured geometry is implemented. The fitting rectangle starts after actual captions/outer padding/legend reservation; no hard-coded radius increment. A shared Bar-only helper for legend extent can live in new radialBarLayout.ts and accept measured item widths/heights plus orientation/gaps, keeping paint and preparation consistent.

## Checks before acceptance

Extend existing radialNumerical, radialEngine and radialSession tests; no test-only production bypass. Add pure helper tests to radialNumerical to keep ownership small. Required cases: category circles N0/1/4, nondefault category padding, unchanged boundaries under group padding; default Bar category line disabled and explicit restoration; category-grid dark/custom/saved/disabled/malformed paint with style cycling in source order; exact retained Bar domain/ticks and raw eight financial amounts unchanged; Column corrected80B/20B fixtures and numerical grids unchanged.

For fit tests use actual text boxes at default/narrow/large-font viewports, verify computed aligned boxes within rectangle, finite geometry and impossible-label null/fallback behavior. Demonstrate increased default Bar radius relative to old conservative geometry without requiring one screenshot-specific radius. Verify nonfixed fallback unchanged. For legend use actual ECharts rendered marker/text bounds: default item gap32, nondefault gap17, marker gap5/default and13/custom (plus0 boundary), selections and IDs unchanged. Literal brace/pipe labels must survive. Options alone cannot establish visual gap.

All new/changed production files must pass400 physical lines,300 logical units,50/function; parent adds the new owned file to the inventory/explicit fork scope. One heavy verification process at a time. Independent review must precede commit/rebuild, followed by identified packaged Column and Bar journeys plus representative screenshot comparison. Deadline may permit source acceptance only; report runtime evidence pending rather than reuse the pre-change image passes.
## Review handoff constraints

Compute category radius fractions from normalized bands, never by dividing an existing pixel center by a possibly zero radius. Handle zero-size rectangles and zero radius explicitly with finite results or the documented existing-layout fallback. A failed actual ECharts marker-padding check is a stop condition for that mapping; do not substitute an untested visual adjustment. See the [independent design review](../../../artifacts/reviewed/chart-radial/bar-refinement-design-review.md). These are implementation constraints, not executed evidence.

The same new helper owner may export a separate prepareBarLayout adapter with readonly mapping input, prepared data, geometry, domain tuple, ticks and available rectangle. It formats/measures already prepared labels and delegates to fitRadialBarCircle; it must not recompute domain/ticks/groups or import radialLayout. The numerical owner chooses the existing fallback on null. This keeps the core fitter formatting-free and prevents a reverse dependency.
