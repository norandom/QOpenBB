# Symbol draft continuity: independent source review

The final two-file repair is **APPROVED for the bounded source join**. An open Symbol draft survives its own exact raw-symbol acknowledgement, while genuine context changes clear it. Failed debounce, Enter, blur and Tab-to-blur acknowledgements retain honest failure feedback without sending another lookup or reopening a closed popup. Packaged real-FMP and persistence acceptance remains open.

Date: 2026-10-30. Reviewer: fresh independent `gpt-6.1-sol` context using the project `kiro-review` protocol. Workspace HEAD: `b5193dbd7a553912daa5ea72df981c3fdb49d365`; checkout: `/home/mc/qopenbb-work/financial-proposals-20261030/sources/workspace`. The reviewed working-tree bytes are identified below, rather than represented as a commit.

## Review Verdict

- VERDICT: APPROVED
- TASK: 7.2, bounded presenter own-raw-symbol acknowledgement repair; underlying presentation/host contracts in tasks 4.2 and 5.2.
- MECHANICAL_RESULTS:
  - Tests: PASS, independent final native suite **52 passed, zero failed, zero skipped**, exit 0, 12.45 seconds, started 19:53:51 local time.
  - TBD/TODO grep: CLEAN; zero `TBD`, `TODO`, `FIXME`, `HACK` or `XXX` matches in the two files.
  - Secrets review: CLEAN; no concrete credentials introduced. Request/authentication configuration remains local/ref data; React draft state contains an opaque scope generation, symbol, mode, open state and classified display feedback.
  - Static checks: PASS, scoped Biome checks two files without changes, exit 0. Whitespace check exit 0. No temporary environment flag remains.
  - Complexity: PASS, actual whole presenter **394 physical / 179 logical / maximum callable 34**, within 400/300/50. Tests are excluded from production caps.
  - Boundary: WITHIN; exactly the presenter and its existing test file differ from HEAD. Ten other frozen production/test hashes match, including the lifecycle/search hooks and comparison control.
  - Boundary audit: CLEAN; no hook, host, transport, provider, dependency, persistence schema or group writer changed.
  - RED phase: VERIFIED from retained behavioral output: original implementation 11 failed / 29 passed; failed-blur follow-up 1 failed / 2 passed / 47 unselected; actual Tab-to-blur follow-up 1 failed / 3 passed / 47 unselected.
- FINDINGS: No remaining blocking finding in the final frozen source. The earlier 50-case candidate had a confirmed Tab-to-blur automatic-retry defect and is superseded by this candidate.
- REMEDIATION: None for this bounded source review. Controller inventory/source binding, build and packaged acceptance remain required joins.
- SUMMARY: The final presenter preserves only its own valid raw acknowledgement, establishes fresh user-search ownership, and closes the demonstrated failed Tab-to-blur retry path without weakening the selection guard.

## Contract and adversarial checks

I read the actual diff and final source, requirements 1.1-1.5, the design's typed ports, selector UI, failure/persistence and verification contracts, and tasks 4.2/5.2/7.2. Current testing, complexity, delegation, CI and documentation steering were applied. The configured core `product.md`, `tech.md` and `structure.md` steering files are absent; this is an existing documented repository condition.

The scope signature normalizes headers like `useCompanySearch` and covers widget, dashboard, source identity/request configuration, provider, immediate/preview/membership state and compatible group identity/members. It excludes the effective symbol and bound group value. The current symbol still enters the draft identity; `selectedAt` does not. I traced the real source constructor and native helper: it constructs the search request with empty parameter options, so a raw Symbol change does not alter the request configuration. Ordinary source-object reconstruction and current-symbol metadata persistence therefore do not create a false financial-context change.

The expectation is created immediately before the actual raw callback and binds originating draft identity, exact single raw symbol and private scope generation. Matching requires the same draft mode/value, matching new effective symbol and unchanged scope. The identity effect clears pending work before deciding whether to rebind. Loading/ready open drafts call `company.search` after hook invalidation, creating fresh user-session/request ownership under the new identity. The accepted private cache remains allowed; no old result object is transplanted. `useCompanySelection.choose`, its `remote.isCurrent` proof and fresh `readContextNow` comparison remain byte-identical. Nonvacuous tests exercise real controlled-parent symbol changes, both immediate and 1500 ms responses, explicit choice after 3250 ms, fresh context mutation before choice, incompatible groups, authentication changes, late results, Escape and unmount.

