# Company Research contract verification

2026-11-14. Tasks 1 and 2 are locally accepted for downstream implementation: measured integration foundations and shared identity/financial-evidence contracts. This publication records those decisions. It does not establish Company Research feature readiness, runtime, provider, persistence, browser, deployment or financial-comparability acceptance. Push status and private-server acceptance are separate and unverified here.

The isolated root commits are a71a9a116865fa3749264b313e04881b0f974d79 (foundation) and 891425bb3feebba77b8d58bc9fe9661c30e8a991 (shared inventory). Workspace commit 71542bbeb85b13c08ace920cdfee786cc6d8287b freezes the contracts. Data API baseline is a965f70c164fe477ce9c99654b9be48e2f1bc9fd. Historical source-identities.json and task1-report.md describe the earlier precommit baseline, not current HEAD.

[Task 1 review](task1-review.md) accepts the explicit-manifest foundation. The [final shared-contract review](task2-final-review.md) independently reran 80 tests: 35 identity and 45 financial. The existing company-selection baseline passed 89 tests with one worker, as recorded in [dependency setup](dependency-setup.md). These are separate suites, not an integrated runtime journey. Strict scoped TypeScript checks were controller-reported; the final reviewer did not independently rerun them.

The final local task2-final-complexity.json measures 710 maintained files with errors=[], violations=[] and combined_acceptance=passed, under 400 physical lines/file, 300 logical units/file and 50/function caps. Existing exceptions remain explicit; this does not assert all historical files fit default caps. The earlier task1 baseline measures 706 files. The complete complexity dumps stay local rather than duplicating large intermediate evidence.

The checker Python regression suite remains qualified: 94 passed, 2 skipped, 1 failed. The existing Windows Git-root separator comparison in tools/quality/changes.py fails test_real_git_scope_verifies_origin_head_cleanliness_and_diff. The prescribed explicit-manifest route passes. The failed test was not relabeled or fixed by this work. Task1 Node syntax suite passed 15 tests.

The dependency receipt records protected Safe Chain1.5.25 / Bun1.4.3 frozen-lock installation, exit0, and unchanged package.json and bun.lock hashes. Installed versions are zod4.4.3, dayjs1.11.13, react-hook-form7.75.0 and Vitest4.1.11. Dependency caches and downloaded tools are omitted.

The final reviewed source files below are under the isolated Workspace terminalpro/src/lib/companyResearch. Their actual SHA256 values were rechecked during publication preparation and match the final review:

| File | SHA256 |
| --- | --- |
| config.ts | d4299d8b8ccc214119b0796dcadb1d2ef0535c4d965470a2be7c089bbc1651c9 |
| selectionReconciliation.ts | 6d1bbea29063ad5477cf6105d1550f7a39a9402cbcb37235734e4a5cc3901e1f |
| financialEnvelope.ts | 341761c7d3bbeb0bb9cbdab894cc750a64821c8d1ac45c369ec8b961539b30d5 |
| eligibility.ts | d75aabe3e44b7d6209d2b26cf8c8c36fa2f3cdcfe1fc144c457c7bf461537bf8 |

The accepted identity contract preserves source/provider/exact-symbol request identity and optional nullable listing evidence without claiming issuer or exchange equivalence. Financial parsing preserves raw rows and metadata, classifies unknown evidence, and never produces a valid-comparable result. Consumer integration, cancellation, stale-response protection and request eligibility application remain downstream obligations.

Publication preparation inspected the selected text for credentials, private keys, account state and authentication material. No concrete secret was found. Exact-byte report/review/dependency receipts are proposed alongside this summary. Raw logs, RED traces, caches, browser profiles, tool archives, intermediate reviews and large complexity dumps remain external. The manifest delta records exact source/published hashes and byte counts. Approval here covers this publication set only; no test, build, provider call or runtime action was executed during preparation.
