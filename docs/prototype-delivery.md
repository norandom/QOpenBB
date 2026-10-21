# Alpha delivery

The development alpha uses prebuilt `latest` images. Each successful main-branch publication creates a tagged GitHub prerelease with Compose, the public environment template and a manifest containing exact image digests. Stable releases will use pinned versions.

Published: [alpha-39584871538-1](https://github.com/norandom/QOpenBB/releases/tag/alpha-39584871538-1), built from Workspace `9e0f2ee` and data API `49cc413`. Both public service identities passed anonymous pulls by digest, release tag and `latest`. See the [pie/donut release verification](../artifacts/reviewed/chart-pie/verification.md). The [earlier alpha evidence](../artifacts/reviewed/alpha-release/verification.md) remains historical.

| Service | Exact published reference |
| --- | --- |
| workspace | `ghcr.io/norandom/qopenbb-workspace@sha256:d4ea3d5d7f92c7b14461e2ea5d0fde774a6ce2a2611165e10557a920d0bff010` |
| data-api | `ghcr.io/norandom/qopenbb-data-api@sha256:317594d49ce67726373011c8e670a43576d1224e9dd1fe58dfb7f5ae28275dbc` |

The published CI-built pair is distinct from the local image used for seven passing browser journeys. The manifest binds the publication to the reviewed release revisions; it does not claim browser execution against the CI-built bytes.

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

The owner accepted the pie/donut milestone in the ordinary Table/File journey. Seven distinct browser journeys passed on production source `9d18838` and local packaged image `sha256:2459fc315b735cb2f66083bb11a10bacaed2b0fdad7f11f46191937661591d81`: captured-FMP quarterly values with independent ring denominators, synthetic edge cases, controls, paging, theme/refresh, save/reopen/export and five prior-family regressions. The owner accepted the disclosed smaller Pie diameter, shifted outer callouts and absent thin slice separators. Release source `9e0f2ee` adds only the reviewed browser tests to that production source. CI-built public image identities and six anonymous pulls were verified separately; the local browser result does not claim execution against the published CI image bytes. Assembled Compose and owner-server acceptance remain open. Unfinished renderer families/callers, provider, persistence, AI and Excel work belongs to successor specs in the [roadmap](roadmap.md).

The earlier CI failure occurred after Workspace export, in engine identity verification. The repair resolves the pinned image through Docker instead of equating a local image ID with a registry manifest digest. Focused tests cover both Docker storage representations; the hosted run now confirms the repaired build outcome.

Earlier tool rejections prevented automatic local runtime startup. The owner subsequently started the identified combination-chart candidate, allowing its recorded browser acceptance; those results do not imply acceptance of other candidates or deployment environments.
