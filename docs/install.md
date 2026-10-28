# Development install with prebuilt alpha images

Run QOpenBB on Linux or in WSL with Docker Compose. Use the prebuilt Workspace and data API alpha images; no application build tools are needed on the installation host.

Development uses the moving `latest` tags below. Each published alpha also has a [tagged GitHub prerelease](https://github.com/norandom/QOpenBB/releases) with installation files and a manifest of exact image digests. Build and publication status are tracked in [GitHub Actions](https://github.com/norandom/QOpenBB/actions/workflows/prototype.yml).

## Requirements

- Docker with the Compose plugin.
- Port 23003 available.
- FMP and FRED API keys.
- The alpha's `compose.yaml`, `.env.sample` and matching image references.

| Service | Environment variable | Alpha image |
| --- | --- | --- |
| Workspace and application backend | `WORKSPACE_IMAGE` | `ghcr.io/norandom/qopenbb-workspace:latest` |
| OpenBB data API | `DATA_API_IMAGE` | `ghcr.io/norandom/qopenbb-data-api:latest` |

Pull both images together when updating development. Stable versions will use pinned references. For an exact alpha snapshot, use the digest pair in its release manifest.

Published [manifest image pair](https://github.com/norandom/QOpenBB/releases/download/alpha-40689838352-1/manifest.json) for `alpha-40689838352-1`:

| Service | Exact published reference |
| --- | --- |
| workspace | `ghcr.io/norandom/qopenbb-workspace@sha256:957f02d18b8365412e68016b1b9e7184a4383cec1fc35774fdc0193ab35d219f` |
| data-api | `ghcr.io/norandom/qopenbb-data-api@sha256:59b94139b34e2195e83d69be959c3f242fdf4ddccf5b2764c0d5154612aab057` |

Both CI jobs, public release-asset checks and six anonymous pulls by digest, release tag and `latest` pass. See the [publication review](../artifacts/reviewed/python-source-packaging/publication-review.md).

This alpha packages the backend with native locked uv, readable Python source under CPython and embedded Valkey 9.0.7. The [accepted local candidate](../artifacts/reviewed/python-source-packaging/runtime-review.md) passes the 36-chart gallery with save/fresh-login reopen and login/current-password checks with clean diagnostics. A separate synthetic Redis 7.0.15 snapshot/RQ job and database-marker probe passes recreation; the gallery browser journey itself did not test recreation. Publication checks identify the released images; browser acceptance has not been repeated on those CI image bytes. The disabled reset form's warnings retain source-test coverage, not browser acceptance. Earlier [login](../artifacts/reviewed/login-password/application-review.md), [historical gallery](../artifacts/reviewed/chart-gallery/publication-review.md) and [live-FMP onboarding](../artifacts/reviewed/prototype-onboarding/application-review.md) evidence remain historical; owner-server deployment remains open.

## Configure

Download [compose.yaml](https://github.com/norandom/QOpenBB/releases/download/alpha-40689838352-1/compose.yaml) and the [environment template](https://github.com/norandom/QOpenBB/releases/download/alpha-40689838352-1/default.env.sample) from the [alpha release](https://github.com/norandom/QOpenBB/releases/tag/alpha-40689838352-1). Save the template as `.env.sample` in the same directory as Compose. Run these commands there in Linux or WSL:

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

### Update the bootstrap administrator password

Keep `OPENBB_ADMIN_EMAIL` unchanged and set a nonempty `OPENBB_ADMIN_PASSWORD` in `.env`. Recreate only Workspace so it receives the updated environment:

```bash
docker compose up -d --no-deps --force-recreate workspace
```

Wait for startup to finish, then log in with that email and the new password. A plain `docker compose restart` does not load changed `.env` values. Keep `./data/workspace`; no database deletion or dashboard reset is needed.

Disposable Compose acceptance confirmed the same administrator UUID and synthetic dashboard database content survive this update: the new credential succeeds and the old one fails. This verifies retained database state; it does not establish dashboard UI save/reopen or the owner's deployment.

To open the supported starter app after login:

1. Open **Connections**, for example <http://127.0.0.1:23003/app/connections>.
2. Select **Connect Backend**.
3. Enter a connection name such as `QOpenBB data API`. Set **URL** to your current Workspace origin followed by `/data`, for example `http://127.0.0.1:23003/data`.
4. Select **Test**, then **add** after the catalog test succeeds.
5. Open **Apps**, then the **QOpenBB starter** card. Its saved parameters select AAPL company profile and annual income data, plus the GDP series from FRED.

Connect from the Connections page before opening a dashboard. Adding a generic widget to an existing dashboard leaves its required symbol empty and currently produces validation errors; the required-symbol guard remains open. Set the required parameters before expecting generic-widget data. The starter supplies AAPL/GDP parameters; the accepted financial comparison covers annual AAPL income, not every provider/widget. Provider entitlement still determines which data can load.

For startup diagnostics:

```bash
docker compose logs --tail=100 workspace data-api
```

Review logs before sharing them for private information. The data API health check checks configuration and installed routes, not live provider access.

## State and updates

Workspace state is stored in `./data/workspace`. Keep that directory and `.env` when replacing containers. The application listens on HTTP port 23003 on all host interfaces; the data API has no published host port.

To update, use the next alpha's matching Compose configuration and both image references, preserving your private settings. Review migration notes and protect existing state before updating.

```bash
docker compose pull
docker compose up -d --no-build
```

Alpha backup/restore and rollback compatibility are not yet verified. To stop containers while keeping the bind-mounted state:

```bash
docker compose down
```

Optional remote access is covered in [Tips and Tricks](tips-and-tricks.md). See the [roadmap](roadmap.md) for planned features.
