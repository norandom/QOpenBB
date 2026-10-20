# Histogram verification

Histogram H0-H5 is accepted and published in [alpha-39460489280-1](https://github.com/norandom/QOpenBB/releases/tag/alpha-39460489280-1). Six candidate-image journeys and six anonymous release-image pulls passed. The ordinary Table/File scope includes captured FMP values, editor controls, navigation, save/reopen and export.

The sections below preserve evidence at each acceptance stage. Earlier statements about pending work describe that stage; H4 and H5 record the final outcome and remaining limitations.

## H0 numerical contract

Independent Astra review approved the histogram numerical contract and H1 boundary on 2026-10-20. H1 owns two inactive pure compatibility modules and one focused test; no production routing or browser acceptance is established. H2/H3 retain mapper and integration review gates. See the [milestone](../../../.kiro/specs/analyst-workspace/histogram-milestone.md) and [design](../../../.kiro/specs/analyst-workspace/histogram-design.md).

The contract retains original default ticks, zero/fractional count behavior, negative floor alignment, ordered membership and final-bin catch-all. It explicitly repairs equal-integer explicit-count nonfinite boundaries and rejects malformed or excessive configurations. These exceptions must appear in regression tests and cannot support unqualified exact-parity claims.

One FMP income-statement request captured 40 AAPL quarters, 2016-09-24 through 2026-06-27, at 2026-10-20T14:06:05.149732+00:00. Parameters: symbol=AAPL, period=quarter, limit=40. Revenue remains original USD amounts. Raw SHA256: `390dc8cbfc8302720a203bd9782d5e3b1f7363a4f762bdfcef079dbbe4c72f6b`. An independent read-only check matched all 40 CSV records and all five fields to the raw response, verified unique dates, quarterly periods and finite revenues. Raw data remains ignored under artifacts/chart-histogram/fmp. Source baseline is Workspace `17a35f3468452c5ae92cbf9f57de4d7bd92cde12`. This is dataset readiness, not displayed-chart acceptance.

Browser acceptance will explicitly select revenue, None category and disabled aggregation so fiscalYear is not treated as the financial field. Additional synthetic checks cover signed, missing, repeated and boundary values. Histogram application acceptance and publication remain open; the previously published XY alpha is unchanged.

## H1 inactive binning accepted

Workspace `42170015627a7a09c1245b2dbf76e602b247d235` implements only histogramTypes.ts, histogramBins.ts and its focused test file. Independent Astra review approved the actual source and tests. The module remains disconnected from UI/routing.

The initial RED run failed all 69 cases against the unimplemented function. Final focused Vitest runs passed 71 tests, including the independent rerun, with one worker and exit zero. Independently extracted original-engine comparisons covered 10,000 bounded default-domain and 2,000 explicit-count cases without differences; count probes also checked index partitioning. Scoped strict TypeScript passed independently. Local evidence is artifacts/chart-histogram/h1-*.

The combined maintained-scope checker passed using explicit Workspace/data-API change manifests. Production sizes: histogramTypes.ts 25 physical / 18 logical; histogramBins.ts 189 physical / 169 logical / maximum 26 per function, below 400/300/50 caps. The inventory includes both new modules; unrelated catalog/Perspective work is excluded from the commit.

The separately reviewed H2 mapper design corrects axis-bound semantics: bounds outside the data extend normally unless minimum exceeds domain maximum or maximum falls below domain minimum. H2 rendering, H3 integration, H4 identified-image FMP acceptance and H5 publication remain open. README and docs checkboxes reflect inactive H1 acceptance only.

## H2 inactive interval mapper accepted

Workspace `88c837f24376135902a9691f9340baceef29989e` adds eight cohesive mapper modules and three test/fixture files. Shared production and H1 files are unchanged. Final focused Vitest passed 33 tests, including ten actual ECharts SVG tests. These inspect unequal interval widths and frequency heights, clipping, centered labels, color/opacity, axes/bounds, empty outer intervals, range/Frequency tooltips and retained-data overview rendering.

Independent review found a real hidden-series defect: removing public data when legend selection was false prevented native restoration from retained intervals. The regression failed before repair. The accepted mapper retains data and lets native legend selection hide it; the same chart now restores/hides/restores three rectangles while H1 runs once. Reviewer independently reran that regression after inspecting the fix. SVG SSR must render after each native action before inspecting its refreshed display list; geometry assertions remain intact.

Final evidence is artifacts/chart-histogram/h2-legend-{red,green,typecheck}.log and h2-legend-syntax-units.json. Scoped TypeScript reports only the inherited typography.ts TS2578 diagnostic, not a clean full-repository compilation. The final combined explicit-scope complexity gate passed: maximum 69 physical lines, 48 logical units/file and 21/function across H2 production files.

The H3 integration handoff and H4 browser source preparation received separate reviews. They do not establish runtime acceptance. Original automatic axis/outer-extent visual comparison, editor/navigation integration, real-FMP browser journeys and publication remain open. README/docs/breadth record H2 as inactive only.

## Reviewed metadata seam for H3

Workspace `ea32516191e3710ad015da9fd655cdb95896e522` extends the supported histogram result with its validated projection and resolved domain. H3 needs the complete bin list, including empty intervals, for the original Bin count display. The mapper remains the sole assembly path and invokes H1 once; failure behavior and Cartesian structural compatibility are unchanged. Independent review approved the narrow three-production-file amendment and its focused regression. The admission change narrows types only.

The metadata regression failed before implementation; final focused mapper/SVG tests passed 34 cases. Scoped TypeScript retains only inherited typography TS2578. Final explicit-scope complexity passed, with maxima 69 physical / 49 logical / 21 per function. Evidence is artifacts/chart-histogram/h2-metadata-*. H3 remains in progress.

Independent H3 ownership review also approved one gallery-reset guard in comboSessionAssignments.ts: preserve the inactive stored inversion setting on entry to histogram while its effective setting is false; other family resets remain unchanged. H3 must prove both behaviors and pass whole-file limits before acceptance. This is a reviewed integration change, not completed application evidence.

## H3 production join source accepted

Workspace `85a30686590e1fb7bc832d14d620c2eae38f16a8` connects histogram to the existing Table/File chart session, setup, editor and host. The reviewed scope contains 36 production files and four tests. The accepted H1/H2 calculation remains the single projection path; navigation and legend updates retain its full interval data. Inactive saved settings survive family changes, and the original Bin count control displays explicit or calculated bin length.

The affected test set passed 301 distinct cases in 19 files: 155 application and 146 compatibility tests, including 25 new H3 tests. Runs use pinned Node and the existing application/compatibility Vitest configurations with one worker. Evidence: artifacts/chart-histogram/h3-application-regressions.log, h3-common-controls.log and h3-compatibility-regressions.log. Tests cover capture before aggregation, first-field selection, empty-selection recovery, saved options, numeric bounds, retained navigation, native legend restoration and session lifecycle.

RED checks found stale bin-count input after a new revision, top/right bound lookup and equal Y-bound degeneration; each has a passing regression. Fixture errors in rowData, padding event shape and capture timing were corrected without production workarounds. Independent source review approved the frozen changes and independently reran all 25 new H3 tests, which passed.

The combined explicit-scope checker passed for all 36 production files, with maxima 383 physical lines, 186 logical units/file and 40/function. Baseline-relative TypeScript ran the same baseline tests twice: both runs report 2713 inherited diagnostics, with no added or removed diagnostic headlines after ignoring line shifts. This establishes no new diagnostics, not a clean full compilation. The comparison binds every production file hash in artifacts/chart-histogram/join-static/comparison.json.

The authentic original Revenue reference shows X from zero through 150 billion and Y from zero through 10; the current mapper uses tighter extents. This concrete automatic-axis difference remains an H4 repair obligation.

H4 still owes image-only browser acceptance with the captured FMP data, original automatic axis/outer-extent comparison and previous-family application regressions. The published alpha is unchanged; no histogram feature or publication acceptance is claimed.

## Automatic-axis refinement source accepted

Workspace `f003fdc7132274fc21511a9546559633bdef5bb7` adds viewport-dependent histogram axis rounding while preserving raw intervals, frequencies and explicit bounds. The shared ordinary-chart step calculation is exported without changing its body or callers. Histogram uses bounded outward rounding and measured axis space; retained navigation uses the same policy. Independent source review accepted the seven production files and four affected test files.

The initial regression run failed three cases for missing rounding and retained pixel budgets. The affected gate then passed 137 cases across seven compatibility files. Review reproduced an ECharts merge behavior: omitting an interval retains the prior native value. A new regression failed before explicit clearing and passed afterward; the final navigator file passes eight cases. Fourteen application tests also pass after correcting two test-fixture typing errors discovered while inspecting the fresh H3 baseline. The independent reviewer reran all 47 histogram compatibility cases successfully; see axis-independent.log. Logs are artifacts/chart-histogram/axis-red.log, axis-green.log, axis-merge-red.log, axis-merge-green.log and axis-application-green.log.

Actual-engine assertions cover reference-sized X ticks at 0/50/100/150 billion, Y ticks at 0/5/10 and rectangle geometry. Narrow/wide, signed, explicit-bound, tiny/extreme, navigator and fallback cases preserve financial observations and avoid forced X zero inclusion. Four-bin frequencies are checked independently as 12/9/14/5.

The final static comparison uses the same corrected existing application fixture in both runs and binds its hash separately. Both runs retain 2713 diagnostic headlines, with none added by the production refinement. This does not claim a clean repository compilation. The earlier one-error comparison and two fixture errors remain recorded in ignored diagnostics. The final explicit-scope complexity gate passes within 400/300/50 caps. Evidence: artifacts/chart-histogram/axis-static-final/comparison.json and axis-complexity-final.json.

The authentic original default reference supports the target rounding. Its four-bin input displayed 4 but did not repaint within the bounded wait; no original four-bin visual match is claimed. The original reference collection also has a disclosed CSV request failure and is not candidate acceptance. Raw financial images remain ignored. H4 image-only FMP, lifecycle, export and visual verification remains open; no new image has been published.


## Endpoint labels and control order source accepted

Workspace `b18082dad1243cb04a7b07c4ec221c818e99e7c4` corrects the remaining default FMP comparison differences: conditional X endpoint-label suppression and Bin count after Tooltips. The public ECharts afterupdate extension changes only matching endpoint text visibility. Native ticks, grids, numeric extents and bars remain unchanged. It restores only its own visibility changes and preserves native collision handling.

Independent review reran all 28 focused cases in three files, exit 0. Actual SVG tests cover endpoint text and tick/grid geometry, short labels, padding, two ticks, top/rotated axes, zoom/reset/resize and unrelated-axis isolation. The DOM test checks control order. Evidence: artifacts/chart-histogram/labels-final-green.log, editor-green.log and labels-independent.log.

The initial RED checks reproduced the control-order and label-subset differences. The first layout-hook implementation changed label options but failed actual SVG assertions because ECharts had already constructed the axis drawing. This rejected approach was replaced with the public afterupdate hook. Its failed raw log was overwritten; the failure is retained in the execution transcript, not presented as a preserved raw artifact. Initial labels-red.log and editor-red.log remain local.

Baseline-relative TypeScript retains 2713 inherited diagnostics in both runs, with none added or removed. The three changed production files pass whole-file caps, with maxima 74 physical lines, 66 logical units and 15 units per function. Evidence: artifacts/chart-histogram/labels-static/comparison.json and labels-complexity-final.json.

Before this correction, image-only candidate `sha256:555004bc932af18a8753891211f878cb35de9a1555763c6865ff2808ae4d2244` at Workspace `f003fdc` passed the captured-FMP journey (run 03) and synthetic journey (run 10). FMP frequencies were 2/7/4/1/9/8/2/4/2/0/1 by default and 12/9/14/5 with four bins. Synthetic checks included signed/missing values, controls, numeric zoom/pan/reset, retained bin count, empty recovery, refresh, reopen/export and browser diagnostics. Intermediate failed runs exposed fixture and drawn-label observer errors, retained in the ignored execution record. These are earlier-image results: the corrected candidate must pass both journeys and prior-family regressions before H4 closes.

The File Table Settings visibility failure remains open in the renderer matrix. Browser mini-chart evidence establishes the presence of the overview; full retained overview geometry is covered by actual-engine unit tests. No new alpha publication is claimed here. Raw provider captures, financial screenshots and runtime credentials remain ignored.


## Miniature geometry source accepted

Workspace `c1ee9ae9063531b0edd0625eacc6a2725897b5cb` restores the histogram miniature's 18px plot height, aligns it with the main plot, displays raw numeric labels and retains the full calculated-bin extent, including empty outer bins. The main rounded axis and original navigation state remain unchanged. Ordinary chart callers retain their existing defaults.

Independent review passed 40 focused tests across histogramNavigator, cartesian.navigator and histogramProductionJoin, exit 0. Native-engine assertions cover both Y-axis sides, fractional tick labels, enabled titles/ticks, 18px geometry, retained bounds and no recalculation. Endpoint-only width estimation initially failed by 14px; including titles/ticks in containment initially failed by 23px. Both RED results remain in ignored overview-fractional-red.log and overview-decorated-red.log. Final evidence: overview-decorated-green.log and overview-independent-final.log under artifacts/chart-histogram/.

The final baseline-relative type comparison retains 2713 inherited diagnostics in both runs, with none added or removed. The earlier candidate had one added type error; numeric-axis narrowing corrected it. Four production files pass caps: maxima 144 physical lines, 52 logical units and 20 per function. Evidence: overview-static-final/comparison.json and overview-complexity-final.json; production hashes match the independently reviewed files.

Preceding image `sha256:a1b14860f8b73a591a244d33f53327d021a2c03e06dfd05c9a937cdf0e39d352` at b18082d passed both histogram journeys and four ordinary/combo/XY regressions. Its same-data miniature comparison revealed the geometry differences repaired here. Original wheel/pan/reset effects were not established in the bounded reference capture; candidate gestures changed the numeric window and reset restored identical full canvas bytes. These observations do not establish original gesture equivalence. The corrected image must repeat the histogram journeys, matching miniature comparison and affected regressions before H4 closes. Publication remains open.


## H4 identified-image acceptance

Independent review accepts production Workspace `c1ee9ae9063531b0edd0625eacc6a2725897b5cb` in image `sha256:d346ac72142f4cab3ddc5c1527dd4383e97608aada180816f96a39ee996e80f3`, packaged-only with no source overlay at loopback port 55537. Both final histogram journeys and four ordinary/combination/scatter/bubble regressions passed with one isolated headless worker, zero retries, no skipped or flaky cases and clean application diagnostics. The final release source `ae45e30e5c574a0b6a3fd61f713abf1b6e7f5c27` differs only by the three reviewed histogram browser files; no production code changed after the tested image was built.

The FMP journey imports the exact retained 40-quarter AAPL response as a five-column CSV, explicitly selects Revenue with None category and no aggregation, and checks every occupied interval, count and tooltip. Default frequencies are 2/7/4/1/9/8/2/4/2/0/1; four-bin frequencies are 12/9/14/5. Values remain raw USD, and Frequency counts observations. Both themes, styling, refresh, saved controls, reopen and exported pixels pass. This proves captured-provider values through File Table, not the live data API route.

The synthetic journey covers signed/zero/missing/invalid values, first selected field, equal-value repair, category aggregation, both axis positions, controls, retained navigation counts, pan/reset, empty-selection recovery, refresh and save/reopen/export. Initial corrected-image run 01 passed FMP but failed the synthetic observer: interior X/count labels were mistaken for Frequency ticks after the miniature geometry changed. The repaired observer requires its numeric zero intercept to agree with the drawn bar baseline. Exact frequency/boundary assertions remain unchanged. Independent replay passed the failed public drawing, four explicitly derived axis placements and 72 earlier captured zoom frames. The final run 02 passes both journeys; the rejected run and RED/GREEN evidence remain local.

The same-data original/final comparison confirms an aligned 18px miniature and matching raw labels/full 40–150B bin extent. Remaining differences are small: main baseline 2px, label anchors about 3.5/5px and handle decoration. Both candidate navigation modes change the window and reset to byte-identical full canvas pixels. Original gesture effects were not established, so original gesture equivalence is not claimed. Original reference transport limitations remain disclosed in its local report. The File Table Settings column-visibility failure remains open in the renderer matrix.

Commands used the existing `run-browser.sh` for the two histogram specs, `run-prior-browser.sh` for ordinary-combo and xy, and the matching FMP `reference/navigation/candidate/run.sh capture-overview` collector. Runtime descriptor, exact image/source, command and test hashes are retained in `overview-h4-execution-02.json`. Reports:

- `artifacts/chart-histogram/browser-h4-c1ee9ae-02/browser-results.json`: 2 passed, SHA256 `c298370774a19268f46b670ca663cb778a4aab11835c2fa7ca4c4b30af6efc75`.
- `artifacts/chart-histogram/prior-ordinary-combo-c1ee9ae/browser-results.json`: 2 passed, SHA256 `a68931735bb8705888045987fd0a5158aff55ebab07bbd229357c3896401d606`.
- `artifacts/chart-histogram/prior-xy-c1ee9ae/browser-results.json`: 2 passed, SHA256 `bb58df7f16b607f22ddd0249ab9974b0e7d670bc38441ea2dac77e0e33f2f469`.

The visual collector passed once in 26.8 seconds with empty diagnostic arrays; its report is `artifacts/chart-histogram/reference/navigation/candidate/capture-overview/report.md`. Financial PNGs, raw captures, private runtime descriptors and traces remain ignored. H4 closes within the ordinary Table/File histogram scope. H5 release publication remains open; unfinished chart families and callers remain unchecked.


## H5 published alpha

[CI run 39460489280](https://github.com/norandom/QOpenBB/actions/runs/39460489280) passed checks, both Dagger builds and publication from root `82932663f243d9e920a895f1d6a1da6ec4d18dcc`. [Tagged prerelease alpha-39460489280-1](https://github.com/norandom/QOpenBB/releases/tag/alpha-39460489280-1) includes Compose, the public environment template and the exact image manifest. Workspace is pinned to `ae45e30e5c574a0b6a3fd61f713abf1b6e7f5c27`; data API remains `49cc413e6ab67eaa0444e07485b0f9243c786f7b`.

- workspace: `ghcr.io/norandom/qopenbb-workspace@sha256:158e11d4b145ec6d51ac201c4361761574e581b5a23dd7fde3bbfc94953d7342`.
- data-api: `ghcr.io/norandom/qopenbb-data-api@sha256:946dcb1bbae0bee8f8d314d481eac91a891121d03196c134ecad9031f6a8cae7`.

Six pulls succeeded with a fresh empty Docker configuration: digest, alpha tag and latest for each service. Remote manifest/configuration digests, source labels, platform and pulled repository digests matched the release manifest. Manifest SHA256: `d670b311b9d9266b6c968b960627212bfb4f59ff8312f73747280d6887bc834a`. Local verification reports are under `artifacts/chart-histogram/release-39460489280/`; credentials and image archives are excluded.

CI rebuilt the pinned source. Browser acceptance belongs to the identified local candidate above, whose production is identical; the pulled release images were checked for identity, not rerun through the browser. README, install links, renderer checklist, roadmap, spec and breadth records are reconciled. Assembled Compose, owner-server deployment, remaining chart families/callers and the disclosed table-visibility issue remain open. Histogram H0-H5 is complete within its stated ordinary Table/File scope.
