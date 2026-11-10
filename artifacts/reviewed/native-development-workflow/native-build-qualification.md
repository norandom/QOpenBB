# Native foundation build qualification

Task 10 is accepted on 2026-11-10. Native Windows staging, pinned Dagger export, archive inspection and Podman loading passed. This qualifies the foundation build path; application images and financial browser journeys remain tasks 11.2 and 11.3.

## Verified identities

- Dagger CLI/SDK: `0.21.8`; engine: `registry.dagger.io/engine:v0.21.8@sha256:c9c1a0a6546380983d42e8d75adde070a2a0935c54b498d8bc9045d9cb2ee336`.
- Owned engine: `qopenbb-dagger-engine-native-qualification-20261110122244`, container `8c14466951bf9ed3b5cbb31fbe971b0ede3e9ff9dd9bcd7ee2fe728898a96c13`. Exact identity, session labels, running/privileged state and dedicated cache mount matched before/after export and loading.
- Workspace: `f832a5593223b1e702970c4de8eceda87a17fa5b`; data API: `2e60c0a7aff039eda5f14a9d494beaec822fb9c4`.
- Archive SHA-256: `81b4bfecbd7893c7f841e5ee217150a60e92104bebbc29a82dddcb2eeb87fb40`.
- Config and loaded image: `sha256:87d67aca398f8d3115666245dfc103a8f14a367ec60f8e2ea02ee46ae8435ca6`.
- Manifest: `sha256:71768c590cd37e604f152038903baf3c1a70f0b676e74d07288e16b3d1c50ef7`; platform: `linux/amd64`. Labels matched; saving and reinspecting the loaded image confirmed configuration bytes.

## Execution and review

From `D:/Source/QOpenBB`, the pinned native pipeline Python ran `-B D:/BuildArtifacts/QOpenBB/native-build-qualification/run_resume_qualification.py`, followed by `run_load_resume.py` in the same directory. Full executable paths, argv, source provenance and exit codes are retained in `resume-receipt.json`. Staging, export, inspection and resumed loading each exited 0. Independent Astra review approved the evidence.

Staging first rejected CRLF-converted source bytes. A separate locked checkout with `core.autocrlf=false` passed unchanged source checks. Engine inspection and loading exposed equivalent Podman digest formats; separately reviewed fixes are commits `5f60325` and `9d46e58`. Initial failure receipts are retained. Loading resumed from the same archive without another export. Final loader revision: `9d46e58e901f026a3a1ea138a1c20d0e027d53c7`.

The global Dagger 0.21.11 engine was not used. No WSL shell, provider request, application-image build, financial browser journey, Linux CI acceptance, publication or deployment is claimed. The owned engine/cache remain available. Raw evidence stays under the external qualification directory. Adapter changes passed their independent reviews and the 97-file combined production gate; execution reports are outside production size caps.
