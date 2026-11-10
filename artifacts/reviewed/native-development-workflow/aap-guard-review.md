# AAP guard correction review

2026-11-10. APPROVED for the code correction only. This review does not authorize another financial batch or accept native-development-workflow task 11.3. Both failed attempts and their claims must remain preserved.

Independently inspected the actual source/test diff and destination, ledger and test contracts. Verified SHA-256: tests/delivery/financial_budget.py fd181cc556e4ef1eb86ef13f1d67785ff9c0939b69beeb1a214831e26aff0e8f; tests/delivery/test_financial_budget.py bf51f56d9e8fd5d771eaeed7edb04006f74eab3260a77f9c99bf761e708ad6fb.

The helper adds only AAP to the existing AAPL/MSFT symbol membership for /stable/profile and /stable/income-statement. The exact HTTPS host, GET method, port, credential presence, query-key sets, periods and limits are unchanged. No new path family, search value, FRED scope, retry behavior or provider allowance is introduced. Maxima remain 80 FMP/16 FRED. The reservation, persistence and cumulative handoff code is unchanged.

The recorded diagnosis ties this change to the existing journey's deliberate raw AAP selection before AAPL: application captures show AAP profile/income requests and two corresponding HTTP 400s; the stopped ledger records 24 FMP/2 FRED and two destination denials. Those are application observations plus source mapping, not captured upstream wire URLs. Income passed, but company diagnostics failed and synthetic/recreation/reopen phases did not execute. Partial progress does not constitute financial acceptance.

New offline tests verify AAP reservations increment only FMP for profile, annual income and quarterly income. Negative cases retain rejection of TSLA, another financial endpoint, widened limits, unsupported periods and extra query keys without incrementing attempted sends. Existing tests cover host/scheme/port and duplicate-query rejection, ceiling exhaustion, persistence and recreation. The controller reports the focused offline suite passed 25 cases in 0.32 seconds and git diff --check passed; the reviewer did not repeat tests or perform runtime/provider/browser operations. The helper is 235 physical lines; the one constant and replaced predicates do not expand function size or approach the 400/300/50 caps.

No blockers in this code delta. Any later live attempt needs fresh bounded owner authorization and a new reviewed runner/helper binding: the old frozen runners deliberately reject this changed helper hash. Do not modify old freezes or relabel their historical proof as execution of this helper.
