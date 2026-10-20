# Histogram verification

## H0 numerical contract

Independent Astra review approved the histogram numerical contract and H1 boundary on 2026-10-20. H1 owns two inactive pure compatibility modules and one focused test; no production routing or browser acceptance is established. H2/H3 retain mapper and integration review gates. See the [milestone](../../../.kiro/specs/analyst-workspace/histogram-milestone.md) and [design](../../../.kiro/specs/analyst-workspace/histogram-design.md).

The contract retains original default ticks, zero/fractional count behavior, negative floor alignment, ordered membership and final-bin catch-all. It explicitly repairs equal-integer explicit-count nonfinite boundaries and rejects malformed or excessive configurations. These exceptions must appear in regression tests and cannot support unqualified exact-parity claims.

One FMP income-statement request captured 40 AAPL quarters, 2016-09-24 through 2026-06-27, at 2026-10-20T14:06:05.149732+00:00. Parameters: symbol=AAPL, period=quarter, limit=40. Revenue remains original USD amounts. Raw SHA256: `390dc8cbfc8302720a203bd9782d5e3b1f7363a4f762bdfcef079dbbe4c72f6b`. An independent read-only check matched all 40 CSV records and all five fields to the raw response, verified unique dates, quarterly periods and finite revenues. Raw data remains ignored under artifacts/chart-histogram/fmp. Source baseline is Workspace `17a35f3468452c5ae92cbf9f57de4d7bd92cde12`. This is dataset readiness, not displayed-chart acceptance.

Browser acceptance will explicitly select revenue, None category and disabled aggregation so fiscalYear is not treated as the financial field. Additional synthetic checks cover signed, missing, repeated and boundary values. Histogram application acceptance and publication remain open; the previously published XY alpha is unchanged.
