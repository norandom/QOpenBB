# Actual Workspace chart checkpoint

The ordinary CSV-to-chart journey now passes against Full Workspace and a disposable SQLite backend. This accepts a browser checkpoint, not task 2.77 or deployment readiness. Continue with filtered/sorted data, unknown-branch preservation and the remaining visual comparison.

On 2026-10-18, one headless Playwright worker passed the maintained `terminalpro/tests/e2e/live-chart/application.spec.ts` in 78.3 seconds, with zero retries, skipped or unexpected tests. Workspace production source was `07d214dafdcf4097dbe1a2d741c407785f7e73cf`, plus the test helpers delivered with this record. Backend image `sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f` used the 43-file API source overlay `23b6323e40a2edaa7267e25f72d032da8e92ccef09cc09545cb749fe2d2a15de`. This is development evidence; the release image is not verified.

The actual application imported Category A/B/C, Revenue 10/20/30 and Cost 4/8/12. Grouped Column, Stacked Column and Line title edits reached canvas drawing. Set Up selected the category column. Representative padding, legend, tooltip, series, labels, markers/shadow and axis edits reached the original saved leaves. Their values survived a fresh authenticated context and an owned backend restart. A deliberately rejected save retained edits; retry succeeded. PNG downloaded and the widget returned to its original table.

The [light](line-light.png) and [dark](line-dark.png) views show deliberately edited settings, not default styling. The controller also inspected the [exported PNG](saved-ordinary-observations.png): its title and six values match the saved chart. Automated PNG checks cover format and dimensions; they do not independently compare image freshness. Saved-control assertions do not prove every styling effect.

## Reproduce this checkpoint

Use the existing WSL toolchain and an owned runtime created by `tests/delivery/workspace_runtime.py`. The runtime requires an explicit loopback frontend origin and chooses an explicit backend port so Docker restart cannot reassign it. Credentials remain in a mode-0600 descriptor outside the repository. Start Vite with `tests/e2e/live-chart/vite.config.ts`, setting `WORKSPACE_BACKEND_ORIGIN`, `WORKSPACE_FRONTEND_PORT` and an isolated `WORKSPACE_VITE_CACHE`; this configuration does not load operator environment files.

From the repository root, set `QOPENBB_PLAYWRIGHT_PACKAGE` to `verification/node_modules/@playwright/test`, `PLAYWRIGHT_BROWSERS_PATH` to `artifacts/playwright-browsers`, `WORKSPACE_RUNTIME_PRIVATE` to the disposable descriptor, `WORKSPACE_RUNTIME_PYTHON` to the WSL interpreter, `WORKSPACE_FRONTEND_ORIGIN` to the owned frontend and `WORKSPACE_EVIDENCE_ROOT` to an ignored artifact directory. Run:

```sh
artifacts/task-1.2/node-v24.22.0-linux-x64/bin/node verification/node_modules/@playwright/test/cli.js test --config vendor/workspace/terminalpro/tests/e2e/live-chart/playwright.config.ts
```

Scoped Biome lint passed for all 11 browser files. Python compilation and independent AST parsing passed for the runtime helper. These files are test infrastructure and exempt from production size caps; no production file changed in this checkpoint.

## Independent review and limits

Fresh-context reviewer `/root/join_browser_review` (`gpt-6-astra`) approved this bounded checkpoint after inspecting the source, completed browser report and screenshots. It independently checked Python syntax and fork whitespace. RED is not applicable to this test-only delivery; the separately committed dashboard-save repair has its own regression evidence.

No uncaught page error occurred. Diagnostics admitted only the intentional save HTTP 500 and the existing missing TradingView datafeed asset HTTP 404 with its associated aborted request. The missing asset remains disclosed; it was not stubbed into a successful response.

Task 2.77 remains open. Filtered/sorted chart data, unknown saved branches, broader rendered effects and original/replacement visual comparison still need evidence. Original numeric-rotation/Auto Rotate and structural-axis restore limitations remain. UI-10 through UI-16 and release acceptance remain pending. A mismatch between saved settings and the reopened chart would invalidate the relevant checkpoint claim.
