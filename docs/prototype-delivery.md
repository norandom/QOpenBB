# Alpha delivery

The development alpha uses prebuilt `latest` images. Each successful main-branch publication creates a tagged GitHub prerelease with Compose, the public environment template and a manifest containing exact image digests. Stable releases will use pinned versions.

Published: [alpha-40652638534-1](https://github.com/norandom/QOpenBB/releases/tag/alpha-40652638534-1), built from QOpenBB `6d97dcb8e6e6de2464e468a8e86229e42f7d6d54`, Workspace `f399e01ee9bb73f55ba36c95318ce7773188f20b` and data API `cab81b16bb9ef49272a6f3b0bf04cf9f34bde0ba`. Both CI jobs, public release-asset checks and six anonymous digest, release-tag and latest pulls pass. Earlier records below remain historical.

| Service | Exact published reference |
| --- | --- |
| workspace | `ghcr.io/norandom/qopenbb-workspace@sha256:d8414d603b9a7bd369650fbaacf71e3271367fe3e9bd6b1be02970289aeab713` |
| data-api | `ghcr.io/norandom/qopenbb-data-api@sha256:9c46ea9954835acdc6b233cd99c6c0e5bcf918d46b6823bde9b9f4820178b6f0` |

The manifest binds this pair to the release sources and packaged historical gallery assets. [Gallery publication evidence](../artifacts/reviewed/chart-gallery/publication-review.md) records the image identities and public pulls. Gallery application acceptance uses local image `sha256:4e60fe498e3272908700d9ad206160ce7d5e5f17a775570d4927b65572e7be70` from Workspace `d6208dd3d44e46760d39c80da47c0b681b91e151`. CI publication uses Workspace `f399e01ee9bb73f55ba36c95318ce7773188f20b` with subsequent test-only changes; the CI image bytes have not repeated the browser journey. Owner-server deployment remains unverified.

## Current prototype repair

The first-login GET now returns HTTP 200 with JSON `null` when no developer questionnaire exists, preserving the ordinary onboarding flow and saved answers. The data image packages and serves the existing `widgets.json` and `apps.json`. Optional external app preview URLs are omitted so Workspace uses its existing fallback. The supported catalog remains FMP company profile/income and FRED series. See the [onboarding source review](../artifacts/reviewed/prototype-onboarding/source-review.md), [catalog source review](../artifacts/reviewed/prototype-onboarding/catalog-source-review.md) and [preview repair review](../artifacts/reviewed/prototype-onboarding/preview-source-review.md).

Fixed GET `/agents.json` returns HTTP 200 with an empty array, truthfully advertising that the data backend has no configured agents. It preserves the Workspace discovery contract without introducing AI functionality; Anthropic remains in its separate spec. See the [agent-discovery review](../artifacts/reviewed/prototype-onboarding/agents-source-review.md).

Earlier assembled runs exposed the missing catalog, external FRED preview and agent-discovery 404 responses. They remain failed evidence. [CI run 40467871625](https://github.com/norandom/QOpenBB/actions/runs/40467871625) published the four repairs together. The final fresh-account browser journey passed in 21.1 seconds on that exact published pair: onboarding returned HTTP 200/null; the starter displayed annual AAPL revenue of 416,161,000,000 USD for period ending 2025-09-27, matching the actual response and refresh; later login bypassed onboarding. First-session and later-session diagnostic arrays were empty. See the [independent application review](../artifacts/reviewed/prototype-onboarding/application-review.md) and [application result](../artifacts/reviewed/prototype-onboarding/application.json).

- [x] Verify the repaired release assets and both public image identities, including all six anonymous pulls.
- [x] Complete the isolated published-image Compose journey: first login, installed annual AAPL income widget, displayed identity/date/currency/revenue, refresh and strict diagnostics.
- [x] Complete the pull-only local installation rehearsal.
- [ ] Verify owner-server deployment and the generic-widget empty-required-symbol guard. Broader providers, analyst persistence and backup/restore remain separate obligations.

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

GitHub Actions runs checks for PRs and ordinary main pushes. After a reviewed feature milestone passes its real-data acceptance, dispatch `gh workflow run prototype.yml --ref main -f build_images=true` once for the set of commits. The main-branch dispatch builds both images, publishes them and creates a tagged prerelease. See [installation](install.md).

Publishing a prerelease manually on GitHub also builds both images through Dagger from that release's tagged QOpenBB commit and its pinned application sources. Use a commit containing the updated workflow. Successful publication attaches `manifest.json`, `compose.yaml` and `.env.sample` to the existing release, preserving its notes. The immutable image version remains `alpha-RUN_ID-ATTEMPT`; the manifest additionally identifies the GitHub release tag and QOpenBB commit. Both verified images receive `latest` aliases. Stable releases and ordinary pushes do not publish images.

Publication jobs share a concurrency group to avoid simultaneous `latest` promotion. GitHub concurrency is not an unlimited release queue; wait for one publication to finish before submitting another. A failed build does not establish available release images. Workflow-created prereleases already follow a successful build and do not recursively trigger another workflow through `GITHUB_TOKEN`.

- [x] Verify prerelease event selection, tagged checkout and existing-release asset upload with focused tests and independent review.
- [ ] Verify the first manually published prerelease through the hosted build/publication path.

CodeQL runs separately from image delivery; see [security scanning](security-scanning.md) for language coverage and scan status.

## Acceptance boundary

Radar Line/Area are accepted in the ordinary Table/File journey on application source `af226971c53922de5925d9b068fbfbd81df02527` and local image `sha256:da46760094b602464e9adefa6caae2b100f34307a486076fa9cec4625125a760`. Both retained-FMP family tests pass, including financial geometry, controls, refresh, fresh reopen, PNG export and observed candidate diagnostics. The owner approved the pictured appearance. CI run 40086673952 rebuilt test-only source `194691e589ad75afb74d227574402dfb43ba6aea`; publication assets and six anonymous pulls pass. This does not establish browser execution of the CI image bytes, assembled Compose acceptance or owner-server deployment. See [Radar verification](../artifacts/reviewed/chart-radar/verification.md#published-radar-alpha).

The following Range and Box Plot records describe earlier releases.

Range Bar/Area are accepted in the ordinary Table/File journey on Workspace `e2b87ed98cd5ef18fb9ca6ddf888802d71fc685e` and local packaged image `sha256:1ff9d136027b0e0ae0f55b89f3faae5892602b2aeb3cee5482f408dc3a3bb0b0`. Both retained-FMP journeys pass, including financial extrema, controls, navigation, refresh, fresh reopen and PNG export. The owner accepted default Area appearance; independent review verified corrected navigator spacing. [Alpha-39920081345-1](https://github.com/norandom/QOpenBB/releases/tag/alpha-39920081345-1) publishes the same source after both CI jobs passed. Release assets, source pins and six anonymous image pulls are verified. These are separate local runtime and CI publication results, not browser execution against the CI image bytes. See [Range verification](../artifacts/reviewed/chart-range/verification.md). Assembled Compose and owner-server acceptance remain open.

The following Box Plot record describes an earlier release.

The owner accepted the Box Plot milestone in the ordinary Table/File journey. Two browser scenarios passed on Workspace `da5979cb020af7737f9a76544ae527d8f2a30831` and local packaged image `sha256:4b7c12f04ab7d5e254c5f0980b310569340f034fcd0b826adf6b495a57717025`: retained-FMP five-number summaries in raw USD, synthetic edge cases, controls, themes/navigation, refresh, save/reopen and PNG export. The owner approved the original/replacement appearance and default miniature on 2026-10-22. CI run `39757904293` passed both jobs and published the same Workspace source; both service identities and six anonymous pulls were verified separately. The local browser result does not establish execution against the published CI image bytes. See [Box Plot verification](../artifacts/reviewed/chart-box/verification.md). Assembled Compose and owner-server acceptance remain open. Unfinished renderer families/callers, provider, persistence, AI and Excel work belongs to successor specs in the [roadmap](roadmap.md).

The previous [pie/donut release](https://github.com/norandom/QOpenBB/releases/tag/alpha-39584871538-1) retains its [acceptance evidence](../artifacts/reviewed/chart-pie/verification.md).

The earlier CI failure occurred after Workspace export, in engine identity verification. The repair resolves the pinned image through Docker instead of equating a local image ID with a registry manifest digest. Focused tests cover both Docker storage representations; the hosted run now confirms the repaired build outcome.

Earlier tool rejections prevented automatic local runtime startup. The owner subsequently started the identified combination-chart candidate, allowing its recorded browser acceptance; those results do not imply acceptance of other candidates or deployment environments.
