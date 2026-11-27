# Events and Documents controlled packaged verification

The controlled journey exercises the installed Workspace catalog and story with synthetic responses at the browser's mounted data routes. Its upstream guard counts provider sends independently. This evidence covers task 5.3. Task 5.4 owns real FMP acceptance.

## Candidate and reproduction

| Service | Source revision | Installed image |
| --- | --- | --- |
| Workspace | `4a079a0384df7151fde8ce3b90d2af6e1f50a1b9` | `sha256:25fcec114dcd25a6cbb0edacadbfd3b29ff625557efd159ed5aeb73c763099f4` |
| Data API | `5583c958d35282cb59037aae8218cec31d540697` | `sha256:c5cbb466ec28790c38cfac02dab3c9bc7b8f51740f27874b91bcf73eb5ceb524` |

Run from the QOpenBB root on Ubuntu with the pinned Node 24.22.1, the isolated Playwright browser cache, and Docker.

```bash
env -u FMP_API_KEY -u FRED_API_KEY \
  PATH="$HOME/.nvm/versions/node/v24.22.1/bin:$PATH" \
  PLAYWRIGHT_BROWSERS_PATH="$HOME/.cache/ms-playwright" \
  DOCKER_HOST=unix:///var/run/docker.sock \
  pipeline/.venv/bin/python tests/e2e/run_events_documents.py controlled
pipeline/.venv/bin/python -m pytest tests/e2e/test_events_documents_verification.py -q -o addopts=''
```

The browser compares each GET with the initial, edited, reopen or controlled-only tuple. The controlled retry uses the unchanged MSFT news window of 2025-07-28 through 2025-08-04, page 1 and limit 10. The AAPL and MSFT transitions reacquire only the company documents and retain the market window. [Base query plan](../../../tests/e2e/events-documents-plan.json) · [Controlled responses and extra tuples](../../../tests/e2e/events-documents-controlled.mts)

## Observed cases

| Area | Browser evidence |
| --- | --- |
| Earnings | Moving the market window produces a 250-row clipped slice, with both same-date MSFT rows inspectable in source order. An actual EPS of zero is plotted and a missing estimate has no mark. The 9,007,199,254,740,993 revenue token is exact in the source detail. The oracle compares the painted mark coordinates, row and field identity, exact value and units against the installed fixture. An empty market response clears the calendar. A nonempty market slice with no issuer match keeps wider coverage unknown. |
| Documents | Filing date, acceptance precision, string CIK, form and separate links remain inspectable. Transcript and news whitespace and markup-shaped text render literally. Safe links expose their exact targets with opener and referrer protection. Invalid schemes, userinfo and remote embeds produce no actions or fixture-host traffic. Metadata-only and partial-content labels remain visible. |
| Recovery and conclusion | A 204 transcript is unavailable for the selected period. A mismatched fiscal quarter fails evidence validation. HTTP 403 displays a Workspace-access failure and offers no retry. Invalid news bounds dispatch no GET. A typed timeout offers a same-query retry while the calendar, filings and transcript citations remain byte-identical. The browser observes evidence available, partial, pending and insufficient conclusions. |
| Keyboard and races | Light and dark theme each exercise source-detail focus, return focus to the invoking controls and keyboard navigation to the conclusion. The earnings heading takes focus after its invoking row disappears. In each theme, the news heading takes focus as the document row disappears in MSFT → AAPL → MSFT. Held AAPL responses are released after the second MSFT acquisition. The superseded success or failure leaves MSFT evidence and its conclusion intact. |
| Persistence | Workspace saves the selected query and chart choices. A fresh authenticated browser context restores those choices and makes four fresh requests. The downloaded template preserves the widget configuration. Strict storage/state comparison and a scan of both payloads check for response content. |

The first browser pass completed the controlled cases while the launcher held an earlier in-memory oracle. The second run passed the browser and oracle but returned exit 1 because the launcher treated injected failures as fatal in controlled mode. The final launcher validates the exact controlled exception counts and retains the blocked and incomplete exit gates for live mode.

## Final result

The launcher exited 0 on 2026-11-27. Chromium 156.0.8078.4 passed the journey with one headless worker. The oracle verified 18 controlled cases, 34 browser acquisitions, 37 painted earnings marks and 28 document rows. The upstream ledger recorded zero sends and zero guard denials. The isolated browser emitted the two expected console errors for the injected HTTP 403 and HTTP 400. Six canceled acquisitions matched the two superseded AAPL stages and their three document slots. No uncaught browser exception, unexpected console or relevant network error, or fixture-host request was observed. The runtime stopped and retained its disposable state under the private run directory.

The disappearing-row checks use the real browser focus state and apply the query change without focusing the external control, so the test can observe fallback from the disappearing detail. Ordinary exploration and close use keyboard events.

The 11 focused verification tests passed. This task changes test harness files and evidence only. The production configurations, provider guard and frozen live tuples are byte-identical to the accepted verifier. [Sanitized counts and harness hashes](summary.json)
