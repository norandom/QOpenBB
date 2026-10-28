# Data platform reuse and requirements research

Research date: 2026-10-28. Two independent Sol research lanes inspected provider reuse and consumer contracts; the controller joins their findings. No live provider request, credential access, installation or application change was made. This is source discovery, not endpoint acceptance.

## Owned OpenBB platform and provider reuse

Owner constraint: retain and extend the existing OpenBB platform in [norandom/openbb-data-api](https://github.com/norandom/openbb-data-api). Do not build a parallel registry, query framework or ORM. Jupyter is a possible external client, not a required deployment service. A future database adapter implements appropriate provider contracts in the custom-data-source spec.

The local checkout, remote `qopenbb/baseline` branch and source lock identify `cab81b16bb9ef49272a6f3b0bf04cf9f34bde0ba`. The code is committed and the checkout was clean. Source history and notices must survive adaptation. Core is pinned at 2.0.1; historical provider package compatibility cannot be assumed.

Earlier owner constraints MD-F1-MD-F5 remain design inputs: owned source/pins/provenance (MD-F1/3), existing OpenBB machinery (MD-F2), shared consumer contracts and future provider extension (MD-F4), explicit selection/no silent semantic fallback (MD-F5). Their observable requirements are carried into requirements 8, 5 and 6; internal architecture belongs in the upcoming design.

## Provider lane findings

Paths below are relative to `vendor/data-api/openbb_platform` at the pinned revision.

| Existing source | Reuse finding |
| --- | --- |
| `core/openbb_core/provider/standard_models/` | Typed query/data models already cover many financial families; a model is not proof of a working installed route |
| `core/openbb_core/provider/abstract/provider.py`, `abstract/fetcher.py`, `provider/registry.py` | Provider registration and transform-query/extract/transform-data extension lifecycle exist |
| `core/openbb_core/app/query.py`, `app/model/obbject.py` | Existing dispatch and results/provider/warnings/extra envelope; complete financial metadata needs explicit verification |
| `providers/fmp/openbb_fmp/provider.py` | Only EquityInfo and IncomeStatement currently registered |
| `providers/fmp/provenance.json` | Historical FMP archive/hash/notices and adaptation provenance retained |
| `providers/fred/openbb_fred/__init__.py` | Multiple fetchers exist; installed extension choices affect exposed command/model identities |

Full historical FMP source is locally recoverable at Git revision `59c7c7eff44^`, path `openbb_platform/providers/fmp/`. Historical yfinance source is recoverable at `7a9ad1ecf10^`, path `openbb_platform/providers/yfinance/`. These are source recovery points, not target build revisions. Historical yfinance declares core 1.x compatibility; no blind package installation is proposed.

The maintained runtime in `services/data-api/pyproject.toml` installs core/equity/economy/FRED plus the adapted FMP package. It does not install yfinance or the commodity/fixedincome extensions. Historical source includes substantially broader FMP/yfinance fetchers, but current API compatibility, licensing notices, entitlement and financial outputs require a bounded restoration assessment.

## Consumer lane findings

- `contracts/datasets.json`, `widgets.json` and `apps.json` expose three configured starter datasets/widgets, not general exploratory coverage. Independent AAPL defaults do not establish shared company state.
- `contracts/openapi.json` and `routes.json` expose parameter/result schemas. The existing statement route has no general date filtering, cursor pagination or field projection. Filters must be described per dataset, not promised universally.
- `pipeline/qopenbb_ci/catalog.py` already freezes routes, validates catalog references, reuses matching upstream widgets and checks compatibility for Workspace/agent/future-Excel consumers. Complete parameter value/schema validation is not established by basic presence checks.
- `pipeline/qopenbb_ci/catalog_runtime.py` and `catalog_upstream.py` already invoke upstream widget generation using identified image inputs. Reuse is the default design path.
- `services/data-api/qopenbb_data/app.py` mounts upstream APIs and supplies discovery; `/agents.json` is empty. This is not accepted AI tooling.
- `services/data-api/qopenbb_data/gallery.py` demonstrates explicit metadata for packaged historical assets. It does not establish live provider metadata or query filtering.
- `contracts/provenance.json` retains generator source `49cc413e6ab67eaa0444e07485b0f9243c786f7b`; `contracts/sources.json` names the later fork revision. Generated-artifact provenance and current source availability must remain distinct.

## Design and verification handoff

The broad endpoint map is [provider coverage](../../../docs/provider-coverage.md) and its linked CSV inventory. Keep separate states for documented endpoint, retained implementation, adapted fetcher, installed route, verified entitlement, live result, widget and future AI exposure. Existing extension-point tests are `tests/contracts/test_catalog.py`, `tests/contracts/test_catalog_runtime.py` and `tests/delivery/test_onboarding_contract.py`; their presence does not count as passing new dataset checks.

After requirements approval, design must define concrete first-batch datasets and their shared input/output metadata, preserving broad FMP coverage as staged scope. Map retained code to required adaptations before writing replacements. Use provider and consumer implementation lanes only once contracts and file ownership are frozen, followed by independent review and an actual integrated journey. Production tasks must update the existing inventory and enforce 400 physical/300 logical/50-function limits; use existing background Playwright/CDP and bounded xdist checks, one heavy build/suite at a time. No implementation tasks are approved by this research.

The default steering files `product.md`, `tech.md` and `structure.md` are absent. Current context comes from AGENTS, the existing spec/roadmap and the available delegation, delivery, documentation, complexity, CI, testing and workspace-experience steering. No missing file was treated as read.

## Requirements review gate

Independent Astra review passed after one bounded repair pass on 2026-10-28. Two Sol research lanes supplied the provider and consumer findings above. The reviewed document has eight numbered requirement areas and 44 acceptance criteria. Corrections normalized EARS phrasing, made broad dataset delivery an obligation rather than a catalog-only promise, and retained the named OpenBB reuse mechanisms as binding owner constraints. Human requirements approval remains pending; design/tasks and implementation are not approved.

The controller verifies numeric IDs, EARS starts, links and JSON/TOML parsing before commit. This is documentation verification only; no provider, browser, financial calculation or image acceptance is claimed.
