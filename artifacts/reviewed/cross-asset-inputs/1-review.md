# Cross-asset input verification, task 1: independent review

- VERDICT: APPROVED
- Task: 1, freeze the request matrix and the result-record contract
- Reviewed: 2026-11-18, second review. The first review rejected the task; its three Important findings are closed.
- Reviewer: fresh-context Claude subagents following kiro-review (reported fallback for gpt-6-astra, which is not available in Claude Code).

## First review (rejected)

1. Each FRED series call makes two provider requests, so 26 route calls cause 34 provider requests; the matrix listed no per-request plan.
2. The matrix hash depended on the checkout's line endings.
3. The contract accepted a verified input without an image digest, with boolean history dates and with a free-text date.

## Second review (approved)

- Scoped test: 22 passed. After two follow-up suggestions were applied (below), 24 pass.
- Send lists match the provider code for all three routes: 12 price, 6 profile and 16 FRED requests, 34 in total. FRED retries are off and the cache is bypassed.
- The matrix identity `3f960e31e0c16e574cdb89a2856d235f9715469de6eaf8090aefd40efaf80130` is the same for LF and CRLF copies, and the record binds it.
- 82 reviewer mutations against the contract: every over-claim is rejected by schema or assertion.
- The generator reproduces the matrix, schema and record byte-identically.
- The design and task plan agree with the matrix: 26 route calls, 18 FMP and 16 FRED requests. The owner confirmed 34 requests on 2026-11-18.
- No placeholders or secrets; no production code touched.

## Suggestions and their handling

- Applied: the fund-type check is now an allowlist (`etf`, `fund`, `unknown`), and a missing type fails by assertion.
- Applied: the design no longer lists the source institution as FRED series metadata.
- Deferred to task 6, before any input is marked verified: stricter `retrieved_at`, calendar-valid dates, `earliest` not after `latest`, non-null `excludes_dividends` for a verified ETF, gap counts paired with gap ranges, non-empty FRED identity and effective query.
- For the task 4 harness review: a provider redirect would be an extra request; the retry setting is read at import; fetcher parity between the working tree and the published image is shown by the in-image rehearsal.
