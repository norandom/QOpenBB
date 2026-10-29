# Dynamic FRED declarations accepted

Repair task 4.6 is accepted at data-fork dca75f9b358c3defe5ab7948f847a120a08ff98e. Typed class declarations expose baseline provider policy, the static date coordinate and runtime resolution for dynamically named quantity columns. Series units, effective frequencies, transformations and vintages remain acquired or resolved at runtime.

Independent Astra checks passed 18 tests in 13.02 seconds, 36 complete baseline comparisons, owning FRED Ruff and whole-file measurements of 334 physical, 88 logical and 22 maximum function units. All eight runtime function ASTs and frozen hashes are unchanged. The combined Node 24.22.1 gate passed 79 files across final ratio/enterprise/FRED adoption without errors or violations.

Wide rows, legacy series keys, quantity-only metadata field keys and oldest acquisition timestamps are preserved. No series enumeration, cache change or point-in-time guarantee is introduced. See [review](review.md). All declaration adoptions are accepted; repair task 5 still must validate real registry/routes before main task 4.1 can close.
