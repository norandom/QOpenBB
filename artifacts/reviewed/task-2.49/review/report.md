# Correct the missing drag source guard before accepting Set Up

The independent review reproduced one contract defect. The existing five focused tests pass, but an external drop emits a reorder when a caller supplies an empty-string stable series ID. Task 2.49 remains unaccepted pending a narrow correction and regression coverage.

## Review Verdict
- VERDICT: REJECTED
- TASK: 2.49
- MECHANICAL_RESULTS:
  - Tests: PASS for the implementer's focused unit command, 5 passed, exit 0 (`focused-unit.json`). FAIL for the independent missing-source regression, 1 failed, exit 1 (`adversarial-unit.json`). Both used existing dependencies and one Vitest worker.
  - TBD/TODO grep: CLEAN across the four owned files.
  - Secrets grep: CLEAN; no credentials or suspicious secret assignments observed.
  - Static checks: scoped Biome PASS, exit 0 (`lint.json`). Source spot check found no runtime import/global defects. The documented unchanged typography.ts TS2578 compiler limitation is retained, not counted as strict compiler acceptance.
  - Boundary: WITHIN. Actual fork status identifies all four reviewed files as untracked; the outer git diff alone is empty, so the actual bytes were read directly.
  - Boundary audit: CLEAN. Controls emit intents, use existing Switch, and introduce no storage, transformations, renderer activation or shared design-system edits. Parent owns inventory/breadth and dock composition integration.
  - RED phase: VERIFIED by the retained missing-module failure in implementer/red.log; it resolves the exact production import tested by the focused suite.
  - Complexity: TSX 82 physical lines, CSS 22; inspected syntax measurement reports 80 logical units and largest function 8, within 400/300/50. Inventory integration remains a parent gate.
- FINDINGS:
  1. Important: `ChartSetupPanel.tsx:47` resolves a missing drag source with `ids.indexOf(source ?? "")`. The frozen API permits string series IDs without a nonempty constraint, so null becomes a real caller ID when one item has `id: ""`. Dropping onto B without any internal drag emits `{kind: "series-order", ids: ["b", ""]}` from initial IDs `["", "b"]`. This violates the design's instruction to ignore missing drag IDs. The independent test `missing-source.test.tsx` demonstrates the actual component behavior. Cancelled drags have the same missing-source representation. This defect does not require financial data or application activation.
  2. FYI: Visual inspection of `implementer/setup-light-dark.png` against `artifacts/reviewed/parity/editor-runtime-next/focused/setup-default.png` confirms the Categories/Series hierarchy, single category selector, Aggregate switch, grip/remove chips and lower transpose switch. Dark presentation is close; light off-switch contrast is faint and glyphs/spacing differ slightly. Exact visual similarity remains the owner's judgment. Existing browser script/results were inspected, but no browser was launched during this review because the shared heavy lane was occupied.
- REMEDIATION: Return early for a null drag source before looking up its exact ID; preserve legitimate empty-string IDs during internal dragging. Add regression coverage for missing/cancelled drag with an empty-string ID and valid internal reordering of that ID. Rerun focused checks and obtain re-review of the changed hashes.
- SUMMARY: The controlled Set Up implementation is bounded and otherwise supported by focused evidence, but the missing-source guard must be corrected before acceptance.

## Reproduction and identities

Run the commands recorded verbatim in `focused-unit.json`, `adversarial-unit.json`, and `lint.json` from the repository root. The first review-only reproducer attempt failed before test execution because React's JSX runtime could not resolve from the artifact directory; the final review config aliases the existing React installation and the retained final failure is the actual assertion, not a harness error.

All four exact SHA256 values in `source-hashes.json` were measured independently from current bytes and match the implementer's frozen manifest:

| File | SHA256 |
| --- | --- |
| ChartSetupPanel.tsx | 2fd5b778f2b44a857d98ec1d9986fc7aadda8cd9ff34acd1f14ef2fab0c8066e |
| chartSetupPanel.css | 43ffe538e9a9881427c3d18dd9d6c58fa168f00b794a7ab273b26d6814c6f597 |
| ChartSetupPanel.stories.tsx | 371364a81207c02de08053013b83ae639c213f3227fcd068f6f221d9e014203c |
| chartSetupPanel.test.tsx | 69558d89144bb5a1ba48ac941527ef5399395acb9532b1816918f6537ac6a75b |

Review scope is the frozen Set Up design and task 2.49, with requirements 4.8/4.9 and 10.1/10.4/10.5/10.6 applied to this component boundary. No dashboard activation, renderer equivalence, persisted chart-session semantics or application acceptance is inferred from this review.
