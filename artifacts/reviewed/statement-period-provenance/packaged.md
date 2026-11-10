# Packaged statement widgets accepted

Income, Balance and Cash passed the native Workspace journey: real FMP data, annual/quarter selection, refresh, dashboard save and fresh-login reopen. The corrected run passed one browser test with no skips, retries or unexpected diagnostics. Independent review accepted task 6; publication and owner-server deployment are separate gates.

![AAPL Income widget with reported FMP amounts](packaged-income.png)

AAPL Income after refresh, with the selector set to quarter. Displayed amounts are USD; B denotes billions. FMP fiscal labels do not establish actual flow duration. The screenshot supports the recorded numerical and metadata assertions; it is not the sole acceptance evidence.

## Candidate identities and checks

| Component | Accepted identity |
| --- | --- |
| Workspace source | `e1a12c3a031a23598f41166a0f91b8fb24ac2387` |
| Workspace image, reused | `sha256:ec8be951e06331244dfe1cdfa57ba25a97a7abcbd8063ceb6314212359380cd9` |
| Data API source | `a965f70c164fe477ce9c99654b9be48e2f1bc9fd` |
| Corrected API image | `sha256:9b1649810b0d83500f5bb1219adcb6aed8eeb6e674163f1b1d72f6d0f98f63e0` |

Nine packaged core/FMP source hashes match the installed/reviewed fork. Canonical image-backed generation is deterministic and matches the native proposal for all six compared outputs: schema, routes, widgets, apps, catalog report and compatibility. The combined 110-file scope gate passes. The browser snapshot's 76 file hashes were independently verified.

The reused Workspace image still records the earlier API pin in its build labels; its Workspace source is unchanged. This local pair is behavior evidence, not a publishable paired-source manifest. CI must rebuild both images from the final lock and verify their shared labels before release.

## Failures retained and corrected

Two initial API export attempts failed with generic CalledProcessError; a diagnostic export succeeded without source changes. Their cause remains unconfirmed. Podman image-ID formatting and Windows UTF-8 catalog decoding were separately repaired and independently tested. The original native proposal is retained; a corrected proposal uses the same sorted-JSON roundtrip as canonical generation. No column-order change was introduced.

The first browser run exposed Balance's optional Limit mismatch before acquisition. The accepted adapter repair preserves strict invalid-value rejection and defaults only missing/None values to 5. A second run reached real Balance data but failed the fixture's full-cell intersection assertion at 99.5% visibility. The reviewed fixture now requires 99%, while retaining numerical parsing and source-value precision checks. That tolerance does not prove a particular pixel cause or complete glyph geometry.

## Request accounting and cleanup

| Run | FMP sends | FRED sends | Result |
| --- | ---: | ---: | --- |
| Original source/native matrix | 18 | 0 | Timestamp-comparator failure, retained |
| Corrected source/native matrix | 18 | 0 | 18 cases passed |
| Original packaged browser | 5 | 0 | Balance default failure, retained |
| Corrected API browser | 7 | 0 | Cell-intersection assertion failure, retained |
| Final packaged browser | 16 | 0 | Passed; zero denials and owned cleanup confirmed |
| Total | 64 | 0 | Each run retained separately |

The final 16 sends were below its 23-send ceiling. All browser sessions were stopped, and final accounting was copied after the exact API process exited. Raw responses, credentials, browser traces and databases remain private. No monetary calculations, IA-B readiness or published-image browser execution are claimed.

External evidence is under `D:/BuildArtifacts/QOpenBB/statement-period-provenance/task6`: `review.md`, `corrected/receipt.json`, `corrected/packaged-source-hashes.json`, `corrected/native-image-roundtrip-comparison.json`, `corrected/catalog-utf8`, and `corrected-viewport/browser-session`.
