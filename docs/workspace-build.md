# Reproduce the Full frontend

For the separately approved chart tooling setup, use [isolated chart foundation verification](chart-foundation.md). It retains the protected Bun lock strategy and does not establish renderer parity.

The Full frontend builds from the owned Workspace monorepo with its unchanged Bun lock. This is task 2.1 packaging evidence, not an accepted application image or dashboard. Image assembly, account startup and routing remain later gates in the [task plan](../.kiro/specs/openbb-self-service/tasks.md).

The adapted `vendor/workspace/lite/Dockerfile` defaults to `OPENBB_IMAGE_VARIANT=full`. Its frontend stage pins Bun 1.4.3 and Node 24.22.0 by image digest, downloads checksum-verified Aikido Safe Chain 1.5.25, verifies protection, then runs `safe-chain bun install --frozen-lockfile` with a 48-hour minimum package age. Bun is retained because migrating the supplied lock to pnpm would change baseline resolution. No package or lock change is part of this task.

Build inputs are `terminalpro/package.json`, `terminalpro/bun.lock`, the owned frontend source and `lite/frontend.full.env`. Supply a nonsecret `VITE_RELEASE_VERSION` explicitly. The build does not read the excluded private `terminalpro/.env`; its generated build environment comes from the selected checked-in Full settings. TradingView is explicitly disabled because its separately supplied entitled assets are unavailable.

The Vite runtime-configuration plugins were extracted into `terminalpro/build/runtimeConfig.ts` to keep the whole maintained configuration within the project size limits. Remote Google font stylesheet loading and its build downloader were removed. Existing repository Inter and Roboto assets remain available; optional font selections fall back when their fonts are absent. This avoids a hosted font fetch during the build.

## Verified frontend checkpoint

On 2026-10-16, the source snapshot at Workspace base `be00e95019a55d57af146919ee46b7e1a4859226` plus the four task changes was installed and built in `/tmp/qopenbb-task-2.1-frontend/terminalpro` under WSL. A native Linux temporary directory avoids dependency-install I/O overhead on the Windows mount. Only checked-in source and the public Full environment were staged; no private environment file was used.

From that staged frontend directory, use the pinned tools described in [development](development.md):

```sh
export SAFE_CHAIN_MINIMUM_PACKAGE_AGE_HOURS=48
export VITE_RELEASE_VERSION=qopenbb-task-2.1
export VITE_TRADINGVIEW_ENABLED=false
export NODE_OPTIONS=--max-old-space-size=8192
safe-chain bun safe-chain-verify
safe-chain bun install --frozen-lockfile
bun run build:runtime
```

Ignored evidence under `artifacts/task-2.1/` records exact commands and exits in `resume-evidence.json`, command logs, before/after lock hashes, the original two failing packaging regressions, their passing rerun and the combined complexity report. The tested lock SHA-256 is `6bf311d0714daa825d7d0b89c9519ce48ed882a23ba7d206565168b61e7149e0`. The portable regression is `tests/delivery/test_workspace_packaging.py`. Reopen this checkpoint if the lock changes, protected install fails, the frontend stops building, or staged source differs from the reviewed changes.

AG Enterprise and Highcharts remain unresolved provisional packaging inputs. Their successful compilation grants no entitlement and establishes no supported dashboard capability. Publication waits for removal and new image evidence in tasks 2.6-2.12. Backend dependency/startup changes belong to 2.2; this checkpoint does not verify backend locks, a Dagger application image, account persistence or live-provider behavior. The disabled TradingView datafeed script still produces an upstream Vite bundling warning; no TradingView capability is claimed.

## Private backend bootstrap checkpoint

Task 2.2 preserves the upstream SQLite migrations, admin initialization and login handler. Startup now stops when migrations or admin initialization fail. Passwords are absent from the entrypoint summary. Retrieve the persisted admin credentials only in an operator session with `docker exec CONTAINER credentials`; its output is private and must not be retained in shared logs or evidence.

The complete `/data` bind remains the state boundary. `secrets.env` is written atomically with mode `0600`, using the previous settings on restart unless the caller explicitly overrides a value. The generated admin TOML also has mode `0600`; its directory has mode `0700`. Quotes and backslashes are escaped, and multiline credential settings are rejected before writing. Changing an explicit bootstrap password causes upstream admin initialization to update that account, so retain the private deployment configuration alongside the stopped-state backup.

Backend installation retains the upstream `backend-api/backend/poetry.lock` without regeneration. Poetry 2.3.2 and export plugin 1.10.0 check and export that lock; protected uv 0.12.5 installs its exact main requirements, including slowapi commit `d3442b2e1425a9db535732a0a06248470c7f9fd5`. `lite/build-tools.in` owns build-tool selections and generated `lite/build-tools.txt` pins their transitive dependencies with hashes. Cython 3.2.4, setuptools 82.0.1 and supervisor 4.3.0 are explicit build/runtime selections. Safe Chain retains its 48-hour minimum package age. The Dockerfile uses the recorded Python image digest and includes curl for its runtime health probe.

The focused executable regression is:

