# Typed statement provenance contract accepted

Task 2 accepted on 2026-11-10 at API commit `b373da3f8d7`. The optional typed statement member preserves old envelopes and FRED serialization, validates row/source attribution and bounded facts, and requires documented convention support for known coverage. Old strict Python readers need the matching updated core.

TDD began with 2 failures and 54 passes. Independent review found baseline-valid fiscal label/date restrictions and unsafe parser messages; these were repaired, along with an arbitrary fiscal-year restriction. Final installed-package suite: **64 passed**, exit 0, independently repeated. No live requests or downstream integration are claimed.

Whole-file gate passed: financial metadata 221 physical / 135 logical / maximum function 12; statement model 149 / 102 / 17. Both satisfy 400/300/50. Final delivery normalized only CRLF to LF; the controller compared staged reviewed bytes with source and installed bytes and proved this exact transformation, with unchanged normalized text/AST. Metadata SHA-256: `38e77fca81ce8ee30bf3a28ded678bd444138a708f7ee4c3f21456a90672a590`; statement model: `b2da3225f74b93049c49175d7b3b154ad9d1e9ad97e9414049b028a741ae4169`.

[Independent acceptance](core-review.md) records the repaired implementation. Original RED, review failures, remediation and LF receipts remain locally under D:/BuildArtifacts/QOpenBB/statement-period-provenance/task2. Provider integration is restricted to approved annual/quarter queries; other Income query behavior stays unchanged. Source pins and generated consumers advance at the joined integration task, not on this standalone core commit. IA-B remains open.
