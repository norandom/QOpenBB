# Factor signal implementation plan

The target runtime is the existing `qopenbb-data-api` container. Paths under `models` and `verification` below are relative to `services/data-api/qopenbb_data/modeling/`. Foundation task references identify capabilities to implement or verify in that package. Use the current data image, root test suites, and existing Dagger and complexity tooling. Each task is a 1–3 hour unit. Use the existing [foundation plan](../financial-modeling/tasks.md) for shared capabilities and the [approved design](design.md) for financial rules.

The controller freezes shared interfaces, integrates registry changes and updates the breadth map with actual evidence. Assign at most two implementers with disjoint writable files. Give each parallel worker a dedicated test module named for the method. An independent author writes references against the frozen inputs and definitions without importing production helpers. Every task requires independent review and fresh verification. The complexity gate means 400 physical lines/file, 300 logical units/file and 50 units/function across each entire changed production file; run one heavy suite at a time.

- [x] 1. Establish the factor package and executable inventory gate
  - Use the existing data runtime manifest and frozen lock. Verify the required Polars version is installed before using it, updating the runtime lock if needed. Apply foundation tasks 1–3 in this package, extend the root complexity inventory and add production modules to the explicit runtime input allowlist. Exercise `tests/delivery/test_data_image.py` against the staged files. Show that an oversized synthetic function fails and a clean package passes the installed checker.
  - _Boundary: Controller owns package setup and shared inventory. Apply the complexity gate to setup and checker changes._
  - _Requirements: 4.4_

- [x] 2. Freeze dated input and output examples
  - Freeze the six descriptors' input keys, units, rule and reference versions, numeric tolerances and trace fields. Include schedule revision, decision and evaluation timestamps, session zone, availability times, entity scope and partial-result states. Agree on fixture ownership and show valid and missing-input examples round-trip through foundation contracts. Review actual provider mappings separately for live eligibility; unknown provenance yields a withheld reason.
  - _Boundary: Controller owns contract fixtures and shared schemas. Apply the complexity gate to maintained schema code._
  - _Depends: 1 and accepted foundation model protocol (task 4.1)_
  - _Requirements: 1.4, 2.3, 3.5, 4.1, 4.4_

- [x] 3. Resolve trading windows and eligible price versions
  - Join expected sessions to prices by date. Show that a shuffled 64-close window resolves in order, holidays preserve adjacency, and gaps, conflicting duplicates, nonpositive closes and unavailable versions fail with dated reasons. Separate calendar endpoint resolution from complete-price validation so DFII10 can use endpoints independently.
  - _Boundary: models/factors/sessions.py and session tests; apply the complexity gate._
  - _Depends: 2_
  - _Requirements: 1.3, 1.4, 2.2_

- [x] 4. (P) Calculate ETF momentum
  - Report percentage price return and dated trace from the first and last eligible closes. Verify a flat and a varying series, dividends-excluded labeling and the missing-session outcome.
  - _Boundary: models/factors/momentum.py and momentum tests; apply the complexity gate._
  - _Depends: 3_
  - _Requirements: 1.1, 1.3, 1.4_

- [x] 5. (P) Calculate ETF realized volatility
  - Verify that the trace contains 63 simple returns, divisor 62 and annualization by the square root of 252. A constant price yields zero and a missing required close withholds the output.
  - _Boundary: models/factors/volatility.py and volatility tests; apply the complexity gate._
  - _Depends: 3_
  - _Requirements: 1.2, 1.3, 1.4_

- [x] 6. (P) Classify the real-yield regime
  - Verify all three signs using exact DFII10 endpoint levels and report percentage-point change. A missing interior date preserves classification; a missing endpoint or unknown vintage availability withholds it. A later revision cannot change the historical signal.
  - _Boundary: models/factors/real_yield.py and regime tests; apply the complexity gate._
  - _Depends: 3_
  - _Requirements: 2.1, 2.2, 2.3_

- [x] 7. Resolve the issuer's trailing cash-flow period
  - Select four consecutive standalone quarters or an annual total for the same trailing period. Prove that overlapping flows, incomplete coverage and a filing published after the historical decision time cannot enter the numerator. Normalize capex spending only with an evidenced sign convention.
  - _Boundary: models/factors/filings.py, consumed by fcf_yield.py, and filing-selection tests; apply the complexity gate._
  - _Depends: 2_
  - _Requirements: 3.2, 3.4, 3.5_

