# Company selector: alpha publication review

**APPROVED for publication of `alpha-42188370167-1`.** The completed CI run built and published the identified Workspace and data API images, created the tagged prerelease, and supplied install assets whose downloaded bytes match the release API digests. Six anonymous pulls verify the immutable, release-tag and `latest` references for both services.

Independent bounded review on 2026-11-06, applying `kiro-review` and `kiro-verify-completion`. The controller executed the publication verifier; the reviewer inspected its exact source, completed receipt, actual pull logs, workflow/release metadata, install assets and identity probe. Independent lightweight audits checked asset sizes/hashes and all six receipt/log/manifest relationships. The reviewer repeated no pull, build, browser, provider or deployment operation.

## Review Verdict

- VERDICT: APPROVED
- TASK: Company-selector completed-feature alpha publication.
- MECHANICAL_RESULTS:
  - CI: PASS. Workflow `42188370167`, source `1ee3576242ed8357dbd494c8b0f181eb92ac2809`, completed successfully; candidate checks, Dagger builds, publication and prerelease creation succeeded.
  - Publication verification: PASS. `pipeline/.venv/bin/python artifacts/company-selector-implementation/verify-publication.py`, final controller process `22602`, exit 0. Final output: `Published alpha verified: six anonymous pulls and install assets.`
  - Anonymous registry access: PASS. Both service repositories were pulled by immutable digest, `alpha-42188370167-1` and `latest`, with an isolated Docker config containing empty `auths` and no `DOCKER_AUTH_CONFIG`. All six return codes are 0.
  - Image identity: PASS. Every reference matches its release manifest/config digests, Linux/amd64 platform, immutable RepoDigest, expected image labels and locked source revisions. Release-tag and latest aliases match the immutable pair at verification time.
  - Release/assets: PASS. The published prerelease is not a draft; its resolved Git tag equals the root source. All three downloaded assets match the API digest and size. Compose and environment-template bytes equal their files at that root commit.
  - Compose: PASS for `docker compose ... config --format json` only, with explicit parser-only provider markers. Source contains two image-based services, no build step, HTTP `0.0.0.0:23003`, sole Workspace bind `./data/workspace:/data`, and no named volumes.
  - Static/boundary audit: CLEAN. Verifier changes remain in ignored verification artifacts; maintained production and publication sources are unchanged by this review. No new placeholder or embedded credential was found in the reviewed helper/publication set.
  - RED phase: N/A for publication verification. Earlier failed verification attempts and their diagnosed causes remain preserved privately.
- FINDINGS: No blocking finding remains within the publication boundary.
- REMEDIATION: None for publication acceptance. The controller must reconcile and independently audit the concise public documentation/evidence set before its separate documentation commit.
- SUMMARY: Actual completed release, asset and anonymous image checks establish this alpha publication.

## Verification Result

- STATUS: VERIFIED
- CLAIM_TYPE: TEST_OR_BUILD
- CLAIM: The company-selector milestone was built and published as tagged alpha `alpha-42188370167-1`, with matching public anonymous image references and verified install assets.
- EVIDENCE: Successful workflow metadata; resolved release-tag/source metadata; completed six-pull and Compose receipt; actual final pull output; independent API asset hash/size audit and six-reference identity audit.
- GAPS: Publication evidence does not extend local application acceptance to the exact CI image bytes. No CI-image browser run, assembled-service startup, private-server deployment, backup/restore, analyst-workspace umbrella, Anthropic or Excel acceptance is claimed.

## Published identity

