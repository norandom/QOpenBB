# Initial modeling contract adoption

Foundation task 9.1 exports the internal v1 modeling API and records the first Workspace consumer contract in QOpenBB. The provider manifest identifies the producer and consumer source commit, consumer ID and version, the exact consumer-file digest, and a SHA-256 digest for each payload. The consumer adoption lock records the source commit and SHA-256 digest of that provider manifest.

The adopted provider and consumer source revision is `31c618559f347f973d07f2dd7b496629fe92e9d5`. The provider manifest SHA-256 is `986a2f33b282b9bdf791f562f376491102dedb3200d4dd4c7ab82e346ddf01aa`. The saved-output consumer manifest SHA-256 is `84ead649b9bd99ed8a8f16eee4d2c7f7c8455f118a094018450bcdd21aab526f`.

The 14 payloads comprise one OpenAPI 3.1 document covering all seven internal routes, ten standalone Draft 2020-12 schemas, the installed model listing and the two Workspace discovery documents. The installed listing is empty at this source revision. A test registration exercises descriptor and rule export through the same registration function as the listener. The consumer mapping declares required widget parameters, result fields, nullability, units, validation status and freshness.

Two independent exports with different time zones and Python hash seeds produced identical file trees. The adoption gate replayed the exporter from its Git commit and regenerated the bundle from the current checkout. A negative test supplies a nonexistent revision with a recomputed digest. Other drift checks change payloads, add unexpected files or alter the consumer pin. Write-side checks verify the source bytes before publishing complete files. The command guide is in `docs/modeling-contract.md`.

A signed Uvicorn loopback check validated current request, stored run, projected output, catalog and wrong-owner error responses against their adopted documents. Tests cover exact decimal output, null withheld values, required discovery fields, signed 64-bit integers, RFC 3339 timestamps and local schema references. The compatibility and impact gates are subsequent foundation tasks 9.2 and 9.3.

Independent review approved the two-way adoption pins and exact-byte replay. Its 82 focused tests passed, including rejection of a nonexistent pinned commit with a recomputed digest and validation of actual HTTP responses. The portable quality gate supplied the locked fork comparison inputs and reported zero inventory errors or complexity violations across 844 files.

The final Ubuntu portable gate passed 1,517 tests, with 12 skipped and one deselected. Scoped Ruff and the staged diff check passed.
