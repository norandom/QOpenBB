# Theme Settings Charts preview control map

Replace the preview renderer inside the existing Charts panel. Preserve its data, controls, draft state, persistence and 300 ms debounce. Several visible controls configure chart features absent from this sample; a native preview must not invent new controls or features to make every field appear active.

Assessment date: 2026-10-27. Workspace source: `e12713d29a9572599c7482d293f37cc040eba12f`. This is source assessment, not browser or renderer acceptance. Adopted as the source reference for the reviewed preview contract. The owner approved making Padding effective on 2026-10-27; other compatibility boundaries remain unchanged.

## Source and sample

Paths below are relative to `vendor/workspace/terminalpro/` unless marked otherwise.

- `src/components/ThemeSettings/ChartSettings.tsx` directly renders `AgCharts`, with debounced options from `chartThemePreview.ts`.
- `ChartPaletteControls.tsx` exposes paired fill/stroke rows and add/remove controls. `ChartParameterControls.tsx` exposes 22 fields in five collapsible groups.
- `ThemeSettingsLayout.tsx` owns Light Mode, Dark Mode, Save Theme and Reset. `useChartSettings.ts` and `chartThemeState.ts` own draft isolation, serialization and reset semantics.
- Exact AG Charts Community 12.1.1 source is retained at root `artifacts/task-2.1/frontend/terminalpro/node_modules/ag-charts-community/dist/package/main.cjs.js`, with version confirmed by the adjacent package.json. Public parameters/defaults: 26226-26267; axis defaults: 26318 onward; chart defaults: 26411 onward; CSS parameter application: 8667-8678; parameter validation: 32805-32845. These are source evidence, not a runtime probe.
- Current application projection: `src/components/General/Table/Chart/caller/themeInputs.ts`, especially `parameterOptions` and `projectCallerTheme`. Its finite field projection does not cover all preview parameters.

Keep the title **Dolphin Interaction Data**, categories **Peter**, **Mary**, **Mercutio**, **Ada**, category-bottom/value-left axes and bottom legend. Each bar series has a two-pixel stroke. The series count equals the fill-array length. The first four series use the following retained values; extra series are named `Series 5`, `Series 6`, etc. For extra index `i` starting at 1, values are `30 + 10i` when `(categoryIndex + i)` is odd and `50 + 10i` otherwise.

| Series, in palette order | Peter | Mary | Mercutio | Ada |
| --- | ---: | ---: | ---: | ---: |
| Number of Looks (TM) | 60 | 57 | 238 | 237 |
| Number of Looks (YM) | 64 | 93 | 217 | 217 |
| Interaction Duration (TM) | 120 | 135 | 140 | 110 |
| Interaction Duration (YM) | 86 | 259 | 145 | 147 |

These sample measures have no financial units or provider provenance. They must not be relabeled as FMP data. The retained FMP journey remains a separate application acceptance check.

The sample's bars are vertical, grouped by category, without stacking. Both mode defaults contain ten palette pairs; UI removal stops at one pair. At one series AG's default legend is disabled even though the builder specifies its bottom position. Persisted empty arrays can bypass the UI minimum; do not silently invent palette entries when assessing such payloads.

Default font is `Verdana, sans-serif`, weight 400. The state initializes fontSize to 12, giving a 17 px title and 12 px category/value labels and legend; title size scales by 17/12 when edited. Explicit chrome typography overrides inherited font settings for tooltip text. The title has 20 px spacing with no subtitle. Chart outer padding remains AG's 20 px default. The legend is horizontal at the bottom, with 30 px spacing from the plot, 15 px markers, 8 px marker-to-label padding and item paddingX 16 / paddingY 8. It lays items into a grid within available width/height and displays pagination only when that layout needs more than one page (source 36248-36300). Replacing this with a single clipped legend row or pagination at every wrap changes behavior. Legend click toggles series; resize can change wrapping/pages.

## Controls and native mapping

“Direct” means the AG source supplies a rendering path in this sample. Conditional effects require hover, keyboard focus or legend overflow. Actual before/after appearance remains untested here. Native paths are implementation targets, not verified equivalents.

