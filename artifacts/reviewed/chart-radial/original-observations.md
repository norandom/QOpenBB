# Original Radial run 3 interpretation

Radial Bar passed; Radial Column retained one deliberate soft failure for normalized `E|Primary|30`. Both tests completed all 19 capture records, including edited controls and same-session reload. This is original characterization, not a clean suite or candidate acceptance. The probe remains frozen.

## Identity and result

- Frontend source: `38dffc33389aca0e4a87e0e88d42f7067aa220df`; loopback frontend `http://127.0.0.1:60307`, with separately qualified backend-only overlay. Runtime qualification remains in `../../../chart-nightingale/original-runtime.json`.
- Command: `wsl -d Debian -- bash /mnt/d/Source/QOpenBB/artifacts/chart-radial/original/run.sh artifacts/chart-radial/original/run-3`. The runner fixes one headless browser worker and zero retries. `exit-code.txt` is `1`; `browser-results.json` reports one passed, one failed, zero skipped/flaky, duration 276.975 seconds.
- Frozen probe SHA256: `567b4a45512de47279c9e869e7d1e0a5b843c8eb4efd656b4ebda078f9df41e0`. Final static evidence: `../preparation/exits.json`, all five entries zero (strict TypeScript, imported-helper baseline, difference, Biome lint, Playwright listing of exactly two tests).
- Browser report SHA256: `9e0bca9a2f819bb1ba49d5605101b689d3400026dd45c748c5b2ae98c84acab6`.
- Raw family records/screenshots: [Column observations](browser-output/radial-original-original-Radial-Column-bounded-contract/observations.json), [Bar observations](browser-output/radial-original-original-Radial-Bar-bounded-contract/observations.json). Each named record has a corresponding PNG. Captured screenshots are not owner visual acceptance.

## Observed defaults and identities

Both default and reselected Grouped views omit root `seriesGroupType`; actual changed Stacked, Normalized and return-to-Grouped views save explicit root values. The initial same-value dropdown choice emits no change in original AG Select, as diagnosed in `../readiness.md`; missing default root is not save-lag evidence.

Each family produced all six exact native tuples for compact Primary `[1,4,9]`, Secondary `[2,8,18]` in grouped, stacked and normalized views. Normalized tooltips retain raw amounts. Hiding Secondary produced all three Primary tuples, and restoration recovered all six. Category identities remained A/B/C. Single-category default, hole 0 and hole .5 views were captured separately.

| Public labels / projected control | Column | Bar |
| --- | --- | --- |
| Compact grouped numerical ticks | 0..20, step 5 | 0..18, step 2 |
| Compact stacked ticks | 0..30, step 10 | 0..35, step 5 |
| Compact normalized ticks | 0..100, step 20 | 0..140, step 20 |
| Inner Radius control | .5 | .2 |
| Axis font size control | 11 | 12 |
| Group / Series Padding controls | 0 / 0 | 0 / 0 |

These are observed tick labels and first-axis control projections, not measured scale-domain endpoints. Bar's displayed padding zeros must not replace the separately source-derived radius-category padding defaults. Both Series panels show stroke width 0, dash 0, line/fill opacity 1, Labels off, Tooltips on and Single tooltip mode. Marker/Shadow controls and axis Shape were absent under asserted selectors.

## Signed, duplicate, zero and missing rows

The mixed source rows remain `[A,A,B,C,D,E]`, Primary `[10,-5,0,20,missing,30]`, Secondary `[-5,10,0,-10,4,6]`. Both public text captures retain duplicate A labels in input order. Bar grouped and normalized native scans found E Primary 30 and Secondary 6, plus signed A/C and D Secondary 4 tuples. Column grouped found both E tuples; Column normalized found E Secondary 6 and the other nonzero Secondary tuples, but did not find E Primary 30. The exact failing assertion and observed five Secondary tuples remain in `browser-results.json`; the soft failure allowed all later evidence to be collected. It is not silently accepted or converted to a pass.

The installed original enterprise source independently confirms a method-level `return` when `innerRadiusDatum` or `outerRadiusDatum` is undefined in shared radial-column node creation (`main.esm.mjs:35439-35440`; source contract in `../../original-contract.md`). That is a confirmed source control-flow defect which can discard a series after invalid accumulated endpoints. The browser's normalized Column result is consistent with it. A bounded saturated-pixel scan is positive evidence for found tooltips and cannot, by itself, prove absence, locate the exact failing source row, establish zero/missing equivalence, or prove numerical geometry. No original-compatibility correction is authorized by this report.

Aggregation saved root `aggFunc: "sum"`; inversion saved `switchCategorySeries: true` after aggregation. Both were reset before appearance edits. Screenshots/models establish these reachable transitions; exact aggregated arithmetic was not independently asserted.

## Observed saved control targets and reload

Under `chartOptions["radial-column"]` or `["radial-bar"]`, Series edits save `series.strokeWidth=3`, `series.fillOpacity=.6`, `series.label.enabled=true`.

| Edited axis control | Column family axes | Bar family axes |
| --- | --- | --- |
| Thickness 3 | angle-category and radius-number `line.width=3` | angle-number and radius-category `line.width=3` |
| Inner Radius .25 | both above `innerRadiusRatio=.25` | both above `innerRadiusRatio=.25` |
| Group Padding .2 | angle-category `paddingInner=.2` | radius-category `paddingInner=.2` |
| Series Padding .3 | angle-category `groupPaddingInner=.3` | radius-category `groupPaddingInner=.3` |
| Parallel orientation | angle-category `label.orientation="parallel"` | angle-number `label.orientation="parallel"` |

The observed spinbutton order is thickness, hole, Group Padding, Series Padding. Single-category hole edits also saved the ratio to both family axes. Models after same-session reload retain normalized root, Series values, both axis settings and existing neighboring common options.

Show navigator was reachable, but its immediate saved common navigator state remained disabled. Show mini chart was also reachable and then saved `chartOptions.common.navigator.enabled=true` and `miniChart.enabled=true`; those flags survived reload for both families. This does not establish a painted navigator/mini-chart effect or fresh-session persistence. No paint-generation assertion was implemented, so an unchanged drawing snapshot is not evidence of a fresh no-op paint.

## Diagnostics and limits

Both original journeys recorded page error `Unexpected token '<'`, one CSV `net::ERR_FAILED` console/request failure at the owned `/api/pro/files/<id>.csv` path, and an empty HTTP-failure array. These original diagnostics are retained, not described as clean. Both tests nevertheless reached reload and persisted their control records.

No new browser run, provider request, production edit, installation or build was performed for this interpretation. No candidate geometry, exported image, retained-FMP comparison, fresh-session reopen, clean diagnostics or numerical signed/zero geometry is certified here. Column boundary feasibility belongs to the separate bounded primitive spike; screenshots and tooltip targets are not a substitute for its geometry evidence.
