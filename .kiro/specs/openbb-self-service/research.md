# OpenBB self service: baseline research

## Renderer parity discovery, 2026-10-16

The owner requires preservation of OpenBB's UX, design, themes, functionality and flag behavior during renderer replacement. This supersedes reduced-feature assumptions in earlier research. Kiro design discovery and controller synthesis produced the [compatibility discovery plan](parity-plan.md), [architecture findings](parity-research.md), [source capability matrix](../../../docs/renderer-capability-matrix.md) and [verification contract](parity-verification.md). Sol inspected original controls and schemas; Astra examined compatibility boundaries and exact installed Perspective declarations. A separate Sol reviewer approved the acceptance contract only, not replacement feasibility.

Critical gaps remain original Enterprise interactions, remote table semantics and open-ended Highcharts inputs. Original aggregation choices also conflict with the uncommitted financial guard. These are explicit design questions, not permission to remove features. The active amendment remains in design discovery; no production remediation or runtime parity is accepted.

Research date: 2026-10-16. Status: requirements approved for design; technical discovery and design review do not constitute implementation acceptance.

## Confirmed direction

Develop on Windows/WSL Docker; deploy to a private Linux server. Establish the upstream Full variant first, using OPENBB_IMAGE_VARIANT=full in the existing combined packaging. FMP and FRED are the primary data providers. Defer the owner's PostgreSQL data integration. Retain the bundled frontend/application backend. Public URL is https://qbb.hanse-hedge.fund through owner-managed Cloudflare Access/cloudflared; origin is plain HTTP on 0.0.0.0:23003. Bind state under ./data; no Docker-managed data volumes. Jupyter and wheel delivery are out of scope. Accept Anthropic integration before Excel implementation starts.

## Verified upstream facts

