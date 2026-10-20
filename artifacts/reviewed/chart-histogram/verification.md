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
