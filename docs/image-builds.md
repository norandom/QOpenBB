# Build and load identified images

Use the portable commands below to acquire locked owned sources, filter them before upload, export a Dagger image and load that exact archive. `foundation-smoke` retains the infrastructure fixture. The `workspace` selection builds the adapted Full application through the same catalog. Its provisional image still contains commercial renderers; task 2.12 must replace it before publication or dashboard baseline acceptance. Data API, Anthropic and Excel images remain separate tasks.

Restore the [locked tools](development.md) first. Run in WSL/Linux from the repository root. The Dagger SDK entry point is `.dagger/src/qopenbb/export.py`; its sole builder is `qopenbb.images.build(service, ...)`. `dagger run` starts the pinned engine and SDK session. It does not load a Dagger module or upload the repository as module source. There is no `dagger call` interface or `dagger.json` bootstrap.

Task 2.5 passed independent review on 2026-10-16: 68 focused tests, the complexity gate and a fresh run of the identified image. Docker health, Full configuration, generated-account login, invalid-password rejection, private-file permissions, secret-free logs and disposable-state cleanup passed. Evidence is in `artifacts/task-2.5/review-runtime.json` and `independent-review-complexity.json`. This checkpoint does not establish integrated dashboards, Compose deployment or publication readiness.

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

## Build the provisional Full application

For Workspace, add `--service workspace --release-version qopenbb-task25` to the staging command and select `--service workspace` at export. The release version is an explicit public identifier, limited to 128 letters, digits, dots, underscores and hyphens, beginning with a letter or digit. It is never read from a private frontend dotenv file. The stage and export service must agree. Foundation stages reject release metadata; Workspace stages require it.

The builder assembles `lite`, `terminalpro` and `backend-api/backend` from the verified filtered monorepo into the upstream Dockerfile layout. It builds `lite/Dockerfile` with `OPENBB_IMAGE_VARIANT=full` and the public release version. It removes the assembled root Docker ignore file because the source filter already protects the input boundary and explicitly retains application state namespaces. Bun retains its frozen lock and protected Safe Chain installation; backend installation retains the locked Poetry export through protected uv. No package-age bypass is supplied.

The source filter also retains exactly `terminalpro/build/runtimeConfig.ts` and `terminalpro/src/components/DataConnectors/NewComponents/Data/Content.tsx`. These are maintained build/plugin and UI source files, respectively. Adjacent generated files, private files and alternate case spellings remain excluded. The first application build exposed the missing plugin input; its diagnostic is retained as `artifacts/task-2.5/build-frontend-filter-failure.log`.

Full configuration does not restore hosted capabilities. TradingView's separately entitled assets are absent and its renderer is disabled. Hosted Copilot, web search, SEC/Jina helpers and AI enhancements are disabled; the later custom agent is a separate integration. See the [Workspace adaptations and routing](workspace-build.md) and [license constraints](licenses.md). A packaging account check does not certify data-provider responses or complete dashboard behavior.

Dagger 0.21.8 cannot translate Dockerfile HTTP `ADD --checksum` instructions. The maintained adapter replaces only recognized checksum-pinned HTTPS instructions with `COPY` of `dag.http` inputs that enforce the same SHA-256. File modes remain unchanged. Unknown ADD syntax fails closed. Image labels record the original and translated Dockerfile hashes plus public tool URLs and hashes; archive inspection retains these labels in its JSON report.

On 2026-10-16, staging directly from the mounted checkouts spent its time scanning excluded dependency directories. A native clean exact-commit checkout avoids that metadata cost. On this WSL installation `/tmp` is a 4.9 GiB tmpfs: a shallow local Git clone attempted to copy the data repository's pack and exhausted it. Use a dedicated owned directory on ext4 for larger snapshots and exports, or an exact checked-out tree with reviewed Git object alternates. Verify identity and copied Git blobs through staging as usual. Never delete or prune unrelated caches to make room. Task 2.5 preserves the initial SDK session and HTTP checksum failures under ignored `artifacts/task-2.5`; those failures do not constitute application build evidence.

Observed on 2026-10-16: the provisional `qopenbb-task25` build exported and loaded successfully using Workspace revision `38dffc33389aca0e4a87e0e88d42f7067aa220df`. The loaded image ID is `sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f`; configuration digest `sha256:1e5c011225ce1273ff3a367484f9dc2b3948624304c26a7ce77bd348643aab17` survived an independent Docker save and inspection. The 210,546,688-byte archive SHA-256 is `22475c8d505b68d15a1cbd00032185ad88c8e40ac89a1b96c5e3d46e5344bac9`. These are local identities with no registry digest. Export/load reports, dependency input hashes and preserved failure diagnostics are in `artifacts/task-2.5`. Runtime packaging acceptance is recorded separately.

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

The foundation is disproved if a forbidden synthetic file reaches staging or an image layer, the engine differs from its locked digest, or archive identity changes on load. The provisional Workspace checkpoint additionally requires actual image health, Full runtime configuration and fresh account sign-in. Publication, pull-only Compose deployment and complete release acceptance remain later tasks.
