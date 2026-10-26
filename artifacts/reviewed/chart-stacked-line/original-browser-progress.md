# Original Stacked Line browser progress

2026-10-26. Both original gallery variants activate on the native Table/File route and retain their exact model tokens and selected columns after save/reload. Financial, discriminator and controls characterization now covers six original cases. SL0 awaits final independent review; no replacement implementation or candidate acceptance is established.

## Reproducible scope

Reviewed retained observations and PNGs from `native-financial-1`, `native-discriminator-1` and `native-controls-1` beneath this directory. Runtime image: `sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f`; original frontend source: `38dffc33389aca0e4a87e0e88d42f7067aa220df`. Runtime identity declares a backend-only source overlay hash `23b6323e40a2edaa7267e25f72d032da8e92ccef09cc09545cb749fe2d2a15de`, `packaged_image_only:false` and `release_image_verified:false`. These are original diagnostic runs, not candidate or release gates.

Commands are retained in each run's `command.txt`: `node verification/node_modules/@playwright/test/cli.js test --config vendor/workspace/terminalpro/tests/e2e/live-chart/playwright.config.ts stacked-line-original.spec.ts --grep` with the respective `financial characterization` or `discriminator characterization` filter. Both exit codes are 0, with two cases passing on one worker; financial duration 52.6 seconds, discriminator 1.2 minutes. A passing observation probe does not assert numerical geometry.

Frozen runner SHA-256: `5188ec846d2bdc7be4c7be9457d796ce89c4c5327a44e8f9bc6ef4ec70286586`. Frozen financial test: `f64a362f910e0275a4d9077092db218d1f89b753912c099a3f14ea9693614955`; discriminator test: `53953ef33712cda496d0d0653d69f3f1910246396df414c97cf9541686b8563a`. Each run retains `frozen-source-hashes.sha256`, `test-source-hashes.sha256`, source copies, command, runtime/reference identity, observations, PNGs and exit/log files.

Both variants in both runs retain original diagnostic errors: two `Unexpected token '<'` page errors and two `net::ERR_FAILED` CSV resource/request failures for their `/api/pro/files/<id>.csv` path. Their diagnostics `failures` arrays are empty. Visible data and restored charts do not erase those errors or establish a clean runtime.

## Retained financial input and visible result

Both financial models select `[Fiscal quarter, Cost of revenue (USD), Gross profit (USD)]` in that order, with exact `chartType` `stackedLine` or `normalizedLine`, `openbb-dark`, `switchCategorySeries:false`, and AG Grid model version `34.1.1`. Before/after persistence records preserve those tokens, selected fields and the saved `line.legend.enabled:true` option; chart IDs are regenerated. This establishes those fields across the recorded save/reload, not universal saved-leaf correctness.

CSV SHA-256 is `ca76bb6fedb7a45709b050bc810c57784ac5543b42120b341b9db0690201331b`. The separately reviewed retained raw input gives cost/gross pairs USD: Q1 66.025/58.275 billion, Q2 50.492/44.867 billion, Q3 50.318/43.718 billion, Q4 54.125/48.341 billion. Their expected cumulative second levels are 124.300, 95.359, 94.036 and 102.466 billion. These are arithmetic/source expectations, not pixel measurements. The visible table rounds each raw component to two decimals in billions and matches that input.

The normalized screenshots show two legend entries, quarterly categories, percent ticks from 50% to 100%, an orange upper line at 100% and a blue line near 53%. The ordinary stacked screenshots show two similarly ordered lines and number ticks labelled 40.00 B through 140.00 B. Their ordering and approximate first-quarter levels are consistent with a positive additive stack: the controller's direct image reading places Q1 blue near 66 B and orange near 124 B against those ticks. An initial visual estimate in this review misread the tick positions and was discarded. No calibrated cumulative pixel proof is claimed for either variant. Selected and reloaded screenshots preserve the same visible shape.

The financial run records 12 attempted tooltip probes per snapshot for both variants, all `No visible tooltip within 180ms`. There are no financial tooltip hits; the sampled public draw calls included axis paths, so no-hit does not prove tooltip absence.

The two selected financial PNGs were inspected with `view_image`. They contain a chart crop, public FMP field labels, fiscal quarters, axes and a generic chart title; no credentials, private identity or unrelated desktop content is visible. Suitable for publication as explicitly labelled original diagnostic samples, subject to the numerical limit above:

