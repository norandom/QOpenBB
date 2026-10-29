# Key-metrics annotation adoption accepted

Repair task 2.1 is accepted at data-fork 304c24dfd0778050f1e9be8a39d4b31e3f27f5ce. Static units and financial bases now belong to typed class declarations. Runtime metadata reads copies of those declarations and supplies observed availability and fiscal periods. Existing query defaults, input aliases, output names, values and metadata are preserved.

Astra independently passed 35 tests in 6.33 seconds and 10 complete baseline row/metadata comparisons, loading both former production classes independently. Owning FMP Ruff passed. The combined Node 24.22.1 scope gate passed 77 files without errors or violations. Final source counts and hashes are in [counts-hashes.json](counts-hashes.json); all production files meet 400/300/50 caps.

See [review](review.md). Main spec acceptance remains 15/26 until the declaration repair and real-class projection join are complete. This source commit does not register new providers or publish a runtime image.
