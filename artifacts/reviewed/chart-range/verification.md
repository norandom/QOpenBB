# Range chart verification

Range Bar/Area source integration is independently accepted through R4i below. Packaged-image behavior, original-runtime comparison, real-FMP application acceptance and publication remain open. The published Box alpha is unchanged. Earlier sections retain their historical acceptance boundaries.

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

## R4c inactive numeric value axis accepted

Workspace `491d6caaf0653a52675d54756eb642e65cc0c443` adds the shared Range numeric value-axis planner. It retains raw financial bounds, applies the accepted linear nicing/tick arithmetic, and crops ticks to the visible interval. Equal values keep their raw value; empty data remains distinct. The existing Box arithmetic now has one neutral owner with compatibility exports for unchanged Box callers.

Independent source review accepted the extraction and planner. Missing-module RED preceded implementation; 49 focused cases and 140 cases in the affected Box/Range join pass, including actual ECharts SVG handoffs. Initial test expectations were corrected for source nicing and ECharts automatic margins; failed logs remain local. Two test-only type errors were corrected and the focused cases rerun after the join, with production unchanged. Read-only Biome and explicit-scope complexity pass. Final canonical compatibility typing matches the pre-change baseline: 3,430 inherited diagnostics, exit 2, with no new diagnostics. This is not a clean typecheck.

Local commands/results remain under `artifacts/chart-range/r4c-*.log`, `.exit` and `r4c-review.md`. The [numeric axis contract](../../../.kiro/specs/analyst-workspace/range-value-axis-design.md) owns the scope. Numeric/date category positioning, calendar ticks, controls and application layout remain open. No browser, FMP acceptance or image rebuild is claimed for this inactive slice.

## R4d continuous category geometry accepted

Workspace `c348a497451df7d876ee127a0a0463f66807c95d` accepts supplied numeric/time coordinates in both inactive Range renderer cores. Uneven spacing, partial windows and observation identity now pass through to actual ECharts geometry. Shared coordinates were committed in `ac12958`, Area in `430a0f3`, and Bar in `c348a49`. Ordinal layout remains supported.

Independent foundation, Bar and Area reviews accepted the source. The joined suite passes 135 tests across ten files, including SVG rendering, both Bar directions, Area path order, supplied ticks and tooltip identity. After a test-only typing correction, the 13 focused Bar checks pass again; production is unchanged. Read-only Biome and explicit-scope complexity checks pass. Canonical compatibility typing is byte-identical to the baseline: 3,430 inherited diagnostics, exit 2, SHA-256 `cd29c0233988b1603d38ade018eb62bcdfe1d31234624e7d0a4d4bc4f1749c5e`. This is not a clean typecheck.

The [category geometry contract](../../../.kiro/specs/analyst-workspace/range-category-design.md) defines the accepted boundary. Local RED/GREEN logs, join results and three independent reviews remain under `artifacts/chart-range/r4d-*`. Caller Date inference, calendar tick selection, hierarchical labels, final application layout/navigation and source-exact pointer interaction remain open. Real-FMP application samples and acceptance are pending. These cores remain inactive; this slice does not rebuild or change the published alpha.

## R4e category capture accepted

Workspace `5e85724c93701d86024dce2e3587a83510542c14` retains the first selected raw category's Date identity and actual Grid column chart metadata before statistical normalization. Capture now resolves the source category kind using model override, column metadata and first-row evidence in that order. Explicit category metadata prevents Date inference; raw numbers alone remain categorical. The validated snapshot keeps these facts through statistical setup aggregation without changing observation rows or Box capture.

Independent review accepted the capture integration and focused regression evidence: 225 affected tests pass, including actual Grid capture, selected bounds, single category-cell reads, metadata precedence and setup retention. After three test annotation corrections, the 40 focused cases pass again with production unchanged. Scoped Biome and inventory-backed complexity checks pass. Canonical application typing matches the unchanged baseline of 3,432 inherited diagnostics, exit 2 (SHA-256 `2507c8e0ac2007713421ce316cfe863d63aef5d5cd9ee4307677c40abc108799`); this is not a clean typecheck. Local commands/results and review remain under `artifacts/chart-range/r4e-*`.

