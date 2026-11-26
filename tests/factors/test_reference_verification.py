from decimal import Decimal

import pytest
from pydantic import ValidationError
from qopenbb_data.modeling.contracts.checks import Tolerance
from qopenbb_data.modeling.contracts.results import ModelRun
from qopenbb_data.modeling.contracts.trace import TraceEntry
from qopenbb_data.modeling.models.protocol import CandidateOutput, CandidateResult
from qopenbb_data.modeling.validation.lifecycle import evaluate_run
from qopenbb_data.modeling.verification.reference import Reference, verify_outputs
from test_model_run_evidence import run_fields as run_fields_fixture

run_fields = run_fields_fixture


def calculate_fixture(inputs, *, mutated):
    close = inputs.tables[0].rows[0].value
    assert close is not None
    return close * (3 if mutated else 2)


def independently_recalculate(inputs, assumptions):
    close = inputs.tables[0].rows[0].value
    assert close is not None
    return close + close


@pytest.mark.parametrize("changed_close", ["10.25", "107.125"])
@pytest.mark.parametrize("mutated", [False, True])
def test_reference_uses_supplied_input_and_detects_mutation(run_fields, changed_close, mutated):
    run_fields["inputs"]["tables"][0]["rows"][0]["value"] = changed_close
    run = ModelRun.model_validate(run_fields)
    production = calculate_fixture(run.inputs, mutated=mutated)
    price = run.outputs[0].model_copy(update={"value": production})
    reference = Reference("1", {"price": independently_recalculate}, {
        "price": Tolerance(unit=price.unit, absolute=Decimal(0)),
    })
    outputs, evidence, _ = verify_outputs(
        run.descriptor, run.inputs, run.assumptions, (price, *run.outputs[1:]),
        run.trace, run.checks, reference,
    )
    assert outputs[0].status == ("withheld" if mutated else "verified")
    assert evidence[0].status == ("mismatch" if mutated else "match")
    assert [item.status for item in outputs[1:]] == (
        ["withheld", "withheld", "unverified"] if mutated else ["unverified"] * 3
    )
    assert str(production) in evidence[0].explanation
    verified_run = ModelRun.model_validate({
        **run_fields, "outputs": outputs, "verification": evidence,
    })
    assert verified_run.verification == evidence
    run_fields["inputs"]["tables"][0]["rows"][0]["value"] = "99"
    with pytest.raises(ValidationError, match="verification fingerprints"):
        ModelRun.model_validate({**run_fields, "outputs": outputs, "verification": evidence})


def test_missing_reference_is_unavailable(run_fields):
    run = ModelRun.model_validate(run_fields)
    outputs, evidence, _ = verify_outputs(
        run.descriptor, run.inputs, run.assumptions, run.outputs, run.trace, run.checks, None,
    )
    assert outputs[0].status == "unverified"
    assert evidence[0].status == "unavailable"


@pytest.mark.parametrize("eligible", [True, False], ids=["eligible-dependency", "missing-dependency"])
def test_withheld_dependency_does_not_hide_independent_eligibility(run_fields, eligible):
    for item in run_fields["outputs"][:3]:
        item.update(status="withheld", value=None, reason="Production value unavailable")
    run = ModelRun.model_validate(run_fields)
    reference = Reference("1", {
        "price": lambda *_: Decimal(0) if eligible else None,
        "spread": lambda *_: Decimal(-2),
        "adjusted": lambda *_: None,
        "independent": lambda *_: Decimal(10),
    }, {})
    outputs, evidence, trace = verify_outputs(
        run.descriptor, run.inputs, run.assumptions, run.outputs, run.trace, run.checks, reference,
    )
    assert outputs[:3] == run.outputs[:3]
    if eligible:
        assert [item.status for item in evidence] == ["mismatch", "mismatch", "unavailable", "match"]
        assert "expected 0" in evidence[0].explanation
        assert "expected -2" in evidence[1].explanation
    else:
        assert [item.status for item in evidence] == ["unavailable"] * 3 + ["match"]
        assert evidence[1].explanation == "A required output was withheld"
    saved = ModelRun.model_validate(run_fields | {"outputs": outputs, "verification": evidence, "trace": trace})
    assert ModelRun.model_validate_json(saved.model_dump_json()) == saved


def test_policy_denial_preserves_withholding_and_dependency_evidence(run_fields):
    run_fields["checks"][0].update(status="fail", explanation="House policy denies this result")
    for item in run_fields["outputs"][:3]:
        item.update(status="withheld", value=None, reason="A blocking financial rule failed")
    run = ModelRun.model_validate(run_fields)
    reference = Reference("1", {
        "price": lambda *_: Decimal(10),
        "spread": lambda *_: Decimal(0),
        "adjusted": lambda *_: Decimal(-2),
        "independent": lambda *_: Decimal(10),
    }, {})
    outputs, evidence, _ = verify_outputs(
        run.descriptor, run.inputs, run.assumptions, run.outputs, run.trace, run.checks, reference,
    )
    assert outputs[:3] == run.outputs[:3]
    assert [item.status for item in evidence] == ["unavailable"] * 3 + ["match"]


@pytest.mark.parametrize("status", ["unknown", "error", "not_applicable"])
def test_reference_match_cannot_promote_unavailable_check(run_fields, status):
    run_fields["checks"][0].update(status=status, explanation="Coverage evidence unavailable")
    run = ModelRun.model_validate(run_fields)
    reference = Reference("1", {"price": lambda inputs, _: inputs.tables[0].rows[0].value}, {})
    outputs, evidence, _ = verify_outputs(
        run.descriptor, run.inputs, run.assumptions, run.outputs, run.trace, run.checks, reference,
    )
    assert evidence[0].status == "match"
    assert run.outputs[0].value == outputs[0].value
    assert outputs[0].status == "unverified"


