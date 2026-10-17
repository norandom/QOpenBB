# Publication link adjustment preserves the scoped approval

APPROVED: the controller changed the canonical specification's three evidence links from ignored local artifact paths to the reviewed publication mirror. Content claims and runtime evidence are unchanged. The historical review and input manifests remain preserved.

The current 28-file input allowlist SHA-256 is `773cedee90a5317fa5f261453c0f9a642f852c7ee6b059d0ded0803ea8726694`; the canonical specification SHA-256 is `7a0c446c33d44599387eab66fe3be497fa3d3f16fa213fabb91dc3790d768a2b`. [Publication check](publication-link-check.json) confirms every actual file hash/size and identifies the specification as the only changed entry. [Current input allowlist](publication-input-allowlist.json) binds those bytes.

Command: `wsl -d Debian -u mc -- /mnt/d/Source/QOpenBB/pipeline/.venv/bin/python /mnt/d/Source/QOpenBB/artifacts/parity/appearance-contract-review/publication-link-check.py`, exit 0. Manual comparison confirms the link-only change. This addendum changes no research scope or acceptance state.
