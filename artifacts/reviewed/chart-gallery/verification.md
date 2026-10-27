# Historical gallery capture evidence

Reviewed on 2026-10-27. The overview and 36 chart screenshots are accepted visual evidence from the local candidate. They do not establish completed gallery integration or release acceptance.

The overview is one application capture containing twelve widgets, not a montage. Each chart image is an unchanged native widget capture. The existing [sync manifest](../sync-manifest.json) records every source path, exact source/published SHA-256 and byte count. Raw browser output and authentication state remain private and ignored.

## Candidate and data

| Component | Captured identity |
| --- | --- |
| Workspace image | `sha256:362b5b37026f735a80487315c290163d9f98a06d5ce6133d43525d679a6b14cc` |
| Workspace fork | `cbe148b36365b9ffae2e841fe6fb1ea0eef095c2` |
| Workspace build root | `806f7f82b04ebce33dfbe98c6004adbc3ae6eaa6` |
| Data API image | `sha256:37e2d9f5c0fe0e9c0c97f3d1280a0441bfaeecc1777694d144b4ee97af9e9904` |
| Data API build root | `c6f6b150923aa1866af115e4fb0a28c506ababa0` |
| Snapshot | `fmp-historical-2025-01-v1` |
| Chart state SHA-256 | `c54619720b96fed6c29c09fc1e1f866867a2f9707f875bf1341360dc4a383d79` |
| Data SHA-256 | `e453f9067b2afd7eac12ba7cfbfabc39b1f188f7a207fbc42eefe4254d1fc60c` |

The [guide](../../../docs/chart-gallery.md) explains periods, formulas, units and interpretation. These are historical observations retrieved later, not a January 2025 information-vintage claim.

## What passed

- All 36 chart configurations rendered and were visually reviewed, along with the twelve-widget overview.
- The final capture run, `initial-10`, passed all 22 representative financial tooltip samples, with exact snapshot-response comparisons and empty console/page/request/HTTP diagnostic arrays. Fourteen additional variants have visual and dataset checks, not separate tooltip claims.
- The Treemap no longer reserves a blank white header for its unnamed virtual root. FY2024 and quarter headers remain visible. The other 35 chart PNGs are byte-identical to their previously reviewed captures.
- Input-integrity checks passed for the fixture, data, catalog and browser test inputs.

The standalone Area chart's default item-hover behavior remains unverified. The Line chart's successful Shared tooltip check does not establish Area hover support.

## Remaining integration boundary

The complete `initial-10` browser test exited **1**, after the captures, because an immediate Custom Combination edit reverted from area to line. This failed journey is not reported as a passing end-to-end test.

A bounded follow-up reproduced the issue directly after opening the Apps card, without a long gallery tour or resize. Saving and reloading the same dashboard allowed the native edit to succeed and be posted, preserving the EPS secondary axis. Separate fresh-session save/reopen checks also passed. The save/reload boundary probe exited 0 with empty diagnostics; its retained evidence SHA-256 is `366ceb664fd2e23701eb2c7b833fd1240c7ed7f40669bbde2514e43a06fb9d13`.

Until corrected, save and reload a newly opened gallery before editing combination-series types. Retained-state container recreation and publication of these gallery images in a tagged alpha remain pending. The repository screenshots are usable now; the currently published alpha is a separate, earlier delivery.