| Visible control / stored field | Existing preview effect from source | Native ECharts target and boundary |
| --- | --- | --- |
| Fill Color / `fills[index]` | Direct bar fill and legend marker color for the corresponding series. | Each bar series `itemStyle.color`; legend marker retains matching fill. Do not color by category. |
| Stroke Color / `strokes[index]` | Direct corresponding bar outline; preview explicitly sets width 2. | Each series `itemStyle.borderColor` and `borderWidth: 2`; preserve marker outline where applicable. |
| Add palette color | Adds a paired fill/stroke from the selected mode's defaults, and one sample series. The pair uses one random index. | Rebuild series from the unchanged state owner; preserve current paired random selection semantics. |
| Remove palette color N | Removes the paired entry and reduces/reorders preview series by the existing sample algorithm. Only shown when more than one fill exists. | Rebuild with replacement option semantics so removed series disappear. Do not retain stale ECharts merged series. |
| Font Family / `fontFamily` | Direct title, axis labels and legend; chrome font inherits it unless explicitly set. | Global `textStyle.fontFamily` plus explicit title/axis/legend/tooltip styles where component defaults override global style. |
| Font Size / `fontSize` | Direct axis/legend size; title default scales by 17/12. Chrome size inherits it unless explicitly set. | Preserve relative sizing with `title.textStyle.fontSize`, axis/legend size and tooltip size. One global size alone is insufficient. |
| Font Weight / `fontWeight` | Direct title, axis labels and legend; chrome weight inherits it unless explicitly set. | Corresponding `textStyle.fontWeight` including tooltip inheritance. Retain saved string values and null/default semantics. |
| Background Color / `backgroundColor` | Direct chart background via `chartBackgroundColor` reference. With absent explicit background in dark mode, builder sets background invisible. | `backgroundColor`, including transparent branch; keep outer panel styling unchanged. |
| Foreground Color / `foregroundColor` | Default text, chrome text, axis/grid mixes and focus/pagination inherit it unless more specific colors are set. | Resolve fallback chains into title/axis/legend/tooltip colors; axis/grid mixes and legend navigation are separate leaves. Do not map only global text. |
| Accent Color / `accentColor` | Conditional keyboard-focus indicator and interactive chrome accents via AG CSS. It does not recolor ordinary bars. | ECharts has no equivalent universal accent parameter or AG keyboard focus UI. Requires a narrow compatible focus treatment if preserving that interaction; do not misuse `emphasis.itemStyle.color`. |
| Border Color / `borderColor` | Conditional tooltip border and chart chrome borders via CSS. Does not set bar strokes or a plot frame. | `tooltip.borderColor`; further chrome paths apply only if present. Keep bar border tied to `strokes`. |
| Text Color / `textColor` | Direct title, legend and axis labels. Does not override independently inherited chrome text. | Explicit title/legend/axis colors; tooltip uses `chromeTextColor` fallback to foreground, not textColor. |
| Subtle Text Color / `subtleTextColor` | No subtitle/footnote in sample; affects inactive legend pagination marker if overflow produces pagination. | `legend.pageIconInactiveColor` if scroll/pagination exists; no subtitle should be added. Ordinary chart appearance need not change. |
| Padding / `padding` | Stored and passed to AG params, but absent from AG public parameter schema and defaults. AG uses `chartPadding`, not `padding`. Existing unit test proves forwarding only. | Owner-approved correction: apply finite nonnegative outer padding, including zero; absent means 20 px. Preserve `params.padding` serialization. Invalid values retain the draft and show a diagnostic, rather than silently clamping. |
| Chrome Background / `chromeBackgroundColor` | Conditional tooltip background and focus-indicator outline. No preview menus/dialogs/toolbars are configured. | `tooltip.backgroundColor`; compatible focus outline if retained. Preserve absence of toolbars. |
| Chrome Text Color / `chromeTextColor` | Conditional tooltip text; default inherits foregroundColor. | `tooltip.textStyle.color`, with explicit fallback resolution. |
| Chrome Font Family / `chromeFontFamily` | Conditional tooltip font; default inherits fontFamily. | `tooltip.textStyle.fontFamily`. |
| Chrome Font Size / `chromeFontSize` | Conditional tooltip font size; default inherits fontSize. | `tooltip.textStyle.fontSize`. |
| Chrome Font Weight / `chromeFontWeight` | Conditional tooltip weight; default inherits fontWeight. | `tooltip.textStyle.fontWeight`. |
| Chrome Subtle Text / `chromeSubtleTextColor` | Tooltip footer secondary text and other chrome secondary text. Default sample tooltip has no configured footer; no guaranteed ordinary visible change. | Preserve secondary tooltip text styling if content requires it. One tooltip text color cannot represent both primary and secondary text. Do not add footer text to demonstrate this setting. |
| Input Background / `inputBackgroundColor` | Recognized AG parameter; no chart-owned text inputs are present in this bar sample. Does not theme the surrounding administration form. | Stored-only in this preview. ECharts option model has no chart input theme equivalent; preserve payload for controls elsewhere. |
| Input Text Color / `inputTextColor` | Same latent chart-input boundary. | Stored-only in this preview; do not apply to form inputs or tooltip text. |
| Grid Line Color / `gridLineColor` | Direct number-axis grid; category-axis grid defaults disabled. | Value-axis `splitLine.lineStyle.color`; keep existing enabled axes/grid pattern. |
| Axis Color / `axisColor` | Category-axis line; ticks default disabled and number-axis line defaults hidden. | `xAxis.axisLine.lineStyle.color`; retain hidden y line/ticks. Coloring newly shown lines/ticks widens the sample. |
| Crosshair Label Background / `crosshairLabelBackgroundColor` | Recognized parameter, but actual crosshair implementation is an Enterprise module absent from current Community-only source imports. No current preview crosshair effect established. | ECharts `axisPointer.label.backgroundColor` is a possible engine equivalent; do not enable axisPointer/crosshair merely to make this latent field visible. |
| Crosshair Label Text / `crosshairLabelTextColor` | Same retained crosshair boundary. | Possible `axisPointer.label.color`; remain latent without an existing crosshair. |
| Light Mode / Dark Mode | Selects isolated draft and base theme; does not change user's app mode. | Rebuild from selected draft/base defaults; preserve tab state and 300 ms debounce. |
| Save Theme | Serializes draft settings for both modes subject to existing reset/default checks; shared store merges theme types, preserving Tables and Grouping. | Keep handler/store/API untouched. Preview options are derived and must never become saved chart-theme payload. |
| Reset | Replaces selected draft with mode defaults and `isReset: true`. Persistence occurs on Save Theme as `chartTheme: null`. | Keep handler untouched; do not reset application mode, opposite draft, Tables or Grouping. |
| Section collapse, color-picker popover/hex entry, font selection and weight dropdown | Existing administration controls and focus behavior belong to the form, outside the chart engine. Hex input forwards text without palette validation. | Keep components and labels unchanged. Handle invalid/unsupported preview inputs explicitly without altering stored text or disabling save. |

