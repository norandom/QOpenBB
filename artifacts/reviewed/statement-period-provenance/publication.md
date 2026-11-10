# Statement-period milestone publication

Accepted source milestone: [alpha-42878062405-1](https://github.com/norandom/QOpenBB/releases/tag/alpha-42878062405-1), built from QOpenBB `e09024aa965757d23937ed0472ccce05d9666aea`. The [independent delivery review](delivery-review.md) accepted this evidence.

The release retains Workspace `e1a12c3a031a23598f41166a0f91b8fb24ac2387` and packages data API `a965f70c164fe477ce9c99654b9be48e2f1bc9fd`. Existing Income, Balance and Cash widgets retain their inputs and row values while the API supplies row-attributable statement-period evidence. Unsupported duration, restatement and historical availability remain unknown.

## Published pair

- workspace: `ghcr.io/norandom/qopenbb-workspace@sha256:d6909de5259d08362e74b9ede98a8ab387e7f8db58da02fe28b7a51f8d753315`.
- data-api: `ghcr.io/norandom/qopenbb-data-api@sha256:6ce9186a0f0a9ddd6022a6703aed65b2899cd3e737e5c468351326c9c9342e6b`.

Both jobs in [workflow 42878062405](https://github.com/norandom/QOpenBB/actions/runs/42878062405) passed. The portable Linux gate reported 461 passed, 12 skipped and one deselected; those skips are not new acceptance claims. The release manifest, Compose file and environment template passed anonymous HTTP size and SHA-256 checks.

Six anonymous native Podman pulls verified both images by immutable digest, release tag and latest. Raw registry manifest hashes, local config IDs, source labels and Linux/AMD64 architecture agree; both final latest observations still match. Public Compose parses with the exact digest pair and parser-only values.

## Packaged acceptance

All nine installed statement source hashes match the accepted source. Regenerated OpenAPI, routes, widgets, apps, catalog report and compatibility report are byte-identical to the accepted local candidate. Four existing network-disabled runtime/catalog checks passed in 45.56 seconds, with no skips. These checks made no provider requests.

The separately accepted [local browser journey](packaged.md) covers all three statements, annual/quarter changes, refresh, save and fresh-login reopening. Its final run used 16 FMP requests; the whole slice used 64 FMP requests and zero FRED requests, including retained failed attempts. Browser behavior was not repeated on the CI image bytes. Owner-server deployment, IA-B analytical readiness, backup/restore and rollback remain unverified.

## Retained delivery repairs

Initial workflow 42876893136 failed before image build because executable resolution followed the SDK virtual-environment Python symlink. The [reviewed launch-path repair](sdk-review.md) passed native tests and an independent Linux regression before the corrected run. No application or provider source changed for that repair.

The first local publication verifier assumed docker.exe; this workstation exposes docker through a PowerShell Podman wrapper. Its native correction also retained Windows SystemRoot for socket initialization. Both failed verifier attempts remain in external evidence; the final native pull and packaged receipts passed. These were verifier-only corrections and required no image rebuild.

Strict financial consumers must upgrade together; see the [migration note](../../../docs/reference/statement-period-provenance.md). The outer schema version alone does not identify the added optional member.
