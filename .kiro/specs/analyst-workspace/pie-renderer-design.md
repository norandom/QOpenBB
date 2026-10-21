# Pie and donut renderer design

The independently reviewed P2 mapper accepts resolved snapshots, P1 assignments and effective appearance; it does not activate a chart, edit saved state or add a control. P3 owns the application join. Independent Astra review approved this design and its inactive implementation on 2026-10-21. Browser acceptance remains open; the verification record below identifies the accepted source and checks.

The source baseline is Workspace `38dffc33389aca0e4a87e0e88d42f7067aa220df`, Grid 34.1.1 and Charts 12.1.1. The local probe exercises original data processing, node creation and legend dispatch; it confirms the observation, radius and legend rules below without claiming browser parity. Raw research remains in ignored `artifacts/chart-pie/p2-contract/`; accepted implementation evidence will be summarized in the [verification record](../../../artifacts/reviewed/chart-pie/verification.md).

## Ownership and interface

All production paths below are relative to `vendor/workspace/terminalpro/src/components/General/Table/Chart/`. One implementer owns the six new `echarts/` modules and focused tests. The parent owns inventories, maintained specifications, evidence, review and commit. Every maintained production file must pass 400 physical lines, 300 logical syntax units and 50 units per function; splitting responsibilities below is part of acceptance.

| File | Responsibility |
| --- | --- |
| `echarts/pieTypes.ts` | Resolved input and internal datum/ring contracts |
| `echarts/pieAdmission.ts` | Snapshot/assignment/appearance/context validation; no partial options |
| `echarts/pieData.ts` | Optional existing aggregation, ring-local raw observations, unique legend keys, positive fractions |
| `echarts/pieLayout.ts` | Polar content rectangle, captions/legend, common radius, ring radii, zero-total outlines |
| `echarts/pieSeries.ts` | Native sectors, independent callout/sector labels, tooltip and paint |
| `echarts/pie.ts` | Small admission/projection/composition entry point |

No shared chrome extraction is proposed for this slice. Reuse public `fontStyle` and `escapeHtml` from `cartesianDisplay`, `measureText` from `cartesianLayout`, `xyApplicationDiagnostics` for common appearance, and `aggregateSetupRows` for the established configured aggregation. Importing these primitives does not create Cartesian axes. The polar layout composes caption/background options directly from the same resolved fields. Do not call `applicationLayout` with a fake bar family or manufacture axis appearance.

The only proposed existing production edits are `compatibility/snapshotTypes.ts` and `compatibility/snapshot.ts`: introduce `"pie-observations"` as an explicit policy allowing an empty selected-numeric list, exactly like the existing family policies. Other snapshot validation remains unchanged. This avoids treating a valid empty selection as an error or naming polar input `"xy-coordinates"`.

```ts
type PieAssignments = Extract<PieAssignmentResult, { status: "resolved" }>;
type PieFont = Pick<ResolvedApplicationSeries["labels"],
  "enabled" | "font" | "size" | "color" | "weight" | "fontWeight" | "fontStyle">;

interface ResolvedPieSeries {
  readonly paint: Pick<ResolvedApplicationSeries,
    "strokeWidth" | "strokeOpacity" | "fillOpacity" | "lineDash" | "shadow"> & {
    readonly fill?: string;
    readonly stroke?: string;
  };
  readonly rotation: number;
  readonly outerRadiusRatio: number;
  readonly innerRadiusRatio?: number;
  readonly calloutLabel: PieFont & {
    readonly offset: number;
    readonly minAngle: number;
  };
  readonly calloutLine: {
    readonly length: number;
    readonly strokeWidth: number;
    readonly colors?: readonly string[];
  };
  readonly sectorLabel: PieFont & {
    readonly positionRatio: number;
    readonly positionOffset: number;
  };
}

interface PieMappingInput {
  readonly snapshot: ChartSnapshot;
  readonly assignment: PieAssignments;
  readonly style: {
    readonly common: Pick<ResolvedCartesianStyle,
      "textColor" | "fontFamily" | "fontSize" | "precision">;
    readonly application: Omit<ResolvedApplicationAppearance, "axes" | "series">;
    readonly series: ResolvedPieSeries;
  };
  readonly context: {
    readonly observations: { readonly kind: "raw-observations" };
    readonly display: ChartDisplayPolicy;
    readonly viewport: { readonly width: number; readonly height: number };
    readonly aggFunc?: SetupAggregation;
    readonly legendSelection?: Readonly<Record<string, boolean>>;
  };
}

export type TranslatePie = (input: PieMappingInput) => CartesianTranslationResult;
export const translatePie: TranslatePie;
```

