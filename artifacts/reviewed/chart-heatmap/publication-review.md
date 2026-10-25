# Heatmap publication verification

INDEPENDENTLY APPROVED: [alpha-40228938438-1](https://github.com/norandom/QOpenBB/releases/tag/alpha-40228938438-1) is a public prerelease from root `64c1cad70037449273475688b9668b895a129da4`. The single authorized [workflow dispatch](https://github.com/norandom/QOpenBB/actions/runs/40228938438) ran `build_images=true` on main; both candidate and publish-alpha succeeded. Run SHA, prerelease target and commit tag all match the frozen root.

- Three public assets (`manifest.json`, `compose.yaml`, `default.env.sample`) returned HTTP 200 without authentication. Their exact bytes, sizes and SHA-256 values match GitHub asset metadata; [asset proof](public-assets.json) retains each result.
- The [release manifest](release-manifest.json) pins Workspace `68b1e41d414234c4e191d39207ca6f84347a5bf5` and Data API `cab81b16bb9ef49272a6f3b0bf04cf9f34bde0ba`, matching the frozen root's sources.lock.json.
- All [six anonymous pulls](anonymous-pulls.json) passed: digest, alpha tag and latest for both services. Remote manifest/config identities, source labels, local image identities and linux/amd64 platforms agree. Final latest observations still matched at verification time. A fresh empty Docker configuration and environment excluding inherited authentication/context settings were used.
- All 27 Docker verification commands exited 0. Public Compose parsed with exact digest overrides and parser-only provider values. No service was started and the installed Compose environment was unchanged.

| Service | Verified manifest digest |
| --- | --- |
| Workspace | `sha256:c834cc9797588cb87b8987061928ce50c5fa3e389c3a75825e58fe68d2681f4a` |
| Data API | `sha256:996466ff214ee7379c6d528c1dc24b1a12c3c11064c0f8050222c1dd30f02375` |

Publication is distinct from HM4 application acceptance. Final controls/missing evidence uses Workspace `5cae43a52317264067951b111048664292882ec2` and local image `sha256:6dc3dbfef52cbaa16cdc062d672c63a114a2d6dc8a17daf32a148c915390d42d`; populated theme evidence uses the separately recorded candidate2. The release Workspace revision adds the accepted regression tests after final production acceptance. CI image bytes were not browser-tested. Deployment, rollback and backup/restore are not established by this verification.

Raw evidence and verifier scripts remain under `artifacts/chart-heatmap/hm5/`, with this run under `run-40228938438/`. The anonymous Docker configuration remains retained pending coordinated cleanup. Independent review approved publication on 2026-10-25 after checking raw CI/tag/release metadata, downloaded asset hashes and sizes, all six remote/local image identities and complete source-label sets, the empty authentication configuration and sanitized verifier environment, all 27 successful Docker commands, and the digest-pinned Compose parse. No blocking findings remain. This review did not repeat pulls or infer CI-image browser or deployment acceptance.
