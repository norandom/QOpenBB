# Historical gallery publication review

Independent review accepts [alpha-40652638534-1](https://github.com/norandom/QOpenBB/releases/tag/alpha-40652638534-1), reviewed on 2026-10-28. This closes the gallery image-publication evidence gate; documentation closure remains controller-owned.

[Workflow 40652638534](https://github.com/norandom/QOpenBB/actions/runs/40652638534) records successful `candidate` and `publish-alpha` jobs, including the Dagger image build. The workflow, release target, Git tag and manifest agree on root `6d97dcb8e6e6de2464e468a8e86229e42f7d6d54`. The downloaded source lock, manifest and image labels agree on Workspace `f399e01ee9bb73f55ba36c95318ce7773188f20b` and data API `cab81b16bb9ef49272a6f3b0bf04cf9f34bde0ba`.

The reviewer recomputed downloaded installation-asset sizes and SHA-256 hashes against both the anonymous HTTP records and GitHub release metadata:

| Asset | Bytes | SHA-256 |
| --- | ---: | --- |
| compose.yaml | 1,359 | `0dda6c229eac7e6c7a8c55fa717bf338acbc5cd5e1634b8e2702de5393344724` |
| default.env.sample | 1,079 | `243112aa5d2e6f0275180d067aab6c8571d03353d2f98ddc8c572e827fdf85cc` |
| manifest.json | 6,740 | `5c84ccc6ef29216ffdc5b448033dd084d989da03c0b31e505a49212077cf921e` |

Six retained anonymous pulls cover both services by immutable digest, alpha tag and `latest`. Saved `docker manifest inspect`, `docker manifest inspect --verbose` and `docker image inspect` outputs agree on registry descriptor digests, config digests, local repository digests, manifest labels and `linux/amd64` platforms. Final `latest` observations match this release; mutable aliases are observations at verification time. The saved manifest-inspection JSON is formatted command output, not original registry bytes, so its file hash is not used as an OCI digest check.

- Workspace: `ghcr.io/norandom/qopenbb-workspace@sha256:d8414d603b9a7bd369650fbaacf71e3271367fe3e9bd6b1be02970289aeab713`; config `sha256:c53a6edd7690cc89c9e8263900e645794fa054ea5e416d03f37965e9356a4207`.
- Data API: `ghcr.io/norandom/qopenbb-data-api@sha256:9c46ea9954835acdc6b233cd99c6c0e5bcf918d46b6823bde9b9f4820178b6f0`; config `sha256:a76049e2e5c22b7d2f59652fcb96e4a59413863b4cd9482f92509f38baea4664`.

The verifier used a fresh empty Docker configuration and restricted environment; HTTP downloads used an opener without authorization, cookies or proxies. All 27 image/Compose command records and 32 metadata/runner records have exit code 0, and referenced output files exist. The retained `docker compose config --format json` output contains exactly two digest-pinned services, no build definitions and parser-only provider values. No service startup or deployment was performed by this verifier or reviewer.

Local application acceptance remains the [separate packaged persistence evidence](verification.md): Workspace image `sha256:4e60fe498e3272908700d9ad206160ce7d5e5f17a775570d4927b65572e7be70`, built from fork `d6208dd3d44e46760d39c80da47c0b681b91e151`. Independent inspection of the exact diff to published fork `f399e01ee9bb73f55ba36c95318ce7773188f20b` confirms that only the persistence test changed; production code is unchanged. CI image bytes differ. This review does not establish a browser run against CI images, backup/restore or owner-server deployment.

## Review verdict

- VERDICT: APPROVED
- TASK: HG4 image-publication evidence.
- MECHANICAL_RESULTS: Read-only asset hashes, release/source identities, six image identities, labels, platforms, command ledgers and Compose consistency passed. No network checks, pulls, builds or application tests were repeated. Scope stayed within the new publication record; unrelated edits were preserved. RED phase is not applicable.
- FINDINGS: No blocking findings. The public record contains no credentials or private runtime paths.
- REMEDIATION: None.
- SUMMARY: Retained evidence supports the exact published release identities and anonymous installation access within the stated runtime limits.
