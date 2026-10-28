# Build and delivery policy

2026-10-28 owner requirement: use Node 24.22.1 or a later supported patched release for active local tooling, CI and build stages (Node2Shell). The exact approved version and checksums belong to `.node-version` and `pipeline/tools.lock.json`; historical evidence retains its original version. Do not run the retired 24.22.0 toolchain for new checks.

2026-10-19 owner amendment: [prototype-first delivery](delivery-workflow.md) is the active scope. AI and Excel have separate specifications and do not block the prototype. Dagger-only builds, portable verification/publication and image-pull deployment remain required.

User direction, 2026-10-16: Dagger builds the images in GitHub; the private Linux server installs via image pull. Adapted from the sibling project's single-pipeline convention.

- Dagger owns image builds only. It does not own testing, consumer generation, publication, release promotion or deployment. This explicit owner clarification supersedes the earlier broader build/check/publish interpretation.
- Portable repository commands own verification, consumer generation, image loading/publication and release manifests. They run locally in WSL and on CI runners without requiring GitHub APIs or event payloads for core logic.
- Use pinned pnpm with Aikido Safe Chain for new or rewritten maintained JavaScript tooling where compatible; use pinned uv/uvx with Safe Chain for maintained Python tooling and provider work. Verify protection in noninteractive WSL/CI commands, not just an interactive shell alias. Preserve frozen upstream locks where migration would change the baseline, and record any compatibility exception. This owner preference was added during task 1.2 on 2026-10-16.
- GitHub Actions is the initial thin runner: checkout, tool setup, permissions/secret plumbing, invocation and artifact retention. Keep the commands reusable by Gitea Actions with wrapper/configuration changes only. Actual Gitea infrastructure or migration is deferred.
- Developers use the same pinned Dagger build definitions locally in WSL. Pin engine/SDK, actions, source revisions, dependencies, and release images. Registry URLs, repository namespace, release ID and source references are explicit inputs; GHCR is the initial default, not a hard-coded dependency.
- Proposed registry: GHCR under the owner's norandom namespace. Confirm package visibility during implementation. Use least-privilege CI publication and read-only server pull credentials when needed.
- PR checks do not publish and do not receive publication/provider secrets. An eligible release is promoted only after required checks pass.
- Publish immutable image digests and a release manifest tying all service images to source revisions and check results. Mutable latest tags are not deployment evidence.
- Build from the owner-controlled forks recorded in sources.lock.json. Runtime deployment has no application build step: pull the manifest's images, then `docker compose up -d --no-build`. Keep deployment credentials and persistent state on the target host.
- The owner runs Compose locally on the deployment host. Agent SSH access is not a prerequisite; verify the image-pull procedure in WSL/Linux and accept owner-run host evidence for production checks, recording unverified results honestly until supplied.
- Include Full Workspace variant and the data API; include the Anthropic agent image before Excel delivery. Jupyter and wheel distribution are out of scope. Keep test/browser tooling in verification containers.
- Record rollback image sets and compatible backup requirements. Test backup/restore before claiming recoverability.
- Do not publish or start placeholder images. The current compose.validation.env is parser-only.

Current state: task 1.8 accepts the pinned Dagger SDK build/export workflow and portable source staging, archive inspection and loading for a foundation smoke image. WSL and fresh Linux userspace checks share the WSL daemon and cached engine. See [image builds](../../docs/image-builds.md). Task 2.5 also accepts the provisional Full Workspace build/export/load and independent runtime smoke. Task 3.6 accepts the identified data image with offline routes, credential readiness, local package origins and secret-exclusion checks. Agent/Excel images, renderer-complete Workspace, GitHub workflows, publication and deployment acceptance remain pending.

Deployment: the private domain configured through PUBLIC_URL, behind owner-managed Cloudflare Access/cloudflared. Publish only plain HTTP on 0.0.0.0:23003, bind mount ./data/workspace, and keep service topology identical on WSL/Linux. No tunnel service, origin certificates, managed data volumes, or notebook service.
