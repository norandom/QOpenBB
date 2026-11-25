# Factor signals design

## Boundary Commitments

Four versioned model descriptors produce ETF momentum, ETF realized volatility, a real-yield regime and issuer FCF yield. A comparison uses the two ETF results at a common evaluation cutoff. The company observation has its own issuer and date and never participates in the ETF ranking.

**Out of Boundary.** Market-data integrations owns provider semantics, rights and dated inputs. Financial modeling owns authenticated evaluation, check resolution and immutable storage. Research stories owns selection, narrative and chart rendering.

**Allowed Dependencies.** Use the foundation's typed snapshots, model protocol, rule runner, independent verification and result projection. Use versioned trading sessions supplied with the evaluation. Each proxy identifies its listing calendar. For the first pair require the same session schedule over the window; withhold a cross-calendar comparison until an alignment method is specified.

**Revalidation Triggers.** Changes to a calendar, source mapping, adjustment basis, availability convention, method or diagnostic assumptions require a new fingerprinted evaluation. Recheck affected consumer contracts if units, trace fields or status semantics change.

## Evaluation and file structure plan

Paths below are relative to QOpenBB. Each new model module implements the planned model protocol inside the packaged data API. The modified registry binds exact versions. The orchestrator resolves the inputs, computes each output, runs checks and persists the result before the App reads its projection.

| Proposed path | Responsibility and approved criteria |
| --- | --- |
| `services/data-api/qopenbb_data/modeling/models/factors/sessions.py` | Resolve the ending session and preceding 63 sessions from the named schedule, sort and validate observations (1.3, 1.4, 2.2). |
| `services/data-api/qopenbb_data/modeling/models/factors/momentum.py` | Compute price momentum from the eligible close window (1.1). |
| `services/data-api/qopenbb_data/modeling/models/factors/volatility.py` | Compute annualized sample volatility from the same window (1.2). |
| `services/data-api/qopenbb_data/modeling/models/factors/real_yield.py` | Compare two DFII10 observations at the ETF window endpoints (2.1, 2.2, 2.3). |
| `services/data-api/qopenbb_data/modeling/models/factors/fcf_yield.py` | Resolve eligible company periods, normalize capex and verify a comparable market value (3.1, 3.2, 3.3, 3.4, 3.5). |
| `services/data-api/qopenbb_data/modeling/models/factors/comparison.py` | Present each leg's status and derive a spread only when both windows and return bases match (4.1). |
| `services/data-api/qopenbb_data/modeling/models/factors/diagnostics.py` | Evaluate dated signal outcomes against explicit assumptions (4.2, 4.3). |
| `services/data-api/qopenbb_data/modeling/models/registry.py` | Register installed model versions and declared input, rule and verifier dependencies. |
| `services/data-api/qopenbb_data/modeling/verification/factors/` and `tests/factors/` | Independent scalar references and dated acceptance fixtures for each method (4.4). |

## Inputs, calculations and result contract

1. **Sessions and prices.** Require a named calendar revision, chosen ending session, evaluation timestamp and 64 dated positive finite split-adjusted closes per proxy. Join expected sessions to source rows by date. Reject duplicate conflicting observations and identify missing dates. Exclude dividends. Momentum in percent is 100 × (last / first − 1). For each adjacent pair calculate the simple return. Annualized volatility in percent is 100 × √252 × the sample standard deviation of those 63 returns, using divisor 62. Preserve unrounded values for verification.
2. **Real yield.** Match DFII10 at the two exact session dates. Select only versions available by the evaluation cutoff. Compare unrounded percent levels and report the difference in percentage points, along with the two dated source references. Positive, negative and zero map to rising, falling and flat. A missing endpoint or unknown historical availability withholds the classification. Interior data gaps do not affect this calculation.
3. **Company yield.** Resolve one issuer's latest complete trailing fiscal year of flows available at the cutoff, including rolling four-quarter windows. Use four consecutive, nonoverlapping standalone fiscal quarters or an evidenced annual total covering the same trailing period. Reject overlapping year-to-date flows; a later amendment is eligible only after publication. Require matching scope, currency and scale, and issuer-level equity market value dated to the observation session and available by the cutoff. Convert capex using the documented source sign convention. An unknown convention fails the check. Yield in percent is 100 × (operating cash flow − capex spending) / market value. Retain negative and zero numerators; withhold on missing inputs or nonpositive market value.
4. **Comparison and diagnostics.** Show each ETF's window, value and check state. A spread in percentage points is meaningful only between like metrics. For timing diagnostics require versioned assumptions for the signal-to-position rule, horizon, benchmark, evaluation dates, partition and drawdown return basis. Form a position only from signals available strictly before its evaluated return starts. Report eligible and excluded counts by reason. Compute hit rate as positive benchmark-relative outcomes / eligible outcomes, counting ties in the denominator. Compute slugging ratio as mean positive outcome / absolute mean negative outcome. Compute drawdown from the running peak of a chronological compounded wealth series on the disclosed basis. Withhold undefined ratios and drawdown for an undefined return path. Do not compound overlapping forward outcomes. An unspecified timing rule or benchmark leaves diagnostics unavailable and preserves separately valid factor values.

