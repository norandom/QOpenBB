# Native projection agreement is ready for independent review

All 24 focused financial OpenAPI cases pass after the controller's canonical response-envelope repair. Tests use actual installed RegistryMap and ProviderInterface types and native route model associations for EquityInfo, IncomeStatement and FredSeries. Each installed route response_model is its corresponding native interface return annotation, and projected success responses resolve to canonical row properties.

An isolated real Registry includes Providers assembled from all eleven accepted first-batch fetchers: profile, income, balance, cash flow, search, peers, historical prices, key metrics, ratios, enterprise values and FRED series. Real RegistryMap and ProviderInterface construct native schemas; FastAPI assembles typed routes. Enterprise values remains test-only registration. Production provider registration and router mounts are unchanged.

Tests check source-class paths, complete canonical templates, declared policies/bounds, FMP static and FRED dynamic semantics, and every projected success-schema branch. Local references resolve. Native components and input documents remain unchanged; projection is deterministic and idempotent. Stale projected envelopes retaining original aliases fail collision validation. Missing annotations on actual enterprise-value data and unsupported typed response models fail explicitly. Original fixture tests remain intact.

Real key-metrics, enterprise-value and FRED transforms consume synthetic acquisitions, then pass through OBBject.from_query serialization. Rows and extra.results_metadata.__qopenbb_financial__ agree with declarations. FRED preserves legacy per-series metadata, dynamic GDP columns, source units and effective percent-change units. No network requests or live entitlement acceptance are claimed.

## Verification and frozen source

- Confirmed RED: native-confirmed-red.log and native-confirmed-red.rc retain two failed native response comparisons and one passed case; actual child exit code 1.
- Initial repaired native check: native-initial-green.log and native-initial-green.rc retain six passed cases, sixteen deselected; actual child exit code 0.
- Final focused file: typed-boundaries.log and typed-boundaries.rc retain 24 passed in 41.42 seconds; actual child exit code 0. One existing aiohttp ClientSession deprecation warning remains.
- Command: existing provider Python runs `-m pytest -c verification/provider/pyproject.toml tests/providers/test_financial_openapi.py -n0 --maxprocesses=2` with accepted source PYTHONPATH. verify-native.py captures actual subprocess codes. No installation, image, browser or live-key use occurred.
- Root accepted baseline: ff451333671e0dc0ca8f9e98141568d3541eec50; data fork: dca75f9b358c3defe5ab7948f847a120a08ff98e.
- Frozen test SHA256: 07e4c8a8946541d2ef470e2fd4f993264ee0abb03c837bf06f6be39b15b8b524.
- Controller-owned projection SHA256 at final check: ee8b006ef260a7673265073e236ad70e17c250d99f2f01888823d197468cb65f.

This worker changed only tests/providers/test_financial_openapi.py and local brief/report/runner evidence. Tests are outside production complexity caps. Controller owns production checks, independent review, combined affected verification, pins, inventory, breadth, publication and acceptance. Unrelated renderer changes were preserved.

## Status Report
- STATUS: READY_FOR_REVIEW
- TASK: financial-annotations repair 5 test integration
- FILES_CHANGED: tests/providers/test_financial_openapi.py
- VERIFICATION: 24 passed; actual pytest child exit code 0
- REMAINING: Independent review and controller combined join; no worker acceptance or production registration claim.
