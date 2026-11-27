# FMP valuation source contract

The 2026-11-27 MSFT captures support the standard snapshot and both custom query forms for independent review. All three calls returned HTTP 200. The paired custom observations support acknowledgement of the beta input. Calculation effects and sensitivity remain unverified.

## Query and response envelope

| Operation | Stable GET endpoint | Effective wire query | Result bound |
| --- | --- | --- | --- |
| Standard | `/stable/discounted-cash-flow` | Required single normalized `symbol`. Observed `symbol=MSFT`. | Accept a top-level array containing zero or one row. Reject larger arrays. |
| Custom | `/stable/custom-discounted-cash-flow` | Required single normalized `symbol` and optional numeric `beta`. Observed `symbol=MSFT` and `symbol=MSFT&beta=1.0`. Omission sends no beta and leaves the default to FMP. QOpenBB admits finite dimensionless beta in [−10, 10]. | Validate every row. Return the first 25 in source order and record observed/returned counts and clipping. |

Each acquisition uses one GET. QOpenBB admits only the listed controls. FMP's published custom path descriptor associates the optional numeric `beta` parameter with the stable custom endpoint. Its published example is `1.244` and does not specify the default or an admissible range. The embedded parameter table was inspected on 2026-11-27. [Standard endpoint](https://site.financialmodelingprep.com/developer/docs/stable/dcf-advanced) · [Custom endpoint and embedded parameter table](https://site.financialmodelingprep.com/developer/docs/stable/custom-dcf-advanced?ref=docs)

Successful `[]` has acquisition metadata and zero results. The existing typed missing-data outcome projects to HTTP 204 with an empty body. A foreign symbol, malformed required value, duplicate custom identity or invalid response shape fails admission. A valid clipped custom result demonstrates local clipping. Upstream completeness is unknown in both captures and remains unknown at the product bounds. The 4 MiB body, 32 nesting levels and 128-character numeric token limits are the approved shared decoding bounds.

## Standard DCF mapping

| Exact source key | Observed JSON kind | Retained meaning and unit |
| --- | --- | --- |
| `symbol` | text | Required normalized listing symbol. Must equal the selected symbol. |
| `date` | text | Required provider valuation civil date with `YYYY-MM-DD` precision. |
| `dcf` | decimal | Required finite provider DCF value, per share, denomination unknown. |
| `Stock Price` | decimal | Optional provider stock-price reference, per share, denomination, price adjustment convention and market observation date unknown. |

The API definition gives the DCF basis as equity value divided by diluted weighted-average shares. It identifies Stock Price as the price used with the share count in a market-cap expression. That provides the per-share basis while leaving the quote convention and timing unknown. There were no unmapped keys in this capture. Record retrieval time separately from the source valuation date and unknown reference market observation date. [FMP DCF formula](https://site.financialmodelingprep.com/developer/docs/dcf-formula)

## Custom DCF mapping

Custom identity is the selected listing symbol and provider year. The required year accepts a canonical four-digit text or JSON integer. Both token kinds identify the same year for duplicate detection. The captured labels are 2031 through 2022 in descending source order. Historical, forecast and fiscal calendar classifications remain unknown. Provider valuation date and reference price observation date remain separate unknowns. Keep the retrieval instant in acquisition metadata.

| Exact retained source key(s) | Observed JSON kind | Retained meaning and unit |
| --- | --- | --- |
| `symbol`, `year` | text | Required listing symbol and provider year label. |
| `equityValuePerShare` | decimal, integer | Required finite provider equity valuation per share. Denomination unknown. |
| `price` | decimal | Separate provider reference price. Unit, denomination, adjustment basis and market observation date unknown. |
| `beta` | decimal, integer | Provider-returned dimensionless beta. Preserve the token on each row. |
| `wacc`, `riskFreeRate`, `marketRiskPremium`, `costOfEquity`, `taxRate` | decimal | Provider-returned financial assumptions. Preserve raw numeric scale. |
| `longTermGrowthRate` | integer | Provider-returned financial assumption. Preserve raw numeric scale. |
| `costofDebt`, `depreciationPercentage`, `ebitdaPercentage`, `ebitPercentage`, `capitalExpenditurePercentage` | decimal | Distinct provider assumptions. Preserve raw numeric scale. |
| `revenuePercentage` | decimal, integer | Provider revenue-related assumption. Definition and financial scale unknown. |
| `revenue`, `ebitda`, `ebit`, `depreciation`, `capitalExpenditure` | integer | Distinct operating inputs or results at source scale. Preserve signed value. Denomination, multiplier and precise basis unknown. |
| `enterpriseValue`, `equityValue`, `ufcf`, `terminalValue`, `netDebt`, `totalDebt`, `totalCash` | integer | Distinct provider valuation and capital structure details at source scale. Denomination and multiplier unknown. |
| `dilutedSharesOutstanding` | integer | Provider share count. Dilution, adjustment and measurement convention unknown. |

Retained details other than identity and per-share equity value are optional. Preserve source keys for origin metadata, including lowercase `o` in `costofDebt`. Keep `depreciation` and `depreciationPercentage` separate. Retain numeric lexemes exactly as integer or decimal tokens, including zeros and trailing zeros. Keep explicit optional null distinct from omission wherever represented in the native result. Use no inferred percent conversion, FX conversion, year-to-date conversion, or implied market date. The lease and minority-interest treatment and equity/debt/cash adjustment bases remain unknown. [Custom endpoint output description](https://site.financialmodelingprep.com/developer/docs/stable/custom-dcf-advanced)

The following observed fields remain unmapped with their definitions or precise bases unresolved:

- Decimal rate and weighting details `afterTaxCostOfDebt`, `debtWeighting`, `equityWeighting`, `inventoriesPercentage`, `payablePercentage`, `receivablesPercentage`, `totalCashPercentage`.
- Integer cash-flow, operating, and capitalization details `ebiat`, `freeCashFlowT1`, `inventories`, `payable`, `presentTerminalValue`, `receivables`, `sumPvUfcf`, `taxRateCash`, `totalCapital`, `totalEquity`.

## Beta and evidence

The custom baseline passed the pre-send requirement for ten unique MSFT identities with valid provider years and finite exact equity value per share on every row. The override had the same ten unique identities. FMP returned the integer token `1` on all ten override rows, exactly equal to requested `1.0` in decimal arithmetic. Baseline returned a different decimal on every matched row. Keep the requested token and observed beta tokens separate. A supplied finite unequal beta is a mismatch. A missing echo or unusable matched pair leaves confirmation unavailable during characterization. A normal query does not send a baseline request. The echo establishes input acknowledgement. Recalculation and sensitivity remain unverified.

[Observations and sanitized receipts](observations.json) contain the ordered source identities, exact beta tokens, response hashes, row hashes, counts and types. A row hash covers each original JSON object from opening through closing brace, excluding surrounding array syntax and whitespace. Complete captures and credentials stay private. [Synthetic cases](synthetic-cases.json) contain invented values and raw JSON body strings for exact-token, envelope, identity, clipping and beta regression checks.
