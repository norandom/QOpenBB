# Node security baseline patch

Node 24.22.1 replaces the active 24.22.0 baseline. Worker edits are frozen for independent parent review. No image build, dependency upgrade, commit or publication ran.

## Sources and verified identities

- Official security release: https://nodejs.org/en/blog/release/v24.22.1
- Published checksums: https://nodejs.org/dist/v24.22.1/SHASUMS256.txt (retained as SHASUMS256.txt).
- Download: https://nodejs.org/dist/v24.22.1/node-v24.22.1-linux-x64.tar.xz
- Published and actual tar SHA256: 6c172a9ab6718f7b801fb5a7bd486af2ee5e32758086a04b84fcce2aa77095e6; sha256sum -c passed before extraction.
- Installed executable SHA256: e32e2d16081cf644f88392934288086e7662529d0d43277c34f7aad2207cfafb.
- Docker registry query: docker buildx imagetools inspect docker.io/library/node:24.22.1-bookworm-slim (exit 0; docker-manifest.txt).
- Registry image index: sha256:be8204d4bd327363357f532187b752ff62759c31bedf98e9e18fc08c9cbd605c.
- Its linux/amd64 manifest: sha256:e1582112fb9f152ed38eefcd712efc93fee1becb519fdfa57574d5e07eaa5e7d.

## Changed scope

.node-version, pipeline/tools.lock.json, verification/package.json; docs/development.md, docs/verification.md, docs/complexity.md, docs/chart-foundation.md, docs/workspace-build.md; vendor/workspace/lite/Dockerfile Node FROM pin only. The historical 2026-10-16 Node 24.22.0 evidence paragraph remains historical. No application dependency lock changed.

Root configuration physical counts are 1, 62 and 20 respectively; Workspace Dockerfile is 188. All are below 400. Configuration/build definitions receive physical counts only; logical/function caps do not apply. Documentation is excluded. Exact bytes are in modified-config-measurements.json. Parent owns combined inventory, source lock and contract integration checks.

## Executed verification

Every JavaScript check set PATH first to $PWD/artifacts/task-1.2/node-v24.22.1-linux-x64/bin. Node 24.22.0 was not executed by this worker.

- node --version: v24.22.1; npm --version: 11.19.1 (exit 0).
- node --test tests/quality/test_syntax_units.mjs: 15 passed, zero skipped (exit 0; node-quality.log).
- node verification/node_modules/typescript/bin/tsc --project tools/quality/tsconfig.json: pass (exit 0; strict-typescript.log).
- pipeline/.venv/bin/python -m pytest -c pipeline/pyproject.toml tests/quality -n0 --maxprocesses=2: 76 passed in 59.16s (exit 0; quality-pytest.log). Includes parent-updated runtime adapter tests.
- artifacts/task-1.2/pnpm/pnpm --dir verification install --offline --frozen-lockfile --lockfile-only --ignore-scripts: pass, pnpm 10.32.1 (exit 0; frozen-lock.log). This checked frozen importer consistency offline; no dependency resolution/download or dependency restoration occurred. git diff -- verification/pnpm-lock.yaml was empty afterward. Lock SHA256 fc24794a0d85054dbaf05ed445a171624590cd4ac84c4f14595805b2c92c7507.

The patched archive was extracted into ignored artifacts/task-1.2 through the existing checksum-before-extraction bootstrap mechanism. Old installed toolchain files were retained without execution. No browser or packaged-image acceptance is claimed by this routine patch.
