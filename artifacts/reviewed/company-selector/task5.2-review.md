# Company selector host integration review

The frozen task 5.2 source is approved. Task completion still requires the controller to bind the approved QueryParams exception to the committed candidate and pass the formal inventory gate. This review does not establish packaged application or persistence acceptance.

## Review Verdict

- VERDICT: APPROVED
- TASK: 5.2, native parameter host integration
- REVIEWER: Independent `gpt-6-astra`, high reasoning, fresh context; 2026-10-30. Applied `.agents/skills/kiro-review/SKILL.md`.
- MECHANICAL_RESULTS:
  - Tests: PASS, 104 cases across the actual host (30), group hook (45), and presenter (29); independent command exited 0.
  - TBD/TODO grep: CLEAN; no placeholder markers in the six changed files.
  - Secrets grep: CLEAN for targeted private-key, AWS access-key, GitHub token and API-key patterns; diff inspection found no introduced credentials.
  - Static checks: PASS, scoped Biome lint on all six files, exit 0. `git diff --check` also exited 0.
  - Boundary: WITHIN the six controller-authorized source/test paths. The array normalization and single-symbol raw-recovery changes are bounded integration repairs.
  - Boundary audit: CLEAN. No new store, dependency, global CSS, flag, provider surface or direct store writer was introduced.
  - RED phase: VERIFIED in the original host, stale-name, default/array, group-array and raw-recovery logs. They contain behavioral assertion failures subsequently covered by the green run.
  - Size: Independently measured QueryParams 993 physical / 364 logical / 38 maximum per function; group hook 356 / 167 / 18; presenter 306 / 147 / 29. All are within their approved ceilings. Exact revision exception activation remains pending.
- FINDINGS:
  1. FYI: No blocking source defect found against requirement criteria 1.1-1.5 and the design's selector, commit/group, failure and persistence integration contracts. The narrower source approval does not certify the later live acceptance criteria.
  2. FYI: QueryParams remains above the ordinary file caps. Its owner-approved 1000 / 390 / 50 exception, expiring 2026-11-30, must be bound to the exact committed candidate and measured source before checking task 5.2 complete. This review approves the measured candidate for that closing step; it does not activate the exception.
  3. FYI: Full native semantic TypeScript checking/build is unverified because of the reported existing cache/composite/Zod graph gap. This review ran the existing runtime imports through native tests and scoped lint, without dependency preparation. Browser geometry/themes, live FMP, fresh-login reopening, retained-state recreation and image acceptance remain tasks 7.1/7.2.
- REMEDIATION: No source remediation required. Complete the controller-owned exception binding and formal inventory check before task acceptance.
- SUMMARY: The actual host preserves the existing parameter paths while adding a bounded, single-update company selection integration with explicit metadata-only handling.

## Reviewed behavior and test limits

The dedicated wrapping, auto-height row precedes ordinary lower controls; only the eligible Symbol leaves its original row. Profile reuses the original `RenderParamsForRow` comparison editor, including its GroupDropdown/tooltip path. Single-symbol widgets retain their group affordance. Period, Limit, manual-run fallback and the original four host regressions remain covered. The existing `enabled=false` caller is `WidgetFallback`; inspection confirms that the baseline flag controls endpoint queries, not row visibility. No visibility regression was established from that flag.

Changed explicit selections reach `syncParams` directly with a typed sibling metadata patch, preserving current parameter refs, local state, stale notifications, copilot notifications and the existing SSRM branch. The functional update is forced once. The lifecycle writes a compatible Symbol group before this local port and the host does not repeat the ordinary grouped writer. The tests assert write count/order and an untouched independent group; the real store hook suite covers shared reactivity and preview/detached safety.

Unchanged symbols persist metadata without refreshing financial data, resetting SSRM state or issuing copilot execution. An implicit default keeps its missing stored-symbol representation. Comparing both captured effective context and the current executed ref prevents an explicit choice from being lost behind a pending raw update. The layout-phase snapshot test proves that an externally changed symbol cannot briefly display the old company name. Stored/bound symbol arrays normalize only at the company context boundary; storage is not rewritten. A single-symbol widget containing CSV remains manually correctable or clearable even when search access fails.

