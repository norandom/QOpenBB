# Radar adapter contract

This contract fixes the inactive boundary for Radar Line and Radar Area in the existing Table/File editor. It combines original application observations with retained AG Grid 34.1.1 and AG Charts 12.1.1 source inspection. It does not establish replacement rendering or visual acceptance. The [milestone](radar-milestone.md) owns completion.

## Financial data and selection

Use the shared fixture `terminalpro/tests/unit/chart-compatibility/fixtures/radarContract.ts` in the Workspace fork. Its principal example is AAPL revenue in reported USD, fiscal years 2023-2025 on Q1-Q4 spokes. FY2026 has three quarters and a missing Q4. All 15 amounts match the retained FMP response with SHA256 `390dc8cbfc8302720a203bd9782d5e3b1f7363a4f762bdfcef079dbbe4c72f6b`, retrieved 2026-10-20. Fiscal years come from `fiscalYear`, not the calendar year of the reporting date. No normalization, annualization or new provider fetch is implied.

Capture displayed rows in their current filtered/sorted order. Apply existing aggregation before category/series inversion. With aggregation off, duplicate labels remain separate rows/spokes; with aggregation on, group by the original dimension-key semantics and retain first occurrence order. Inversion uses selected field order for spokes and one series per resulting row, retaining distinct row identity even where category text repeats. The mapper never aggregates a second time.

Preserve original capture normalization precedence: numeric `.value` wrapper, own `toString` parsed with `parseFloat`, then callable `toNumber`, otherwise unchanged. Engine validation accepts finite numbers, valid Dates and supported own-`valueOf` numeric wrappers; primitive numeric strings, null/undefined and nonfinite numbers become missing, not zero. The named Radar capture policy must turn admitted values into finite snapshot numbers while preserving missing positions. Do not execute arbitrary values from serialized chart configuration; these wrappers belong to the existing Grid value boundary.

## Geometry and domains

The mixed fixture uses categories C,A,B,D,A,E with Primary values 10,-5,0,missing,20,30 and Secondary 5,10,15,20,25,30. The original draws clockwise from the top, retains both A spokes, and uses radial ticks -10,0,10,20,30. Negative -5 is one eighth of the outer radius and zero one quarter in that view; do not take absolute values or clip negative data.

Radar Line breaks across missing values while preserving last-to-first closure when those endpoints are valid. Radar Area sends an invalid spoke to the geometric center and closes its polygon; the center is not necessarily the numeric-zero radius. Keep missing source values separate from that geometry. Preserve raw signed values in tooltip/label callbacks.

Each nonempty visible numeric domain includes zero before extent calculation. Positive-only values start at zero, negative-only values end at zero, and a nonzero constant spans zero to that value. Empty data stays empty. The retained scale path maps the degenerate all-zero domain to the range midpoint; this is source-derived, not a browser observation. Hidden series do not contribute to the radial domain, while their category contribution remains: hiding a series must not reorder or remove spokes.

Calculate the final nice domain from the polar axis's actual radial span. Do not hard-code the mixed fixture's ten-unit step or reuse Cartesian primary-axis matching. Retained source references: Enterprise `RadiusAxis.calculateTickLayout` (1996-2025); Community `Axis.calculateDomain` (17861-17902), `AxisTickGenerator` (19260-19512), `estimateTickCount` (18687-18706), `getTicks` (19660-19735), and `LinearScale.niceDomain` (30423-30480). The default tick count is five, default minimum spacing fifty; interval overrides and label collisions affect the selected count. Nice steps use the 1/2/5/10 power-of-ten sequence. Reimplement the behavior behind the adapter; do not copy dependency source into production. Verify several radii, constant domains and the FMP-sized values in focused numerical checks, then compare the actual FMP view at RD4.

## Existing appearance and controls