The [capture contract](../../../.kiro/specs/analyst-workspace/range-category-capture-design.md) defines this input boundary. Calendar planning, current-model editor selection, full Range session wiring, pointer behavior and real-FMP browser acceptance remain open. Range is not activated and the published alpha is unchanged.

## R4f composed application mapping accepted

Workspace `9f5a9c2d22d99fcd72d7721705c6e2fe0a6dfd43` composes Range Bar/Area projection, saved styling, captions, legend and measured axes into actual ECharts output. Numerical and calendar categories retain their coordinate identity; existing MIT Community calendar helpers supply local/UTC interval arithmetic without creating an AG chart. Reversed axes preserve endpoint labels and Area hit rectangles. Empty plot space produces no glyphs.

Independent review accepted the final source after correcting ignored saved tick spacing, explicit-step singleton labels, undefined optional bound precedence and colliding Area series IDs. The joined checks pass 226 Range compatibility tests across 17 files and seven composed application tests. These include actual SVG output and native-Date Grid capture through setup into composition. Read-only Biome passes 36 files; explicit-scope complexity has zero errors or violations across the 28 changed production files. Canonical application typing is byte-identical to accepted `5e85724`: 3,432 inherited diagnostics, exit 2, SHA-256 `2507c8e0ac2007713421ce316cfe863d63aef5d5cd9ee4307677c40abc108799`. Scoped strict compilation covering every new/changed test retains only inherited typography.ts TS2578; neither result is a clean typecheck.

The [application contract](../../../.kiro/specs/analyst-workspace/range-application-design.md) owns this boundary. Commands, RED/GREEN logs, source hashes and independent review remain locally in `artifacts/chart-range/r4f-*`; joined suites ran with one worker and `TZ=Europe/Berlin`. Live session/editor activation, navigator and pointer wiring, save/reopen/export, real-FMP browser samples and publication remain open. The published Box alpha is unchanged; no image or visual acceptance is claimed here.

## R4g live Range integration accepted

Workspace `1a692c8fe1e78825aded85d4fa0b905eef77eddc` connects Range Bar/Area to the ordinary Table/File caller, existing session and editor, navigator and pointer lifecycle. Saved category semantics and axis preferences survive transactions and fresh-owner reopening. Separate physical-axis windows preserve horizontal navigation; each redraw supplies current geometry to tooltip selection. Retained MIT Community scale and spatial helpers provide calculations without creating an AG chart.

Independent review approved the source after five corrections: drag suppression across redraws, endpoint-independent Area selection identity, asymmetric reversed-axis autoscaling, single error reporting after a failed double-click, and ordinal band-leading-edge autoscale conversion. Fresh joined application checks pass 176 tests across 13 files, lifecycle passes 31, and the final navigation/pointer suite passes 32 across eight files. These totals include installed-ECharts rendering and transport checks; they are not browser acceptance.

No-fix formatting passes all 71 changed source/test paths. Explicit inventory-backed complexity passes all 54 production paths with maxima 392 physical lines, 231 logical units and 43 units/function; zero errors or violations. Canonical TypeScript retains the same 3,432 inherited diagnostic headers after line/column normalization, compiler exit 2. The comparison is recorded in `artifacts/chart-range/r4g-typing-comparison.json`; this is zero new diagnostics, not a clean typecheck.

Local commands and outputs: `r4g-join.sh`, `r4g-lifecycle.sh`, `r4g-b-green-final.log`, `r4g-biome.log`, `r4g-complexity.json`, and independent `r4g-review.md`, under `artifacts/chart-range/`. The [live contract](../../../.kiro/specs/analyst-workspace/range-live-design.md) owns this boundary. Actual packaged-image behavior, retained-runtime navigation comparison, FMP financial/appearance checks, browser save/reopen/export and samples remain open. No Range image publication or visual acceptance is claimed; the published Box alpha remains unchanged.

## R4h integrated zoom defaults

Workspace `6188a1f651f2c29f3bfa5ea16f9b91749856a465` restores the original Workspace zoom defaults at the Range caller boundary: enabled wheel/pan, pointer anchors, four configured visible items and dependent autoscaling. Defaults have lower precedence than explicit theme, generated and effective saved-family settings. Ordinary callers and standalone engine defaults remain unchanged.

