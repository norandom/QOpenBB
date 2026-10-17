# Original settled dark grouped-column reference

The real original chart's settled processed options are accessible for reference research. The chart instance proxy exposes `chart` through a prototype accessor, which an enumerable-only walk misses. This closes one default-dark grouped-column resolver observation; it does not establish light/custom/line/stacked behavior or replacement parity.

Capture dated 2026-10-17. Image `sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f` and Workspace label `38dffc33389aca0e4a87e0e88d42f7067aa220df` were verified before startup. The successful disposable container was `2d1db1cedd598fe81be677fc08d2fb4405031cb184404991309b940eb3b1a4a7`, bound only to `127.0.0.1:32769`; health returned 200. Original locked AG Charts is 12.1.1, Grid 34.1.1. No install/build/production edits or owner-state access occurred.

## Inputs and observed output

`fixture.json` supplies an ordinary table widget. Both series are explicitly labelled USD millions: Revenue 100/null/140/160 and Operating Income 20/null/30/40 for 2024-Q1 through Q4. Matching units are synthetic declared provenance for this fixture, not a claim that arbitrary production columns carry unit metadata. The runner checked displayed periods and revenue values, clicked the actual chart-view button, and used real Control+Shift+S. One selected-dashboard POST was captured; its chart model is groupedColumn with openbb-dark.

`resolved-dark-grouped-column.json` projects finite processed style leaves and retains the supplied theme. Selected results after `await proxy.waitForUpdate()`:

- Background `#151518`; padding 20 on every side.
- Title disabled, retained default text `Title`, Verdana size 12/weight 400/color `#fff`.
- Legend enabled/top, spacing 20/maxHeight 50, square marker size 11/padding 5, item paddingX 32/paddingY 8, Verdana size 11/color `#fff`.
- Bottom category and left number axis labels enabled, Verdana size 11/weight 400/color `#fff`; both axis titles disabled with retained `Axis Title`. Number grid enabled and category grid disabled, stroke `#515153`.
- Revenue first slot fill `#5090dc`/stroke `#74a8e6`; Operating Income second slot fill `#ffa03a`/stroke `#ffbe70`; both bar stroke widths 0 and labels disabled.

`chart-dark.png` was visually inspected: original widget shell, two legend items, grouped blue/orange columns, empty Q2 interval and dark axes/grid are visible. It is original-only reference evidence. No candidate comparison, export, reopen or restart persistence was tested.

## Inspector and execution evidence

First approach followed bounded enumerable React/DOM references (73,320 visits on final run). It found the real Grid API, stored model and `chartRef.current.chart` proxy, but no processedOptions. Second approach used the discovered proxy's public `waitForUpdate()` and inspected own/prototype descriptors. `chart` is a prototype accessor; reading it exposed the actual settled `chart.chartOptions.processedOptions`. That private read is reference-only and must never enter production. `getOptions()` remains supplied user options, not the resolver oracle.

The second approach initially failed JSON serialization because user options contain circular `context.beans`. This was corrected with a finite supplied-options projection and explicit cycle/function markers; `[reference]` and `[callback]` are serialization markers, not resolved style values. The same approach was rerun once, exited 0, and closed the browser in finally. `inspector-second.json` is private raw research and may include internal context; use only the finite resolved projection for durable summaries. Callback implementations remain pinned original source, not JSON-reconstructed code.

Initial launcher preparation hit unavailable Python aliases; switching to existing Node fixed preparation. Initial browser sign-in used an invalid hex-only password. Original login's zodPassword requires uppercase and special characters; that failure is retained as `login-policy-attempt*`. A fresh disposable state directory and policy-valid random credential corrected the cause. No credential, .env file or key was read or printed. Private disposable credential/state files must not be published.

Runner: existing Node 24.22.0 under `artifacts/task-1.2`, existing verification Playwright 1.64 import, installed Chromium headless-shell 1248, one context at 1440x1000, CDP Runtime/Network enabled, external origins blocked. Fixed PATH was `/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin`.

```powershell
wsl -e bash -lc 'export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin; cd /mnt/d/Source/QOpenBB && PLAYWRIGHT_BROWSERS_PATH=/mnt/d/Source/QOpenBB/artifacts/playwright-browsers artifacts/task-1.2/node-v24.22.0-linux-x64/bin/node artifacts/parity/theme-contract-capture/journey.mjs'
```

Final runner exit 0. `hashes.json` pins inputs, scripts, screenshot, write payload, finite output and diagnostics. Final diagnostics retain two original `Unexpected token '<'` page errors with CDP exceptions; this is not a clean diagnostics claim. Cleanup `docker rm -f` against the exact owned container ID returned that ID successfully. A post-run process check found no matching runner/profile processes. The earlier invalid-password container was also removed by its exact owned ID. Disposable artifact state remains private.

Next bounded work can reuse this discovered accessor to capture the previously planned 12 stock/custom light/dark/family cases, recording mode and exact input overrides per case. It has not run here. The production bridge still requires an audited finite rule set and public ECharts implementation, not AG's private resolver.
