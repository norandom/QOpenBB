# Packaged statement widgets accepted

APPROVED for statement-period provenance task 6 on 2026-11-10. The local packaged Income, Balance and Cash journey passed with source-backed displayed values, annual/quarter controls, refresh, invalid-input recovery and saved selections after fresh-login reopen. Task 7 publication remains open.

## Independent review verdict

- VERDICT: APPROVED
- TASK: 6, native packaged statement acceptance; requirements 3.1, 3.3, 4.2 and 4.3.
- Findings: no unresolved blocking findings. No additional live requests or browser reruns were made by this reviewer.
- Mechanical evidence: final Playwright result is one passed, zero skipped, zero unexpected and zero flaky, retry 0, one worker, exit 0. The run lasted approximately 55 seconds.
- Boundary: existing financial journey and owned candidate runtime only. No chart matrix, FRED acquisition, owner-server action or UI/theme production change.
- Placeholder/secret review: no new placeholder or hardcoded credential in the reviewed test delta. Raw captures, credentials and private runtime state remain excluded from this record.
- Complexity: browser tests and this record are exempt from production size caps. The bounded production repairs received separate independent review; the controller's final 110-file gate passed.

## Candidate and source identity

| Component | Accepted identity |
| --- | --- |
| API source | `a965f70c164fe477ce9c99654b9be48e2f1bc9fd` |
| Workspace source | `e1a12c3a031a23598f41166a0f91b8fb24ac2387` |
| API image | `sha256:9b1649810b0d83500f5bb1219adcb6aed8eeb6e674163f1b1d72f6d0f98f63e0` |
| Workspace image | `sha256:ec8be951e06331244dfe1cdfa57ba25a97a7abcbd8063ceb6314212359380cd9` |
| Browser test SHA-256 | `5416266eb510cdbfa4ae197a08b0d5d927fd7c41036c6ae3cbb4386404e6258d` |

The reviewer independently matched all 76 final snapshot files to `corrected-viewport/browser-source-manifest.json`, all nine corrected packaged core/FMP hashes to the installed repair baseline, and all six canonical JSON contracts to the native proposal after the same sorted-JSON roundtrip. Those contracts are OpenAPI, routes, widgets, apps, catalog report and compatibility. The reused Workspace image retains its original build's API-source label; the separate runtime API is the corrected image above, and Workspace source is unchanged.

## Behavior established

The final result and its decoded attachments contain seven Income observations and eight Balance/Cash observations. Cached Income observations are distinct UI checks, not extra provider requests. Balance and Cash each cover annual selection, quarterly selection, explicit refresh and fresh-login quarterly reopen. The passed test verifies widget discovery, symbol/currency/date cells, financial values against the captured native response at displayed precision, and saved AAPL/quarter/FMP parameters. Income also covers MSFT selection and empty-symbol failure/recovery. No duplicate programmatic statement GET is used.

All 15 attached observations retain false point-in-time safety, unknown flow coverage, null start/duration and empty provider conventions. Row attribution and instant-date assertions remain active, including unavailable beginning-cash date. The browser result proves native display and persistence; the accepted task 5 source comparisons and subsequent repair regressions supply separate provider/financial-contract evidence.

Fresh-login diagnostics contain no application, console, network or request failures. Initial-session diagnostics contain only the eight expected missing-symbol/invalid-query HTTP 422 responses and their console entries; the test validates their scope before excluding them. There are no request failures.

## Repairs, request usage and cleanup

The original failure remains retained: Balance's omitted native limit became None and was rejected before acquisition. The two-adapter repair resolves only missing/None to the declared default 5. Independent review passed 66 selected tests; the worker's affected run passed 144. Raw zero, booleans, floats and malformed strings remain invalid. The corrected API was rebuilt and rechecked before the next browser run.

The second failure remains retained: the amount cell repeatedly measured viewport intersection 0.9950000047683716 against an exact 1.0 assertion. The final test accepts 0.99 while preserving numeric parsing, suffix scaling, display-precision tolerance and source comparison unchanged. This accepts near-full cell visibility; it does not prove exact glyph bounds or a particular pixel-rounding cause.

| Attempt | FMP sends | FRED sends | Outcome |
| --- | --- | --- | --- |
| Accepted native task 5 runs, including retained failed comparator attempt | 36 | 0 | Source/native acceptance |
| Original packaged browser | 5 | 0 | Native-limit failure retained |
| Corrected API browser | 7 | 0 | Strict viewport failure retained |
| Final corrected viewport browser | 16 | 0 | Passed |
| Total | 64 | 0 | Below declared cumulative ceiling 71 |

The final stopped ledger has maximum 23 FMP/0 FRED, phase initial, PID 1 and zero destination, exhaustion, ledger, persistence or process denials. Startup proof identifies the sole guarded packaged application at `/app/qopenbb_data/__init__.py`; the final ledger was extracted only after the exact API container stopped. Owned-session cleanup is confirmed. These are attempted transport sends, not a provider billing assertion. Both corrective runs followed diagnosed, reviewed changes; no automatic retry occurred.

Initial API export failures and their diagnostic recovery remain recorded in the build receipts. The UTF-8 catalog decoding repair has separate independent 19-test acceptance. The original native proposal is retained alongside the corrected generation-roundtrip comparison; it was not silently replaced to assert equivalence.

## Evidence and limits

Evidence is under `D:/BuildArtifacts/QOpenBB/statement-period-provenance/task6`: final `corrected-viewport/browser-session/{browser-outcome.json,final-budget.json,initial-process.json,cleanup.json,evidence/browser-results.json}`, final snapshot manifest, corrected candidate receipt/source hashes/catalog, the two earlier session records, and `native-defaults` repair evidence. The executed existing Playwright CLI selects only `local packaged financial widgets support native company period recovery and saved reopen$` through the frozen financial-workspace configuration. The reviewer inspected recorded execution and independently recomputed file hashes and contract equality without repeating provider traffic.

Acceptance covers local candidate images and the affected native workflow. It does not certify publication, registry-image equivalence, owner-server deployment, broader financial compatibility, exact full-glyph visibility, or IA-B analytical readiness. Task 7 must bind published artifacts to these accepted sources and retain those limitations.
