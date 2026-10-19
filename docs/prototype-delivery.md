# Prototype delivery status

The two-service prototype now has a Compose definition, portable build orchestration, identity-checked publication tooling and a GitHub candidate workflow. It is not yet a published or accepted deployment. Candidate-image smoke and the prototype promotion gate remain open. Dashboard persistence acceptance belongs to analyst-workspace; infrastructure recovery verification is deferred and does not block this prototype.

## Run the source and configuration checks

With the pinned Python/Node toolchains restored and owned sources acquired at `sources.lock.json`, run `bash pipeline/ci.sh check` from WSL/Linux. This invokes the full maintained-file complexity checker and focused image, Compose, build and publication tests. It does not replace the existing browser/CDP or live financial checks.

`python -m qopenbb_ci.build_cli --output NEW_RUN_DIRECTORY --release-version prototype-ID` uses the pipeline virtualenv and existing Dagger stage/export/load commands. Both service builds run serially. The output directory must be new. `summary.json` appears only after both image loads succeed.

The pinned GitHub workflow runs portable checks for pull requests and main. Main pushes build both candidate images through Dagger after checks pass; manual dispatch also builds by default and can opt out. Successful builds retain image archives for three days and upload identity reports. Pull requests run checks only. The workflow has no package-write permission and cannot publish or promote; image-based smoke acceptance and the prototype publication gate still need connecting.

## Publication boundary

`pipeline/.venv/bin/python -m qopenbb_ci.publish_cli --archive IMAGE.tar --load-report LOAD.json --repository REGISTRY/NAMESPACE/IMAGE --tag UNIQUE_VERSION --report NEW_REPORT.json` is a low-level publication primitive. It requires existing Docker authentication, independently inspects/reloads the archive, verifies source labels and checks the pushed remote configuration/platform and immutable digest. It does not authorize release promotion or prove E2E acceptance. Do not invoke it as a substitute for the pending prototype release gate.

Compose consumes `WORKSPACE_IMAGE` and `DATA_API_IMAGE`, exposes HTTP on `0.0.0.0:23003`, and persists Workspace under `./data/workspace`. Its interpolation requires image values but does not validate digest syntax; the pending release gate must enforce immutable references. Provider keys stay in ignored `.env`; AI and Excel inputs are not required. Optional admin settings are documented in `.env.sample`; generated credentials remain private in the state directory.

## Remaining release gates

1. Verify login and supported dashboard use in the candidate image with the existing isolated browser flow, including absence of the obsolete script error.
2. Verify the real Compose pair and supported catalog identity/routing using disposable state. Preserve persistence/recovery tests for their deferred acceptance, without treating them as prototype release gates.
3. Join these results into an explicit prototype acceptance/promotion contract, keeping the existing full AI/Excel release gate intact.
4. Wire eligible publication to CI, publish digest-pinned images and the release manifest, then rehearse pull-only installation. Record the owner's server outcome separately.

On 2026-10-19 automatic approval review rejected starting the isolated Workspace test runtime with only "blocked by policy". The image build completed; that rejection prevented fresh runtime acceptance. The operator's existing preview was not replaced.
