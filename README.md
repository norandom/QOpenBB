# QOpenBB

Full OpenBB Workspace, self-hosted data API with FMP/FRED, and Anthropic AI. Development on Windows/WSL Docker; same Compose topology on private Linux. Current status: requirements and deployment proposal, not a running implementation.

## Deployment contract

- Public URL: https://qbb.hanse-hedge.fund behind owner-managed Cloudflare Access/cloudflared.
- Origin: plain HTTP, one published port at 0.0.0.0:23003. No origin TLS or tunnel service in this stack.
- State: ./data/workspace bind-mounted to /data; no Docker-managed data volumes.
- Dagger builds/checks/publishes in GitHub. Server installs by image pull, without compiling source.
- First: ready-made FMP/FRED widgets and saved dashboards. Next: working Anthropic agent. Only then: regenerated/adapted Excel integration.
- Jupyter is managed independently by the owner; no notebook service or wheel publication now. Custom PostgreSQL remains deferred.

## Owned sources

- [Workspace fork](https://github.com/norandom/openbb-workspace): frontend, application backend, Full packaging, Excel source.
- [Data-platform fork](https://github.com/norandom/openbb-data-api): data API and provider source.
- [Initial source pins](sources.lock.json): acquisition snapshots, not yet validated releases.

Target the latest validated data API release, regenerate widgets/functions, and adapt FMP as needed. The older FMP/EconDB provider packages cannot simply be installed with v5. All release images must come from recorded revisions of the owned forks.

Real credentials stay in ignored .env; [.env.sample](.env.sample) has empty values. Anthropic model selection and integration remain pending. Never include .env in Dagger uploads, Docker contexts, images, traces, or logs.

## Specification and workflow

- [Requirements](.kiro/specs/openbb-self-service/requirements.md)
- [Research and deployment proposal](.kiro/specs/openbb-self-service/research.md)
- [Compose proposal](.kiro/specs/openbb-self-service/compose.proposed.yaml)
- [Phase status](.kiro/specs/openbb-self-service/spec.json)
- [Lite versus Full](.kiro/specs/openbb-self-service/lite-vs-full.md)
- [Delegation and fan-out](.kiro/steering/delegation.md)
- [Complexity caps for future tasks](.kiro/steering/complexity.md)
- [Background verification](.kiro/steering/testing.md)
- [Dagger delivery](.kiro/steering/ci.md)
- [Feature/spec/test mapping](.kiro/breadth.toml)

Validate proposal syntax only, from this repository root:

```powershell
docker compose --project-directory . --env-file .kiro/specs/openbb-self-service/compose.validation.env -f .kiro/specs/openbb-self-service/compose.proposed.yaml --profile excel config --quiet
```

The fixture file contains fake images/credentials. No builds, proxy routing, provider/AI integrations, Dagger workflow, or runtime acceptance are claimed. Next formal phase after requirements review is design, followed by dependency-mapped tasks.
