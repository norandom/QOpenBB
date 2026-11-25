# Factor contract foundation acceptance

The data API accepts typed, dated snapshots and immutable model-run evidence. This checkpoint covers serialization, validation, domain imports and staging. Financial formula execution, provider availability, persistence and dashboard integration require their own checks.

On Ubuntu, `bash pipeline/ci.sh check` passed 583 tests with 12 skipped and one deselected. The combined complexity gate measured 794 files with zero violations. Using the service interpreter with `PYTHONPATH=services/data-api`, all 78 tests in `tests/factors` passed. Ruff passed on the modeling package and factor tests.

Independent review reproduced and then verified repairs for text and decimal round trips, decision-time eligibility, blocking failures, evidence ownership and reference fingerprints. A trace expression or check change invalidates its previous reference match. A 38-significant-digit control survived serialization under both Pydantic 2.12.5 and 2.14.1. The 17 run-evidence regression cases include a verified round trip and propagation of withheld results.

Scope is limited to the synthetic contract examples and existing data-image staging path. No provider calls, candidate image or release were needed.
