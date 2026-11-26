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

Select the story suite after Dagger builds and loads the three local candidate images. Set the image variables to the full local content IDs and use the private environment file for FMP and FRED.

```bash
export PLAYWRIGHT_BROWSERS_PATH="$HOME/.cache/ms-playwright"
mkdir -p artifacts/modeling-journey
pipeline/.venv/bin/python verification/modeling-journey/packaged.py \
  --suite story --local-images --workspace-image "$WORKSPACE_IMAGE" \
  --data-image "$DATA_IMAGE" --modeling-image "$MODELING_IMAGE" \
  --evidence artifacts/modeling-journey
```

The story smoke checks the packaged app catalog and opens its default DBC/XLK selection while modeling is stopped. It starts the same modeling container, retries the comparison on the open dashboard and checks that the verified spread reaches the verdict. The runner records container identities and Playwright evidence under the run directory. Omit `--local-images` to use immutable registry references. The issuer suite remains the default.

Use `--suite story-selection` with the same images and an ignored evidence directory for the financial evidence journey. On Ubuntu, one headless Chromium worker changes the proxy roles and date by keyboard. The journey compares the charts and dated drill-downs with the immutable runs read back through the authenticated bridge. It checks the January 13 short window and recovery, both Workspace themes, the spread verdict, and the November 13 DFII10 withholding. If the saved FRED run has eligible endpoint observations, it checks the endpoint chart and its dated rows.

The browser writes a credential-free `story-selection.json` summary and representative FMP price and risk chart PNGs inside its run directory. The summary contains run IDs, counts, dates, value spreads and hashes. Screenshots contain only chart figures. The verdict and source checks use real provider acquisitions from the candidate.

Run the preflight against a disposable Compose candidate built with Dagger and published only on a loopback port. The candidate needs the research story catalog, the authenticated modeling bridge and configured FMP and FRED entitlements. Set `STORY_ORIGIN` to the candidate's loopback HTTP origin with its explicit port. Pass the disposable login through `OPENBB_ADMIN_EMAIL` and `OPENBB_ADMIN_PASSWORD`.

```bash
STORY_ORIGIN=http://127.0.0.1:8601 \
STORY_EVIDENCE=artifacts/research-stories/story-preflight.json \
  python3 verification/modeling-journey/story_preflight.py
```

The preflight reopens each run through the bridge. It checks DBC/XLK, GLD/XLK and DBC/VGT over the 64 NYSE Arca sessions from August 17 to November 13, 2026. It recalculates percent price changes, sample annualized volatility from 63 adjacent returns and left-minus-right spreads in percentage points. The FMP rows represent split-adjusted USD closes with dividends excluded on a retrieved-history basis. The November 13 DFII10 context must carry a dated blocking check for the unavailable endpoint. The verified price spread still determines the verdict. [Source qualification](../../.kiro/specs/research-stories/source-qualification.md)

The JSON report links run IDs to calendar and source-row digests, receipts, output values, check results and reference fingerprints. A blocked input or verification mismatch exits nonzero and records the failure and prior completed checks. The report omits raw provider rows and login credentials. [Preflight acceptance criteria](../../.kiro/specs/research-stories/design.md#requirements-traceability-and-verification)

Use `--suite story-persistence` with the same image arguments to verify saved stories. The runner provisions two ordinary users inside the disposable Workspace and starts one fresh authenticated Chromium process per phase. The owner saves a real DBC/XLK comparison, changes the input and result chart types and series, and downloads the App through the dashboard menu. The check compares the complete exported document with the allowlisted story configuration.

For the controlled revision, a temporary data API fixture replaces the provider service on the disposable network. It serves the original 128 dated closes with one dollar added to the ending DBC close. The second analyst evaluates the same acquisition through the authenticated bridge and checks the updated rows and verified spread. The runner then restores the original data API container. Fresh reopen reads both original immutable runs, compares their full hashes and checks the displayed price, volatility, DFII10 and chart settings. A final login checks an actual other-owner comparison and a deleted macro run. Each phase records its browser evaluation count. The private checkpoint labels the real acquisitions and the controlled cases separately.
