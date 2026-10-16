# Development toolchain

Set up the locked tools before implementing or rebuilding QOpenBB. Use pnpm for maintained JavaScript projects and uv/uvx for Python, with Aikido Safe Chain protecting dependency installation. Task 1.2 establishes dependency installation and version/import checks in WSL; it does not yet provide a running Workspace or data API. Follow the [roadmap](roadmap.md) for the remaining acceptance gates.

## Prepare the host

Use Linux on amd64, either WSL or a disposable Linux runner, with Git, CA certificates, curl, tar, xz, sha256sum and a local Docker daemon. The observed host is Debian 13.5 under WSL. A clean CI runner must supply these prerequisites before invoking repository commands; no GitHub API, event payload or runner variable is required by the packages.

Install uv 0.12.5, Dagger CLI 0.21.8, Docker client/engine 29.7.2 and Compose plugin 5.4.0 through host setup. Use the [uv release](https://github.com/astral-sh/uv/releases/tag/0.12.5), [Dagger release](https://github.com/dagger/dagger/releases/tag/v0.21.8), [Docker instructions](https://docs.docker.com/engine/install/) and [Compose release](https://github.com/docker/compose/releases/tag/v5.4.0). Match [tools.lock.json](../pipeline/tools.lock.json); an unversioned installer or a Dagger 1.0 beta is not the pinned setup. The Docker context must address the local daemon. The user running checks needs daemon access and write access to this checkout and its ignored artifacts.

Keep installation and runner permissions outside core build and verification logic. Changing from GitHub to Gitea later changes this host setup and the thin workflow wrapper. Actual clean-runner execution remains unverified at this checkpoint.

## Install project-local runtimes

Run the following in a Linux shell at the repository root. They install Python, Node, Bun, pnpm and Safe Chain under ignored `artifacts/task-1.2`, without replacing host defaults. uv uses Astral's managed CPython distribution; [its Python installation guide](https://docs.astral.sh/uv/guides/install-python/) explains that source. Bootstrap binaries are pinned and checksummed separately from package installation.

```sh
set -eu
export QOPENBB_ROOT="$(pwd)"
export QOPENBB_TOOLS="$QOPENBB_ROOT/artifacts/task-1.2"
export UV_PYTHON_INSTALL_DIR="$QOPENBB_TOOLS/python"
export UV_CACHE_DIR="$QOPENBB_TOOLS/protected-uv-cache"
mkdir -p "$QOPENBB_TOOLS"
uv --version
uv python install --no-bin "$(cat .python-version)"
QOPENBB_PYTHON="$(uv python find 3.13.15)"
for runtime in node bun pnpm safe_chain; do
  url="$("$QOPENBB_PYTHON" -c 'import json,sys; print(json.load(open("pipeline/tools.lock.json"))["tools"][sys.argv[1]]["linux_x64_url"])' "$runtime")"
  digest="$("$QOPENBB_PYTHON" -c 'import json,sys; print(json.load(open("pipeline/tools.lock.json"))["tools"][sys.argv[1]]["linux_x64_sha256"])' "$runtime")"
  curl -fsSL "$url" -o "$QOPENBB_TOOLS/$runtime.archive"
  printf '%s  %s\n' "$digest" "$QOPENBB_TOOLS/$runtime.archive" | sha256sum -c -
done
tar -xJf "$QOPENBB_TOOLS/node.archive" -C "$QOPENBB_TOOLS"
"$QOPENBB_PYTHON" -m zipfile -e "$QOPENBB_TOOLS/bun.archive" "$QOPENBB_TOOLS"
chmod +x "$QOPENBB_TOOLS/bun-linux-x64/bun"
mkdir -p "$QOPENBB_TOOLS/pnpm" "$QOPENBB_TOOLS/safe-chain/bin"
cp "$QOPENBB_TOOLS/pnpm.archive" "$QOPENBB_TOOLS/pnpm/pnpm"
cp "$QOPENBB_TOOLS/safe_chain.archive" "$QOPENBB_TOOLS/safe-chain/bin/safe-chain"
chmod +x "$QOPENBB_TOOLS/pnpm/pnpm" "$QOPENBB_TOOLS/safe-chain/bin/safe-chain"
"$QOPENBB_TOOLS/safe-chain/bin/safe-chain" setup-ci
export PATH="$QOPENBB_TOOLS/safe-chain/shims:$QOPENBB_TOOLS/safe-chain/bin:$QOPENBB_TOOLS/pnpm:$QOPENBB_TOOLS/node-v24.22.0-linux-x64/bin:$QOPENBB_TOOLS/bun-linux-x64:$PATH"
export SAFE_CHAIN_MINIMUM_PACKAGE_AGE_HOURS=48
safe-chain -v
pnpm safe-chain-verify
uv safe-chain-verify
uvx safe-chain-verify
```

Node 24.22.0 supplies npm 11.19.1, but maintained verification uses pnpm 10.32.1 and its committed lock. Bun 1.4.3 is reserved for the owned Full Workspace's frozen-lock installation in task 2.1. Its compatibility with that application lock and Safe Chain remains unverified; do not rewrite that lock during foundation setup.

[Safe Chain 1.5.25](https://github.com/AikidoSec/safe-chain/tree/1.5.25) supports pnpm, Bun, uv and uvx. `setup-ci` creates project-local executable shims; explicit PATH setup also works outside GitHub. Each verification command above must print `OK: Safe-chain works!`. Keep the default 48-hour package-age protection; resolve an older compatible dependency or report a blocker if a frozen version is too recent. Playwright 1.64.0 was selected because 1.64.1 was inside that window on the setup date. Safe Chain checks package downloads for known malware; it does not establish provider correctness or application acceptance.

## Restore dependencies and check tools

Run the same lock-based setup locally or on the prepared Linux runner:

```sh
uv sync --project pipeline --locked --python 3.13.15
uv sync --project .dagger --locked --python 3.13.15
pnpm --dir verification install --frozen-lockfile --ignore-scripts --store-dir "$QOPENBB_TOOLS/protected-pnpm-store"
uv run --project pipeline --locked qopenbb-ci --version
uv run --project pipeline --locked qopenbb-ci --help
uv run --project pipeline --locked python --version
uv run --project pipeline --locked python -m pytest --version
uvx --from pytest==9.1.1 pytest --version
uv run --project .dagger --locked python -c 'import qopenbb, importlib.metadata as m; print(qopenbb.Qopenbb.__name__, m.version("dagger-io"))'
node --version
npm --version
pnpm --version
bun --version
dagger version
docker version --format '{{.Client.Version}} {{.Server.Version}}'
docker compose version --short
node verification/node_modules/@playwright/test/cli.js --version
node verification/node_modules/typescript/bin/tsc --version
```

Expected versions are Python 3.13.15, pytest 9.1.1, pytest-xdist 3.8.0, Dagger CLI/SDK 0.21.8, Playwright 1.64.0 and TypeScript 6.0.3, together with the host/runtime versions above. Python's `ast` parser follows CPython 3.13.15; the later JavaScript/TypeScript counter uses the TypeScript compiler AST. `uv sync --locked` and pnpm's `--frozen-lockfile` must fail on inconsistent project manifests and locks. Do not regenerate locks merely to make a verification run pass.

The portable `qopenbb-ci` entry point provides package identity and [evidence validation](evidence.md). Generation, publication and promotion commands remain pending. The `.dagger` package defines the image module type and imports the published stable SDK. Task 1.8 will add `dagger.json`, generated engine bindings, filtered source inputs and image exports. No Dagger build command is available at this checkpoint.

## Preserve the verification boundary

The base images in [tools.lock.json](../pipeline/tools.lock.json) use registry-returned manifest digests, recorded on 2026-10-16. These are future build inputs, not evidence that an application image builds or runs. Task 1.7 has accepted the pinned headless browser and fixture checks on WSL; follow [verification infrastructure](verification.md) for setup and evidence limits. Task 1.8 owns the first image export/load round trip; actual Compose lifecycle acceptance comes later.

The Python project defaults to serial pytest with an xdist ceiling of two. Use at most `-n 2 --maxprocesses=2` when isolated tests exist. Playwright starts at one worker when its runner is implemented. Only one heavy install, build or suite may run at a time. See the [testing policy](../.kiro/steering/testing.md) for state isolation and evidence requirements; installed packages alone do not satisfy requirement 10.4.

On 2026-10-16, protected frozen restoration succeeded in WSL with fresh Python caches and a fresh pnpm store: eight pipeline packages, 41 SDK packages and four verification packages. A protected uvx invocation also installed and ran pytest. An initial frozen Python restore correctly blocked pluggy 1.7.0 for package age; protected re-resolution selected pluggy 1.6.0 and platformdirs 4.13.0. No package-age bypass was used. This demonstrates this dependency setup; it does not demonstrate a clean CI runner, an application build or a browser journey.

Task-local setup and parser/import smoke output is retained in ignored `artifacts/task-1.2/smoke.json` and `protected-smoke.log`. The age-block evidence is in `blocked-young-pluggy.json`; initial missing-scaffold output is in `pre-setup.txt`. Lock hashes and provisional code measurements are in `lock-hashes.json` and `provisional-complexity.json`. Task 1.4 accepted the executable cross-language quality gate and retrospectively checked this foundation; use the current [complexity command](complexity.md) for subsequent changes. The production limits remain 400 physical lines per file, 300 logical units per Python/JavaScript/TypeScript file, and 50 per function.

Keep provider keys, `.env`, account state and browser traces out of setup output. This procedure needs no provider or registry publication credentials. Consult [contribution guidance](contributing.md) before adding application behavior.
