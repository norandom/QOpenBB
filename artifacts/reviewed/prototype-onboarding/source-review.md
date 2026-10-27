# First-login nullable questionnaire repair

ON1 source acceptance is complete on 2026-10-27. Workspace `c767b02019efe1e2bc0070fb180003584648935f` changes only the GET response model and removes the absent-record 404 branch. The real helper already returns an optional questionnaire. Existing authentication, stored answers, POST and skip behavior are unchanged; no empty record is created.

The focused route/SQLite group failed against the baseline only because an absent record returned 404 instead of 200. The other three cases passed. With the repair, all four pass in 7.105 seconds using the pinned published Workspace image with an explicit read-only backend source overlay, isolated temporary SQLite and no network. The maintained test is `tests/delivery/test_onboarding_contract.py`; its `--probe` entry runs in the backend interpreter. Earlier harness setup failures were corrected before the actual baseline comparison and are not product failures.

AST parsing and Python compilation pass. Ruff was unavailable in the existing tools; no dependency was installed solely for lint. Scoped Python complexity passes with no errors or violations: 1999 physical lines, 605 logical units, and unchanged login function at 69. The three no-growth exceptions and their expiry are recorded in the owning first-login contract and inventory. This is Python-only evidence; the CI combined gate remains required.

An independent Sol reviewer inspected the actual diff, tests and recorded outputs and returned APPROVED for ON1. This does not accept first-login browser behavior, assembled Compose, live FMP or deployment. Those remain the next batch criteria. No diagnostics are suppressed and no questionnaire is seeded.
