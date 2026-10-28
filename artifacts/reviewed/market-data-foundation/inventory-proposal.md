# Batch 1 scope proposal

Controller must add each path before its production implementation is accepted. Existing mappings remain intact. Caps: 400 physical lines, 300 logical units/file, 50/function; tests and generated output are excluded.

Data fork (`openbb_platform/` prefix):
- core/openbb_core/provider/standard_models/financial_metadata.py
- core/openbb_core/provider/utils/financial_errors.py
- core/openbb_core/provider/utils/financial_validation.py
- core/openbb_core/provider/standard_models/enterprise_values.py
- providers/fmp/openbb_fmp/models/{equity_search,balance_sheet,cash_flow,equity_historical,equity_peers,key_metrics,financial_ratios,enterprise_values,balance_sheet_data,cash_flow_data}.py
- providers/fred/openbb_fred/utils/{cache,acquisition}.py
- extensions/equity/openbb_equity/fundamental/{fundamental_router,enterprise_router}.py

Root repository:
- services/data-api/qopenbb_data/{financial_catalog,financial_errors,financial_openapi,financial_policy}.py
- pipeline/qopenbb_ci/catalog_financial.py

Existing planned modified paths already mapped: FMP profile/income/helpers/errors/definitions/provider, FRED series/rate_limiter, root app/config/catalog/catalog_runtime/catalog_upstream. Existing exclusions for notices/provenance and generated contracts remain applicable. Review docs/reference/provider-coverage.json as maintained data: add explicit ownership rather than broad documentation exclusion. Add service dependency manifest/lock only at serialized join. Brace notation is proposal shorthand, never checker input.
