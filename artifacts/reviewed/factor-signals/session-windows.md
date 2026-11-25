# Trading sessions and historical close selection

Factor task 3 passed independent Astra review on Ubuntu on 2026-11-25. The resolver accepts a supplied calendar revision and resolves the exact ending session and 63 predecessors. Calendar endpoints are available independently for DFII10. Each proxy's close window preserves the winning source rows and reports dated failures for missing, conflicting, unavailable or invalid closes.

Review identified an estimate that could replace an observed close. Both schedule and close selection now exclude estimates before comparing eligible revisions. Replaying the failure selected the observed 120 over the estimate of 240 and withheld the window when only the estimate remained.

All 42 resolver cases and all 148 factor tests passed in the service environment. The portable check passed 661 tests, with 13 skipped and one deselected, including staged-runtime checks. Ruff passed and the 797-file complexity gate reported zero violations. Evidence uses synthetic observations. The next tasks implement factor values and traces.
