# Issuer free cash flow yield

Factor tasks 7 and 8 passed independent financial review on Ubuntu on 2026-11-25. The issuer method selects trailing consolidated operating cash flow and capex from four consecutive standalone fiscal quarters or a comparable annual filing. The filing selector in filings.py retains original observations and fiscal boundaries for the model in fcf_yield.py. Filing revisions and dated equity values must be available at the historical cutoff.

The frozen annual example produced 5% from 60 of operating cash flow, 20 of capex spending and 800 of equity market value. The rolling four-quarter example produced 4.75% from 50 of operating cash flow, 12 of spending and 800 of equity value. The selected observations, substitutions, numerator components and denominator are available in the trace. Negative and zero FCF remain meaningful. Unavailable or incompatible inputs produce a withheld reason.

Independent review reproduced and verified corrections for YTD reclassifications, 52/53-week calendar boundaries, the latest complete window and component-by-component reconciliation of annual and quarterly totals. Missing capex cannot hide conflicting OCF evidence. The denominator review confirmed that a stale explicit period end and a publication after the cutoff both withhold the yield.

The service suite passed all 274 factor tests, including 52 filing-selection and 26 yield tests. The portable repository check passed 805 tests, with 13 skips and one deselection. Ruff and staging checks passed. The combined complexity gate measured 803 files with zero violations. Verification used synthetic supplied observations. Live point-in-time input qualification, independent reference recalculation, saved evaluations and dashboard integration remain open.
