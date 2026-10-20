# Alpha delivery

The development alpha uses prebuilt `latest` images. Each successful main-branch publication creates a tagged GitHub prerelease with Compose, the public environment template and a manifest containing exact image digests. Stable releases will use pinned versions.

Published: [alpha-39415813584-1](https://github.com/norandom/QOpenBB/releases/tag/alpha-39415813584-1), built from Workspace `6123991` and data API `49cc413`. See the [combination-chart and release verification record](../artifacts/reviewed/chart-combo/verification.md). The [earlier alpha evidence](../artifacts/reviewed/alpha-release/verification.md) remains historical.

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

GitHub Actions runs checks for PRs and ordinary main pushes. After a reviewed feature milestone passes its real-data acceptance, dispatch `gh workflow run prototype.yml --ref main -f build_images=true` once for the set of commits. Manual runs can build images; publication additionally requires main and receives package/release write permissions. It downloads the built archives, publishes the images and creates a tagged prerelease. Package visibility determines whether users need registry pull credentials. See [installation](install.md).

## Acceptance boundary

The owner accepted shipping the current development alpha with the existing functionality. The combination-chart milestone passed browser checks on an identified local packaged image, including captured FMP values, editor controls, save/reopen/export and navigator/theme/refresh retention. CI rebuilt the same source revisions; registry verification is separate from browser acceptance. Assembled Compose and production-server acceptance remain open. Unfinished renderer, provider, persistence, AI and Excel work belongs to successor specs in the [roadmap](roadmap.md).

The earlier CI failure occurred after Workspace export, in engine identity verification. The repair resolves the pinned image through Docker instead of equating a local image ID with a registry manifest digest. Focused tests cover both Docker storage representations; the hosted run now confirms the repaired build outcome.

Earlier tool rejections prevented automatic local runtime startup. The owner subsequently started the identified combination-chart candidate, allowing its recorded browser acceptance; those results do not imply acceptance of other candidates or deployment environments.
