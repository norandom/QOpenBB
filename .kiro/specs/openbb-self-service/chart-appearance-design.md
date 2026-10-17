# Explicit Cartesian appearance mapping

## Overview

Proposed bounded amendment after accepted tasks 2.24-2.27. Extend the existing three-family ECharts mapper so resolved inputs can express separate fill/stroke, title visibility, caption typography, missing-observation connection and circular markers. These are necessary distinctions for preserving OpenBB's appearance. This slice does not infer the entire original theme or reconnect incomplete application controls.

Current Workspace baseline: `5c2df9864bed000170ffccde146273b468e0552e`. Original reference: `38dffc33389aca0e4a87e0e88d42f7067aa220df`. This supplements the parent design and its requirement coverage; human design approval is pending.

## Boundary Commitments

### This slice owns

- Additive explicit appearance fields in the existing resolved-style contract, preserving old fixture behavior when they are absent.
- Validation and ECharts projection of those fields for groupedColumn, stackedColumn and line.
- Isolated browser and numerical evidence for title retention, independent colors, typography, line gaps and circular marker visibility.

### Out of Boundary

Full original theme/default resolution, arbitrary AG option decoding, original editor implementation, application activation, new controls/flags, grid capture, financial formatting changes, other chart families, other marker shapes, saved backend state and SQLite repair. All remain obligations of eventual application parity. No existing feature is disabled or hidden by this slice.

### Allowed Dependencies

Locked ECharts 6.0.0, existing snapshot/style contracts, accepted EChartsHost and the existing verification toolchain. No new runtime package. Production code must not import AG Charts, its private APIs, GridApi, providers or stores. Original AG source and outgoing captures supply reference evidence only.

### Revalidation Triggers

Changes to style precedence, series identity, palette assignment, null handling, types, typography, ECharts version or lifecycle revisions invalidate affected unit/browser evidence. Actual theme decoding and original-control adoption require separate integration contracts and original light/dark comparisons.

## Architecture and Evidence

Keep one Cartesian mapper. Move its style validation and appearance construction into a cohesive style module so the numerical mapper remains within the whole-file complexity caps. The mapper continues to own source-mode/unit checks, selected series order, ordinal category identity, exact data values, same-sign stacking and escaped display formatting.

Original dark-theme UI capture on 2026-10-17 used four synthetic periods with revenue 100/null/140/160 and EPS 1.2/null/1.6/1.8. Five outgoing dashboard payloads and screenshots confirm `line.title.text`, independently retained `line.title.enabled`, and `line.series.marker.enabled`. Default lines span the interior null without markers; enabling markers draws circles only at non-null points. Circle and size seven are visible editor values. This is a reference observation, not a mixed-unit acceptance fixture for our single-axis mapper. New mapper browser fixtures use two series with the same explicit unit and scale.

No Connect Missing Data control was observed in the inspected original Series panel. Original theme source explicitly sets connectMissingData true; configuration behavior can therefore be projected without inventing a new product control. The capture did not test false through the original UI, light mode, resolved marker fill/stroke or full typography.

Original `AgChartInstance.getOptions()` returns user options. It is not an effective-style oracle. AG's internal processedOptions includes resolution, but initialization depends on the real chart factory and internal registries. Do not introduce a guessed JSON merge, private AG runtime dependency or copied AG resolver. Supply explicitly resolved values to this mapper; the next theme-resolution boundary will establish their provenance.

Build versus adopt: use ECharts title, textStyle, itemStyle, lineStyle, connectNulls and symbol fields. Small explicit projection is needed to preserve the financial observations while adapting the two libraries' different field names. No second renderer abstraction is introduced.

## Components and Interfaces

### Extended resolved style

Keep `translateCartesian(snapshot, family, style)` and its supported/unsupported/invalid result. Retain all existing required fields and their behavior. Add these optional fields to `ResolvedCartesianStyle`:

| Field | Contract | Projection |
| --- | --- | --- |
| `titleEnabled` | boolean; requires `title` to be a string, including empty | Set title.show explicitly, retaining title.text even when false |
| `typography` | complete object with `title`, `legend`, `axis`, each `{color:string,fontFamily:string,fontSize:number}` with finite nonnegative fontSize | Caption-specific textStyle and both axisLabel styles |
| `line` | complete `{connectMissingData:boolean,markers:LineMarkerStyle}` | Explicit line connection and marker behavior |

