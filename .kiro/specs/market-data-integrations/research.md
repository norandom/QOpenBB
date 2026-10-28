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

Independent Astra review passed after one bounded repair pass on 2026-10-28. Two Sol research lanes supplied the provider and consumer findings above. The reviewed document has eight numbered requirement areas and 44 acceptance criteria. Corrections normalized EARS phrasing, made broad dataset delivery an obligation rather than a catalog-only promise, and retained the named OpenBB reuse mechanisms as binding owner constraints. Requirements were subsequently owner-approved; current phase approvals are recorded in spec.json.

The controller verifies numeric IDs, EARS starts, links and JSON/TOML parsing before commit. This is documentation verification only; no provider, browser, financial calculation or image acceptance is claimed.

---

## Approved-requirements gap analysis

Owner approved the 44 criteria on 2026-10-28. Discovery is an integration-focused extension of the existing framework, with focused external API compatibility research. The controller applied Kiro gap/design rules, COBESY composition and corporate-finance conventions already loaded for this work. No new dependency selection or application implementation occurred.

| Requirements | Existing asset | Gap classification |
| --- | --- | --- |
| 1, 6 | Installed OpenAPI, native widget generator and catalog compatibility checks | Missing broad descriptors, bounds/value validation and metadata schema exposure |
| 2 | Two maintained FMP fetchers and retained historical implementations | Missing restoration/installed routes; unknown live entitlement and latest response details |
| 3 | Standard search/profile/price models | Missing adapted FMP search; unknown provider identity equivalence |
| 4 | AnnotatedResult and OBBject metadata transport | Missing common typed financial metadata and field-level semantic guarantees |
| 5 | Provider registry and existing query executor | Constraint: explicit provider/default policy; no implicit cross-provider financial equivalence |
| 7 | Sanitized FMP transport and existing exception handlers | Missing stable typed attributes/retry information; unsafe legacy multi-request path |
| 8 | Owned forks, source pins, Dagger/publication and existing verification | New coverage needs independent actual evidence; historical artifact generation source is distinct |

### Architecture pattern evaluation

| Option | Benefit | Limitation |
| --- | --- | --- |
| Extend each provider using existing free-form metadata only | Least shared code | Repeated metadata conventions and no discoverable schema; insufficient consumer consistency |
| New facade/ORM and parallel query registry | Could centralize all behavior | Duplicates OpenBB, breaks owner reuse constraint; rejected |
| Extend existing providers plus small typed metadata/catalog/error contracts | Reuses execution and generation while making semantics explicit | Requires a reviewed shared contract and coordinated catalog regeneration |

The hybrid extension is selected for design. Broad restoration has high integration risk and XL scope overall; the first financial-input batch is L scope, not a single implementer task. These are planning categories, not delivery-date promises. Endpoint restoration is split by model, with shared-contract work first.

## Design discovery findings

### Provider restoration

The retained FMP tree supplies balance_sheet, cash_flow, equity_historical, equity_peers, key_metrics and financial_ratios modules. Name/symbol search uses the existing standard EquitySearch model with a new FMP adaptation. Current core/historical FMP lack a dedicated enterprise-values model; an inspectable provider EV-input dataset needs a small standard model, fetcher and native equity route rather than disguising the inputs as key metrics.

