# Periodic query provenance: bounded repair design

## Overview

Expose the existing `ttm=exclude` selection in Metrics and Ratios effective-query metadata. Both routes already validate this selection and reject TTM acquisition; their metadata currently omits it. The repair lets widgets and programmatic consumers inspect the same actual query without changing financial values or adding a calculation.

This amendment uses the already approved market-data-integrations requirements 4.1, 4.2, 4.3 and 6.1-6.3. Requirements 4.4-4.7 and 7.1-7.2 remain constraints. The existing broader design and completed initial batch remain accepted; this production repair needs its own design/task approval. No new requirements phase or service is proposed.

## Boundary Commitments

### This Spec Owns

The public effective-query contract for the two installed FMP periodic routes, its native/core validation, and the corresponding source/catalog acceptance. Success means default and explicit periodic-only queries both retain `ttm: exclude` alongside their actual symbol, period and limit.

### Out of Boundary

No TTM fetching/synthesis, new endpoints, financial formulas, date alignment, currency inference, provider fallback, DCF restoration, financial-model repository, dashboard, AI or Excel work. Actual duration/YTD/restatement and valuation/share/claim conventions remain unresolved where the source does not establish them.

The three accounting-field omissions reported by IA-A came from test-evidence sanitization, not provider annotations. Their correction belongs to the existing analyst-workspace verification task; do not modify Balance or Cash field declarations for this repair.

### Allowed Dependencies

Reuse the owned OpenBB query/data models, `FinancialResultMetadata`, FMP metadata emitters, native API and existing catalog/release tools. Keep the locked Python environment, uv/Safe Chain, and current dependencies. No new package or abstraction is needed.

### Revalidation Triggers

Changes to query choices/defaults, the safe-public-query validator, provider emitters, source pins or generated metadata contracts require affected checks. House/UI changes require their own contracts. Historical acceptance remains tied to its original source and acquisition time.

## Source findings and synthesis

At API revision `28423762e8cc3faae978e770899834b41e7cde99`, `FinancialResultMetadata` permits a bounded public-query key set that excludes `ttm`. Metrics and Ratios each construct `effective_query` with symbol, period and limit only. Both query models already restrict `ttm` to `Literal["exclude"]`, with that default; `include`, `only` and period `ttm` are rejected before transport.

Reuse the existing metadata contract and emit the validated query value. Do not copy a new default table into the service/catalog or create another metadata adapter. No external API change or new library needs research: the source and accepted IA-A receipts establish this local omission.

## Contract and compatibility

- Core accepts `ttm` as another safe public effective-query key. Existing key/value sanitization and credential rejection remain active; core does not impose FMP-only allowed values on other providers.
- The two FMP emitters include the validated `query.ttm`, including when the caller omitted it and the model supplied the default. Do not merely echo raw request arguments.
- Preserve both routes, public field names, result ordering, values, units, bounds, defaults, typed errors and upstream requests. No TTM endpoint is selected and no rows are derived.
- Keep `extra.results_metadata.__qopenbb_financial__`, the metadata shape and schema-version 1. The effective-query dictionary gains one entry. Generated query definitions already expose the selector; check them rather than introducing a second definition.
- Existing consumers that treat the public query dictionary generically remain compatible. An older Python `FinancialResultMetadata` validator with the old key allowlist rejects this added key: it must be updated to the matching reviewed core fork revision. Ship the core/provider revision together, document that migration, and do not claim compatibility for the older strict validator. No dual response format or new versioning framework is introduced.

## File Structure Plan

Paths under `openbb_platform/` belong to the owned data-api fork. Root verification/catalog files belong to QOpenBB.

