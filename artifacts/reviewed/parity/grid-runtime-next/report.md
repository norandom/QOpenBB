# Grid reference capture ready for review

2026-10-17. Seven original-runtime cases completed; fifteen independent finite-array assertions passed. Start/journey/cleanup exited 0. The resulting evidence supports review of an explicit-category ordinary displayed-grid capture. It does not establish candidate parity, UI filter/sort control acceptance, backend persistence or a general category inference rule.

The authoritative contract and remaining cases are in [chart-grid-runtime-next.md](../../../.kiro/specs/openbb-self-service/chart-grid-runtime-next.md). Original source is `38dffc33389aca0e4a87e0e88d42f7067aa220df`; verified image is `sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f`; candidate contract source is `945e438a9a65c3eeef7073dbce64a03b02f0ff6f`.

`ordinary.json` and `filtered-sorted-bounds.json` record exact displayed observations, stable-in-this-dataset node IDs, category/series binding, inclusive bounds and numeric series ordering. `numeric-only.json` observes generated category values 1..6. `multiple-category.json` records visible period/region input and the final period-only category without claiming the unresolved normalization cause. `formatted-margin.json` records displayed `20.0 %` against chart value 0.2. `hidden-selected.json` records the hidden series omission. `synthetic-value-getter.json` records getter output independently of raw data and remains explicitly synthetic instrumentation.

Reproduce from repository root:

```powershell
wsl -d Debian -u mc -- bash /mnt/d/Source/QOpenBB/artifacts/parity/grid-runtime-next/run.sh
wsl -d Debian -u mc -- /mnt/d/Source/QOpenBB/artifacts/task-1.2/node-v24.22.0-linux-x64/bin/node artifacts/parity/grid-runtime-next/assert.mjs
```

The runner uses a new disposable account/state/container and one headless browser. It verifies the cached original image rather than building/installing. Output records are `command-status.json`, `assertions.json`, `cleanup-report.json` and the fixture/case JSON/PNGs. `journey.log` records each case's exact finite output. Actual start/journey/cleanup and assertion exits are 0. Preparation initially had a shell PATH quoting failure before execution; corrected preparation and syntax validation exited 0.

The original bundle JavaScript parse defect and initial 404/Axios error remain in `diagnostics-public.json`; clean application acceptance is not claimed. All external browser requests were denied by routing, with none attempted. This lane read no owner credentials, state or environment files, called no external provider, and changed no production code. Runtime credentials and owned bind state were deleted. `runtime.json` and raw `diagnostics.json` stay local and are excluded from publication.

`publication-allowlist.json` freezes only completed synthetic fixtures, projections, screenshots, scripts, logs, assertions, cleanup and this report. The sanitized diagnostic derivative records its own hash and the raw source hash; it does not claim unchanged bytes. The original source references and runtime identity are explicit. Parent-owned independent review and public-mirror synchronization remain required before publication or acceptance.
