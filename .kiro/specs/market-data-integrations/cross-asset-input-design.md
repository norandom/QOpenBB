# Cross-asset and macro input verification design

Status: design owner-approved, 2026-11-18. Implements the approved [requirements](cross-asset-input-requirements.md). No live request is sent before the harness review in task 4 is accepted.

## Decision summary

Verify the 14 inputs against the published data image, through its installed native routes, with the send-guard pattern already reviewed in Batch B. Record the results in one new reviewed reference file. Change no production code and build no new image.

| Decision | Choice | Reason |
| --- | --- | --- |
| Runtime under test | Published data API image `sha256:3db18506631972b3a3a176f45069cdac6574af7c35543e261ce7153b58ed25e4` (alpha-44340458084-1), started alone | The evidence then describes what installations actually run. No Workspace is needed, because this slice has no dashboard. |
| Routes | Existing `equity/price/historical` (FMP) and `economy/fred_series` (FRED), plus `equity/profile` for ETF identity | Requirement boundary: no new adapter. |
| Send control | A frozen request matrix and a one-slot-per-send guard derived from the reviewed Batch B harness, extended to count FRED sends | Every outbound request is planned, counted and attributable (5.1). |
| Comparison | A standard-library oracle that reads only the private raw captures and the public results | Independent of adapter code (2.3). |
| Result record | New `docs/reference/cross-asset-inputs.json`, with a schema and a contract test | The coverage index is keyed by model, not by symbol, and is packaged into the image. A separate record avoids an image rebuild. |

## Request matrix

Frozen before the first send: 26 route calls, which cause 34 provider requests. Each FRED series call makes two requests, one for observations and one for series metadata. Reruns need a recorded reason and a new slot. The FRED client's automatic retries are switched off for the run, because a retry would be an unplanned request.

| Group | Calls | Query |
| --- | --- | --- |
| ETF recent prices | XLK, DBC, GLD, XLE, XLB, SPY (6) | daily, 2026-08-03 to 2026-11-13 |
| ETF early-window probe | same six (6) | daily, 2007-01-03 to 2011-12-30, the five-year maximum |
| ETF identity | same six (6) | profile by symbol |
| FRED series | DFII10, T10Y2Y, T10YIE, DTWEXBGS, DCOILWTICO, DHHNGSP, STLFSI4, NFCI (8) | one series per call, no date bounds |

The requirements estimated about 20 requests. The six identity calls answer their open question about instrument type and exchange; they bring the plan to 26 route calls. Amendment, 2026-11-18: the task 1 review found that the count of 26 understated provider requests. The plan is 18 FMP and 16 FRED requests, 34 in total. The owner set no fixed cap; the corrected count is reported to the owner.

The matrix identity is the SHA-256 of its canonical JSON form, so it does not depend on line endings. The FRED series route does not return the source institution, so that attribute stays unknown unless another reviewed source supplies it.

## What is checked

- **Identity (1.1–1.4).** The profile response supplies instrument type, exchange and currency where FMP provides them. A missing attribute is recorded as unknown. If the profile route rejects an ETF, that outcome is recorded and the attribute stays unknown. FRED metadata (title, units, frequency, seasonal adjustment) comes from the series response; it does not include the source institution.
- **Price meaning (2.1–2.4).** Each public row is compared with its raw row: date, open, high, low, close, volume. The record states the served adjustment basis (`splits_only`) and that dividends are excluded. The oracle counts gaps against the exchange's weekday calendar, duplicate dates and ordering faults. A weekday gap is reported, not judged: holidays are not modelled. Missing FRED observations must stay missing.
- **History depth (3.1–3.4).** Earliest and latest returned dates per input. An empty or truncated early window is recorded as observed, with the response's own truncation metadata.
- **Provenance and display status (4.1–4.4).** Provider, route, effective query and retrieval time come from the response metadata. Display status is assigned from the series notes returned by FRED: a "Copyright" marker means third-party copyrighted and restricted. ETF prices are provider-licensed. A status that cannot be established from the response is unknown.
- **Bounded verification (5.1–5.5).** The guard ledger lists every send with its case and purpose. An entitlement denial marks the input blocked and stops its dependent calls. Raw captures stay under the private evidence directory.

## Result record

`docs/reference/cross-asset-inputs.json`, one entry per input:

- `id`, `role`, `provider`, `route`
- `identity`: instrument or series attributes, each a value or `unknown`
- `price_basis` (ETFs): adjustment basis, `excludes_dividends`
- `history`: earliest and latest returned dates, row counts, truncation, gap counts
- `display_status`: `government-source`, `provider-licensed`, `third-party-copyrighted` or `unknown`, with the evidence phrase category, not the text
- `verification`: `verified`, `blocked-entitlement`, `failed` or `unverified`; checked date; image digest; evidence hashes
- `limits`: the route limits and the statement that history depends on the installation's provider plan

A contract test validates the schema, requires all 14 inputs, and fails if a `third-party-copyrighted` input is marked usable in stories.

## Boundaries

- No change to provider adapters, the data service or the Workspace. If an existing route cannot serve a candidate, the task stops and returns to the owner; this design does not authorize an adapter.
- No returns, factors or regime rules.
- The guard harness is private verification tooling under the evidence directory, not shipped code.

## Risks and how they are handled

| Risk | Handling |
| --- | --- |
| The price route rejects ETF symbols, or FMP's plan excludes ETFs | Recorded as failed or blocked; the story's proxy choice returns to the owner. |
| The profile route is company-shaped and returns little for a fund | Attributes recorded as unknown; a recorded manual source is a follow-up decision. |
| An early window returns nothing because of the plan tier | Recorded as observed (3.3); `factor-signals` then designs for the available depth. |
| A FRED series turns out to be copyrighted | Marked restricted and excluded from stories (4.3). |
| Large FRED responses | The route's 100,000-row limit applies; the longest candidate is about 10,000 rows. |

## Evidence and acceptance

- Harness review before any send, as in Batch B task 5.1: offline rehearsal with synthetic responses and zero sends, guard unit tests, frozen identity.
- One live run of the matrix. Independent financial review of the comparison and of every statement in the result record.
- Documentation: a "Cross-asset and macro inputs" checkpoint in `docs/provider-coverage.md`, including the FRED notice; breadth evidence for requirements 2.3, 3.4, 4.8 and 5.6 limited to what is verified.
- The sanitized mirror receives the reviews and a summary only. Check-only CI must pass before acceptance. No image is built.

Disproof condition: if the oracle finds any value difference between a public row and its raw row, or an input cannot be tied to one unambiguous instrument or series, that input is not verified.
