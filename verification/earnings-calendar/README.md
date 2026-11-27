# Microsoft earnings selection and chart verification

On November 27, 2026, the local packaged Events and Documents App displayed Microsoft's actual and estimated EPS and revenue for July 30, 2025. The calendar edit and authenticated dashboard reopen each retrieved 1,440 market rows from FMP. Microsoft was the 1,334th row in both responses. Each listing-scoped response returned that one row, with all four chart values and source details matching the underlying FMP response. The final view also contained SEC filings, transcript and news evidence. [Source and local image identities](candidate.json)

The earnings route takes an optional listing. It validates the market response for the date window, selects that listing and applies the 250-row cap in provider order. A query without a listing retains the market-wide behavior. A populated window with no match returns HTTP 200 with an empty result and retrieval metadata. Empty upstream data uses the existing HTTP 204 response. Source completeness remains unknown.

The isolated Chromium 156.0.8078.4 journey passed 23 browser assertions, with 16 HTTP 200 provider receipts and zero guard denials. The post-run comparison initially failed on a variable name in the document verifier. The corrected verifier passed offline against those same receipts, including chart marks and document comparisons. The retained source replay also reproduced the old market slice and the corrected Microsoft selection on the original capture. [Browser journey](../../tests/e2e/events-documents-workspace.spec.mts) · [Independent response comparison](../../tests/e2e/events_documents_oracle.py) · [Mounted API and SDK regressions](../../tests/providers/test_fmp_batch_b_installed_join.py)

The packaged controlled journey also passed 18 scenarios across 40 browser acquisitions with zero provider sends. It exercised missing values, clipping, recovery and saved state.

The Data API and Workspace images were built and tested locally. The source lock identifies both changes. [Pinned sources](../../sources.lock.json)

## Published alpha

[alpha-46047645104-1](https://github.com/norandom/QOpenBB/releases/tag/alpha-46047645104-1) was built from QOpenBB `66fd752157749b420f3540509fe708d25a09e27b`, Workspace `fe5e2e5e4a9aedc1f618f781faa02d22eaa990eb` and Data API `5efa7b6d24aae219a9dd80d4f61e0c6290f3368d`. The public Compose file and environment template matched the release commit byte for byte. All six anonymous pulls resolved to the expected image digests and carried both source pins. [Release manifest](https://github.com/norandom/QOpenBB/releases/download/alpha-46047645104-1/manifest.json)

| Service | Published digest |
| --- | --- |
| Workspace | `sha256:f7eb919b385a16299e0675519b21ec17d5b702b6a40ee0d10649fe89ff29215e` |
| Data API | `sha256:305b292976456e7fd78e304721ee7ecbc16d507624dd4bf2fe21c265a851af11` |

The published image pair passed the guarded earnings check in headless Chromium `156.0.8078.4`. All 16 FMP requests returned HTTP 200 and the guard denied zero sends. After changing the issuer to Microsoft and reopening the saved Workspace, the July 30, 2025 earnings row displayed actual and estimated EPS of 3.65 and 3.37 and actual and estimated revenue of 76,441,000,000 and 73,926,767,276. The oracle matched the values and all four chart marks to FMP on both acquisitions. Microsoft appeared at row 1,334 of 1,440 before the listing filter. All four evidence inputs were usable at reopen.

On the same released images, a Chromium File widget journey switched from Range Bar to Range Area using AAPL quarterly revenue and net income. The chart preserved both fields' extrema, regrouped the data by quarter when the category changed, and moved the horizontal axis when its position changed. Refreshing the file replaced FY2017–2020 with FY2021–2024 from the same 40-row FMP income statement capture. The journey checked 48 minimum/maximum pairs across six chart states and recorded zero browser or network errors.

The broad Workspace run exposed 20 failing suites. The subsequent focused runs covered the Range regression, the repaired tests and the Community replacement coverage for three retired renderers. The Workspace rerun passed 542 tests across 28 files, and the native Node suite passed 38 tests. Deployment of this pair on the owner's server awaits owner verification.
