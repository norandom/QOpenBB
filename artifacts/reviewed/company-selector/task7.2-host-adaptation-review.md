# Group-context host test: independent review

The frozen test-only adaptation is **APPROVED**. It verifies both effects of an incompatible group change: existing suggestions close without writes, and a fresh listing-selection attempt remains blocked. It preserves the original assertion that the origin remains AAPL and does not change production behavior.

Date: 2026-10-30. Reviewer: independent `gpt-6.1-sol` context, applying `kiro-review` and `kiro-verify-completion`. Workspace HEAD: `b5193dbd7a553912daa5ea72df981c3fdb49d365`; checkout: `/home/mc/qopenbb-work/financial-proposals-20261030/sources/workspace`.

## Review Verdict

- VERDICT: APPROVED
- TASK: 7.2 bounded host-test adaptation following the approved Symbol draft repair.
- MECHANICAL_RESULTS:
  - Tests: PASS, independent full native host file **30 passed, zero failed, zero skipped**, exit 0. Started 20:06:44 local time; duration 31.84 seconds.
  - TBD/TODO grep: CLEAN; zero placeholder-marker matches in the changed test.
  - Secrets review: CLEAN; no credentials or new credential handling introduced.
  - Static checks: PASS, scoped Biome checks one file without changes, exit 0; `git diff --check` exits 0.
  - Boundary: WITHIN; only the existing `terminalpro/tests/unit/components/General/Table/NavBar/QueryParams.test.tsx` changed in this follow-up. Its hash and all twelve previously frozen accepted production/test hashes match the worker freeze. The presenter and its 52-case unit file remain unchanged.
  - Boundary audit: CLEAN; no production, dependency, build, browser, provider or commit changes by this reviewer. Production complexity caps do not apply to this test-only adaptation.
  - RED phase: VERIFIED, retained original host receipt has 29 passed / 1 failed, exit 1. Failure occurs when the old helper clicks an option after the real group mutation has already invalidated the popup.
- FINDINGS: No blocking finding. The adaptation retains the fresh group-compatibility check and adds nonvacuous popup-invalidation coverage.
- REMEDIATION: None for this bounded test change.
- SUMMARY: The host regression now asserts current invalidation behavior and still proves that an actual fresh selection cannot write into an incompatible group.

## Evidence and acceptance boundary

Reviewed test SHA-256: `5725b8a9fbc821cc6c6de338f7709b179f42066c8fc41dd2225199ce11550165`.

The actual diff splits `lookupCompany` from the existing click helper and adapts one test; other differences only reorder imports. It first proves that Microsoft is visibly offered and the field is expanded. A real Zustand mutation changes the grouped peer to `fred_series`. Assertions then require the option/listbox to disappear, the field to close, both writer spies to remain unused and the origin Symbol to remain AAPL. A new lookup renders a real option which the original click helper selects; the original compatibility feedback, no-write and preserved-AAPL assertions remain. No optional click or detached-node shortcut bypasses the interaction.

This aligns with company-selector requirements 1.3-1.5, the design's exact compatible-group and current-context commit contracts, and tasks 4.2, 5.2 and 7.2. It does not replace the presenter unit test that mutates fresh context immediately before a choice, nor modify the strict production guard.

Independent verification used the existing helper without changing it:

```sh
/mnt/d/Source/QOpenBB/pipeline/.venv/bin/python /mnt/d/Source/QOpenBB/artifacts/company-selector-implementation/check-draft-host.py
```

The helper runs pinned Node 24.22.1 and Vitest 4.1.11 against `tests/unit/components/General/Table/NavBar/QueryParams.test.tsx`, with `--maxWorkers=1 --fileParallelism=false`. It exited 0. The fresh independent receipt is privately retained at `artifacts/company-selector-implementation/task7.2-host-adaptation-review-vitest.log`, SHA-256 `d211c84bc857719271d1757a38cceb07975624e2758c3022d0cb721bb190fd68`. The helper's original worker receipt was restored byte-for-byte after copying the new independent output, preserving the worker freeze's historical evidence identity.

From the Workspace `terminalpro` directory, the scoped static command was:

```sh
/mnt/d/Source/QOpenBB/artifacts/task-1.2/node-v24.22.1-linux-x64/bin/node node_modules/@biomejs/biome/bin/biome check tests/unit/components/General/Table/NavBar/QueryParams.test.tsx
```

It exited 0 and checked one file. An initial attempt using bare `python3` found no executable and did not execute a suite; it supplies no independent test evidence. The successful absolute-Python invocation above is the fresh verification receipt.

## Verification Result

- STATUS: VERIFIED
- CLAIM_TYPE: TEST_OR_BUILD
- CLAIM: The exact frozen host-test adaptation passes the independent complete 30-case host suite and scoped static checks, with no remaining task-local review finding.
- EVIDENCE: Fresh commands above exited 0; no failed or skipped cases; frozen test plus twelve accepted hashes matched; whitespace clean.
- GAPS: Packaged real-FMP, browser timing/layout, saved reopen, retained-bind recreation, source pin/inventory binding and rebuild acceptance remain controller-owned and open. This verdict does not complete task 7.2 or approve feature GO.
