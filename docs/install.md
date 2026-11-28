# Install QOpenBB with Docker Compose

## Automated full installation

Use the [platform commands in the README](../README.md#start-with-docker-compose) from a repository checkout or an extracted ZIP. The full installer starts Workspace, the data API and the modeling service. Windows uses Docker Desktop in Linux-container mode. PowerShell accepts the `.ps1` launcher as a script file. Run it from the full checkout or extracted repository. If Windows marks the downloaded ZIP as coming from the Internet, review the download and use **Properties → Unblock** on the ZIP before extracting, or use a Git checkout.

Setup reads your existing `.env` without changing its contents or permissions. It creates the file if absent and stores generated settings and prompted keys in a separate private `.env.setup`. You can set `FMP_API_KEY` and `FRED_API_KEY` there before setup, supply them through the process environment, or enter them at the prompts. Setup provisions the initial account with the available data apps, the historical chart gallery and a saved model output dashboard. Each account owns its dashboards and saved model runs. The modeling dashboard requires a run and output you own.

| Setting | Full installer behavior |
| --- | --- |
| `WORKSPACE_IMAGE`, `DATA_API_IMAGE` | Pull the Compose defaults tagged `latest`, or use your configured references. |
| `MODELING_IMAGE` | Use your selected image. Setup derives the default from the checkout's modeling package version each time it runs. An explicit reference takes precedence. |
| `WORKSPACE_HOST_PORT`, `PUBLIC_URL`, `WORKSPACE_BIND_IP` | A new installation uses loopback and port 23003. For remote access set the browser origin and binding before setup. [Remote access](tips-and-tricks.md) |
| `OPENBB_ADMIN_EMAIL`, `OPENBB_ADMIN_PASSWORD` | Set these before setup to choose the bootstrap login. Leaving them blank uses the generated or persisted credentials. |

Use the URL printed by setup. Initial login details are shown on a private interactive terminal. For unattended installations, retrieve them locally with `docker compose --env-file .env.setup --env-file .env --env-file deploy/setup/defaults.env exec workspace credentials`. Use your configured browser URL if the credentials command also lists a container address.

### Update or stop a full installation

Rerun the installer in the same checkout and Compose project. Ask users to save their work and close Workspace during setup. Provisioning a new catalog signs in as the bootstrap administrator and can expire that account’s earlier browser session. Existing dashboards keep their edits. Keep `.env`, `.env.setup`, `data/workspace/` and the modeling storage. Linux stores model runs in `data/modeling/` with owner 10001 and mode 0700. On Windows, a fresh installation uses the Compose project's `model-runs` Docker volume so saved runs have Linux ownership and permissions. Preserve that volume when updating Docker Desktop. An existing model bind directory must retain its Linux ownership and permissions. Workspace stores its data in `data/workspace/` on both platforms.

To inspect all three services or stop them while retaining data, run these commands in the installation directory:

```sh
docker compose --env-file .env.setup --env-file .env --env-file deploy/setup/defaults.env -f compose.yaml -f deploy/setup/compose.full.yaml ps
docker compose --env-file .env.setup --env-file .env --env-file deploy/setup/defaults.env -f compose.yaml -f deploy/setup/compose.full.yaml down
```

A successful install verifies service readiness and provisions dashboards. Provider credentials and entitlements determine which observations load. If a chart stays empty, check its symbol, date window and provider access. [Provider coverage](provider-coverage.md)

## Manual two-service installation

Use this alternative to run only Workspace and the data API. Accounts using this route require the manual connection and dashboard steps below.

Development uses the moving `latest` tags below. Each published alpha also has a [tagged GitHub prerelease](https://github.com/norandom/QOpenBB/releases) with installation files and a manifest of exact image digests. Build and publication status are tracked in [GitHub Actions](https://github.com/norandom/QOpenBB/actions/workflows/prototype.yml).

## Requirements

- Linux or WSL on x86-64; the alpha images target `linux/amd64`.
- Docker with the Compose plugin.
- Port 23003 available.
- FMP and FRED API keys.
- The alpha's `compose.yaml`, public `default.env.sample` asset and matching image references. Save the downloaded environment template locally as `.env.sample` before the commands below.

| Service | Environment variable | Alpha image |
| --- | --- | --- |
| Workspace and application backend | `WORKSPACE_IMAGE` | `ghcr.io/norandom/qopenbb-workspace:latest` |
| OpenBB data API | `DATA_API_IMAGE` | `ghcr.io/norandom/qopenbb-data-api:latest` |

Pull both images together when updating development. Stable versions will use pinned references. For an exact alpha snapshot, use the digest pair in its release manifest.

To reproduce a particular alpha, open the release's `manifest.json` and copy the two `images.*.reference` values into `WORKSPACE_IMAGE` and `DATA_API_IMAGE` in your private `.env`. [Published releases and manifests](https://github.com/norandom/QOpenBB/releases)

## Configure

Use the repository's [compose.yaml](../compose.yaml) and [.env.sample](../.env.sample), or download both files from the same alpha release and save its `default.env.sample` as `.env.sample`. Run these commands there in Linux or WSL:

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

On a manual two-service install, a fresh account starts without a connected data backend or populated dashboard. The images include the components, but this alpha does not automatically register the bundled backend or instantiate its app templates. Complete this setup once for each Workspace account. The connection and saved dashboards belong to that account and are stored in the bind-mounted Workspace data described under [persistence and updates](#persistence-and-updates).

### Connect the bundled data backend

1. Open **Connections**, for example <http://127.0.0.1:23003/app/connections>.
2. Select **Connect Backend**.
3. Enter a connection name such as `QOpenBB data API`. Set **URL** to your current Workspace origin followed by `/data`, for example `http://127.0.0.1:23003/data`.
4. Select **Test**, then **add** after the catalog test succeeds.
5. Open **Apps** to see the connected backend's templates. The widget library also exposes the connected financial datasets and historical gallery widgets. Eligible FMP widgets support [selection by company name or symbol](company-selection.md).

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

For another component, use **Add widgets**, choose its definition and fill the required fields. Eight immediate FMP widgets offer [Company name autocomplete alongside Symbol](company-selection.md); selecting a listing keeps both fields linked. FRED still uses its own series identifier. Its observations retain the selected series' units and frequency conventions; they are not limited to GDP. The generic-widget empty-required-symbol guard remains a separately tracked gap.

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
