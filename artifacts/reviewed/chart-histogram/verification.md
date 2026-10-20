# Histogram verification

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
