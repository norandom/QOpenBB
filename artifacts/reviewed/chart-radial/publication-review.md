# RC5 publication independent review

## Review Verdict

- VERDICT: APPROVED
- TASK: RC5 publication identity and anonymous-access evidence, release `alpha-40125164959-1`.
- MECHANICAL_RESULTS:
  - Tests: PASS. Independent Python evidence assertions through `py -3 -`, exit 0; three public assets downloaded again through default urllib without credentials and compared byte-for-byte with retained files and GitHub asset SHA256 metadata.
  - TBD/TODO grep: CLEAN across retained JSON, Markdown, Python, Compose and environment sample evidence.
  - Secrets grep: CLEAN for concrete GitHub/provider token, bearer-token and private-key patterns; inspected configuration contains parser-only provider values, empty admin inputs and no authentication state.
  - Static checks: SPOT_CHECKED. Inspected verification helpers directly; independently checked all six retained pull/manifest/verbose/inspect sets and all 28 command records, rather than relying on generated boolean summaries.
  - Boundary: WITHIN. This review writes only this file; unrelated tracked edits remain untouched. No Docker pull, build, browser, runtime startup, workflow dispatch or deployment was performed by the reviewer.
  - Boundary audit: CLEAN. Publication is explicitly separated from RC4 local browser acceptance and deferred host acceptance.
  - RED phase: N/A; publication evidence review changes no application behavior.
- FINDINGS:
  1. No blocking findings in the publication evidence boundary. The manifest schema/version and service identities are consistent; all three asset hashes match actual bytes. Manifest SHA256 is `55e291fe320afb8b2e136d070d90a7e1ff995282cfd58ddb740ac9559f1fc03d`, Compose SHA256 is `0dda6c229eac7e6c7a8c55fa717bf338acbc5cd5e1634b8e2702de5393344724`, and sample environment SHA256 is `243112aa5d2e6f0275180d067aab6c8571d03353d2f98ddc8c572e827fdf85cc`.
  2. Fresh read-only GitHub tag/run queries both identify root `fe6826f35b0a76789a4d3841f5b2b8cc852de6a8`; run `40125164959` is completed/success. Retained job metadata shows candidate and publish-alpha successful, with a nondraft prerelease and exactly the three expected assets.
  3. Workspace immutable digest `sha256:f5947359ea5e2e822eefc0effa1876b5ba86b5f973b3c9cf842ab6cd253d89c6` and API immutable digest `sha256:533538235e0030596e6d0ed6ef0358f872ae3088f1a12ba1ba8e32c9f476ca5a` agree across digest, alpha and latest references in the retained evidence. Remote config digests equal the manifest's CI loaded image IDs. Inspected labels match all expected provenance labels and source pins Workspace `9d007b2f40b65ec5f1e2e760787a9fc2d9e4e3d5` / API `cab81b16bb9ef49272a6f3b0bf04cf9f34bde0ba`; inspected platforms are linux/amd64 and RepoDigests include the immutable references. The containerd manifest-as-local-ID distinction is accurately documented.
  4. Anonymous pull evidence uses an explicitly initialized empty Docker configuration for every registry command, records absent DOCKER_AUTH_CONFIG, contains six successful pull logs and matching inspections, and records cleanup. The reviewer independently repeated public asset downloads; registry pulls were assessed from recorded evidence to respect the occupied heavy-check queue.
  5. Parsed public Compose resolves both explicit overrides to the manifest digests, with parser-only provider values. The released template retains latest defaults, relative bind persistence and the expected HTTP port. No parser result is presented as a runtime check.
  6. FYI: This approves the publication verification sub-boundary. Parent-owned RC5 checklist/breadth reconciliation, reviewed-mirror synchronization and selective delivery remain separate completion work. The report correctly states that the RC4 browser image has different bytes from the CI publication; no CI-byte browser acceptance, owner-server deployment, rollback or backup/restore is established here. Latest identity is a timestamped observation, not a permanent guarantee.
- REMEDIATION: None required for publication verification.
- SUMMARY: The released assets, successful workflow/tag identity, anonymous pull evidence and immutable image provenance support accepting RC5 publication verification within its stated limits.
