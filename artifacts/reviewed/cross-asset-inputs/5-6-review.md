# Cross-asset input verification, tasks 5 and 6: financial review

- VERDICT: APPROVED
- Tasks: 5 (live matrix run) and 6 (comparison and financial meaning).
- Reviewed: 2026-11-18, two rounds. The first round rejected the record on two points; both are fixed.
- Reviewer: fresh-context Claude subagents following kiro-review (reported fallback for gpt-6-astra, which is not available in Claude Code).

## Live run (task 5)

- Exactly the frozen matrix ran once: 34 provider requests (18 FMP, 16 FRED), in plan order, all answered with status 200, no guard denial, unique single-use slots.
- The run is bound to the accepted harness: matrix identity, image digest, harness file hashes and the acceptance hash agree across ledger, report, summary and record.
- No key material is present in any written file.

## Independent recomputation (task 6)

The reviewer recomputed every comparison with a separate standard-library script.

- Prices: 40,020 fields equal the raw provider rows by date. Each fund returned 74 rows for the recent window and 1,260 for the 2007 to 2011 window, with no duplicate or ordering fault.
- FRED: 54,146 rows equal the raw values by date. Missing observations stay missing; none became zero.
- Every number, date, retrieval time, effective query and evidence hash in the record matches.
- The fund weekday gaps equal the U.S. exchange holidays exactly: 43 in the early window and Labor Day 2026 in the recent one.
- "Excludes dividends" is supported by the route metadata and the raw price fields.
- The record holds no raw price, observation value or series notes text.

## First round (rejected) and fixes

1. The record gave the funds' exchange as "AMEX", which is the provider's code. The record now states the venue from the same provider response, New York Stock Exchange Arca, and keeps the code separately.
2. The contract test accepted a dividend over-claim. It now requires split-adjusted prices to be recorded as excluding dividends.

Also fixed from the suggestions: the test rejects further over-claims (series typed spot without a provider title saying so, limits without the plan statement, missing row or missing-observation counts, a source claim in a series identity); fund entries carry early-window fault counts and retrieval time; Henry Hub is typed spot because its provider title says so.

## Owner decisions of 2026-11-18

- FRED data are public. QOpenBB is an academic, MIT-licensed project that ships no provider data.
- Stories attribute by naming the source in the chart or widget headline.
- All eight FRED series are therefore usable in stories. Four are labelled public domain on their FRED page (government source); four are published by Federal Reserve Banks and labelled citation required (public source). Institution and label are recorded as observed.

## Second round (approved)

- 47 contract tests pass. Of 79 reviewer mutations of the filled record, 65 were rejected, including every over-claim from the first round.
- After the review, two of the remaining guard gaps were closed: the venue name must differ from the provider code and must not be "unknown", and a named source institution must not be "unknown".

## Open items carried forward

- The contract does not require a rights label, does not tie status to the label, and checks the page reference only loosely.
- The public FRED pages were read through a summarising fetch, not raw HTML.
- Henry Hub has about 1,400 missing days across the 2000s and WTI 122 in 2003; factor work must handle them.
- WTI has role "oil-spot" and type "unknown", because its provider title does not say "spot".
- Fund holdings (bullion for GLD, futures for DBC) are not in the record and belong in the task 7 documentation.
