# FMP discovery adaptation

Task 3.1 restores installed FMP discovery against the selected core candidate. Deterministic financial and failure fixtures are recorded below; live account access remains unverified. The discovery test makes no provider requests and requires no credentials.

The owned data fork restores `openbb_platform/providers/fmp` from the retained FMP 1.6.1 source archive. Its `provenance.json` records the archive URL and SHA256, exact unchanged member hashes, the selected API base and maintained adaptations. Release metadata declares AGPL-3.0-only; the archive omits standalone license and notice files. `LICENSE` retains the historical upstream AGPL text already recorded in [license provenance](../sources/notices.json), without asserting a new license.

The local version is `1.6.1+qopenbb.1`. Packaging replaces the released `openbb-core ^1.6.10` constraint with the selected `2.0.1` candidate and pins Hatchling `1.32.4`. This permits discovery testing; it does not establish route or fetcher compatibility. The entry point remains `openbb_fmp:fmp_provider`. Registration exposes only `EquityInfo` and `IncomeStatement`. The response helper is maintained under task 3.4, with its original archive hash retained in `adapted_files`. The income model is maintained under task 3.3 with its original archive hash retained in `adapted_files`. The profile model is maintained under task 3.2, with its original archive hash retained in `adapted_files`. The maintained definitions module retains only the statement-period literal required by the income model.

For a fresh checkout, first restore the source archive to the ignored `artifact.retained_path` recorded in `vendor/data-api/openbb_platform/providers/fmp/provenance.json`. Download only its recorded `artifact.url` and compare SHA256 with `artifact.sha256` before running provenance tests. The archive is an explicit test prerequisite; it is not committed or fetched by pytest.

The isolated `verification/provider` project locks Python `3.13.15`, the owned core, equity/economy routers and FRED, alongside the restored FMP package. Local uv sources prevent substitution with registry packages. It omits the omnibus `openbb` distribution and unrelated provider packages. Follow [protected tool setup](development.md), then run from the repository root in WSL:

```sh
uv sync --project verification/provider --locked --python 3.13.15
uv run --project verification/provider --locked python -m pytest \
  -c verification/provider/pyproject.toml tests/providers/test_discovery.py -n0
```

Run these through Safe Chain 1.5.25 shims with the default 48-hour package-age protection. The project also fixes the resolver cutoff at `2026-10-14T00:00:00Z`; frozen sync retains that setting. Discovery checks installed metadata, the real core extension loader, the two registrations, installed candidate versions and exact retained-source/license hashes. It does not fetch financial data, invoke shared routes or establish dashboard readiness. A discovery failure, mismatched hash or unexpected registration disproves this task's readiness claim.

On 2026-10-16, protected resolution and frozen restoration completed under WSL with 55 locked packages. Both discovery/provenance tests passed against a task-owned native Linux mirror; all 640 copied source files matched the owned checkout by SHA256. The run emitted one upstream aiohttp inheritance deprecation warning. Ignored evidence is retained in `artifacts/task-3.1/protected-install.log`, `mirror-sources.json` and the earlier failing `red.log`. This is WSL packaging evidence; Linux deployment, route fixtures and live FMP remain separate acceptance gates.

## Profile fixture verification

Task 3.2 exercises the installed shared `/api/v1/equity/profile` route with `provider=fmp` and lower-case comma-separated symbols. A direct ASGI request passes through the real API, shared equity router, core query machinery and registered FMP fetcher. Only the provider network boundary and server settings reader are replaced. This proves route compatibility without installing another HTTP test client or contacting FMP. The server credential is a synthetic sentinel, never a live key.

The stable profile request uses URL-encoded `symbol` and `apikey` parameters. Symbol lists preserve order and punctuation while trimming surrounding whitespace. Fixtures verify company identity, USD currency, market capitalization, last price, average volume, dividend amount, price range, employee count and IPO date. Numeric source values are preserved; the range is split into low/high prices. Missing provider flags become nullable instead of failing validation, and empty currency remains null. The API may omit unset fields; it never substitutes zero for missing financial values. Transforming data leaves the provider input intact.

Run the focused checks from the protected locked provider environment:

```sh
python -m pytest -c verification/provider/pyproject.toml \
  tests/providers/test_profile.py tests/providers/test_discovery.py -n0
```

