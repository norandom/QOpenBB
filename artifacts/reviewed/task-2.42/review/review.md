# Task 2.42 preserves selected saved options without changing state

## Review Verdict

- VERDICT: APPROVED
- TASK: 2.42
- MECHANICAL_RESULTS:
  - Tests: PASS. Fresh complete application suite: 126/126 tests, 6 files, exit 0; complete compatibility suite: 260/260 tests, 9 files, exit 0. The application total includes all 38 composition tests. No skipped tests or unhandled-error result was reported.
  - TBD/TODO grep: CLEAN, including FIXME/HACK/XXX.
  - Secrets grep: CLEAN. Explicit source and publication files contain no concrete credential finding.
  - Static checks: PASS. Both prescribed strict TypeScript projects exit 0. Prescribed scoped Biome checks 23 files, applies no fixes and exits 0.
  - Boundary: WITHIN. Only appearanceComposition.ts and its owned regression file introduce task 2.42 behavior.
  - Boundary audit: CLEAN. No reducer, baseline selector, theme generator, renderer, application hook, dependency, feature flag, guard, menu or UI changes belong to this task.
  - RED phase: VERIFIED as a preimplementation missing-module failure, with zero tests executed. It establishes the regression file preceded the helper, not that behavioral assertions failed during RED.
  - Complexity: PASS from the controller's frozen complete 175-file report: errors and violations are empty. This production file measures 59 physical lines, 30 logical units and function sizes of 12 and 13, below 400/300/50.
- FINDINGS:
  1. FYI: Review acceptance covers the pure composition contract against accepted sibling dependencies. Concurrent tooltip implementation, colors, the later combined 2.45 join and renderer/application persistence acceptance are outside this result.
  2. FYI: The controller's first complexity run used stale prerequisite revision manifests and failed. Its preserved failure is followed by refreshed explicit scope and a successful complete gate. No production correction was needed for this metadata fault.
- REMEDIATION: None for task 2.42.
- SUMMARY: The frozen helper reproduces the owned merge operation on detached validated data and stays within the approved composition boundary.

## Verification Result

- STATUS: VERIFIED
- CLAIM_TYPE: TASK
- CLAIM: Task 2.42's frozen pure saved-option composition and tests satisfy the approved source contract against accepted Workspace bc42d604855a6b5d943ce05ee9fcce11e356435a dependencies.
- EVIDENCE: Fresh independent complete suites, both strict compilers, prescribed scoped lint, immutable input hashes, original-source inspection, fixture provenance checks and controller complete complexity evidence.
- GAPS: No task-local blocking gap. B2 field projection, ECharts effects, original docked editor integration, application activation, numeric transformations and backend save/reopen/restart remain unverified by these checks. This result does not accept the current concurrent tooltip lane or the complete renderer.
- NOTES: The controller owns breadth acceptance status, reviewed publication and selective commits. The later 2.45 check must freeze and verify the actual joined lanes.

## Why the implementation meets the contract

The approved saved operand is `baseline.options`. The helper passes the original baseline into the existing descriptor-safe selector with an empty synchronization and no partition replacement; that preserves and copies its selected options. It does not select `model.chartOptions`. The mismatched-model regression would detect that substitution. The original model is validated but never merged or written.

The original hook at `Chart/hooks/useChartOptions.tsx:431`, revision `38dffc33389aca0e4a87e0e88d42f7067aa220df`, assigns `chartOptions.common = options.common` and returns `merge(options, chartOptions)`. The helper applies the same order to detached copies: generated common replaces the saved branch wholesale, then lodash merges generated options with saved overrides. It keeps own undefined, null, indexed array behavior, inactive families and unknown branches. The four frozen captured fixtures provide independent expected winners; the 64-pair matrix additionally compares with the pinned source operation, not the new helper itself.

Descriptor inspection rejects accessors without property reads; the existing selector rejects nonplain values, cycles and executable leaves. The public catch contains inspection failures. Tests cover both operands, hostile/revoked proxies, stored-model getters/cycles, array accessors, non-enumerable and symbol properties. No saved getter or function is invoked. Frozen and aliased inputs remain intact, and mutating the returned nested values does not alter input state.

This matches task 2.42 and the design's Saved composition, File Structure Plan and Testing Strategy sections. Requirements 1.1/1.4 receive pinned source/dependency identities and an explicit local adaptation; 4.2/4.7 receive state-preserving unit evidence only; 4.8/4.9 receive composition parity evidence only. Requirements 10.5/10.6 remain bounded by actual test paths and the unverified downstream gates recorded above.

## Reproducible evidence and isolation

[Verification script](verify.py), [stage identities](stage.json) and [exact commands, exits and log hashes](results.json) record a new WSL Debian stage with pinned Node 24.22.0 and the accepted dependency tree. The stage starts from the frozen accepted 2.41 Linux baseline, then copies current owned files and the relevant immutable source/test/config closure. Immutable files are compared with accepted Git bytes, permitting only checkout newline normalization. All six sibling-owned source/test paths are overlaid consistently from accepted `bc42d60`, with current and staged hashes retained. No workspace sibling file was changed. Both owned source hashes and the complete staged closure remained unchanged after verification.

Commands ran serially after the controller granted the heavy-check slot. [Application strict](application-strict.log), [compatibility strict](compatibility-strict.log), [application suite](application-suite.log), [compatibility suite](compatibility-suite.log) and [scoped lint](scoped-lint.log) all passed on their first independent attempt. No browser, install or retry-to-pass was performed. A historical intermittent AG/jsdom teardown failure was not reproduced in this run and is not erased by this pass.

The worker's [report](../implementation/report.md) accurately preserves the missing-module RED, BigInt title formatter failure, corrected proxy test setup, mixed sibling snapshot compiler failure and scoped formatting failure. Those failures are retained in the publication set rather than relabeled as successes. The controller's [stale-manifest failure](../controller/complexity-stale-manifest-failure.json), [successful complete size report](../controller/complexity.json), explicit fork scopes and source hashes are also retained. The complete size gate is controller evidence independently inspected here; it was not rerun by this reviewer.

[Evidence audit](audit.json) confirms implementer allowlist hashes, captured-fixture provenance, unchanged staged inputs, exact composition metrics and dependency package identities. [Publication allowlist](publication-allowlist.json) selects only completed synthetic reports, scripts, logs and manifests, preserves original paths/hashes and includes all failed attempts. It excludes credentials, environment files, caches, profiles, private state and image archives. No unowned source is selected for the evidence mirror.
