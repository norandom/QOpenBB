# Podman loaded image identity

Accepted on 2026-11-10. Loading now accepts Podman inspection IDs without the `sha256:` prefix when the digest exactly matches the load announcement. The returned identity uses the canonical prefix.

Archive equality, exact platform and labels, and saved configuration byte verification remain mandatory. The observed Podman fixture failed before the correction and passed afterward; four focused cases and 26 loader/publication checks passed. Independent Astra review repeated four cases and approved. The combined production gate passed 97 files; images.py measures 90 physical lines, 71 logical units and maximum function size 29.

Task 10 resumes loading the existing verified archive; this correction does not claim actual load acceptance or publication. Raw evidence remains under D:/BuildArtifacts/QOpenBB/native-build/podman-load.
