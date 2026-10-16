# Build and load a foundation image

Use the portable commands below to acquire locked owned sources, filter them before upload, export a Dagger image and load that exact archive. The only implemented build selection is `foundation-smoke`: a pinned Python base, a tiny smoke program, source provenance and the permitted source files. It provides delivery infrastructure evidence; it does not start Workspace, the data API, Anthropic or Excel.

Restore the [locked tools](development.md) first. Run in WSL/Linux from the repository root. The Dagger SDK entry point is `.dagger/src/qopenbb/export.py`; its sole builder is `qopenbb.images.build(service, ...)`. `dagger run` starts the pinned engine and SDK session. It does not load a Dagger module or upload the repository as module source. There is no `dagger call` interface or `dagger.json` bootstrap.

```sh
pipeline/.venv/bin/python -m qopenbb_ci.image_cli acquire \
  --lock sources.lock.json --destination artifacts/image-run/acquired
pipeline/.venv/bin/python -m qopenbb_ci.image_cli stage \
  --lock sources.lock.json --policy contracts/sources.json \
  --workspace artifacts/image-run/acquired/workspace \
  --data-api artifacts/image-run/acquired/data_api \
  --destination artifacts/image-run/stage
pipeline/.venv/bin/python -m qopenbb_ci.image_cli export \
  --stage artifacts/image-run/stage --tools pipeline/tools.lock.json \
  --lock sources.lock.json --policy contracts/sources.json \
  --sdk-python .dagger/.venv/bin/python --service foundation-smoke \
  --archive artifacts/image-run/image.tar --report artifacts/image-run/export.json
pipeline/.venv/bin/python -m qopenbb_ci.image_cli load \
  --archive artifacts/image-run/image.tar --report artifacts/image-run/load.json
```

Acquisition and staging require fresh destination directories. On WSL, an owned directory on the Linux filesystem can replace `artifacts/image-run` when Windows-mounted filesystem metadata operations are slow. Keep its absolute path and cleanup ownership in the run record. The loader uses the Docker CLI available on PATH; the Windows PowerShell Docker function is not an executable for this command.

## Review the source boundary

Acquisition fetches the exact commit from each HTTPS owner repository in `sources.lock.json`. Staging independently checks checkout root, origin, actual HEAD and tracked-file cleanliness. It selects only tracked files through the existing [source policy](../contracts/sources.json), requires every essential owned root, rejects symlinks and verifies copied bytes against Git blob identities. Untracked operator files cannot enter staging. The retained source namespace exceptions include Workspace storage/state modules and public data assets, and OpenBB logging modules.

The stage contains only `sources/workspace`, `sources/data_api`, the maintained `smoke.py` fixture and `provenance.json`. Provenance records relative file paths and SHA-256 hashes. Export rejects unknown or duplicate metadata fields, malformed types and digests, missing essential source roots and incomplete tree scans. It requires exactly the declared files and their implied directories, including rejecting unlisted empty directories. It rechecks source identities, filtering policy, hashes and the smoke fixture before any Dagger invocation or the SDK's single `dag.host().directory` input. No broad Docker ignore rule is applied afterward. The SDK imports its maintained Python files locally; `.dagger/.venv`, repository ancestors, real `.env`, runtime data and browser artifacts are never directory inputs.

Export starts Dagger with a fresh empty HOME and Docker configuration and an explicit environment allowlist. Provider, publication and Dagger cloud credentials are not forwarded. The engine runner reference comes from the digest in `tools.lock.json`; the CLI version must match that lock. The builder has no test, generation, push, promotion or deployment commands.

## Interpret the identities

`export.json` records the requested and independently observed engine references, SDK version, base reference, source commits, archive SHA-256, image configuration digest, archive manifest digest, architecture and labels. `load.json` adds the actual loaded ID and any Docker RepoDigests. The archive checksum is a file checksum; it is not a registry digest. A locally loaded image can have no RepoDigests. No registry digest is claimed before publication.

`qopenbb_ci.images.inspect_archive` reads archive metadata and every layer outside Dagger, including decoded compressed layers. Its optional synthetic sentinel argument makes the disposable secret check fail on a match. The portable loader requires the loaded ID to match the independently hashed archive configuration or manifest, compares OS, architecture and labels, then saves the loaded image to verify the exact configuration bytes. It never rebuilds the image. Keep inspection and test evidence beside the run report.

Observed on 2026-10-16 with Docker 29.7.2: `docker image load` returned the archive manifest digest as its image ID, while the configuration digest was different. The loaded image's `Descriptor.digest` matched the archive manifest. Both fields remain in the report; treating the configuration digest as Docker's only possible image ID fails this daemon. The source-only foundation archive was approximately 105 MiB and contained 5,721 staged files. This is a small build operation with no application compilation, rather than a packaged application service.

## Verification scope

Focused synthetic regressions live in [test_image_builds.py](../tests/delivery/test_image_builds.py). Task 1.8 evidence belongs under ignored `artifacts/task-1.8`. A clean runner for this task means a fresh pinned Linux container, explicit sanitized source/tool inputs, fresh caches and dependency environments, and access to the WSL-hosted Docker daemon solely for verification. It shares that daemon with WSL; it is not an independent daemon, GitHub execution or production-host acceptance. Git bootstrap packages are runner provisioning, separately recorded from the image's pinned application inputs.

The WSL and clean userspace runs reused the task-owned Dagger engine and its image cache. Only the runner's HOME, dependency caches and Python environments were fresh. Both exported the same archive/configuration/manifest identities. This proves portable execution with the shared daemon; it does not establish a cold engine build or a clean production host.

The foundation is disproved if a forbidden synthetic file reaches staging or an image layer, the engine differs from its locked digest, or archive identity changes on load. Application builds, publication, pull-only Compose deployment and complete release acceptance remain later tasks.
