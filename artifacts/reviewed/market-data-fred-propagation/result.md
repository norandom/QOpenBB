# FRED acquisition propagation

Task 3.2 is frozen for independent review. `fred_get(with_provenance=True)` returns original acquisition time and network/memory/disk/coalesced state. Default calls retain raw payloads. Cache bypass neither reads nor writes nor joins flights. Cancellation of one waiter cannot cancel the shared flight.

Requirements: 4.1, 7.4, 7.5. Design: FRED compatibility and acquisition provenance.

The accepted acquisition/disk serialization contract is unchanged. Memory and in-flight keys now use the `fred-acquisition:1:` namespace with credential redaction. Successful network receipt is stamped before persistence; disk promotion preserves the original timestamp. Existing retry/backoff and request kwargs remain intact.

Evidence:
- `red.txt`: 5 failed, 1 passed before implementation.
- `green.txt`: 30 passed in 34.74s across propagation, acquisition and installed FRED regression tests.
- `ruff.txt`: explicit provider configuration, no-fix check passed.
- `size.json`: whole maintained file 322 physical lines, 179 logical units, largest callable 19; measured by repository checker with CPython 3.13.15.

Validation command:
```sh
PYTHONPATH="$PWD/vendor/data-api/openbb_platform/core:$PWD/vendor/data-api/openbb_platform/providers/fred" verification/provider/.venv/bin/python -m pytest -c verification/provider/pyproject.toml tests/providers/test_fred_propagation.py tests/providers/test_fred_acquisition.py tests/providers/test_fred.py -n0 --maxprocesses=2
verification/provider/.venv/bin/ruff check --config vendor/data-api/ruff.toml --no-fix vendor/data-api/openbb_platform/providers/fred/openbb_fred/utils/rate_limiter.py
PYTHONPATH="$PWD" verification/provider/.venv/bin/python artifacts/market-data-fred-propagation/measure.py
```

Tests use offline boundary fixtures and disposable disk storage. No live-provider, build or installed application acceptance is claimed. The existing aiohttp subclass deprecation warning persists. Parent owns independent review, acceptance, inventory/breadth updates and commits. Pre-existing renderer edits and concurrent FMP edits are excluded.