`LineMarkerStyle` is a discriminated union: `{enabled:false}` or `{enabled:true,shape:string,size:number}`. Size is finite nonnegative, measured in pixels. Other shapes yield unsupported diagnostics when line is active; malformed fields yield invalid. No automatic shape substitution. Disabled marker objects do not require size/shape. Only the active line family projects these fields; valid line settings can remain in a style object while a column family is rendered, without adding line properties to bar options.

Add optional `fill`, `stroke`, `strokeWidth` and `markerFill`, `markerStroke`, `markerStrokeWidth` to `CartesianSeriesStyle`. Colors are strings; widths are finite nonnegative numbers. Overrides remain keyed by numeric descriptor ID, never display label or series index. Marker-specific fields are used only for enabled line markers. Existing `color` and `lineWidth` retain their legacy meanings when the corresponding new field is absent.

Validation checks every provided optional field, including inactive-family fields, for malformed values. Unsupported shape is a semantic result only when active line markers are enabled; the same well-formed but unimplemented shape in an inactive line configuration is retained without projection. To represent this distinction, enabled marker `shape` is typed as string at the boundary; only circle is supported for active rendering. A non-string shape is invalid. Optional fields omitted or explicitly undefined are absent; null is invalid. This matches the existing style boundary's optional-field convention.

### Deterministic appearance precedence

For each selected numeric descriptor, let paletteColor be `palette[index % palette.length]`, where index is its selected numeric-series position. Resolution applies only to rendering; input styles and original stored models are never rewritten.

- Column fill: explicit fill, then legacy color; if neither exists, preserve the existing ECharts palette behavior.
- Column border color: explicit stroke only. Do not infer a column border from legacy color, because the previous mapper did not set one.
- Column border width: explicit strokeWidth, then legacy lineWidth; otherwise preserve the previous omitted field.
- Line stroke: explicit stroke, then legacy color. When the new line object is present, resolve any remaining fallback explicitly to paletteColor, so line and marker colors cannot diverge after a selection reorder. When line is absent, retain the prior omitted color and ECharts palette behavior. Width: explicit strokeWidth, then legacy lineWidth.
- With explicit enabled markers, fill is markerFill, then explicit fill, then legacy color, then paletteColor. Marker stroke is markerStroke, then the resolved explicit line stroke, then paletteColor. Marker border width is markerStrokeWidth, then resolved explicit line width, then zero. These are fixture-resolved fallback rules, not inferred AG defaults; original adoption must supply values that match the original effective style.
- With line absent, retain current connectNulls false and omitted showSymbol. With line present, use its connectMissingData and set showSymbol from markers.enabled; enabled circle maps to symbol circle and symbolSize. Missing/null rows remain null and have no point marker. No interpolation or data filling occurs.
- With typography absent, emit the previous text/axis options unchanged. With typography present, use each complete font tuple for its caption; global textStyle remains the legacy base for other text.
- With titleEnabled absent, preserve prior title emission exactly. A disabled explicit title retains its text in the ECharts option and saved input. Re-enabling must not need to restore text from elsewhere.

Projection code must not let stale family properties survive replacement. Column options have no line connection or marker fields; line options have no stack/bar-border residue. The accepted host continues to replace full options with monotonic render revisions. Data revision stays unchanged for appearance-only edits.

### Style module

New `echarts/cartesianStyle.ts` owns validation and appearance projection. Its validation result distinguishes malformed fields from an unsupported active marker shape and reports diagnostic paths. Typed helper functions return title/legend text options, axis-label style and family-specific series appearance. They accept explicit values and perform no store lookup or financial transformation.

Freeze these exports in the shared contract task: `validateCartesianStyle(input: unknown, family: CartesianFamily): StyleValidation`, where StyleValidation is `{status: "valid", style: ResolvedCartesianStyle}` or `{status: "invalid" | "unsupported", diagnostics: readonly SnapshotDiagnostic[]}`; `seriesAppearance(style: ResolvedCartesianStyle, seriesId: string, paletteIndex: number, family: CartesianFamily): CartesianSeriesAppearance`; and `captionAppearance(style: ResolvedCartesianStyle): CartesianCaptionAppearance`. CartesianSeriesAppearance contains itemStyle `{color?,borderColor?,borderWidth?}` and optional lineStyle `{color?,width?}`, connectNulls, showSymbol, symbol and symbolSize. Color fields are strings, dimensions numbers, flags booleans and projected symbol is literal circle. CartesianCaptionAppearance contains `title: EChartsOption["title"]`, legendText with required color/fontFamily/fontSize, and axisLabelStyle with required color and optional fontFamily/fontSize. These types live in cartesianTypes.ts. The numerical mapper delegates style work and retains its public function signature. Any extraction of existing validation is behavior-preserving and must pass all existing negative tests. Do not compress the mapper or create forwarding-only modules to meet caps.

