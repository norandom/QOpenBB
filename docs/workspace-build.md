# Reproduce the Full frontend

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
