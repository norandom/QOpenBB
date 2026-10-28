# FMP transport review candidate

Task 2.1 is ready for independent review. No provider activation or live calls were performed. Source edits are frozen in the three FMP utility files; root changes are confined to tests/providers/test_fmp_transport.py. Other working-tree changes were preserved.

## Contract

Default calls retain raw payloads and legacy safe FMP exception classes/body/status dispatch. Opt-in with_provenance=True on get_data/get_data_many/get_data_one returns FMPAcquisition(payload, retrieved_at), timestamped after successful network receipt. Failures in this mode are exact accepted-core FinancialError instances. Error classification remains in errors.py; Retry-After uses core bounded parsing. No new wrapper traversal protocol is introduced.

get_data_urls accepts 1-20 nonempty URL strings, validates the entire batch before I/O, requests serially, stops at first failure, and performs no retries. Default output retains upstream flattened-list shape; opt-in output retains each acquisition envelope. Existing core request timeout behavior is retained (default ten seconds).

create_url encodes query/key values and excludes query-supplied apikey overrides. validate_statement_query freezes new-adapter single-symbol annual/quarterly semantics, normalizes quarterly to quarter, and bounds integer limits at 1-1000. Explicit allow_zero preserves existing income semantics when downstream adapters opt in. Existing profile/income code was not edited.

## Evidence

- red.log: 15 failed before implementation, including absent acquisition/bounds API, unsafe URL encoding and missing categorized attributes.
- green.log: 62 passed, one existing aiohttp inheritance deprecation warning.
- ruff.log: All checks passed with explicit owning-FMP config and --no-fix.
- size.json: project-syntax-units-v1 whole-file counts helpers 340 physical/163 logical/max function27; errors96/32/12; definitions27/7/4. Parent owns combined scope gate.
- git diff --check passed for fork changes and exclusive root test.

Exact focused command (WSL Debian, repository root):

```sh
PYTHONPATH=/mnt/d/Source/QOpenBB/vendor/data-api/openbb_platform/core:/mnt/d/Source/QOpenBB/vendor/data-api/openbb_platform/providers/fmp verification/provider/.venv/bin/python -m pytest -c verification/provider/pyproject.toml tests/providers/test_fmp_transport.py tests/providers/test_profile.py tests/providers/test_income.py tests/providers/test_errors.py -n0 --maxprocesses=2
verification/provider/.venv/bin/ruff check --config vendor/data-api/openbb_platform/providers/fmp/pyproject.toml --no-fix vendor/data-api/openbb_platform/providers/fmp/openbb_fmp/utils/helpers.py vendor/data-api/openbb_platform/providers/fmp/openbb_fmp/utils/errors.py vendor/data-api/openbb_platform/providers/fmp/openbb_fmp/utils/definitions.py
PYTHONPATH=. pipeline/.venv/bin/python artifacts/market-data-fmp-transport/measure.py
```

## Frozen SHA256

- helpers.py: 204E5064E3A63302A7B63D0E7444E74B861423ECBBA61D29480AE99FE6101699
- errors.py: 307045FF328A871138C755AF46C5C3C5E9C91C876EF91703FB652DD2EA8F5570
- definitions.py: F3DF8215D927DAB0B0CF034761D151D5D2E692433721BCD018CCA56507B973CD
- test_fmp_transport.py: F3F08A3EEAB05451C4D80DE1477810C58556D3EFA02135E93F13B6F600658303

Requirements 2.4,2.5,7.1,7.2,7.3,7.4 checked against approved design sections Provider fetchers and first-batch surface, FRED compatibility and acquisition provenance, and Financial failures and HTTP compatibility. Dataset-level result truncation/completeness remains the downstream adapter responsibility. Existing historical/transcript utility functions are unactivated legacy code and were preserved; this task removes the specifically identified multi-request bypass.