Official documentation consulted by the provider lane:
- [FMP catalog](https://site.financialmodelingprep.com/developer/docs)
- [Daily EOD history](https://site.financialmodelingprep.com/developer/docs/stable/historical-price-eod-full)
- [Peer references](https://site.financialmodelingprep.com/developer/docs/stable/peers)
- [Symbol search](https://site.financialmodelingprep.com/developer/docs/stable/search-symbol) and [name search](https://site.financialmodelingprep.com/developer/docs/stable/search-name)
- [Enterprise values](https://site.financialmodelingprep.com/developer/docs/stable/enterprise-values)

These establish documented endpoints, not subscription access. Statement/metric/EV documentation reports 1000-record limits and EOD history a 5000-record limit; design applies explicit bounded first-batch policies subject to actual response verification.

Restoration hazards: current statement aliases need fiscalYear/filingDate compatibility; historical limit-zero behavior silently falls back to five; TTM metrics fabricate today's date and mix requests; price transformations mutate input and lose exact zero percentage changes. Legacy multi-request extraction bypasses the complete sanitized transport wrapper. These require focused regressions, not blind file restoration. Full symbol/date coverage is unknown until marked live checks run.

### Consumer contracts

`AnnotatedResult.metadata` is unwrapped into `OBBject.extra.results_metadata`; `extra.metadata` is separate execution information. Financial metadata is validated in fetchers and described by a generated schema/operation extension. Unrestricted OBBject.extra does not itself supply that schema. Output callbacks are unsuitable as the required correctness seam because their activation/validation behavior is optional.

The mounted upstream API owns its exception handlers. Installing only outer-app handlers is insufficient. Existing OpenBB wrappers can retain typed exceptions under original; normalize recognized typed categories without parsing arbitrary provider messages. Preserve baseline 204 empty results and existing detail-compatible status behavior while adding safe machine-readable fields.

The service/API and Python defaults are not interchangeable: native Python container selection can fall back through credential-based provider priorities, while API assembly discards provider from ordinary command defaults. New service commands therefore use explicit provider parameters; generated widgets pin that value. Baseline route defaults remain disclosed and tested. No global Python/core provider-selection rewrite is proposed.

### Design synthesis

- Generalize only shared financial metadata, failure categories and schema descriptions; use existing dataset-specific provider QueryParams/Data classes.
- Adopt existing Provider/Fetcher/Query/OBBject and upstream widget generation. Keep one runtime descriptor projection, reused by generation, with compatibility validation in the existing pipeline.
- Separate evidence states from executable provider dispatch. The coverage index is documentation/evidence, not a routing registry.
- Do not introduce database storage, AI execution, a generic query language, mutable callback layer or a new testing harness.
- Query bounds and shared metadata freeze before disjoint provider and consumer implementation lanes. The controller owns registrations, pins, generated proposals and joins.

## Risks and open acceptance evidence

Account entitlement, actual stable responses, detailed TTM semantics, paginated completeness and provider-specific identity mappings remain live-verification work. Unknown source dates/vintages stay unknown. A real-provider failure is not repaired by silently substituting a gallery fixture. Existing unrelated catalog renderer edits must be preserved and reconciled before production changes to overlapping files. Modified upstream files still require whole-file complexity enforcement or a reviewed design exception.


## Final design review and decisions

Independent Astra design review passed after one local repair pass on 2026-10-28. All 44 requirements appear in the traceability table. Requirements and design approval are recorded.

The four repaired seams are now explicit in design.md: the generated-descriptor-based service guard enforces explicit provider selection on the named non-baseline operations; common metadata uses `extra.results_metadata.__qopenbb_financial__` while preserving FRED's per-series entries and available vintage facts; advertised-route validation/response/unexpected failures use sanitized handlers and safe logging; FRED cache/in-flight acquisitions retain original retrieval timestamps through an opt-in provenance envelope while default raw callers remain compatible. These are designed behavior changes, not verified runtime claims.

Additional inspected sources were `providers/fred/openbb_fred/models/series.py`, `utils/rate_limiter.py`, `utils/cache.py`, core `api/exception_handlers.py`, `app/model/defaults.py`, `app/static/container.py` and API `router/commands.py`. Cache-key versioning avoids inventing retrieval times for legacy entries; the installed runtime keeps its existing disk-cache-off setting. Required response metadata is not injected through optional output callbacks. No application/source package changes were made.

Controller checks confirm 44/44 criterion mapping, populated boundaries/file plan and valid local document links/metadata. Owner design approval on 2026-10-28 opened task generation. Tasks must include the existing inventory/checker foundation, scoped source ownership, independent review and real-provider/browser acceptance without multiplying test harnesses.

## Task-plan review gate

The first financial-input batch contains 26 executable tasks in six groups. A fresh independent Astra sanity review passed after one repair: task 5.1 now installs and identifies the candidate fork before service integration tests; final root pins and catalogs are promoted together later. The [review](task-plan-review.md) records the bounded gate.

Controller checks found an acyclic dependency graph, explicit done/boundary/complexity criteria on every task, and all 44 requirement IDs mapped across executable tasks and explicitly deferred family obligations. This is planning coverage, not implemented coverage. The owner must approve [tasks](tasks.md) before implementation. Shared contracts precede up to two disjoint implementation lanes, with independent review and serialized joins. No tests, live-provider requests or image builds were run for this documentation change.
