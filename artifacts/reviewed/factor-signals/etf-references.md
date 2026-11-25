# ETF price and comparison references

Factor task 12 independently reconstructed the 64-session window from dated inputs, calculated the 63 simple returns and used the sample variance to verify annualized volatility. Comparison references independently verified both legs and their ordered percentage-point spreads.

The foundation verifier rejected a population divisor, a shifted endpoint and reversed spreads. Both left-side values verified when the right input failed. Missing the right table produced unknown checks. Omitting one required close from the supplied right table produced failed checks. The frozen tolerances are 0.00000001 percent and 0.00000002 percentage points.

Independent financial review approved the change and ran 85 focused ETF tests. An additional controller calculation compared 54 values from nine uneven paths with exact rational returns and sample standard deviations. The scoped lint and combined complexity checks passed. Base revision 80c7a1a. Evidence uses synthetic snapshots.
