# Theme Settings preview publication review

Independent review accepts publication of [alpha-40506541604-1](https://github.com/norandom/QOpenBB/releases/tag/alpha-40506541604-1) on 2026-10-27. This is the TP4 publication evidence gate; documentation closure remains controller-owned.

[Workflow 40506541604](https://github.com/norandom/QOpenBB/actions/runs/40506541604) records successful `candidate` and `publish-alpha` jobs, including `Build candidate images through Dagger`. The run, release target, Git tag and manifest agree on QOpenBB `2826ea2610b1f8c37b7c9bb5eb109eb41609cd42`. The committed source lock, manifest and image labels agree on Workspace `cdefb7638c0991281551db66415328e420287009` and data API `cab81b16bb9ef49272a6f3b0bf04cf9f34bde0ba`.

The reviewer recomputed the three downloaded asset hashes and byte counts against both the anonymous HTTP records and GitHub release metadata:

| Asset | Bytes | SHA-256 |
| --- | ---: | --- |
| compose.yaml | 1,359 | `0dda6c229eac7e6c7a8c55fa717bf338acbc5cd5e1634b8e2702de5393344724` |
| default.env.sample | 1,079 | `243112aa5d2e6f0275180d067aab6c8571d03353d2f98ddc8c572e827fdf85cc` |
| manifest.json | 6,740 | `a6e13b81e67775cebb9adb65a3402b1381d02b6a104ed435bbfac81fe308e281` |

Six retained anonymous pulls cover each service by immutable digest, alpha tag and `latest`. Raw manifest bytes hash to their recorded digests; remote config identities, local inspection, repository digests, all manifest labels and `linux/amd64` platforms agree. Both final `latest` observations match this release. Mutable aliases are observations at verification time.

- Workspace: `ghcr.io/norandom/qopenbb-workspace@sha256:0cae952463e0eb927ae54ffd1473e9e62e75a27ab04a2c5fdeaca0cf8e8f7335`; config `sha256:4f1dbf84ba532abc5f0d0a67dd9141aab6d9b0fd4d24adcc653f56cce98d7793`.
- Data API: `ghcr.io/norandom/qopenbb-data-api@sha256:48c5d80d6b212a4421a5ffb650f193cc7649acbea56bb1399746b4be6936280c`; config `sha256:5e979a6270642027187da80e363f63ae3764ef1212b8ba72ef3119bc5faaf64c`.

The verifier uses a fresh empty Docker configuration and a restricted environment. HTTP asset downloads use an opener without authorization, cookies or proxies. The reviewer inspected these mechanisms and the raw outputs. All 27 image/Compose command records and 34 metadata/runner records have exit code 0; referenced outputs exist. The retained Compose parse contains exactly the two digest-pinned services, no build definitions and parser-only provider values. No service startup or deployment was performed.

Earlier application acceptance belongs to local image `sha256:9b0db4b2a3021cd8554b60bf3302affd9740d7087e672bf42594197f6dc2cd9b`, built from Workspace `c425134e95ac47961143988b5da315abb2969ae1`. The reviewer inspected the exact diff to `cdefb7638c0991281551db66415328e420287009`: one test screenshot call changes from preview capture to page capture; production code is unchanged. CI image bytes differ. This review establishes neither a new browser run against CI images nor server deployment, rollback or backup/restore.

## Review Verdict

- VERDICT: APPROVED
- TASK: TP4 publication evidence.
- MECHANICAL_RESULTS: Read-only asset, raw manifest, source, label, platform, command-ledger and Compose consistency checks passed. No application tests, pulls, builds or network checks were repeated. Placeholder and credential review of this public record is clean. Boundary: within scope; unrelated changes preserved. RED phase: not applicable to publication review.
- FINDINGS: No blocking findings. Local browser acceptance and CI publication are separate evidence sets.
- REMEDIATION: None.
- SUMMARY: The saved evidence supports the exact published release identities and anonymous access, within the stated runtime limits.
