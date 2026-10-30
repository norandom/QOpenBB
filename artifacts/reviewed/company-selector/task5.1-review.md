## Review Verdict
- VERDICT: APPROVED
- TASK: 5.1, reactive and freshly checked dashboard group context.
- REVIEWER: gpt-6-astra, high reasoning; independent review started in fresh context, with two bounded repair reviews by the same reviewer. No fallback model used.
- MECHANICAL_RESULTS: Fresh focused Vitest PASS 43/43, exit 0; Biome PASS two files, exit 0; fresh syntax-unit parser PASS 166 logical units and maximum 18 per function, exit 0; physical count 353. Exact commands are retained in the initial review below. Caps 400/300/50 pass without an exception. Controller combined inventory gate remains separate.
- BOUNDARY: WITHIN the existing group hook and existing test file. No frozen NavBar modules, dependencies, broad writer semantics or subscriptions changed. Production introduces no direct setState or new identity/group registry. No new placeholders or hardcoded credentials found in the reviewed diff.
- RED_PHASE: VERIFIED. Final null-value repair log `task5.1-null-red.log` records 3 failed/40 passed before the fix. Earlier substantive RED results are retained below.
- FINDINGS: Both acceptance-blocking effective-provider findings are resolved. No remaining blocking finding within task 5.1.
- REMEDIATION: None for this bounded review.
- SUMMARY: Current local/shared group snapshots, fresh guarded writes, provider compatibility and preview/detached isolation are approved at source level for task 5.1.

## Final accepted candidate

Base Workspace HEAD remains `d6fcf07131ec7c134fe06485aa236584cb7ded4d`; acceptance applies to the following exact working-tree bytes:

| File | SHA-256 |
| --- | --- |
| terminalpro/src/components/Widgets/Helpers/useParamGroupBindings.ts | 9953f465187dd9ce9d034aacc450db08fdb19029ed2b02c948bda3c46c1753b5 |
| terminalpro/tests/unit/components/Widgets/Helpers/useParamGroupBindings.test.tsx | 57e4e6a7205fd3087df9e356456cb931c5205c666f672cc7262590ee205bc7dc |

The final repair defaults only undefined values, matching native `createWidgetInitParams`. Stored and bound null providers remain ineligible; null Symbol remains empty in the company context without restoring a default ticker. Three regressions compare these cases with actual native helpers and verify writer refusal where provider identity is unavailable.

The first repair remains intact: native group application owns option filtering and ordering, while differing individually applicable provider values conservatively disable company eligibility in either order. That ambiguity limit prevents state-dependent native subscription filtering from authorizing an incompatible provider. Invalid provider options are ignored according to native behavior. Original controls and legacy writers remain available; this feature does not resolve ambiguous provider groups automatically.

Final verification reran the full affected 43-case file, the two-file Biome check and the actual syntax-unit parser against the hashes above. Native TypeScript/build, host wiring, browser, live FMP, theme and persistence acceptance remain outside this task, as recorded below. This approval does not mark tasks 5.2, 6 or 7 complete.

## First repair review history (rejected, now resolved)

Current production SHA-256: `2eb8dd445de60eef9b8f694503f15d2d9c0bffd88f33b3d0a217c60e242be297`. Current test SHA-256: `3fed9bed128780a50bbf9b75ced393948db33aa48ea5a1c426b4d6fbbaad2f2e`. Base HEAD and two-file boundary are unchanged. Reviewer remains gpt-6-astra, high reasoning; this is the same independent reviewer reassessing the bounded repair.

- Fresh tests: PASS, 40/40, exit 0, using the exact focused command recorded in the initial review below.
- Fresh Biome: PASS, two files, no fixes, exit 0, using the same recorded command.
- Fresh size parser: PASS, 165 logical units, maximum 18 per function, exit 0. `wc -l` confirms 350 physical lines. No exception.
- Repair RED: VERIFIED, `task5.1-review-red.log` has 4 failed/35 passed, and `task5.1-conflict-red.log` has 1 failed/39 passed. Tests exercise both provider-group orders in local/shared stores and the native subscription prefilter difference.
- Resolved: the hook now calls the existing `updateWidgetGroupValues` on a cloned resolved widget, so native option applicability and group order own the effective snapshot. It also blocks differing individually applicable provider-group values. That conservative restriction is appropriate because `needsGroupValueUpdate` filters already-equal values before native subscription application, making conflicting providers state-dependent. Rejected options do not count as conflicts. Original writers and subscriptions remain unchanged.
- Remaining Important finding: `useParamGroupBindings.ts:80-82` still uses `effectiveWidget.storage?.params?.[name] ?? definitionDefault`. An explicit stored or singly grouped `provider: null` therefore becomes `fmp` if the definition default is fmp. Native `createWidgetInitParams` in `terminalpro/src/lib/utils/widgetParams.ts:319-320` preserves null because it checks `!== undefined`; native text provider groups with no option restriction can also assign null. The repaired `companyWidget` consequently retains provider null while `companyContext.provider` and the binding guard classify it as fmp. The provider conflict set has at most one value in this case and does not reject it. This is the explicit-value part of the original effective-provider mismatch, violating the design's effective-provider eligibility requirement.
- Required remediation: preserve explicit null and other defined native parameter values; default only where the canonical native initialization does. Add focused stored-null and applicable grouped-null provider regressions covering the fresh context and live-writer refusal, while retaining valid FMP behavior. Keep the repair inside the same two files and rerun focused checks. No broad store or writer changes are needed.

That candidate was rejected. The final accepted repair above resolves its null-value finding. Full native TypeScript/build and browser/runtime limits below remain unchanged.

## Initial review history