The Tab repair stores only classified failure feedback on the existing closed draft before cancellation clears remote state. Blur can then snapshot that failure immediately before the raw callback. Requery requires an open draft and loading/ready remote state; a closed failed draft only cancels automatic exact-symbol resolution. The actual keydown-Tab then blur test proves one raw callback, one search request, unresolved/error feedback and a closed popup. A separate matching external AAP update between Tab and blur proves that closing does not arm an acknowledgement early: the external update clears the draft and cancels the pending raw callback. New edits replace the draft without feedback, and genuine scope/identity changes clear it through the same bounded invalidation effect.

## Reproduction and source identity

From the Workspace `terminalpro` directory, the independent final commands were:

```sh
/mnt/d/Source/QOpenBB/artifacts/task-1.2/node-v24.22.1-linux-x64/bin/node node_modules/vitest/vitest.mjs run tests/unit/company-selector.test.tsx --maxWorkers=1 --fileParallelism=false
/mnt/d/Source/QOpenBB/artifacts/task-1.2/node-v24.22.1-linux-x64/bin/node node_modules/@biomejs/biome/bin/biome check src/components/General/Table/NavBar/CompanySymbolSelector.tsx tests/unit/company-selector.test.tsx
git diff --check
```

Each exited 0. Receipts: final native suite (private receipt: `task7.2-draft-review-tab-vitest.log`), final Biome (private receipt: `task7.2-draft-review-tab-biome.log`), independent identity/physical/static checks (private receipt: `task7.2-draft-review-tab-static.log`). The existing root `tools/quality/syntax_units.ts` JSON-stdin CLI independently measured the actual presenter with Node 24.22.1, exit 0; parser receipt (private receipt: `task7.2-draft-review-tab-size.json`). Physical lines were independently counted from the same source bytes with terminal newlines excluded. The controller owns the maintained inventory gate.

| File | Final SHA-256 |
| --- | --- |
| `terminalpro/src/components/General/Table/NavBar/CompanySymbolSelector.tsx` | `74afb26dd872b158ebd6ad2831b8e35c2741cc67c37271a5c0bb67b207fe2cf5` |
| `terminalpro/tests/unit/company-selector.test.tsx` | `e49c6f97f1bc89ea951deafce543eabcd83d088e9668269ad52addfa05164824` |

These match the final worker freeze (private receipt: `task7.2-draft-tab-freeze.json`). The prior independent 50-test receipt and prior 380/178/34 parser receipt apply only to the superseded pre-Tab bytes. The worker's original RED, failed-blur RED and Tab RED receipts were inspected; RED runs are historical evidence and were not rerun by this reviewer. No source/test edits, dependency install, broad native TypeScript graph, build, browser or provider requests were performed by this reviewer.

## Limits and next action

This review approves the local source repair only. jsdom interaction tests do not establish real browser timing/layout, actual financial data, saved reopen or retained-bind recreation. The known native composite/Zod graph limitation remains unverified. The controller must bind the accepted bytes in the source pin/inventory, rebuild through Dagger and complete the real-FMP, persistence and isolated browser evidence before task 7.2 or feature acceptance.

## Verification Result

- STATUS: VERIFIED
- CLAIM_TYPE: TEST_OR_BUILD
- CLAIM: The exact final presenter/test hashes above pass the independent focused 52-case native suite, scoped Biome, whitespace, frozen-file and whole-presenter size checks; task-local source review has no remaining blocking finding.
- EVIDENCE: Fresh final-candidate commands exited 0; 52 passed with no skips; actual 394/179/34; final two and ten unchanged hashes matched. Review-local evidence links resolve.
- GAPS: This is not a task-7.2 completion or FEATURE_GO claim. Controller inventory/source binding, rebuilt packaged real-data/persistence/browser checks and the known native TypeScript graph gap remain outside this review.

Publication note: this derivative keeps the independent review text and replaces links to private raw receipts with their filenames. Original reviewed record SHA-256: `53a42208fd0c168c00a3604b4de9c093ba1ccff76145796d65207f617085e173`. Raw logs remain local.
