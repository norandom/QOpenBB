# Event contract freeze

Review the five JSON contracts before adapter work. They distinguish exact retained-model schemas from the proposed public schemas and procedural admission rules. The executable verifier checks fixture consistency and isolated Pydantic model behavior. It does not verify an installed Fetcher, mounted HTTP route, SDK or account entitlement.

Run from the Batch B root:

```powershell
D:/BuildArtifacts/QOpenBB/native-foundation/pipeline-venv/Scripts/python.exe -B tests/providers/fixtures/fmp_batch_b/events/freeze.py
```

`--write` intentionally regenerates the five contracts from retained declarations and the proposed schema definitions. Review generated differences before accepting them. The loader executes only retained model classes and validators, with native core declarations; it excludes Fetchers and transport imports. Pydantic is 2.12.5. No dependency installation or authenticated request is required.

## Financial decisions

[Unit evidence](unit_evidence.json) independently corroborates percentage-point input scale for the two published dividend examples. Output is a ratio: raw yield / 100 for any non-null value, including zero. This is a scale decision; annualization, trailing/forward basis and price-date conventions remain unknown. The generic FMP formula page and unrelated ratios endpoints do not establish this endpoint's scale. The retained divide-by-100 validators are compatibility observations, not financial evidence.

Historical adjusted amount becomes nullable to preserve absent source values. Calendar amount and adjusted amount remain independently nullable. Neither may substitute for the other. Dividend dates retain separate ex-, declaration, record and payment roles. Blank optional date strings become null; an absent required event date fails. No currency is inferred from a listing suffix.

Splits preserve positive finite new/old components. Historical components may remain null where the standard permits; a supplied zero, negative or nonfinite component fails. Both calendar components are required. A 1:10 reverse split remains numerator 1 and denominator 10. No price history is adjusted.

Earnings preserve actual and estimated EPS/revenue separately. Actual zero remains zero; unreported actual remains null. Report and update dates are civil dates. No confirmed status, fiscal period, currency or timezone is inferred.

## Procedural admission and clipping

Calendar dates are required and inclusive, at most seven civil days: January 1 through January 7 is valid; January 1 through January 8 fails before I/O. Calendars are market-wide and reject a symbol filter. History requires exactly one symbol. Historical dividend date bounds are independently optional and local; both provided bounds must be ordered. Explicit null is rejected instead of treated as omission. Limits are strict integers. HTTP numeric wire strings are admitted by the public policy in task 2.2, which also owns repeated scalar rejection.

One valid invocation permits exactly one stable endpoint acquisition. No loops, pagination, retries, alternative provider or fallback period are allowed. Validate every acquired row, including rows beyond the eventual cap, before clipping. Preserve source order and separate rows with the same event date. Do not sort or deduplicate.

Calendar rows cap at 250; historical splits cap at 100. Historical dividends forwards limit 1 through 100, default 20, then defensively caps to that requested limit before applying local ex-date filters. A nonempty limited acquisition filtered to no rows is successful empty output, distinct from safe transport's empty acquisition outcome. Full pages do not prove completeness. Runtime metadata reports actual returned count, effective inputs and observed clipping; upstream completeness remains unknown.

## Baseline incompatibilities and remaining verification

The retained dividend validators turn zero yield into null. Retained historical adjusted amount is required. Retained calendars insert implicit dates or issue multiple chunked calls, and earnings/dividend transformations sort rows. These behaviors are characterized, not accepted. The desired schemas and procedural rules supersede them in the owning adapter tasks.

The native Data standard allows extra row fields. Contracts retain this baseline; unknown provider fields must not receive invented financial annotations. Historical rows receive an exact requested listing only when source identity is absent; a supplied foreign identity rejects the acquisition. Calendar rows require their own nonblank listing.

Fixtures freeze schemas, aliases, field meaning and target values. Row-level strict civil-date rejection, symbol attribution, validate-before-clip behavior, transport interception, effective metadata, duplicate preservation, eighth-day rejection through all public entry points and installed serialization require the owning adapter and join tests. None are marked production-verified here. Tests and documentation are excluded from production 400/300/50 caps; no production file changes belong to this task.

Official documentation was accessed on 2026-11-17: [dividends](https://site.financialmodelingprep.com/developer/docs/stable/dividends-company), [dividend calendar](https://site.financialmodelingprep.com/developer/docs/stable/dividends-calendar), [splits](https://site.financialmodelingprep.com/developer/docs/stable/splits-company), [split calendar](https://site.financialmodelingprep.com/developer/docs/stable/splits-calendar), [earnings calendar](https://site.financialmodelingprep.com/developer/docs/stable/earnings-calendar). Endpoint names and economic roles are documented. Product date/row/call caps are local policy. Retained archive member hashes are recorded in each contract; foundation provenance owns archive and notices.