## Retained fields outside visible controls

`selectedBaseTheme` is read from storage and used by the preview, but no base-theme dropdown is currently rendered. `backgroundImage` metadata is serialized but deliberately excluded from the Community preview. Legacy `backgroundImage*` params are also filtered from preview options while retained by serialization. Do not add an image control, draw stored images, drop metadata or claim image support in this slice.

The plain-color picker cannot author image/gradient/pattern palette objects. Persisted runtime payloads can still contain them. The separate `advanced-palettes.md` boundary requires unchanged payload retention and an accessible unsupported-paint diagnostic. Native ECharts can represent some gradients/patterns, but that fact does not authorize accepting or coercing arbitrary existing object payloads. Do not stringify objects, supply fallback blue fills or silently change saved themes.

## Shared application semantics remain a separate boundary

Current `projectCallerTheme` explicitly projects font family/size/weight, text and subtitle colors, padding, chart background, axis and grid color. Foreground feeds color tokens, and borderColor only feeds navigator border. It does not project accent, chrome, input or crosshair parameters. Therefore a locally successful tooltip preview is not evidence that saved chrome settings affect all ordinary widgets. Repairing shared theme projection requires a separate scoped change and acceptance, including explicit style precedence and affected renderer coverage.

The existing caller is not a drop-in preview builder: it would newly activate `padding`, omit the exposed chrome effects and change parts of the fallback chain. Reuse stable lifecycle/rendering helpers where possible, while keeping preview-specific finite semantics explicit.

## Smallest production boundary and acceptance risks

1. Modify `ChartSettings.tsx` to replace only the preview element. Preserve `useChartSettings`, `ThemeSettingsLayout`, both control components and the debounce.
2. Modify `chartThemePreview.ts` to derive native options from exactly the retained sample and supported fields. Extract cohesive preview appearance/tooltip mapping only if required by caps or clarity. Avoid touching the shared application projection in this slice.
3. Reuse the existing `General/Table/Chart/echarts/EChartsHost.tsx` and its sole lifecycle owner. TP1 extends its typed legend and keyboard plans as specified in the reviewed contract; do not add a second preview lifecycle.
4. Update `tests/unit/chartThemeCommunity.test.ts` at the same boundary: sample values/series growth, palette pairs, explicit/default typography, tooltip chrome, absent image/crosshair and metadata retention. Existing forwarding assertions need native-option assertions; do not call forwarding visual parity.
5. Later extend/reuse `tests/e2e/live-chart/funnel-palette.spec.ts` for public admin save/reset/read-back and retained FMP Cone paint/export identity. Do not create a separate financial fixture or claim full cross-widget theme coverage from this one family.

Before acceptance, explicitly resolve these risks: AG keyboard focus/accessibility versus native ECharts; tooltip structure/hover targeting and primary/secondary text; overflow legend pagination and toggling; default color mixes; default 20 px padding and the owner-approved saved `padding` override, including zero; font fallback and title scaling; removed-series replacement; responsive resize, remount and disposal; invalid colors and advanced payload diagnostics. A bar-only screenshot does not establish these outcomes.

No control removal, disabled action, hidden flag, new toolbar, new animation or sample-data change is needed. The implementation handoff must carry 400 physical lines/file, 300 logical units/file and 50 logical units/function, with controller-owned maintained scope inventory/checker evidence. This report is documentation-only and outside production caps.
