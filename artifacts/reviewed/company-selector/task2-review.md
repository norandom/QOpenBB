## Review Verdict

- VERDICT: APPROVED
- TASK: Company selector 2, connected-source company search
- MECHANICAL_RESULTS:
  - Tests: PASS. Fresh independent native Vitest run passed 35 tests in one file, exit 0, on 2026-10-30 at 14:43:15 Europe/Berlin; duration 3.64 seconds.
  - TBD/TODO grep: CLEAN. No TBD, TODO, FIXME, HACK or XXX matches in the three reviewed files; grep exit 1 denotes no matches.
  - Secrets grep: CLEAN. Direct source inspection and targeted search found no credential material or raw-error logging. The URL password guard and synthetic secret/private test values are intentional checks.
  - Static checks: PASS for scoped Biome, three files, exit 0, no fixes applied. Runtime imports and concrete new types were manually inspected. Native TypeScript checking is BLOCKED by the existing dependency/composite prerequisite described below; no full native typecheck pass is claimed.
  - Complexity: PASS. Fresh existing project-syntax-units-v1 parser: companySearch.ts 218 physical/79 logical/max 14 per function; useCompanySearch.ts 198/99/max 21. Both satisfy 400/300/50.
  - Boundary: WITHIN. The bounded Git diff was empty because all three task files were untracked; their complete actual contents were inspected. No source, dependency or configuration edits, commits, builds or browser operations were made by this reviewer.
  - Boundary audit: CLEAN. Transport and transient search state remain separate from selection commits, UI, group writes and persistence. The existing request helper and frozen contract remain their owners.
  - RED phase: VERIFIED from the implementer's original retained tool output, not rerun or reconstructed. Original functions.exec chunk 8b6b50, exit 1, records five native public-error assertion failures and 30 passes before correction. Details follow below.
- FINDINGS:
  1. FYI: No blocking source findings. The bounded adapter/hook meets task 2's requirements 1.1/1.3/1.4/1.5 contribution. This does not accept downstream explicit commits, paired controls, dashboard grouping, save/reopen or real-FMP behavior.
  2. FYI: Native full-project TypeScript and packaged runtime verification remain unverified. The existing shared task27 dependency cache lacks the required Zod type and chart dependency; focused tests mock only unrelated chart imports. A compiled candidate and actual integration acceptance remain required at the controller's join/release gates.
- REMEDIATION: None within task 2. Controller retains combined scope/inventory enforcement, source acceptance and selective commit; full native build and application acceptance remain open.
- SUMMARY: Approve the frozen connected-source adapter and search hook for task-local acceptance, with the native typecheck/build limit explicitly retained.

## Reviewed source and contracts

Workspace checkout: `/home/mc/qopenbb-work/financial-proposals-20261030/sources/workspace`.

Reviewed HEAD: `4b03f11044dc9dae70828b94224a00664c0032fe`. The three new files were untracked against that HEAD, so the empty Git diff did not establish their content; direct full-file inspection did.

| Workspace-relative path | Independently verified SHA-256 |
| --- | --- |
| terminalpro/src/components/General/Table/NavBar/companySearch.ts | eed7de3c22e7ca88da09d9afa81a09c996c302736b3e5c0e4d5b2e1e3527e3f3 |
| terminalpro/src/components/General/Table/NavBar/useCompanySearch.ts | 3c820da557b2cb05ce1edf9afdca256a6140361ac0db324cfbbc34c8821989a6 |
| terminalpro/tests/unit/company-search.test.ts | 8d4b4669e70918bcc1f6e2f1e14d9af2dcee6b55e16550032f148cd5f0470476 |
| terminalpro/src/components/General/Table/NavBar/companySelection.contract.ts, frozen dependency identity | 05df8c419f6b2c2921e31ddc7e1bbbba785a308b76421d1085d4145d16ee3ac0 |

All identities matched the worker report and frozen contract after verification. Final status contained only the three task 2 files. The parent removed the three untracked compiler outputs from the failed preparation attempt; no task source changed.

Read task 2 and its Search adapter/search hook boundary, requirements 1.1/1.3/1.4/1.5, and design sections Typed ports, Search adapter, and Failure and persistence behavior. Checked the actual getEndpointParamRequestArgs implementation. The unchanged data API at `28423762e8cc3faae978e770899834b41e7cde99` supplied the local equity_search.py, discovery_data.py and financial_errors.py contracts. No network lookup or broad infrastructure audit was performed.

