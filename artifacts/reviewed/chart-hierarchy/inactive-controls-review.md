# H2 controls implementation review

The inactive controls foundation is approved. Its appearance projection, editor state and transactions satisfy the accepted seam; this decision does not accept live hierarchy integration or rendered effects.

## Review Verdict

- VERDICT: APPROVED
- TASK: H2 controls lane, as defined by the canonical hierarchy renderer/control design, Controls lane and Join and evidence sections.
- MECHANICAL_RESULTS:
  - Tests: PASS. Independently ran the existing compatibility Vitest configuration against `hierarchyAppearance.test.ts` with pinned Node24.22.0 and `--maxWorkers=1`; 32 tests passed, exit0. See `reviewer-tests.log`.
  - TBD/TODO grep: CLEAN across the seven production owners. See `reviewer-scan.json`.
  - Secrets grep: CLEAN for concrete credential/private-key patterns in those owners; source inspection found no credentials.
  - Static checks: baseline-relative PASS, overall strict compilation remains FAIL. Independently ran TypeScript6.0.3 with `--noEmit --pretty false --project` for `baseline-tsconfig.json` and `tsconfig.json`; both exit2 with exactly the same four inherited diagnostics, comparison exit0. See `reviewer-baseline-tsc.log` and `reviewer-tsc.log`. No new-owner/test diagnostics appear. Reviewed worker Biome format/lint evidence; lint exits0 for all seven owners. Runtime import/value usage was independently spot-checked.
  - Boundary: WITHIN the seven production owners and one focused test in `frozen-files.json`; no session, shared declaration, storage, setup or renderer ownership was introduced.
  - Boundary audit: CLEAN. Common composition, chrome, typography, validation, primitives and reduction remain the existing owners. Neither new UI group fabricates axes or categorical legend state.
  - RED phase: VERIFIED. `red.log` records the focused behavioral suite failing because the production appearance owner did not exist; the report identifies 25 initial behavioral cases and subsequent expansion to 32.
  - Complexity: PASS in the controller's inventory-backed `combined.json`; inspected all seven included owners, maxima 223 physical lines, 112 logical units/file and 24 logical units/function, below 400/300/50. This review did not repeat the combined gate.
  - Frozen identity: all eight SHA256 values matched before and after independent verification. See `reviewer-hashes-before.json` and `reviewer-hashes-after.json`.
- FINDINGS:
  1. FYI: the initial TypeScript5.9 configuration failure is not a valid preimplementation strict baseline. The corrected TS6 baseline is a retrospective unchanged-dependency comparison, excludes the new modules/test and reproduces the final candidate's inherited typography/Zod failures. This supports zero added diagnostics; it does not establish a clean project typecheck. The implementer report describes the compiler exit as1; the independent invocations above actually exit2.
  2. FYI: these owners remain inactive. H3 must validate current stamp/family and capture/setup/baseline identity, resolve fresh theme/style/assignment context and use the existing reducer/commit owner. H4 still owns visible spacing, gradient, typography, tooltip, theme, export and fresh-session persistence evidence.
  3. FYI: advanced gradient/pattern/image fills and all four wrapping policies are retained in detached resolved data. This approval covers the demonstrated generated/public-control/string-palette route. It does not certify native rendering of active advanced fills or text-fitting parity.
- REMEDIATION: None required for this bounded foundation acceptance.
- SUMMARY: The inactive controls foundation preserves selected-baseline semantics and original leaf paths with independently passing focused behavior tests and no added scoped strict diagnostics.

## Contract and source assessment

Reviewed the actual untracked source files in full after inspecting the Workspace diff/status, rather than treating the implementer report as the implementation. Governing references are `.kiro/specs/analyst-workspace/hierarchy-renderer-design.md` (Shared contract and scope, Controls lane, Join and evidence), `hierarchy-contract.md` (Controls and appearance, Capture and implementation constraints), and the accepted executable appearance/editor/paint declarations at Workspace `fc0f02f`. The exact editor mapping/admission reports were also read. No numbered generic task criteria are invented: this lane is the authorized bounded milestone task, and its owning specification language is English.

`resolveHierarchyAppearance` calls the authoritative selected-baseline composition and applies defaults, theme common/family and composed common/family in the required order. It neither reselects model options nor writes the baseline. Explicit false/zero, separate Treemap group/tile label and spacing targets, Sunburst shape, theme hierarchy palette input and retained data-only fills are implemented. The unit suite checks precedence, detached data, malformed consumed inputs and getter rejection within the option boundary.

The editor projection returns frozen detached common state, four independently named Treemap spacing controls and a semantic gradient group. Color assignment controls applicability even when observations are missing; removing Color retains the saved enabled preference. Existing typography menus preserve current custom values and the mapper derives predefined weight/style from the selected resolved context. Bounds retain saved values above the stock slider maximum.

The mapper validates intent/edit records descriptor-first, validates correlated field/value choices, colors and finite nonnegative numbers, rejects cross-family/inapplicable edits and catches hostile failures without inspecting thrown properties. It emits only the original family-root leaf patch. The reducer regression proves unknown/inactive baseline fields survive. The new controls reuse existing group, switch, caption-color and legend choice/number primitives; the gradient fieldset disables interaction without rewriting the saved preference.

## Reproduction and limits

Reviewed on 2026-10-25 at root `ce568b0310f67ea73bef169ef4eefa911da8970d`, Workspace `ce91431ae371a6d33350ebde27c8d85ab4ceaea2`, plus the exact frozen uncommitted controls bytes. Independent tests used the existing Workspace configuration from `vendor/workspace/terminalpro`:

```sh
/mnt/d/Source/QOpenBB/artifacts/task-1.2/node-v24.22.0-linux-x64/bin/node node_modules/vitest/vitest.mjs run --config tests/unit/chart-compatibility/vitest.config.mjs tests/unit/chart-compatibility/hierarchyAppearance.test.ts --maxWorkers=1
```

From the repository root, independent strict comparisons used the same pinned Node with `verification/node_modules/typescript/bin/tsc --noEmit --pretty false --project artifacts/chart-hierarchy/h2-controls/baseline-tsconfig.json`, then the equivalent candidate `tsconfig.json`. Outputs match byte-for-byte. The baseline imports accepted declarations and unchanged composition/chrome/validation/legend owners rather than the new controls owners.

No full-repository suite, browser, image build, installation, live application mutation or commit ran in this review. Test and strict work used the controller-released verification slot. Source hashes, scoped evidence and this inactive-boundary decision do not establish packaged application acceptance.