On 2026-10-16, the native WSL provider environment passed the profile fixtures with the temporary behavioral flag enabled and after its removal. Evidence is retained in `artifacts/task-3.2/`: `red.log`, `green-flag.log`, `green.log` and `source-sync.json`. The initial RED run returned HTTP 500 for null/missing flags and failed symbol normalization. A failing field/value assertion, credential leak, wrong request parameters or changed input fixture disproves this claim. Live account entitlement, deployment settings injection, income statements, provider error classification and Workspace comparison remain later gates.

## Annual income fixture verification

Task 3.3 verifies the installed `/api/v1/equity/fundamental/income` route for `provider=fmp`, annual periods and explicit limits. Fixtures preserve FY labels, reporting and filing dates, acceptance timestamps, USD currency, revenue, expenses, net income, earnings per share and share counts. Source amounts stay in their supplied units; explicit zeros and null values remain distinct. This is deterministic route evidence, not live entitlement or Workspace comparison evidence.

The maintained income fetcher trims surrounding single-symbol whitespace and URL-encodes query parameters. It retains the default limit of five when omitted and passes an explicit zero through because the selected core schema permits nonnegative limits. The historical `fillingDate` alias remains supported; the selected core also accepts stable `filingDate` through its camel-case field alias. No statement fields are calculated or filled. Tests also verify punctuation, non-mutating transformations and rejection of invalid periods and negative limits before network access.

On 2026-10-16, the native WSL environment passed 11 focused income, profile and discovery tests. The temporary flag produced a failing whitespace assertion when disabled; enabled and removed runs passed. Reproduce with the locked provider environment using `python -m pytest -c verification/provider/pyproject.toml tests/providers/test_income.py tests/providers/test_profile.py tests/providers/test_discovery.py -n0`. Evidence is in `artifacts/task-3.3/red.log`, `green-flag.log`, `green.log` and `source-sync.json`. A changed financial value, missing date, altered period, wrong request parameter or credential in the API output disproves this readiness claim. Shared error classification and live FMP access remain later gates.


## Failure and credential boundary

Task 3.4 preserves distinct FMP authentication, entitlement, throttling, invalid-parameter and missing-data outcomes through the installed profile and income routes. The helper classifies HTTP statuses first, then legacy HTTP-200 error envelopes. When a legacy error mentions both a reached limit and an upgrade, throttling takes precedence. Unknown provider errors remain upstream failures. Transport timeouts and connection failures have separate categories.

Error messages use fixed `FMP[category]` text. Provider error bodies, credential-bearing URLs and transport exception text are discarded before the shared API error handler logs or serializes them. Original unsafe transport and JSON-decoding exceptions are not chained into rendered tracebacks. Successful financial transformations remain covered by the profile and income regressions. The helper does not retry with another provider or supply fabricated observations.

The selected core maps authentication and entitlement exceptions to HTTP 502, other provider failures to HTTP 400, and missing data to HTTP 204 with an empty body. Category text distinguishes failures that share a status; the 204 status explicitly identifies absence. These are compatibility observations, not a proposed HTTP status redesign. No core exception handler changed.

On 2026-10-16, 40 deterministic checks passed in the native WSL provider environment: `tests/providers/test_errors.py`, `test_profile.py`, `test_income.py` and `test_discovery.py`. Failure checks exercise both real installed routes with a replaced provider network boundary, synthetic server credentials, protocol and legacy-payload failures, and timeout/connection failures. They assert no sentinel credential appears in responses, captured logs, console output or rendered transport tracebacks. The same command as the annual checks above reproduces them after adding `tests/providers/test_errors.py` to its file list.

Ignored evidence is retained in `artifacts/task-3.4/red.log`, `green-flag.log`, `green.log` and `source-sync.json`. The temporary flag produced 21 failing checks and three passing checks when disabled; enabled checks passed before removal. The final run includes five additional transport/JSON regression checks and the two discovery checks. Source, native mirror and installed Python files match by SHA256. A wrong category, exposed sentinel, substituted result or changed financial fixture disproves this readiness claim. Live FMP credentials, entitlement and deployment remain unverified; unregistered historical/transcript helpers are outside these route fixtures.


Independent review found that bare `apikey` detection misclassified credential URLs echoed in otherwise meaningful errors. The repair matches explicit authentication failure phrases and excludes echoed HTTP URLs from semantic classification. Six installed-route regressions first failed, then passed for entitlement, invalid parameters and missing data containing synthetic credential URLs. The full repaired suite passed 46 checks; evidence is in `artifacts/task-3.4/review-red.log` and `review-green.log`.
