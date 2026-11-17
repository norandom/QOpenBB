# FMP successful empty-list acquisition correction

2026-11-17. Bounded implementation correction to the approved Batch A empty-result contract (requirement 4.5 and design Typed row and financial meaning). Adapter lanes remain paused until independent review and compatibility verification accept this correction. The eleven operations, 26 tasks and 48-request ceiling do not change.

## Observed conflict

The existing FMP response callback and list helper both classify an HTTP-200 JSON `[]` as missing data. Batch A requires successful empty arrays. A read-only debugger reproduced both gates and demonstrated that native Fetcher execution and OBBject JSON can carry an empty AnnotatedResult with acquisition metadata. The debugger's in-memory candidate is feasibility evidence, not implementation acceptance.

## Bounded interface

Add explicit keyword-only `allow_empty: bool = False` to `response_callback`, `get_data`, and `get_data_many` in `openbb_platform/providers/fmp/openbb_fmp/utils/helpers.py`.

- Only a successful actual top-level JSON empty list is accepted when the caller explicitly opts in. Existing callers retain their current default behavior.
- Consume and forward the option explicitly; never pass it to HTTP request kwargs.
- Status failures, provider error envelopes and invalid JSON retain their existing ordering and safe typed/legacy categories. Empty dictionaries, null, malformed rows and scalar payloads remain failures.
- A missing named sub-dictionary and an empty extracted sub-dictionary retain their existing failure behavior. Do not mistake a derived empty list for a successful top-level response.
- Create FMPAcquisition in get_data after the successful request completes and retain the exact retrieved_at through get_data_many. Adapters must not fabricate receipt timestamps after catching errors.
- Each Batch A array adapter opts in explicitly and makes at most one request. No retry, fallback or result-schema change is introduced.

The existing admission interfaces and frozen query/result contracts remain unchanged. Optional OBBject DataFrame/LLM/NumPy/Polars conversions and Fetcher.test's nonempty testing assertion are outside this repair; normal OBBject JSON is the empty-result acceptance surface.

## Ownership and completion

Controller-owned repair paths are the API helper above, root `tests/providers/test_fmp_empty_acquisition.py`, and the exact helper ownership entry in `.kiro/complexity/data-api.json`. Existing transport and baseline tests are read-only. Adapter workers retain their original endpoint files and resume only after this shared correction is accepted.

The helper baseline is 342 physical lines, 164 logical units and 27 in its largest function. The actual modified whole file must pass 400/300/50 and the combined inventory gate. No exception is proposed.

Implementation and independent compatibility review must verify:

1. Typed and legacy default rejection, opt-in empty-list success and nonempty parity through real helpers with intercepted transport.
2. HTTP 401/403/404/429/500, error envelopes, invalid JSON/scalars/rows, transport redaction and unchanged Retry-After behavior.
3. Missing/null/empty/malformed named sub-dictionaries remain failures; no option leaks into request kwargs.
4. Exactly one intercepted request and exact acquisition receipt timestamp preservation under a controlled clock.
5. Native Fetcher.fetch_data to OBBject JSON retains empty results and financial metadata; report the dedicated test boundary accurately.
6. Existing transport/baseline compatibility checks pass and the selection/schema admission source hashes remain frozen.

Before accepting each adapter, test its actual Fetcher with real helpers and an intercepted empty HTTP array. Tasks 4.1/4.2 must additionally prove actual generated SDK and mounted HTTP return successful empty JSON and metadata. Dedicated prerequisite fixtures cannot substitute for that production join.

No live request is needed for this correction. Preserve failed baseline probes and distinguish them from the final implemented-source evidence.
