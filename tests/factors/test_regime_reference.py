"""Independent DFII10 comparison against dated candidates."""

from datetime import timedelta
from decimal import Decimal

import pytest
from fixtures.factor_examples import EXAMPLES, UNKNOWN_DFII10_AVAILABILITY, build_run
from qopenbb_data.modeling.contracts import CheckOutcome
from qopenbb_data.modeling.models.factors.real_yield import RealYieldModel
from qopenbb_data.modeling.validation.outputs import resolve_outputs
from qopenbb_data.modeling.validation.rules import Rule, RuleContext, evaluate_stage
from qopenbb_data.modeling.verification.factors.regime_reference import regime_reference
from qopenbb_data.modeling.verification.reference import verify_outputs

EXAMPLE = EXAMPLES["real_yield_regime"]


def verify(run, values, *, trace=None):
    outputs = tuple(row.model_copy(update={"value": value})
                    for row, value in zip(run.outputs, values, strict=True))
    return verify_outputs(run.descriptor, run.inputs, run.assumptions, outputs,
                          run.trace if trace is None else trace, run.checks, regime_reference())[:2]


def with_levels(run, *levels):
    sessions, table = run.inputs.tables
    inputs = run.inputs.model_copy(update={"tables": (sessions, table.model_copy(update={"rows": levels}))})
    return run.model_copy(update={"inputs": inputs})


@pytest.mark.parametrize(("last_value", "regime", "change"), [
    ("1.75", "rising", "0.25"), ("1.50", "flat", "0"), ("1.25", "falling", "-0.25"),
])
def test_point_in_time_regime_and_late_revision_mutant(last_value, regime, change):
    run = build_run(EXAMPLE, False)
    first, last = run.inputs.tables[1].rows
    last = last.model_copy(update={"value": Decimal(last_value)})
    late = last.model_copy(update={
        "record_id": "later_revision", "vintage_at": run.inputs.cutoff.decision_at + timedelta(seconds=1),
        "value": Decimal(-1),
    })
    run = with_levels(run, late, last, first)
    candidate = RealYieldModel().calculate(run.inputs, run.assumptions)
    assert [item.substitutions[-1].period_end for item in candidate.trace] == [last.observation_date] * 2
    assert [item.substitutions[0].period_end for item in candidate.trace] == [first.observation_date] * 2
    assert all(late.record_id not in item.source_record_ids for item in candidate.trace)
    values = tuple(item.value for item in candidate.outputs)
    assert values == (regime, Decimal(change))
    outputs, evidence = verify(run, values, trace=candidate.trace)
    assert [item.status for item in outputs] == ["verified", "verified"]
    assert [item.status for item in evidence] == ["match", "match"]
    outputs, evidence = verify(run, ("falling", Decimal("-2.50")))
    assert [item.status for item in outputs] == [
        "verified" if regime == "falling" else "withheld", "withheld",
    ]
    assert [item.status for item in evidence] == [
        "match" if regime == "falling" else "mismatch", "mismatch",
    ]


@pytest.mark.parametrize("case", ["missing", "unknown", "unit", "early_evaluation"])
def test_missing_regime_is_checked_independently(case):
    run = build_run(UNKNOWN_DFII10_AVAILABILITY if case == "unknown" else EXAMPLE,
                    case in {"missing", "unknown"})
    if case == "unit":
        first, last = run.inputs.tables[1].rows
        run = with_levels(run, first, last.model_copy(
            update={"context": last.context.model_copy(update={"unit": "ratio"})}))
    if case == "early_evaluation":
        cutoff = run.inputs.cutoff
        cutoff = cutoff.model_copy(update={"evaluated_at": cutoff.decision_at - timedelta(hours=2)})
        run = run.model_copy(update={"inputs": run.inputs.model_copy(update={"cutoff": cutoff})})
    candidate = RealYieldModel().calculate(run.inputs, run.assumptions)
    for output in candidate.outputs:
        expected = regime_reference().calculations[output.output_id](run.inputs, run.assumptions)
        assert expected is output.value is None
        assert str(run.inputs.cutoff.observation_date) in output.reason
    if case in {"missing", "unknown"}:
        assert [item.status for item in run.checks] == ["fail", "fail"]
        assert [item.reason for item in candidate.outputs] == [item.explanation for item in run.checks]
        outputs, evidence, _ = verify_outputs(run.descriptor, run.inputs, run.assumptions, run.outputs,
                                             candidate.trace, run.checks, regime_reference())
        assert [item.status for item in outputs] == ["withheld", "withheld"]
        assert [item.status for item in evidence] == ["unavailable", "unavailable"]


