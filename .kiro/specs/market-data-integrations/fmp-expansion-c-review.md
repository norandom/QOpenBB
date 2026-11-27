# Batch C independent design review

**Passed independent review for task generation on November 27, 2026.** The reviewed design has SHA-256 `f0be6e26662862849ac3f88d0c8334fe44b2c579a172753989f4b028e2509088`. The reviewer used a fresh gpt-6.2-astra context and checked the five proposed native operations against the expansion inventory, existing source and historical DCF evidence. [Reviewed design](fmp-expansion-c-design.md)

| Review finding | Resolution in the reviewed design |
| --- | --- |
| Ordinary JSON decoding can round valuations and share counts, collapse duplicate keys, and make unequal beta values look equal. | All five adapters use a bounded, opt-in raw-body decoder. Public values retain the source number token. A comparison of the requested and returned beta uses exact decimal values. The tests include an integer above the JavaScript safe range and a near-but-unequal beta. |
| A second unnamed fundamental subrouter could displace the existing enterprise command during discovery. | One shared router owns the existing enterprise command and the new commands. The compatibility check repeats composition and verifies unique HTTP operations and SDK discovery. |
| Legacy reported financials turn zero into null. Multiple filings for one fiscal period can also look identical if filing identity is discarded. | Three distinct statement models share a lossless fact representation. Statement identity includes the available source filing context. Conflicting complete identities and unresolved vintages have explicit outcomes. |

The earlier three direct MSFT DCF probes establish historical observations, including a beta echo for matched issuer and year. They leave recalculation, statement access and current entitlement open. This review made zero FMP sends. The design proposes up to 30 sends across source characterization, installed comparison, browser verification and diagnosed follow-up. Owner approval of the execution plan and its live allowance is a later decision. [Prior DCF observations](../analyst-workspace/research-input-assessment.md)
