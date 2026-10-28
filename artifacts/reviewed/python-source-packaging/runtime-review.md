# Python source and Valkey candidate runtime review

VERDICT: APPROVED for PY3/VK3 within the tested candidate and operations. Publication verification remains separate.

Candidate: `sha256:6417e5fb24339894463a5a4bd9d095b127b5ac46694755f4a7c32b96f861833f`; Workspace source: `dfda735c527663dd7ecc2f80af18e25843f575af`; root build: `c25da590bc804f6c469d5fd00fdb2031127608c3`. Independent review read the actual probe/verifier code, retained build/load evidence, migration results, gallery result and password journey. No builds, tests or runtime operations were repeated.

## Evidence and findings

- Dagger acquisition, staging, export and load all exited 0. Loaded identity and source/provenance labels match the reviewed source, including the final Dockerfile hash and pinned Valkey archive.
- The actual image passes backend health, runs Supervisor and uvicorn, reports uv/uvx 0.12.5, has no installed Cython distribution and no application `.so` files under api/routers/utilities. Package origins resolve to `.py`; representative schema/router source files exist. The working health, authentication and chart journeys provide application execution evidence beyond filesystem presence.
- Actual responding-server INFO reports `server_name:valkey`, `valkey_version:9.0.7`, executable `/usr/local/bin/valkey-server`, and a localhost-only listener on port 6379. The compatibility `redis_version:7.2.4` field is not the Valkey release number. The package query finds no installed `redis-server`; the controller's command lookup returns no Redis executable. `ldd` reports no unresolved server libraries.
- A synthetic snapshot was explicitly saved by Redis 7.0.15 in the previous candidate, whose Workspace was then stopped. Valkey loads the same random key and RQ queue/job metadata. Ping, expiry and publish/subscribe checks pass. After a Valkey save and Workspace force-recreation, the key and queue/job metadata still match. This proves the tested Redis 7.0.15 snapshot and operations, not arbitrary Redis formats or modules.
- The same synthetic account and dashboard database content remain present through replacement and recreation, checked directly against the retained SQLite markers. This is a database-marker retention check, not UI dashboard reopening after recreation.
- The existing gallery browser test passes once with one worker, zero retries, exit 0 and a five-minute duration. Its recorded image/source match this candidate. The initial journey renders the gallery, saves native state and reopens the edited combo in a fresh authenticated context. Financial failure collection is empty and both browser/CDP diagnostic records are clean. This is the required existing dashboard journey; it does not claim that this newly created gallery was subsequently reopened after a container recreation.
- The password browser/API journey reports PASS at complete for the same candidate/source: exact weak-password submission reaches authenticated Workspace, wrong login fails, weak new password and wrong current password fail, the correct weak current password authorizes a strong replacement, and the old password fails while the new session accesses the protected endpoint. All six diagnostic fields are clean. Reset-form UI warnings remain untested because that form is disabled in the packaged configuration.

No blocking findings remain. RQ evidence covers enqueue, persisted queue membership and job metadata retrieval; **it does not execute an RQ job**. The gallery retains its existing single-Area hover limitation. This review adds no new appearance acceptance, live-provider coverage, owner deployment, backup/restore, build-speed comparison or published-CI-image browser claim.

## Reviewed evidence identities

SHA256:

- Redis seed result: `178a4ca3fbd19051288269826ddc8bc43015969c5eb619333af3d96e7ebf7ef0`
- Candidate/recreation result: `ce4b57fa239ce220f9ea4301589dcf5d1291bbc999efff56f572d831b67cc7a8`
- Actual server INFO: `37969253c99ae818b5d955ff66e233241dc2a44f7cb5567a8c7f7b8d3c2d6ab7`
- Password result: `7e656fc79da2103b276bb2e84c9f09ad28668d2e6cda3b5c56383687ad1d9563`
- Gallery journey: `8241c22b76b069883b43726e576b229599b7d731aeb0720273b70bed03e52861`

Raw records remain in the ignored runtime/browser artifact directories. Public summaries must omit private bind/fixture paths and authentication data.
