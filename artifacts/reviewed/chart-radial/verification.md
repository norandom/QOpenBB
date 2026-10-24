# Radial source checkpoint

The inactive Radial renderer, controls and Column geometry helper are independently accepted. Radial charts are connected in the accepted application source; the published Nightingale alpha remains unchanged.

| Slice | Workspace commit | Verified scope |
| --- | --- | --- |
| RC0C | f18bb5c | Frozen control declarations and fixture; exact-byte materialization review |
| RC2 | 2339c73 | 11 focused tests, lint, no added typing diagnostics; existing four retained |
| RC0G | 26f1c8c81333bf7cb09f69cc3e24d213bd7c4096 | 30 actual ECharts path/boundary tests, strict typing and lint |

The combined inventory-backed gate passes with zero errors or violations. All new production files meet 400 physical lines, 300 logical units and 50 per function. The source commits are separate; application routing is unchanged.

The control review caught and corrected the explicit-stroke fallback: an explicit stroke without width resolves to width 1, while palette-only strokes stay at width 0. The geometry review caught large finite pixel overflow; inputs above 1,000,000 pixels now reject without clamping. This is a geometry bound, not a restriction on financial values.

Reviews: [controls contract](controls-contract-review.md), [materialization](controls-materialization-review.md), [controls](controls-review.md), [geometry](geometry-review.md). [Original observations](original-observations.md) distinguish the passing Bar journey from the retained Column normalized-missing failure. The bounded hover probe and the source early return are separate evidence.

## Remaining decisions and work

The owner approved keeping valid Column observations visible when another category is missing. RC0 is now frozen after independent numerical review. Real-FMP packaged comparison and publication remain open. Treemap/Sunburst are queued directly afterward.

The retained FMP AAPL quarterly cost-of-revenue and gross-profit fixture reconciles to reported revenue. No new provider fetch or replacement FMP screenshot is claimed at this inactive checkpoint. Financial chart samples will accompany packaged acceptance.

## Numerical boundary freeze

RC0 is independently accepted at Workspace fa7f464bf7ca95248b755971c08ffcd5730236ae. The prepared-pixel model and shared compact fixture pass scoped typing with the same four inherited diagnostics; the combined gate has no errors or violations. See [renderer contract review](renderer-contract-review.md). Numerical preparation and painting have exclusive files; neither changes routing. No new runtime or image acceptance is claimed.

## Accepted inactive renderer

Numerical preparation is committed as 2ced45c54fa27fb64429ccac0432a456f1222ec0; painting and translation as 767512f4b86467d39d36663be9299e2c97f73a9e. The independent joined run passes 23 tests. Twelve additional adversarial model combinations and the final combined complexity gate pass. Lint passes and scoped typing retains the same four inherited diagnostics. Actual ECharts paths, raw click identity and count labels are covered. See [numerical review](numerical-review.md), [paint review](paint-review.md) and [integration plan review](integration-plan-review.md).

The owner-approved missing-value correction is implemented in numerical preparation. At that renderer checkpoint, live routing and packaged acceptance remained open. Application source acceptance follows below.

## Application integration

Readable series names were repaired in 974e4f8a5d241dd99e377182b33f987886223e9a, preserving internal IDs for selection. Application integration 2831436bc1eefb9030d2ab1c154f67603f58689a passed independent review: the 80-test integration suite, 45 model tests, final 44-test Histogram/session join and 28-test readable-label join pass. These runs overlap and are not a count of distinct tests. Lint and the combined cap gate pass.

Strict baseline/current each report 2,680 inherited primary diagnostics. The Histogram intent narrowing regression was fixed; 26 remaining message-order variants were independently reviewed. See [application review](application-review.md). This is no clean-compile or packaged-runtime claim.

[Browser preparation](browser-preparation-review.md) at f9b29ddd4e2d1367f08eafe67e82e2a8a357f320 was reviewed and statically checked before the initial candidate runs. That pre-refinement image was not used for final acceptance; final packaged evidence follows.

## RC4 packaged and appearance acceptance

RC4 is independently accepted on the local Dagger candidate image `sha256:f1b71c759334ea08bf1a197a12ce855ac5252ab2d0acd87469f1398dae0f5291`, built from Workspace `9d007b2f40b65ec5f1e2e760787a9fc2d9e4e3d5`. The Column retained-FMP journey passed once in 360.243 seconds; the Bar journey passed once in 274.652 seconds. Both ran serially with one worker, zero retries, skips or errors. The independent final review verified image/runtime identity, exact retained AAPL FY2025 reported-USD tuples, grouping and control effects, unchanged CSV refresh, fresh-session reopen as the final operation, and UI PNG export. Original comparisons remain separate; their retained CSV request/console diagnostic is disclosed.

The owner approved both final appearances with “Keep these appearances.” The [independent RC4 review](final-acceptance-review.md) records evidence boundaries and the remaining layout differences. Compact [real-FMP comparison samples](real-fmp-samples.md) preserve the four owner-reviewed light-theme original/replacement PNGs; final browser evidence also covers both dark-theme captures. This is local application acceptance only. RC5 publication, registry identity verification and anonymous image pulls remain open; the pre-existing Nightingale alpha is unchanged.
