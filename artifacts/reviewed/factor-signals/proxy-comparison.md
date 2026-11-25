# Ordered ETF comparison

Factor task 9 passed independent financial review on Ubuntu on 2026-11-25. The method runs the pinned momentum and realized-volatility methods for each ETF. It subtracts the right value from the left in percentage points when the trading windows match. The frozen example produced momentum of 20% and 10%, and annualized volatility of 40% and 20%. Reversing the pair produced spreads of −10 and −20 percentage points.

The two legs resolve independently. Different calendars retain eligible leg values and withhold the spreads. A missing close, invalid binding or unrepresentable metric carries a dated reason and preserves results that can still be calculated.

Independent review found that a foreign proxy or calendar published after the decision time could make identity selection ambiguous. The corrected implementation uses only eligible observations to infer identities and retains the bound entity’s versions for dated availability checks. Both failing cases passed on re-review, with identical values and selected source records before and after the later publication.

Verification used synthetic supplied observations. A separate calculation checked 54 values across nine price paths, and complete and partial runs round-tripped through the wire contracts. All 305 factor tests passed, including 31 comparison tests. The portable repository check passed 839 tests with 13 skips and one deselection. Ruff and the 804-file complexity gate passed. Saved-run endpoint and story dashboard acceptance remain scheduled.
