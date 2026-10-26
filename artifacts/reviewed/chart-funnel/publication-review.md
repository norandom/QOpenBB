# Funnel F5 publication review

APPROVED publication identity and anonymous distribution verification for [alpha-40334144666-1](https://github.com/norandom/QOpenBB/releases/tag/alpha-40334144666-1). This is not a deployment or browser-acceptance claim for the newly published CI images.

The retained [workflow run](https://github.com/norandom/QOpenBB/actions/runs/40334144666) is completed/success; both candidate and publish-alpha jobs succeeded. Run head, release target and tag commit all identify root `e0107cd969c57a5ffe75237e74355f548c7aff65`. The release is published, non-draft and marked prerelease. Manifest provenance identifies Workspace `0b2190354d2dc5f4175ffb989cf652ac36237c77` and data-api `cab81b16bb9ef49272a6f3b0bf04cf9f34bde0ba`.

Three installation assets passed unauthenticated HTTP 200 checks. I independently hashed the downloaded files against the release metadata: compose.yaml `0dda6c229eac7e6c7a8c55fa717bf338acbc5cd5e1634b8e2702de5393344724`, default.env.sample `243112aa5d2e6f0275180d067aab6c8571d03353d2f98ddc8c572e827fdf85cc`, and manifest.json `9924a61fa5a5e7f62dc0bb53f2ab7da6e7ba5723bce13f4d90781fd05bfd7f67`.

| Published service | Manifest digest | Config digest |
| --- | --- | --- |
| Workspace | `sha256:6cb3fd626a8910e8194a001ecfb461cea04f242fe90d23dbcde0a3efb0aec801` | `sha256:5e627674ab741db65422ed399f4cfd7682bfd5793c551893d8b170ed2ccec428` |
| data-api | `sha256:ceb6db4eb02c4ac2a1ca0fda4ea8d8cbf9a6e3943db1fa509d77a0a7b60bfe7c` | `sha256:6405ace28562b30f16ef4d02a939d6a2cc7360db7140babe775fd0eeb7cbea4b` |

Both services passed anonymous Docker pulls by immutable digest, alpha tag and latest: six successful pulls. The verifier used a fresh empty Docker configuration and sanitized environment without DOCKER_AUTH_CONFIG or DOCKER_CONTEXT. I independently compared all six retained remote manifest/config descriptors and local inspections against the release manifest: manifest digests, config digests, repository digests and every expected provenance label agree; platform is linux/amd64. Final latest descriptors still resolve to the same release digests. Manifest digest and config digest are distinct identities; the local containerd image ID may use the former, while the publication loaded-image record uses the latter.

The public Compose configuration parses with the exact two pinned image references and parser-only provider placeholders. No service was started. This proves configuration syntax and image wiring, not application health or a private-server deployment.

## Source and gate qualification

F4 browser acceptance remains attached to Workspace production source `6c7632329bbddc89f8986b0183d7b3a8750dd5eb` and candidate image `4ae3695d4c691f3da326ad2310b2e60ed7ee6fc254d4de9b46fe8c8798437814`. I inspected the Git difference from that source to published Workspace `0b21903`: only four browser-test/helper files changed, with no production edits. The release image is nevertheless a different build and was not browser-tested by this publication verifier; source equivalence does not turn it into the earlier image.

The normal Linux clone local gate passed at the exact release root/vendor revisions: portable exit 0, combined complexity acceptance passed, zero errors/violations and 186 pipeline tests passed in 35.34 seconds. The earlier worktree attempt remains FAILED, exit 2, due to `.git` file ownership classification and a 60-second TypeScript parser timeout. Its empty violations array was not a pass. The separate source-input gate passed but explicitly reported runtime_accepted=false. These qualifications are retained in the local gate review.

## Retention and public subset

Raw evidence remains locally retained in `artifacts/chart-funnel/f5/run-40334144666`; gate evidence remains in `artifacts/chart-funnel/f5/gate` and `artifacts/chart-funnel/f5/gate-clone`. No network, build or heavy test was rerun for this independent review.

The approved public subset is the exact public manifest copied as release-manifest.json, the anonymous-pulls summary with local-only anonymous_config and anonymous_config_retained_pending_coordinated_cleanup fields omitted, and this review. Preserve the original unredacted summary locally. The omitted fields describe a local temporary path/cleanup detail and are unnecessary for public verification. Do not publish raw Docker inspections, environment/config files, command logs or runtime directories. No credentials were found in the proposed manifest, summary results or this review.

F5 publication verification is accepted within that scope. The earlier F4 limitations and separately retained failed fixture/onboarding evidence are unchanged; no CI-image browser or deployment completion is asserted.
