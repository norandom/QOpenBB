# Periodic FMP metrics and ratios acceptance

Tasks 2.7 and 2.8 are source-accepted on 2026-10-28 after independent financial review. Metrics source: e5cfbd5a2c96698dbc22347befa2521a88d90e7e. Ratios source: 4bef44cd5622f834df0b9afdb20c0d1f1183f013.

Independent verification passed 62 tests in 10.61 seconds, actual subprocess exit 0: 33 metrics and 29 ratio cases. Owning FMP Ruff passed all four production files. The Node 24.22.1 combined scope/size gate passed 78 files without errors or violations. Frozen source hashes/counts are in final-source.json; all satisfy 400 physical / 300 logical / 50 per function.

Both adapters request periodic annual/quarter data only, accept the quarterly alias, require one symbol and strict integer limits 1 through 1000 with default 5, and reject unsupported TTM modes before I/O. Signed, zero and null values remain provider observations/calculations. Receipt timestamps, stable ordering/duplicates and observed clipping remain explicit; completeness is otherwise unknown.

Metrics use declared field units, retain source aliases and optional missing financial dates, and publish only modeled fields with metadata. No date, fiscal label or currency is synthesized. Ratios distinguish fraction and percentage-point dividend yield without silent rescaling; price multiples, per-share amounts and solvency fractions carry explicit units. Required missing ratio dates fail safely rather than being fabricated. Financial-period labels do not establish provider calculation windows, annualization or actual market valuation dates.

Independent review repaired metrics extra-field leakage and ratio valuation-date implications. Final focused tests verify those repairs. Actual preimplementation missing-module RED was captured for both tasks; early wrapper exit caveats are recorded transparently. A worker model reached capacity while reporting after source/tests completed; controller finalized that report from saved final outputs and independent review verified the exact frozen snapshot.

No shared transport/helper changes, provider registration, installed API/widget acceptance, live account/entitlement proof or image publication is claimed. These are provider-derived inputs, not the separate house modeling engine.
