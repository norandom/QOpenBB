# Installed factor methods and saved evaluations

The existing data API registers six version-1 factor methods. Their descriptors bind rule-set version 1 and independent reference version 1. Signed discovery and reproducible provider export use the same registry.

| Method | Saved output checked through the modeling listener |
| --- | --- |
| ETF momentum | Split-adjusted price return over 63 trading sessions |
| ETF realized volatility | Annualized sample volatility of 63 daily returns |
| Real-yield regime | DFII10 endpoint change in percentage points and rising, flat or falling classification |
| Issuer FCF yield | Trailing operating cash flow less capital expenditure as a percentage of dated equity market value |
| Ordered proxy comparison | Per-leg financial results, coverage and spread for the ordered pair |
| Timing study | Regime-specific hit rate and slugging, and compounded-path drawdown |

The signed HTTP tests evaluate dated synthetic snapshots, reopen owner-scoped runs and compare the widget projections with their saved outputs, scoped traces, check states and verification evidence. An incomplete comparison preserves the eligible results. Missing real-yield evidence withholds the affected result. An unsupported timing horizon withholds the study outputs.

The issuer fixture changes operating cash flow in an amended filing and retains positive capital spending and dated market value. The original evaluation reopens at 5 percent after a listener restart. The amendment produces a distinct run at −10 percent and a different input fingerprint. These values demonstrate saved-run behavior on synthetic financial inputs. Historical live filing and market-value coverage, the Workspace browser journey and the packaged image have separate acceptance gates.

The check-state regression deliberately withholds an eligible result. For zero and negative FCF yields the independently reconstructed amount records a mismatch on the saved run. An ineligible observation remains withheld with unavailable verification.

## Contract adoption

Source revision `7f62bf5fd1f9bede9e08030a5db5f20a88eeb4aa` produced manifest `d544b544f8f036caf0f72dd5b7026d36edc7c27f0bffd34f3b4ce2b4545f13dc`. The provider added the six descriptors while the exported route, schema, widget and app documents and consumer contract retained their accepted bytes. The pre-adoption baseline `986a2f33b282b9bdf791f562f376491102dedb3200d4dd4c7ab82e346ddf01aa` accepted the candidate using exercised evidence `98ab29748e6d0748978aa173149f89bb92a52c96c5973ac247cb4ef49ed53807`. The consumer's SHA-256 is `84ead649b9bd99ed8a8f16eee4d2c7f7c8455f118a094018450bcdd21aab526f`. Both provider and consumer continue to use contract version 1.

Independent review approved the runtime after 275 focused checks. With missing issuer market value the blocking eligibility check ran before calculation. In a partial proxy comparison only the eligible leg's metrics ran. A hit-rate-only computation skipped drawdown and returned only its own trace. Removing issuer FCF yield version 1 from a copy of the newly adopted catalog produced an incompatible-method-removal finding.

The full Ubuntu verification suite reported 1711 passed, 12 skipped, 1 deselected in 205.31s (0:03:25).
