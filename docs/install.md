# Development install with prebuilt alpha images

Run QOpenBB on Linux or in WSL with Docker Compose. Use the prebuilt Workspace and data API alpha images; no application build tools are needed on the installation host.

The first registry image references are pending publication. They will be listed here when available. Build status is tracked in [prototype delivery](prototype-delivery.md).

## Requirements

- Docker with the Compose plugin.
- Port 23003 available.
- FMP and FRED API keys.
- The alpha's `compose.yaml`, `.env.sample` and matching image references.

| Service | Environment variable | Alpha image |
| --- | --- | --- |
| Workspace and application backend | `WORKSPACE_IMAGE` | Pending publication |
| OpenBB data API | `DATA_API_IMAGE` | Pending publication |

Use both images from the same alpha version. Published references use the form `registry/namespace/image@sha256:DIGEST`.

## Configure

Put [compose.yaml](../compose.yaml) and [.env.sample](../.env.sample) from the alpha version in your installation directory. Run these commands there in Linux or WSL:

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
| `WORKSPACE_IMAGE` | Published Workspace alpha reference |
| `DATA_API_IMAGE` | Matching data API alpha reference |
| `PUBLIC_URL` | `http://127.0.0.1:23003` |
| `FMP_API_KEY` | Your FMP key |
| `FRED_API_KEY` | Your FRED key |
| `OPENBB_ADMIN_EMAIL` | Optional initial administrator email |
| `OPENBB_ADMIN_PASSWORD` | Optional initial administrator password |

Keep `.env` private. AI, Excel and optional provider settings can stay blank. Provider subscriptions determine which datasets your keys can access.

## Pull and start

For private images, first authenticate with `docker login REGISTRY_HOST` using pull access.

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
