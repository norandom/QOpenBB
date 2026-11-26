# Verify the Workspace FCF yield journey

The isolated Linux check signs into the Full Workspace frontend, evaluates supplied FMP inputs through the session bridge, saves a dashboard and reopens it after both Workspace and modeling are recreated. A final login verifies that the direct provider widget still displays live data while modeling is stopped. The run creates a unique Docker Compose project, a disposable account, a private run directory and a fresh Playwright context per phase. The driver removes its containers, volumes and financial run state on exit.

Use the locked QOpenBB Python environment, the pinned Node and Bun versions, the installed verification Playwright package and its matching Chromium cache. The private repository-root `.env` supplies the provider service credential. The browser process receives only the disposable Workspace login. [Real inputs and reference](../financial-real-inputs/README.md).

Compile the reviewed Workspace source into an empty, user-owned directory. The build uses the Full runtime defaults and the bundle tag identifies the source revision.

```bash
export JOURNEY_ASSETS="$(mktemp -d)"
(
  cd vendor/workspace/terminalpro
  safe-chain bun install --frozen-lockfile
  set -a
  source ../lite/frontend.full.env
  set +a
  VITE_RELEASE_VERSION="$(git rev-parse --short HEAD)" VITE_TRADINGVIEW_ENABLED=false \
    NODE_OPTIONS=--max-old-space-size=8192 bun run build:runtime --outDir "$JOURNEY_ASSETS"
)
```

Pass the local content IDs of the Workspace and data API images under test. The test Compose file mounts the compiled SPA and changed bridge files into Workspace. The modeling process loads the maintained analytics source and locked Polars and PyJWT modules. This evidence covers the integrated source candidate. The release image milestone has its own build and verification gates.

```bash
export PLAYWRIGHT_BROWSERS_PATH="$HOME/.cache/ms-playwright"
mkdir -p artifacts/modeling-journey
pipeline/.venv/bin/python verification/modeling-journey/run.py \
  --workspace-image "$WORKSPACE_IMAGE" --data-image "$DATA_API_IMAGE" \
  --frontend "$JOURNEY_ASSETS" --evidence artifacts/modeling-journey
```

The generated evidence directory holds the three Playwright reports, dashboard/run checkpoint and before/after container IDs. The checked-in numerical fixtures and the saved-run widget work offline. The outage proof requires access to the FMP profile endpoint.

## Verify the commodities versus technology story

Run the preflight against a disposable Compose candidate built with Dagger and published only on a loopback port. The candidate needs the research story catalog, the authenticated modeling bridge and configured FMP and FRED entitlements. Set `STORY_ORIGIN` to the candidate's loopback HTTP origin with its explicit port. Pass the disposable login through `OPENBB_ADMIN_EMAIL` and `OPENBB_ADMIN_PASSWORD`.

```bash
STORY_ORIGIN=http://127.0.0.1:8601 \
STORY_EVIDENCE=artifacts/research-stories/story-preflight.json \
  python3 verification/modeling-journey/story_preflight.py
```

The preflight reopens each run through the bridge. It checks DBC/XLK, GLD/XLK and DBC/VGT over the 64 NYSE Arca sessions from August 17 to November 13, 2026. It recalculates percent price changes, sample annualized volatility from 63 adjacent returns and left-minus-right spreads in percentage points. The FMP rows represent split-adjusted USD closes with dividends excluded on a retrieved-history basis. The November 13 DFII10 context must carry a dated blocking check for the unavailable endpoint. The verified price spread still determines the verdict. [Source qualification](../../.kiro/specs/research-stories/source-qualification.md)

The JSON report links run IDs to calendar and source-row digests, receipts, output values, check results and reference fingerprints. A blocked input or verification mismatch exits nonzero and records the failure and prior completed checks. The report omits raw provider rows and login credentials. [Preflight acceptance criteria](../../.kiro/specs/research-stories/design.md#requirements-traceability-and-verification)
