# Stock theme matrix capture

Original-reference research, 2026-10-17. This evidence observes original rendering; it establishes no candidate parity, backend save/reopen persistence, custom-theme contract or export behavior.

The source is `38dffc33389aca0e4a87e0e88d42f7067aa220df`, image `sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f`. Each runnable attempt verifies image labels, creates disposable state/account and a loopback-only container, and uses the existing headless Playwright Chromium in Debian WSL at 1440x1000. No builds or installs occurred. Explicit fixture values are Revenue 100/null/140/160 and Operating Income 20/null/30/40, both USD millions, for 2024-Q1 through Q4.

## Commands and attempts

All commands started in `D:/Source/QOpenBB`. Final runner command: `wsl -d Debian bash artifacts/parity/theme-matrix/run.sh`. The launcher sets the pinned Node path and `PLAYWRIGHT_BROWSERS_PATH=/mnt/d/Source/QOpenBB/artifacts/playwright-browsers`. Both scripts redirect output to this directory; the shell EXIT trap removes only the exact owned container and disposable credential file.

Preparation initially failed because Windows `python` was an unavailable Store alias, default WSL lacked python3, and the first generated shell had CRLF. Windows `py` successfully prepared files and normalized LF. Debian-MW then failed before container creation because Docker was unavailable. Debian provided Docker, but the first browser run failed because its default home-cache browser was absent. The prior reference report supplied the existing project-local browser cache. These failures installed nothing.

The first matrix pass exited 1 after successfully capturing three dark families: Settings was incorrectly selected as role menuitem. Source inspection established that the real Settings entry is an anchor with role link. The corrected second pass retains that actual UI transition. `first-pass/` preserves the failed journey log and output diagnostics.

## Observation contract

Each case verifies the actual Grid chart model family and `openbb-dark` or `openbb-light` theme before projecting effective options and taking screenshots. Family changes click the real Chart-panel thumbnail; the proxy is reacquired after replacement and its public `waitForUpdate()` awaited. The private `chart.chartOptions.processedOptions` read is reference-only. Finite projections contain titles, legend, axes/grid, series colors/markers, padding/background and supplied theme. Callbacks serialize to markers.

The screenshot panel state affects chart geometry: grouped baseline has its settings panel closed; subsequent family cases leave the Chart tab open. Do not compare plot widths without accounting for that state. Save commands produce selected-dashboard POST evidence, while GET dashboard route overlays supply the fixture. This is explicitly not persistence evidence.

## Diagnostics

The original `Unexpected token '<'` errors are now attributable to `/assets/js/datafeeds/udf/dist/bundle.js`: HTTP 200 serves `text/html`, then the browser rejects `<` as JavaScript at line 0. CDP reports SyntaxError and the script URL/ID; a parse-time call stack is unavailable. An initial onboarding-info request also returns JSON 404. These original defects are retained, not declared clean diagnostics.

An initial visual reading incorrectly suggested that the grouped screenshot omitted the Q1 blue revenue bar. The dark line case later starts at Revenue100. That visual reading was incorrect: pixel-probe.json records the Q1 bar bounding box and exact #5090dc pixels in both initial and delayed images. Grid rows and public input data both contain Revenue100. The Q1 bar is present; no missing-bar defect is established.

## Final result and case mapping

Six of six requested stock cases have verified original model/effective JSON and screenshots. Final runner exited 0. No stock case is missing. The intermediate stability probe exited 1 because raw per-series data exposed circular context; final projection selects only explicit fixture fields and exits 0.

| Case | Authoritative JSON/screenshot prefix | Attempt | Panel |
| --- | --- | --- | --- |
| dark groupedColumn | `dark-groupedColumn` | final pass | closed |
| dark stackedColumn | `first-pass/dark-stackedColumn` | first matrix pass, runner exited1 later | Chart open |
| dark line | `first-pass/dark-line` | first matrix pass, runner exited1 later | Chart open |
| light groupedColumn | `light-groupedColumn` | final pass | closed |
| light stackedColumn | `light-stackedColumn` | final pass | Chart open |
| light line | `light-line` | final pass | Chart open |

Final-pass cases include a second delayed `-stable.png` after actual Confirm toast dismissal, 1.5 seconds apart. This is a finite stability observation; animation completion is not independently instrumented. The chart-view tooltip remains in grouped screenshots. First-pass dark family screenshots retain save toasts. No claim of identical panel geometry across families is made.

Both modes retain blue/orange fills #5090dc/#ffa03a. Dark bar strokes are #74a8e6/#ffbe70; light bar strokes are #2b5c95/#cc6f10. Bar stroke width is0. Background is #151518 dark and #FFFFFF light. Both line cases have width2, connectMissingData=true, and disabled circle markers retaining size7. All six retain disabled Title text and a top legend. Refer to JSON for exact finite leaves, not inferred defaults.

The final EXIT trap removed the exact owned container; a subsequent exact-name Docker listing was empty. The runner process listing was empty (grep exit1). browser.close() ran in finally. The disposable credential file and all owned bind-state directories were removed. See cleanup-report.json. No operator application, browser, environment credential or provider account was accessed.

Custom-theme cases, editor/control expansion, exports, backend reopen and candidate parity remain unverified. Production code and runtime dependencies were not changed. Research artifact scripts are outside maintained production complexity scope; no production checker acceptance is claimed.
