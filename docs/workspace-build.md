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
