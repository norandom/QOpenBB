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

## R3 inactive Range Area renderer

R3 inactive Range Area is independently accepted at Workspace `c6d4329960a5176775a47aba2bfefcac36d0cd8e`. Sixteen focused tests pass (10 unit and six actual ECharts SVG); Biome passes 10 files and combined complexity reports zero errors/violations. Scoped typing retains only inherited typography.ts TS2578, exit 2. Final canonical baseline/candidate each retain 3,427 identical inherited diagnostics, exit 2, with no added/removed diagnostics. Application integration, real-FMP image/browser acceptance, visual comparison and publication remain open. Box Plot remains the active delivery milestone; the published alpha is unchanged.

The seven new production files and three test files preserve each selected measure's within-category min/max envelope, null-run gaps, separate boundary/paint semantics and raw financial labels/tooltips. There is no application activation. Independent approval and frozen hashes are retained in `artifacts/chart-range/r3-revision-review.md`.

Fresh independent remediation verification passed 10 unit and six actual ECharts SVG tests, exit 0 (`r3-revision-review-tests.log`); no-fix Biome passed 10 files, exit 0 (`r3-revision-review-biome.log`). Scoped strict typing exits 2 solely for inherited typography.ts(1,1) TS2578 (`r3-revision-review-types.log`). Final shared canonical comparison `artifacts/chart-parallel/b3c-r3-typing-final-comparison.json` records 3,427 identical baseline/candidate diagnostics, compiler exit 2, no additions/removals; raw final output is retained beside it. These checks establish no new typing delta, not a clean typecheck. Controller `r3-complexity.json` reports zero errors/violations under 400/300/50 caps.

Stronger actual-SVG assertions exposed four stale endpoint labels after singleton-to-empty updates. The retained failing transition (`r3-revision-red.log`) preceded the production repair: `$mergeChildren:false` replaces the complete custom glyph group. The final checks also cover band/boundary paths, clipping, markers, supplied ticks, equal-domain raw text, hidden-field restoration and native null-slot tooltip identity. The jsdom canvas text-measurement warning limits typography claims; SVG checks do not establish application pointer or visual parity.

`r3-financial-comparison.json` passed a local comparison of all five fixture rows against retained raw FMP observations, including partial FY2016. FY2017 extrema remain revenue USD 45,408,000,000 to 78,351,000,000 and net income USD 8,717,000,000 to 17,891,000,000. They describe quarterly dispersion within fiscal years, not annual totals or confidence bounds. This is source/fixture evidence only. No application-rendered FMP acceptance, browser run, provider request or image build belongs to R3.

## R4a inactive capture/setup accepted

Workspace `102b53ad677f057903af50ea315c3c790ee67789` adds the neutral `statistical-observations` policy for Range Bar/Area capture and setup. It reuses the accepted category and aggregation helpers because the retained original Range and Box proxies share those methods. Existing Box behavior is preserved. Raw aggregation keys remain distinct from normalized statistical categories, and each selected field reaches its own min/max projection. Both Range families remain inactive in the application.

Independent design and source review approved the five production edits and one new test. The missing-policy RED preceded implementation. All 16 new capture/setup cases pass; the affected five-file Range/Box/grid/setup join passes 168 tests. Review caught a shell-timezone dependency in the new Date test; the test now controls/restores its own timezone, and its 16 cases pass with `TZ` unset. The production join was not repeated for that test-only fix. Read-only Biome passes all six owned files. Whole-file complexity reports no errors or violations under 400/300/50 caps. Final canonical TypeScript baseline/candidate logs are byte-identical: 2,711 inherited diagnostics, exit 2; this is no new typing delta, not a clean typecheck.

Local commands/results are retained under `artifacts/chart-range/r4a-*.log`, `.exit` and `r4a-review.md`. The source-backed boundary is [R4a capture/setup](../../../.kiro/specs/analyst-workspace/range-capture-design.md). No browser, provider request, image build or Range appearance claim belongs to this inactive slice. Next: effective appearance, axes/layout and application/editor integration, followed by retained-FMP image acceptance.

## R4b inactive series appearance accepted

Workspace `912f97e1732bfd1b8d91c110e8e37b19a559233c` resolves Range Bar/Area field styles from the selected theme, generated options and saved overrides. The helper preserves original label defaults, independent marker paint and generated-only filtering. It remains inactive; axes, editor integration and real-FMP application acceptance are still open.

Independent source review accepted the two new production modules and focused test. Review corrected array merging between theme layers so a higher-priority dash pattern replaces the lower pattern completely; saved/generated composition retains its existing semantics. Missing-module RED preceded implementation. All 42 focused tests and scoped Biome pass. Explicit-scope complexity passes the 400/300/50 limits. Canonical typing is byte-identical to the accepted baseline: 2,711 inherited diagnostics, exit 2, with no new diagnostics. This is not a clean typecheck.

Local evidence is retained in `artifacts/chart-range/r4b-*.log`, `.exit` and `r4b-review.md`. See the [series appearance contract](../../../.kiro/specs/analyst-workspace/range-series-appearance-design.md). No browser, provider request or image build was required for this inactive source slice. The published alpha remains unchanged.
