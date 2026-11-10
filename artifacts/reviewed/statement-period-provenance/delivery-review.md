# Statement provenance delivery accepted

APPROVED for task 7 publication evidence on 2026-11-10. No blocking findings remain. The controller may promote the published catalog provenance and hashes, sync sanitized evidence, and close the seven-task slice after updating its delivery and migration documentation. This review does not attest those subsequent edits.

The independently reviewed release is alpha-42878062405-1 from root e09024aa965757d23937ed0472ccce05d9666aea, API a965f70c164fe477ce9c99654b9be48e2f1bc9fd and Workspace e1a12c3a031a23598f41166a0f91b8fb24ac2387. Both jobs in workflow 42878062405 succeeded. The retained Linux candidate log records 461 passed, 12 skipped and 1 deselected; these are portable checks, not a live-provider or image-browser acceptance claim.

## Independent joins

The reviewer inspected the requirements/design/task plan, task 6 packaged and prepublication reviews, strict-client migration note, SDK repair review, verifier implementations and completed raw receipts. Read-only independent checks recomputed all three public asset SHA-256 values, all six raw registry manifest SHA-256 values, their config references against local Podman image IDs, every source/build label and both Compose digest references. The prerelease and lightweight tag target the accepted root; sources.lock and the manifest agree with both accepted fork revisions.

Both linux/amd64 images were pulled by immutable digest, alpha tag and latest using an explicit empty Podman authfile. Registry manifests were also fetched with anonymously granted bearer tokens; their exact byte hashes agree with the publication manifest. The final latest observations still match. Local VM SSH credentials provide transport only and are not registry credentials. Public installation assets passed anonymous HTTP 200, size and digest checks. Compose was parsed with exact digest overrides and parser-only provider values; it was not deployed.

| Service | Published manifest digest | Local config identity |
| --- | --- | --- |
| Workspace | sha256:d6909de5259d08362e74b9ede98a8ab387e7f8db58da02fe28b7a51f8d753315 | sha256:06dd955aed763ffa7bfa95638418b65841474734856e6740b409b31c05679a8b |
| Data API | sha256:6ce9186a0f0a9ddd6022a6703aed65b2899cd3e737e5c468351326c9c9342e6b | sha256:7dfa3fc8f6c3a19932d38fa3609c9aa749d3b78ca2bb85935c4af4f2e91772bd |

The reviewer independently joined all nine packaged core/FMP hashes to the accepted task 6 installed-source baseline. OpenAPI, routes, widgets, apps, catalog report and compatibility are byte-identical to the accepted task 6 canonical output. All eight entries in the new catalog hash manifest recompute correctly, including unchanged datasets and updated published-image provenance. The clean controller at the exact root revision used the five accepted generator modules; dirty renderer work was excluded.

Published data-image runtime evidence records four passed tests, zero failures/errors/skips and exit 0. The cases cover health/routes/credentials/dependencies with both credential configurations, unsupported-auth rejection, and served-schema/upstream-generator repeatability. The JUnit and command receipts identify the actual executed selection. These network-disabled checks and the installed source/catalog binding support published data-package acceptance. The reviewer did not rerun containers, builds, provider calls or browser checks.

## Retained failures and boundaries

Initial workflow 42876893136 failed before image building because SDK Python launch-path resolution lost its virtual environment. Its separately accepted repair and actual Linux regression remain evidence; only corrected run 42878062405 establishes publication. Local verification also retained the missing docker.exe and Windows SystemRoot launch failures. The successful native Podman/Compose correction is separately recorded; the failed outer metadata wrapper is not represented as a successful complete verifier invocation.

Task 6 browser acceptance remains evidence for the local candidate images. It is not browser execution against these CI image bytes. Published source identities and data-package checks close the bounded delivery contract; owner-server deployment, rollback/restore, broader financial compatibility and IA-B analytical readiness remain unverified. Flow duration/restatement uncertainty and false point-in-time safety remain intentional contract limits. Old strict validators must upgrade matching core/FMP packages; package version strings alone are insufficient identifiers.

The controller must publish the migration note with this release identity, preserve earlier release availability and failure records, promote only reviewed generated/evidence paths, and retain the unrelated dirty renderer/inventory work. Generated outputs, evidence and documentation are exempt from production size caps; the bounded SDK production repair has separate accepted 400/300/50 measurements and combined gate evidence.

Evidence root: D:/BuildArtifacts/QOpenBB/statement-period-provenance/task7. Principal receipts: run-42878062405/{run.json,release.json,tag-ref.json,manifest.json,public-assets.json,anonymous-pulls.json,image-commands.json,compose-config.json}, ci-candidate.log, native-pull-corrected.log, published-source-hashes.json, published-catalog, published-catalog-comparison.json, published-runtime-command.json, published-runtime.xml and published-packaged-verification.json. Raw credentials and provider payloads are not part of this report.
