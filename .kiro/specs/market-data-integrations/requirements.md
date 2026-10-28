# Requirements Document

## Project Description (Input)
Financial analysts need broad FMP, yfinance, FRED and later provider coverage behind consistent named-instrument, date, unit and provenance contracts. Current adapters cover a small subset. Expand horizontal data access independently of prototype deployment. Existing installed adapters remain part of the baseline.

## Requirements
The next bounded discovery slice supplies the [investment-analysis contract](../analyst-workspace/investment-analysis-contract.md): statements, peers/multiples, FMP DCF/model inputs, macro capital-cost inputs and later estimates/news/transcripts. Verify plan entitlement and actual response semantics before promising widgets. Preserve provider-reported values and provenance; analyst scenarios and valuation presentation belong to analyst-workspace. Detailed adapter requirements and tasks remain open.

## Owned OpenBB platform and provider reuse

Owner direction, 2026-10-28: maintain the reusable data platform and provider implementations in our own Git repositories. Continued operation and development must not depend on upstream support. Reuse the OpenBB Python platform used from notebooks; Jupyter hosting is not required.

- MD-F1: The maintained data platform shall live in [norandom/openbb-data-api](https://github.com/norandom/openbb-data-api), with adapted providers committed alongside it. QOpenBB shall build from exact owned-fork revisions in `sources.lock.json`; provider functionality shall not depend on uncommitted local patches.
- MD-F2: The integration shall reuse OpenBB standard query/data models, `Provider`, `Fetcher`, query execution, routers and `OBBject`. Extend those mechanisms where a demonstrated gap requires it; do not introduce a parallel registry, query framework or ORM solely to wrap them.
- MD-F3: When restoring legacy FMP or yfinance capabilities, retain upstream provenance, history and applicable notices, and adapt the implementations to the pinned core and current provider API. Old provider packages shall not be treated as install-compatible with core 2.x without verification. Current FMP coverage is profile/income only.
- MD-F4: Widgets and later AI tools shall consume the same maintained command/API schemas and financial metadata. Future database providers shall implement appropriate dataset contracts through the provider extension mechanism; they shall not require consumer-specific data access. Database implementation remains deferred to custom-data-source.
- MD-F5: Provider selection shall be explicit or follow a documented configured default. Any future fallback must expose actual provenance and reject incompatible financial semantics; matching field names alone shall not establish interchangeability.

Git verification on 2026-10-28: the owned data API repository is a GitHub fork; remote branch `qopenbb/baseline`, local checkout and the source lock all identify `cab81b16bb9ef49272a6f3b0bf04cf9f34bde0ba`. The checkout is clean. The standard model, provider, fetcher, query and result machinery is present in that source. These facts establish source ownership and reuse availability, not complete FMP/yfinance coverage or a completed database adapter.


