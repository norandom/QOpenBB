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

Verified public image pair for `alpha-40002594897-1`:

| Service | Exact published reference |
| --- | --- |
| workspace | `ghcr.io/norandom/qopenbb-workspace@sha256:6ea21dfb5ae3956e65f85b10728c3551ecb775ca5591efbae2226260ee32078d` |
| data-api | `ghcr.io/norandom/qopenbb-data-api@sha256:29509b63af9bfef8e8449276ae342bd0e0ec7e964dc6e0419036d8387b5454a7` |

Both services passed anonymous pulls by digest, release tag and `latest`. See [release verification](../artifacts/reviewed/chart-waterfall/verification.md#published-waterfall-alpha).

## Configure

Download [compose.yaml](https://github.com/norandom/QOpenBB/releases/download/alpha-40002594897-1/compose.yaml) and the [environment template](https://github.com/norandom/QOpenBB/releases/download/alpha-40002594897-1/default.env.sample) from the [alpha release](https://github.com/norandom/QOpenBB/releases/tag/alpha-40002594897-1). Save the template as `.env.sample` in the same directory as Compose. Run these commands there in Linux or WSL:

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

Open a supported widget and load data. For startup diagnostics:

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