Independent review accepted the three-file repair. Eight focused caller tests pass, including actual navigation carriers with both navigator controls hidden and explicit override checks. Reconstructed baseline evidence shows the two new cases fail against committed R4g; it was captured after implementation because WSL was temporarily unavailable, and is not historical TDD evidence. Final formatting and two-file complexity checks pass. Canonical typing retains 3,432 inherited diagnostic headers with zero normalized delta, compiler exit 2. Review and logs remain under `artifacts/chart-range/r4h-*`. Packaged browser/FMP and original-runtime acceptance remain open.

## R4i original appearance refinement

Workspace `07b91c8163f9b502c1188fd56bcab052e6ab9a40` implements the requested Range-only appearance refinement: Area endpoints reach the plot edges, year labels use the original wrapping/collision rules, and Area legends combine a line with an outlined marker. Bar grouping and explicit saved settings remain supported. The owner requested this closer match after comparing the first packaged candidate in qView; the refined packaged appearance is not yet accepted.

Independent review accepted eight production files and the new appearance regression. The focused application run passed 18 cases; after the final legend-only correction, all 11 appearance cases passed, including diamond/triangle outline bounds. The final affected category/navigation/pointer run passed 62 cases across nine suites. These are separate executions, not one combined run. No-fix formatting and inventory-backed complexity pass: maxima 293 physical lines, 123 logical units and 36 per function. Canonical typing retains 3,432 inherited diagnostics, compiler exit 2; its log is byte-identical to R4h. Local review and commands are recorded under `artifacts/chart-range/r4i-*`.

The earlier packaged source `6188a1f` passed real-FMP Bar and Area behavior journeys: raw quarterly extrema, controls, navigation, refresh, fresh reopen and sampled PNG export. Bar passed within a combined run that failed on an Area observation helper; the corrected Area-only run passed. Independent review recomputed all 40 source observations and 22 extrema per family. These results predate R4i and do not verify its new legend image decoding or appearance.

The retained original passed financial geometry assertions before a later observation failure. A focused original run recorded an unchanged default-wheel frame and slider cropping of the value axis. Its explicit autoscale-off contrast failed after reload, before the second wheel. Untimed native errors prevent attributing the default-wheel outcome solely to autoscaling. Neither original run passed overall. These limitations remain open; no full parity claim is made.

Next: inspect the refined packaged image, verify actual legend paint/export, obtain visual acceptance and publish selected real-FMP samples. The published Box alpha is unchanged.


## R4i packaged checkpoint, 2026-10-23

The owner accepted the refined default Range Area appearance in qView: every-year labels, unwrapped partial-year labels, flush plot edges and outlined square/line legend samples. This decision covers the default view, not the navigator layout.

The identified packaged image `sha256:f488a8c3447ef9a94b088919416ca4d6cdffc4d419c4238000f3733d8c433a2d` contains application source `07b91c8163f9b502c1188fd56bcab052e6ab9a40`. Bar passed its complete retained-FMP journey in `browser-07b91c8-1`; Area passed the focused `browser-07b91c8-area-2` run after a test-only precision repair. The first combined run remains recorded as one pass and one failure. Area miniature y coordinates differed by 0.000040 CSS pixels; the repaired assertion allows at most 0.001 CSS pixels while retaining exact marker count, x/order and diameter. Bar comparison and financial assertions are unchanged.

Both completed journeys check controls, navigation, refresh, fresh-session reopen, financial geometry and PNG export. Direct inspection confirms the Area outlined legend/line samples paint in the application and export. The fixture contains 40 historical AAPL quarterly observations grouped into 11 fiscal years: independent minimum/maximum revenue and net income in raw reported USD, not annual totals or OHLC. Default-light original and replacement screenshots use the same fixture; default-dark parity is not claimed. Original geometry checks passed before a later reference navigation failure, which remains disclosed above.

Independent review accepts this refinement and test repair, but rejects full Range completion pending one concrete layout repair: the miniature begins below the plot without allowing space for the main axis labels, causing overlap. This existed before R4i and is not covered by the owner's default-view acceptance. No new Range release is claimed.


## R4j navigator label spacing

Workspace `8047c093f16fb04c62afb22ced8104651aa95118` places the navigator after the measured bottom-axis label/title footprint instead of a fixed ten-pixel plot offset. It reuses the resolved axis settings and final rotations, accounts for miniature labels on a top-positioned axis, and preserves the main financial plot, navigation controls and full data domains. No new feature eligibility rule is introduced.

