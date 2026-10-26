# Stacked Line atomic join review

2026-10-26. **Final SL2 source-gate verdict: APPROVED with the exact inherited TypeScript qualification below.** Both requested repairs are resolved, and joined regression, lint and inventory-backed complexity evidence is accepted. This closes the shared source-verification conditions on the independently approved A/B lanes and atomic J integration. It does not accept SL3 browser/candidate behavior or publication.

## Final joined verification

Independently inspected the completed artifacts: `join/compatibility.log` records 178 passing tests across nine files; `join/application.log` records 53 passing tests across five files. `join/lint-final.log` records a nonmutating check of 24 files with no fixes. Earlier formatting output remains separate in `join/lint.log`.

`complexity.json` reports combined acceptance passed, with no errors or violations. All 20 inventoried Workspace production files are within the whole-file limits; maxima are 304 physical lines, 115 logical units and 29 units per function. Explicit Workspace and unchanged data_api manifests remain controller-owned. The existing checker and shared-module audit are used; no exception or uncapped extraction is introduced.

Fresh strict same-root comparison in `typecheck.json` reports 2,791 baseline and 2,789 candidate diagnostics, one textually added diagnostic and raw failure. **This is not a clean compile or an unqualified zero-added comparison.** Independently compared the sole added candidate with its baseline counterpart: unchanged `src/lib/types/app.ts`, TS2345, start 2080, length 26. Both have exactly the same ZodOptional/ZodDefault/ZodEnum-to-`$ZodRecordKey` incompatibility chain, ending in `string | undefined` versus `string | number | symbol`. Only the displayed order/subset of truncated enum members changes. This exact pair is adjudicated as inherited diagnostic rewording; the raw failed result is retained. There are no candidate diagnostics on the frozen owned root files and no other added diagnostics. Foundation raw evidence is retained separately; no broad suppression or unrelated typing repair is approved.

Final reviewed J hashes: `cartesian.ts` SHA-256 `30eba31f1c8b7f9f16502f015dd3e106fba65855e4a83ceb4b6318725ecc9721`; `cartesianTooltip.ts` `311e4fc908eab46b66f50c71fd4fa774e42b887e1300aa3916b786e56aba2691`; session projection retains the repair hash below. No production edits or heavy tests were performed by this reviewer during final evidence adjudication. No blocking source findings remain.

## Repair re-review

Independently reread the two frozen repair files. The legend callback recognizes `line-stack-overflow`, creates the shared `LineStackOverflowError`, and preserves the diagnostic code and specific cumulative-amount explanation in its message. The existing lifecycle catches this error and releases the renderer; no new state or renderer owner is introduced. The new cancellation/visibility test starts from a ready session and requires the specific diagnosis when the cancelling middle series is hidden.

The session fixture now enables navigator and miniature. Both variants assert two grids, four line series, changed main geometry after hiding revenue, unchanged miniature data, and explicit full-context cumulative overview values. These assertions close the earlier test-name-only claim.

Inspected `join/review-fixes-red.log`: three relevant failures before repair, including both overview cases and the lost overflow diagnosis. `join/review-fixes.log` then records all eight tests passing. Reviewed SHA-256: application session projection `c412894af205e4171722b1845310a55f3c9bb634e6b10f95d4df3aaa30502f0d`; session test `289994482a485cab25dee9ee5e44c65b5495b47f275c0d8fc1c2521b72670d17`. No reviewer heavy checks were run while the controller gate was active. No blocking source findings remain; final acceptance still waits for the joined gates.

## Historical first review (resolved)

Initial verdict: REJECTED pending legend-error preservation and an overview assertion, as recorded below.

## Required remediation

1. **Important:** `applicationSessionProjection.ts` discards failed legend translation diagnostics and throws only `Invalid chart legend projection`. A valid stacked row `[MAX_VALUE,-MAX_VALUE,MAX_VALUE]` has finite prefixes; hiding the middle series makes the required second visible prefix overflow. The translator correctly produces `line-stack-overflow`, but the callback replaces its useful financial diagnosis with generic text. Preserve that code/message through the existing lifecycle error boundary and test this visibility-triggered failure. Existing lifecycle catches interaction failure and releases the renderer, so no new session or renderer owner is needed.
2. **Important verification gap:** the new session test claims a full overview but leaves navigator/miniature disabled and checks only main series. Enable the existing miniature path in a focused test and assert that legend reprojection changes main cumulative geometry while the overview retains the original full selected-series data. This is a required joined contract, not proven by the present test name.

## Supported integration

The controller admits exact line tokens through the existing Cartesian guard while leaving bar normalization admission unchanged. New projection runs before rendering; raw values feed labels/tooltips and derived values feed coordinates. Percentage tick formatting uses the explicit empty flag. Translator overflow maps to a specific invalid diagnostic without partial options. Shared/single/compact tooltips filter their raw row by finite drawn admission, preserving existing callers when no drawn snapshot is supplied. Session identity/stamps and raw storage remain with existing owners.

The foundation test update is appropriate for this explicit controller join amendment: it now expects admitted variants while retaining rejection from the bar normalization predicate. Historical inactive-guard evidence remains at foundation `21b3515`; no half-admission commit is authorized.

## Evidence and boundary

Inspected current J production diffs, the session test and updated foundation test. `join/red.log` shows seven expected unsupported-family failures; `join/green.log` shows seven passing tests. No reviewer heavy check was launched during the controller gate. Final approval waits for the two remediations and joined verification evidence. A/B files and other lanes were not edited; only this report was written.
