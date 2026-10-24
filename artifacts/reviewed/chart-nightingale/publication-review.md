# N5 independent publication review

- VERDICT: APPROVED
- TASK: Nightingale release evidence, 2026-10-24. No blocking findings.
- Release: [alpha-40104927952-1](https://github.com/norandom/QOpenBB/releases/tag/alpha-40104927952-1), [workflow 40104927952](https://github.com/norandom/QOpenBB/actions/runs/40104927952).

## Independent checks

Read report, release/run/tag metadata, both verification scripts, command records and all six raw pull/remote/local inspection sets. Fresh offline assertions exited 0: workflow candidate and publish-alpha jobs succeeded; release is a public prerelease, not draft; tag, workflow head and manifest root agree at `6d0dce31e9fa28165976c2c47e3cd7f329ed8ae6`. Workspace source is `e29db76041944a368c7dac446c2f894afea05e68`; API source is `cab81b16bb9ef49272a6f3b0bf04cf9f34bde0ba`.

The release contains exactly manifest.json, compose.yaml and default.env.sample. Fresh SHA256 values match all three GitHub asset digests and the recorded summary. All 28 recorded verification commands exit 0, including six actual pulls covering digest, alpha tag and latest for both services. Raw pull logs contain the expected digest, not just a successful inspect.

- Workspace manifest: `sha256:73e5da5356a4b02ab00991f1c64ee93262d1ce92274f0054b317718446e7157a`.
- Data API manifest: `sha256:602e1fd61abac162064b45c9a67e7736162400247b492a8fe10964581f7160b0`.

Every remote descriptor, local RepoDigest, expected provenance label and linux/amd64 platform matches. Docker containerd local Id equals the manifest digest here; independently inspected config digests equal each CI loaded_image_id. These are distinct identities and the report correctly distinguishes them.

Anonymous access evidence is adequate: every registry command uses the dedicated explicit --config path, initialized to an empty object; the retained environment check records DOCKER_AUTH_CONFIG absent without exposing values. Cleanup commands succeeded. Compose output contains the exact pinned image references; parser-only provider placeholders do not claim provider execution or service startup. Earlier preparation failures remain disclosed and do not invalidate the successful pulls.

## Publication scope and safety

The report, anonymous-pulls summary, manifest and public asset templates are suitable for the reviewed evidence mirror. Their fields are public provenance or blank/template configuration; no credentials/private account state were found. Preserve source hashes and identify any sanitized derivative in the sync manifest. Raw image inspection/configuration outputs and operational logs need not be mirrored.

Fresh git comparison confirms the Workspace difference from browser-tested source `596a5234f7dec5c672dd97b09e365bfb90aac755` to published source `e29db76041944a368c7dac446c2f894afea05e68` contains only the two Nightingale browser test files. This does not make independently rebuilt CI bytes browser-tested. No owner-server deployment, assembled runtime acceptance of CI bytes, or new provider execution is claimed. Latest verification is point-in-time; immutable digests retain the release identity.

No pulls, browser runs, builds or deployment were repeated by this reviewer. Parent documentation/mirror closure remains separate from this publication-evidence approval.