- TASK: 5.1, reactive and freshly checked dashboard group context.
- REVIEWER: gpt-6-astra, high reasoning, independent fresh context; no fallback model used.
- MECHANICAL_RESULTS:
  - Tests: PASS, 35/35, exit 0. From the Linux Workspace terminalpro directory: `/mnt/d/Source/QOpenBB/artifacts/task-1.2/node-v24.22.1-linux-x64/bin/node node_modules/vitest/vitest.mjs run tests/unit/components/Widgets/Helpers/useParamGroupBindings.test.tsx --maxWorkers=1 --fileParallelism=false`.
  - Static checks: PASS, exit 0. Same directory and Node: `node_modules/@biomejs/biome/bin/biome check src/components/Widgets/Helpers/useParamGroupBindings.ts tests/unit/components/Widgets/Helpers/useParamGroupBindings.test.tsx`. Two files checked; no fixes applied.
  - Size: fresh parser PASS, 155 logical units and maximum 18 per function. Root command: `/mnt/d/Source/QOpenBB/artifacts/task-1.2/node-v24.22.1-linux-x64/bin/node tools/quality/syntax_units.ts < artifacts/company-selector-implementation/task5.1-paths.json`, exit 0. Source has 330 physical lines; 400/300/50 caps apply without an exception. Controller combined inventory gate remains separate.
  - TBD/TODO/FIXME/HACK/XXX: CLEAN in production diff. No new placeholders in the test diff.
  - Secrets: no hardcoded credentials found in either actual diff.
  - Boundary: WITHIN. Git status contains only the approved existing hook and its existing unit-test file. Six accepted NavBar modules are unchanged. No source edits, dependency changes or commits were made by this reviewer.
  - Boundary audit: no new store, registry, permission bypass or direct setState in production. One effective-provider contract violation remains below.
  - RED phase: VERIFIED from task5.1-red.log (25 failed, 5 passed) and task5.1-isolation-red.log (3 failed, 32 passed). Failures exercise missing context, freshness and isolation behavior, rather than merely test discovery.
- FINDINGS:
  1. Important: effective provider can differ from the native widget execution provider. In `terminalpro/src/components/Widgets/Helpers/useParamGroupBindings.ts:56`, `effective(name)` uses the first matching group's value, then falls back with nullish coalescing. The native `terminalpro/src/lib/utils/app.ts:636` function `updateWidgetGroupValues` reduces groups in order, uses `isValidParamOption` (line 1083) for plain parameter groups, and assigns each accepted group value into storage; later applicable groups overwrite earlier ones. The real subscription in `terminalpro/src/components/widgetSync/useWidgetSubscriptions.ts` calls that native helper for applicable groups. A compatible company widget with a text provider definition and two bound plain provider groups ordered [fmp, other] can therefore execute with provider other while this hook reports provider fmp and eligible=true. One valid Symbol binding still passes `checkCompanyGroup`, allowing `writeBoundSymbol` to update the group. Distinct groups mapping to one parameter are deliberately retained by the existing binding API and its tests; the new safety guard cannot assume provider uniqueness. Conversely, reversed order can falsely block a native FMP context. This violates task 5.1 and the design's Exact eligible bindings / Commit and group contract: every current member must have effective provider fmp. The existing 35 tests vary stored provider values but do not cover competing provider-group precedence or native applicability.
- REMEDIATION: Resolve effective parameter values consistently with the existing native group application semantics, including applicable-group filtering, ordering and explicit values; do not change the broad legacy writer. Add focused failing-then-passing real-store regressions for conflicting provider groups in both orders, including a peer whose effective provider becomes incompatible. Verify the fresh imperative read and guarded writer before rerender, in local and shared dashboards. Keep changes inside the assigned hook and existing test file, preserve the accepted interface, and rerun focused tests, Biome and caps.
- SUMMARY: Reactive membership selection and isolated writes are implemented, but the new guard must use the same effective-provider semantics as native execution before task 5.1 can be accepted.

## Candidate identity and reviewed boundaries

Workspace checkout: `/home/mc/qopenbb-work/financial-proposals-20261030/sources/workspace`, base HEAD `d6fcf07131ec7c134fe06485aa236584cb7ded4d`.

| File | SHA-256 |
| --- | --- |
| terminalpro/src/components/Widgets/Helpers/useParamGroupBindings.ts | 94d6673c331533b521e3c02668b195ce60d334d3b89eddeb8746798efebf2e10 |
| terminalpro/tests/unit/components/Widgets/Helpers/useParamGroupBindings.test.tsx | 4b08c42fd239cb082a67843b1a0d9534ee19f70328fac01f8d39e46138633052 |

Reviewed requirements 1.3, 1.4 and 1.5; task 5.1; design Typed ports, Exact eligible bindings, and Commit and group contract. Both actual data.widgets and data.groups are selected from the chosen local/shared store. Fresh reads fetch that store and current connector definitions; sparse records use the existing definition/parameter helpers. The new writer rechecks the pure guard, exact group ID and membership, rejects local/shared dashboard-ID collisions, and calls the original updateGroup once. Preview uses its local widget and ungrouped context; the inspected WidgetsBuilder caller establishes isPreview=true through WidgetProvider. Detached nonpreview contexts expose no company binding. Existing writer functions retain their signatures and use the same callback.

No full native TypeScript/build, browser, theme, FMP, save/reopen or packaged-runtime acceptance is claimed. Native full-build verification has the existing composite/Zod-cache gap reported by the controller. Host integration is task 5.2; browser acceptance is task 7. Core product.md, tech.md and structure.md are absent from this root; applicable existing complexity, testing, documentation and delegation guidance was read.

