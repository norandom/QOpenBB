# Stock original theme matrix findings

All six stock cases, dark/light by grouped-column/stacked-column/line, now have verified original models, finite effective options and screenshots from actual UI transitions. This advances discovery for requirements 4.8 and 4.9; it does not freeze the renderer contract or establish candidate parity.

On 2026-10-17 the reference used original source `38dffc33389aca0e4a87e0e88d42f7067aa220df` and image `sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f`, with a disposable account/state, loopback runtime and isolated headless WSL browser at 1440x1000. Both synthetic series are USD millions. The fixture includes a null Q2 interval and checks the displayed table before chart entry.

Each captured model is checked against the chosen family/theme, and each replacement chart proxy is reacquired before public `waitForUpdate()` and a reference-only `processedOptions` projection. Real Chart settings thumbnails and explicit dashboard saves produce the model transition evidence. Dashboard GET overlays mean this run cannot establish backend save/reopen persistence.

The previous unattributed `Unexpected token '<'` error is caused by the original `/assets/js/datafeeds/udf/dist/bundle.js` script route returning HTTP200 `text/html`. CDP identifies a JavaScript SyntaxError at line0 on that route; no parse-time call stack is available. Retain this as an original defect rather than a clean acceptance result.

Ignored local evidence and exact commands live in `artifacts/parity/theme-matrix/report.md`, with per-case model/effective JSON, screenshots, diagnostics, saved-widget writes and SHA-256 manifest. `first-pass/` retains the three dark cases and the Settings role mismatch failure. The actual Settings entry is a link; selecting it as a menuitem timed out. The later data-probe failure is retained separately: raw chart series data contained circular context, so the final probe selects only the three known fixture fields.

A suspected missing Q1 bar was a visual reading error. Exact pixel samples and a Q1 blue bounding box, pinned to image hashes in pixel-probe.json, show #5090dc at the expected Q1 Revenue100 bar in both initial and delayed images. Grid rows and public chart data agree. No missing-bar defect is established.

The final runner exited0. Dark stacked/line evidence belongs to the first pass, whose later Settings selector failed; the final pass supplies dark grouped plus all three light cases. The artifact report maps each case to its attempt. Delayed screenshots after toast dismissal exist for the final-pass cases. Chart-panel state differs by family and must be considered when comparing geometry. Exact-name container/process checks are empty, and disposable credentials/state were removed.

Both themes retain blue/orange fills, with mode-specific bar strokes and backgrounds. Line defaults connect missing data, use width2, and retain disabled size7 circle markers. All six retain disabled Title text and a top legend. These observed defaults belong to the pinned original fixture/runtime. Custom themes, expanded controls, exports, backend reopen and candidate parity remain unverified.