The interface uses existing types without changing their owners or creating a persisted pie model. A resolved assignment must match a fresh `resolvePieAssignments` result for the snapshot's ordered selected numeric columns, including saved spelling, canonical family, offsets and title flags. Reject mismatches, missing descriptors and unsupported family input before producing options. P1's empty-string assignment IDs cannot bypass the snapshot's existing nonempty-ID rule. Dimensions, font sizes, widths and callout length/offset are finite nonnegative numbers; opacities and radius/position ratios are in [0,1]; callout minAngle is in [0,360]; rotation and sector positionOffset are finite signed numbers. Validate callback presence and dense nonempty palettes. Admission returns copied snapshot, style and selection, and every projection step uses those copies. Eagerly evaluate display callbacks inside the translator's failure boundary; renderer closures retain primitive display strings and copied metadata, never application callbacks or mutable input objects. Failed reads and formatter exceptions return diagnostics without partial options.

## Financial observations and legend identity

Use `aggregateSetupRows` only when `context.aggFunc` is configured. Otherwise every observation remains separate, including duplicate category text. P3 resolves category choice and supplies the already established aggregation option; P2 does not infer either from captions. Validate aggregate output before geometry, including overflow.

Each ring datum retains `colId`, row ID, source row IDs, category, descriptor and raw finite value separately from its angle contribution. Omit missing/null values in that ring. Reject malformed/nonfinite snapshot values through the existing snapshot boundary; P3's capture owns conversion of invalid source cells into missing data. Zero and negative finite values remain in legends and raw metadata with zero angular contribution. A positive enabled contribution is `max(rawValue, 0)`; normalize using only that ring's enabled positive observations. Never apply descriptor scale or sum revenue and gross profit together. Use stable normalization that cannot overflow and retain original raw values for labels/tooltips.

Use `pie-item:${JSON.stringify([colId, row.id])}` for a native legend/data name. Aggregated rows already have deterministic source-row-based IDs. Category captions and field-title prefixes are display text, never keys. Explicit `legend.data` contains every eligible main-ring datum once, in assignment then observation order. Format a separate key-to-label map with the exact `field display name + " - " + category` prefix only where P1 sets `titleInLegend` and a field display name exists. Equal labels remain distinct keys. Ordinary legend toggles affect only the selected observation in its ring; cross-filter legend coupling is outside this slice.

Palette lookup uses the observation index after configured aggregation but before invalid-value filtering, modulo the palette length, independently per ring. Invalid omissions leave color gaps; filtering never renumbers the palette. Each ring starts with the same full fill/stroke arrays, so the same row has the same palette color across rings. Saved scalar fill/stroke overrides retain their existing precedence.

`legendSelection` is transient rendering context, with absent keys enabled. Keep data entries, item IDs and palette indices stable when disabled; set their projected angle contribution to zero and set `legend.selected` consistently. Native ECharts filters the same item name in both label layers. Do not use field IDs alone or category names, which would couple unrelated slices. Preserve disabled names in the legend so users can restore them.

Tooltips use `trigger: "item"`, only on the painted series. Escape every text component. The original pie-specific branch uses the raw value's `.toLocaleString()`, field title and fiscal category heading; it does not use the Cartesian decimal override. Use `display.legend(category)` for the existing fiscal heading callback and raw `.toLocaleString()` for the value. Do not display normalized ECharts `value` or `percent` as an original financial observation. Callout text uses `display.seriesLabel(category)`; sector text uses `display.seriesLabel(rawValue)`. The ordinary Table policy's effective formatter is zero-decimal `formatNumber(value, 0)` for numeric labels; it overrides the theme's generic sector formatter. P3 passes the actual application callbacks rather than reproducing financial formatting in this mapper. Zero/negative slices have no positive area to hover; retained raw metadata is not a claim of a visible negative-sector tooltip.

## Geometry and independent labels

Use native `type: "pie"` for both families, numeric pixel radii, `clockwise: true` and `startAngle: 90 - rotation`, no minimum sector enlargement, no rose mode, no selected offset, no animation and no emphasis scaling. Set `stillShowZeroSum: false` and `showEmptyCircle: false`; ECharts defaults would invent equal slices or a filled placeholder.

Measure titles/subtitles, padding and the actual formatted legend entries before defining one polar content rectangle. Reserve callout room with the measured callout font and configured leader length/offset. Every donut ring shares the resulting center and available radius R. Apply P1 offsets as pixels, not percentages: `outer = max(R * outerRadiusRatio + outerOffset, 0)`; `innerCandidate = R * (innerRadiusRatio ?? 1) + innerOffset`; inner becomes zero when negative or exactly R. Pie without ring metadata uses inner zero. When inner exceeds outer, draw no sector instead of allowing ECharts to swap radii. Preserve collapsed rings: at R=50 three rings are `[30,50]`, `[0,10]`, `[0,0]`; at R=20 they are `[0,20]`, `[0,0]`, `[0,0]`. Keep legend metadata for collapsed rings and avoid labels on empty geometry. A zero viewport produces finite empty drawing options and recovers on resize.

