# OpenBB self service: baseline research

Research date: 2026-10-16. Status: requirements-phase research and deployment proposal, not an approved implementation design.

## Confirmed direction

Develop on Windows/WSL Docker; deploy to a private Linux server. Establish the upstream environment as-is first. Defer the owner's PostgreSQL data integration. Avoid splitting the bundled application into new microservices in the baseline.

## Verified upstream facts

The [Workspace repository](https://github.com/OpenBB-finance/workspace) is public, archived, and contains terminalpro, backend-api, lite, and excel-add-in. The inspected main revision is `be00e95019a55d57af146919ee46b7e1a4859226`. Its root license is Apache-2.0; component notices must also be preserved. Archival is verified; a broader claim about the company's legal status is not needed for this spec.

The [Lite packaging](https://github.com/OpenBB-finance/workspace/blob/be00e95019a55d57af146919ee46b7e1a4859226/lite/README.md) already combines Workspace, its application backend, SQLite, Redis, and nginx. Persistent application state lives under `/data`. This is the lowest-change baseline. Its published quickstart names `openbb/lite:latest`; availability and a digest have not been verified here. Do not treat that mutable tag as a reproducibility pin. Some frontend settings are locked at build time.

The [data-platform repository](https://github.com/openbq-org/OpenBB) is separate and open source; the former OpenBB-finance/OpenBB URL redirects there. Its license must be inspected independently when pinning a release. The [OpenBB API launcher](https://docs.openbb.co/odp/python/extensions/interface/openbb-api) serves installed data extensions and Workspace metadata. Thus two different backends are needed: application state/authentication, and financial data.

The data API has [v4](https://docs.openbb.co/odp/v4/python/quickstart/workspace) and [v5](https://docs.openbb.co/odp/python/quickstart/workspace) documentation. Do not install unbounded latest dependencies and assume archived Excel functions match. Select the version only after comparing the add-in's generated OpenAPI snapshot, widget metadata, function signatures, and auth contracts. FMP credentials are supplied server-side; [credential documentation](https://docs.openbb.co/odp/python/user-guide/credentials) describes `FMP_API_KEY` and precedence. Verify these settings against the selected version.

The released [Excel auth source](https://github.com/OpenBB-finance/workspace/blob/be00e95019a55d57af146919ee46b7e1a4859226/excel-add-in/src/backend/auth.api.ts) calls `/pro/login`, `/pro/validate`, `/pro/logout`, and `/pro/user`. Its [data fetcher](https://github.com/OpenBB-finance/workspace/blob/be00e95019a55d57af146919ee46b7e1a4859226/excel-add-in/src/functions/fetcher/platform.api.ts) sends the user's Workspace bearer token to the configured platform URL. The standalone API's [documented authentication](https://docs.openbb.co/odp/python/quickstart/rest_api) is not proof that it accepts this token. This is an integration spike, not a solved configuration detail.

The [Excel environment example](https://github.com/OpenBB-finance/workspace/blob/be00e95019a55d57af146919ee46b7e1a4859226/excel-add-in/.env.example) separates backend, platform, and add-in URLs. The [Vite config](https://github.com/OpenBB-finance/workspace/blob/be00e95019a55d57af146919ee46b7e1a4859226/excel-add-in/vite.config.ts) uses `ADDIN_BASE_URL` while building the manifest and changes the function namespace for localhost builds. Preserve that distinction when validating workbooks. The package references `@openbb/ui`; public package availability and clean installation remain unverified.

## Proposed single-Compose organization

Primary user journey: add ready-made FMP-backed widgets, arrange/resize them, save a dashboard, reopen it, and refresh its data. The [OpenBB connector documentation](https://docs.openbb.co/odp/v4/python/quickstart/workspace) says installed endpoints become available as widgets through the data API. The v5 launcher similarly generates widgets.json. This is our self-hosted API, not OpenBB's hosted data service. The frontend's [widget search](https://github.com/OpenBB-finance/workspace/blob/be00e95019a55d57af146919ee46b7e1a4859226/terminalpro/src/components/LayoutAuth/Search/hooks/useFilterWidgets.ts) includes external-connector widgets; "external" here means outside the application backend, including our other Docker service.

Distinguish endpoint-generated widgets from the historical curated/premium data catalog. Lite locks packageDataEnabled off; Full enables that flag by default. Neither flag proves that historical catalog endpoints work against the self-hosted API. Verify the first dashboard using API-discovered widgets and actual FMP entitlements. Do not promise the whole historical catalog or premade dashboards without checking their routes and dependencies.

| Service | Baseline responsibility | State | Initial treatment |
| --- | --- | --- | --- |
| workspace | Upstream Lite: frontend + application API + bundled SQLite/Redis | `/data` named volume | Required; retain packaging |
| data-api | Pinned OpenBB API + compatible FMP provider | configuration, no custom DB | Required; small reproducible image to build |
| excel | Serve upstream add-in build and manifest | generated assets in image | Excel profile; build/auth verification required |
| jupyter | Authenticated JupyterLab client of data-api | notebook volume | Optional notebooks profile |
| TLS ingress | Trusted client-facing HTTPS, private reachability | certificates/configuration | Reuse server ingress if available; establish during design |

`compose.proposed.yaml` captures the service arrangement. It is deliberately not a root deployment file. Data API, Excel, and notebook images are explicit required inputs, not fictitious upstream image names. The file has no build recipes and must not be described as a working deployment. Image names in `compose.validation.env` are syntax-check fixtures only.

An initial local Workspace-only experiment can use the documented Lite image, but that does not prove the data API or Excel integration works. The selected baseline should ultimately build Lite from the pinned monorepo and record image digests for deployment. The [Lite Dockerfile](https://github.com/OpenBB-finance/workspace/blob/be00e95019a55d57af146919ee46b7e1a4859226/lite/Dockerfile) expects an assembled build context: Lite files plus `backend/` from `backend-api/backend/` and `terminalpro/`. Do not assume the monorepo root is already that context. Its build also contains dependency-resolution steps that need checking for reproducibility.

## Development and deployment workflow proposal

1. Keep this repository as the controlling setup, specs, configuration templates, and verification scripts. Acquire the upstream source at the recorded revision in a separate checkout, preserving notices. Keep adaptations as reviewable commits or patches.
2. Place the working clone in WSL's Linux filesystem for source builds; use Windows Excel as the external client. Verify that Windows can reach the chosen WSL/Docker addresses. Do not place Docker DNS names in browser or Office configuration.
3. Establish Lite login, dashboard persistence, and backup/restore before changing upstream behavior.
4. Build the pinned data API/provider environment and prove an FMP request. Register its client-reachable URL in Workspace; verify widget discovery and one returned dataset.
5. Build the released Excel add-in. Set `VITE_ENV=ONPREM`, the application backend URL, platform URL, `VITE_ADDIN_BASE_URL`, and `ADDIN_BASE_URL`. These are public configuration values, never FMP secrets. Validate generated manifest URLs and namespace. Test login, a function, refresh, and workbook reopen in Windows Excel.
6. If Excel fails, capture the exact contract failure. Evaluate compatible API versions and make the small Excel compatibility changes explicitly allowed by the owner. Keep URLs, auth, manifest, and response handling changes reviewable and preserve function signatures. Do not disable authentication merely to make a smoke test pass.
7. Add Jupyter as an optional client of the same API. A notebook kernel runs inside Docker and uses `http://data-api:6900`; the user's browser uses the external notebook HTTPS address. Persist work under `/home/jovyan/work`. Use a scoped service credential once the API auth contract is established. Do not give notebooks direct access to Workspace's database or Docker socket.
8. Build/check/publish with Dagger in GitHub Actions. Propose GHCR under `ghcr.io/norandom/` for the image registry. Record the complete release image set by immutable digest. The private Linux server uses `docker compose pull` and `docker compose up -d --no-build`; it does not clone or compile the application. Reuse the same Compose definition and use profiles for optional services. Do not copy development secrets or data by accident.

For source development, use each component's upstream development command when appropriate; the first milestone is a reproducible rebuild, not mandatory hot reload for every service. A later dev profile can add source mounts without changing the baseline's production behavior.

## Addressing, authentication, and persistence

- Proposed client addresses: `https://workspace.<private-domain>`, `https://data.<private-domain>`, `https://excel.<private-domain>`, and optionally `https://notebooks.<private-domain>`. They are examples, not configured DNS names.
- The baseline Compose proposal binds ports to loopback. On a Linux server, host ingress can proxy them. A containerized ingress needs shared Docker networking instead of localhost. Do not change bindings to all interfaces as a substitute for private access controls.
- Excel requires trusted HTTPS assets and a suitable sideload/install mechanism. [Microsoft's Windows sideload guidance](https://learn.microsoft.com/en-us/office/dev/add-ins/testing/create-a-network-shared-folder-catalog-for-task-pane-and-content-add-ins) is a starting point; exact Excel edition and organizational policy remain installation inputs. Do not assume a taskpane opening proves custom functions are supported.
- Workspace login does not automatically protect the separate data API. Validate auth, CORS origins, forwarded headers, token handling, and Office requests separately. An interactive ingress login page may not work for Excel custom-function requests.
- Back up the entire Workspace state, including its encryption/authentication material. For the first baseline use a stopped-service backup of the volume so SQLite and associated files are consistent. Treat backups as sensitive. Test restore into a separate volume.
- Jupyter credentials and notebooks persist independently. [Jupyter Docker Stacks](https://jupyter-docker-stacks.readthedocs.io/en/latest/using/common.html) documents storage and user permissions; check image UID ownership on the Linux server.
- Outbound access to FMP remains necessary. Office runtime/CDN resources and package registries may also be required. Self-hosted does not mean air-gapped.

## Deferred PostgreSQL integration

Keep the owner's future PostgreSQL data store separate from Workspace's application state. A later connector service can query that database and expose supported Workspace metadata/data endpoints. Excel and Jupyter consumption will need their own contract checks. No PostgreSQL service, schema, migration, or connector is introduced in this baseline.

## Baseline evidence required before declaring success

- Clean image builds from recorded sources; dependency availability and licenses recorded.
- Compose validation, startup health, Workspace login, save/restart persistence, backup and clean restore.
- Real entitled FMP request plus missing/invalid credential behavior; no key in frontend assets or sample outputs.
- Workspace widget discovery and a data result through the self-hosted API.
- Windows Excel trusted manifest, login, a supported data function, refresh, and reopen.
- Optional authenticated notebook fetch and notebook persistence across service recreation.
- Private Linux deployment repeats those checks from the Windows client over trusted HTTPS.

No runtime integration checks have been performed at this specification stage. Docker and Compose were detected locally. A Compose parser check alone cannot establish service compatibility.

## Delivery and verification amendments

The user requires Dagger as the build/check/publish owner and GitHub Actions as its runner. The [official Dagger integration](https://docs.dagger.io/getting-started/ci-integrations/github-actions/) supports invoking Dagger functions from GitHub Actions. Pin the Dagger engine/SDK and action revisions during implementation. Pull-request checks must not receive publish secrets; promotion follows successful checks. Keep browser tooling in verification images, not application runtime images. No Dagger module or GitHub workflow exists yet; these are spec requirements, not completed CI.

The user requested conventions from `../because-security-quant-terminal`. Adapted testing and CI policies live in `.kiro/steering/testing.md` and `ci.md`, with initial feature-to-spec-to-check mapping in `.kiro/breadth.toml`. No source-project PostgreSQL fixture, Angular/Perspective runner, browser profile, credentials, or acceptance status is imported. Those are specific to that application. The portable browser/parallelism rules are copied; actual QOpenBB runners will be implemented against its stack.

See [Lite versus Full](lite-vs-full.md) for source-verified differences. This comparison does not change the selected baseline variant automatically.
