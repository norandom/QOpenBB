# Verify infrastructure without provider credentials

For the separately accepted backend test and query layers, use the [SQLite repair verification](../.kiro/specs/openbb-self-service/sqlite-repair-verification.md). With the frozen backend Python environment restored, run from the repository root:

```sh
/home/mc/qopenbb-work/sqlite-runtime/venv/bin/python \
  vendor/workspace/backend-api/backend/tests_sqlite/run.py
```

That interpreter path identifies the exercised WSL environment. The maintained launcher creates an isolated child with synthetic configuration, blocks operator env/account reads and network access, and removes its file databases after exit. Its 60 tests cover six read paths, sharing/creator semantics, actual bulk save/update and SQLite engine recreation. They do not prove browser save/reopen, container restart or deployment. No provider credentials are needed.

Run the fixture checks before attaching application acceptance tests. They display a synthetic observation of `123.45 USD`, verify fresh cookie/local-storage state, and deliberately produce console/network failures through the owned browser's CDP session. A green result establishes verification infrastructure only. Workspace, live FMP/FRED, Anthropic, Excel, Compose and deployment remain unverified.

## Run in WSL or Linux

Restore the pinned [development tools](development.md). From the repository root:

```sh
export PATH="$PWD/artifacts/task-1.2/node-v24.22.0-linux-x64/bin:$PATH"
PLAYWRIGHT_BROWSERS_PATH="$PWD/artifacts/playwright-browsers" \
  node verification/node_modules/@playwright/test/cli.js install chromium
# A prepared runner also needs Playwright's Chromium OS dependencies.
node verification/node_modules/@playwright/test/cli.js test --config verification/playwright.config.ts
pipeline/.venv/bin/python verification/runner.py tests/delivery/test_verification.py
```

Playwright 1.64.0 selects Chromium revision 1248 (156.0.8078.4). The runner launches that exact project-local Linux executable; no operator browser discovery or CDP attachment is available. On the observed Debian host, the first launch failed because libglib was absent. Installing the pinned Playwright CLI's `install-deps chromium` OS dependency list enabled actual browser execution. A fresh Linux runner and native Windows browser execution still need separate verification.

The canonical browser command uses one worker and rejects CLI worker overrides and debug environment settings. The Python wrapper permits zero to two xdist workers, removes inherited pytest/plugin options, uses explicit synthetic fixture markers, and isolates output and temporary directories. `live` is excluded by default and recorded as unverified. No live credential is loaded. A separately authorized live check must report missing credentials as skipped/unverified, never successful acceptance.

## Interpret evidence

Each browser run writes one `artifacts/task-1.7/runs/run-*/evidence.json` with source revision, tool/browser versions, timestamp, command identity, result, diagnostic categories and artifact root. Browser profiles are disposable and removed after success and fault paths. The fixture listener binds a dynamic loopback port and refuses an existing listener. Tests prove closure after success, startup failure, artifact failure and diagnostic failure. The standalone `node verification/runner.ts --failure` command exits nonzero on unexpected console/network errors.

CDP uses Playwright `context.newCDPSession` on the browser this run owns. Runtime and Network events retain category and HTTP status only. They discard URLs, headers, cookies, request/response bodies, exception text and console arguments before writing evidence. This protects even secret-bearing error strings; it is deliberately less detailed than an application debug log. Synthetic sentinel regressions check retained evidence for leakage. Raw screenshots, video and traces remain off; requesting capture for credential entry is refused before creating a run. Credential scenarios must never enable capture.

Browser children receive an environment allowlist; provider/model/registry variables, dotenv files and inherited Node options are unavailable. The runner invokes no external server helper: the HTTP fixture is an owned in-process server. Playwright launches hidden browser processes; the Git metadata helper uses `windowsHide`, and the Python subprocess uses `CREATE_NO_WINDOW` where supported. Native Windows execution has not been exercised by this WSL evidence.

Python evidence lives under `artifacts/task-1.7/pytest/run-*`, with bounded worker count, exact command, exit and numeric result counts. Raw pytest stdout and JUnit are never retained, because failure assertions can expose credentials. xdist temporary roots and test-local paths separate workers; the wrapper removes its temporary root in finally so failing-test sources and bytecode are not retained. These are disposable synthetic records. Do not reuse operator account state or interpret skipped live tests as verified provider behavior.

Task-local RED, flag-enabled GREEN, flag-removed GREEN, type checks, dependency setup and complexity reports are retained under `artifacts/task-1.7`. Re-run the [combined complexity gate](complexity.md) after changes. The acceptance disproof is a missing observation/unit, shared browser state, retained synthetic secret, leaked owned process/listener, unbounded worker override, or a failure reported as passed.