| Paths | Responsibility |
| --- | --- |
| `vendor/data-api/openbb_platform/core/openbb_core/provider/standard_models/financial_metadata.py` | Admit the additional public query key without weakening value/secret validation |
| `vendor/data-api/openbb_platform/providers/fmp/openbb_fmp/models/key_metrics.py` | Emit the validated periodic-only selector |
| `vendor/data-api/openbb_platform/providers/fmp/openbb_fmp/models/financial_ratios.py` | Emit the validated periodic-only selector |
| `tests/providers/test_financial_metadata.py` | Public key round-trip and existing sensitive-key/value rejection |
| `tests/providers/test_fmp_key_metrics.py`, `tests/providers/test_fmp_financial_ratios.py` | Default/explicit selector, annual/quarter modes, unchanged source requests/results and unsupported-mode rejection |
| `tests/providers/test_service_financial.py` | Actual mounted metadata and Python/native value consistency for both routes |
| `tests/providers/test_live_financial.py` | Remove only the TTM metadata exemption and obsolete finding for newly executed repaired-source cases |
| `sources.lock.json`, reviewed fork inventory input and generated `contracts/` provenance/schema artifacts | Controller-owned source identity and consumer consistency join using existing tools |
| `docs/provider-coverage.md`, owning spec status, `.kiro/breadth.toml`, README and one reviewed milestone receipt | Actual source/live/release evidence and remaining limits |

The production baseline physical sizes are 193/140/141 lines respectively. All three modified files must pass 400 physical lines, 300 logical units and 50 per function using the existing checker and explicit source manifests. Tests/generated contracts/docs are excluded; no new exception or checker is needed. Preserve unrelated catalog-renderer/inventory edits and use clean reviewed generator inputs when regenerating contracts.

## Verification and delivery

1. Before edits, establish the exact core/provider source and installed-package identity. Existing verification installs are copied package contents, so changes in the fork must be installed with the existing protected/locked toolchain before testing the repaired behavior; old-package test results are not acceptance.
2. Extend existing focused tests: default and explicit `exclude`, each annual/quarter mode, exact unchanged result values/upstream query routing, and rejection of `include`/`only`/period `ttm`. Core tests retain unsafe keys and credential-bearing value rejection. Mounted service tests assert the selector reaches the native result envelope.
3. The existing canonical provider command is `env PYTHONPATH=services/data-api verification/provider/.venv/bin/python -m pytest -c verification/provider/pyproject.toml <selected files> -n0 --maxprocesses=2`. Task generation freezes actual selections and installation/source checks. Do not invent another harness.
4. At the join, regenerate/validate the affected catalog with accepted generator inputs, preserve widget IDs and schemas unrelated to the selector, and run the existing complexity command from `docs/complexity.md` with actual fork base/head or explicit manifests. Never reuse historical example heads as current evidence.
5. Confirm the metadata with at most four newly scoped FMP calls: Metrics and Ratios, default annual and explicit quarterly selection. Preserve source values and distinguish newly repaired metadata from old receipts. Do not repeat the 49-call IA-A assessment, overwrite its hashes or mark unrelated compatibility findings resolved.
6. This production change uses the normal milestone image pipeline once after accepted source/catalog/integration checks. Dagger builds images only; existing portable publication and pull verification remain. Retain the accepted Workspace source pin and current UX. Use the existing packaged API/consumer smoke required by the release flow; no new screenshot matrix or browser framework is warranted for metadata-only behavior.

## Requirements traceability

| Approved requirements | Observable acceptance |
| --- | --- |
| 4.1 | Effective query retains the validated default/explicit periodic-only selector |
| 4.2, 4.3 | Existing units/origins/period labels remain unchanged; periodic selection is not advertised as TTM or fiscal comparability |
| 6.1 | Installed query choices/defaults agree with emitted metadata and generated discovery |
| 6.2 | Python and native/widget-facing queries retain matching values and selector provenance |
| 6.3 | Existing dictionary consumers remain usable; older strict-model migration is explicit and checked |
| 4.4-4.7, 7.1-7.2 | No transformation, zero substitution, vintage/valuation claim, unsafe error or credential exposure is introduced |

## Execution boundary

Keep the core allowance and both emitters in one small implementation unit, followed by an independently reviewed source/catalog join and one milestone release. Native API/consumer checks depend on that shared contract. Parallel work is useful for independent review or documentation, not concurrent edits to the same metadata seam. Task generation must retain per-task commits and the actual complexity gate. This design does not authorize implementation before design and task approval.
