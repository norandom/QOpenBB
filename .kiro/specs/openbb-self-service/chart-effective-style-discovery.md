# Effective Cartesian style: next evidence boundary

Stored option fidelity does not yet supply an effective renderer style. The next bounded input must separate fill from stroke, title visibility from title text, and missing-data connection from markers. Passing saved `bar` or `line` objects straight into the current Cartesian mapper would lose those distinctions. This is read-only discovery, dated 2026-10-16, not a production design or parity acceptance.

## Source and scope

Original reference: Workspace `38dffc33389aca0e4a87e0e88d42f7067aa220df`, read with local `git show`; paths below are relative to `terminalpro/src/components/General/Table/`:

- `Chart/themes.tsx`: `getLegend`, `defaultOverrides`, `getOpenBBChartTheme`, `getCustomChartTheme`, `useAgThemes`, `createItemStyler`.
- `Chart/hooks/useChartOptions.tsx`: `getDefaultChartOptions`, generated `options`, `chartThemeOverrides` (especially lines 367-434).
- `Chart/utils.tsx`: `createDefaultSeries`, `createDefaultAxis`, `getSeriesType`.
- `AgChartFromTable.tsx`: detached range-chart setup and options event (lines 299-319); forecast is a separate explicit-options path and outside this three-family boundary.

Current mapper inspected: `vendor/workspace/terminalpro/src/components/General/Table/Chart/echarts/{cartesianTypes,cartesian}.ts`. Tests inspected: `tests/unit/chart-compatibility/cartesian.test.ts`, `snapshot.fixtures.ts` by import, and `tests/e2e/chart-compatibility/cartesian.spec.ts`. No tests, builds, browser sessions, dependency changes or network calls were run in this lane. Existing test source is evidence of assertions, not a fresh passing result.

## Source-provable composition

1. `useAgThemes` selects `custom-${theme}` only when the matching configured theme has truthy `baseTheme`, `palette` and `params`; otherwise it selects `openbb-${theme}`. Selection must use the active mode. The separately returned `themePalette` is assigned while looping both modes and is not a safe substitute for the selected theme's palette.
2. OpenBB dark uses `ag-default-dark`, background parameter `#151518`; light uses `ag-default`, `#FFFFFF`. Both carry common legend/title overrides and the line defaults below. Custom themes choose the dark/light OpenBB override template from `baseTheme`, then replace `palette` and `params` with configured objects. Replacement is not a leaf merge with the OpenBB background parameter object. The underlying AG base theme still supplies unspecified values.
3. `createDefaultSeries` supplies labels disabled and an enabled tooltip; it does not define Cartesian fill, stroke, stroke width, missing-data connection or markers. `createDefaultAxis` supplies generated axes, optional widget x/y titles and formatter callbacks. Those axis titles are distinct from the chart title.
4. Caller `chartSeries` and `chartAxis` are lodash-merged over generated series/axes. `getDefaultChartOptions` places axes under `common.axes`. It retains the full series object under `line`; for `bar` it removes `connectMissingData` and marker, retaining other series fields and setting label placement `outside-end`. Grouped and stacked columns use the `bar` series namespace; line uses `line`.
5. The hook inserts a generated OpenBB-mode legend under `options.common.legend`, including a fiscal-period formatter. It sets the generated navigator. Before merging saved overrides it performs `chartOptions.common = options.common`; stored common settings therefore do not survive this effective-options composition. Then `merge(options, chartOptions)` gives saved family fields precedence over generated family fields. Inactive family branches remain present but are not applied as the active family's settings.
6. This proves the application's theme and override objects. AG's subsequent base-theme/common/family resolution and auto defaults are a separate boundary. Do not label a guessed flattened precedence as observed effective AG runtime behavior.

## Finite leaf contract for the next slice

This inventory describes the minimum evidence-bearing inputs needed for translation; it does not authorize a new interface. Values must be supplied as explicitly resolved leaves with provenance (selected base/custom theme, generated override, saved active-family override or AG runtime default). Missing evidence is a diagnostic, not an ECharts default.

