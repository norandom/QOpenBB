# FCF yield in a retained Workspace dashboard

Financial-modeling task 12.1 exercised Workspace `aa1a625e5d9478f023226b9ac9acd3bcfb71da4a` against the existing QOpenBB analytics source from `d77a695`. The source-stage runtime used Workspace base image `sha256:c2e9869c5756b689069dfaaac9c53bc17e876d4e2edd1619533ed96927c99fd9` and data API image `sha256:79d46d09a913a1b6583ae823961ca87b9e4a6bb112739ca738567b131ca79a73`. The driver mounted the reviewed Full frontend and Workspace bridge into the former and ran the maintained modeling source using the latter. Model image assembly and release verification remain separate milestones.

## Financial result

SAP.DE's FY2025 operating cash flow of EUR 9.156 billion less EUR 0.739 billion of capex gave EUR 8.417 billion of FCF. The FMP quote supplied EUR 222,345,903,252 in issuer capitalization. Its actual receipt preceded the decision within the same Xetra session. The production method and independent reference both returned 3.7855431005897290522658664811512252004 percent. AAPL's dated historical capitalization lacked publication evidence and yielded a withheld value with an explanation. The independent numerical suite passed 65 tests. [Capture receipts, decision timestamps and reproducible requests](../../../verification/financial-real-inputs/README.md).

## Browser evidence

The final headless Playwright/CDP run used one worker and a fresh context for every phase. All three phases passed with zero skips or retries.

| Phase | What the analyst observed | Evaluation POSTs |
| --- | --- | ---: |
| Evaluate and save | Native controls displayed the withheld AAPL result, SAP's exact verified yield, assumptions, checks and source trace. Editing an assumption marked the prior result stale. The analyst bound the final run to the read-only widget and saved both widgets on one dashboard. | 3 |
| Recreate and reopen | The driver recreated both containers with retained state. Fresh sign-in, reopen and explicit refresh recovered the same saved run, input snapshot and verified value. Both container IDs changed. | 0 |
| Modeling outage | Both saved widgets surfaced the outage. The analyst opened a direct FMP profile widget, selected Apple and saw its symbol, company name and currency. The four expected 503 responses were confined to modeling reads. | 0 |

The two online phases had zero HTTP errors, console errors, page errors or failed network requests. The outage phase had zero page errors or failed network requests and only the expected service-unavailable console messages. The isolated project and its volumes were removed. Independent review approved the frozen source, verified recreation and reproduced the financial reference. [Linux reproduction](../../../verification/modeling-journey/README.md).
