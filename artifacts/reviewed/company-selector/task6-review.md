# Company selector source and catalog join review

## Review Verdict

- VERDICT: APPROVED
- TASK: 6, source and catalog contract join only.
- REVIEWER: Independent gpt-6.1-sol, high reasoning, 2026-10-30, following `kiro-review` and `kiro-verify-completion`.
- MECHANICAL_RESULTS:
  - Native join: controller-observed Vitest exit 0, six suites and 287 cases in 46.63 seconds. Counts are 88/35/60/29/45/30. `task6-native-controller-observation.log` is a transcription of tool session 80335, explicitly not raw output or a second run. Prior task-local independent reviews and source tests were also inspected; this reviewer did not repeat the suites.
  - Portable contracts: the existing catalog, financial catalog, boundary/schema and financial proposal suites produced 156 passes and one environment failure. Restoring the existing pinned Node directory in the isolated snapshot allowed the affected URL-composition case to pass: 1 passed, 15 deselected, exit 0. No application/test/dependency change was needed. Together these runs verify all 157 selected cases; they are not one uninterrupted green run.
  - Corrected portable quality: controller-observed exit 0; independently inspected completed receipt reports 680 maintained files, zero errors, zero violations, Node 24.22.1 and TypeScript 6.0.3. Inventory is measured at 397 physical lines; QueryParams is 993 physical / 364 logical / maximum 38 per function.
  - Independent source/catalog assertions: PASS, exit 0. Both fork worktrees are clean; source lock, consumer source contract and maintained inventory agree. All eight changed selector production files have inventory ownership.
  - Placeholder/secret spot check: CLEAN for introduced production changes. The password-property reference is connector URL validation, not a credential. Fork `git diff --check` passes.
  - Static checks: source/provenance/query-boundary inspection PASS. No additional code was introduced by this join, apart from inventory whitespace repair. Earlier task-local lint/type evidence remains scoped to those tasks.
  - Boundary: WITHIN. Foreign working-tree inventory semantics, catalog CLI edits, renderer helper and renderer test remain excluded from the reviewed candidate.
  - Boundary audit: CLEAN. No new provider surface, endpoint, group schema or generated widget regeneration.
  - RED phase: N/A for this reconciliation task. The actual-byte quality failure supplies the failing evidence for its inventory repair; preceding behavioral tasks retain their reviewed RED evidence.
- FINDINGS: One important verification mismatch was found and resolved before approval, as described below. No unresolved blocking finding remains.
- REMEDIATION: None for task 6. The controller must stage the reviewed owned inventory bytes, preserve the unrelated changes and publish the corrected evidence attribution.
- SUMMARY: The frozen selector candidate and unchanged data API contract join correctly, with an actual-byte size gate replacing the earlier minified-inventory measurement.

## Source and catalog findings

Workspace is `ab3c357a00cd9ad7395ea2cad0cdbec09a2f3598`; data API remains `28423762e8cc3faae978e770899834b41e7cde99`. Root inspection began at `5aeaa56`. Requirements 1.2-1.5, the design's exact binding table and task 6 boundary were read directly.

Each of Profile, Income, Balance, Cash, Historical prices, Metrics, Ratios and Enterprise values in `COMPANY_BINDINGS` matches `contracts/widgets.json`: exact native widget ID and endpoint, table type, effective FMP provider, visible text Symbol and immediate execution. Profile alone is multiple-symbol capable. The external generated definitions are the relevant catalog; Workspace's internal navigation/utils `src/lib/widgets.json` is not the FMP definition source. Existing native interaction tests exercise all eight bindings; the independent generated-definition assertions close that seam without changing fixtures or regenerating catalogs.

All retained `contracts/hashes.json` entries match the actual files. The data API generator blobs match both their pinned Git objects and the hashes in `contracts/provenance.json`. Every recorded maintained generator hash matches committed root bytes, including the committed catalog CLI rather than its foreign working-tree edit. The historical data image records Workspace `c652b909627d7634241eee2ed13a561fbb4f177b`; that label accurately describes the retained data-image generation checkpoint and is not evidence of a newly built selector image. The unchanged data API identity remains consistent.

QueryParams writes the selection at `storage.companySelection` beside `storage.params` in one functional update. Its host regression checks exact financial/copilot parameter payloads and absence of `companySelection`; the same-symbol branch preserves the params object and avoids refresh/execution. The existing request initialization reads declared parameters from `storage.params`, while the search adapter explicitly constructs only provider/query/is_symbol/limit. Inspection found no metadata forwarding into financial parameters. Packaged network verification is still task 7.2.

## Resolved verification mismatch

The committed root inventory had 404 physical lines. The prior `combined.json` receipt, SHA-256 `1a9bf7fe82fb0df58992693f58b8df24ecb6ad9e51aeec6672864848df1b19f7`, measured that file as one line because the helper serialized a minified copy. Therefore that receipt and task 5.2 closing report did not establish the committed root inventory's physical cap, although their fork measurements remain useful historical evidence. The clean canonical quality run reproduced the 404-line violation.

The controller removed exactly seven blank LF lines, producing 397 lines. Independent assertions confirm identical parsed JSON and identical nonblank lines. The clean join snapshot contains exactly those repaired bytes. The helper now copies the owned inventory with `write_bytes`, preserving its physical representation. The corrected canonical `qopenbb_ci.quality_cli` receipt supersedes the earlier root-inventory cap claim; QueryParams still uses only its approved 1000/390/50 ceiling, bound to the exact candidate and expiring 2026-11-30.

| Reviewed artifact | SHA-256 |
| --- | --- |
| Repaired `inventory-owned.json` | `c015f593f204c09387c8f0cde0746a4fffbacc53c7fb91dd09c60fa5c86887e9` |
| `task6-quality-corrected.json` | `c6cfc13ea6fd7157ac6d473556a5f45005a74d1bce5f6ca74f7d9a619c526eb4` |

## Commands and evidence boundary

The controller used the existing six-file Vitest command with one worker and file parallelism disabled, `python -m qopenbb_ci.quality_cli --output .../task6-quality-corrected.json`, and `python -m pytest -c pipeline/pyproject.toml tests/contracts/test_catalog.py tests/contracts/test_catalog_financial.py tests/contracts/test_boundaries.py tests/contracts/test_financial_proposals.py -n0 --maxprocesses=2 -q`. The isolated snapshot uses committed root modules and real clean fork checkouts. Only the missing-Node test was rerun after the environment repair. The reviewer inspected commands, receipts, raw portable logs, controller-native observation and actual source bytes; duplicate suites or builds were not run.

Local evidence: `task6-review-contract.log`, `task6-review-inventory.log`, `task6-review-repair.log`, `task6-contracts.log`, `task6-contract-node-recheck.log`, `task6-native-controller-observation.log`, `task6-quality-corrected.json` and `check-corrected.py`. The initial `task6-clean-checks.json` retains its failing exits and must not be relabelled as green.

This approval does not establish full native TypeScript compilation, a packaged build, live FMP/browser behavior, save/reopen, retained-bind recreation or image publication. Tasks 7.1 and 7.2 remain open. No production or test file was changed by this reviewer.
