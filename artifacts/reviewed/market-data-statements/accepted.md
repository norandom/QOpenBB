# FMP statement adapter acceptance

Tasks 2.3 and 2.4 are source-accepted on 2026-10-28 after independent financial review. Balance source commit: `072a6c6c2bf374d4f33b43bbed5d95c5eff34275`; cash source commit: `93d34aebaef3d1c0ddaaa981f5aefd9bdb2f546d`.

Balance:20 focused tests pass; cash:34 focused tests pass after strict-bound and stock-date repairs. Independent combined run54passed; transport baseline18passed. Owning FMP Ruff passes explicitly. The combined Node24.22.1 quality check passes78files without errors or violations. Final packaging normalized LF/EOF only; final source measurements/hashes are in final-source.json. This does not change calculations.

Adapters preserve aliases, fiscal/filing dates, original acquisition timestamps, signs, zeros, nulls and row currencies. Queries are single-symbol annual/quarter with quarterly alias, strict integer1..1000 bounds and default5. Latest-first ordering retains duplicate order; observed clipping is disclosed. Balance amounts are instant stocks. Cash flows retain annual/discrete-quarter/unknown bases from reported labels; opening/closing cash are instant stocks, and unknown opening dates are explicit.

Balance's intermediate failing newline-validation regression preceded repair. Cash has no historical preimplementation RED: the controller serialized suite access after implementation. A transparently labeled postimplementation pre-repair sensitivity check produced5expected failures, proving strict bounds and stock metadata checks detect those regressions. No historical testing chronology is inferred.

Provider registration, installed API/widget contracts, live provider access, entitlement and image publication remain open. This acceptance adds data adapters, not house financial modeling. Existing catalog still exposes only its accepted baseline commands.
