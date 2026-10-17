# Nested editor capture: bounded contracts now observed

The focused original-runtime journey completed 18 UI actions without action failures. It closes selected axis, legend, column-label/stroke, line-marker and Set Up model contracts. It does not close the complete editor or approve application implementation. Review [patch-ledger.json](patch-ledger.json), [control-ledger.json](control-ledger.json), [domains.json](domains.json) and [verification.json](verification.json) before using these observations.

2026-10-17. Original owned source `38dffc33389aca0e4a87e0e88d42f7067aa220df`; unchanged image `sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f`. Debian WSL, Node 24.22.0, existing Playwright dependencies/cache, headless isolated contexts, disposable account/container/bind state. No install, build, production edit, owner browser or owner state. Research scripts are outside maintained production complexity caps.

## Selector root cause and bounded remediation

The previous class selector was correct. Its anchored text regular expression was wrong: the title-bar textContent contains leading and trailing whitespace, for example `   Horizontal Axis `. The successful probe retained the class and admitted surrounding whitespace. [selector-proof.json](selector-proof.json) derives the text from the observed DOM; it is not a source-code conjecture. Initial snapshots also require waiting for the editor/tab to render.

The first action run then exposed hidden numeric duplicates in collapsed groups, Size as a combobox, and the actual label Tooltip Mode. It was deliberately stopped instead of spending additional 30-second waits on absent controls. Its action failures, partial ledger, command exit 1 and browser-close exception are retained separately. The focused replay uses observed visible controls, exact roles and four-second action deadlines; it exited 0. It does not convert the stopped run into a pass.

Runtime acquisition is bounded to `.ag-root-wrapper` React parents (18 maximum), the named original `gridRef.current.api` or `child.stateNode.api`, then `getChartModels()` and `getChartRef(chartId).chart`. There is no arbitrary object graph search. Values are projected through finite scalar/array/field schemas, including explicit top/bottom/left/right axis branches. The projection preserves false, zero and null; unknown objects reject. JSON flattening runs offline over these already finite captures.

## Observed model and effective values

Paths below are relative to `model.chartOptions` unless stated otherwise. Each row has actual UI input, before/after model and effective-option evidence. `chartOptionsChanged` events are separately retained; the events are not invented from the resulting model.

| UI action | Observed model path/value | Effective result |
| --- | --- | --- |
| Horizontal Axis / Padding = 9 | `bar.axes.category.top.label.spacing` and `.bottom.label.spacing = 9` | Bottom category label spacing 9. The UI word Padding maps to spacing. |
| Horizontal Axis / Auto Rotate off | Same top/bottom namespaces, `label.autoRotate = false` | Bottom label autoRotate false. |
| Vertical Axis / first visible Thickness = 3 | `bar.axes.number.left/right.line.enabled = true`, `.width = 3` | Left number-axis line enabled, width 3. Grid Lines has a separate Thickness control. |
| Vertical Axis / Size = 14 | `bar.axes.number.left/right.label.fontSize = 14` | Left label fontSize 14. |
| Series / Labels on | `bar.series.label.enabled = true` | Both column series labels enabled; Font, Weight, Size and Color controls appear. Placement was not exposed in this fixture. |
| Series / Stroke Width = 3 | `bar.series.strokeWidth = 3` | Both column series stroke widths 3. |
| Legend / Weight = Bold | `bar.legend.item.label.fontWeight = "bold"`, `.fontStyle = "normal"` | Same effective values; two options events. |
| Legend / Size = 14 | `bar.legend.item.label.fontSize = 14` | Effective 14. |
| Legend / Marker Size = 15 | `bar.legend.item.marker.size = 15` | Effective 15. |
| Legend / Horizontal Spacing = 40 | `bar.legend.item.paddingX = 40` | Effective 40. |
| Aggregate on/off | Root `model.aggFunc = "sum"`, then absent | Effective rows become Q1 220/45, Q3 140/30, Q4 160/40; off restores four ordered source rows including duplicate Q1 values 100/20 and 120/25. |
| Switch Category / Series on/off | Root `model.switchCategorySeries = true/false` | On uses four series `period:0` through `period:3`, xKey `AG-GRID-DEFAULT-CATEGORY`; off restores revenue/operatingIncome. Transposed numeric row leaves were omitted by this fixture whitelist and remain unverified. |
| Line / Markers on | `line.series.marker.enabled = true` | Both line markers enabled; Shape, Size, Stroke Width become visible. |
| Line / Shape = Diamond; Size = 9 | `line.series.marker.shape = "diamond"`, `.size = 9` | Both series have those values. Inspected final screenshot shows diamond markers at the four original values. |

