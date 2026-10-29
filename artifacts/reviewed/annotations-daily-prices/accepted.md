# Daily-price declaration adoption accepted

Repair task 2.2 is accepted at data-fork 5886418167223374e207e01115d2e4f098d07121. Class declarations now own the existing five-calendar-year window, 5,000-row cap and static field semantics. Validation, clipping and metadata read those same declarations. Runtime helpers copy templates and supply observed availability.

Astra independently passed 33 tests in 6.16 seconds and seven complete comparisons against former rows and metadata, including more than 5,000 duplicate observations. Owning FMP Ruff passed. The task-scoped combined Node 24.22.1 size gate passed 76 files without errors or violations; unrelated unfinished provider lanes were outside that fork manifest. Production measures 214 physical lines, 73 logical units and 12 maximum function units.

All source values, nulls, zeroes, dates, ordering, errors, aliases and percentage conversion remain unchanged. See [review](review.md) and [source hashes](counts-hashes.json). Main spec progress remains 15/26 pending the remaining declarations and real-class projection join.
