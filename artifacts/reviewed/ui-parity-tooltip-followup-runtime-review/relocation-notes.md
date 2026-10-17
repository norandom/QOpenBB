# Resolve the frozen plan snapshot from its original base

Preserve the exact bytes of the [executed-attempt plan snapshot](../ui-parity-tooltip-followup/capture/attempt-20261017-tooltip-followup-a1/reviewed-plan.md). Its links were authored for the [canonical plan](../ui-parity-tooltip-followup/plan.md), which is `../../plan.md` relative to the snapshot. Copying the plan into the attempt moved its file location without rebasing its Markdown links. Eleven links consequently do not resolve from the snapshot directory.

This supplementary independent review, dated 2026-10-17, accepts preserving the snapshot as immutable provenance when this relocation note accompanies it. Use the public links below for navigation. They resolve each original target against the canonical plan's directory; they do not change the snapshot, its historical meaning, source hashes or execution claims. The canonical plan already has valid links. A future edited snapshot would require a separately labelled derivative and distinct published hash.

| Snapshot label | Original target text | Valid published destination |
| --- | --- | --- |
| frozen earlier plan | `../ui-parity-tooltip-plan/plan.md` | [Earlier plan](../ui-parity-tooltip-plan/plan.md) |
| outcome report | `../ui-parity-tooltip-plan/capture/report.md` | [Earlier outcome report](../ui-parity-tooltip-plan/capture/report.md) |
| independent source diagnosis | `../ui-parity-tooltip-review/runtime-review.md` | [Source diagnosis](../ui-parity-tooltip-review/runtime-review.md) |
| accepted acquisition review | `../ui-parity-tooltip-review/correction-1-review.md` | [Acquisition review](../ui-parity-tooltip-review/correction-1-review.md) |
| Baseline copies | `capture/baseline/harness` | [Baseline harness](../ui-parity-tooltip-followup/capture/baseline/harness) |
| Proposed collector | `capture/harness` | [Proposed harness](../ui-parity-tooltip-followup/capture/harness) |
| Explicit diff | `capture/source-diff.patch` | [Source diff](../ui-parity-tooltip-followup/capture/source-diff.patch) |
| caption helper's | `../ui-parity-captions/capture/journey.mjs` | [Caption helper](../ui-parity-captions/capture/journey.mjs) |
| five-row fixture | `capture/harness/fixture.json` | [Five-row fixture](../ui-parity-tooltip-followup/capture/harness/fixture.json) |
| static verification | `capture/static-verification.json` | [Static verification](../ui-parity-tooltip-followup/capture/static-verification.json) |
| offline verification | `capture/offline-verification.json` | [Offline verification](../ui-parity-tooltip-followup/capture/offline-verification.json) |

The twelfth snapshot link, `source-hashes.json`, happens to resolve to the attempt's copied manifest. Its intended canonical destination is [Source hashes](../ui-parity-tooltip-followup/source-hashes.json); the two files are byte-identical at review time. This coincidence does not rebase the other eleven links.

Verification checked all eleven mapped public destinations, both plan hashes and the copied/canonical source-manifest hashes. The [supplementary receipt](relocation-verification.json) records the results. APPROVED: exact-byte preservation with this explicit relocation map. This supplements the [bounded publication review](review.md) and grants no further runtime or semantic acceptance.
