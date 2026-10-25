# Independent hierarchy publication review

**APPROVED: H5 publication.** [alpha-40201437272-1](https://github.com/norandom/QOpenBB/releases/tag/alpha-40201437272-1) is a public prerelease from root `3941cf8982919c6a5a468e1c0cebb1ee0b694c31`. Both `candidate` and `publish-alpha` jobs succeeded; the release and commit tag resolve to that exact root.

Independent read-only checks passed against the completed raw records, not only the summary:

- All three public assets—`manifest.json`, `compose.yaml`, `default.env.sample`—returned HTTP 200; downloaded bytes, sizes and SHA-256 values match the recorded GitHub asset metadata.
- The [release manifest](release-manifest.json) pins Workspace `33a81d387b62e962ecced465b78bf2d303530468` and Data API `cab81b16bb9ef49272a6f3b0bf04cf9f34bde0ba`.
- All [six anonymous pulls](anonymous-pulls.json) succeeded: digest, alpha tag and `latest` for each service. Raw pull logs, remote manifest/config digests, local image identities, source labels and `linux/amd64` platform agree. Final `latest` observations still matched at verification time. The Docker config was independently confirmed empty during review; the recorded environment excludes inherited authentication/context settings.
- All 27 Docker verification commands exited 0. Public Compose parsed with the two exact digest overrides and parser-only provider values; no service was started.

| Service | Verified manifest digest |
| --- | --- |
| Workspace | `sha256:284ecc13e40a5443a7e06d2d52fd9c9ba8f9f31eef1de1982777b7cf466d4653` |
| Data API | `sha256:c6feb30cd8ceedd213e134ca0912d97dcff4d19bee62f31ccf0e5a605c776add` |

Publication is distinct from [H4 application acceptance](verification.md). The release Workspace revision adds only the five accepted browser files to runtime source `432c26b93328b14b7a9d79d37bafe6203a738cfa`; production bytes are unchanged. Browser tests were not repeated on CI image bytes. Acceptance remains limited to the documented onboarded-user chart scope; first-login diagnostics remain open. This review establishes neither deployment nor rollback/backup/restore behavior, and does not authorize changing the installed Compose environment.

Raw evidence is retained under `artifacts/chart-hierarchy/h5/run-40201437272/`. No production source, runtime or browser state was changed by the reviewer.

Subsequent controller cleanup is recorded separately: the empty anonymous config and owned keepalive were removed, the dedicated engine was stopped with its isolated cache retained, and four owned disposable chart runtimes were removed. Cleanup records preserve unrelated containers. The pull snapshot's retained-config flag describes verification time, before cleanup.
