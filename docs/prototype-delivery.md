# Alpha delivery

The development alpha uses prebuilt `latest` images. Each successful main-branch publication creates a tagged GitHub prerelease with Compose, the public environment template and a manifest containing exact image digests. Stable releases will use pinned versions.

Published: [alpha-39237590906-1](https://github.com/norandom/QOpenBB/releases/tag/alpha-39237590906-1). Both public `latest` images were pulled anonymously and matched the release manifest. [Verification record](../artifacts/reviewed/alpha-release/verification.md).

## Build and publication

`bash pipeline/ci.sh check` runs maintained-scope complexity checks and focused delivery tests. `bash pipeline/ci.sh build --output NEW_DIRECTORY --release-version alpha-ID` builds both services serially through Dagger and records their inspected and loaded identities. Dagger builds images only.

After a successful build, the portable publication command is:

```bash
pipeline/.venv/bin/python -m qopenbb_ci.alpha_cli \
  --build-output artifacts/ci-candidate \
  --registry-namespace ghcr.io/norandom \
  --manifest artifacts/alpha-release/manifest.json
```

It publishes unique alpha tags for both services, verifies their remote identities and shared source revisions, then updates `latest`. It writes a completed manifest only when both aliases match. Updating two registry tags is not atomic: a failed second update can leave mixed aliases. Use the pair of exact references in a completed release manifest to reproduce an alpha.

GitHub Actions runs checks for PRs. Only the main-branch publication job receives package/release write permissions. It downloads the built archives, publishes the images and creates a tagged prerelease. Package visibility determines whether users need registry pull credentials. See [installation](install.md).

## Acceptance boundary

The owner accepted shipping the current development alpha with the existing functionality. That does not mark unfinished renderer, provider, persistence, AI or Excel work complete. Candidate-image browser/Compose verification and live-data checks remain recorded follow-up evidence; broader work belongs to the successor specs in the [roadmap](roadmap.md).

The earlier CI failure occurred after Workspace export, in engine identity verification. The repair resolves the pinned image through Docker instead of equating a local image ID with a registry manifest digest. Focused tests cover both Docker storage representations; the hosted run now confirms the repaired build outcome.

On 2026-10-19 automatic approval review rejected starting the isolated local Workspace test runtime with only "blocked by policy". That run did not establish fresh browser acceptance. The existing preview was not replaced.