The [Workspace repository](https://github.com/OpenBB-finance/workspace) is public, archived, and contains terminalpro, backend-api, lite, and excel-add-in. The inspected main revision is `be00e95019a55d57af146919ee46b7e1a4859226`. Its root license is Apache-2.0; component notices must also be preserved. Archival is verified; a broader claim about the company's legal status is not needed for this spec.

The [Lite packaging](https://github.com/OpenBB-finance/workspace/blob/be00e95019a55d57af146919ee46b7e1a4859226/lite/README.md) already combines Workspace, its application backend, SQLite, Redis, and nginx. Persistent application state lives under `/data`. Use its Full build variant for the selected baseline; it retains the combined packaging. Its published quickstart names `openbb/lite:latest`; availability and a digest have not been verified here. Do not treat that mutable tag as a reproducibility pin. Some frontend settings are locked at build time.

The [data-platform repository](https://github.com/openbq-org/OpenBB) is separate and open source; the former OpenBB-finance/OpenBB URL redirects there. Its license must be inspected independently when pinning a release. The [OpenBB API launcher](https://docs.openbb.co/odp/python/extensions/interface/openbb-api) serves installed data extensions and Workspace metadata. Thus two different backends are needed: application state/authentication, and financial data.

The data API has [v4](https://docs.openbb.co/odp/v4/python/quickstart/workspace) and [v5](https://docs.openbb.co/odp/python/quickstart/workspace) documentation. The owner selected the latest API and regeneration of consumers. The [v5 provider FAQ](https://docs.openbb.co/odp/python/faqs/data_providers) states that FMP and EconDB packages were removed and their last releases require openbb-core 1.x. Therefore FMP adaptation is an explicit work item; adding the old package to a v5 image is not a supported solution. Pin the latest validated release and compare generated OpenAPI, widget metadata, function signatures, and auth contracts. Keep FMP credentials server-side; the adaptation must consume the project's FMP_API_KEY setting. The earlier general v5 credential guidance does not establish v5 FMP package compatibility.

The released [Excel auth source](https://github.com/OpenBB-finance/workspace/blob/be00e95019a55d57af146919ee46b7e1a4859226/excel-add-in/src/backend/auth.api.ts) calls `/pro/login`, `/pro/validate`, `/pro/logout`, and `/pro/user`. Its [data fetcher](https://github.com/OpenBB-finance/workspace/blob/be00e95019a55d57af146919ee46b7e1a4859226/excel-add-in/src/functions/fetcher/platform.api.ts) sends the user's Workspace bearer token to the configured platform URL. The standalone API's [documented authentication](https://docs.openbb.co/odp/python/quickstart/rest_api) is not proof that it accepts this token. This is an integration spike, not a solved configuration detail.

The [Excel environment example](https://github.com/OpenBB-finance/workspace/blob/be00e95019a55d57af146919ee46b7e1a4859226/excel-add-in/.env.example) separates backend, platform, and add-in URLs. The [Vite config](https://github.com/OpenBB-finance/workspace/blob/be00e95019a55d57af146919ee46b7e1a4859226/excel-add-in/vite.config.ts) uses `ADDIN_BASE_URL` while building the manifest and changes the function namespace for localhost builds. Preserve that distinction when validating workbooks. The package references `@openbb/ui`; the exact locked version 0.3.0 is publicly downloadable. Clean installation and license provenance remain unverified; see [feasibility assessment](feasibility.md).

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
6. Dagger builds images only; portable repository commands check and publish immutable image sets, initially run by GitHub Actions. The Linux server pulls those images and runs the same Compose service topology as WSL, with public URL settings adjusted for each environment. No source compilation on the server.

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

The owner clarified that Dagger owns image builds only. Verification, generation, publication and promotion belong to portable repository commands; GitHub Actions is the initial runner and Gitea Actions is a future replacement. No Gitea server or workflow migration is included now. The [official Dagger integration](https://docs.dagger.io/getting-started/ci-integrations/github-actions/) supports invoking Dagger functions from GitHub Actions. Pin the Dagger engine/SDK and action revisions during implementation. Pull-request checks must not receive publish secrets; promotion follows successful checks. Keep browser tooling in verification images, not application runtime images. No Dagger module or GitHub workflow exists yet; these are spec requirements, not completed CI.

The user requested conventions from `../because-security-quant-terminal`. Adapted testing and CI policies live in `.kiro/steering/testing.md` and `ci.md`, with initial feature-to-spec-to-check mapping in `.kiro/breadth.toml`. No source-project PostgreSQL fixture, Angular/Perspective runner, browser profile, credentials, or acceptance status is imported. Those are specific to that application. The portable browser/parallelism rules are copied; actual QOpenBB runners will be implemented against its stack.

See [Lite versus Full](lite-vs-full.md) for source-verified differences. The owner subsequently selected Full explicitly; that selection is now the baseline.

## Access and keys

- FMP: account/API key and endpoint entitlements for the desired widgets. Get the key from the [FMP dashboard](https://site.financialmodelingprep.com/developer/docs/dashboard). Required primary provider alongside FRED.
- FRED: required primary macroeconomic data source; uses FRED_API_KEY. See the [OpenBB FRED setup](https://docs.openbb.co/odp/python/quickstart/user).
- EconDB: optional; registered users can retrieve a token from their account. See [EconDB's access example](https://www.econdb.com/blog/pandas-datareader/). A v5 provider adaptation is required before promising this integration.
- ECB, IMF, OECD and other sources: use only the desired supported connectors. The [current provider inventory](https://docs.openbb.co/odp/python/extensions/providers) identifies keyless and credentialed providers; no universal subscription or key bundle is required.
- AI: required before Excel, but separate from data access. A custom agent can run as a self-hosted service implementing [agents.json and a streaming query endpoint](https://docs.openbb.co/workspace/developers/agents-integration), with its chosen model provider credentials or a reachable local model. An LLM key alone does not recreate the former hosted Copilot. Extra web-search services may need separate credentials. Anthropic is selected as the default Workspace AI provider. Model selection and the self-hosted agent implementation remain pending. ANTHROPIC_API_KEY is local-only; it must not enter frontend bundles or data-provider services. Direct model discovery authenticated successfully on 2026-10-16; inference and Workspace integration remain untested. See [feasibility assessment](feasibility.md) for the bounded provider probes and build findings.
- Infrastructure: private Workspace login/bootstrap secrets, data API authentication, GitHub publication permissions, and registry pull access are separate from financial provider keys. GitHub/registry credentials must not be forwarded into application containers.

The root `.env.sample` contains empty keys and image settings. `.env` is gitignored and excluded from Docker contexts. Dagger must independently exclude secrets when constructing source contexts; .dockerignore alone does not guarantee that arbitrary Dagger directory uploads respect it. Pass only required keys to each runtime service. Never put provider keys in VITE_* variables or registry images. The Compose file remains a proposal; optional keys are not evidence of working integrations.

## Design discovery and synthesis: 2026-10-16

Discovery scope: complex integration. Applied `kiro-spec-design` full discovery, boundary-first synthesis and review rules, plus the project's COBESY documentation, complexity, testing, CI and delegation steering. Existing core product/tech/structure steering is absent; approved requirements and custom steering supplied the project context. Two bounded read-only research workers inspected runtime and delivery contracts; the controller synthesized the design.

### Runtime findings

- [Workspace request helper](https://github.com/norandom/openbb-workspace/blob/be00e95019a55d57af146919ee46b7e1a4859226/terminalpro/src/lib/api.tsx) uses substring matching for its backend URL. Consequently `/data/api/v1` can receive application authentication intended for `/api`. Extract an origin/path-boundary matcher and test both route families before dashboard acceptance.
- [Application auth helpers](https://github.com/norandom/openbb-workspace/blob/be00e95019a55d57af146919ee46b7e1a4859226/backend-api/backend/api/auth_helpers.py) issue opaque database session IDs, not portable JWTs. [OpenBB API auth](https://github.com/norandom/openbb-data-api/blob/7c9d4221bdf66965e3f6c7f4dc6ee848073e5ae2/openbb_platform/core/openbb_core/api/auth/user.py) instead offers HTTP Basic. The design deliberately uses the owner's existing Access/origin boundary for data and agent services, with API Basic disabled; it does not introduce a session-to-service gateway.
- [Bootstrap](https://github.com/norandom/openbb-workspace/blob/be00e95019a55d57af146919ee46b7e1a4859226/lite/entrypoint.sh) persists secrets but prints administrator credentials. Suppress those log messages. [nginx](https://github.com/norandom/openbb-workspace/blob/be00e95019a55d57af146919ee46b7e1a4859226/lite/nginx.conf.template) overwrites the forwarded protocol with origin HTTP; derive forwarded scheme from validated deployment configuration.
- Connector discovery and widget requests run in the browser. Use absolute public connector bases and preserve generated internal API paths. Install shared equity/economy routers explicitly to avoid FRED fallback route/ID changes. First acceptance covers FMP profile/income and FRED GDP; unsupported mappings are not advertised as accepted.
- The inspected [agent SDK models](https://github.com/OpenBB-finance/openbb-ai/blob/9a2f0991002cd48d2d0bc5606498b52167a1c6fc/openbb_ai/models.py) support a stateless selected-data callback. Use that existing protocol rather than arbitrary server-side widget URL fetching. Disable hosted Copilot enhancements so custom-agent use does not trigger unavailable title/prompt endpoints.

### Architecture pattern evaluation

| Option | Decision | Reason |
| --- | --- | --- |
| Retain Full combined packaging and add data/agent services | Selected | Preserves app state/auth and the owner's single Compose control point |
| Split all bundled Workspace processes into new services | Rejected for baseline | Adds lifecycle and storage migration work without a requested outcome |
| New authentication gateway or shared application JWTs | Rejected | Existing session IDs are not portable; owner-managed edge/origin already supplies the chosen service boundary |
| Rebuild schema/widget generators | Rejected | Existing generators support the required contract; adapt inputs and test output |
| Dagger controls verification and publication | Rejected by owner clarification | Dagger is exclusively the image builder; CI commands must remain portable to Gitea |
| Compose translation inside Dagger for acceptance | Rejected | It is outside Dagger's scope and cannot establish real bind/lifecycle behavior |

### ECharts amendment synthesis

The owner selected Apache ECharts after requiring original OpenBB control, theme, state and feature-flag parity. Current evidence and unresolved contracts are in [ECharts findings](echarts-findings.md), the [editor contract](echarts-editor-contract.md) and the [integration proposal](echarts-integration-proposal.md). The proposal is not a finalized design or implementation approval.

Generalization: integrated and detached chart paths should retain their original storage forms while sharing renderer lifecycle and option mapping. Unknown-field retention is distinct from semantic support. One original state owner must serve controls, refresh and saved configuration.

Build versus adopt: ECharts supplies rendering and public interaction/export APIs; existing OpenBB/Radix/react-colorful components supply control primitives. The AG-owned docked editor still needs compatible field/state behavior. No inspected library is a complete drop-in replacement for that editor. Native Perspective UI and a new chart toolbar do not satisfy the owner's requirement.

Simplification: integrate at the existing chart container and existing action/state seams, without emulating all AG Grid APIs, introducing a general renderer framework or replacing dashboard storage. Keep provider fetching and SQLite persistence repair separate. Table capabilities and open Highcharts options remain required compatibility work, not implicitly covered by a grouped-column probe.

Workflow guidance: `kiro-spec-design` supplies discovery, synthesis and the final design review gate; `kiro-review` and `kiro-verify-completion` constrain evidence claims. Existing documentation steering supplies COBESY's conclusion-first, evidence-qualified format. Core product/tech/structure steering remains absent; approved requirements and the available specialized steering remain authoritative. Final design generation is deferred until the concrete compatibility gaps are resolved.

### Design decisions

Generalization: one selected API schema and dataset inventory supplies widget generation, later Excel generation and data-fidelity checks. One immutable release/evidence identity supplies local verification, CI promotion and Linux install. These contracts reduce duplicate configurations without introducing a general plugin framework.

Build versus adopt: adopt upstream application state/auth, shared data routers, widget generator and SDK event models. Build only the FMP compatibility changes, narrow origin/request fixes, Anthropic adapter and portable build/release glue needed for the selected journeys. Keep provider licenses and unavailable/commercial chart capabilities visible.

Simplification: Dagger builds/exports images only. Repository commands run actual Compose tests, generation, image push and promotion directly on the supported local Docker host. GitHub wrappers supply inputs/secrets and retain artifacts. [Gitea Actions](https://docs.gitea.com/usage/actions/overview/) is broadly compatible but a later migration still needs wrapper/runner validation; the design does not claim that validation has happened. Registry and source locations are inputs, not embedded GitHub service dependencies.

### Risks and implementation evidence

- Frozen Bun installation, selected API/FMP compatibility and exact tool pins must pass clean builds before becoming validated release inputs.
- Request-boundary correction, public paths, account setup, mixed dashboards, selected-data callbacks and Office behavior need runtime evidence; static inspection establishes contracts only.
- Actual Compose runs use disposable daemon-host bind roots and fixed port 23003; path ownership and port collision handling are foundation checks.
- Candidate manifests permit pull-only Linux and Office acceptance before promotion, avoiding a circular release gate. All required records must match the candidate's exact image/contract identities.
- Changing the runner must preserve the same repository commands and secret boundaries. A clean environment without GitHub-specific variables tests this seam; actual Gitea migration remains deferred.

### Next chart boundary discovery, 2026-10-16

Two independent Sol source investigations established the [displayed-row and SQLite contracts](chart-next-discovery.md). Parent synthesis keeps resolved numerical snapshots separate from grid capture, editor decoding and backend persistence. Existing ECharts rendering and SQLAlchemy dialect support remain the adopted mechanisms; no new service or generic renderer framework is proposed. The [bounded design](chart-snapshot-design.md) passed independent Astra review after explicit category ownership and unit/scale rules were added. The owner subsequently approved design and tasks 2.19-2.23; their implementation is now [accepted within that boundary](chart-snapshot-verification.md). Broader parity and persistence remain unverified. The kiro-spec-design discovery/synthesis/review workflow and COBESY documentation steering guided this work.

### Original editor integration discovery, 2026-10-16

Parallel Sol source and original-browser investigations established [saved option paths and resolution boundaries](chart-option-discovery.md). Seven actual outgoing synthetic-dashboard payloads show family-specific bar edits retained across family changes. Source inspection establishes generated-common replacement and distinct integrated/detached semantics. Controller synthesis proposes a pure original-options resolver and typed editor patches, retaining existing reducers. Current mapper style inputs cannot yet represent the complete original theme/editor contract; effective formatting and application activation remain design work. No new implementation approval or parity acceptance follows from this research.

### Option-state design synthesis, 2026-10-16

The next bounded design separates saved option state from effective rendering. Generalization: initialization and later partition synchronization share a copied baseline but have different fallback rules; an explicit transition preserves that difference. Existing integrated and detached reducers remain authoritative. Build versus adopt: retain pinned lodash clone/merge and current reducer types; add only application-specific baseline selection and typed captured-control patches. No new library or service is required.

Simplification: defer generated function-bearing options, theme precedence and renderer projection to their own reviewed contract rather than introduce a JSON-only approximation that would lose formatters. The column editor mapper covers observed bar title, legend and stroke semantics; detached composition must supply complete event options because the original reducer replaces them. A Sol source investigation confirmed current types and transition rules; the controller synthesized the draft under kiro-spec-design. Production implementation remains gated on design and task approvals.

The [option-state design](chart-option-state-design.md) passed independent Astra review after one repair pass clarified own undefined chart-type rejection, exact event fields and validation of unused fallback inputs. The review is `artifacts/option-state-design/review.md`. This is design readiness for owner review, not implementation or renderer acceptance. Core product/tech/structure steering remains absent; approved requirements and specialized project steering supplied the context.

During option-state implementation, a parallel read-only Sol investigation recorded the [next effective-style boundary](chart-effective-style-discovery.md). It separates source-proven OpenBB defaults from AG inherited runtime values, identifies independent fill/stroke and line marker/gap semantics, and defines the remaining capture matrix. No production styling change or visual parity claim follows from that research.

### Explicit appearance synthesis, 2026-10-17

Parallel Sol lanes captured original line-editor actions and investigated the pinned AG effective-options API. [Line appearance findings](chart-line-appearance-findings.md) record payload hashes, default gap/marker behavior, retained title text and diagnostic limitations. Public getOptions returns user inputs; private processed options require the real chart factory. Neither a guessed JSON merge nor a production dependency on AG internals is acceptable.

Controller synthesis under kiro-spec-design keeps explicitly resolved appearance separate from theme resolution. Extend the existing mapper contract and adopt ECharts fields for separate fill/stroke, title visibility, typography, gap connection and circular markers. Preserve legacy inputs and numerical mapping. Extract cohesive style logic to satisfy the existing complexity limits, with no additional renderer abstraction. Original theme defaults, layout, financial formatters and application activation remain subsequent contracts. COBESY steering guides evidence-qualified documentation for financial engineers; core product/tech/structure steering remains absent.

The [appearance design](chart-appearance-design.md) passed independent Astra review after one local repair made caption font-size validation explicit. Review: `artifacts/chart-appearance-design/review.md`; reviewed design SHA-256 `49e7250ea4d2f3a8f91bf99ee3cad62b74477e29673fced751826ccb8466272b`. Human design approval remains pending; no new implementation or test pass is claimed.

The owner subsequently approved the appearance design. Kiro task generation produced six bounded tasks, 2.28-2.33, with shared contract freeze, two disjoint Sol lanes, serial mapper/browser joins and independent Astra acceptance. Independent task-graph sanity review returned PASS (`artifacts/appearance-tasks/review.md`). The merged task map covers all 69 acceptance criteria; this is a planning coverage check, not passing runtime evidence. Tasks await human approval. Approval-status wording in the published design was updated after its recorded review hash; technical contracts are unchanged.

The owner then approved tasks 2.28-2.33. Their [implementation is independently accepted](chart-appearance-verification.md): explicit styles now project through the existing mapper, with 260 units, four reproduced browser cases, thirteen-module caps and matching source identities. Pixel checks cover gaps, markers, captions, retained titles and rejection/recovery. This closes the bounded appearance input/projection work; original theme resolution and application parity remain open.

### Completion and SQLite synthesis, 2026-10-17

The owner clarified that completion means a deployable original-looking Workspace. Parallel Sol source audits found the accepted chart chain has no working application caller, and identified SQLite query repair as an independent persistence boundary. The [completion plan](../../../docs/completion-plan.md) now distinguishes these joins from provisional packaging and removes stale native-explorer next-step wording. The original per-chart editor is enterprise-owned UI; the separate entity theme settings controls are reusable application code. Effective-theme research and original browser capture remain necessary before a real application join can claim parity.

Controller synthesis under kiro-spec-design keeps the persistence repair inside existing CRUD. Generalization: all six name projections use the same typed string expression; their joins and permissions remain distinct. Adopt SQLAlchemy's dialect-aware string operation rather than a SQLite function shim or new adapter. Simplification: seven targeted sites with a reviewed exact size exception avoid unrelated decomposition of the large upstream file. Core product/tech/structure steering is absent; approved requirements and specialized project steering supply the constraints.

The [SQLite supplement](sqlite-repair-design.md) passed independent Astra design review after preimport configuration isolation was made explicit. Review: `artifacts/completion-path/sqlite-design-review.md`. Proposed exceptions are bounded to the final measured file/revision, expire 2026-11-17 and preserve function caps. Owner design approval and implementation tasks remain pending. No database test or production repair is claimed by this research; the inspected pipeline environment lacks the backend dependencies.

The owner subsequently approved the SQLite design and exception and requested task generation. Kiro task generation now defines an independent backend branch with explicit runtime setup, real read regressions, storage reopening and controller-owned acceptance. This approval does not waive task review or subsequent implementation verification.

Tasks 4.6-4.9 passed independent Sol task-graph review (`artifacts/completion-path/sqlite-task-review.md`). The merged plan contains 89 unique task IDs and covers all 69 active criteria; these counts describe planning, not execution. Task 4.5 now explicitly waits for 4.9, while the new backend branch starts from accepted foundations and 2.5, avoiding a dependency cycle. Tasks await owner approval.

Parallel original-browser research captured [settled dark grouped-column defaults](chart-theme-runtime-findings.md) through the original table button and a reference-only private inspector after rendering settled. This closes one effective-default observation, with source/image identities and a visually inspected screenshot. Two original page errors remain recorded; no clean-diagnostics, candidate parity or persistence claim follows. The light/custom/other-family matrix remains open. Both owned containers and the isolated browser were cleaned up.

### SQLite implementation follow-through, 2026-10-17

The owner subsequently approved tasks 4.6-4.9. Tasks 4.6-4.8 are independently accepted at Workspace `f23cb786a946a6a996deedbe87be9c7ca86b221e`: the restored locked runtime executes 60 regression cases, including six reads and actual bulk storage across SQLite engine recreation. The missing creator join is a reproduced upstream defect; current SQLite supports the previous concat expression, so the other six edits address portability. No database migration or adapter was introduced. The [verification record](sqlite-repair-verification.md) owns final joined acceptance and its remaining application-level limits.

### Real application design review, 2026-10-17

The [application integration draft](chart-application-integration-design.md) connects displayed-grid capture, effective appearance, the original docked editor and existing state reducers to the actual Workspace journey. Independent Astra review found the architecture and exclusive lane ownership sound, but returned NO-GO for runtime task generation until finite theme, field/event, range and formatter contracts are evidenced and frozen. It does not require every release capability before this bounded integration. Review: `artifacts/chart-application-design/review/design-review.md`. Fourteen current source boundaries were measured with the pinned WSL parser; current files meet caps, while restoring original monoliths would require cohesive extraction. Original-reference research continues within the authorized discovery scope; new runtime tasks and approval are not implied.

The [grid range source contract](chart-grid-range-contract.md) separates integrated live-grid inputs from detached extraction and state behavior. The [stock theme matrix](chart-theme-matrix-findings.md) then captured all six initial family/mode combinations through actual original UI actions, with exact case/attempt mapping and disposable-state cleanup. The first Settings selector and raw-data projection failed before correction; those failures remain retained. A suspected missing bar was disproved by pixel measurements and matching numeric inputs. The remaining custom-theme and expanded editor/range observations still gate interface freeze; no candidate renderer acceptance follows.

### Custom themes, formatting and published evidence, 2026-10-17

The [custom-theme run](chart-custom-theme-findings.md) observes actual dark/light admin edits, two successful Save Theme responses and grouped-column effective palette/background values matching the saved inputs. The initial stock-theme assertion was corrected for custom names. Node and output assertions exited 0; a trailing CR-only shell line produced wrapper exit 1 after browser completion. Cleanup and these distinct outcomes remain recorded. Independent review accepts only these two reference cases, not broader custom inheritance or backend reread.

The [formatting contract](chart-format-control-contract.md) records original callbacks and saved-option composition. Review corrected date-only versus datetime handling and the unguarded Index formatter call. Numeric/fiscal semantics remain source observations; nested editor event paths and library range/formatter invocation still gate runtime task generation. The [review](../../../artifacts/reviewed/formatter-contract-review/review.md) preserves that bounded decision.

The owner requested artifact commits and folder synchronization before push. [Reviewed artifacts](../../../artifacts/reviewed/README.md) now publish selected exact-byte evidence with source/published hashes, explicit exclusions and independent publication review. Raw credentials, accounts, runtime state and caches stay local. Git attributes preserve byte hashes across Windows/Linux. This adds evidence availability without upgrading application or deployment acceptance.

### Source-safe integration contracts, 2026-10-17

The revised application design makes session addresses/revisions, four existing column edits, reducer ownership and financial display callbacks explicit. Independent Astra review permits controller contract freeze and A1/B1 task planning after the required human phase approvals. A conflicting capture envelope was corrected to the canonical `SessionResult<ResolvedSnapshotInput>` with stamp/value. The remaining range, nested-control and formatter invocation evidence gates its consuming A2/mapper/C/D work; it no longer blocks source-safe state and formatting tasks. This is a scoped design decision, not renderer or deployment acceptance. Review: `artifacts/chart-integration-freeze-review/review.md`.

The Kiro design workflow and root-cause debug protocol guided this refinement. Documentation follows the project COBESY policy: distinguish observed behavior from planned work and make each remaining gate actionable. The nested-editor probe and its bounded retry are recorded in [the runtime ledger](chart-editor-runtime-contract.md); unsuccessful actions establish no new control contracts.

### Approved design and bounded task plan, 2026-10-17

The owner approved the reviewed application integration design. Tasks 2.34-2.37 now cover controller contract/test-scope setup, parallel A1 session/range and B1 financial formatting work, and a joined source-safe verification gate. Independent Astra task-graph review passed after one repair added the existing compatibility strict check and clarified path ownership. The merged plan has 93 unique task IDs and maps all 69 acceptance criteria; mapping is not evidence that the criteria pass.

The top-level lanes and parent tasks 2.12, 3.8, 4.1, 4.3 and 4.5 now preserve current renderer/catalog/image prerequisites and original controls/state rather than relying on the superseded Perspective baseline. Unresolved runtime components remain explicit followups requiring frozen contracts and reviewed tasks. No production code or application verification ran in this planning turn. [Task review](../../../artifacts/reviewed/chart-integration-task-review/review.md) records the bounded PASS; task approval remains separate under the Kiro task-generation workflow.

### Original runtime contracts and bounded capture amendment, 2026-10-17

The owner approved parallel runtime-contract research after tasks 2.34-2.37. The Kiro extension discovery/design workflow and project COBESY policy guide this batch. The [results and next boundary](chart-runtime-next-plan.md) distinguish source rules, original observations and proposed internal validation policy. No new dependency is needed: reuse public Community GridApi values, the frozen capture signature and the accepted snapshot validator rather than a parallel extractor or private chart inspector.

The grid lane captured seven cases with fifteen array/identity assertions. The focused editor lane exercised eighteen actions with twenty-two evidence assertions; earlier failures remain preserved. Independent appearance audit identifies inherited grid/subtitle changes beyond palette/background and the absence of conflict-precedence evidence. The design implication is a bounded explicit-category capture amendment while appearance and editor obligations remain separate named joins. This generalizes the observation boundary, not category inference or whole-theme inheritance. It adds no production capability gate and does not narrow the required original UX.

Human approval of the concrete capture amendment remains distinct from approval of this research plan. Existing accepted helpers and the main application design retain their recorded status. No implementation tasks are silently approved by these findings.

## Ordinary grid-capture task plan, 2026-10-17

The approved design is split into sequential tasks 2.38-2.40: actual Community-grid fixture/setup, bounded adapter with tests, and joined verification. Independent Sol review passed with all 69 numeric requirements mapped and no explicit dependency cycles. See the [frozen review](../../../artifacts/reviewed/grid-capture-tasks/review/review.md). The application test configuration avoids the root AG Grid mock; fixture imports require a narrow controller-owned resolveJsonModule addition. These are checked prerequisites and planned tests, not implementation acceptance. Production ownership retains the 400/300/50 caps and application activation remains gated.

## Ordinary grid-capture acceptance, 2026-10-17

Tasks 2.38-2.40 are independently accepted at Workspace 76edf85a46298f7bc5212ff9944e4b66e9baa4af. A revoked-Proxy exception escaped the first error handler; two failing regressions drove a private WeakMap repair, independently reverified. The final join passes 88 application tests, 260 compatibility tests, both strict compilers, scoped lint, 66 source/config identities and the 173-file maintained audit. The [verification report](chart-grid-capture-verification.md) owns scope and evidence. Original UI activation, complete appearance/editor behavior and deployment remain open.

## Appearance and editor discovery follow-up, 2026-10-17

The owner authorized continued research. Sol lanes ran source analysis concurrently, with isolated original browser captures serialized; Astra independently reviewed the frozen evidence. Kiro extension discovery and the COBESY documentation policy guide the [joined findings](chart-runtime-next-plan.md#appearance-and-editor-follow-up-2026-10-17). No candidate production code or dependency changed.

The appearance review disproved a byte-domain color shortcut even though it matched the captured examples. Preserving normalized-channel floating-point evaluation matches the installed MIT utility across 262,144 channel comparisons. This supports resolved color tokens, not an arbitrary theme interpreter. Saved-widget composition must be assessed through the owned hook, separately from direct library updates. Tooltip patches, hover content, numerical transpose and Sum geometry likewise remain distinct evidence layers.

Controller synthesis: retain the existing theme/session/state owners and ECharts public rendering APIs. Join derived tokens, saved-family precedence and mapper coverage in the appearance boundary rather than treating a tiny color helper as application completion. Keep numerical transformation separate from option patches and financial display formatting. Existing libraries already own rendering, persistence and state merging; no new service, generic resolver, storage envelope or alternate editor is justified by these findings. The finite captures do not waive remaining appearance/editor fields, full capability coverage or backend save/reopen. New implementation still requires a concrete reviewed design and approved tasks with the existing inventory and 400/300/50 caps.

## Appearance/editor contract design, 2026-10-17

The [design amendment](chart-appearance-editor-integration-design.md) turns the reviewed findings into explicit composition, color and grouped-tooltip contracts. Kiro extension discovery reused the pinned local source and completed runtime evidence; no new library or external service is proposed. A Sol explorer checked existing signatures and file responsibilities. The controller performed synthesis and Astra reviewed the draft independently. Documentation follows the project COBESY convention: the review decision and acceptance limits precede reference detail.

The design retains `OptionBaseline` and existing reducers as state owners, with generated render options kept separate from saved options. The helper consumes explicit resolved color tokens instead of recreating AG's parameter graph. Tooltip edits extend the existing typed command rather than creating another editor store. The mapper still needs explicit original appearance fields and visual evidence; transpose/Sum belong to a separate numeric contract. These boundaries allow source-contract work to proceed after approval without pretending that full B2/C is complete.

Review tightened three handoffs: exact baseline/generated operands and reducer inputs, session-level unresolved handling distinct from mapper validation errors, and descriptor-safe color token classification without a CSS parser. The main design retains all 69 criteria; this amendment changes only named chart contracts. Core product/tech/structure steering files remain absent; the existing specialized steering supplied project policy. No production implementation, task approval or application acceptance is inferred from this design work.
