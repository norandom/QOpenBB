# Original line editor capture

Original UI actions emitted selected-dashboard POSTs for a line chart, a disabled title with retained text, the same enabled title, and enabled markers. The default line visibly spans the interior null observation without point markers. This is observed UI and outgoing-state evidence; no resolved AG options were extracted.

Runtime on 2026-10-17: original image `sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f`, source label `38dffc33389aca0e4a87e0e88d42f7067aa220df`. New owned container `qopenbb-line-style-capture-20261017` used loopback port 32768 and disposable bind state under `state/`. Image/source identity and HTTP health 200 were checked. No owner state, real.env, frontend overlay, image build or dependency installation was used.

## Finite observations

`observations.json` preserves four periods and numeric observations: revenue 100/null/140/160 and EPS 1.2/null/1.6/1.8. The table displayed all periods and non-null revenue values before the real chart-view button was used. Synthetic financial-data GET responses supplied these exact numbers/nulls. Dashboard GET routes supplied the synthetic fixture; outgoing writes were captured only for dashboard `11111111-1111-4111-8111-111111111111`. No application store or internal handler was invoked.

All paths below start at the selected dashboard item. See `widget-writes.json` and `payload-deltas.json`.

| Actual UI action | Outgoing result |
| --- | --- |
| Select Line in Chart settings | `data.widgets.0.storage.chartType` and `data.widgets.0.storage.default.chartModel.chartType` become `line`. |
| Enable title, type text, disable title | `data.widgets.0.storage.default.chartModel.chartOptions.line.title.text="Synthetic line retained title"`; sibling `enabled=false`. |
| Enable title again | Only sibling `enabled` changes to true; text remains unchanged. |
| Enable Markers in Series | `data.widgets.0.storage.default.chartModel.chartOptions.line.series.marker.enabled=true`; enabled title and text remain. |

`line-default.png` shows blue/orange lines spanning Q2 with no point markers. `title-disabled-retained.png` has no drawn chart title; `title-enabled.png` draws the retained title. `markers-toggled.png` draws markers at Q1, Q3 and Q4, with none at null Q2. The visible enabled marker controls show Shape Circle and Size 7. These are editor/display observations, not a claim about fully resolved marker fill, stroke or inherited options.

The opened Series DOM lists Tooltips, Tooltip Mode, Line Width, Line Dash, Line Opacity, Markers and Labels; it exposes no Connect Missing Data label/control (`line-series-default.html/.json`, `connect-missing-unavailable.txt`). One unique-checkbox query found zero. No second speculative attempt or injected toggle was used. Source discovery already identifies the explicit application default `line.series.connectMissingData=true` in original `Chart/themes.tsx`; the screenshot is consistent with it. A user toggle payload and false-state drawing remain unobserved. Light mode was not explored; the bounded capture stayed on the actual default dark theme.

## Execution and limits

Command: WSL `PLAYWRIGHT_BROWSERS_PATH=/mnt/d/Source/QOpenBB/artifacts/playwright-browsers artifacts/task-1.2/node-v24.22.0-linux-x64/bin/node artifacts/parity/line-style-capture/journey.mjs`, importing root verification Playwright 1.64. One isolated headless Chromium/context at 1440x1000 ran with CDP Runtime and Network enabled; external origins were blocked. Disposable credentials were read programmatically and never output. Browser closure ran in `finally`; runner exit 0. Each stage used the real product Control+Shift+S and collected one matching POST after ten seconds; no timer fallback ran. Scripts, DOM snapshots, screenshots, sanitized diagnostics and deltas are in this directory.

Diagnostics are not clean: the known original `Unexpected token '<'` page error occurred twice with corresponding CDP exceptions. Initial disposable onboarding also returned 404 for `/api/pro/pro-developer-onboarding-info`, followed by 200 later; console errors are preserved. No save/restart/reopen or backend persistence proof was attempted. JSON captures cannot establish runtime callbacks, effective theme inheritance, AG resolved option precedence or renderer parity.

Cleanup removed only owned container `qopenbb-line-style-capture-20261017` with `docker rm -f`; exit 0. The browser/runner finished normally. Private disposable `state/` remains ignored and must not be published. No production or specification files were changed.
