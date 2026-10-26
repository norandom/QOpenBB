# Stacked Line documentation and retained-fixture review

2026-10-26. APPROVED for the bounded documentation/publication set and retained financial input only. Original browser results are excluded from this review. This does not complete SL0, approve implementation, accept a rendered sample or establish a new provider retrieval.

Reviewed working-tree files: `README.md`, `docs/roadmap.md`, `docs/echarts-status.md`, `.kiro/specs/analyst-workspace/{research.md,stacked-line-milestone.md,spec.json}`, `artifacts/reviewed/chart-stacked-line/{original-source.md,integration-source.md,assessment-review.md}`, and the three Stacked Line entries in `artifacts/reviewed/sync-manifest.json`.

## Publication and completion boundaries

- Both JSON files parse successfully with PowerShell `ConvertFrom-Json`.
- All Markdown file-link targets in the eight reviewed Markdown documents exist after resolving relative paths. External HTTP availability and section anchors were not checked.
- The three manifest entries have matching source/published SHA-256 values, actual bytes and exact-copy declarations: original source 7,520 bytes; integration source 11,595 bytes; assessment review 4,803 bytes. Actual source and published hashes match each other and the manifest.
- Actual original-source hash is `d1e31a33d0f0ce7102036203ecb74fc5e8866d0609a9ece541c5895aee69b5df`; integration-source hash is `f9bd9333a56cc18be50e848fd90073be139d58e9c53b795c3bc853de75dbf952`; assessment-review hash is `8082493e6dba5d36b85bae0dbe140ad27ce7cdd0d30cc24012bef2b871ba1ad2`.
- The review's recorded input hashes match current research (`3c0460f97bfae46f407e453f33ab402204d76f064947290b1740eb69b8e8b7ae`) and milestone (`d1e7df37897c2fc54d047adf3f30b5053a5737891da7d4c20d08b41c026f1325`) as well as both source reports.
- README links the assessment; roadmap and ECharts status say source assessment reviewed and browser characterization/admission open. `spec.json` retains `assessment-in-progress`. SL0 through SL4 remain unchecked. Research and review expressly distinguish source findings from application parity. No false Stacked Line completion was found.
- The neighboring Funnel publication wording is consistent across the inspected summaries, but release assets/pulls were not independently reverified in this documentation review.

## Financial fixture verification

Independently loaded `artifacts/chart-histogram/fmp/raw.json`, followed `raw_record_index` from `artifacts/chart-heatmap/fmp/provenance.json`, and compared each cost/gross value with `artifacts/chart-heatmap/fmp/fy2025-heatmap.csv`. All eight CSV numerical cells equal the retained provider fields. Four AAPL records report USD, and the dates match provenance. The source is retained, retrieved 2026-10-20, not a fresh retrieval.

| Fiscal quarter / period end | Cost of revenue USD | Gross profit USD | Sum USD | Raw revenue USD | Difference USD |
| --- | ---: | ---: | ---: | ---: | ---: |
| FY2025 Q1 / 2024-12-28 | 66,025,000,000 | 58,275,000,000 | 124,300,000,000 | 124,300,000,000 | 0 |
| FY2025 Q2 / 2025-03-29 | 50,492,000,000 | 44,867,000,000 | 95,359,000,000 | 95,359,000,000 | 0 |
| FY2025 Q3 / 2025-06-28 | 50,318,000,000 | 43,718,000,000 | 94,036,000,000 | 94,036,000,000 | 0 |
| FY2025 Q4 / 2025-09-27 | 54,125,000,000 | 48,341,000,000 | 102,466,000,000 | 102,466,000,000 | 0 |

Formula for each row: costOfRevenue + grossProfit - revenue = 0 USD. No scaling or currency conversion was applied. These two additive components provide a defensible positive financial stack; including revenue as a third stacked component would double-count the aggregate. For this selected order, cumulative normalized levels are cost/revenue times 100 and 100; the gross-profit share is the difference between those levels. This fixture cannot establish signed, missing, duplicate-category or zero-total semantics.

Freshly computed SHA-256 values match the provenance's declared raw/CSV hashes:

- Raw response: `390dc8cbfc8302720a203bd9782d5e3b1f7363a4f762bdfcef079dbbe4c72f6b`.
- CSV: `ca76bb6fedb7a45709b050bc810c57784ac5543b42120b341b9db0690201331b`.
- Heatmap provenance file itself: `50965d20d7393fb97a45ae3b7e44dc158241e8c79943cfb7be054cd4ea8925f3`.

The provenance retains its historical `prepared-not-browser-accepted` status and `browser_accepted: false`; this review validates its retained input/reconciliation, not its later chart acceptance status. Python was unavailable through the Windows launcher; exact integer comparisons and arithmetic were executed in PowerShell instead. No broad tests, production edits, provider calls or browser actions were performed. Only this review document was written.
