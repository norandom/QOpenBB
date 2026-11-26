# Versioned modeling contract

The internal analytics listener serves the v1 modeling API under `/modeling/v1`. QOpenBB records the provider and Workspace consumer contracts in this repository. The provider bundle describes the saved-output widget and the six installed factor methods at its pinned source revision. [Provider bundle](../contracts/modeling/v1/manifest.json) · [Consumer mapping](../contracts/consumers/financial-modeling/saved-output.v1.json) · [Adopted provider](../contracts/consumers/financial-modeling/provider.lock.json)

## Evaluate a registered factor

Use signed discovery at `GET /modeling/v1/models` to obtain each method's model ID, versions, inputs, assumptions and output definitions. Submit a dated snapshot and its assumptions to `POST /modeling/v1/evaluations`. The owner can reopen the immutable response at `GET /modeling/v1/runs/{run_id}` and select a saved output through `GET /modeling/v1/widget-results` using its run and output IDs.

The six methods cover ETF momentum, annualized realized volatility, the DFII10 real-yield regime, company FCF yield, ordered proxy comparison and regime-conditioned timing diagnostics. For company FCF yield the numerator is trailing operating cash flow less capital expenditure. A negative numerator and positive market value produce a negative percentage. Missing eligible inputs withhold the result. An amended filing supplies a new input snapshot and evaluation, while the original run keeps the figures and filing evidence available at its cutoff.

The timing study evaluates one-session open-to-open returns across the supplied study calendar. The execution worker caps the whole snapshot at 10,000 observation rows across all tables. Each saved output retains its applicable checks and independent verification status. A mismatch keeps the displayed value withheld.

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

Run the source-level integration check from a clean candidate checkout. Supply the revision immediately before the change range. The prototype workflow uses the push's previous tip or the pull request's base revision. A manual or release run without either uses the initial adoption revision.

```bash
bash pipeline/ci.sh modeling-impact "$base" artifacts/modeling-impact/report.json
```

The report identifies changed financial contracts, owning requirements, pytest selectors and the outcome of each selected check. An unresolved change triggers broader checks and keeps the decision blocked until its mapping is repaired. Missing and skipped tests keep the affected capability unverified. An unaffected range is reported separately.

For an affected range, the gate exports the candidate from its checked-out source and exercises the saved-output endpoint. The report retains the candidate and adopted contract identities, the response evidence digest, the source lock digest and the Workspace and data API fork revisions. The adjacent evidence file contains synthetic financial responses. These checks run against source packages. Image and browser acceptance have their own verification steps.

## Connect a Workspace session

Send the Workspace bearer session to the same-origin `/modeling/v1` routes. Workspace validates the session for every request using its normal expiry and renewal policy. It signs the validated user UUID into a short-lived assertion and sends that assertion to the private modeling listener. The listener enforces ownership when it saves or reopens a run. The provider-data proxy continues to serve provider requests independently.

When provisioning the private listener, configure the same dedicated `QFM_IDENTITY_CURRENT_KID` and `QFM_IDENTITY_CURRENT_SECRET` in Workspace and the listener. Generate at least 32 random bytes for the secret and supply their encoded text to both processes. Only the listener needs the optional `QFM_IDENTITY_PREVIOUS_KID` and `QFM_IDENTITY_PREVIOUS_SECRET`. To rotate, first configure the listener to accept the new current and outgoing previous key, then switch the Workspace signer. Retire the previous key after all signers have switched and their outstanding 60-second assertions have expired.

The bridge forwards to `http://modeling:6901/modeling/v1` on the private network. The current two-service Compose file supplies the Workspace signing configuration. Enable the independent listener with the [pull-only Modeling candidate procedure](modeling-deployment.md).

## Evaluate and reopen an issuer FCF yield

In a Workspace dashboard, open **Add widgets** and select **Issuer FCF yield**. Paste the input snapshot object into **Input snapshot JSON**, enter the assumption version and effective date, and select the CapEx sign convention used by the filing. **Evaluate FCF yield** creates an owner-scoped run. The result shows the exact percentage, saved run ID, assumptions, checks, independent verification and calculation trace. Editing an input marks the previous result stale. An ineligible observation produces a withheld result with an explanation.

Add **Saved model output** to the dashboard for a read-only view. Enter the saved run ID and the output ID `fcf_yield`, then save the dashboard. Refreshing or reopening reads that run. The [acceptance inputs](../verification/financial-real-inputs/README.md) include a same-session SAP example and an Apple example with insufficient publication evidence. The [Linux journey](../verification/modeling-journey/README.md) exercises both through the real session bridge.
