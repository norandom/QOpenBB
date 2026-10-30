# Financial-input alpha published

Task 6.3 is accepted on 2026-10-30. [alpha-41030227140-1](https://github.com/norandom/QOpenBB/releases/tag/alpha-41030227140-1) publishes Full Workspace and the OpenBB data API from QOpenBB `6cca7e4`, with the accepted application/provider pins. Both CI jobs succeeded. The three release assets passed anonymous HTTP, hash and byte checks; both images passed anonymous pulls by digest, alpha tag and `latest`. The final `latest` pair matches the release manifest.

| Service | Exact published reference |
| --- | --- |
| Workspace | `ghcr.io/norandom/qopenbb-workspace@sha256:b40a2472b3a5f6ca325aa126b7a2131aa517dc1a622f4f1a3a7cae24f105f269` |
| Data API | `ghcr.io/norandom/qopenbb-data-api@sha256:743b9fd657e8e2e8346a42fb8b3f8146b49ebf134987ffcd6363c879ffc5e6d1` |

The published data image serves eleven native widget definitions and eleven installed financial descriptors, with source and response-contract bindings checked. Fifteen committed runtime inputs match CI provenance, and thirteen resident runtime files match the installed image. The existing historical gallery remains available. An isolated data API container ran without external networking, host ports, mounts or provider keys; it served health, catalog, discovery and OpenAPI responses, reported missing keys as unready, and was removed after ownership checks. Compose was parsed separately with immutable image overrides; no Compose deployment was started.

[Live FMP/FRED inputs](../market-live-financial-inputs/accepted.md) and the [packaged Income journey](../market-packaged-financial/accepted.md) retain their distinct acceptance scopes. The local UI checks cover company/period changes, financial values actually in the clipped viewport, missing-input recovery, refresh and save/reopen. They are not browser execution against the CI image bytes. Workspace provenance changes only by release version. The sole local data-input byte difference is CRLF versus LF after the module docstring in `qopenbb_data/__init__.py`; the other fourteen inputs match exactly. Original and normalized hashes are recorded, without claiming identical local and CI image identities.

See [independent review](review.md), [source and publication identities](final-source.json), the [pipeline](https://github.com/norandom/QOpenBB/actions/runs/41030227140) and the [installation guide](../../../docs/install.md). Main-branch portable checks passed 210 cases and CodeQL passed Python and JavaScript/TypeScript. The current 79-file local complexity join has no errors or violations; this milestone changes evidence and documentation only. No second image build is needed for this bookkeeping commit.

The initial financial-input batch is 26/26 accepted. The broader market-data specification stays open: DCF/estimates/segments, narrative content, remaining FMP families, Yahoo supplementation and extended FRED need their bounded follow-on plans. Financial modeling, AI, Excel and custom data remain separate workstreams. Installer entitlements, CI Workspace browser execution, owner-server deployment and recovery are not established by this publication.
