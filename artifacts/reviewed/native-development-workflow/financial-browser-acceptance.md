# Native financial browser acceptance

Task 11.3 accepted on 2026-11-10. The existing financial journeys passed on native Windows with Podman Compose and Playwright, using the qualified Dagger-built application pair. Independent Astra review accepted the evidence and retained-state behavior.

| Journey | Result |
| --- | --- |
| Income values, company/period changes, recovery and saved reopen | Prior corrected-image run passed; exact report retained without repeating requests |
| Company name MSFT then symbol AAPL, linked research and saved login | Passed |
| Keyboard cancellation, entitlement failure and stale-search protection | Passed with synthetic failure responses |
| Actual container recreation, retained selection and fresh login | Passed with Profile, Income and FRED values |

Each new report contains one passed test, zero failed/skipped/flaky cases and zero retries. The native continuation runner exited 0. Cumulative attempted provider sends finished at **58 FMP / 6 FRED**, within 80/16 limits; this continuation added 34/4 to the preserved 24/2 ledger. Two historical destination denials remain recorded; the corrected continuation had no new denials. The owner authorized the necessary requests without further approval prompts for this verification.

Workspace image: `sha256:05e16ad56e7275a71edb3aadd4449063f3df40073713588b1f0dedee55e60053`, source `e1a12c3a031a23598f41166a0f91b8fb24ac2387`.

Data API image: `sha256:b3e56de1878d02f894d80111ba4ecff14b98292b9045ea6cc88e793f41a5f807`, source `2e60c0a7aff039eda5f14a9d494beaec822fb9c4`.

The AAP-only guard correction is root commit `e96d0e5`; production image inputs did not change. The frozen continuation identity is `f9b9e76e0214bb7b94637c3ab217e327dfc05b4b9452c704b081771ca029d08e`; its final receipt SHA-256 is `1576ef2b0ed46ba70b7076b260c777c00041d525b0ed5313a80a07bc391e43fd`.

Execution used the native pipeline Python with `-B D:/BuildArtifacts/QOpenBB/native-financial-remaining/run_live.py`, from the repository, with `PYTHONPATH` pointing to its pipeline. Private runtime configuration, provider payloads and raw reports remain under D:/BuildArtifacts; they are not public artifacts. The approved original offline proof and carried Income report remain hash-bound to the continuation.

See [independent review](financial-browser-review.md). This establishes the selected development workflow and financial journeys, not complete provider coverage, a new published release or an owner-server deployment.
