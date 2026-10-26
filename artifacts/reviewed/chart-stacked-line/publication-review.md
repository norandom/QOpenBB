# Stacked Line publication review

2026-10-26. **APPROVED SL4 publication verification** for [alpha-40371082771-1](https://github.com/norandom/QOpenBB/releases/tag/alpha-40371082771-1). Reviewed retained metadata, downloaded assets, verifier source and completed anonymous-pull results without running builds, tests or services.

The release tag and successful workflow run identify root `fee0f4df87e0bf6ea89128978f39656febc5ca0f`. Both candidate and publication jobs succeeded; the focused portable check passed in 11 seconds, superseding the incomplete local attempt. Source labels consistently identify Workspace `404fd8022250db3903d7e9c1fa290662720a06cf` and data API `cab81b16bb9ef49272a6f3b0bf04cf9f34bde0ba`.

All three installation assets returned anonymous HTTP 200. Independently recalculated hashes of `compose.yaml`, `default.env.sample` and `manifest.json` match the retained verification results. The manifest and public sample contain image/source identities and empty credential placeholders, not credentials.

All six anonymous pulls succeeded: digest, release tag and latest for both services. Inspected results preserve matching manifest/config identities, source labels, repository digests and linux/amd64 platforms. All 27 recorded image/Compose verification commands exited zero; final latest observations still matched. Public Compose parsed with exact digest overrides and parser-only provider values; no service was started.

- Workspace manifest: `sha256:96970f0d963b3195407cfd7209d718154659e4d7c5c6847d69928ef9b7571b10`.
- Data API manifest: `sha256:397019cd0d52b529b2027a121c45567cdaca1c580351b5faac79604626c33f07`.

Application acceptance remains the separately reviewed local Workspace `64b7fecea1619547b439cb4a7fbcbfcf431ed904`, image `sha256:948e6cdfcd7cf5340a632bef8a984e2d71c867f12869efcc085dc3d9108053e2`. The intervening Workspace commit changes browser tests only. Publication checks establish CI-image identity and anonymous availability, not a repeated browser run on those distinct CI bytes. No private-server deployment is claimed; the inherited compiler and onboarding qualifications remain unchanged.

For the selected public mirror, `release-manifest.json` and this review are suitable as inspected. Remove the local `anonymous_config` path from the copied `anonymous-pulls.json`; retain authentication method, all six result records, identities and scope. Raw environment/command files with local filesystem paths are outside the selected mirror. This sanitization does not alter the verification outcome.
