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

The saved-output consumer reads exact display text, the declared unit, verification state, selection freshness and output-specific checks. A withheld result has a null display value. A stale selection retains the original run's verification status. The compatibility policy for changing these meanings belongs to foundation task 9.2.