```sh
QOPENBB_STARTUP_PYTHON=/absolute/path/to/restored/backend/bin/python \
QOPENBB_STARTUP_REDIS_PORT=16379 \
pipeline/.venv/bin/python -m pytest -c pipeline/pyproject.toml \
  -n0 --maxprocesses=2 tests/delivery/test_workspace_startup.py
```

The optional runtime check requires a compatible restored backend interpreter and disposable Redis on the selected port. Without the interpreter input, pytest reports that runtime check as skipped. It copies checked-in backend source to a fresh temporary directory, migrates a new SQLite database, initializes a disposable account and calls the upstream login handler twice across separate migration/bootstrap processes. It verifies a successful session response, unchanged account identity and persisted dashboard content in the repeated login response. Only the request rate-limit decorator is bypassed; authentication, account validation, session creation and database persistence remain upstream code. This is backend startup evidence, not browser or Compose acceptance.

On 2026-10-16, protected frozen dependency restoration and first/repeated backend startup passed in a native WSL temporary directory. The first runtime regression used a reserved `.invalid` email domain and correctly failed upstream email validation; the disposable address was corrected to `example.com`, with email delivery disabled. Sanitized command records and lock/source hashes are under ignored `artifacts/task-2.2/`. Actual Cython application image compilation, image-layer inspection, Compose health and browser sign-in remain later gates. Reopen this checkpoint if the lock changes, a protected install fails, bootstrap exposes credentials, or repeated login loses the saved state.

## Application request boundary

Task 2.3 resolves request URLs against the browser origin and compares the configured backend's normalized origin and full path segment. With `/api` configured, `/api/pro/user` receives the Workspace session; `/data/api/v1/...`, `/agent/...`, lookalike prefixes and other origins retain connector-supplied headers. Historical hosted file URLs receive no local session exception. Explicit application Authorization replacement uses the case-insensitive Headers API.

Run `node --test tests/unit/backendOrigin.test.mjs` from `vendor/workspace/terminalpro` for URL/header cases. With the frozen frontend dependencies restored, run `node_modules/.bin/vitest run --config tests/unit/requestBoundary.config.mjs` there to exercise `useJsonData`, `useMultipleQueries` and `fetchWithToken` with a captured fetch boundary. From the repository root, `tests/delivery/test_request_boundary.py` runs the URL/header suite through the portable pytest gate. Use pinned Node 24.22.0. These fixture checks do not establish browser login, origin routing, provider connectivity or Office compatibility.

On 2026-10-16, 24 URL/header cases and 27 actual caller cases passed in WSL, and the unchanged frozen frontend dependency snapshot built with Bun 1.4.3. Ignored task evidence is under `artifacts/task-2.3/`. Reopen this checkpoint if the backend base, header handling or request callers change.
## Single public origin checkpoint

Set `PUBLIC_URL=https://qbb.hanse-hedge.fund` for the owner-managed Cloudflare Access tunnel, or `http://localhost:23003` for direct local development. The same topology accepts plain HTTP on `0.0.0.0:23003` and preserves the whole `./data/workspace:/data` bind. The owner manages cloudflared, policies and public HTTPS; Workspace manages no origin certificates or tunnel process.

Startup validates an HTTP(S) origin with no credentials, path, query or fragment. It renders `FRONTENDURL` and `PROURL` from that origin, `SELFURL` with `/api`, and forwarded protocol from the configured public scheme. Incoming protocol headers cannot replace that scheme. Changing the public origin requires a container restart, not an image rebuild.

Register the data connector with the absolute base `https://qbb.hanse-hedge.fund/data`, and later register the custom agent with `https://qbb.hanse-hedge.fund/agent`. Runtime `config.js` advertises these as `urls.data` and `urls.agent` metadata for registration; the current frontend does not automatically consume those keys or register a connector. Use the corresponding localhost bases for direct development. Actual account/connector discovery remains task 4.3. Hosted Copilot, web search, SEC/Jina helpers and AI enhancements are disabled; the custom agent does not implement the hosted AI API.

The origin removes exactly `/data` or `/agent` before forwarding, retains query parameters, and preserves existing application `/api` rewriting and WebSocket behavior. Failed API requests retain API/proxy failures instead of returning the frontend document. Agent streaming disables buffering and uses a 300-second idle timeout. Agent and Excel DNS resolve per request with a one-second resolution bound, so their absence does not prevent nginx startup. Excel returns 404 unless `EXCEL_ENABLED=true`; enable it only with the later accepted Excel service. No Excel source or functionality is implemented here.

Run the focused fixture gate in WSL with `pipeline/.venv/bin/python -m pytest -c pipeline/pyproject.toml -n0 tests/delivery/test_origin_routing.py`. It uses the already cached nginx image identity `sha256:df221db836e1754089190208cee7eeda94f233197056426eda74a43ab1abeac2`, disposable ports and a named disposable container, with synthetic upstream responses and no provider/model requests. Tests exercise public URL validation, the actual frontend renderer, prefix/query and HTTPS forwarding, API failures, missing agent DNS, optional Excel absence and SSE delivery before stream completion. This establishes route behavior with fixtures; application-image, Compose and browser acceptance remain later gates. Reopen this checkpoint if routing, URL rendering or the selected nginx runtime changes.