For a historical observation the cutoff is its decision timestamp on the observation date, bounded above by the evaluation timestamp. Record both timestamps and the session time zone. Apply this cutoff to all price versions, macro vintages, filings and market values. Withhold the affected output if availability cannot be established. A December observation reconstructed in February excludes a January filing or price correction.

Register two additional model descriptors for the derived results. The comparison descriptor consumes the ordered left and right proxy observations and their versioned method references. Report the left value minus the right value in percentage points. Validate each leg separately; a failed right leg withholds the spread and preserves the left result. The timing-study descriptor consumes dated signals, regime observations, subsequent returns, benchmark and assumptions. Its reference verifier reconstructs group membership and outcomes from the dated snapshot; the comparison verifier independently recalculates both legs and subtracts in the declared order. Run each verifier against its own evaluation.

Group timing outcomes by decision-time regime and study partition. Report the universe, calendar span, coverage limitations, eligible and excluded counts, hit-rate denominator, mean winner and absolute mean loser in every group. Test opposite outcomes in two regimes and a tie in one group so pooling regimes or excluding ties changes the expected result. For drawdown, follow the study wealth path chronologically and disclose whether the reported series covers the whole study or a regime-conditioned strategy; require an explicit exposure rule for sessions outside the regime.

Results use the foundation's OutputResult and TraceEntry. Each value references the source rows, issuer or proxy, exact dates, units, basis, assumption version, substitutions and affecting checks. Financial input failures produce a null value and a reason. The story can therefore distinguish insufficient history, unavailable vintage, incomplete filings and an undefined diagnostic. Reads of saved runs reuse the original snapshot and checks.

## Verification and delivery

- Independently reconstruct a flat and a varying 64-close path, the 63 returns and sample variance. Shuffle dates, drop a trading day, include a holiday, apply a correction published after the historical decision timestamp, introduce a conflicting duplicate and span the verified history gap. Verify each proxy independently and suppress the comparison if either fails.
- Compare all three regime signs using exact endpoint levels. Remove an interior observation, then an endpoint. Move publication beyond the cutoff and verify that the historical signal is withheld.
- Recalculate FCF yield from dated filings and market value. Cover both capex sign conventions, zero and negative FCF, fiscal-year boundaries, overlapping periods, later restatements, ambiguous currency and a missing dated denominator.
- Rebuild timing outcomes from independently dated inputs, including a tie, no losers, a drawdown and a signal published after the return begins. Verify that study partitions and exclusions remain visible.
- The reference implementation may share input types only. Freeze unit-specific numeric tolerances with the method version before acceptance; assert statuses, classifications and dates exactly. The foundation checker and inventory must run before model tasks and enforce 400 physical lines/file, 300 logical units/file and 50 units/function.
- End-to-end story acceptance uses the published result contract to change symbols and dates, inspect source rows, save and reopen a run, and verify insufficient data on an incomplete window. This is planned coverage. The existing Company Research test proves a different journey.