Tooltip Mode was successfully changed from Multiple to Single and emitted an options event. Its UI domain is Single/Multiple/Compact. The projection did not capture a changed leaf for this edit, so **the tooltip mode patch namespace/effective behavior is not frozen**. This is one of the 18 successful UI actions, not a proved renderer behavior.

Domains observed by opening actual menus: Weight = Predefined, Normal, Bold, Italic, Bold Italic; font Size = 8, 10, 11, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36; marker Shape = Square, Circle, Cross, Diamond, Plus, Triangle, Heart. Full control snapshots include number/range min/max/step, checked/disabled values, labels and tab text. Computed visibility does not certify every control was simultaneously within the scrolled viewport. Color text is present in panel text; color-picker domains were not explored.

Switching from edited groupedColumn to Line exposed default line controls and a `line` namespace. Do not generalize the observed reset to every family. No new stackedBar transition was executed.

## Rendering and persistence limits

The fixture units are USD millions. Aggregate 220 = 100 + 120 and 45 = 20 + 25 are independently asserted against effective chart data. The immediate aggregate screenshot has three categories but intermediate animation heights; it does not prove settled bar geometry. `waitForUpdate()` is not an animation-completion oracle. Final line screenshot visibly preserves 100/120/140/160 and 20/25/30/40 with diamond markers. No pixel-level geometry or typography acceptance is claimed.

One explicit Ctrl+Shift+S was issued at the end and one POST with the synthetic dashboard item was captured. [outgoing-storage-projection.json](outgoing-storage-projection.json) records the finite selected values: line type, series count 2, chartSettingsOpen, default model and enabled diamond markers size 9. This proves outgoing storage serialization for the final line state only. Backend response-body correctness, save/reload, other intermediate saves and persistence of all preceding edits remain unverified. Raw synthetic request bytes are omitted from publication in favor of this derivative.

The original datafeed HTML-as-JavaScript issue remains: two page errors and matching CDP exceptions `Unexpected token '<'`; no recorded CDP network loading failures. [diagnostic-summary.json](diagnostic-summary.json) is sanitized and does not certify a clean browser run.

## Reproduction, verification and cleanup

From repository root, using WSL Debian user mc:

```powershell
wsl -d Debian -u mc -- bash artifacts/parity/editor-runtime-next/run.sh
wsl -d Debian -u mc -- bash artifacts/parity/editor-runtime-next/rerun.sh
wsl -d Debian -u mc -- /mnt/d/Source/QOpenBB/artifacts/task-1.2/node-v24.22.0-linux-x64/bin/node /mnt/d/Source/QOpenBB/artifacts/parity/editor-runtime-next/stop.mjs
wsl -d Debian -u mc -- bash artifacts/parity/editor-runtime-next/focused.sh
wsl -d Debian -u mc -- /mnt/d/Source/QOpenBB/artifacts/task-1.2/node-v24.22.0-linux-x64/bin/node /mnt/d/Source/QOpenBB/artifacts/parity/editor-runtime-next/cleanup.mjs
wsl -d Debian -u mc -- /mnt/d/Source/QOpenBB/artifacts/task-1.2/node-v24.22.0-linux-x64/bin/node /mnt/d/Source/QOpenBB/artifacts/parity/editor-runtime-next/analyze.mjs
```

Executed order/results: discovery 0; initial action run intentionally stopped, recorded exit 1; focused replay 0; cleanup 0; offline analysis 0 with 22 assertions. Scripts do not reconstruct private credentials after cleanup; a fresh execution starts with start.mjs through run.sh and must use a fresh owned output/state directory if preserving this evidence. Do not rerun scripts over these reviewed outputs.

Cleanup validates the owned absolute state target under this lane, removes only the owned container/state/credential file and verifies their absence. No Node/Chromium process remained at queue handoff. The browser/heavy queue is free for the grid lane.

Publication uses [publication-allowlist.json](publication-allowlist.json), selected file hashes and explicit exclusions. Raw diagnostics, runtime/state locations, credentials, account databases and original outgoing request bytes are not publication candidates. The selected-leaf presence ledger describes only whitelisted projected leaves; an omitted branch is not proof that the original runtime lacks it.

Remaining gaps include root tooltip semantics, nested titles/color pickers/shadows, legend marker stroke and vertical/item spacing edits, axis type/position/grid/tick editing, complete aggregate function domain, numeric transpose output, reorder/category-range changes, stackedBar and other families, light/detached/forecast/keyboard paths, settled geometry and backend persistence. Independent review is required before accepting these bounded contracts; complete C and renderer parity remain gated.