## File Structure Plan

Frontend paths are relative to `vendor/workspace/terminalpro/`.

| Path | Responsibility |
| --- | --- |
| `src/components/General/Table/Chart/echarts/cartesianTypes.ts` | Additive appearance types |
| `src/components/General/Table/Chart/echarts/cartesianStyle.ts` | Style validation, diagnostic paths and appearance projection |
| `src/components/General/Table/Chart/echarts/cartesian.ts` | Delegate style work while preserving numerical mapping |
| `tests/unit/chart-compatibility/cartesian.test.ts` | Existing behavior and new appearance mappings |
| `tests/unit/chart-compatibility/appearance.fixtures.ts` | Explicit synthetic style cases with source/capture provenance labels |
| `tests/unit/chart-compatibility/snapshotContracts.types.ts` | New valid/invalid type assertions |
| `tests/e2e/chart-compatibility/appearance.html` and `appearance.tsx` | Isolated real mapper/host composition; fixture controls only |
| `tests/e2e/chart-compatibility/appearance.spec.ts` | User-visible render/update/export observations |
| Existing fixture Vite/Playwright configuration | Register the added fixture using the existing one-worker setup |

The controller owns inventory, breadth, source pins and acceptance documentation. Existing reducers, option-state helpers, data snapshots, EChartsHost, application callers, dependency locks and product flags remain unchanged. All maintained new/modified files pass 400 physical lines, 300 logical units and 50/function, measured as whole files. No new exception is proposed.

## Requirements Traceability and Testing Strategy

This slice contributes to 4.8 and 4.9 but cannot complete them. Criteria 10.1, 10.2, 10.3 and 10.4 govern isolated headless/CDP journeys, reproducible outcome checks and one-worker execution. Criteria 10.5 and 10.6 govern actual test paths and explicit remaining gaps. Persistence criteria 4.2 and 4.7 remain separate; all other requirement coverage remains in the parent design.

- Keep all 221 accepted units passing; add complete optional-field validation, null/undefined distinctions, unsupported active marker shapes, inactive-family retention and all precedence branches.
- Assert independent fill/stroke, zero/fractional widths, marker-specific colors/widths and identity-bound overrides under reordered selected series. Assert no data rounding, conversion, sorting or mutation.
- Assert false/true title visibility retains nonempty and empty text, and separate title/legend/axis font tuples project exactly. Legacy inputs produce the prior output shape.
- Use a homogeneous-unit four-observation line fixture with one interior null. Both connect states retain identical numeric arrays; false leaves a gap, true bridges it. Markers toggle without marking the null row. Verify actual rendered circle counts/positions and exported pixels as well as ECharts options.
- Browser sequence: render default explicit no-marker/connected line, toggle circular markers, hide/re-enable retained title, change typography and distinct colors, switch to columns and back, resize and export. Appearance edits use new render revisions at unchanged data revision; invalid/unsupported style does not replace the last good render, then a valid correction recovers.
- Preserve existing browser smoke, lifecycle and Cartesian cases. Build the actual fixture, run strict checking, repository-configured lint and the registered module audit. Record exact source/dependency identities. Original dark-mode screenshots corroborate selected semantics; they do not certify pixel equality, light-mode parity or full original Workspace integration.

## Error Handling and Delivery

Malformed appearance yields invalid diagnostics, unsupported active marker shape yields unsupported, and neither produces partial options. Fixture UI shows the diagnostic while retaining the previous good chart; this is not a new production error UX. Original stored configurations remain untouched.

After human design approval, generate bounded tasks. Freeze types and fixtures first. Style-module work and isolated browser-fixture scaffolding can proceed in disjoint lanes only after shared signatures are fixed; the numerical-mapper join and actual browser verification are sequential gates. Sol owns bounded implementation; Astra reviews contract/financial continuity and final acceptance. No image is promoted by this slice.
