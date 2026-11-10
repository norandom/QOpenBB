# Podman DNS image acceptance

The corrected Workspace image passes native Podman discovery. The route that failed in the financial attempt, /data/widgets.json, now returns HTTP 200 with all eleven native financial definitions and the expected Income period/response contract. Financial browser acceptance remains open.

On 2026-11-10, native Dagger 0.21.8 built, exported and loaded Workspace from root 0f4a8c9af13be0829e3be34220e882f29a8ecdfc and owned fork e1a12c3a031a23598f41166a0f91b8fb24ac2387. The existing data API image was reused.

| Component | Image ID |
| --- | --- |
| Workspace | sha256:05e16ad56e7275a71edb3aadd4449063f3df40073713588b1f0dedee55e60053 |
| Data API | sha256:b3e56de1878d02f894d80111ba4ecff14b98292b9045ea6cc88e793f41a5f807 |

Workspace archive SHA-256: ac559d1ae72bcd97e7b63d762d3cd546a38eb3483ee5af75589fba061ca72d01. Engine identity was unchanged before and after the build. This is a local image qualification, not registry publication or server deployment.

## Observed behavior

One sentinel-key Compose session passed the existing packaged smoke and added metadata checks:

- Full configuration and health 200; login 200 and incorrect password 401.
- Verified bind state, owner-only Windows ACLs and container-internal 0600 configuration files.
- Installed startup-script hash matches the reviewed source. Generated nginx resolver 10.89.13.1 matches this session's container nameserver; the address is observed, not hardcoded.
- Published host /data/widgets.json and /data/readyz both return 200. All eleven native definitions, Income annual/quarter options and results response contract match.
- Logs were secret-free; owned containers were removed and state retained.

The qualification only requested configuration, health, authentication and discovery metadata. It did not invoke financial provider endpoints or run a browser journey. Its zero-provider-endpoint field describes that scope; it is not an instrumented outbound packet count.

The earlier financial attempt remains failed, with an instrumented final ledger of zero FMP and zero FRED sends. It was not retried. The owner had approved one batch with no automatic reruns, so another financial attempt needs renewed authorization.

## Evidence and next action

Local retained evidence: D:/BuildArtifacts/QOpenBB/native-dns/receipt.json, workspace.export.json, workspace.load.json, check_runtime.py, qualification.json and runtime-review.md. The qualification command used native Python -B, repository pipeline on PYTHONPATH, repository working directory and --workspace-image with the immutable ID above; exit 0.

[Source review](podman-dns-review.md), [pin review](podman-dns-pin-review.md) and [image/runtime review](podman-dns-runtime-review.md) distinguish source, build and runtime acceptance. [Linux CI](https://github.com/norandom/QOpenBB/actions/runs/42827481611) and [CodeQL](https://github.com/norandom/QOpenBB/actions/runs/42827481547) passed on the corrected source pin, without image publication.

Next: after owner approval, bind the financial runner to this corrected image, retain the previous failed run and execute one bounded financial batch. Task 11.3 and whole-migration closeout task 12 remain open; the native specification has 13 of 15 executable tasks accepted.
