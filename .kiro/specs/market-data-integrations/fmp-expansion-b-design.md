# FMP Batch B design for events and company documents

Extend the 21 accepted FMP models with eight operations. An analyst can inspect corporate actions and earnings dates, read the supplied news excerpt or transcript inside Workspace, and identify filings by company, date and form. The [approved requirements](requirements.md) and [expansion inventory](fmp-expansion-inventory.md) own scope. This amendment is for owner review.

## Source boundary

Use root c2c4e04172eb3a532f4b65820c3bac0b575e98c7, API a7c6ae2139b4dcc16571d0c23ade483a114a0068 and Workspace bf180ef506286886da224df9ff184cd1ace2397e as the baseline. Resolve vendor junctions into isolated Batch B worktrees before runtime edits. Recover only the eight members below from the retained FMP 1.6.1 archive identified in the inventory. Retain member hashes and notices. The provider owns acquisition and financial meaning. Workspace owns presentation and saved choices. Company Research peer state, house modeling and deployment retain their own contracts.

## Public query contracts

REST paths below follow /api/v1/. SDK commands use the same dotted path. Require explicit REST provider=fmp and preserve native SDK provider resolution. Apply selected-variant validation at HTTP, generated SDK and direct Fetcher boundaries. One valid invocation permits one upstream call. Use the accepted safe transport including its empty-list policy. Reject unknown parameters, repeated scalar HTTP inputs, multiple symbols, invalid dates, inverted windows, explicit null bounds and boolean integers before I/O. All ranges below are inclusive product limits.

| FMP model / adapter module | REST route | Stable operation and accepted financial inputs |
| --- | --- | --- |
| HistoricalDividends / historical_dividends | equity/fundamental/dividends | dividends. Require one symbol. Forward limit 1–100, default 20. Optional start_date and end_date filter the fetched ex-dates locally. Disclose that the upstream limit applies first. |
| HistoricalSplits / historical_splits | equity/fundamental/historical_splits | splits. Require one symbol. Cap returned rows at 100. |
| CalendarEarnings / calendar_earnings | equity/calendar/earnings | earnings-calendar. Require start_date and end_date, spanning at most seven calendar days inclusive. Forward from/to. |
| CalendarDividend / calendar_dividend | equity/calendar/dividend | dividends-calendar. Same date contract. |
| CalendarSplits / calendar_splits | equity/calendar/splits | splits-calendar. Same date contract. |
| CompanyNews / company_news | news/company | news/stock. Require one symbol, forwarded as symbols. Optional paired dates start_date/end_date span at most 31 days, forwarded as from/to. page 0–99 default 0, limit 1–50 default 10. Stock subtype only. |
| EarningsCallTranscript / earnings_call_transcript | equity/fundamental/transcript | earning-call-transcript. Require one symbol, year 1900–2100 and integer quarter 1–4. Forward all three. No availability probes or period substitution. |
| CompanyFilings / company_filings | equity/fundamental/filings | sec-filings-search/symbol. Require one symbol and both dates spanning at most 365 days. Forward symbol/from/to/page/limit. page 0–99 default 0, limit 1–100 default 20. Form type is an output. |

Calendars are market-wide, capped at 250 rows. Validate rows before clipping, preserve source order and report observed clipping, effective query and actual count. Distinguish empty acquisition, locally filtered empty results and malformed responses. Keep unknown completeness explicit. A full page or historical filter cannot establish exhaustive history. Check docs, SDK default coercion and wire spelling before freezing synthetic fixtures. Reopen the affected contract if characterization contradicts it.

## Financial results

- Dividends map date to ex-dividend date. Preserve declarationDate, recordDate and paymentDate separately, dividend and adjDividend as distinct cash amounts per share, and zero as a value. Keep missing currency and adjustment methodology unknown. Freeze the upstream yield scale before exposing a converted ratio. Unresolved scale blocks that mapping.
- Splits retain numerator (new shares) and denominator (old shares) separately, each positive and finite when supplied. Never infer a missing component. Preserve the event date and company identity. No adjustment to price history.
- Earnings preserve report date, last update and separate estimated and actual EPS and revenue. Zero is distinct from an unreported actual. Leave unknown confirmation status, fiscal period and time zone explicit.
- Stock news maps publishedDate to publication time, site and publisher to distinct source/publisher attribution, symbol to company linkage, text to excerpt and url to article link. Publisher alone does not identify a journalist. Nonempty excerpts are partial. Headlines without text are metadata-only.
- Transcripts require exact normalized symbol, year and quarter in the returned row. Reject duplicates and mismatches. An empty list means unavailable. Preserve supplied event timestamp and text verbatim, including whitespace. A nonblank transcript has unknown completeness unless the source explicitly establishes completeness. Missing required content is a validation failure.
- Filings preserve filingDate, acceptedDate timestamp precision, form type, string CIK, company linkage and separate document/index URLs. Label inline coverage metadata-only. No document retrieval.

