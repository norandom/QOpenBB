# Historical gallery capture evidence

Reviewed on 2026-10-27. The overview and 36 chart screenshots are accepted visual evidence from the capture candidate. Local packaged gallery integration was accepted on 2026-10-28 as recorded below. Publication of [alpha-40652638534-1](https://github.com/norandom/QOpenBB/releases/tag/alpha-40652638534-1) is verified separately in the [release review](publication-review.md).

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

## Historical first-open failure and correction

The complete `initial-10` browser test exited **1**, after the captures, because an immediate Custom Combination edit reverted from area to line. This failed journey is not reported as a passing end-to-end test.

A bounded follow-up reproduced the issue directly after opening the Apps card, without a long gallery tour or resize. Saving and reloading the same dashboard allowed the native edit to succeed and be posted, preserving the EPS secondary axis. Separate fresh-session save/reopen checks also passed. The save/reload boundary probe exited 0 with empty diagnostics; its retained evidence SHA-256 is `366ceb664fd2e23701eb2c7b833fd1240c7ed7f40669bbde2514e43a06fb9d13`.

This workaround is no longer required in the accepted local candidate below. The earlier failures remain historical evidence and are not relabelled as passing tests. The corrected gallery is now included in [alpha-40652638534-1](https://github.com/norandom/QOpenBB/releases/tag/alpha-40652638534-1); its image publication is verified separately.

## Accepted packaged persistence, 2026-10-28

Independent review accepted the first-open correction and retained-state journey. Workspace image `sha256:4e60fe498e3272908700d9ad206160ce7d5e5f17a775570d4927b65572e7be70` was built through Dagger from root `be828b6305e2632b6bf7afe60ea64d885f106ae1`, Workspace fork `d6208dd3d44e46760d39c80da47c0b681b91e151`. The data API image and historical datasets above are unchanged. Final verification source `f399e01ee9bb73f55ba36c95318ce7773188f20b` differs from that packaged fork only in the persistence test.

- The native schema correction preserves absent chart-family keys instead of adding undefined entries. Two new regressions failed before the correction; all 17 focused tests passed afterward. The integrated validator is unchanged. See the [reviewed schema exception](../../../.kiro/specs/analyst-workspace/gallery-schema-exception.md).
- The initial one-worker browser run passed in 41.9 seconds: first-mounted area assignment without reload, EPS secondary axis, native resize, exact snapshot refresh, financial tooltip, PNG export, native save and fresh authenticated reopen.
- Both Compose containers were force-recreated. Their container IDs changed; their exact images and the Workspace bind directory remained the same. Health and login passed after replacement.
- The corrected reopen run passed in 45.9 seconds. All 48 native widget instances covering 36 chart types, their saved chart states and the complete layout survived. Dark theme persisted. Opening the Apps gallery produced a numbered copy and left the edited original unchanged.
- Both runs passed input-integrity checks and had empty diagnostics in both authenticated contexts. The diagnostic helper actually opened Chrome DevTools sessions and enabled Runtime and Log observation. Snapshot responses matched exactly; no live provider API requests occurred.
- Separate route recovery returned the expected unknown-dataset 404, then an exact valid snapshot 200; the subsequent application rendered the valid widget.

The first reopen attempt failed while collecting Overview response bodies after navigation. Its corrected test waits for those bodies before navigating and closes the old page before a second login replaces its session. No failed response or diagnostic is filtered out. `reopen-1` remains failed evidence; `reopen-2` supplies acceptance.

The 37 published screenshots retain their original capture identities above; they were not recaptured or substituted. Standalone Area item-hover behavior remains unverified. This local acceptance does not establish CI-image browser testing, backup/restore or owner-server deployment.

### Retained evidence hashes

| Local evidence | SHA-256 |
| --- | --- |
| `artifacts/historical-gallery/persistence/initial-1/browser-output/historical-gallery-persist-3798f-pen-and-retained-recreation/historical-gallery-persistence.json` | `b803cfd671d708ee85f2aada57f4f9adcbec0e80328a9852719342d3a6db67a9` |
| `artifacts/historical-gallery/persistence/reopen-2/browser-output/historical-gallery-persist-3798f-pen-and-retained-recreation/historical-gallery-persistence.json` | `2d1da4dc184e63b51a9bd274f14094bd91dcc1424afb37f90e03149b7380d1a5` |
