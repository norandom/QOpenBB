# Podman engine identity compatibility

Accepted on 2026-11-10. Native image inspection now accepts equivalent Docker and Podman encodings while retaining exact owned-container and immutable-image checks.

The correction covers an optional leading slash on container names, a tag omitted from a digest-bound repository reference, and an optional `sha256:` prefix on image IDs. Wrong names, IDs, repositories, digests and stopped engines remain rejected.

Verification: eight behavior checks failed before the correction; 55 focused engine checks passed afterward. Independent Astra review repeated ten targeted checks and approved. Read-only verification accepted the retained pinned 0.21.8 engine. The combined production gate passed with the frozen lifecycle changes included; image_cli.py measures 218 physical lines, 167 logical units and maximum function size 28.

No engine creation, image export, load or publication is established by this record. Task 10 owns actual build qualification. Raw evidence remains under D:/BuildArtifacts/QOpenBB/native-build/podman-engine.
