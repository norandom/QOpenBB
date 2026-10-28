# Python source and Valkey publication review

VERDICT: APPROVED for [alpha-40689838352-1](https://github.com/norandom/QOpenBB/releases/tag/alpha-40689838352-1).

Independent read-only audit of the verification scripts and retained workflow, release, source lock, assets, manifests, image inspections, pull logs and Compose output confirms root `4aa3969ea4ceedf492ac6ffe7546518db5bc0a12`, Workspace `dfda735c527663dd7ecc2f80af18e25843f575af` and data API `cab81b16bb9ef49272a6f3b0bf04cf9f34bde0ba`. No network request, image build, pull or application operation was repeated.

## Accepted evidence

- Both workflow jobs succeeded. The workflow path/event, head revision, release target and commit tag match the expected publication.
- All three installation assets match the release metadata's SHA256 and byte lengths. Retained anonymous HTTP responses are successful.
- All six anonymous pulls succeed: digest, alpha tag and latest for both services. Independent hashing of decoded raw manifests matches each published digest; config digests, complete source/provenance labels, repository digests, pull logs and Linux/amd64 inspections agree.
- Final latest observations match the same manifest pair. Compose parsing resolves exactly two services to those digests with parser-only provider values; no service startup is claimed.
- All 27 image/Compose commands and 18 metadata commands exited 0. Pulls used a fresh empty Docker configuration without inherited authentication configuration.

| Service | Exact published reference |
| --- | --- |
| Workspace | `ghcr.io/norandom/qopenbb-workspace@sha256:957f02d18b8365412e68016b1b9e7184a4383cec1fc35774fdc0193ab35d219f` |
| Data API | `ghcr.io/norandom/qopenbb-data-api@sha256:59b94139b34e2195e83d69be959c3f242fdf4ddccf5b2764c0d5154612aab057` |

Workspace config digest: `sha256:956faa728c88ba22b6811a02a57540db91522aa569b7b1b9444491ace854a7b2`. Data API config digest: `sha256:9d5fb2611b7a115023b702a5b2d1619e829315dc758fb6865174ac763b029ed5`.

## Acceptance boundary

The accepted local runtime/browser candidate is `sha256:6417e5fb24339894463a5a4bd9d095b127b5ac46694755f4a7c32b96f861833f` from the same Workspace source. Its Python-source, Valkey, synthetic Redis snapshot, database-retention, gallery and password evidence remains the application acceptance basis. This publication audit establishes CI image identity and anonymous availability; it does not repeat those journeys on the published CI image bytes.

RQ job execution, arbitrary Redis-format compatibility, enabled reset-form warning rendering, owner-server deployment, rollback and backup/restore are not established. No blocking findings remain for publication closure within these bounds.
