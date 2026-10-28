# Daily historical-price adapter review

The restored FMP daily-history model is frozen for independent review. Registration, installed-route acceptance, live entitlement and source-pin promotion remain controller-owned work.

## Status Report
- STATUS: READY_FOR_REVIEW

## Scope and semantics

Task 2.6 restores `openbb_platform/providers/fmp/openbb_fmp/models/equity_historical.py` from retained model responsibility inspected at data-fork commit `2e3d8ef6b25`. It replaces the legacy multi-request helper with `FMPAcquisition` typed transport and common financial metadata. No shared helper, registration, locks or financial modeling code changed.

One symbol, explicit ordered dates and a maximum five-calendar-year anniversary are required. Leap-day anniversaries clamp to February's final day. Only daily `1d` and the retained `splits_only` full-endpoint mode are supported; intraday and other adjustments fail before transport. Query dictionaries and provider rows remain unchanged.

OHLC uses the full endpoint's provider split-adjusted convention; `adjClose` is not substituted for close. The controller checked the [provider documentation](https://site.financialmodelingprep.com/developer/docs/stable/historical-price-eod-full); no empirical corporate-action verification is claimed. Currency and corporate-action implementation remain unknown. Price metadata uses currency/share. Provider percentage points are divided by 100 into a fraction with explicit transformation provenance and locally-derived origin; zero remains zero and null remains null. Nullable OHLC does not invent prices. Dates are sorted ascending; duplicates retain provider order and count toward the 5000-row cap. Missing dates are not filled. Observed clipping is partial; otherwise completeness remains unknown. Out-of-window or malformed rows fail safely rather than being silently dropped.

## Verification evidence

The focused suite command runs in WSL Debian from `/mnt/d/Source/QOpenBB`, with PYTHONPATH set to the owned core, FMP and FRED directories:

```text
verification/provider/.venv/bin/python -m pytest -c verification/provider/pyproject.toml tests/providers/test_fmp_daily_history.py -n0 --maxprocesses=2
```

- RED before production restoration: `red.log` records zero collected tests and one collection error for the missing historical model, 18.14 seconds. The shell wrapper reported exit 0 despite pytest's collection error; this is actual failing pytest output, not a reliable captured shell exit status.
- First GREEN: 31 passed, 9.90 seconds, actual Python subprocess return code 0.
- Final GREEN after unit/origin assertions: 31 passed, 10.43 seconds, actual subprocess return code 0 saved in `green-status.json`; output in `green.log`.
- Owning-fork lint: `verification/provider/.venv/bin/python -m ruff check --config vendor/data-api/openbb_platform/providers/fmp/pyproject.toml --no-fix vendor/data-api/openbb_platform/providers/fmp/openbb_fmp/models/equity_historical.py` passes. Initial import-format finding was repaired explicitly.
- Project `measure_python` whole-file measurement: 165 physical lines, 73 logical units, maximum 12/function; `caps.json` records details. Limits 400/300/50 pass. Controller owns inventory and combined cross-lane gate.
- Production and test bytes use LF and one terminal newline. Independent review and acceptance remain pending. No network provider requests, keys, installations, image builds or commits occurred.

The suite covers calendar/leap bounds, pre-I/O rejection, typed encoded transport, zero/null percentage and OHLC observations, nonmutation, stable duplicates, missing dates, clipping, safe malformed/nonfinite responses and distinct missing-data errors. These fixtures establish adapter behavior only.

## Frozen source identities

| File | SHA256 |
| --- | --- |
| `vendor/data-api/openbb_platform/providers/fmp/openbb_fmp/models/equity_historical.py` | `a9d43baaba1cf04fa32b6ea0ed081759d3bbc0f957318feabe00e653b237af42` |
| `tests/providers/test_fmp_daily_history.py` | `560aafcdbf2ae26172c3a32b6872707d25d5a80834a41ff66e38340f5ded32d0` |

Both new files require explicit controller staging. Other workers' discovery models were preserved. The default `product.md`, `tech.md` and `structure.md` steering files are absent in this checkout; the supplied task and available steering were used.
