# QOpenBB feasibility assessment

Assessed 2026-10-16. QOpenBB is feasible as a maintained integration project. The pinned sources are not a ready-to-run baseline: FMP compatibility and the Workspace build recipe need adaptation before dashboard acceptance. Cloudflare Access and the tunnel are owner-managed and are not feasibility blockers.

The first useful outcome for a financial engineer is a saved dashboard with FMP company data and FRED macroeconomic series that survives a restart and refreshes successfully. Full Workspace remains the chosen frontend. Feature flags alone do not prove that every upstream service or commercial chart component is available.

## Evidence and remaining work

| Area | Evidence obtained | Required acceptance |
| --- | --- | --- |
| FMP credentials | Direct profile and income-statement requests returned HTTP 200 and one record each | Requests through the maintained OpenBB API, with fixtures and selected live checks |
| FRED credentials | Direct GDP observations request returned HTTP 200 and one observation | Registered API route, generated widget, rendered data and error handling |
| Latest API | Pinned develop acquisition snapshot declares OpenBB 5.0.0 and core 2.0.1; FRED 2.0.0 supports core 2 | Select and pin the latest validated release, then build and accept owned sources; current snapshot is not a validated release |
| FMP extension | Released 1.6.1 requires core below 2; provider absent from V5 source | Maintain a compatible extension; validate registration, selected endpoints and schemas |
| Workspace build | Dockerfile references absent npm lockfile; monorepo supplies bun.lock | Choose and pin a reproducible package-manager path; clean Full build |
| Dashboards | API widget generator and bundled FRED app exist | FMP catalog/defaults; add, arrange, save, reopen and refresh actual dashboards |
| Anthropic | Model discovery authenticated with HTTP 200 | Select model; verify inference, streaming, selected-data context and recovery in Workspace |
| Excel | Source and generator exist; exact locked UI package is publicly downloadable | Regenerate against accepted API and verify Office behavior after Anthropic acceptance |
| Delivery | Compose proposal passes configuration checks | Dagger image builds, portable verification/publication and pull-only Linux deployment |

Direct credential probes ran on 2026-10-16. They used existing local credentials without publishing values. The local report is in ignored `artifacts/feasibility-provider-probes.json`. They establish access to those specific requests, not all subscription entitlements, LLM inference, or end-to-end application behavior. No clean image build, running application, browser acceptance or Excel acceptance has been completed.

## Data integration is the first compatibility gate

The latest [FMP package metadata](https://pypi.org/pypi/openbb-fmp/json) constrains `openbb-core` to `>=1.6.10,<2.0.0`. The [owned API snapshot](https://github.com/norandom/openbb-data-api/tree/7c9d4221bdf66965e3f6c7f4dc6ee848073e5ae2) uses core 2.0.1. Installing both unchanged is therefore incompatible.

A static inspection found all 74 imported core module paths and referenced symbols from the released FMP extension in the pinned core. That supports investigating a bounded port; it does not establish runtime compatibility. Select shared routers explicitly, register the maintained provider, and test the endpoints needed for the first dashboard before expanding coverage. Most FMP requests use stable endpoints, but the confirmed-earnings calendar still references a legacy endpoint and needs separate validation.

The existing [widget generator](https://github.com/norandom/openbb-data-api/blob/7c9d4221bdf66965e3f6c7f4dc6ee848073e5ae2/openbb_platform/extensions/platform_api/openbb_platform_api/utils/widgets.py) can generate catalogs from registered routes. FRED includes a dashboard whose widget IDs depend on router selection. Regenerate and check references after fixing the route contract; a wholesale generator rewrite is not justified by current evidence.

The released FMP extension retains AGPL-3.0-only metadata. Preserve component licenses and notices when incorporating it; the new API's Apache license does not relicense that extension.

## Workspace needs a reproducible build and a chart inventory

The pinned [Dockerfile](https://github.com/norandom/openbb-workspace/blob/be00e95019a55d57af146919ee46b7e1a4859226/lite/Dockerfile) copies a missing `terminalpro/package-lock.json` and runs `npm ci`. The tree contains `bun.lock`, with matching root dependency declarations. Existing assembly scripts also reference split repositories unavailable to anonymous requests. Build directly from the owned monorepo, pin tools, and prevent dependency resolution from rewriting locks during release builds.

Full selects the unrestricted frontend renderer, but the shared image still starts the backend in lite mode with some routers suppressed. Validate each required workflow rather than treating Full as proof that hosted features are present.

TradingView Advanced Charts is not distributed in this source tree and is disabled by default. AG Grid Enterprise, AG Charts Enterprise and Highcharts have separate commercial terms; a checked-in upstream key does not establish QOpenBB's rights. Public package availability, including Excel's locked `@openbb/ui` 0.3.0, proves downloadability only. Inventory the components actually used, preserve notices, and establish applicable rights or replacements before release. This does not require changing the selected Full variant.

## Deployment and delivery fit the requested setup

Use one steering Compose definition, with Full Workspace/application backend, a separate data API and an Anthropic agent. Excel joins later. Publish only plain HTTP `0.0.0.0:23003`; the owner routes `https://qbb.hanse-hedge.fund` through their existing tunnel. Persist state through project-relative bind mounts under `./data`. Keep the same service topology on WSL and private Linux.

Dagger builds owned pinned sources into images only. Portable repository commands execute acceptance checks and publication, with GitHub Actions as the initial runner and Gitea Actions a later replacement. The server then pulls those images. This is an architectural fit, not a validated pipeline. Build resource needs, package resolution, native dependencies, routing, streaming and bind-mount restore still need execution evidence.

No Jupyter service, notebook image, wheel publication or PostgreSQL integration is needed for this baseline.

## Recommended sequence and disproof conditions

1. Freeze the API routes, source/dependency locks, image contract and component license inventory. Establish complexity checking and the feature-to-spec-to-test map.
2. Adapt the FMP extension and Workspace build in separate owned lanes. Join them only at real FMP/FRED dashboard acceptance.
3. Integrate Anthropic and independently verify the complete Workspace interaction. Model discovery alone cannot pass this gate.
4. Start Excel implementation only after Anthropic acceptance. Regenerate functions and document compatibility changes.
5. Complete portable image publication, clean image-pull deployment and backup/restore acceptance.

Reassess the baseline if the selected FMP endpoints cannot be supported on the pinned API, essential dashboard components cannot be used under applicable terms or replaced, or saved dashboards cannot survive the required restart/restore workflow. The decision is supported only when these observable gates pass.

Future tasks must carry the 400 physical lines/file, 300 logical units/file and 50/function caps, with explicit exclusions and enforcement from [complexity steering](../../steering/complexity.md). Documentation and roadmap milestones do not approve design, tasks or implementation phases.
