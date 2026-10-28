# FRED acquisition storage task 3.1

Ready for independent review. Sixteen offline checks pass against source overrides; owning-fork Ruff passes with its explicit configuration and `--no-fix`. Rate-limiter propagation remains task 3.2.

The acquisition envelope requires an aware retrieval timestamp and normalizes the same instant to UTC. Disk records and keys use version 1. Raw callers retain payload results, while provenance callers receive the original acquisition time and disk state. Unknown raw timestamps, legacy keys and malformed provenance are misses; cache reads never manufacture a fresh retrieval time. Legacy and unrelated records remain untouched. Disk-cache-off never opens storage; installed runtime configuration is unchanged.

Requirements checked: 4.1, 6.3, 7.5. Design checked: FRED compatibility and acquisition provenance.

## Evidence

- `red.txt`: missing acquisition module at collection, before implementation.
- `green.txt`: initial 10 checks pass.
- `final-tests.txt`: final 16 checks pass in 19.84 seconds; one existing aiohttp deprecation warning.
- `ruff.txt`: all checks passed.
- `size.json`: whole-file acquisition 48 physical / 25 logical / 7 maximum function; cache 255 / 79 / 10. Limits are 400 / 300 / 50.

Commands ran under WSL Debian from `/mnt/d/Source/QOpenBB`:

```sh
PYTHONPATH="$PWD/vendor/data-api/openbb_platform/core:$PWD/vendor/data-api/openbb_platform/providers/fred" verification/provider/.venv/bin/python -m pytest -c verification/provider/pyproject.toml tests/providers/test_fred_acquisition.py -n0 --maxprocesses=2
verification/provider/.venv/bin/ruff check --config vendor/data-api/ruff.toml --no-fix vendor/data-api/openbb_platform/providers/fred/openbb_fred/utils/acquisition.py vendor/data-api/openbb_platform/providers/fred/openbb_fred/utils/cache.py
verification/provider/.venv/bin/python artifacts/market-data-fred-acquisition/measure.py
```

Frozen SHA256 identities:

| File | SHA256 |
| --- | --- |
| acquisition.py | b0d5aa930c3862631ef8ec853e73af2f786144ad80a74f82fc09d3b21a817834 |
| cache.py | c9e39b7e92d7d54ddc94664cb6cce2af02758fda162e20a636adad781af37994 |
| test_fred_acquisition.py | b4bf8eefd3f7cb10876da06e323aabf93d444c1fc87e805d9ac8842a3ded75b6 |

No live provider requests ran. Parent owns the joined complexity gate and regression gate. Core steering product.md, tech.md and structure.md do not exist in the checkout; the task-specific steering files and approved spec were read.
