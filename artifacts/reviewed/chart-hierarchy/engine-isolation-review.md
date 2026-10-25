# Independent engine-isolation repair review

**APPROVED: source repair only.** No remaining concrete defects found in the two-file change against the approved isolation plan. Dedicated-engine creation, the packaged rebuild and H4 synthetic acceptance remain separate work.

`pipeline/qopenbb_ci/image_cli.py` adds an export-only engine option. Explicit mode checks the exact name, QOpenBB ownership labels, immutable configured reference, locked repository digest, actual image identity and running state before connection and after export; the container ID must remain unchanged. Both inspections receive the runner's exact sanitized environment inside the same temporary HOME/DOCKER_CONFIG lifetime. Caller Docker context/config and credentials are excluded, allowlisted DOCKER_HOST is consistent, and inspection failures publish value-free codes with stderr captured. Default export behavior and pinned SDK/CLI checks remain intact. The exporter performs no container lifecycle operations.

Independent verification: `tests/delivery/test_image_builds.py` passed **90 tests** in 7.17 seconds, exit 0. Frozen source hashes matched before and after the run. Evidence: `artifacts/chart-hierarchy/h4/reviewerlogs/engine-isolation-result.json` and `engine-isolation-pytest.log` in that directory. Tests cover poisoned environments, temporary configuration lifetime, classic/containerd identity, preflight rejection, post-export replacement/ownership changes, default compatibility and private-stderr nondisclosure.

Reviewed retained implementer evidence: the final tests fail against baseline in 25 explicit-mode cases; 23 existing build/prototype tests pass. The combined inventory checks 567 files with no errors or violations. The whole exporter measures **181 physical lines / 136 logical units / maximum 28 per function**, within 400/300/50. Evidence is retained in `artifacts/chart-hierarchy/h4/engine-isolation/{red.log,regression.log,combined.json,whole-file.json}`.

Reviewed frozen SHA-256 values:

- `pipeline/qopenbb_ci/image_cli.py`: `77f6a3de6ab2a0bcf2a1a8082dd6b8eac00a17b1e25a8304aea60463c99b127f`
- `tests/delivery/test_image_builds.py`: `c9884995f6a2f0add3fbdf10d92a1912d28672ec849a84de948baed65c55bf19`

No production files were edited by the reviewer. The verification queue is released.
