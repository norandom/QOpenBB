# Dated factor contract examples

Factor task 2 passed on Ubuntu on 2026-11-25. Six version-1 descriptors and synthetic runs cover ETF momentum, realized volatility, DFII10 regime, issuer FCF yield, ordered proxy comparison and timing diagnostics. Each populated output remains unverified until independent recalculation. Unknown DFII10 availability withholds both endpoint-change outputs. A missing benchmark preserves the synthetic exposed drawdown of 8.8%. The volatility trace preserves every dated adjacent return.

Independent Astra review accepted the corrections to all three examples. The 17 example tests and all 106 service factor tests passed. The portable repository check passed 616 tests with 13 skips and one deselection. Polars materialization ran in the service environment. The combined complexity check measured 796 files with zero violations. The provider-field inventory records which live inputs still need dated availability evidence.
