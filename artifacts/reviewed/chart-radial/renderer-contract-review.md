# RC0 final numerical contract review

## Review Verdict
- VERDICT: APPROVED
- TASK: RC0 numerical/interface freeze and exclusive RC1 lane plan, under radial-milestone.md Acceptance contract and Work and dependency queue, and radial-contract.md Numerical boundaries and Rendering design.
- MECHANICAL_RESULTS:
  - Tests: NOT RUN; this is a contract review, not implementation acceptance. No build or browser ran.
  - TBD/TODO grep: CLEAN in the three freeze artifacts; command exited 0.
  - Secrets grep: CLEAN for concrete token/private-key markers in those artifacts; command exited 0.
  - Static checks: SPOT_CHECKED declarations and existing callers; declaration materialization/typecheck remains controller work before dispatch.
  - Boundary: WITHIN; author owns contract.md, interfaces.ts and report.md only. This reviewer owns review.md only.
  - Boundary audit: CLEAN after explicit label anchors, axis stroke primitives and rotation corrections.
  - RED phase: N/A for contract-only work; required for subsequent behavioral implementation.
- FINDINGS:
  1. Resolved: full-turn Column rotation now uses the modulo angular difference, preserving the source top-facing one-row shape rather than an arithmetic midpoint.
  2. Resolved: prepared marks expose source label anchors independently of shape orientation, including the original one-row Column distinction and modulo-angle Bar label placement.
  3. Resolved: explicit category/numerical circle and ray primitives let paint apply independent axis styles without reconstructing geometry from offset labels.
  4. FYI: original source evidence and original run-3 observations remain distinct. The retained Column failure is not a passing test; the owner-approved missing-observation correction is explicit.
- REMEDIATION: None for this bounded freeze. Subsequent implementation, inventory/cap checks, independent review and packaged acceptance remain required.
- SUMMARY: The frozen prepared-pixel boundary supports two disjoint inactive implementation lanes without transferring normalization, geometry or session ownership to paint.

## Evidence and scope

Reviewed final SHA256 identities: contract.md `433e0c61149a69f6c3b55ce9e4b62d8cdbb69f05ad2f7f8b64e640287b318509`; interfaces.ts `171abf701242426b48df174229feeb165d85cef346b7e72685862c504f188bab`; report.md `3e592898e35b06bad653cf1037379c052a2b1458004325812bcc59b200a0d40e`. Final Bar label correction was read back from disk before acceptance.

Reviewed existing Workspace HEAD `26f1c8c81333bf7cb09f69cc3e24d213bd7c4096`, accepted radialContracts/radialAppearance/radialAssignments and radialColumnShape, the maintained milestone and contract, original-contract.md, angle-scale/report.md, analytical geometry report, and original/run-3/review-summary.md. Narrow fresh reads of the pinned installed E/C bundles confirmed BandScale arithmetic and its singleton rule, descending Bar radius mapping, signed angular endpoint swap, Column width/rotation/baseline conditions, and the special angular nice-domain extension. These are source checks, not new application observations.

Raw financial values and stable row IDs survive missing filtering and normalization. Hidden series change totals, domains and group slots while preserving legend and palette identity. Zero-denominator normalized rows have no marks. The Bar domain fixtures preserve normalized 100 as 225 degrees in a positive domain [0,160]. Invalid numerical geometry uses the existing invalid envelope. No Nightingale cast, setup replay, routing change or second session state owner is authorized.

Controller owns radialModel.ts materialization, the shared test fixture, inventory and the serialized join. Numerical ownership is radialData.ts, radialScale.ts, radialLayout.ts and radialNumerical.test.ts. Paint ownership is radial.ts, radialSeries.ts, radialChrome.ts and radialEngine.test.ts. Family-local chrome composition is permitted because no existing exported generic polar chrome owner exists; this does not authorize edits to Nightingale or shared lifecycle files. Each production file must meet 400 physical lines, 300 logical units and 50 per callable through the maintained checker.

This approves the RC0 contract and RC1 handoff only. It does not accept replacement circle fitting, browser zero-mark behavior, tooltip picking, stroke containment, label collisions, real-FMP appearance, fresh-session reopen, or publication. Those remain the declared join and RC3/RC4 gates.