| Leaf group | Finite resolved input | Original source / consequence |
| --- | --- | --- |
| Family | `groupedColumn`, `stackedColumn`, `line` | Resolve `bar` for either column family; never apply retained bar settings to line. |
| Theme shell | background color; separate text/font leaves for title, legend and axes where they differ | The current single font/color tuple cannot express OpenBB title size 12, legend size 11 and axis size 11 independently. Resolve AG inherited fonts/colors before claiming parity. Background image is outside a plain-color shell. |
| Palette | nonempty fills and strokes, independently, plus explicit series assignment order | Original custom theme has distinct `palette.fills` and `palette.strokes`. `defaultFills` in `themes.tsx` belongs to `createItemStyler`; it is not proof of AG's ordinary series palette. |
| Chart title | `{enabled: boolean, text: string}` plus resolved title typography | Saved active namespace has `title.enabled` and `title.text`. Empty text and disabled title are separate states; do not infer visibility from nonempty text. OpenBB sets only common title font size 12. Base title visibility/text require inherited resolution. |
| Column style | each stable numeric descriptor ID -> `{fill, stroke, strokeWidth}` | Saved `bar.series.fill`, `stroke`, `strokeWidth` affect family series; descriptor mapping happens after series construction/order. Palette fallback must retain separate fill/stroke. Width zero is meaningful. |
| Line style | each stable numeric descriptor ID -> `{stroke, strokeWidth}` and marker leaves below | Saved `line.series` overrides the theme line defaults. A line stroke is not automatically a column fill. |
| Legend | `{enabled: boolean, position: top/bottom/left/right}` plus resolved label style, marker and layout leaves if visual parity is claimed | OpenBB `getLegend` sets top, maxHeight 50, spacing 20; item paddingX 32/paddingY 8, square marker size 11/padding 5; label color white/black and size 11. It does not explicitly set enabled. Saved `bar.legend`/`line.legend` can carry family settings; saved common legend is replaced by generated common. |
| Missing observations | `connectMissingData: boolean` for line | OpenBB explicit default is true. Current mapper fixes `connectNulls: false`, so it contradicts that default on interior nulls. Preserve observation nulls; change only the drawn connection. |
| Markers | `enabled: boolean`; if enabled, resolved shape, size, fill, stroke, strokeWidth | OpenBB explicit default is `line.series.marker.enabled: false`; current mapper supplies no `showSymbol`, allowing an ECharts default. Enabled marker details require AG inherited resolution. |
| Display precision | explicit bounded precision plus formatting semantics | Existing mapper uses fixed decimals. Original generated axis/tooltip/legend formatters use magnitude, fiscal-period and column context. A precision integer alone does not prove original formatting parity. |

For the smallest source-provable first bridge, constrain fixtures to plain background, disabled distinct-bar fill, no navigator/mini-chart, explicitly supplied inherited style leaves, and original line markers disabled. Report unsupported features when present rather than silently approximating them. Keep any future modules within 400 physical lines/file, 300 logical units/file and 50/function; include them in the existing checker inventory.

## Current mapper gaps that follow directly from source

- `CartesianSeriesStyle.color` drives item fill and line stroke together; column border color has no field. `lineWidth` maps to bar border width and line width. Separate fill/stroke cannot round-trip through that contract.
- `ResolvedCartesianStyle.title?: string` expresses title omission/text but cannot retain disabled title text separately. An adapter can suppress a disabled title while retaining original state elsewhere; the state itself must not be rewritten.
- Legend has show/position but omits original marker/layout constraints. Setting `left: 0` or `right: 0` alone also does not establish original orientation or centering.
- `connectNulls: false` is hardcoded; markers are omitted. Neither follows the original OpenBB explicit defaults.
- Unit checks, stable IDs, same-sign stacking and unchanged observations are already mapper responsibilities. Theme research must not replace them or round the data.

The existing unit suite asserts the explicit synthetic style, bar widths, legend positions, title omission/empty text, stable IDs and numeric preservation. It has no original effective-theme resolver assertion and no AG/ECharts marker/gap comparison. The E2E fixture checks synthetic rendering and observations; it does not establish original Workspace theme parity.

## Exact observations still needed

| Observation | Why source alone is insufficient |
| --- | --- |
| Original resolved options for groupedColumn, stackedColumn and line in dark/light, with and without one valid custom theme | Establish AG inherited palette, font/color defaults, title/legend enabled defaults, palette slot assignment and actual common/family precedence. Capture input overrides and resolved options together. |
| Original line with one interior missing observation and no line edits, then connect-missing-data toggled | Default true is source-proven; actual event path/payload for the control and drawn null behavior remain unobserved here. Compare unchanged underlying values. |
| Original line marker toggle, then one shape/size/fill/stroke edit | Disabled default is source-proven; editor event namespaces and resolved enabled marker appearance are not. |
| Independent column fill and stroke edit with different colors and nonzero width, then series reorder | Proves editor payload shape, global/per-series application, palette assignment and stable-ID mapping. Existing observed width patch does not prove colors. |
| Title enabled false with nonempty retained text, then true; repeat for line | Column text/enabled patch path is captured in prior approved work. Line event namespace, inherited title behavior and drawn visibility need their own observation. |
| Legend toggle and all four positions, with duplicate display labels and one/multiple series | Existing bottom-position column capture does not establish auto enabled behavior, line control payloads, vertical orientation or layout. |
| Original and ECharts at the same fixed viewport, selected series, theme and fixture values | Needed for a no-UX-delta claim about spacing, axis typography, legend/title placement and symbol visibility. Resolved option equality alone is insufficient. |

The above is a finite capture matrix, not permission to run it in this lane. Extra fields such as background images, per-datum distinct fill, navigator, fiscal formatting and axis titles need separate evidence/contracts if admitted later. `createItemStyler` is source-provably conditional: when enabled it skips data containing multiple numeric series keys and assigns colors using xValue for detected BarSeries or yValue otherwise. Its map therefore must not be casually reinterpreted as category-index coloring. Keep it outside this first bridge until a dedicated fixture establishes the behavior to preserve.