The host fixture imports the production hook, selector, lifecycle and native group store; it supplies the widget context/update callback and mocks unrelated chart helpers and GroupDropdown presentation. It asserts the callback's force flag, not a real backend save. Real persistence, group menu interactions, clipped viewport geometry and financial request results require the later packaged journey.

## Reproduction and evidence

Workspace checkout: `/home/mc/qopenbb-work/financial-proposals-20261030/sources/workspace`, inspected base HEAD `44dbbc205fcd2097554d91207d324862e9a5dd90` with the six-file uncommitted candidate below. Run from `terminalpro`, with `NODE=/mnt/d/Source/QOpenBB/artifacts/task-1.2/node-v24.22.1-linux-x64/bin/node`:

```sh
"$NODE" node_modules/vitest/vitest.mjs run tests/unit/components/General/Table/NavBar/QueryParams.test.tsx tests/unit/components/Widgets/Helpers/useParamGroupBindings.test.tsx tests/unit/company-selector.test.tsx --maxWorkers=1 --fileParallelism=false
"$NODE" node_modules/@biomejs/biome/bin/biome lint src/components/General/Table/NavBar/QueryParams.tsx src/components/Widgets/Helpers/useParamGroupBindings.ts src/components/General/Table/NavBar/CompanySymbolSelector.tsx tests/unit/components/General/Table/NavBar/QueryParams.test.tsx tests/unit/components/Widgets/Helpers/useParamGroupBindings.test.tsx tests/unit/company-selector.test.tsx
git diff --check
```

The independent test run finished with 3 files / 104 tests passed in 61.12 seconds, exit 0. Lint checked six files without changes, exit 0. From QOpenBB, the actual `tools/quality/syntax_units.ts` parser received the three absolute production paths from `task5.2-paths.json` on stdin under Node 24.22.1; exit 0. Physical lines were counted independently from normalized source lines. An initial attempted `.mjs` checker path did not exist; the corrected existing `.ts` checker produced the accepted counts. The standalone syntax measurement is not the formal inventory/exception gate.

Original local RED evidence: `task5.2-red.log` (14 failed / 7 passed), `task5.2-stale-red.log` (1 / 25), `task5.2-default-array-red.log` (3 / 26), `task5.2-group-array-red.log` (2 / 43), and `task5.2-raw-recovery-red.log` (2 / 27), all beside this report. The worker's final green/lint/size evidence agrees with the independent run and measurements.

Core `product.md`, `tech.md` and `structure.md` steering files were requested but are absent in this checkout. The available delegation, complexity, testing, CI and documentation policies were read; the owning specification language is English.

## Frozen source identities

Paths are relative to Workspace. SHA-256 values were independently recomputed from the actual files and match the controller's frozen candidate.

| Path | SHA-256 |
| --- | --- |
| `terminalpro/src/components/General/Table/NavBar/QueryParams.tsx` | `4ade26d1910e23c6ade5f942c24f41043fa8b770e5a3303778c03e36c649d055` |
| `terminalpro/src/components/Widgets/Helpers/useParamGroupBindings.ts` | `75f5ad1452085d0bf0bcfe4f0506e945e081354d747b345687d6fdbacfd6f98d` |
| `terminalpro/src/components/General/Table/NavBar/CompanySymbolSelector.tsx` | `d5ecebb571cca42eeb0fbe8f28f3118b30fc1f9e665377931d9f842bcbc03f17` |
| `terminalpro/tests/unit/components/General/Table/NavBar/QueryParams.test.tsx` | `b8ff5a51968a5e3d7ecee07cf6371a5a2a9dbb8462824a076df4c5ea54cad0c7` |
| `terminalpro/tests/unit/components/Widgets/Helpers/useParamGroupBindings.test.tsx` | `110249259162aae6be3f06a5631adab054a8f892e5c2a6cd9d5bfdeb4de44a5b` |
| `terminalpro/tests/unit/company-selector.test.tsx` | `f7745600e75ef107107ac23bf57ce4f435913ccf9a27bd9a2b4c718bea0a9696` |
