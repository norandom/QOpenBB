# Tile Padding source repair review

The bounded source repair is approved. It restores the independent series inset used for label fitting, while preserving explicit padding for active label boxes. This verdict does not certify the initial image or rebuilt browser behavior.

## Review Verdict

- VERDICT: APPROVED
- TASK: H4 Tile Padding source repair, limited to Workspace `terminalpro/src/components/General/Table/Chart/echarts/hierarchyLabels.ts` and `terminalpro/tests/unit/chart-compatibility/hierarchyEngine.test.ts`.
- MECHANICAL_RESULTS:
  - Tests: PASS. Independent canonical focused Vitest run passed 29/29, exit 0. Two additional reviewer probes passed with the existing suite, 31/31, exit 0. Exact commands and exits are in `reviewer-results.json`; output is in `reviewer-tests.log` and `reviewer-probes.log`.
  - TBD/TODO grep: CLEAN. No TBD, TODO, FIXME, HACK or XXX matches in either changed file.
  - Secrets grep: CLEAN. No secret/password/api_key/token matches; diff inspection found no credentials.
  - Static checks: PASS for scoped Biome, exit 0, and `git diff --check`. Scoped strict baseline and candidate each exit 2 with the identical sole inherited `src/components/ds/plugins/typography.ts(1,1)` TS2578 diagnostic. There is no added diagnostic; this is not a clean application compile.
  - Complexity: PASS. Independently inspected parent-produced `combined.json`: no errors or violations; the inventory owns the changed file under analyst-workspace and measures 231 physical lines, 119 logical units, maximum 22 per function, within 400/300/50. The parent reports gate exit 0; these counts also agree with the implementer measurement.
  - Boundary: WITHIN. Only the two assigned maintained files are reviewed; reviewer writes are confined to ignored evidence. No source/test edits, commits, build or browser process were performed by the reviewer.
  - Boundary audit: CLEAN. Label adaptation remains in the renderer-design label helper. No changes to native layout ownership, appearance defaults, prepared values, persistence, shared declarations or dependencies.
  - RED phase: VERIFIED from `red.log`, `red-final.log`, `red-identity.json` and the checked replay driver. Original Workspace 2647 adapter fails the composed-default painted-text regression, including after fixture calibration.
- FINDINGS:
  1. FYI: `hierarchyLabels.ts:48` now derives fit dimensions from the independent series argument. `hierarchyLabels.ts:56` selects saved native boxing padding only when normalized fill or border paint is active. The existing `box()` normalizer retains numeric zero and per-side arrays and makes an explicitly disabled border inactive. Independent probes cover fill, stroke-only, omitted border-enabled, disabled border and numeric zero; no new border semantics were introduced.
  2. FYI: The native composed-default regression checks actual display-list text at padding 0, 3 and 10, with full text, wrapping, and smaller font respectively. It checks invariant rectangles/transforms and weight 4, reversed edits, tiny hiding and restored viewport. Both family boxing tests retain visible fill and explicit zero/per-side values. The independent Sunburst probe additionally verifies that saved series inset affects visible text despite label padding 8 and that reverting the inset and resizing restores text.
  3. FYI: The viewport adjustment from 52 to 72 is justified by the actual 20-pixel ECharts root-header reservation recorded in native metrics. It provides sufficient leaf height for the intended two-line threshold. It does not neutralize the regression: the old adapter still fails at the final viewport in `red-final.log`, while the fixed adapter passes. The original failing small-viewport and descriptor-only logs are retained rather than represented as passing evidence.
  4. FYI: Active boxed labels keep the existing ECharts clipping behavior. This change separates the series fit inset and saved native box padding; it does not establish exact original pixel parity for every boxed-label geometry.
- REMEDIATION: None for this bounded source review. Complete the parent-owned source commit/build and packaged browser checks before H4 acceptance.
- SUMMARY: The independent renderer checks support the padding repair and its boundaries, with packaged application acceptance still pending.

## Reviewed identity and reproduction

Reviewed 2026-10-25 against Workspace base `2647c37f9dd1d84b1f41da28383ace73e0b10c15` with these working-file SHA256 values, verified before and after independent checks:

- `hierarchyLabels.ts`: `ecd2a9b69f0a04ea9d7dd5023ab56fffd339e1bbe28a34b56244003ccb6bb44e`.
- `hierarchyEngine.test.ts`: `e085864a477b66424b0a71b0a29c2a39e42aeaf070fbd43fa3151b91dd93a7ac`.

Run `pipeline/.venv/bin/python artifacts/chart-hierarchy/h4/tile-padding-fix/reviewer-run.py` from the repository root in WSL Debian as `mc`. It serializes the focused suite, supplemental probes, scoped lint and strict baseline/candidate checks using pinned Node. The probe config appends assertions in memory to the existing fixture module; it does not modify maintained source/tests or create a competing maintained harness. Baseline typing supplies the exact original adapter through the compiler host while retaining the current test/import graph, rather than claiming a pre-edit compile.

Review inputs were the actual diff, `.kiro/specs/analyst-workspace/hierarchy-renderer-design.md`, `.kiro/specs/analyst-workspace/hierarchy-contract.md`, `artifacts/chart-hierarchy/h4/tile-padding-investigation.md`, `artifacts/chart-hierarchy/h4/tile-padding-fix/report.md`, and the project review/testing/complexity/delegation/documentation rules. The owning specification language is English; core product/tech/structure steering files are absent. No broad suite, image, live FMP, packaged browser, persistence or visual acceptance is inferred from these source checks.