- Normalized: `native-financial-1/browser-output/stacked-line-original-orig-36991--financial-characterization/selected-two-series.png`, SHA-256 `1f9d2f7047b63f6efe718d37964553d0850742cee64fd016e3e9e9e57467a5a0`.
- Stacked: `native-financial-1/browser-output/stacked-line-original-orig-df66f--financial-characterization/selected-two-series.png`, SHA-256 `e320d82221a6a354c2eb5f2784e4999ef798306dae4013b7dbb1f4f923d22898`.

## Discriminator and control observations

The discriminator selects `[Category, Primary, Secondary]`; rows are Positive `(60,40)`, Mixed `(60,-80)`, Cancel `(60,-60)`, Negative `(-30,-70)`, Zero `(0,0)`, Missing `(blank,20)`, After `(20,30)`. Exact variant tokens and selected columns persist after reload. Screenshots display signed lines, negative ticks and a straight visible connection across some missing/zero positions; they do not distinguish a genuine node from interpolation. CSV blank typing and cumulative coordinates still require an explicit contract.

The revised discriminator tooltip sweep successfully displays raw pairs for Positive, Mixed, Cancel, Negative and After, and Secondary 20 for Missing, in both variants. Stacked additionally displays both raw zero values at Zero. No normalized Zero tooltip was recorded. These tooltip observations support raw-value display, including normalized Line's Mixed raw Secondary -80; they do not establish normalized plotted endpoint values or an absent zero node. Reloaded observations repeat these raw strings.

The financial and discriminator runs expose Chart / Set Up / Customize, both checked legend item switches, and zoom controls. Captured Customize sections expose title/subtitle/axis-title toggles; Series tooltips enabled with Multiple mode, Line Width 2, Line Dash 0, Line Opacity 1, Markers and Labels unchecked; and Legend enabled, Verdana font, size 11, top position, spacing and marker controls. This inventories reachable controls, not successful edits. The follow-up below resolves native Connect Missing Data availability and exercises legend/order changes.

## Bounded controls follow-up

`native-controls-1` completed two cases on one worker in 56.1 seconds, exit 0. Its command uses the same Playwright invocation above with `controls characterization`; frozen test SHA-256 is `3048b8e00ab011677c1d4938a510077d93dd9904c8ebfdb6d5061502f624362d`, with the same runner hash. Both `controls.json` files retain five records: initial, secondary-hidden, secondary-restored, reordered and reloaded. Both retain the same two page errors and CSV request/resource failures described above; no clean-original-runtime claim follows from exit 0.

The hidden record changes the Secondary legend switch from checked to unchecked while retaining `[Category, Primary, Secondary]` in the model range. Restoring it returns both switches to checked. Viewed PNGs show only Primary while Secondary is hidden: ordinary ticks contract to -40 through 60; normalized Primary reaches positive/negative 100% and Secondary is dimmed in the legend. This visibly demonstrates legend-dependent redraw; it does not calibrate every coordinate.

Native Set Up reorder selects Secondary before Primary. Both reordered models become `[Category, Secondary, Primary]`, and accessible legend order changes to Secondary then Primary. Viewed reordered PNGs show Secondary as the first blue line and Primary as the orange cumulative line, with materially changed normalized intermediate levels. Reload preserves the reordered `cellRange` and entire `chartOptions` exactly; both persistence records declare exact token, `cellRangeEqual:true` and `chartOptionsEqual:true`. Series order and visibility are therefore observed rather than outstanding probes.

Neither original Series panel offers a checkbox or switch labelled Connect Missing Data. The probe records `offered:false` and does not inject engine state. Crucially, original Workspace `38dffc33389aca0e4a87e0e88d42f7067aa220df`, `terminalpro/src/components/General/Table/Chart/themes.tsx:173`, sets `line.series.connectMissingData:true` and markers disabled. This was independently read from `git show`. The library's false default in the source report is not the effective Workspace theme. Interpret these visible missing-span observations under the theme override; an unavailable native toggle is an observed limitation, not an unfinished toggle test.

The bounded original characterization is ready for final independent review and contract decisions. Keep SL0 pending that review. Raw tooltip versus plotted-coordinate meaning and normalized zero/missing observations retain the limits above; duplicate-category and continuous/time-axis cases remain explicit scope boundaries. These six passing original observation cases do not imply replacement or candidate acceptance, and do not require an expanded pixel-calibration matrix to describe their bounded findings accurately.
