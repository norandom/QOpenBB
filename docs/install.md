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

Published manifest image pair for `alpha-40467871625-1`:

| Service | Exact published reference |
| --- | --- |
| workspace | `ghcr.io/norandom/qopenbb-workspace@sha256:4754c820716672edcdc5e0fde252a90a4801e3d5d17be78772766ca6bc80d31a` |
| data-api | `ghcr.io/norandom/qopenbb-data-api@sha256:131eeb9dadfbe3b429845ddb07266fc81cc70b03e5bd558da6fb628e5f8f1162` |

Both CI jobs, public release-asset checks and six anonymous pulls by digest, release tag and `latest` pass. See [delivery status](prototype-delivery.md#current-prototype-repair).

This alpha includes the reviewed first-login nullable-response fix, the existing widget/app catalog's packaging and GET routes, Workspace's fallback for external app previews, and an empty agent-discovery response for the data-only backend. Its published-image Compose journey and isolated pull-only local installation rehearsal are independently accepted. Acceptance covers fresh onboarding, later login, the starter's live annual AAPL income values and refresh, with clean diagnostics. See the [application review](../artifacts/reviewed/prototype-onboarding/application-review.md) and [recorded result](../artifacts/reviewed/prototype-onboarding/application.json). Owner-server deployment, broader provider acceptance and AI remain separate.

## Configure

Download [compose.yaml](https://github.com/norandom/QOpenBB/releases/download/alpha-40467871625-1/compose.yaml) and the [environment template](https://github.com/norandom/QOpenBB/releases/download/alpha-40467871625-1/default.env.sample) from the [alpha release](https://github.com/norandom/QOpenBB/releases/tag/alpha-40467871625-1). Save the template as `.env.sample` in the same directory as Compose. Run these commands there in Linux or WSL:

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
| `PUBLIC_URL` | `http://127.0.0.1:23003` |
| `FMP_API_KEY` | Your FMP key |
| `FRED_API_KEY` | Your FRED key |
| `OPENBB_ADMIN_EMAIL` | Optional initial administrator email |
| `OPENBB_ADMIN_PASSWORD` | Optional initial administrator password |

Keep `.env` private. AI, Excel and optional provider settings can stay blank. Provider subscriptions determine which datasets your keys can access.

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

Do not share that output. Existing state preserves its administrator settings; changing `.env` is not a password-reset procedure.

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