def test_exact_text_comparison_with_large_values_retains_serializable_evidence(run_fields):
    run_fields["descriptor"]["outputs"][0]["value_type"] = "text"
    run_fields["outputs"][0].update(value="a" * 4096, value_type="text")
    run = ModelRun.model_validate(run_fields)
    reference = Reference("1", {"price": lambda *_: "b" * 4096}, {})

    def calculate(inputs, assumptions, eligible):
        return CandidateResult(
            outputs=(CandidateOutput(output_id="price", value_type="text", value="a" * 4096),),
            trace=(TraceEntry(
                trace_id="candidate-text", formula_id="produce-text", formula_version="1",
                expression="Produce the textual conclusion", output_id="price",
            ),),
        )

    saved = evaluate_run(
        run.descriptor, run.inputs, run.assumptions, run_id=run.run_id,
        owner_id=run.owner_id, created_at=run.created_at, rules=(),
        calculate=calculate, reference=reference,
    )
    restored = ModelRun.model_validate_json(saved.model_dump_json())
    price = restored.outputs[0]
    assert price.status == "withheld"
    assert restored.verification[0].status == "mismatch"
    comparison = next(entry for entry in restored.trace if entry.formula_id == "independent-text-comparison")
    assert comparison.trace_id in price.trace_ids
    assert {item.transformation_id: item.description for item in comparison.transformations} == {
        "observed-text": "a" * 4096, "expected-text": "b" * 4096,
    }


@pytest.mark.parametrize("changed", ["assumption", "reference_version", "input"])
def test_stale_match_cannot_verify_a_new_run(run_fields, changed):
    run = ModelRun.model_validate(run_fields)
    reference = Reference("1", {"price": lambda inputs, _: inputs.tables[0].rows[0].value}, {})
    outputs, evidence, _ = verify_outputs(
        run.descriptor, run.inputs, run.assumptions, run.outputs, run.trace, run.checks, reference,
    )
    assert outputs[0].status == "verified"

    if changed == "assumption":
        run_fields["assumptions"]["effective_date"] = "2024-01-03"
    elif changed == "reference_version":
        run_fields["descriptor"]["reference_version"] = "2"
    else:
        run_fields["inputs"]["tables"][0]["rows"][0]["value"] = "12"
    with pytest.raises(ValidationError, match="verification fingerprints|reference version"):
        ModelRun.model_validate({**run_fields, "outputs": outputs, "verification": evidence})

    changed_run = ModelRun.model_validate(run_fields)
    outputs, evidence, _ = verify_outputs(
        changed_run.descriptor, changed_run.inputs, changed_run.assumptions, outputs,
        changed_run.trace, changed_run.checks, None if changed == "assumption" else reference,
    )
    assert outputs[0].status == ("withheld" if changed == "input" else "unverified")
    assert evidence[0].status == ("mismatch" if changed == "input" else "unavailable")


@pytest.mark.parametrize("limit", ["output", "run"])
def test_text_mismatch_fails_if_trace_is_full(run_fields, limit):
    run_fields["descriptor"]["outputs"][0]["value_type"] = "text"
    run_fields["outputs"][0].update(value="observed", value_type="text")
    run = ModelRun.model_validate(run_fields)
    reference = Reference("1", {"price": lambda *_: "expected"}, {})
    output_ids = ("price",) if limit == "output" else tuple(item.output_id for item in run.outputs)
    trace = tuple(
        TraceEntry(
            trace_id=f"trace-{key}-{index}", formula_id="produce-text", formula_version="1",
            expression="Produce the textual conclusion", output_id=key,
        )
        for key in output_ids for index in range(256)
    )
    outputs = tuple(
        item.model_copy(update={"trace_ids": tuple(entry.trace_id for entry in trace if entry.output_id == item.output_id)})
        for item in run.outputs
    )
    with pytest.raises(ValueError, match="Trace capacity exhausted"):
        verify_outputs(
            run.descriptor, run.inputs, run.assumptions, outputs, trace, run.checks, reference,
        )


@pytest.mark.parametrize(("kind", "observed", "bad_reference"), [
    ("text", "observed", ""),
    ("text", "observed", " \t\n"),
    ("text", "observed", "b" * 4097),
    ("integer", 1, 2**63),
    ("integer", 1, -(2**63) - 1),
])
def test_invalid_reference_scalar_does_not_abort_independent_sibling(
    run_fields, kind, observed, bad_reference,
):
    run_fields["descriptor"]["outputs"][0]["value_type"] = kind
    run_fields["outputs"][0].update(value=observed, value_type=kind)
    run = ModelRun.model_validate(run_fields)
    reference = Reference("1", {
        "price": lambda *_: bad_reference,
        "independent": lambda *_: Decimal(10),
    }, {})

    def calculate(inputs, assumptions, eligible):
        return CandidateResult(
            outputs=(
                CandidateOutput(output_id="price", value_type=kind, value=observed),
                CandidateOutput(output_id="independent", value=Decimal(10)),
            ),
            trace=tuple(
                TraceEntry(
                    trace_id=f"candidate-{key}", formula_id="test-calculation", formula_version="1",
                    expression="Evaluate the supplied test inputs", output_id=key,
                )
                for key in ("price", "independent")
            ),
        )

    result = evaluate_run(
        run.descriptor, run.inputs, run.assumptions, run_id=run.run_id,
        owner_id=run.owner_id, created_at=run.created_at, rules=(),
        calculate=calculate, reference=reference,
    )
    assert result.outputs[0].status == "unverified"
    assert result.verification[0].status == "unavailable"
    assert result.outputs[-1].status == "verified"
    assert result.verification[-1].status == "match"
