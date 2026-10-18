# Ordinary Set Up adapters pass independent task review

## Review Verdict

- VERDICT: APPROVED
- TASK: 2.73
- MECHANICAL_RESULTS:
  - Tests: PASS. Independent rerun of setupProjection/setupTransitions: 33 passed, exit 0. ChartSetupPanel: 8 passed, exit 0.
  - TBD/TODO grep: CLEAN across the nine scoped production/test files, including FIXME/HACK/XXX.
  - Secrets grep: CLEAN; inspected code contains no credentials or external transport.
  - Static checks: scoped Biome lint PASS, nine files, exit 0. Affected TypeScript project reports only unchanged `src/components/ds/plugins/typography.ts:1` TS2578, exit 1; whole-project typecheck is not claimed clean.
  - Boundary: WITHIN the five new setup modules, existing setup panel and three focused test files. Controller-owned cartesianTypes declaration inspected read-only. Concurrent renderer work is outside this verdict.
  - Boundary audit: CLEAN. Selection and projection remain pure; existing session/range/Widget owners retain capture, stamps and persistence.
  - RED phase: VERIFIED from local `setup/red.log`, `setup/red-transitions.log` (missing new modules) and `setup/red-panel.log` (two required predicate/heading failures).
  - Complexity: PASS. Independent syntax checker rerun and physical counts cover all six production files; maxima are 229 physical lines, 91 logical units/file and 26/function, below 400/300/50.
- FINDINGS:
  1. No material implementation defect found against task 2.73, requirements 4.2/4.7-4.9/10.1/10.3-10.6 and the canonical live-editor design/contracts.
  2. FYI: session integration must consume `observationKind: count` with neutral number-axis/crosshair/label/tooltip callbacks, perform requested category recapture, and use existing range/model reducers. Real-route persistence, save/reopen and renderer acceptance remain unverified by this task.
- REMEDIATION: None within this boundary.
- SUMMARY: The source-coordinate transitions and numerical Set Up projections are ready for the session join, with the disclosed pre-existing TypeScript diagnostic retained.

Reviewed on 2026-10-18 against Workspace HEAD `a709c520b04e7265495b914aeb3478d296c7f221` plus the working files identified below. The review read actual untracked modules as well as the tracked diff. It independently inspected the original AG Grid reducer and inversion source referenced in [the source handoff](setup-source.md), and checked the finite shared witness declaration against the producer. The original retained `ResolvedRange.originalRange` remains provenance; resolved IDs/bounds supply persistence through the existing range reducer.

The expected-value assertions cover seven operators, negative/zero/null/missing observations, 220/45 duplicate-category sums, aggregation before transpose, selected order, absent endpoints, duplicate-label positional series, safe coerced keys, known-unit rejection before transpose, derived count units, unchanged unknown units and original provenance. Model tests cover unknown siblings, accepted own `chartOptions: undefined`, omitted root aggregation flag when disabled, and category recapture without fabricated categories. Panel tests exercise both original switched headings and the default-category aggregation predicate.

## Reproduced commands

Run in WSL Debian as `mc`, from `/mnt/d/Source/QOpenBB/vendor/workspace/terminalpro`, using `/mnt/d/Source/QOpenBB/artifacts/task-1.2/node-v24.22.0-linux-x64/bin/node` as `NODE` below. Test configs bound workers to one. No browser, install or broad suite ran.

```sh
"$NODE" node_modules/vitest/vitest.mjs run --config tests/unit/chart-application/vitest.config.mjs tests/unit/chart-application/setupProjection.test.ts tests/unit/chart-application/setupTransitions.test.ts
"$NODE" node_modules/vitest/vitest.mjs run --config tests/unit/chart-editor/vitest.config.mjs tests/unit/chartSetupPanel.test.tsx
"$NODE" node_modules/@biomejs/biome/bin/biome lint src/components/General/Table/Chart/application/setupTypes.ts src/components/General/Table/Chart/application/setupAggregation.ts src/components/General/Table/Chart/application/setupProjection.ts src/components/General/Table/Chart/application/setupDescriptors.ts src/components/General/Table/Chart/application/setupTransitions.ts src/components/General/Table/Chart/editor/setup/ChartSetupPanel.tsx tests/unit/chart-application/setupProjection.test.ts tests/unit/chart-application/setupTransitions.test.ts tests/unit/chartSetupPanel.test.tsx
"$NODE" node_modules/typescript/bin/tsc --project tests/unit/chart-application/tsconfig.json --noEmit
```

From the QOpenBB root, `"$NODE" tools/quality/syntax_units.ts < artifacts/live-editor/setup/paths.json` independently reproduced the stored six-file logical measurement, exit 0. Physical counts were independently calculated from normalized source text. Inventory/breadth registration and the combined controller gate remain controller-owned.

## Reviewed source identity

Paths are relative to `vendor/workspace/terminalpro`; `Chart/` abbreviates `src/components/General/Table/Chart/`.

| File | SHA256 |
| --- | --- |
| Chart/application/setupTypes.ts | 4ad087841b725d73506014d1c97969e6b5e5114b6379a2db8884a0281fdb468b |
| Chart/application/setupAggregation.ts | e8ceb7f8530950fe1838c1cc0341bd95dd40fedb1d6bd40e76182c04a8f0aae |
| Chart/application/setupProjection.ts | 4518d2589423ae2d08712bb890810d72439cffe36165d0b7c3a653c5fccd38da |
| Chart/application/setupDescriptors.ts | 670b0ed38b864915e10221fb132f59a16cbcc753b0f437347ba8115104ba2a34 |
| Chart/application/setupTransitions.ts | e8aadd29e5f0391435cb9aab22854a2e3fe018148ce88f0c69d562e0a4447ed2 |
| Chart/editor/setup/ChartSetupPanel.tsx | b7688e5e309cf1f47c74802c3173907a4267158b6b649a7c619cd541013d511d |
| tests/unit/chart-application/setupProjection.test.ts | a5b99418de1332967bd3ace6b63b9e2b700af4505c4778b0ec7d0188822d7674 |
| tests/unit/chart-application/setupTransitions.test.ts | 4b1c3a2461e76c4f50aa0009cf805695766a12437813d301baf9c11360a7a9d7 |
| tests/unit/chartSetupPanel.test.tsx | b22dc0229ee230b6477c60d80075170a9c9d7a1fafcfe5ddce4a195ce9efc603 |