## Behavioral assessment

Request construction requires the resolved widget endpoint to match its source prefix and known native binding. It clones header configuration before calling the actual existing helper, preserves connector prefixes and effective headers, and targets the owned search route with explicit FMP provider, mode, bounded query and limit 20. The new modules introduce no dependency installation or alternate request helper.

The adapter validates the native results envelope, dataset/provider, effective query and limit, mode-specific source endpoint and retrieval timestamp. It maps canonical snake-case identity fields into the frozen listing type, preserves alternatives and order, and keeps omitted optional fields null. It does not synthesize a company name or acquisition time. The pinned API indeed uses effective_query.query/limit and search-name/search-symbol provenance, without effective_query.is_symbol.

Public native error codes are read independently of their historical HTTP statuses. Authentication/entitlement, throttling, invalid input, invalid response and network failures map to safe fixed messages; raw bodies and connector credentials are not logged or returned in outcomes. Empty valid results remain distinct from failures.

The hook uses 250 ms debounce, asymmetric 2/1 character thresholds, no retries and a 30-second, at-most-20-success per-mount cache. Cache keys contain opaque mount identity, generation, source, mode and query; effective headers/configuration stay in private memory. Source/auth changes remove old entries, clear visible results and increment generation. Abort plus active request/configuration checks reject late replies even when the port ignores cancellation. isCurrent additionally checks generation, request ID, source, mode and query before a result can be used by downstream selection logic. Cache hits keep their original acquisition timestamp while acquiring current request identity.

Focused tests exercise the actual helper, prefix/header immutability, native error statuses/codes, malformed contracts, alternatives/nulls, debounce and thresholds, out-of-order replies, cancel, header/source mutation, ignored abort, cache expiry/identity, explicit recovery, size bounds and cleanup. They assert meaningful output and lifecycle effects rather than only module availability. Tests mock AgGridUtils and useUpdateColumnState because their unrelated chart graph requires echarts, absent from the current shared dependency cache; the request helper and URL/header utilities execute unchanged.

## Reproduced checks and limits

Commands ran from the checkout's terminalpro directory through WSL Debian. NODE denotes `/mnt/d/Source/QOpenBB/artifacts/task-1.2/node-v24.22.1-linux-x64/bin/node`.

```text
NODE node_modules/vitest/vitest.mjs run tests/unit/company-search.test.ts --maxWorkers=1 --fileParallelism=false
NODE node_modules/@biomejs/biome/bin/biome check src/components/General/Table/NavBar/companySearch.ts src/components/General/Table/NavBar/useCompanySearch.ts tests/unit/company-search.test.ts
```

The existing `/mnt/d/Source/QOpenBB/tools/quality/syntax_units.ts` accepted a JSON array containing the two absolute production paths, through pinned NODE, exit 0. Independent wc line counts confirmed 218 and 198 physical lines. Git diff --check exited 0, with the limitation that Git does not include untracked contents. WSL rg was unavailable on the initial convenience probe; plain grep supplied the required marker scan.

The worker's original behavioral RED output, forwarded from its retained transcript, used the same focused Vitest command. It records start 14:37:53, duration 5.29 seconds, five failures and 30 passes. Failing cases were HTTP 502/authentication and 502/entitlement (expected entitlement, received network), 400/throttling (expected rate_limit, received invalid), 502/invalid_response (expected contract, received network), and 400/timeout (expected network, received invalid). Original tool identity: functions.exec chunk 8b6b50, exit 1, original_token_count 2359. The output was not retained as a standalone raw file. The fresh independent GREEN above confirms all 35 current assertions pass.

Read the retained task2-tsc-pinned.log and task2-tsc-preparation.log. The pinned noEmit attempt stopped at TS6305 for unbuilt runtimeConfigSchema.d.ts. The authorized TypeScript 6.0.3 preparation attempt exited 1 with existing TS2724 errors in runtimeConfigSchema.ts lines 215, 266 and 280: shared task27 Zod v4 does not export AnyZodObject. Its conditional follow-up noEmit did not run. No complete native typecheck or build reached the new sources. Manual inspection found no concrete new type/runtime import fault; this narrower observation cannot substitute for that gate. The reviewer did not repeat the heavy preparation attempt or alter dependencies.

No live provider, packaged application, browser, selection write or persistence acceptance is claimed. The canonical combined inventory and compiled full candidate remain controller-owned gates.
