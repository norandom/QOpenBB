# QOpenBB

Self-hosted OpenBB baseline: develop on Windows/WSL Docker and deploy to a private Linux server.

The current work is a Kiro specification, not a runnable or verified deployment.

- [Requirements](.kiro/specs/openbb-self-service/requirements.md)
- [Upstream findings and proposed baseline](.kiro/specs/openbb-self-service/research.md)
- [Proposed controlling Compose file](.kiro/specs/openbb-self-service/compose.proposed.yaml)
- [Phase and approvals](.kiro/specs/openbb-self-service/spec.json)
- [Lite versus Full comparison](.kiro/specs/openbb-self-service/lite-vs-full.md)
- [Background verification policy](.kiro/steering/testing.md)
- [Dagger build and pull-only delivery policy](.kiro/steering/ci.md)
- [Feature/spec/test breadth map](.kiro/breadth.toml)

Start with upstream Lite packaging, which contains the Workspace frontend and application backend, plus a separate open-source data API for FMP. Verify the released Excel add-in against that baseline and make Jupyter optional. The owner's future custom PostgreSQL data integration is explicitly deferred.

Small, documented Excel compatibility changes are permitted. Dagger will own local and GitHub Actions checks/builds/publication; the private Linux server will install immutable release images through Compose pulls. These are requirements, not an installed pipeline.

First acceptance journey: build, save, reopen, and refresh dashboards using ready-made FMP-backed widgets from the self-hosted open-source OpenBB data API. Both backends are self-hosted; FMP supplies the external data.

Validate the proposal's Compose syntax only:

```powershell
docker compose --env-file .kiro/specs/openbb-self-service/compose.validation.env -f .kiro/specs/openbb-self-service/compose.proposed.yaml --profile excel --profile notebooks config --quiet
```

The validation file contains fake image references and fake credentials. It is not a deployment configuration. Required build recipes, authentication integration, TLS, pinned images, and operating procedures belong to the implementation after the specification phases.

Next Kiro phase after requirements review: `$kiro-spec-design openbb-self-service`.