A zero positive total does not produce sectors. For each assigned ring, render an unfilled 1px outer outline with full stroke opacity in callout-label color as a silent `graphic` circle, refreshed by the existing legend reprojection callback. This also applies to empty and all-invalid input for an assigned ring. No assignments means no rings/outlines. Draw the inner empty outline only when saved `innerRadiusRatio` is explicitly present, greater than zero and different from one. Normal offset-based donut therefore has only an outer empty outline.

Use two synchronized native pie series per ring when both label channels are enabled:

1. The painted main series owns sectors, callout labels/leader lines, item tooltip and native legend visuals. Emit it before its companion: ECharts takes the first matching legend data provider, so this order preserves painted swatches.
2. A companion pie uses the same data names, order, angle values, center, radii, rotation and filtering. It draws only sector labels: transparent fill, zero border, no shadow, `silent: true`, tooltip disabled, emphasis/select disabled and no automatic palette allocation. `legend.data` lists main datum keys once. Layer identity is a stable ring ID plus `:sector-labels`; it never enters saved state.

Sector-label radius is `inner + (outer - inner) * positionRatio + positionOffset`, with horizontal centered text. Before composing options, measure each already formatted label, calculate its coordinates from ring-local fractions and test all four text-box corners against the sector. Set that datum's `label.show` and text from the fit result; zero-span or degenerate sectors have no labels. A `labelLayout` callback supplies positions only, because its supported return type has no visibility switch. Legend reprojection recomputes both fit and coordinates. One enabled legend item with no inner radius centers its sector text, matching the original special case. Default sector ratio/offset are 0.5/0. Default callout offset/minAngle are 3px/0.001 degrees, line length/width 10px/2px; saved/effective values remain inputs. Callout min-angle suppression does not enlarge slices. Keep sector-label opacity independent of sector fill opacity. Explicit graphics for all labels would require duplicating native callout collision/leader layout; the synchronized layer is the smaller proposal. Acceptance must disprove stale coordinates, accidental pointer interception, duplicate tooltips, duplicate legend entries or phantom companion paint.

Native sector borders remain the bounded P2 paint strategy. The original renderer applies a stroke/spacing inset; exact thick-stroke and saved sector-spacing appearance remains an explicit P4 comparison risk. P2 does not introduce a custom sector renderer or claim pixel parity from numeric radius assertions.

The existing host already reads native legend selections and calls `projectLegendSelection` with immutable keys. P3 wires that callback to `translatePie` so selection recomputes per-ring fractions, position-ratio labels and zero-total outlines before repaint. P2 engine tests exercise this same dispatch-and-reprojection pattern. Native filtering must keep both layers geometrically aligned even before the callback; a raw `setOption` assertion is insufficient evidence.

## Bounded P2 acceptance and P3 handover

Write `tests/unit/chart-compatibility/pie.fixtures.ts`, `pie.test.ts` and `pie.render.test.ts`. Extend `snapshot.test.ts` only for the new empty-selection policy. Use the current one-worker Vitest configuration and existing SVG SSR geometry-test pattern; do not add a browser runner or install a dependency.

- Admission tests cover immutable input/output, mutation of caller objects after translation, eager formatter exceptions, assignment/snapshot disagreement, empty selection, saved alias, malformed style/callback/viewport, aggregate overflow and explicit missing-value handling. Renderer callbacks must still return the captured text after caller mutation and must not invoke the original formatting callbacks again.
- Numerical tests use independent expected fractions for unequal ring totals, repeated categories, zero/negative/null observations, toggled slices and configured aggregation. Include the retained four-quarter FMP fixture's raw values and separate totals without a provider request. This is fixture arithmetic, not application acceptance.
- Actual ECharts tests inspect rendered sector endpoints/radii, both label channels and glyph styles, callout leaders, zero-total outlines, negative/zero suppression, single/multiple rings, small viewports, rotation, label-position changes and finite SVG. Dispatch native legend actions against duplicate labels and multiple rings; verify labels, denominators, outlines, tooltips and restored entries after the existing callback pattern.
- Exercise shared caption/legend/font/background behavior in both palettes and ensure neither axes nor dataZoom/grid navigation appears. Capture no new feature flag or editor delta.
- Run scoped strict TypeScript, focused tests and the existing explicit-scope complexity checker on every changed production file. The parent updates inventory/breadth before acceptance, obtains independent review and records exact revision/results. P2 does not require an image build.

P3 starts only after mapper acceptance and separately freezes its writable session/caller/editor files. It owns effective saved-option resolution, original family panel visibility, category/aggregation/capture semantics, ordinary invalid-cell handling, display callbacks, host dimensions/stamps, legendScope/reprojection, saved `doughnut`, family switches and export/session behavior. Preserve saved radius/rotation semantics; the original standard pie panels do not expose rotation or the generic polar hole slider, so do not invent those controls. Its reviewer checks that this mapper's keys remain native transient selection identities and that no parallel state owner appears. P4 retains matched original/replacement appearance, real application FMP, refresh, save/reopen, export and candidate-image acceptance. P2 alone cannot close any of those claims.
