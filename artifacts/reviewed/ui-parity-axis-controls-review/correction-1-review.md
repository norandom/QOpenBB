# Preserve original row bounds before validating the fixture

Approve collector correction `d399418ffe848bc1f0137ba60613b02f1a9c008077d2884d720df81fa062600a` for a separately granted bounded attempt. The plan, fixture, cases and limits are unchanged. Ten frozen-file hashes match; the corrected offline checks were freshly rerun and all 24 passed. See [identity verification](correction-1-verification.json).

The first attempt stopped at entry with `Four-row chart range required`: nine actions, four edits, zero cases and zero settled checkpoints. Its executed harness matches the reviewed manifest `e95ec51e…`. The earlier preflight did not catch its incorrect requirement that row bounds equal 0 and 3. Prior caption evidence preserves own null start/end bounds for a whole-table chart. The failing axis attempt did not save its model before asserting, so its actual rejected bounds are unavailable; the diagnosis must not present those missing values as observed.

The correction writes finite identity before assertions, accepts only paired null bounds or literal 0/3, and separately saves and validates exactly four Period/Revenue/Operating Income rows from the already permitted getOptions data projection. Every amount and period must match its fixture and ordinal. Null bounds are retained as null, with no normalization or injected engine data. This repairs the collector prerequisite rather than changing original behavior.

The failed attempt's browser/context and listener were closed or disposed; its container, owned state and credential file are absent, with an empty remaining-owned-state list. The failure and cleanup receipts remain intact. This review performed no new runtime and does not establish any axis-case outcome, candidate acceptance or persistence.
