# Original editor outgoing payload capture

Actual original UI edits emitted seven selected synthetic-dashboard POST payloads. `widget-writes.json` preserves only dashboard `11111111-1111-4111-8111-111111111111`; `payload-deltas.json` compares consecutive records, including deletions. No credentials, headers, cookies or other dashboards are recorded in these payload artifacts.

Original image: `sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f`. Workspace source label: `38dffc33389aca0e4a87e0e88d42f7067aa220df`. No frontend overlay was used. Dashboard GET and synthetic financial-data routes were overlaid with the fixture, and external origins were blocked. State was new and disposable. The UI displayed 2024-Q1/2024-Q2, revenue 100/120 and EPS 1.20/1.40 before chart interaction.

## Observed outgoing fields

All paths below start at the selected dashboard item. Edits were sequential, with a save between each change, so each delta isolates that control against the immediately preceding saved state.

| UI stage | Payload result |
| --- | --- |
| Chart toggle baseline | `data.widgets[0].storage.chartView.enabled=true`; `storage.chartType` and `storage.default.chartModel.chartType` are `groupedColumn`. |
| Enable Chart Title, type Synthetic Revenue and EPS | `storage.default.chartModel.chartOptions.bar.title.text="Synthetic Revenue and EPS"` and `.enabled=true`; `storage.chartSettingsOpen=true` also appears after opening settings. |
| Legend Position Bottom | `storage.default.chartModel.chartOptions.bar.legend.position="bottom"`. |
| Stroke Width 4 | `storage.default.chartModel.chartOptions.bar.series.strokeWidth=4`. |
| Stacked Column | Both `storage.chartType` and `storage.default.chartModel.chartType` change to `stackedColumn`. |
| Grouped Column | Both chart-type fields change back to `groupedColumn`. |
| Line | Both chart-type fields change to `line`. |

The edited `chartOptions.bar` title, legend and stroke leaves remain present and unchanged across stacked, grouped and line outgoing payloads. No leaf removal was observed. This proves retained outgoing state, not effective styling for each family. The final line Titles/Legend panel observations are in `line-titles.*` and `line-legend.*`; earlier grouped-column edited observations are in their named per-control artifacts. Runtime formatter callbacks and effective common-option reconstruction cannot be inferred from JSON.

## Execution and limits

The successful command was WSL, with `PLAYWRIGHT_BROWSERS_PATH=/mnt/d/Source/QOpenBB/artifacts/playwright-browsers`, pinned `artifacts/task-1.2/node-v24.22.0-linux-x64/bin/node`, and `journey.mjs`; the runner imports Playwright from `verification/node_modules/@playwright/test/index.mjs` (1.64). One isolated headless browser/context ran. CDP Runtime/Network diagnostics were enabled. Browser closure executed in `finally`. Exit code was 0. `run.log` records one matching write at each stage; no timer fallback was required on the successful run.

Each save used the product's real Control+Shift+S keyboard shortcut and waited ten seconds for collection. The response log records `/api/pro/dash/sync` responses with HTTP 200. The logger did not attach method/stage to response records, so these statuses are supplementary evidence only. No save/restart/reopen was performed, and no backend persistence claim follows. The known original HTML-as-JavaScript `Unexpected token '<'` exception occurred twice and is retained in sanitized diagnostics.

The initial timer attempt was stopped after baseline activity. A subsequent shortcut attempt exposed a success-toast overlay blocking the chart-menu pointer click; `shortcut-toast-attempt.log` preserves that failure. The successful run opened the same actual menu with keyboard focus and Enter. No application-store mutation or internal handler invocation was used.

Owned container `qopenbb-editor-payload-capture-20261016` used loopback ephemeral port 32778 and was removed after completion. Only owned browser/runner processes were stopped. Disposable private state remains under ignored `state/` and must not be published. These are research artifacts, not maintained application tests or acceptance of renderer parity.