@pytest.mark.parametrize(("offset", "comparison", "status"), [
    ("0.00000002", "match", "verified"), ("0.000000021", "mismatch", "withheld"),
])
def test_frozen_regime_tolerance(offset, comparison, status):
    run = build_run(EXAMPLE, False)
    outputs, evidence = verify(run, ("rising", Decimal("0.25") + Decimal(offset)))
    assert (evidence[1].status, outputs[1].status) == (comparison, status)


@pytest.mark.parametrize("field", ["schema_id", "schema_version", "version", "effective_date", "assumptions", "cutoff"])
def test_regime_requires_versioned_dated_assumptions(field):
    run = build_run(EXAMPLE, False)
    if field in {"schema_id", "schema_version", "cutoff"}:
        inputs = run.inputs.model_copy(update={field: None if field == "cutoff" else "2"})
        assumptions = run.assumptions
    else:
        inputs = run.inputs
        values = {"version": "2", "effective_date": run.inputs.cutoff.observation_date + timedelta(days=1),
                  "assumptions": ()}
        assumptions = run.assumptions.model_copy(update={field: values[field]})
    assert all(calculate(inputs, assumptions) is None
               for calculate in regime_reference().calculations.values())


def evaluate_reference(run, candidate):
    reference = regime_reference()

    def bind(output):
        rule_id, = output.required_check_ids

        def evaluate(context):
            value = reference.calculations[output.output_id](context.inputs, context.assumptions)
            return CheckOutcome(
                rule_id=rule_id, rule_version="1", severity="blocking",
                input_ids=output.required_input_ids, output_ids=(output.output_id,),
                status="fail" if value is None else "pass",
                observed="insufficient evidence" if value is None else "eligible dated inputs",
                expected="eligible dated inputs",
                explanation="Independent calculation has insufficient evidence" if value is None else None,
            )

        return Rule(rule_id, output.required_input_ids, (output.output_id,), evaluate)

    rules = tuple(bind(output) for output in run.descriptor.outputs)
    checks = evaluate_stage(run.descriptor, rules, "precondition", RuleContext(run.inputs, run.assumptions))
    outputs = resolve_outputs(run.descriptor, candidate, checks, inputs=run.inputs)
    outputs, evidence, _ = verify_outputs(run.descriptor, run.inputs, run.assumptions, outputs,
                                         candidate.trace, checks, reference)
    return checks, outputs, evidence


@pytest.mark.parametrize(("case", "check_status", "explanation", "output_reason"), [
    ("missing_table", "unknown", "Required input table is absent", "A required input table is absent"),
    ("wrong_unit", "fail", "Independent calculation has insufficient evidence", "A blocking financial rule failed"),
    ("valid", "pass", "Observed condition met the expectation: eligible dated inputs", None),
])
def test_regime_reference_preconditions(case, check_status, explanation, output_reason):
    run = build_run(EXAMPLE, False)
    original, measured = run.inputs.tables
    tables = (original, measured)
    if case == "missing_table":
        tables = (original,)
    elif case == "wrong_unit":
        row = measured.rows[-1]
        wrong_unit = row.model_copy(update={"context": row.context.model_copy(update={"unit": "ratio"})})
        tables = (original, measured.model_copy(update={"rows": (*measured.rows[:-1], wrong_unit)}))
    run = run.model_copy(update={"inputs": run.inputs.model_copy(update={"tables": tables})})
    candidate = RealYieldModel().calculate(run.inputs, run.assumptions)
    reference = regime_reference()
    values = tuple(reference.calculations[item.output_id](run.inputs, run.assumptions)
                   for item in candidate.outputs)
    assert values == tuple(item.value for item in candidate.outputs)
    checks, outputs, evidence = evaluate_reference(run, candidate)
    assert [(check.rule_id, check.status, check.explanation) for check in checks] == [
        (definition.rule_id, check_status, explanation) for definition in run.descriptor.rules
    ]
    verified = case == "valid"
    assert [(item.status, item.value, item.reason, item.check_ids) for item in outputs] == [
        ("verified" if verified else "withheld", value, output_reason, definition.required_check_ids)
        for value, definition in zip(values, run.descriptor.outputs, strict=True)
    ]
    assert [item.status for item in evidence] == ["match" if verified else "unavailable"] * len(values)
