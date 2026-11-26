# Versioned modeling contract

The internal analytics listener serves the v1 modeling API under `/modeling/v1`. QOpenBB records the provider and Workspace consumer contracts in this repository. The initial bundle describes the saved-output widget and the installed registry at its source revision. Factor registration is a later task. [Provider bundle](../contracts/modeling/v1/manifest.json) · [Consumer mapping](../contracts/consumers/financial-modeling/saved-output.v1.json) · [Adopted provider](../contracts/consumers/financial-modeling/provider.lock.json)

## Verify the adopted contract

Run from the repository root with the locked pipeline environment. The adoption check regenerates the provider documents from both the pinned Git commit and the current checkout, compares their bytes, verifies the consumer binding and checks the digest of the adopted provider manifest. The pinned commit must be present locally. Validation uses the locked pipeline environment and local schemas.

```bash
PYTHONPATH=services/data-api pipeline/.venv/bin/python -m pytest -q tests/contracts/test_modeling_adoption.py
```

## Generate a candidate

Commit the provider and consumer source changes before generating a candidate. Use the full SHA of the checkout that supplies the modeling implementation, export tooling and consumer manifest. Generate into a fresh directory, then review the documents before adopting a new digest. Keep the provider bundle and consumer adoption pin together when updating the baseline.

```bash
revision=$(git rev-parse HEAD)
candidate=$(mktemp -d)
PYTHONPATH=services/data-api pipeline/.venv/bin/python -m qopenbb_ci.modeling_bundle write \
  --revision "$revision" --output "$candidate/v1" \
  --consumer contracts/consumers/financial-modeling/saved-output.v1.json
PYTHONPATH=services/data-api pipeline/.venv/bin/python -m qopenbb_ci.modeling_bundle check \
  --revision "$revision" --output "$candidate/v1" \
  --consumer contracts/consumers/financial-modeling/saved-output.v1.json
```

The saved-output consumer reads exact display text, the declared unit, verification state, selection freshness and output-specific checks. A withheld result has a null display value. A stale selection retains the original run's verification status.

## Check a candidate against the saved-output dashboard

From the checkout containing the candidate provider, run the seven authenticated HTTP cases and save their responses. The gate needs local Git history for both the adopted contract and the selected provider revision.

```bash
export PYTHONPATH=services/data-api
consumer=contracts/consumers/financial-modeling/saved-output.v1.json
QOPENBB_MODEL_COMPAT_BUNDLE="$candidate/v1" \
QOPENBB_MODEL_COMPAT_CONSUMER="$consumer" \
QOPENBB_MODEL_COMPAT_EVIDENCE="$candidate/evidence.json" \
  pipeline/.venv/bin/python -m pytest -q \
  tests/factors/test_financial_compat_cases.py::test_financial_compat_cli_writes_exercised_evidence
pipeline/.venv/bin/python -m qopenbb_ci.financial_compat \
  --candidate-bundle "$candidate/v1" --candidate-consumer "$consumer" \
  --evidence "$candidate/evidence.json"
```

A compatible result requires both structural compatibility and agreement with the financial expectations pinned for the saved-output dashboard. The synthetic cases exercise the difference between a negative amount, zero and a withheld value. They also cover partial results, stale verification, invalid input and an inaccessible saved run. A blocked result identifies the affected consumer and findings. Retain the adopted interface or review and adopt a versioned migration before promoting the change.

## Verify the impact of a committed change

Run the source-level integration check from a clean candidate checkout. Supply the revision immediately before the change range. The prototype workflow uses the push's previous tip or the pull request's base revision. A manual or release run without either uses the adopted contract revision.

```bash
bash pipeline/ci.sh modeling-impact "$base" artifacts/modeling-impact/report.json
```

The report identifies changed financial contracts, owning requirements, pytest selectors and the outcome of each selected check. An unresolved change triggers broader checks and keeps the decision blocked until its mapping is repaired. Missing and skipped tests keep the affected capability unverified. An unaffected range is reported separately.

For an affected range, the gate exports the candidate from its checked-out source and exercises the saved-output endpoint. The report retains the candidate and adopted contract identities, the response evidence digest, the source lock digest and the Workspace and data API fork revisions. The adjacent evidence file contains synthetic financial responses. These checks run against source packages. Image and browser acceptance have their own verification steps.
