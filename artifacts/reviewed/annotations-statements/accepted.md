# Balance-sheet and cash-flow declarations accepted

Repair task 4.2 is accepted at data-fork 537cf473d4ecd6bc8f24649bebcd720d6aeca93c. Both statement families now share class-owned static templates with runtime metadata. Actual fiscal-period inference, availability and acquisition provenance remain resolved at runtime.

Independent Astra checks passed 66 tests in 7.62 seconds, 14 complete baseline row/metadata comparisons, owning FMP Ruff and whole-file measurements. All child return codes are zero. The combined Node 24.22.1 gate passed 81 files across frozen income and statement changes without errors or violations. Final source hashes are in [hashes.json](hashes.json).

Stock balances retain instant dates; flow periods and the unknown opening-cash date are preserved. Values, nulls, zeroes, aliases, limits, errors and complete metadata are unchanged. See [review](review.md). Main spec progress remains 15/26 pending the remaining declarations and real-class projection join.