| Input | Exact identity |
| --- | --- |
| Release | [alpha-42188370167-1](https://github.com/norandom/QOpenBB/releases/tag/alpha-42188370167-1) |
| Build/publication run | [42188370167](https://github.com/norandom/QOpenBB/actions/runs/42188370167), both jobs successful |
| Root/tag source | `1ee3576242ed8357dbd494c8b0f181eb92ac2809` |
| Workspace source | `https://github.com/norandom/openbb-workspace.git`, `f832a5593223b1e702970c4de8eceda87a17fa5b` |
| Data API source | `https://github.com/norandom/openbb-data-api.git`, `28423762e8cc3faae978e770899834b41e7cde99` |
| Workspace immutable image | `ghcr.io/norandom/qopenbb-workspace@sha256:7795861f0a3b2e5df03d945f185621b31a4965890c88eb506f057207a0a47fab` |
| Workspace CI config/image ID | `sha256:8dcde6c1fc765cf9248e3ab207ab5c4a035ef3eaaa5414bf0bd982abcc22fabd` |
| Data API immutable image | `ghcr.io/norandom/qopenbb-data-api@sha256:c8630e39aded926391204e1b5e4b915584527aedc621ec3c4faed88816d0e4b4` |
| Data API CI config/image ID | `sha256:b5b73d45a4b766a26645c595a89768771df8e8446696d74ff4ddcac281cdad72` |

Anonymous checks also passed for `ghcr.io/norandom/qopenbb-workspace:alpha-42188370167-1`, `ghcr.io/norandom/qopenbb-workspace:latest`, `ghcr.io/norandom/qopenbb-data-api:alpha-42188370167-1` and `ghcr.io/norandom/qopenbb-data-api:latest`. Mutable aliases remain time-specific observations; the manifest retains the immutable references.

| Actual release asset | Bytes | SHA-256 |
| --- | ---: | --- |
| `compose.yaml` | 1359 | `0dda6c229eac7e6c7a8c55fa717bf338acbc5cd5e1634b8e2702de5393344724` |
| `default.env.sample` | 1299 | `8958b109b85f8e818e5b6d595b422881ed2e611f45106bde2ec268afc552348b` |
| `manifest.json` | 7061 | `c4753db4f86bc24350032e6d34ca485607f5f6fe32dc67794bdcb4d8d7b4f2e1` |

GitHub exposes the uploaded `.env.sample` as `default.env.sample`. Its bytes match the committed `.env.sample`; the local `.env.sample` alias used for parser validation is byte-identical. Source locks were read from the exact root commit and checked against the working-tree lock before checking both image source labels.

## Diagnosed verification failures

The first verifier required a local image ID equal to the CI config digest. Actual Docker 29.9.2 with `io.containerd.snapshotter.v1` reported the immutable manifest digest as the local ID and Descriptor digest. The remote manifest/config pair, platform and RepoDigest were correct. The ignored verifier now accepts only the exact expected config or manifest ID, and requires an exact Descriptor digest for the manifest-ID case. All final records report manifest IDs. Remote config, manifest, source and label checks remain strict; the maintained loader already recognizes both ID forms. This was a verification compatibility correction, not an image or production change.

The following attempt completed all six image checks but rejected Compose interpolation because the public template intentionally leaves required FMP/FRED keys blank. Final parser validation supplies explicit `qopenbb-parser-only` markers and removes ambient install-variable overrides. It changes no downloaded asset, starts no service and makes no provider request. Both earlier failures remain distinct from the final exit-0 result.

## Scope and retained evidence

Local application acceptance remains the separately reviewed company-selector result at the same Workspace/API source revisions. The CI images have different config IDs from that locally tested pair; this review verifies their publication and provenance, without claiming a browser rerun against their exact bytes. Production complexity caps remain 400 physical lines, 300 logical units and 50/function; this publication review introduces no maintained production change. The four foreign root inventory/catalog changes remain outside this delivery.

The completed private receipt is `publication-verification.json`, SHA-256 `b908f957bc107a9d099bbe48b3534c845be5197af9aa9b29ea8df4ab33d63ab0`. Supporting private inputs are `publication-workflow.json`, `release.json`, `publication-id-probe.json`, final anonymous pull logs and the two independent lightweight audit receipts. Public evidence should retain this concise review, the exact release manifest and selected sanitized verification result; raw logs and helper iterations remain ignored.
