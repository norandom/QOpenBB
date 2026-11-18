# Cross-asset input verification, task 4: harness gate review

- VERDICT: APPROVED
- Task: 4, review of the frozen harness before any live send. Covers the task 2 harness and the task 3 comparison oracle.
- Reviewed: 2026-11-18, second review. The first review rejected the harness; its four findings are fixed.
- Reviewer: fresh-context Claude subagents following kiro-review (reported fallback for gpt-6-astra, which is not available in Claude Code).
- Scope of approval: one live run of the frozen matrix, 34 provider requests, at the identity below.

## Reviewed identity

- Matrix: `3f960e31e0c16e574cdb89a2856d235f9715469de6eaf8090aefd40efaf80130`
- Image: `sha256:3db18506631972b3a3a176f45069cdac6574af7c35543e261ce7153b58ed25e4`
- Harness files: as recorded in `reviewed-identity.json` beside this file (nine Python files).

## First review (rejected)

It established that no unplanned request can leave the container: redirects are denied at each hop, a rate-limit response produces one request, the cache is bypassed, and only the guarded HTTP client is loaded. It found four defects:

1. A provider response echoing a key made the live script discard the whole run record.
2. The guard's send-to-send floor could deny the planned second FRED request.
3. An HTTP 402 plan denial did not stop an input's remaining calls.
4. No red-phase evidence for tasks 2 and 3.

## Second review (approved)

All checks ran offline, with no network and sentinel keys.

- Unit tests: 23 pass. Offline rehearsal: 26 calls, 34 synthetic interceptions, 0 sends, 0 denials.
- Six live-path scenarios against a loopback server, through the real live entrypoint and the real in-image program:
  - Key echo: raw output held the sentinel keys six times; the written document, oracle report, summary and stderr held none. All four files were written even on a failing exit.
  - Slow first connect: both FRED requests of a call were admitted, with no denial. A clean run gave 34 of 34 sends, and the ledger equalled the server log.
  - Denials: a 402 and a 403 each stopped that input's remaining calls. 401, 429, 500 and a FRED 400 did not block.
  - Stops: a redirect produced one denial, a stopped run and a failing exit. Nothing beyond the plan was sent in any scenario.
- The comparison oracle reports no fault on a clean run and catches value changes, dropped, duplicated or shifted rows, a missing observation turned into a number, metadata changes, a capture bound to the wrong input and a tampered capture.
- Red evidence: seven new tests fail against the old code and pass after the fix.

## Limits accepted with this approval

- Redaction matches the literal key. The controller confirmed, without displaying them, that both installation keys are alphanumeric, so encoded forms are identical.
- If the container is killed or the host times out, the ledger is lost and the send count must be treated as unknown.
- A redacted capture on an acquired call would be reported as a capture-binding fault, not compared.
- A 401 does not stop an input: an invalid key would spend that provider's planned requests, each recorded.
- An off-host redirect causes a connection attempt to that host before the denial; no request or key is sent.
- There is no single-call rerun path. A diagnosed rerun needs a harness change and a new acceptance.
