# Run the Workspace backend from Python source

Owner approved removing source-hiding compilation and completing the uv/uvx migration on 2026-10-28. Keep CPython as the interpreter, the Full Workspace profile, application behavior and deployment contract. Complete the running login release before publishing this separate packaging change.

## Acceptance boundary

- PY1: the maintained Workspace Dockerfile ships `api`, `routers` and `utilities` as Python source; it neither invokes Cython nor deletes those sources. Remove the explicit Cython build-tool requirement and installation. Native third-party dependencies may still require their own build tooling.
- PY2: migrate backend project metadata to standard Python project/dependency groups and a native `uv.lock`; use protected frozen `uv sync` instead of Poetry installation/export. Preserve resolved application versions and the locked Git dependency revision where possible; explicitly review any unavoidable difference. Include supervisor in locked runtime dependencies. Use pinned `uvx` only for isolated tools when needed, never runtime dependency resolution. Preserve Full frontend configuration, entrypoint, migrations, persistence and service routing. Do not rewrite unrelated legacy upstream Dockerfiles.
- PY3: build through Dagger and inspect the actual image: representative application modules resolve to `.py`, compiled application extensions and Cython are absent, and health/login works. Verify login correction, current/new-password boundaries and one existing dashboard journey on the packaged source image.
- PY4: independently review the source and image evidence, update the maintained inventory and docs, then publish one verified image milestone. Do not claim a build-time improvement without measured comparable builds.

## Work split and limits

The dependency implementer owns backend `pyproject.toml`, `uv.lock` and the old Poetry lock migration. The controller owns the maintained Dockerfile, obsolete build-tool inputs, focused packaging regression checks, source pins, inventory, build/publication and documentation. Freeze the handoff at a non-package project with Python 3.13, runtime supervisor and a frozen uv lock before joining. Independent review checks dependency and runtime seams. Production limits remain 400 physical lines, 300 logical units and 50 per function; generated dependency locks are excluded with their generator recorded. No existing authentication source changes are required.

## Progress

- [x] Remove Cython and Poetry from maintained packaging; native uv lock preserves all historical versions. Source independently accepted with the joined 76-file complexity gate; runtime verification remains open.
- [ ] Verify the source-based image and existing user journeys.
- [ ] Publish and verify the updated Full Workspace image.