Use the established palette, font, caption, legend, background, padding and tooltip owners. Defaults observed in the original dark view are evidence for that view, not hard-coded cross-theme colors. Radar Line markers start enabled; Radar Area markers start disabled. Both retain marker settings. Original stroke width is two, opacity one, solid dash; Area fill opacity is 0.8 and labels start disabled. Preserve separate fill/stroke palette semantics.

The original exposes one Polar Axis group: Color, Thickness, Shape, Inner Radius, and label Font, Weight, Size, Color, Orientation. Shape is `circle` or `polygon`; orientation is `fixed`, `parallel` or `perpendicular`. Inner radius is `innerRadiusRatio`, a fraction in [0,1], with slider step 0.05. It is not pixels or percentage points. Preserve predefined font weight/style values during roundtrips.

Original options use `radar-line` and `radar-area`, while saved chart families remain `radarLine` and `radarArea`. Thickness edits atomically update the relevant `axes.angle-category.line.width` and `axes.radius-number.line.width`; both families persisted three and visibly painted width three. Other Polar fields follow the original option service's applicable-axis filtering, not an unrestricted copy to every axis. The retained Grid `PolarAxisPanel` at 48576-48734 and axis option service at 52985-53018 define those paths.

Preserve both navigator quick actions and their existing caller state ownership. In the observed original Radar views, Show navigator and Show mini chart produced unchanged chart drawings and no slider/toolbar. Do not invent an additional Radar navigation surface or infer persistence solely from unchanged chart-model fields.

Line tooltips exposed the tested raw values 10,-5,0. The Area probe retained a stale first-point tooltip at the tested negative/zero coordinates. This is an original interaction limitation, not permission to deliberately reproduce stale financial values. Replacement tooltips must identify their actual datum and raw value. Original CSV requests also failed after some actions; these runs do not establish clean network diagnostics.

## Shared inactive declarations and ownership

`compatibility/radarContracts.ts` is the sole shared type prerequisite. It defines concrete family/option names, series assignments, resolved polar appearance, mapping input/result, editor state/intents, and prepared selection. It has no runtime registration. `RadarTranslationResult` reuses only the existing result envelope, not Cartesian numerical semantics.

RD1 exclusively owns new `compatibility/radarAssignments.ts` and `echarts/radar.ts`, `radarData.ts`, `radarSeries.ts`, `radarLayout.ts`, with focused assignment/mapping/engine tests. The pure mapper receives an already selected snapshot, resolved style, viewport and transient legend selection. It does not read storage, GridApi or React state.

RD2 exclusively owns new `application/radarSessionSelection.ts`, `radarAppearance.ts`, `radarEditorState.ts`, `radarEditorTransaction.ts`, and `editor/radar/RadarControls.tsx`, with focused selection/appearance/transaction tests. It receives resolved baseline/range/setup/projection from the existing owners and returns prepared mapping inputs. It must not import RD1 implementations or cast Radar to a Cartesian family. Existing reducers retain persistence and stale-edit checks at the join.

Resolve appearance using the current composition contract: generated common replaces saved common, then saved family options merge over generated family options. Retain stock/custom theme parameters, effective overrides and inactive saved keys. Original generated polar options strip Cartesian marker/connect-missing additions. Avoid new option/state owners.

The shared join is two sequential review units: RD3a capture/setup policy, then RD3b session/editor/caller routing. Initial whole-file physical baselines include gridCapture 326, setupProjection 276, useApplicationChartSession 308 and AgChartView 337. Measure logical/function caps before edits; extract cohesive dispatch responsibilities when needed. Neither parallel lane edits these shared files or the application family union. Additional helper files require controller registration before writing; all modified production files must pass 400/300/50 caps before acceptance.

## Evidence limits

The original probes, source hashes, fixture derivation and static checks are retained under ignored `artifacts/chart-radar/`. Publish only the concise reviewed report and selected derived fixture; raw dependency excerpts and authentication/runtime artifacts remain private. Actual application rendering, light/dark parity, complete controls, fresh reopen, export and image publication remain RD3-RD5 work. No source contract is a substitute for that acceptance.
