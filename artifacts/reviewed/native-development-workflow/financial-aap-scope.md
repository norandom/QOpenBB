# Financial acceptance: raw-symbol scope correction

The corrected Podman image passed the Income widget browser journey. The following company-selection journey stopped because the test guard omitted a legitimate raw-symbol transition. Financial acceptance remains open; no automatic rerun occurred.

## Executed evidence

One authorized corrected batch used Workspace sha256:05e16ad56e7275a71edb3aadd4449063f3df40073713588b1f0dedee55e60053 and data API sha256:b3e56de1878d02f894d80111ba4ecff14b98292b9045ea6cc88e793f41a5f807.

- Income journey: passed in 27.1 seconds, one result, no retry or skip. This covers the existing real-data display, company/period changes, recovery and saved reopening assertions.
- Company initial journey: failed in 43.7 seconds at the final application diagnostics assertion. Profile and Income each returned HTTP 400 during an intermediate raw AAP selection.
- The stopped ledger records 24 FMP and 2 FRED attempted sends, plus two destination denials. No ceiling, ledger, persistence or process denials occurred. The API was stopped by the runner; the controller then stopped Workspace. Containers and private state remain retained.
- Synthetic failure and recreated-session company journeys did not execute.

The earlier DNS-failed attempt used zero provider sends and remains separate. Raw browser evidence, credentials and private configuration are not published.

## Cause and correction

The existing test explicitly types AAP, waits for Current Symbol: AAP, and then selects the AAPL listing. The Symbol control supports delayed raw-symbol submission, so Profile and Income legitimately acquire AAP before AAPL. Captured application requests confirm that transition. This is not evidence of a new clear/reset defect.

The guard admitted AAP autocomplete but only AAPL/MSFT Profile and Income. The correction adds AAP to those existing two endpoint families. Search scope, allowed hosts, GET-only transport, query keys, period/limit restrictions and cumulative maxima of 80 FMP/16 FRED are unchanged. No production application or image change is required.

The implementer reported 25 passing focused offline checks, including three AAP admission cases and six adjacent rejection cases. Independent [code review](aap-guard-review.md) verified the frozen hashes and bounded diff; it did not repeat those tests or approve live execution. The exact upstream wire query was not retained; upstream attribution follows the captured application symbol and inspected provider/guard contracts.

## Resume boundary

Request approval to retry the failed company journey and execute the remaining synthetic/recreated-state journeys, including AAP Profile and Income. Retain the passed Income result without repeating it. Carry the 24/2 usage into a distinct reviewed continuation, leaving at most 56 further FMP and 14 FRED sends. Do not clear prior claims, overwrite failed evidence, reset the allowance or claim the full financial task passed.

Retained local evidence under D:/BuildArtifacts/QOpenBB/native-financial-corrected: review.md, diagnosis.md and live-session/evidence/{0-initial,1-initial}/browser-results.json, failed-final-ledger.json and failed-stop.json. Guard correction review is under D:/BuildArtifacts/QOpenBB/aap-guard. Root helper and tests are tests/delivery/financial_budget.py and tests/delivery/test_financial_budget.py. Their current hashes and the historical frozen helper identity are distinct by design.