Independent source review accepted the production change and five layout regressions. The final affected run passes 16 tests across navigator layout, live projection and navigation windows. The initial RED run includes five meaningful layout failures plus an abandoned tiny-widget policy case; that extra case and its proposed behavior are absent from the final code. No-fix formatting passes. Corrected inventory-backed complexity reports no errors or violations: 196 physical lines, 54 logical units and 14 units in the largest function. An earlier scope run failed on a stale data API base revision and is not counted as passing. Scoped TypeScript baseline/current diagnostics match exactly: one inherited typography TS2578, zero additions; this is not a clean full-project typecheck.

Source acceptance permits a new candidate build, not full Range completion. The next gate is the identified packaged navigator layout and PNG export. Commands/results and independent review remain in local `artifacts/chart-range/r4j-navigator-*` and `r4i-packaged-review.md`. The published alpha remains unchanged.


## R4j packaged rejection and hidden-miniature correction

The packaged `8047c09` image failed both Range journeys before family selection completed (`browser-8047c09-1`, two failures). With a top legend, hidden navigator and enabled zoom, the spacing change attempted to project an unused miniature outside the viewport. The renderer rejected its geometry. The earlier layout fixtures did not exercise this combination. This image is not accepted and was not released.

Workspace `e2b87ed98cd5ef18fb9ca6ddf888802d71fc685e` skips miniature projection when the miniature is disabled. It preserves the visible-miniature spacing correction, inside zoom carriers, wheel/pan settings and existing control eligibility. Both real-default cases fail against the previous source and pass after the repair, including installed-ECharts rendering with finite SVG output and explicit wheel/pan assertions.

Independent review approves this source correction for a new build. The final focused run passes 18 cases across three suites; formatting and complexity pass (200 physical lines, 54 logical units, largest function 14). Exact scoped baseline/current TypeScript diagnostics retain one inherited typography TS2578 and zero additions. These checks do not replace packaged acceptance: both Range journeys must pass in the rebuilt image before milestone completion or publication.


## Range packaged acceptance

The corrected packaged image `sha256:1ff9d136027b0e0ae0f55b89f3faae5892602b2aeb3cee5482f408dc3a3bb0b0`, built from Workspace `e2b87ed98cd5ef18fb9ca6ddf888802d71fc685e`, passes both retained-FMP Range journeys in one run: `browser-e2b87ed-1`, two passed, exit 0. Independent review accepts the ordinary Table/File Range Bar/Area milestone. This supersedes the failed `8047c09` candidate; its failure and repair remain recorded above.

The checks cover actual raw-USD quarterly extrema and tooltips, editor controls, theme/direction changes, miniature stability, slider/wheel/pan/reset, legend toggling, refresh, fresh-context save/reopen, and PNG export with sampled financial-pixel comparisons and browser diagnostics. Direct inspection of both exports confirms separation between main-axis labels and the miniature. The Area outlined-square/line legend also paints correctly in the exported image. No new provider request is claimed: these are the retained historical FMP observations described above.

The owner accepted the refined default Area appearance on 2026-10-23. Long partial-year labels can still clip at the outer canvas boundary, as they do in the original default view. This acceptance covers the bounded Range journey, not exact pixel equality, all renderer families, assembled deployment, or the previously unverified original autoscale-off contrast. Registry publication remains a separate gate.


## Published Range alpha

[alpha-39920081345-1](https://github.com/norandom/QOpenBB/releases/tag/alpha-39920081345-1) publishes both service images after hosted checks and Dagger builds. The release manifest pins the accepted Workspace source `e2b87ed98cd5ef18fb9ca6ddf888802d71fc685e` and data API `cab81b16bb9ef49272a6f3b0bf04cf9f34bde0ba`. Both services passed anonymous pulls by immutable digest, alpha tag and `latest`; remote manifest/config identities, source labels and release installation assets were verified.

The [manifest](release-manifest.json) records the exact pair and [anonymous pull evidence](anonymous-pulls.json) records all six pulls. Local browser acceptance used image `1ff9d136`; the CI images are separate build outputs from the same pinned source. Their publication checks do not claim browser execution against the CI image bytes, assembled Compose runtime acceptance or owner-server deployment.
