# Alpha delivery

The development alpha uses prebuilt `latest` images. Each successful main-branch publication creates a tagged GitHub prerelease with Compose, the public environment template and a manifest containing exact image digests. Stable releases will use pinned versions.

Published: [alpha-39757904293-1](https://github.com/norandom/QOpenBB/releases/tag/alpha-39757904293-1), built from Workspace `da5979c` and data API `49cc413`. Both public service identities passed anonymous pulls by digest, release tag and `latest`. See the [Box Plot release verification](../artifacts/reviewed/chart-box/verification.md). The [earlier alpha evidence](../artifacts/reviewed/alpha-release/verification.md) remains historical.

| Service | Exact published reference |
| --- | --- |
| workspace | `ghcr.io/norandom/qopenbb-workspace@sha256:fd5ebf74f1d945c7add6afe82e142a2efe381bcca6208b3f53384d1e16b12928` |
| data-api | `ghcr.io/norandom/qopenbb-data-api@sha256:72d4c59a46b65c966f26085f05e53749c62ed5257268159d8039a0d954c9a551` |

The published CI-built pair is distinct from the local image used for the two passing Box Plot browser scenarios. The manifest binds the publication to the reviewed release revisions; it does not claim browser execution against the CI-built bytes.

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

The owner accepted the Box Plot milestone in the ordinary Table/File journey. Two browser scenarios passed on Workspace `da5979cb020af7737f9a76544ae527d8f2a30831` and local packaged image `sha256:4b7c12f04ab7d5e254c5f0980b310569340f034fcd0b826adf6b495a57717025`: retained-FMP five-number summaries in raw USD, synthetic edge cases, controls, themes/navigation, refresh, save/reopen and PNG export. The owner approved the original/replacement appearance and default miniature on 2026-10-22. CI run `39757904293` passed both jobs and published the same Workspace source; both service identities and six anonymous pulls were verified separately. The local browser result does not establish execution against the published CI image bytes. See [Box Plot verification](../artifacts/reviewed/chart-box/verification.md). Assembled Compose and owner-server acceptance remain open. Unfinished renderer families/callers, provider, persistence, AI and Excel work belongs to successor specs in the [roadmap](roadmap.md).

The previous [pie/donut release](https://github.com/norandom/QOpenBB/releases/tag/alpha-39584871538-1) retains its [acceptance evidence](../artifacts/reviewed/chart-pie/verification.md).

The earlier CI failure occurred after Workspace export, in engine identity verification. The repair resolves the pinned image through Docker instead of equating a local image ID with a registry manifest digest. Focused tests cover both Docker storage representations; the hosted run now confirms the repaired build outcome.

Earlier tool rejections prevented automatic local runtime startup. The owner subsequently started the identified combination-chart candidate, allowing its recorded browser acceptance; those results do not imply acceptance of other candidates or deployment environments.
