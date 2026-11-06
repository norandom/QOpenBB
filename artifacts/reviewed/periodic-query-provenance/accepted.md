# Periodic query provenance

Metrics and Ratios now expose their validated `ttm: exclude` selection, including defaulted requests. Source/native checks and four fresh FMP comparisons passed. Image and deployment acceptance remain open; this record does not establish IA-B analytical readiness.

- [Approved repair and task state](../../../.kiro/specs/market-data-integrations/periodic-query-provenance-tasks.md)
- [Consumer migration](../../../docs/provider-coverage.md#periodic-query-metadata-compatibility)
- [Provider coverage identities](../../../docs/reference/provider-coverage.json)

## Source and verification

Data API commit `2e60c0a7aff039eda5f14a9d494beaec822fb9c4` changes three production lines: the core public-query allowlist and the Metrics/Ratios metadata emitters. Installed core/provider copies matched all three committed module hashes before testing. The older strict Python validator requires the matching updated core/provider pair; metadata remains schema version 1. This adds no TTM acquisition or calculation.

The focused suite reproduced 19 failures before the repair and then passed 125 tests. Independent Astra source review passed, including four fresh identity/schema/empty-result checks. Native/offline integration passed 73 tests with 23 live cases deselected. An initial integration run exposed two test assumptions: stale historical adapter proofs must remain stale, and native responses omit unset/null fields that Python models retain. The corrected assertions preserve both distinctions. The existing aiohttp deprecation warning remains.

The canonical command is `verification/provider/.venv/bin/python -m pytest -c verification/provider/pyproject.toml`, with `PYTHONPATH=services/data-api`, `-n0` and `--maxprocesses=2`. The focused selection uses the metadata, metrics and ratios test modules; native integration uses service-financial and live-financial with `-m 'not live'`. Both accepted runs exited 0. Source/native schema checked through the accepted clean generator reports no route changes or affected consumers; this is not canonical image-backed catalog generation.

Whole-file physical/logical/maximum-function sizes are 193/115/9, 140/56/10 and 141/59/10. Owning-fork lint and the combined source-pin scope gate pass with no errors or violations. The first pin-join scope attempt rejected an old manifest base against the promoted inventory; the final clean committed-snapshot declaration rechecks maintained controller files and validates the promoted fork identities. The unchanged three fork-file measurements are retained from task 2 and joined by their identical committed/installed hashes. Existing unrelated renderer/inventory work was excluded.

## Four real-provider observations, 2026-11-06

One serial run completed four cases in 34.18 seconds. Each sent one MSFT request with limit 1, returned HTTP 200, preserved source/API values and emitted the validated periodic selection. Run counters are exactly 1 through 4. No retries, FRED calls or repeated IA-A assessment occurred.

| Dataset | Caller selection | Emitted period / TTM | Original receipt SHA256 |
| --- | --- | --- | --- |
| Metrics | Period and TTM omitted | annual / exclude | `95b1832f111c0a358637174c104075028c4edbef3cd822ab76962174e43809f8` |
| Metrics | quarter, exclude | quarter / exclude | `6424d7136736673301ecd804fb8c5ebcd57ba3f7651c901870c186ac02ec48fc` |
| Ratios | Period and TTM omitted | annual / exclude | `6a2aa88f95cb1f5c27dcec10cf765787a8bacf80a48849585821be37969f85dc` |
| Ratios | quarter, exclude | quarter / exclude | `0234c0e16b9e0cc691b17bea484b2f8dda97c531c9523d83828140bb5fc9c885` |

Local original run: `artifacts/periodic-query-provenance/live-20261106T135844Z`. Execution-record SHA256: `6a0c3d4968ea74f03b3e14ed6120934de0c27e808ab7fb46d27d53a0c4f3267d`; pytest-log SHA256: `ea5e4fd6c3a0c25a3965d2279da0b1b8505c27dc8d6c6553c0f355fc335d5abd`. The record identifies controller base `70853da2ac5138a1ce6292c463d6e07243b4d9d4`, the exact then-uncommitted test-file hashes, data commit and four selected node IDs. Raw receipts/logs remain local. The two renewed real-data proofs identify only these adapters and their unchanged contract hashes; all other coverage and historical IA-A receipts remain unchanged.

## Delivery boundary

Native/source acceptance is distinct from image publication, packaged consumer verification and owner-server deployment. No new image is accepted by this record yet. Actual duration/YTD, restatement, valuation/share/claim conventions and both false IA-B readiness flags remain unresolved. The repair changes query provenance, not financial conclusions.

Independent Astra integration review approved the source/native join on 2026-11-06, with two fresh offline checks and an audit of all four live receipts, the two renewed proofs and 50 unchanged historical receipt hashes. Original review SHA256: `f4b5d9379f42eebbb7b856a27441757a7f1ad08db16eca97c6ca95eae55e5df3`. Image delivery remains the next acceptance gate.