Use the installed standards and typed FMP row extensions where source attribution or time precision would otherwise be lost. On narrative rows expose content_status with partial, metadata_only, completeness_unknown or full (requires explicit source evidence). Freeze aliases, field names, nullability and annotations in reviewed fixtures before adapter fan-out. Preserve civil dates, source time precision and timezone uncertainty. Emit the accepted AnnotatedResult financial metadata with effective query, retrieval time, limitations, field origins and bounds. Keep credentials out of schemas, output, logs and evidence.

## Runtime, catalog and Workspace ownership

1. Controller owns services/data-api/pyproject.toml and uv.lock. Install local openbb-news 2.0.0, review feedparser/lxml and core extras in the lock, and verify installed origin. The retained openbb_news/router.py imports news and RSS. Compose only the company command for the owned deployment. Verify a clean startup, SDK, mounted route inventory, OpenAPI and catalog including absence of new RSS/world surfaces. Preserve existing routes.
2. Freeze aliases and strict input admission under tests/providers/fixtures/fmp_batch_b/. Each adapter worker owns its named file under openbb_platform/providers/fmp/openbb_fmp/models/ and root tests/providers/test_fmp_<module>.py. Controller owns provider registration, provenance, shares the existing financial_query_policy.py and native admission logic, and updates exact-set tests for 21 preserved and eight additional models. Keep oversized equity routers untouched. Check original SDK, REST and Fetcher paths with invalid and valid inputs.
3. Controller owns sources.lock.json and generated contracts, including openapi.json, routes.json, datasets.json, widgets.json and compatibility.json. Add catalog regression tests under tests/contracts/. Preserve existing widget IDs and source-qualified parameters. Report documented coverage, installed capability, entitlement and browser acceptance separately.
4. Use generated tables for the five event operations. Calendar widgets own their market-wide dates. Use a dedicated Workspace terminalpro/src/components/Widgets/CompanyDocuments/CompanyDocuments.tsx detail view for three narrative datasets, with controller-owned renderer registration/catalog mapping. Bind through normal widget acquisition. Provide a keyboard-operable row selector, readable wrapping, focus return and visible company, date, source, content status and period. Render escaped text. Allow optional validated HTTP(S) links and suppress remote images and link prefetch. Save only dataset and query choices. Reject superseded responses, clear evidence on context change, and label same-context results stale after refresh failure. Preserve existing peer storage and app layout. Verify exact registration and persistence file paths against the host before task assignment.

## Evidence and dependency order

| Criteria | Acceptance evidence |
| --- | --- |
| 1.1–1.4, 2.3–2.6, 5.1–5.3, 6.1–6.3, 6.5 | Frozen query/row schemas, installed discovery, zero sends on invalid input, one bounded send on valid input, complete baseline identity comparison and distinct empty/partial-page cases. |
| 3.1–3.3, 4.1–4.6, 6.4 | Dated and attributed rows, amount and ratio bases, zero/null, estimated vs actual, news excerpt, exact transcript period, linked filing and sourced timestamps. Include foreign rows and mismatched periods. |
| 7.1–7.5, 8.1–8.5 | Typed failure and recovery, secret-free records, visible content and limitations, saved context, keyboard interaction, unsafe link and literal markup fixtures, real-data comparison through installed runtime. |

Controller freezes contracts and the executable complexity inventory first. Enforce 400 physical lines/file, 300 logical units/file and 50/function. Keep dependency installs, joins and heavy checks serialized. Independently review bounded tasks before acceptance. Verify actual package installation, generator and runtime, then compare each acquired response with its public result. An entitlement denial blocks the corresponding live case. Keep raw licensed material private. Publish redacted counts, hashes and synthetic examples. Update breadth, delivery docs and release evidence only for verified scope. Dagger builds milestone images after the normal release gates.

Propose a fresh 36-request FMP ceiling: 16 for direct and installed executions across eight operations, four focused financial/period comparisons, ten for initial load and saved reopen across five representative widgets (history, calendar, news, transcript, filings), and six reserved for diagnosed reruns. Record exact symbols, periods, windows and isolated browser settings before the first call. Count every outbound send including errors and background requests. Compare moving sources against each native call's own capture. Stop at the ceiling. The task plan and live allowance require owner approval.
