# Events and Documents integration validation

The installed candidate passed financial acceptance on November 27, 2026. Chromium verified actual and estimated EPS and revenue against FMP, retained missing estimates as missing, and opened SEC filings, earnings-call transcripts and company news. The CVNA run displayed four usable inputs. Three guarded journeys used 34 provider sends with zero guard denials. [Financial evidence and live chart](supplemental.md) · [Controlled browser results](controlled.md)

## Catalog compatibility

The repository regression suite found that changing the example listing of a single native widget could prevent the catalog generator from producing any Apps. The story now takes its initial issuer from the transcript example. All three document widgets retain their respective examples and validate their own listings. The 45 financial proposal checks and 16 Events catalog checks passed after the repair. Independent review approved the change in root revision `4e0e8cb`.

Both the original catalog source image and the accepted Data API candidate reproduced the checked-in Apps, widgets, OpenAPI, datasets, routes, compatibility and catalog report byte for byte. The generator fingerprint changed and the provenance checksum was updated. All 78 staged runtime inputs matched the accepted candidate. The complexity checker examined 221 files and found zero violations. [Candidate identities](candidate.json)

## Workspace regression gate

The repository-wide Workspace gate is blocked. The full unit and integration selection, run with one Vitest worker and fail-fast enabled, passed 391 tests before stopping on the internal widget schema snapshot. A broader run exposed the three other failing files below. All four reproduced on the pre-feature Workspace revision `eeb11a2`. Its first snapshot failure matched the candidate error byte for byte. The feature-specific Workspace suite passed 193 tests across 14 files.

| Suite | Pre-feature result to address |
| --- | --- |
| `app.test.ts` | Three schema shape snapshots and the `cellRangeCols` definition assertion fail. Reconcile the expected schemas with the maintained widget contract. |
| `callerRoute.test.tsx` | The mock lacks `AG_CHART_TYPES`, preventing collection. Supply the expected export. |
| `histogramNavigator.test.ts` | The host test expects two listener registrations and observes three. Check listener lifetimes before updating its assertion. |
| `radialNumerical.test.ts` | DOM and canvas setup reference unavailable globals. Initialize the intended test environment before imports. |

## Root regression gate

The broad root suite found a second stale compatibility assertion that enumerated curated widget IDs. The expected set now includes the Events and Documents widget. The assertion still rejects unknown IDs and compares the pre-existing Company Research layout. Sixteen adjacent catalog tests passed, and independent review approved the test correction in root revision `c581d87`.

The failed-first offline run passed 1,458 cases before reaching that assertion. After the correction, the run from the affected file through the remaining test directories reported 5,952 passes, 56 skips and 35 failures. The two pass counts overlap because previously failing cases ran first. Forty-three live-marked tests were deselected. Provider activity for financial acceptance is accounted for in the three dedicated ledgers.

Fourteen of those 35 cases passed unchanged when run with their expected prerequisites. The five modeling ownership and origin-routing cases passed against the local Workspace Python environment and candidate image. Nine provider checks passed with separate installed-package and source-import processes and the frozen provider dependency environment.

Twenty-one root cases remain outside the accepted feature gate. Sixteen require the historical FMP source archive, which the local checkout lacks. One descriptor test expects CRLF checksums for eleven checked-in JSON fixtures whose Linux bytes use LF. Restore the original archive with its recorded digest and reconcile the byte convention to reproduce those checks. Four synthetic company-research tests failed cash-flow acceptance on both the current installation and pre-feature root revision `5846339`. Their annual and quarterly cash-flow fixture receipts require investigation in the Company Research workstream.

**Disposition.** Local Events and Documents financial acceptance passed. The repository-wide gate remains blocked by the Workspace and root checks above. No release image was published or deployed during this verification.
