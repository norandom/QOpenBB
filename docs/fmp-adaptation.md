# FMP discovery adaptation

Task 3.1 restores installed FMP discovery against the selected core candidate. Financial results, error semantics and live account access remain unverified until tasks 3.2-3.4 and later integration gates pass. The discovery test makes no provider requests and requires no credentials.

The owned data fork restores `openbb_platform/providers/fmp` from the retained FMP 1.6.1 source archive. Its `provenance.json` records the archive URL and SHA256, exact unchanged member hashes, the selected API base and maintained adaptations. Release metadata declares AGPL-3.0-only; the archive omits standalone license and notice files. `LICENSE` retains the historical upstream AGPL text already recorded in [license provenance](../sources/notices.json), without asserting a new license.

The local version is `1.6.1+qopenbb.1`. Packaging replaces the released `openbb-core ^1.6.10` constraint with the selected `2.0.1` candidate and pins Hatchling `1.32.4`. This permits discovery testing; it does not establish route or fetcher compatibility. The entry point remains `openbb_fmp:fmp_provider`. Registration exposes only `EquityInfo` and `IncomeStatement`. Models and response helpers remain exact archive imports, including their existing financial mappings and error handling. The maintained definitions module retains only the statement-period literal required by the income model.

For a fresh checkout, first restore the source archive to the ignored `artifact.retained_path` recorded in `vendor/data-api/openbb_platform/providers/fmp/provenance.json`. Download only its recorded `artifact.url` and compare SHA256 with `artifact.sha256` before running provenance tests. The archive is an explicit test prerequisite; it is not committed or fetched by pytest.

The isolated `verification/provider` project locks Python `3.13.15`, the owned core, equity/economy routers and FRED, alongside the restored FMP package. Local uv sources prevent substitution with registry packages. It omits the omnibus `openbb` distribution and unrelated provider packages. Follow [protected tool setup](development.md), then run from the repository root in WSL:

```sh
uv sync --project verification/provider --locked --python 3.13.15
uv run --project verification/provider --locked python -m pytest \
  -c verification/provider/pyproject.toml tests/providers/test_discovery.py -n0
```

Run these through Safe Chain 1.5.25 shims with the default 48-hour package-age protection. The project also fixes the resolver cutoff at `2026-10-14T00:00:00Z`; frozen sync retains that setting. Discovery checks installed metadata, the real core extension loader, the two registrations, installed candidate versions and exact retained-source/license hashes. It does not fetch financial data, invoke shared routes or establish dashboard readiness. A discovery failure, mismatched hash or unexpected registration disproves this task's readiness claim.

On 2026-10-16, protected resolution and frozen restoration completed under WSL with 55 locked packages. Both discovery/provenance tests passed against a task-owned native Linux mirror; all 640 copied source files matched the owned checkout by SHA256. The run emitted one upstream aiohttp inheritance deprecation warning. Ignored evidence is retained in `artifacts/task-3.1/protected-install.log`, `mirror-sources.json` and the earlier failing `red.log`. This is WSL packaging evidence; Linux deployment, route fixtures and live FMP remain separate acceptance gates.
