# ETF price and real-yield method acceptance

On 2026-11-25, factor tasks 4–6 passed independent financial review on Ubuntu. All three methods match their frozen version-1 descriptors and return supplied-input calculation candidates in the existing data API package. Historical eligibility uses the earlier of the decision and evaluation timestamps. Traces identify the selected observations.

- ETF momentum uses split-adjusted closes excluding dividends. The frozen 100-to-120 path produced 20% over 63 sessions.
- ETF realized volatility uses 63 simple returns, sample divisor 62 and annualization by the square root of 252. The single-jump example produced 40%. A constant daily return of −2/3 produced exactly zero volatility with all 63 dated returns retained.
- DFII10 classifies the exact change between the two scheduled endpoint levels. The frozen increase from 1.50% to 1.75% produced a rising classification and a 0.25 percentage-point change. A missing or historically ineligible endpoint withholds both outputs. If the change exceeds the decimal contract, both outputs carry the dated reason.

Astra re-review accepted the corrections for constant-return volatility, endpoint period preservation and paired withholding of the regime and change. The controller also compared both ETF methods against a separate 64-close series with a varying daily return using Python statistics. The service suite passed all 196 factor tests. The portable repository check passed 721 tests with 13 skips and one deselection. Staging imported the packaged methods, Ruff passed, and the 801-file complexity gate reported zero violations.

These checks used synthetic data. Independent reference implementations, authenticated saved evaluations and story dashboard acceptance remain scheduled in the factor and story plans.
