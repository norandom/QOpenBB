from decimal import Decimal

import pytest
from qopenbb_data.modeling.contracts.checks import CheckOutcome, Tolerance
from qopenbb_data.modeling.contracts.results import ModelRun
from qopenbb_data.modeling.contracts.trace import TraceEntry
from qopenbb_data.modeling.models.protocol import CandidateOutput, CandidateResult
from qopenbb_data.modeling.validation.lifecycle import evaluate_run
from qopenbb_data.modeling.validation.rules import Rule
from qopenbb_data.modeling.verification.reference import Reference
from test_model_run_evidence import run_fields as run_fields_fixture

run_fields = run_fields_fixture


@pytest.mark.parametrize(
    ("precondition", "expected_calls", "expected"),
    [
        ("all", [], ("withheld", "withheld")),
        ("partial", [("independent",)], ("withheld", "verified")),
        ("false_numeric_pass", [("independent",)], ("withheld", "verified")),
        ("bare_pass", [("independent",)], ("withheld", "verified")),
        ("numeric_boundary", [("price", "spread", "adjusted", "independent")], ("verified", "verified")),
        ("unknown", [("independent",)], ("withheld", "verified")),
        ("invariant_failure", [("price", "spread", "adjusted", "independent")], ("verified", "withheld")),
        ("postcondition_failure", [("price", "spread", "adjusted", "independent")], ("verified", "withheld")),
        ("pass", [("price", "spread", "adjusted", "independent")], ("verified", "verified")),
        ("mutated", [("price", "spread", "adjusted", "independent")], ("withheld", "verified")),
    ],
)
def test_evaluate_run_gates_calculation_and_verifies_independent_sibling(
    run_fields, precondition, expected_calls, expected,
):
    run_fields["descriptor"]["rules"][0].update(stage="precondition")
    stage = "invariant" if precondition == "invariant_failure" else "postcondition"
    run_fields["descriptor"]["rules"][1].update(stage=stage)
    run = ModelRun.model_validate(run_fields)
    calls = []
    checks_called = []
    affected = ("price", "independent") if precondition == "all" else ("price",)

    def check_coverage(context):
        checks_called.append("precondition")
        assert context.candidate is None
        if precondition == "unknown":
            status = "unknown"
        else:
            status = "fail" if precondition in {"all", "partial"} else "pass"
        evidence = {"observed": "Complete observations", "expected": "Complete observations"}
        if precondition in {"false_numeric_pass", "numeric_boundary"}:
            boundary = precondition == "numeric_boundary"
            evidence = {
                "observed_value": Decimal("1.125") if boundary else Decimal(9),
                "expected_value": Decimal(1),
                "tolerance": Tolerance(unit="usd", scale=3, absolute="0.125" if boundary else "0"),
            }
        elif precondition == "bare_pass":
            evidence = {}
        return CheckOutcome(
            rule_id="coverage", rule_version="1", severity="blocking",
            status=status,
            output_ids=affected, input_ids=("prices",),
            explanation=None if status == "pass" else "Observation coverage insufficient",
            **evidence,
        )

    def check_calculation(context):
        checks_called.append(stage)
        assert context.candidate is not None
        fails = precondition in {"invariant_failure", "postcondition_failure"}
        return CheckOutcome(
            rule_id="reconciliation", rule_version="1", severity="blocking",
            status="fail" if fails else "pass", output_ids=("independent",),
            observed="Reconciliation recorded", expected="Reconciliation recorded",
            explanation="Reconciliation difference exceeds tolerance" if fails else None,
        )

    def calculate(inputs, assumptions, eligible):
        calls.append(eligible)
        close = inputs.tables[0].rows[0].value
        assert isinstance(close, Decimal)
        outputs = tuple(
            CandidateOutput(
                output_id=key, value=close * (3 if key == "price" and precondition == "mutated" else 2),
            )
            for key in eligible
        )
        trace = tuple(
            TraceEntry(
                trace_id=f"trace-{key}", formula_id="double-close", formula_version="1",
                expression="close * 2", output_id=key,
                input_ids=("prices",), source_record_ids=("prices-close",),
            )
            for key in eligible
        )
        return CandidateResult(outputs=outputs, trace=trace)

    def reference_value(inputs, assumptions):
        close = inputs.tables[0].rows[0].value
        assert close is not None
        return close + close

    result = evaluate_run(
        run.descriptor, run.inputs, run.assumptions,
        run_id=run.run_id, owner_id=run.owner_id, created_at=run.created_at,
        rules=(
            Rule("coverage", ("prices",), affected, check_coverage),
            Rule("reconciliation", (), ("independent",), check_calculation),
        ),
        calculate=calculate,
        reference=Reference("1", {"price": reference_value, "independent": reference_value}, {}),
    )
    if precondition in {"false_numeric_pass", "numeric_boundary", "bare_pass"}:
        check = result.checks[0]
        assert check.status == {
            "false_numeric_pass": "fail", "numeric_boundary": "pass", "bare_pass": "unknown",
        }[precondition]
        if precondition == "false_numeric_pass":
            assert (check.observed_value, check.expected_value) == (Decimal(9), Decimal(1))
            assert check.tolerance == Tolerance(unit="usd", scale=3, absolute="0")
    assert calls == expected_calls
    assert checks_called == (["precondition", stage] if expected_calls else ["precondition"])
    by_id = {item.output_id: item.status for item in result.outputs}
    assert (by_id["price"], by_id["independent"]) == expected
    if precondition == "mutated":
        assert (by_id["spread"], by_id["adjusted"]) == ("withheld", "withheld")
        assert next(item for item in result.verification if item.output_id == "price").status == "mismatch"
    assert ModelRun.model_validate_json(result.model_dump_json()) == result