- [x] 8. Calculate dated company FCF yield
  - Verify issuer-level market value on the same observation date, compatible scope, units and currency. Show positive, zero and negative yields, and withheld outputs for a missing or nonpositive denominator or unknown availability. Preserve numerator components and filing references.
  - _Boundary: models/factors/fcf_yield.py and yield tests; apply the complexity gate._
  - _Depends: 7_
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

- [x] 9. Compare two proxies on matched windows
  - For each like metric verify left minus right in percentage points. Reverse the pair, change its calendar, and invalidate one leg; preserve the independently valid leg and identify the reason a spread is withheld.
  - _Boundary: models/factors/comparison.py and comparison tests; apply the complexity gate._
  - _Depends: 4, 5_
  - _Requirements: 4.1_

- [x] 10. Build decision-time study groups
  - Use explicit benchmark, position rule, horizon, dates and partition. Verify that a signal published at or after the start of its outcome cannot enter the group. Report universe, coverage and exclusions separately by regime and partition.
  - _Boundary: models/factors/study_schedule.py and study_groups.py, consumed by diagnostics.py, and group-selection tests; apply the complexity gate._
  - _Depends: 2, 6_
  - _Requirements: 4.2, 4.3_

- [x] 11. Compute timing diagnostics
  - Verify that a tie stays in the hit-rate denominator, opposite regimes remain distinct, absent winners or losers give an undefined slugging ratio, and drawdown uses the disclosed chronological exposure path. Reject overlapping returns for compounding. Missing study assumptions leave base factors available.
  - _Boundary: models/factors/diagnostics.py and study-result tests; apply the complexity gate._
  - _Depends: 10_
  - _Requirements: 4.2, 4.3_

- [x] 12. Independently verify the ETF factors and comparison
  - From dated input fixtures independently reconstruct the session window, both price metrics and ordered spread. Feed candidate outputs to the foundation verifier; perturb a divisor, observation date and spread direction and show each discrepancy fails.
  - _Boundary: verification/factors/ ETF and comparison references and reference tests; apply the complexity gate._
  - _Depends: 9 and foundation rule runner (task 5)_
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 4.1, 4.4_

- [x] 13. Independently verify DFII10 and issuer FCF yield
  - Reconstruct endpoint eligibility, filing periods, capex and market value from original dated inputs. Detect a late revision, wrong capex sign and incorrect zero/negative handling against frozen tolerances and exact check states.
  - _Boundary: verification/factors/ regime and company references and reference tests; apply the complexity gate._
  - _Depends: 6, 8 and foundation task 5_
  - _Requirements: 2.1, 2.2, 2.3, 3.1, 3.2, 3.3, 3.4, 3.5, 4.4_

- [x] 14. Independently verify regime-conditioned diagnostics
  - Rebuild groups and wealth paths from dated observations and assumptions. Prove the verifier rejects pooling regimes, dropping ties and including a late signal; verify check states for undefined statistics.
  - _Boundary: verification/factors/ timing reference and reference tests; apply the complexity gate._
  - _Depends: 11 and foundation task 5_
  - _Requirements: 4.2, 4.3, 4.4_

- [x] 15. Register the six descriptors and verify saved evaluations
  - Bind exact model, rule and reference versions. Through the authenticated evaluation and read endpoints, exercise verified, partial and withheld results, inspect traces, and show that a saved run retains its original snapshot after a source revision. Export the compatible projection and identify actual contract tests in the breadth map.
  - _Boundary: Controller integration across registry, foundation contract tests and breadth mapping; apply the complexity gate to changed production files._
  - _Depends: 12, 13, 14 and foundation registry, orchestration, persistence, API and contract delivery (tasks 4–9)_
  - _Requirements: 1.4, 2.3, 3.5, 4.1, 4.4_

## Downstream story acceptance

Task 15 closes the model-spec handoff when all prerequisite tasks and independent checks pass. The completed factor spec can then satisfy the real-model prerequisite for foundation task 12.1. At the foundation 12.2 packaging milestone, rebuild the existing data API image through Dagger and verify its route schema and source hashes.

The research-stories plan owns the subsequent browser journey against a runnable App, the accepted bridge, bound widgets and packaged images. In isolated Ubuntu Playwright, change the proxy pair and date, compare a displayed value and its source rows with the saved run, exercise insufficient history, and save and reopen. Record image identities and verified live inputs. An issuer needs evidenced historical filings and dated market value before live numerical FCF yield acceptance. Track this journey separately from factor-spec completion.
