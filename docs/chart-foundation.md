# Verify the isolated chart foundation

Task 2.13 establishes ECharts tooling only. It does not establish the production host, saved chart compatibility, renderer parity or a release image. The [approved task boundary](../.kiro/specs/openbb-self-service/tasks.md#approved-design-slice-chart-state-and-lifecycle-foundation) retains those gates.

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

The focused TypeScript configuration includes the complete new compatibility/host module directories, unit tests and browser fixture sources. It is separate from the upstream whole-application TS6305/TS5103 failures. Vitest uses one worker; its real-library SVG server-rendering check validates known synthetic values. The browser fixture uses `envDir: false` and only hardcoded observations, `123.45 USD` and `67.89 USD`.

The root verification environment pins Playwright 1.64.0. The application lock separately retains 1.62.1. For the browser command, temporarily resolve the fixture's `@playwright/test` to the root verification package in the disposable copy; mixing the copies fails test registration. `QOPENBB_ROOT` must name the absolute root checkout path:

```sh
export PLAYWRIGHT_BROWSERS_PATH="$QOPENBB_ROOT/artifacts/playwright-browsers"
export CHART_EVIDENCE_ROOT="$QOPENBB_ROOT/artifacts/task-2.13"
mv node_modules/@playwright/test node_modules/@playwright/test-app-1.62.1
ln -s "$QOPENBB_ROOT/verification/node_modules/@playwright/test" node_modules/@playwright/test
trap 'rm node_modules/@playwright/test; mv node_modules/@playwright/test-app-1.62.1 node_modules/@playwright/test' EXIT
node "$QOPENBB_ROOT/verification/node_modules/@playwright/test/cli.js" test --config tests/e2e/chart-compatibility/playwright.config.ts
```

The config starts its own loopback production preview on port 4293, refuses an existing server, uses a fresh headless browser context and rejects worker/debug overrides. The smoke asserts visible SVG category, unit and numeric labels, the real library version and option values, then explicit disposal. CDP retains diagnostic categories/statuses only; a synthetic screenshot and JSON result identify the output. No operator browser or stored authentication is used. Preview shutdown belongs to Playwright; browser disposal is automatic at test completion.

## Evidence and limits

On 2026-10-16 the checks ran in `/mnt/wsl/qopenbb-task28/terminalpro` under WSL Debian as `mc`, against the accepted Workspace base `48e3f59cc48e0ae7aa6f6ce92069fc5b10ee3e86` plus this task's package, lock and fixture files. The selected application tools were Vite 8.2.1, Vitest 4.1.11 and TypeScript 5.9.2. Root verification used Playwright 1.64.0 and its pinned Chromium. Ignored `artifacts/task-2.13/` retains the initial missing-dependency RED, protected add/frozen restore, fresh restore, verification log, browser JSON, screenshot and sanitized CDP attachment. ECharts and zrender license hashes are retained with restore output.

The fixture imports ECharts directly to prove tooling; it is not a production lifecycle implementation. Its large full-library bundle warning is expected for this isolated setup and does not change application bundling. Browser acceptance is disproved by missing/incorrect visible observations, dirty diagnostics, a failed disposal or an orphaned owned preview listener. Use the [current scoped complexity gate](complexity.md), with truthful dirty-fork manifests; tests and fixture configurations are explicitly excluded as tests, while the maintained package manifest remains measured.
