# Original chart options: integration findings

Preserve original saved option branches and resolve their effective meaning before connecting the replacement renderer. Seven original editor saves now establish the title, legend and stroke field paths. They do not establish full visual parity or persistence after reopening.

## Evidence and scope

Discovery date: 2026-10-16. Original Workspace source: `38dffc33389aca0e4a87e0e88d42f7067aa220df`; current fork: `06fdb859bf426eb44dce13c54b21c494fcc244fd`. Two GPT-6.1 Sol lanes separately inspected source and exercised the original editor. The controller joined their findings using kiro-spec-design and the project's COBESY documentation policy.

Local research evidence: `artifacts/parity/editor-payload-capture/report.md`, `widget-writes.json`, `payload-deltas.json` and `diagnostics.json`. Original image: `sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f`. One isolated headless browser used synthetic financial data and a disposable dashboard. No frontend overlay or application-store mutation was used; fixture dashboard GET and data routes were overlaid. The actual Control+Shift+S save shortcut emitted each captured POST.

The successful run exited zero. Response logs include HTTP 200 but lack method/stage correlation. Two original HTML-as-JavaScript exceptions remain in diagnostics. The owned browser and container were removed. Private disposable state is excluded from publication. These artifacts are research, not maintained regression tests.

Captured evidence SHA-256: `widget-writes.json` is `038b51a8cab49352da8edc978b30519e3c88e2a285b35ed41fb578d563069017`; `payload-deltas.json` is `237aa77c3ec40c1309a64110c55271fdf33e448fac258d3686968903383f6d0e`.

Independent GPT-6 Astra review found the research supported with no blocking corrections. It recomputed consecutive payload changes, confirmed zero removed leaves and checked source contracts and current mapper limitations. Review record: `artifacts/parity/editor-payload-review.md`. This is a research review, not design approval or implementation acceptance.

## Saved fields established by actual UI edits

Option paths below are relative to the selected widget's `storage.default.chartModel.chartOptions`. The family-selection row uses widget-relative storage paths.

| Control | Observed saved fields |
| --- | --- |
| Enable title and enter text | `bar.title.enabled=true`, `bar.title.text="Synthetic Revenue and EPS"` |
| Legend position | `bar.legend.position="bottom"` |
| Stroke width | `bar.series.strokeWidth=4` |
| Stacked, grouped, then line selection | Both `storage.chartType` and `storage.default.chartModel.chartType` change |

All edited `bar` leaves remain stored across the three family selections; deletion-aware payload comparison found no removal. Retained bar settings do not imply that a line chart renders them. Enabled/text separation and family-specific settings must survive subsequent edits and saved-state round trips.

## Source-owned resolution rules

Paths here are relative to `terminalpro/src/` at the original source revision.

| Boundary | Observed behavior | Integration consequence |
| --- | --- | --- |
| `components/General/Table/Chart/hooks/useChartOptions.tsx:307` | Options start from partition model options, then root `storage.chartOptions`, then empty object | Do not substitute root `storage.chartModel.chartOptions` as the fallback |
| Same file, line 326 | A nonempty partition model replaces options/model references | Capture the selected partition with its model |
| Same file, line 431 | Generated `common` replaces saved `common` before lodash merge | Plain saved-option decoding cannot reproduce the effective result |
| Same file, line 436 | Integrated edits merge into cloned options, remove root theme and preserve other model fields | Reuse the accepted integrated state reducer |
| `components/General/Table/AgChartFromTable.tsx` | Detached edits replace root options | Retain the distinct detached reducer semantics |
| `components/General/Table/hooks/useUpdateColumnState.ts:84` | Destination-family range takes precedence over current model range | Resolve the destination range before family-change reduction |
| `lib/constants.ts::CHART_TYPE_TO_SERIES_TYPE` | Grouped/stacked column models use the `bar` branch; line uses `line` | Model type and option namespace are different concepts |
| `components/General/Table/Chart/themes.tsx:179` | Original line defaults connect missing data and disable markers | Add explicit resolved behavior before original application adoption |

JSON cannot preserve runtime formatter callbacks. Axis formatting, fiscal dates, custom palettes, distinct-category fills, tooltips and generated labels also depend on source context. Their effective precedence still needs focused source/runtime fixtures; the outgoing payload capture does not certify it.

## Proposed next boundary

Separate two responsibilities while retaining the accepted state reducers and immutable snapshots:

1. A pure original-options resolver combines captured storage address/model, original option baseline, generated defaults and explicit theme/formatting context. Its result records resolved semantics and unsupported settings. Preserve original merge ordering without mutating caller input.
2. A typed editor-event mapper creates original option patches and passes them to the existing integrated or detached reducer. Destination range and family selection remain explicit inputs.

This is a boundary proposal, not an approved implementation design. It adds no service or general chart framework. ECharts remains the renderer; existing OpenBB control primitives and storage remain the integration targets.

The current `ResolvedCartesianStyle` is insufficient for original adoption: it conflates fill/stroke, has no independent title enablement, and lacks separate axis/title/legend typography and original formatting context. Its isolated line mapping intentionally leaves missing values as gaps. That accepted fixture behavior must stay covered while a separately specified missing-data/marker contract adds original theme semantics. Silently changing the existing default would conceal a compatibility regression.

## Conditions for an executable design

The next design must freeze precedence, explicit inputs, output types and unsupported-setting diagnostics before parallel implementation. It must identify which editor controls it covers and keep broader application activation gated until every existing enabled path works. Do not hide or disable remaining controls to obtain a passing slice.

Initialization and later partition changes need distinct contracts: the original references refresh only for nonempty partition models. An absent or empty destination partition can retain the earlier baseline. A stateless resolver that silently resets it would change behavior; make the prior baseline and transition explicit where required.

Required checks include storage fallback/partition changes; generated-common replacement with family retention; lodash null/undefined/array semantics; immutable inputs and unknown-field retention; detached replacement; destination-family range; separate enabled/text and fill/stroke; stable series identity; explicit line missing-data/marker semantics. Effective palette and formatting claims require their own fixtures, not only outgoing JSON.

Every changed production file must pass the existing inventory/checker at 400 physical lines, 300 logical units and 50 per function. Controller ownership covers shared contracts and mapper expansion; disjoint resolver and editor lanes can fan out only after contracts and task boundaries are approved. Existing 124 unit and three browser checks remain evidence for the preceding slice, not these proposed additions.

Full editor/theme parity, grid capture, transformed data, save/restart/reopen and SQLite repair remain open. See [prior grid and persistence findings](chart-next-discovery.md) and [accepted snapshot evidence](chart-snapshot-verification.md).
