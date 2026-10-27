# Sankey alpha publication review

VERDICT: APPROVED

Reviewed on 2026-10-27. [Release alpha-40489065805-1](https://github.com/norandom/QOpenBB/releases/tag/alpha-40489065805-1) is published from QOpenBB `c551afe56fa967878c73b39fd4bc71a0d180b9d0`, with Workspace `e12713d29a9572599c7482d293f37cc040eba12f` and data API `cab81b16bb9ef49272a6f3b0bf04cf9f34bde0ba`. The release target, tag object, manifest, expected identities and committed source lock agree.

Both jobs in [workflow run 40489065805](https://github.com/norandom/QOpenBB/actions/runs/40489065805) completed successfully: `candidate`, including portable checks and Dagger image builds, and `publish-alpha`. The release is a published prerelease, not a draft.

| Service | Published immutable image |
| --- | --- |
| Workspace | `ghcr.io/norandom/qopenbb-workspace@sha256:72fa23477449fa003702af91fbe456bd71940c41415f929bfa277e23e54b780f` |
| Data API | `ghcr.io/norandom/qopenbb-data-api@sha256:f96ac83099577b3c0baf317448315ba91ef217dd386fd5c537a62c6671e6df3c` |

The three public installation assets passed anonymous HTTP 200 checks. Independently hashing the retained downloaded bytes reproduces each GitHub asset digest and size: `compose.yaml` 1,359 bytes, `default.env.sample` 1,079 bytes and `manifest.json` 6,740 bytes. The download implementation uses an opener without proxies, cookies or authentication headers.

The retained command log contains six anonymous pulls, covering digest, alpha tag and `latest` for each service. All 27 image-verification commands exit 0. Independently comparing all six retained image inspections and remote manifests confirms the published manifest/config identities, repository digests, complete expected labels and `linux/amd64` platform. Both final `latest` observations match these immutable digests. The verification uses a fresh empty Docker configuration and excludes inherited authentication/context settings.

Public Compose parses with both exact digest overrides and parser-only provider values. Its parsed service images match the manifest. The commands perform image and configuration inspection; no application service startup or server deployment is included.

The separately accepted local browser journey used Workspace `e12713d29a9572599c7482d293f37cc040eba12f` in local image `sha256:b18d296f007935dc40c8b329939e15cdd27120e2e573bbca20d7b84ff200d523`. Publication shares that Workspace source revision; the CI-built image bytes have not repeated browser acceptance. This review accepts publication identities and anonymous distribution only. Server deployment, rollback and backup/restore remain unverified.

Evidence inspected: retained `run.json`, `release.json`, `tag-ref.json`, `expected.json`, `manifest.json`, `public-assets.json`, metadata/image command records, six local/remote image inspections, final alias observations, Compose configuration, verifier implementations and the independent local application review. No build, browser test or pull was repeated for this review. No blocking finding or required remediation remains in this publication boundary.
