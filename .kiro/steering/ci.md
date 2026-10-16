# Build and delivery policy

User direction, 2026-10-16: Dagger builds the images in GitHub; the private Linux server installs via image pull. Adapted from the sibling project's single-pipeline convention.

- Dagger owns checks, builds, and publication. GitHub Actions checks out the repository, sets permissions/credentials, invokes Dagger, and retains reports; it must not duplicate the check/build logic in shell/YAML.
- Developers use the same pinned Dagger definitions locally in WSL. Pin engine/SDK, actions, source revisions, dependencies, and release images.
- Proposed registry: GHCR under the owner's norandom namespace. Confirm package visibility during implementation. Use least-privilege CI publication and read-only server pull credentials when needed.
- PR checks do not publish and do not receive publication/provider secrets. An eligible release is promoted only after required checks pass.
- Publish immutable image digests and a release manifest tying all service images to source revisions and check results. Mutable latest tags are not deployment evidence.
- Build from the owner-controlled forks recorded in sources.lock.json. Runtime deployment has no application build step: pull the manifest's images, then `docker compose up -d --no-build`. Keep deployment credentials and persistent state on the target host.
- Include Full Workspace variant and the data API; include the Anthropic agent image before Excel delivery. Jupyter and wheel distribution are out of scope. Keep test/browser tooling in verification containers.
- Record rollback image sets and compatible backup requirements. Test backup/restore before claiming recoverability.
- Do not publish or start placeholder images. The current compose.validation.env is parser-only.

Current state: requirement/policy only. No GitHub workflow or Dagger module exists yet.

Deployment: qbb.hanse-hedge.fund behind owner-managed Cloudflare Access/cloudflared. Publish only plain HTTP on 0.0.0.0:23003, bind mount ./data/workspace, and keep service topology identical on WSL/Linux. No tunnel service, origin certificates, managed data volumes, or notebook service.
