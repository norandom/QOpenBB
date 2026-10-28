# Login password policy publication review

VERDICT: APPROVED for publication `alpha-40676586728-1`.

Independent read-only review of retained workflow, release, manifest, pull, image-inspection and Compose evidence confirms root `eb0b18bf83f2597f126b89e8483e38ccac296ab9`, Workspace `22180d8ec206e088a384f2a3c7345358b1832c7c` and data API `cab81b16bb9ef49272a6f3b0bf04cf9f34bde0ba`. No network, build, pull or application operation was repeated by the reviewer.

Mechanical audit passed:

- Both CI jobs succeeded; workflow head, release target and release tag resolve to the expected root.
- All three downloaded public installation assets match GitHub's SHA256 and byte lengths.
- All six retained anonymous pulls succeed: digest, alpha tag and latest for each service. Decoded raw manifest bytes independently hash to the reported manifest digest; config digests, all provenance/source labels, Linux/amd64 inspection and pull-log digests agree with the release manifest.
- Final latest observations still match. Public Compose resolves both services to the exact manifest references.
- All 27 image/Compose commands and 27 metadata commands have exit code 0. Anonymous access used a fresh empty Docker configuration and an environment without inherited authentication configuration.
- Public application review and application JSON are exact byte mirrors of the accepted local evidence. They contain no private state paths, credentials or tokens.

Published references:

| Service | Manifest digest |
| --- | --- |
| Workspace | `sha256:ba994b3f22d05cea141d54084d5aae33723669a7f66b690cd579a95cec6f25f9` |
| Data API | `sha256:1aec3870770ceec8b63074da93ed931c678e0a67e7d495d6705ab1d6932c4354` |

Installation guidance and the login policy milestone accurately separate the accepted local candidate `sha256:9a0854a4720c099f333c4f597b594c5b327dacabdb7229590eade6015c18d358` from these published CI images. Candidate browser/API acceptance and retained-state bootstrap replacement are approved in the application review; browser acceptance was not repeated on CI image bytes. The disabled reset form's warnings remain outside browser acceptance. Owner-server deployment, rollback and backup/restore are not established.

No blocking findings remain for publication closure. Concurrent uv packaging edits are outside this release and this review. Final documentation may mark this publication independently accepted while retaining the stated boundaries.
