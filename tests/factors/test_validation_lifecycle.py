from decimal import Decimal

import pytest
from qopenbb_data.modeling.contracts.checks import (
    CheckOutcome,
    PolicyException,
    Tolerance,
)
from qopenbb_data.modeling.contracts.results import ModelRun
from qopenbb_data.modeling.models.protocol import CandidateOutput, CandidateResult
from qopenbb_data.modeling.validation.outputs import blocked_outputs, resolve_outputs
from qopenbb_data.modeling.validation.rules import Rule, RuleContext, evaluate_stage
from qopenbb_data.modeling.validation.tolerance import within_tolerance
from test_model_run_evidence import run_fields as run_fields_fixture

run_fields = run_fields_fixture


def test_exact_scaled_tolerance():
    tolerance = Tolerance(unit="usd", scale=3, absolute="0.001", relative="0.01")
    assert within_tolerance(Decimal(101), Decimal(100), tolerance, unit="usd")
    assert not within_tolerance(Decimal("101.00001"), Decimal(100), tolerance, unit="usd")
    with pytest.raises(ValueError, match="unit"):
        within_tolerance(Decimal(1), Decimal(1), tolerance, unit="eur")


@pytest.mark.parametrize(("mode", "status"), [
    ("missing", "unknown"), ("raises", "error"), ("excluded", "not_applicable"),
    ("bad_scope", "error"), ("ready", "pass"),
])
def test_rule_outcomes(run_fields, mode, status):
    run = ModelRun.model_validate(run_fields)
    definition = run.descriptor.rules[0]
    table_id = "missing" if mode == "missing" else "prices"

    def evaluate(context):
        if mode == "raises":
            raise ArithmeticError("private calculation detail")
        return CheckOutcome(
            rule_id=definition.rule_id, rule_version=definition.version,
            severity=definition.severity, input_ids=(table_id,),
            output_ids=("not-a-result",) if mode == "bad_scope" else ("price",),
            status="not_applicable" if mode == "excluded" else "pass",
            observed="One close per session", expected="One close per session",
            explanation="Unadjusted close requested" if mode == "excluded" else None,
        )

    rules = (Rule("coverage", (table_id,), ("price",), evaluate),)
    context = RuleContext(run.inputs, run.assumptions, CandidateResult(outputs=()))
    checks = evaluate_stage(run.descriptor, rules, "postcondition", context)
    assert checks[0].status == status
    if status == "pass":
        assert checks[0].explanation and "One close per session" in checks[0].explanation
    assert "private" not in (checks[0].explanation or "")


def test_blocking_postcondition_and_scoped_policy(run_fields):
    run = ModelRun.model_validate(run_fields)
    candidates = CandidateResult(outputs=tuple(
        CandidateOutput(output_id=item.output_id, value_type=item.value_type, value=item.value)
        for item in run.outputs
    ), trace=run.trace)
    failure = CheckOutcome(
        rule_id="coverage", rule_version="1", severity="blocking", status="fail",
        output_ids=("price",), explanation="Coverage below house policy",
    )
    exception = PolicyException(
        exception_id="exception", rule_id="coverage", rule_version="1", author="reviewer",
        output_ids=("price",), rationale="Approved use with limited coverage", policy_version="1",
    )
    outputs = resolve_outputs(run.descriptor, candidates, (failure,), inputs=run.inputs)
    assert [item.status for item in outputs] == ["withheld", "withheld", "withheld", "unverified"]
    allowed = resolve_outputs(
        run.descriptor, candidates, (failure,), inputs=run.inputs, exceptions=(exception,),
    )
    assert allowed[0].status == "unverified"
    assert allowed[0].exception_ids == ("exception",)
    with pytest.raises(ValueError, match="policy"):
        resolve_outputs(
            run.descriptor, candidates, (failure,), inputs=run.inputs,
            exceptions=(exception.model_copy(update={"policy_version": "old"}),),
        )


@pytest.mark.parametrize("stage", ["precondition", "invariant", "postcondition"])
def test_domain_failure_at_each_stage_cannot_be_excepted(run_fields, stage):
    run_fields["descriptor"]["rules"][0].update(stage=stage, exception_policy_version=None)
    run = ModelRun.model_validate(run_fields)

    def evaluate(context):
        assert (context.candidate is None) == (stage == "precondition")
        return CheckOutcome(
            rule_id="coverage", rule_version="1", severity="blocking", status="fail",
            input_ids=("prices",), output_ids=("price",), explanation="Mathematical domain failure",
        )

    rules = (Rule("coverage", ("prices",), ("price",), evaluate),)
    candidate = None if stage == "precondition" else CandidateResult(outputs=())
    checks = evaluate_stage(run.descriptor, rules, stage, RuleContext(run.inputs, run.assumptions, candidate))
    assert blocked_outputs(run.descriptor, checks) == {"price", "spread", "adjusted"}
    exception = PolicyException(
        exception_id="exception", rule_id="coverage", rule_version="1", author="reviewer",
        output_ids=("price",), rationale="Requested exception", policy_version="1",
    )
    with pytest.raises(ValueError, match="house policy"):
        blocked_outputs(run.descriptor, checks, (exception,))
