# Radial source checkpoint

Inactive controls and the pure Column geometry helper are independently accepted. No Radial chart is activated, and the published Nightingale alpha remains unchanged.

| Slice | Workspace commit | Verified scope |
| --- | --- | --- |
| RC0C | f18bb5c | Frozen control declarations and fixture; exact-byte materialization review |
| RC2 | 2339c73 | 11 focused tests, lint, no added typing diagnostics; existing four retained |
| RC0G | 26f1c8c81333bf7cb09f69cc3e24d213bd7c4096 | 30 actual ECharts path/boundary tests, strict typing and lint |

The combined inventory-backed gate passes with zero errors or violations. All new production files meet 400 physical lines, 300 logical units and 50 per function. The source commits are separate; application routing is unchanged.

The control review caught and corrected the explicit-stroke fallback: an explicit stroke without width resolves to width 1, while palette-only strokes stay at width 0. The geometry review caught large finite pixel overflow; inputs above 1,000,000 pixels now reject without clamping. This is a geometry bound, not a restriction on financial values.

Reviews: [controls contract](controls-contract-review.md), [materialization](controls-materialization-review.md), [controls](controls-review.md), [geometry](geometry-review.md). [Original observations](original-observations.md) distinguish the passing Bar journey from the retained Column normalized-missing failure. The bounded hover probe and the source early return are separate evidence.

## Remaining decisions and work

The owner approved keeping valid Column observations visible when another category is missing. RC0 is now frozen after independent numerical review. Family numerical mapping, live controls/session integration, real-FMP packaged comparison and publication remain open. Treemap/Sunburst are queued directly afterward.

The retained FMP AAPL quarterly cost-of-revenue and gross-profit fixture reconciles to reported revenue. No new provider fetch or replacement FMP screenshot is claimed at this inactive checkpoint. Financial chart samples will accompany packaged acceptance.

## Numerical boundary freeze

RC0 is independently accepted at Workspace fa7f464bf7ca95248b755971c08ffcd5730236ae. The prepared-pixel model and shared compact fixture pass scoped typing with the same four inherited diagnostics; the combined gate has no errors or violations. See [renderer contract review](renderer-contract-review.md). Numerical preparation and painting have exclusive files; neither changes routing. No new runtime or image acceptance is claimed.
