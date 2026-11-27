# Microsoft earnings selection and chart verification

On November 27, 2026, the local packaged Events and Documents App displayed Microsoft's actual and estimated EPS and revenue for July 30, 2025. The calendar edit and authenticated dashboard reopen each retrieved 1,440 market rows from FMP. Microsoft was the 1,334th row in both responses. Each listing-scoped response returned that one row, with all four chart values and source details matching the underlying FMP response. The final view also contained SEC filings, transcript and news evidence. [Source and local image identities](candidate.json)

The earnings route takes an optional listing. It validates the market response for the date window, selects that listing and applies the 250-row cap in provider order. A query without a listing retains the market-wide behavior. A populated window with no match returns HTTP 200 with an empty result and retrieval metadata. Empty upstream data uses the existing HTTP 204 response. Source completeness remains unknown.

The isolated Chromium 156.0.8078.4 journey passed 23 browser assertions, with 16 HTTP 200 provider receipts and zero guard denials. The post-run comparison initially failed on a variable name in the document verifier. The corrected verifier passed offline against those same receipts, including chart marks and document comparisons. The retained source replay also reproduced the old market slice and the corrected Microsoft selection on the original capture. [Browser journey](../../tests/e2e/events-documents-workspace.spec.mts) · [Independent response comparison](../../tests/e2e/events_documents_oracle.py) · [Mounted API and SDK regressions](../../tests/providers/test_fmp_batch_b_installed_join.py)

The packaged controlled journey also passed 18 scenarios across 40 browser acquisitions with zero provider sends. It exercised missing values, clipping, recovery and saved state.

The Data API and Workspace images were built and tested locally. The source lock identifies both changes. [Pinned sources](../../sources.lock.json)
