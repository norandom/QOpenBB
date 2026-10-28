# Replace embedded Redis with Valkey

Owner approved a recent compatible Valkey release on 2026-10-28. Preserve the two-service deployment, client protocol, local port and persistent data path. Join this packaging change with the separately reviewed uv/source-Python image for one build and publication.

## Bounded contract

- VK1: install the official Valkey 9.0.7 Jammy x86_64 prebuilt archive, checksum `bf0f19982dd464ea111617608a90f1a6eaad2c9c59b2e289cbc1591129f6d2e4`. Keep its license. Declare required runtime libraries; do not compile Valkey or replace the Debian base. The current image supports linux/amd64 only.
- VK2: replace the embedded server command while preserving localhost:6379, the existing `/data/redis` bind content, save settings and application user. Retain redis-py, `REDIS_*` settings and protocol compatibility. Remove the installed Redis server package. No extra Compose service or public port.
- VK3: verify the actual built image reports Valkey, Python application modules remain source, and required dynamic libraries resolve. Run representative client operations, queue access, application login and persistence after recreation. Load a synthetic snapshot made by the current Redis version; never use owner data for verification.
- VK4: independently review the source and bounded evidence, update source inventory and deployment documentation, then verify the published image identities. Claim compatibility only for the tested deployment and operations, not arbitrary Redis modules or newer Redis CE data formats.

Research: the official binary's required symbol versions are GLIBC_2.34, OPENSSL_3.0.0 and LIBSYSTEMD_209, compatible with Bookworm's library baseline. The actual candidate passes dynamic-library and running-server identity checks. [Valkey migration documentation](https://valkey.io/topics/migration/) covers Redis OSS 7.2 and earlier; Redis CE 7.4+ persistence is outside this contract.

The implementer owns the maintained Workspace Dockerfile and Supervisor configuration plus one focused packaging regression. The controller owns build/publication, inventory and documentation. Caps remain 400 physical lines, 300 logical units and 50 per function. No other application behavior changes are authorized.

- [x] Accept the pinned server replacement source and focused check: four packaging checks and the joined 76-file complexity gate pass; independent source review accepted.
- [x] Verify the combined image, application access and retained data: Redis 7.0.15 synthetic snapshot, RQ queue access, expiry, pub/sub and state after recreation pass on Valkey 9.0.7. Gallery and login journeys pass separately. [Independent runtime review](../../../artifacts/reviewed/python-source-packaging/runtime-review.md).
- [x] Publish the updated prebuilt image and reconcile documentation: `alpha-40689838352-1`, exact source labels and anonymous digest/tag/latest pulls verified. [Publication review](../../../artifacts/reviewed/python-source-packaging/publication-review.md).
