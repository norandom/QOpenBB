# Market data foundation baseline, 2026-10-28

The locked provider environment is restored and baseline profile/income behavior is characterized without live-provider calls. FRED's existing fixture import is repaired; check the adjacent GREEN log for its final outcome. This evidence does not establish entitlement or live coverage.

## Source and scope

Root HEAD at start: cafca4a46451dd61e786c48f781be901263aea64. Data fork: cab81b16bb9ef49272a6f3b0bf04cf9f34bde0ba. Workspace: dfda735c527663dd7ecc2f80af18e25843f575af. Both match source locks. Initial root dirty paths: complexity-budgets.json, market-data spec.json, catalog_cli.py, new catalog_renderers.py and test_renderers.py; preserved. Data fork tracked/untracked status was empty. Workspace has historical untracked helper/test/generated paths retained in workspace-status.txt, including financial TS files; they are not this batch. Empty Workspace manifest declares no batch changes and must not be interpreted as a clean complete checkout audit. Parent owns reconciliation before shared acceptance.

Historical recovery: FMP 59c7c7eff44^:openbb_platform/providers/fmp/; yfinance 7a9ad1ecf10^:openbb_platform/providers/yfinance/. These are recovery points, not install targets. Existing FMP provenance retains archive SHA256 5f6f27af6283075912df42f373c45ed37bc6970097342ed73110fb6101be5517 and original notices. contracts/provenance.json records generator revision 49cc413e6ab67eaa0444e07485b0f9243c786f7b and data image sha256:5c23441a269126ebeee5d315caa922993c638d2527d4789684f32d6270cdc7fb; current source and historical generation are distinct.

## Commands and results

Run in WSL at /mnt/d/Source/QOpenBB. Protected restoration: prepend artifacts/task-1.2/{safe-chain/shims,safe-chain/bin,node-v24.22.0-linux-x64/bin} to PATH, set UV_PYTHON_INSTALL_DIR=$PWD/artifacts/task-1.2/python, then `uv safe-chain-verify` and `uv sync --project verification/provider --locked --python 3.13.15`. Exit 0; protection OK; 52 packages installed. Locked Python3.13.15, core2.0.1, equity/economy/FRED2.0.0, FMP1.6.1+qopenbb.1, Pydantic2.14.1, FastAPI0.143.0. No lock edits. Initial absent venv required restoration; cross-filesystem hardlink warning used ordinary copy.

`pipeline/.venv/bin/python -m pytest -c pipeline/pyproject.toml tests/quality/test_scope.py tests/quality/test_combined.py -n0 --maxprocesses=2`: exit0, 26 passed,17.32s. Existing test_missing_mapping_and_syntax_errors_fail injects missing maintained path; no replacement checker.

`verification/provider/.venv/bin/python -m pytest -c verification/provider/pyproject.toml tests/providers/test_profile.py tests/providers/test_income.py tests/providers/test_fred.py -n0 --maxprocesses=2`: exit1,9 passed,5 FRED fixture setup errors,70.30s. Missing packaged catalog was caused by FRED omitting existing packaged_catalog autouse fixture import. RED log provider-tests.log; one-line import fix only. Affected rerun fred-green.log.

Profile checks preserve provider/symbol/name/currency/financial values and nulls, multi-symbol uppercase normalization, nonmutation and EmptyDataError. Income preserves dates/fiscal periods/currency/aliases/nulls and accepted dates. Its default5 remains; limit0 is forwarded as zero and an empty provider fixture raises EmptyDataError. This is fixture semantics, not an assertion that a live provider always returns empty for zero. FRED checks GDP wide rows, missing value as null and legacy GDP frequency/units/seasonality metadata, plus sanitized failure paths.

`PATH=$PWD/artifacts/task-1.2/node-v24.22.0-linux-x64/bin:$PATH pipeline/.venv/bin/python -m tools.quality.complexity --check --changes workspace=artifacts/market-data-foundation/workspace-changes.json --changes data_api=artifacts/market-data-foundation/data_api-changes.json --output artifacts/market-data-foundation/complexity.json`: see JSON/log. Initial invocation before manifests existed exited2 and was corrected after manifests existed; no production gate was reported passing from that attempt.

## Next worker invocation

Local uv path dependencies are installed snapshots. Prefix source roots explicitly for changes: `PYTHONPATH=$PWD/vendor/data-api/openbb_platform/core verification/provider/.venv/bin/python -m pytest -c verification/provider/pyproject.toml <focused-test> -n0 --maxprocesses=2`. Add FMP/FRED source roots when those workers change providers. No concurrent reinstall required. Root services are loaded by existing test runtime fixture. Update actual change manifest entries after fork edits; empty foundation scope is not reusable for implementation. See inventory-proposal.md; controller owns maintained inventory updates.

Core steering product.md,tech.md,structure.md were absent; available complexity/testing/ci/delegation/documentation policies applied. Test-only fixture import is exempt from production caps. No build, live call, publication or task-checkbox edit occurred.

Final focused FRED rerun: exit0,5 passed,1 existing warning,27.74s. Combined complexity completed measurement and exited1 on pre-existing violations (see JSON); this is not a passing production acceptance gate. No production code was changed in this task.

Exact affected GREEN command (WSL repository root, no PYTHONPATH override used for this unchanged installed-provider baseline): `verification/provider/.venv/bin/python -m pytest -c verification/provider/pyproject.toml tests/providers/test_fred.py -n0 --maxprocesses=2 > artifacts/market-data-foundation/fred-green.log 2>&1`. Exit0;5 passed,1 existing warning,27.74s. Controller compacted inventory formatting to397 physical lines without semantic changes; a fresh combined checker run replaces the earlier414-line failing report. No provider rerun was needed for this configuration-only correction.

Fresh final combined checker after controller formatting correction: exit0; combined_acceptance=passed, zero errors and zero violations. The checker command is exactly the portable invocation above, with the two explicit foundation manifests. This supersedes the earlier414-line inventory failure; it does not certify excluded unrelated Workspace untracked files or future production changes.
