"""Detect false withholding using the installed issuer reference in the worker."""

import asyncio
import os
from dataclasses import replace
from json import dumps
from pathlib import Path

import pytest
from fixtures.factor_examples import EXAMPLES, build_run
from qopenbb_data.modeling.contracts import CheckOutcome
from qopenbb_data.modeling.models.protocol import CandidateOutput, CandidateResult
from qopenbb_data.modeling.service import bootstrap
from test_model_http import call
from test_model_identity import ENV, assertion


def _false_fcf_eligibility(_context):
    return CheckOutcome(
        rule_id="eligible_inputs.fcf_yield",
        rule_version="1",
        severity="blocking",
        status="fail",
        input_ids=("cash_flows", "market_value"),
        output_ids=("fcf_yield",),
        explanation="Mutant withheld the FCF yield",
    )


def _false_fcf_calculation(_inputs, _assumptions, eligible):
    return CandidateResult(
        outputs=tuple(
            CandidateOutput(
                output_id=output_id, value=None, reason="Mutant withheld the FCF yield"
            )
            for output_id in eligible
        ),
    )


@pytest.fixture
def mutant_app(monkeypatch, tmp_path):
    for name, value in ENV.items():
        monkeypatch.setenv(name, value)
    monkeypatch.setenv("QOPENBB_MODEL_RUN_DIR", str(tmp_path / "runs"))
    monkeypatch.setenv(
        "PYTHONPATH", str(Path(__file__).resolve().parent), prepend=os.pathsep
    )
    ((model, binding),) = (
        (model, binding)
        for model, binding in bootstrap._INSTALLED_METHODS
        if model.describe().model_id == "issuer_fcf_yield"
    )
    (rule,) = binding.rules
    mutant = replace(
        binding,
        rules=(replace(rule, evaluate=_false_fcf_eligibility),),
        calculate=_false_fcf_calculation,
    )
    monkeypatch.setattr(bootstrap, "_INSTALLED_METHODS", ((model, mutant),))
    app = bootstrap.create_app()

    async def mounted(scope, receive, send):
        await app({**scope, "path": "/modeling/v1" + scope["path"]}, receive, send)

    return mounted


@pytest.mark.parametrize(
    ("cash", "input_issue", "verification", "expected"),
    [
        ("-60", None, "mismatch", "-10"),
        ("20", None, "mismatch", "0"),
        ("-60", "late-filing", "unavailable", None),
        ("-60", "missing-market-value", "unavailable", None),
        ("-60", "nonpositive-market-value", "unavailable", None),
    ],
    ids=[
        "eligible-negative",
        "eligible-zero",
        "filing-after-cutoff",
        "missing-market-value",
        "nonpositive-market-value",
    ],
)
def test_installed_worker_detects_false_fcf_withholding(
    mutant_app,
    cash,
    input_issue,
    verification,
    expected,
):
    example = build_run(EXAMPLES["issuer_fcf_yield"], missing=False)
    inputs = example.inputs.model_dump(mode="json")
    filings = inputs["tables"][0]["rows"]
    filings[0]["value"] = cash
    if input_issue == "late-filing":
        for row in filings:
            row["published_at"] = inputs["cutoff"]["evaluated_at"]
    elif input_issue == "missing-market-value":
        inputs["tables"][1]["rows"].clear()
    elif input_issue == "nonpositive-market-value":
        inputs["tables"][1]["rows"][0]["value"] = "0"
    payload = dumps(
        {
            "model_id": "issuer_fcf_yield",
            "method_version": "1",
            "inputs": inputs,
            "assumptions": example.assumptions.model_dump(mode="json"),
        }
    ).encode()
    owner = assertion(claims={"sub": "fixture_analyst"})
    status, run = asyncio.run(
        call(mutant_app, "/evaluations", token=owner, body=payload)
    )
    assert status == 200, run
    assert asyncio.run(call(mutant_app, "/runs/" + run["run_id"], token=owner)) == (
        200,
        run,
    )
    (output,) = run["outputs"]
    assert (output["status"], output["value"]) == ("withheld", None)
    (proof,) = run["verification"]
    assert proof["status"] == verification
    if expected is not None:
        assert f"expected {expected} in percent" in proof["explanation"]
    projection_path = "/runs/" + run["run_id"] + "/outputs/fcf_yield"
    status, projection = asyncio.run(call(mutant_app, projection_path, token=owner))
    assert status == 200
    assert projection["verification"] == [proof]
    (row,) = projection["results"]
    assert (row["status"], row["value"], row["display_text"]) == (
        "withheld",
        None,
        None,
    )
