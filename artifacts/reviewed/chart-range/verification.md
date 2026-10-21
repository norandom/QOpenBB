# Range chart verification

R1's inactive numerical helper is independently accepted at Workspace `0bc5109671c3ca1af43b863a0da3616ab78ae968`. R2 inactive Range Bar is accepted below; Range Area, editor integration, real-FMP application acceptance and publication remain open. Box Plot is still the active delivery milestone.

Retained Grid 34.1.1 RangeChartProxy emits one series per selected measure and calculates minimum/maximum observations within each category. It does not pair adjacent fields into low/high coordinates. The [reviewed contract](../../../.kiro/specs/analyst-workspace/range-chart-plan.md) preserves that meaning within the existing finite-number/null capture domain. Original infinities and argument-spread limits are outside this bounded helper.

The helper and its test are the only two added files. It performs no grouping, aggregation or rendering and imports only the existing diagnostic type. It preserves counts, null omission, singleton/empty behavior, Math.min/Math.max signed zero, and finite extremes without subtracting endpoints. Invalid, sparse or throwing input returns diagnostics atomically; inputs remain unchanged.

Missing-module RED preceded implementation. Author and independent reviewer each passed all 42 focused tests, strict scoped TypeScript and scoped Biome. The combined checker passes with no errors or violations: 53 physical lines, 37 logical units and maximum 20 per function. Independent contract/source review and raw commands/logs remain under `artifacts/chart-parallel/` and `artifacts/chart-range/r1-*`; this concise record is the public mirror.

The existing captured-FMP quarterly revenue/net-income dataset is suitable for later fiscal-year min/max comparisons in raw USD, with partial years labelled. No provider request, browser run, image build or visual acceptance occurred for R1. Selected financial screenshots remain pending until the actual Range widgets are verified.

## R2 inactive Range Bar renderer

R2 inactive Range Bar is independently accepted at Workspace `1732847552a762c38e1cb1408d1efebccdeb0e6a`. Seventeen focused tests pass (nine unit and eight actual ECharts SVG); Biome passes 11 files and combined complexity has zero errors/violations. Scoped strict typing retains only inherited typography.ts TS2578; canonical strict baseline/candidate each retain 3,427 identical diagnostics, compiler exit 2. Range Area, application integration, real-FMP image/browser acceptance and publication remain open. Box Plot remains the active delivery milestone; the published alpha is unchanged.

The eight new production files consume the accepted R1 helper and an explicit resolved scale. They preserve separate selected-measure extrema, raw units, category identity/null slots, grouping geometry, endpoint labels and escaped tooltips. There is no application activation or Range Area implementation. Independent approval and exact frozen hashes: `artifacts/chart-range/r2-review.md`. Final remediation added test assertions only; production hashes were unchanged.

Fresh reviewer commands under WSL Debian user mc, pinned Node 24.22.0 and the existing one-worker config: `r2-test.sh review-final-tests` passed nine unit/eight SVG tests, exit 0; `r2-review-static.sh` passed Biome on 11 files, exit 0. `r2-review-static.sh typing` exited 2 solely for inherited typography.ts(1,1) TS2578. The canonical same-config baseline/candidate comparison has 3,427 identical inherited diagnostics, compiler exits 2, zero added/removed blocks; complete sorted raw output comparison also found zero differences. These are baseline-delta checks, not clean typechecks.

Controller combined complexity reports zero errors/violations: production maxima 263 physical lines, 119 logical units and 28 per callable, within 400/300/50. Missing-renderer/projection RED evidence preceded implementation. Scripts, logs, exits, canonical comparison and source hashes remain local under `artifacts/chart-range/r2-*`.

Independent retained-raw-FMP review confirmed FY2017 revenue extrema USD 45,408,000,000 to 78,351,000,000 and net income USD 8,717,000,000 to 17,891,000,000 across four quarters. This verifies source extrema and test assertions only; it establishes no application-rendered financial acceptance. No provider request, browser run or image build belongs to R2.
