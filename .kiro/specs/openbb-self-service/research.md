# OpenBB self service: baseline research

Research date: 2026-10-16. Status: requirements-phase research and deployment proposal, not an approved implementation design.

## Confirmed direction

Develop on Windows/WSL Docker; deploy to a private Linux server. Establish the upstream Full variant first, using OPENBB_IMAGE_VARIANT=full in the existing combined packaging. FMP and FRED are the primary data providers. Defer the owner's PostgreSQL data integration. Retain the bundled frontend/application backend. Public URL is https://qbb.hanse-hedge.fund through owner-managed Cloudflare Access/cloudflared; origin is plain HTTP on 0.0.0.0:23003. Bind state under ./data; no Docker-managed data volumes. Jupyter and wheel delivery are out of scope. Accept Anthropic integration before Excel implementation starts.

## Verified upstream facts

The [Workspace repository](https://github.com/OpenBB-finance/workspace) is public, archived, and contains terminalpro, backend-api, lite, and excel-add-in. The inspected main revision is `be00e95019a55d57af146919ee46b7e1a4859226`. Its root license is Apache-2.0; component notices must also be preserved. Archival is verified; a broader claim about the company's legal status is not needed for this spec.

The [Lite packaging](https://github.com/OpenBB-finance/workspace/blob/be00e95019a55d57af146919ee46b7e1a4859226/lite/README.md) already combines Workspace, its application backend, SQLite, Redis, and nginx. Persistent application state lives under `/data`. Use its Full build variant for the selected baseline; it retains the combined packaging. Its published quickstart names `openbb/lite:latest`; availability and a digest have not been verified here. Do not treat that mutable tag as a reproducibility pin. Some frontend settings are locked at build time.

The [data-platform repository](https://github.com/openbq-org/OpenBB) is separate and open source; the former OpenBB-finance/OpenBB URL redirects there. Its license must be inspected independently when pinning a release. The [OpenBB API launcher](https://docs.openbb.co/odp/python/extensions/interface/openbb-api) serves installed data extensions and Workspace metadata. Thus two different backends are needed: application state/authentication, and financial data.

The data API has [v4](https://docs.openbb.co/odp/v4/python/quickstart/workspace) and [v5](https://docs.openbb.co/odp/python/quickstart/workspace) documentation. The owner selected the latest API and regeneration of consumers. The [v5 provider FAQ](https://docs.openbb.co/odp/python/faqs/data_providers) states that FMP and EconDB packages were removed and their last releases require openbb-core 1.x. Therefore FMP adaptation is an explicit work item; adding the old package to a v5 image is not a supported solution. Pin the latest validated release and compare generated OpenAPI, widget metadata, function signatures, and auth contracts. Keep FMP credentials server-side; the adaptation must consume the project's FMP_API_KEY setting. The earlier general v5 credential guidance does not establish v5 FMP package compatibility.

The released [Excel auth source](https://github.com/OpenBB-finance/workspace/blob/be00e95019a55d57af146919ee46b7e1a4859226/excel-add-in/src/backend/auth.api.ts) calls `/pro/login`, `/pro/validate`, `/pro/logout`, and `/pro/user`. Its [data fetcher](https://github.com/OpenBB-finance/workspace/blob/be00e95019a55d57af146919ee46b7e1a4859226/excel-add-in/src/functions/fetcher/platform.api.ts) sends the user's Workspace bearer token to the configured platform URL. The standalone API's [documented authentication](https://docs.openbb.co/odp/python/quickstart/rest_api) is not proof that it accepts this token. This is an integration spike, not a solved configuration detail.

The [Excel environment example](https://github.com/OpenBB-finance/workspace/blob/be00e95019a55d57af146919ee46b7e1a4859226/excel-add-in/.env.example) separates backend, platform, and add-in URLs. The [Vite config](https://github.com/OpenBB-finance/workspace/blob/be00e95019a55d57af146919ee46b7e1a4859226/excel-add-in/vite.config.ts) uses `ADDIN_BASE_URL` while building the manifest and changes the function namespace for localhost builds. Preserve that distinction when validating workbooks. The package references `@openbb/ui`; public package availability and clean installation remain unverified.

## Proposed single-Compose organization

Primary user journey: add ready-made FMP-backed widgets, arrange/resize them, save a dashboard, reopen it, and refresh its data. The [OpenBB connector documentation](https://docs.openbb.co/odp/v4/python/quickstart/workspace) says installed endpoints become available as widgets through the data API. The v5 launcher similarly generates widgets.json. This is our self-hosted API, not OpenBB's hosted data service. The frontend's [widget search](https://github.com/OpenBB-finance/workspace/blob/be00e95019a55d57af146919ee46b7e1a4859226/terminalpro/src/components/LayoutAuth/Search/hooks/useFilterWidgets.ts) includes external-connector widgets; "external" here means outside the application backend, including our other Docker service.

Distinguish endpoint-generated widgets from the historical curated/premium data catalog. Lite locks packageDataEnabled off; Full enables that flag by default. Neither flag proves that historical catalog endpoints work against the self-hosted API. Verify the first dashboard using API-discovered widgets and actual FMP entitlements. Do not promise the whole historical catalog or premade dashboards without checking their routes and dependencies.

| Service | Baseline responsibility | State | Initial treatment |
| --- | --- | --- | --- |
| workspace | Upstream Full variant: frontend + application API + bundled SQLite/Redis | `./data/workspace` bind-mounted to `/data` | Required; retain packaging |
| data-api | Latest validated OpenBB API + FMP adaptation + FRED | configuration, no custom DB | Required; small reproducible image to build |
| excel | Serve upstream add-in build and manifest | generated assets in image | Excel profile; build/auth verification required |
| agent | Self-hosted Anthropic agent discovery and streaming | local runtime key; app-managed chat state | Required before Excel |
| Existing Workspace nginx | Single HTTP entry point and path routing | configuration in Full image | Minimal routing adaptation; Cloudflare stays owner-managed |

`compose.proposed.yaml` captures the service arrangement. It is deliberately not a root deployment file. Data API, Anthropic agent, and Excel images are explicit required inputs, not fictitious upstream image names. The file has no build recipes and must not be described as a working deployment. Image names in `compose.validation.env` are syntax-check fixtures only.

An initial local Workspace-only experiment can use the documented Lite image, but that does not prove the data API or Excel integration works. The selected baseline builds the Full variant from the owner-controlled Workspace fork and record image digests for deployment. The [Lite Dockerfile](https://github.com/OpenBB-finance/workspace/blob/be00e95019a55d57af146919ee46b7e1a4859226/lite/Dockerfile) expects an assembled build context: Lite files plus `backend/` from `backend-api/backend/` and `terminalpro/`. Do not assume the monorepo root is already that context. Its build also contains dependency-resolution steps that need checking for reproducibility.

## Development and deployment workflow proposal

1. Use QOpenBB as the controlling repository. Source lives in the owner's forks: [Workspace](https://github.com/norandom/openbb-workspace) and [data platform](https://github.com/norandom/openbb-data-api). sources.lock.json records exact initial snapshots. The data snapshot is develop at acquisition, not yet a validated release selection. Preserve notices and use reviewable adaptation commits.
2. Establish shared source/image/routing contracts, then implement independent lanes under .kiro/steering/delegation.md. Source builds run in WSL and GitHub through the same Dagger pipeline. Build Full from the monorepo's required assembled context.
3. Prove Full Workspace login, FMP/FRED widgets, dashboard editing, saved-layout reopen, and bind-directory backup/restore. Regenerate widgets against the latest validated API; adapt FMP as needed.
4. Implement and accept the self-hosted Anthropic agent: discovery, configured model access, streamed answer using selected dashboard data, errors, and dashboard usability when AI is down. This is a hard dependency before Excel implementation.
5. Then regenerate Excel functions and adapt authentication/URLs/manifest as needed. Build assets for the public /excel/ path and test through Cloudflare Access in the actual Office runtime. Preserve function compatibility or document migrations.
6. Dagger checks/builds/publishes immutable image sets in GitHub. The Linux server pulls those images and runs the same Compose service topology as WSL, with public URL settings adjusted for each environment. No source compilation on the server.

Jupyter is owner-managed on a separate VM. No notebook service, image, credentials, notebook test lane, or wheel publication is included now. Future wheel packaging can be specified separately if requested.

## Addressing, authentication, and persistence

- Public application: https://qbb.hanse-hedge.fund. Cloudflare handles client-facing HTTPS and Access; the owner manages cloudflared. The origin binds 0.0.0.0:23003 and speaks plain HTTP. 0.0.0.0 is the listen address; cloudflared's target is the reachable host/IP on port 23003.
- Reuse the Full container's nginx for one entry point. Proposed paths: / for Workspace, /api/ for its application backend, /data/ for the data API, /agent/ for the agent, /excel/ for add-in assets. Prefix rewriting, generated endpoint URLs, redirects, cookie settings, forwarded scheme, WebSockets and SSE must be verified; these routes are not implemented merely by declaring Compose services.
- Publish no other host ports. Do not bundle cloudflared, origin TLS certificates, or a separate certificate manager. WSL can use http://localhost:23003 for ordinary development; Office acceptance uses the HTTPS public hostname.
- Cloudflare Access is external infrastructure. The owner's network controls restrict direct origin access as appropriate. Application auth and Access are different layers: verify Office runtime login and noninteractive API calls. [Cloudflare service tokens](https://developers.cloudflare.com/cloudflare-one/access-controls/service-credentials/service-tokens/) may serve machine clients, but never bake an Access client secret into add-in JavaScript. Do not assume an interactive browser cookie automatically authenticates custom functions.
- Store persistent application data in ./data/workspace, bind-mounted to /data. Additional persistent application files, if needed, must also stay under ./data in the deployment directory. No named/anonymous Docker data volumes. Bind mount ownership must work on WSL and Linux. Use --project-directory . while the proposal resides under .kiro so relative paths resolve at the deployment root.
- Back up the bind directory and required secret configuration consistently; use a stopped-service backup for SQLite initially. Restore into a separate test directory. Jupyter state is not ours to back up.
- Keys stay in ignored .env and are passed only to the consuming runtime service. Outbound access to FMP, FRED and Anthropic is required. Office runtime/CDN resources and build registries may also be needed.

## Deferred PostgreSQL integration

Keep the owner's future PostgreSQL data store separate from Workspace's application state. A later connector service can query that database and expose supported Workspace metadata/data endpoints. Excel and Jupyter consumption will need their own contract checks. No PostgreSQL service, schema, migration, or connector is introduced in this baseline.

## Baseline evidence required before declaring success

- Clean image builds from recorded sources; dependency availability and licenses recorded.
- Compose validation, startup health, Workspace login, save/restart persistence, backup and clean restore.
- Real entitled FMP request plus missing/invalid credential behavior; no key in frontend assets or sample outputs.
- Workspace widget discovery and a data result through the self-hosted API.
- Windows Excel trusted manifest, login, a supported data function, refresh, and reopen.
- Anthropic discovery, streamed dashboard-aware answers, failure handling, and acceptance evidence before Excel starts.
- Private Linux deployment repeats those checks from the Windows client over trusted HTTPS.

No runtime integration checks have been performed at this specification stage. Docker and Compose were detected locally. A Compose parser check alone cannot establish service compatibility.

## Delivery and verification amendments

The user requires Dagger as the build/check/publish owner and GitHub Actions as its runner. The [official Dagger integration](https://docs.dagger.io/getting-started/ci-integrations/github-actions/) supports invoking Dagger functions from GitHub Actions. Pin the Dagger engine/SDK and action revisions during implementation. Pull-request checks must not receive publish secrets; promotion follows successful checks. Keep browser tooling in verification images, not application runtime images. No Dagger module or GitHub workflow exists yet; these are spec requirements, not completed CI.

The user requested conventions from `../because-security-quant-terminal`. Adapted testing and CI policies live in `.kiro/steering/testing.md` and `ci.md`, with initial feature-to-spec-to-check mapping in `.kiro/breadth.toml`. No source-project PostgreSQL fixture, Angular/Perspective runner, browser profile, credentials, or acceptance status is imported. Those are specific to that application. The portable browser/parallelism rules are copied; actual QOpenBB runners will be implemented against its stack.

See [Lite versus Full](lite-vs-full.md) for source-verified differences. The owner subsequently selected Full explicitly; that selection is now the baseline.

## Access and keys

- FMP: account/API key and endpoint entitlements for the desired widgets. Get the key from the [FMP dashboard](https://site.financialmodelingprep.com/developer/docs/dashboard). Required primary provider alongside FRED.
- FRED: required primary macroeconomic data source; uses FRED_API_KEY. See the [OpenBB FRED setup](https://docs.openbb.co/odp/python/quickstart/user).
- EconDB: optional; registered users can retrieve a token from their account. See [EconDB's access example](https://www.econdb.com/blog/pandas-datareader/). A v5 provider adaptation is required before promising this integration.
- ECB, IMF, OECD and other sources: use only the desired supported connectors. The [current provider inventory](https://docs.openbb.co/odp/python/extensions/providers) identifies keyless and credentialed providers; no universal subscription or key bundle is required.
- AI: required before Excel, but separate from data access. A custom agent can run as a self-hosted service implementing [agents.json and a streaming query endpoint](https://docs.openbb.co/workspace/developers/agents-integration), with its chosen model provider credentials or a reachable local model. An LLM key alone does not recreate the former hosted Copilot. Extra web-search services may need separate credentials. Anthropic is selected as the default Workspace AI provider. Model selection and the self-hosted agent implementation remain pending. ANTHROPIC_API_KEY is local-only; it must not enter frontend bundles or data-provider services. Credential validity has not been tested.
- Infrastructure: private Workspace login/bootstrap secrets, data API authentication, GitHub publication permissions, and registry pull access are separate from financial provider keys. GitHub/registry credentials must not be forwarded into application containers.

The root `.env.sample` contains empty keys and image settings. `.env` is gitignored and excluded from Docker contexts. Dagger must independently exclude secrets when constructing source contexts; .dockerignore alone does not guarantee that arbitrary Dagger directory uploads respect it. Pass only required keys to each runtime service. Never put provider keys in VITE_* variables or registry images. The Compose file remains a proposal; optional keys are not evidence of working integrations.
