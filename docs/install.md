# Development install with prebuilt alpha images

Run QOpenBB on Linux or in WSL with Docker Compose. Use the prebuilt Workspace and data API alpha images; no application build tools are needed on the installation host.

Development uses the moving `latest` tags below. Each published alpha also has a [tagged GitHub prerelease](https://github.com/norandom/QOpenBB/releases) with installation files and a manifest of exact image digests. Build and publication status are tracked in [GitHub Actions](https://github.com/norandom/QOpenBB/actions/workflows/prototype.yml).

## Requirements

- Linux or WSL on x86-64; the alpha images target `linux/amd64`.
- Docker with the Compose plugin.
- Port 23003 available.
- FMP and FRED API keys.
- The alpha's `compose.yaml`, `.env.sample` and matching image references.

| Service | Environment variable | Alpha image |
| --- | --- | --- |
| Workspace and application backend | `WORKSPACE_IMAGE` | `ghcr.io/norandom/qopenbb-workspace:latest` |
| OpenBB data API | `DATA_API_IMAGE` | `ghcr.io/norandom/qopenbb-data-api:latest` |

Pull both images together when updating development. Stable versions will use pinned references. For an exact alpha snapshot, use the digest pair in its release manifest.

Published [manifest image pair](https://github.com/norandom/QOpenBB/releases/download/alpha-41030227140-1/manifest.json) for `alpha-41030227140-1`:

| Service | Exact published reference |
| --- | --- |
| workspace | `ghcr.io/norandom/qopenbb-workspace@sha256:b40a2472b3a5f6ca325aa126b7a2131aa517dc1a622f4f1a3a7cae24f105f269` |
| data-api | `ghcr.io/norandom/qopenbb-data-api@sha256:743b9fd657e8e2e8346a42fb8b3f8146b49ebf134987ffcd6363c879ffc5e6d1` |

Both CI jobs, three public release-asset checks and six anonymous pulls by digest, release tag and `latest` pass. See the [publication review](../artifacts/reviewed/financial-input-milestone/review.md).

This alpha packages native locked uv, readable Python source under CPython and embedded Valkey 9.0.7. It adds ten FMP financial-input adapters and the generic FRED series contract, served through eleven reusable native widget definitions. [Live provider acceptance](../artifacts/reviewed/market-live-financial-inputs/accepted.md) and the [local packaged Income journey](../artifacts/reviewed/market-packaged-financial/accepted.md) cover the recorded data and user flows. The published data image separately passes installed catalog/source checks without provider calls. CI Workspace image bytes have not repeated browser acceptance, and the owner's deployment is separate.

The earlier [Python-source/Valkey acceptance](../artifacts/reviewed/python-source-packaging/runtime-review.md), [login repair](../artifacts/reviewed/login-password/application-review.md) and [historical chart gallery](../artifacts/reviewed/chart-gallery/publication-review.md) remain scoped historical evidence. Backup/restore and rollback remain unverified.

## Configure

Download [compose.yaml](https://github.com/norandom/QOpenBB/releases/download/alpha-41030227140-1/compose.yaml) and the [environment template](https://github.com/norandom/QOpenBB/releases/download/alpha-41030227140-1/default.env.sample) from the [alpha release](https://github.com/norandom/QOpenBB/releases/tag/alpha-41030227140-1). Save the template as `.env.sample` in the same directory as Compose. Run these commands there in Linux or WSL:

```bash
mkdir -p data/workspace
if [ ! -e .env ]; then
  cp .env.sample .env
fi
chmod 600 .env
```

Edit `.env`:

| Setting | Value |
| --- | --- |
| `WORKSPACE_IMAGE` | `ghcr.io/norandom/qopenbb-workspace:latest` |
| `DATA_API_IMAGE` | `ghcr.io/norandom/qopenbb-data-api:latest` |
| `PUBLIC_URL` | The browser-facing origin: `http://127.0.0.1:23003` locally, or your HTTPS domain behind a proxy |
| `FMP_API_KEY` | Your FMP key |
| `FRED_API_KEY` | Your FRED key |
| `OPENBB_ADMIN_EMAIL` | Optional bootstrap administrator email |
| `OPENBB_ADMIN_PASSWORD` | Optional bootstrap password; choose a strong, unique value |

Keep `.env` private. AI, Excel and optional provider settings can stay blank. Provider subscriptions determine which datasets your keys can access.

Use your own password or leave the administrator fields blank to generate credentials on first start. Single-quote a password value in `.env` if it contains `$`, so Compose does not interpolate it. Avoid exporting the same variables in your shell: exported values take precedence over `.env`.

Login checks an existing nonempty password unchanged against the stored credential; it does not apply new-password strength rules. Password creation, reset and replacement retain the strength policy: at least eight characters with uppercase, lowercase, a digit and a special character such as `!`, with no whitespace.

## Pull and start

The alpha images are public. No registry login is required.

```bash
docker compose config --quiet
docker compose pull
docker compose up -d --no-build
docker compose ps
```

Open <http://127.0.0.1:23003> and log in. If you left the administrator fields blank, display the generated credentials in your private terminal:

```bash
docker compose exec workspace credentials
```

Do not share that output. Blank administrator settings reuse persisted bootstrap credentials. Nonempty settings override them at container startup; the initializer creates the configured administrator or updates that account's password.

## First login and onboarding

A fresh account starts without a connected data backend or populated dashboard. The images include the components, but this alpha does not automatically register the bundled backend or instantiate its app templates. Complete this setup once for each Workspace account. The connection and saved dashboards belong to that account and are stored in the bind-mounted Workspace data described under [persistence and updates](#persistence-and-updates).

### Connect the bundled data backend

1. Open **Connections**, for example <http://127.0.0.1:23003/app/connections>.
2. Select **Connect Backend**.
3. Enter a connection name such as `QOpenBB data API`. Set **URL** to your current Workspace origin followed by `/data`, for example `http://127.0.0.1:23003/data`.
4. Select **Test**, then **add** after the catalog test succeeds.
5. Open **Apps** to see the connected backend's templates. The widget library also exposes its eleven native data definitions and the historical gallery widgets.

Use the origin you actually opened in your browser. For a proxied deployment, append `/data` to that public origin rather than using the example's loopback address. The data API uses the provider keys already supplied through `.env`.

### Open a populated example

| App | What it opens |
| --- | --- |
| **QOpenBB starter** | Live AAPL company profile and annual income, plus FRED GDP observations |
| **QOpenBB Historical Chart Gallery - January 2025** | The populated 36-chart showcase using fixed historical FMP observations |

Select an app card to open its dashboard. The starter demonstrates working components; it is not yet the curated investment-research dashboard planned in the [analyst workstream](../.kiro/specs/analyst-workspace/investment-analysis-contract.md).

### Choose companies and economic series

The example parameters are defaults, not the scope of the providers:

| Widget | Parameter | Example values |
| --- | --- | --- |
| Company Profile | **Symbol** | `AAPL`, `MSFT`, `GOOGL`, subject to FMP listing coverage and your entitlement |
| Income | **Symbol**, **Period** | `AAPL` or `MSFT`; `annual` or `quarter` |
| FRED Series | **Symbol**, date range and frequency controls | `GDP` or `DGS10`; enter the FRED series identifier in the field labelled Symbol |

For another component, use **Add widgets**, choose its definition and fill the required fields. An empty required Symbol produces a validation error until supplied. The current company Symbol input is plain text; company-name autocomplete is not connected yet. FRED observations retain the selected series' units and frequency conventions; they are not limited to GDP.

Save the dashboard with **Ctrl+Shift+S**, then reopen it to confirm the selected parameters. The [accepted Income journey](../artifacts/reviewed/market-packaged-financial/accepted.md) covers AAPL/MSFT, annual/quarterly periods, visible values, error recovery and save/reopen in a fresh browser context. It does not certify every provider/widget or full research-context reopening after container recreation. Provider entitlement still determines which live data can load.

Return to your saved instance through **My Dashboards** or its saved URL. Selecting the template in **Apps** again can create another copy; packaged templates and your saved dashboard instances are separate.

### Check startup problems

For startup diagnostics:

```bash
docker compose logs --tail=100 workspace data-api
```

Review logs before sharing them for private information. The data API health check checks configuration and installed routes, not live provider access.

## Persistence and updates

The supplied Compose file bind-mounts `./data/workspace` on the host to `/data` in Workspace. It uses no Docker-managed data volume. Keep the same deployment directory and account when updating.

| Keep on the host | Purpose |
| --- | --- |
| `data/workspace/` | Workspace database, account connections, saved dashboards/parameters and generated bootstrap credentials |
| `.env` | Private provider keys, public origin, administrator overrides and image settings |
| `compose.yaml` | Service configuration and the relative data bind mount |

Pulling images, restarting or recreating containers, and `docker compose down` retain that host directory. Deleting/replacing it or resolving the relative bind mount to a different directory gives Workspace fresh state. A different account also has its own connections and dashboards. If an update appears empty, check the account and resolved bind path before redoing onboarding.

The data API has no host data mount; transient provider caches are not a durable market-data store. The historical gallery's fixed data is packaged in the image. Keeping Workspace state does not freeze live provider responses.

The application listens on HTTP port 23003 on all host interfaces; the data API has no published host port.

To update, use the next alpha's matching Compose configuration and both image references, preserving your private settings. Review migration notes and protect existing state before updating.

```bash
docker compose pull
docker compose up -d --no-build
```

### Update the bootstrap administrator password

Keep `OPENBB_ADMIN_EMAIL` unchanged and set a nonempty `OPENBB_ADMIN_PASSWORD` in `.env`. Recreate only Workspace so it receives the updated environment:

```bash
docker compose up -d --no-deps --force-recreate workspace
```

Wait for startup to finish, then log in with that email and the new password. A plain `docker compose restart` does not load changed `.env` values. Keep `./data/workspace`; no database deletion or dashboard reset is needed.

Disposable Compose acceptance confirmed the same administrator UUID and synthetic dashboard database content survive this update: the new credential succeeds and the old one fails. This verifies retained database state; full analyst dashboard UI reopening after container recreation remains separate acceptance.

Alpha backup/restore and rollback compatibility are not yet verified. To stop containers while keeping the bind-mounted state:

```bash
docker compose down
```

Optional remote access is covered in [Tips and Tricks](tips-and-tricks.md). See the [roadmap](roadmap.md) for planned features.
