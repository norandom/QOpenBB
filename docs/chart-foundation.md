# Verify the isolated chart foundation

The chart foundation provides separate integrated/detached state reducers and a React host for ECharts, verified in isolated fixtures. Application controls do not yet import these modules. Resolved flat snapshots and three Cartesian mappings now pass isolated verification; see [snapshot verification](../.kiro/specs/openbb-self-service/chart-snapshot-verification.md). Original editor behavior, styling, full family coverage and backend save/reopen remain later gates under the [approved task boundary](../.kiro/specs/openbb-self-service/tasks.md#approved-design-slice-chart-state-and-lifecycle-foundation).

The next stored-option slice is also accepted: baseline initialization/partition transitions and column-editor patches compose with the original reducers. Fresh verification passes 221 unit tests, strict TypeScript, scoped lint and twelve-module complexity checks. See [option-state verification](../.kiro/specs/openbb-self-service/chart-option-state-verification.md). This adds state compatibility evidence; it does not establish effective styling or application parity.

ECharts is pinned to 6.0.0 in the owned Workspace package and Bun lock, with zrender 6.0.0 and tslib 2.3.0. Bun 1.4.3 remains the existing lock compatibility exception; migrating to pnpm would change unrelated baseline resolution. Retain the installed ECharts `LICENSE` and `NOTICE` and zrender `LICENSE`; these packages use Apache-2.0 and BSD-3-Clause respectively. Lock integrity hashes identify the downloaded package contents.

## Restore and run

Use Node 24.22.0 and Safe Chain 1.5.25 from the [pinned development setup](development.md). In a disposable Linux copy of `terminalpro`, without `.env`, account state or provider credentials, restore through the protected wrapper:

```sh
export SAFE_CHAIN_MINIMUM_PACKAGE_AGE_HOURS=48
safe-chain bun safe-chain-verify
safe-chain bun install --frozen-lockfile
node node_modules/vitest/vitest.mjs run --config tests/unit/chart-compatibility/vitest.config.mjs
node node_modules/typescript/bin/tsc --project tests/unit/chart-compatibility/tsconfig.json --noEmit
node node_modules/vite/bin/vite.js build --config tests/e2e/chart-compatibility/vite.config.ts
```

The focused TypeScript configuration includes the complete new compatibility/host module directories, unit tests and browser fixture sources. It is separate from the upstream whole-application TS6305/TS5103 failures. Vitest uses one worker; its real-library SVG server-rendering check validates known synthetic values. The browser fixture uses `envDir: false` and only synthetic observations. The original smoke uses `123.45 USD` and `67.89 USD`; the Cartesian fixture adds fractional, negative, zero and null Revenue/Costs observations with repeated dates.

The root verification environment pins Playwright 1.64.0. The application lock separately retains 1.62.1. For the browser command, temporarily resolve the fixture's `@playwright/test` to the root verification package in the disposable copy; mixing the copies fails test registration. `QOPENBB_ROOT` must name the absolute root checkout path:

```sh
export PLAYWRIGHT_BROWSERS_PATH="$QOPENBB_ROOT/artifacts/playwright-browsers"
export CHART_EVIDENCE_ROOT="$QOPENBB_ROOT/artifacts/chart-foundation-verification"
mv node_modules/@playwright/test node_modules/@playwright/test-app-1.62.1
ln -s "$QOPENBB_ROOT/verification/node_modules/@playwright/test" node_modules/@playwright/test
trap 'rm node_modules/@playwright/test; mv node_modules/@playwright/test-app-1.62.1 node_modules/@playwright/test' EXIT
node "$QOPENBB_ROOT/verification/node_modules/@playwright/test/cli.js" test --config tests/e2e/chart-compatibility/playwright.config.ts
```

The config starts its own loopback production preview on port 4293, refuses an existing server, uses a fresh headless browser context and rejects worker/debug overrides. The smoke asserts visible SVG category, unit and numeric labels, the real library version and option values, then explicit disposal. CDP retains diagnostic categories/statuses only; a synthetic screenshot and JSON result identify the output. No operator browser or stored authentication is used. Preview shutdown belongs to Playwright; browser disposal is automatic at test completion.

## Evidence and limits

On 2026-10-16 the checks ran in `/mnt/wsl/qopenbb-task28/terminalpro` under WSL Debian as `mc`, against the accepted Workspace base `48e3f59cc48e0ae7aa6f6ce92069fc5b10ee3e86` plus this task's package, lock and fixture files. The selected application tools were Vite 8.2.1, Vitest 4.1.11 and TypeScript 5.9.2. Root verification used Playwright 1.64.0 and its pinned Chromium. Ignored `artifacts/task-2.13/` retains the initial missing-dependency RED, protected add/frozen restore, fresh restore, verification log, browser JSON, screenshot and sanitized CDP attachment. ECharts and zrender license hashes are retained with restore output.

The tooling fixture imports ECharts directly. The separate host fixture imports the maintained React host and exercises the actual lifecycle implementation. Its large full-library bundle warning is expected for this isolated setup and does not change application bundling. Browser acceptance is disproved by missing/incorrect visible observations, dirty diagnostics, a failed disposal or an orphaned owned preview listener. Use the [current scoped complexity gate](complexity.md), with truthful dirty-fork manifests; tests and fixture configurations are explicitly excluded as tests, while the maintained package manifest remains measured.

## Component contracts and joined checks

| Boundary | Preserved behavior | Actual check |
| --- | --- | --- |
| State inputs | Unknown JSON fields, narrowly permitted runtime undefined values, repeated-edit closure | 10 contract cases and strict type fixtures |
| Integrated reducer | Resolved option baseline, lodash array merging, top-level theme removal, shallow model overlay and original metadata ordering | 16 reducer cases shared with the detached path |
| Detached reducer | Existing model retained except chart type; options replaced, including an own undefined property | Original-source reference cases in the reducer suite |
| Lifecycle owner | Complete options, increasing revisions, zero-size deferral/recovery, PNG export and terminal cleanup | 13 mocked-library lifecycle cases |
| React host | Observer ownership, updates, error reporting, StrictMode cleanup and retained export handles | 6 host unit cases |
| Real renderer | Known numeric values, visible output, resized/updated PNG contents, hidden remount, formatter failure and recovery | Actual-host browser journey plus the original tooling smoke |

The current focused suite contains 124 tests: 46 foundation, 26 snapshot and 52 mapping cases. Its production browser suite has three cases with captured CDP diagnostics and synthetic image evidence. The earlier foundation gate also verified the existing Perspective runtime with 10 unit cases, strict checking and four browser regressions; that evidence is historical and was not rerun for this isolated mapping slice. These counts describe component verification, not dashboard acceptance.

Task-local evidence is under ignored `artifacts/task-2.13/` through `task-2.17/`; independent reports live in each task's `review/` directory. Joined evidence and the Perspective regression are under `artifacts/task-2.18/`. Use the [foundation verification record](../.kiro/specs/openbb-self-service/chart-foundation-verification.md) for source identities, review status and remaining integration obligations.

Commands above remain portable verification commands outside Dagger. A successful isolated PNG export does not establish the original menu, filename or persistence behavior. Full-application TypeScript remains outside this focused gate, and no renderer-complete image is promoted by it.
