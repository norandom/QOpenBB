# Install QOpenBB from prebuilt images

Run QOpenBB on Linux or in WSL using Docker Compose and the two prebuilt service images. The installation host does not need Node, Python, Dagger or application source builds.

**Release status: pending.** No accepted registry image pair or release manifest is published yet. This guide describes the intended installation using the current Compose configuration; the complete pull-and-start procedure still needs its release rehearsal. Follow [prototype delivery](prototype-delivery.md) for acceptance status. Do not substitute CI archive IDs or local image IDs for registry digests.

## What you need

- Docker Engine and the Docker Compose plugin on Linux, or Docker available inside WSL.
- Port 23003 available on the host.
- FMP and FRED API keys for the installed provider routes.
- A published QOpenBB release with its matching `compose.yaml`, `.env.sample` and two immutable image references.
- Registry pull access if the published packages are private. Package visibility is not yet finalized.

| Service | Release environment variable | Published reference |
| --- | --- | --- |
| Full Workspace, including its application backend | `WORKSPACE_IMAGE` | Pending publication |
| OpenBB data API | `DATA_API_IMAGE` | Pending publication |

Both references must come from the same accepted release. Their format is `registry/namespace/image@sha256:DIGEST`; the publisher supplies the real values. GHCR is the planned initial registry, but Compose accepts other registries.

## 1. Prepare the installation directory

Place the release's Compose file and public environment template in an empty directory, then run these commands there in a Linux/WSL shell:

```bash
mkdir -p data/workspace
if [ ! -e .env ]; then
  cp .env.sample .env
fi
chmod 600 .env
```

The current templates are [compose.yaml](../compose.yaml) and [.env.sample](../.env.sample). For installation, use the versions supplied with the accepted release rather than mixing a newer main-branch Compose file with older images.

Edit `.env` locally. Never commit or share the populated file.

| Setting | Value to supply |
| --- | --- |
| `WORKSPACE_IMAGE` | Workspace digest reference from the release manifest |
| `DATA_API_IMAGE` | Data API digest reference from the same manifest |
| `PUBLIC_URL` | `https://qbb.hanse-hedge.fund` for the intended deployment; `http://127.0.0.1:23003` for local-only testing |
| `FMP_API_KEY` | Your FMP key |
| `FRED_API_KEY` | Your FRED key |
| `OPENBB_ADMIN_EMAIL` | Optional initial administrator email |
| `OPENBB_ADMIN_PASSWORD` | Optional initial administrator password |

For a fresh install, set the administrator fields if you want explicit initial login credentials. Blank values preserve the image's generated or persisted bootstrap settings. Changing these fields is not a documented password-reset procedure for existing state.

AI, Excel and optional provider fields may remain blank. They are outside this two-service prototype. Provider keys configure access; they do not establish entitlement to every dataset.

## 2. Pull and start

If the release uses a private registry, authenticate with `docker login REGISTRY_HOST` using a credential with pull access before continuing. Do not put registry credentials in application environment variables.

```bash
docker compose config --quiet
docker compose pull
docker compose up -d --no-build
docker compose ps
```

`config --quiet` checks configuration without printing expanded keys. It does not verify image digests, provider entitlements or application behavior. Compose waits for data API readiness before starting Workspace; that readiness check does not call the providers.

Open your configured `PUBLIC_URL`. For a local-only install, this is <http://127.0.0.1:23003>. Log in using the initial administrator credentials and verify a supported dashboard/widget with data, not just the login page. The release must identify its supported catalog and known gaps.

If you left the administrator fields blank, retrieve the persisted bootstrap credentials in your private operator terminal:

```bash
docker compose exec workspace credentials
```

This command prints credentials. Do not capture its output in shared logs, screenshots or support reports.

If startup fails, inspect the services locally:

```bash
docker compose ps
docker compose logs --tail=100 workspace data-api
```

Review logs before sharing them; they can contain bootstrap credentials or private request details. A healthy data API alone does not establish that Workspace routing and widget data work.

## 3. Connect the existing Cloudflare tunnel

The origin listens on plain HTTP at `0.0.0.0:23003`. Configure your existing cloudflared to reach `http://127.0.0.1:23003` when it runs on the same host, or the reachable host address when it runs elsewhere. `0.0.0.0` is the bind address, not a tunnel destination.

Keep `PUBLIC_URL=https://qbb.hanse-hedge.fund` for this deployment. Cloudflare manages the public HTTPS/Access boundary. Compose does not install cloudflared or origin TLS. Workspace application login remains separate from Cloudflare Access. The data API has no published host port in this Compose file.

## State and updates

Workspace state is bind-mounted at `./data/workspace`, relative to the Compose directory. Keep that directory and `.env` when replacing containers. There are no Docker-managed data volumes. Jupyter is managed separately.

For a later accepted release, review its compatibility notes, keep a copy of the previous release configuration and protect existing state before migration. Update both image references and any matching Compose/template changes, preserving private settings, then run:

```bash
docker compose pull
docker compose up -d --no-build
docker compose ps
```

Repeat login and supported-widget checks. Backup/restore and rollback compatibility are not yet verified; changing back to older image references is not evidence that a migrated database can be rolled back. Dashboard persistence acceptance is tracked in the analyst-workspace spec.

To stop services without deleting bind-mounted state:

```bash
docker compose down
```

See the [roadmap](roadmap.md) for planned provider coverage, analyst workflows, AI and Excel.
