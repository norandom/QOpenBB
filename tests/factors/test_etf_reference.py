"""Exercise ETF references against production candidates and the foundation verifier."""

from datetime import timedelta
from decimal import Decimal
from functools import cache, partial

import pytest
from fixtures.factor_examples import EXAMPLES, build_run, text_assumption
from fixtures.factor_inputs import END, HOLIDAYS, SESSIONS, START, utc
from qopenbb_data.modeling.contracts import CheckOutcome, InputSnapshot
from qopenbb_data.modeling.models.factors.comparison import ProxyComparisonModel
from qopenbb_data.modeling.models.factors.momentum import MomentumModel
from qopenbb_data.modeling.models.factors.volatility import VolatilityModel
from qopenbb_data.modeling.validation.outputs import resolve_outputs
from qopenbb_data.modeling.validation.rules import Rule, RuleContext, evaluate_stage
from qopenbb_data.modeling.verification.factors.etf import (
    comparison_reference,
    momentum_reference,
    volatility_reference,
)
from qopenbb_data.modeling.verification.reference import verify_outputs

MODELS = (
    (MomentumModel(), momentum_reference),
    (VolatilityModel(), volatility_reference),
    (ProxyComparisonModel(), comparison_reference),
)
RIGHT_AND_SPREADS = {"right_momentum", "right_volatility", "momentum_spread", "volatility_spread"}


@pytest.fixture(params=MODELS, ids=["momentum", "volatility", "comparison"])
def case(request):
    model, factory = request.param
    return model, factory(), build_run(EXAMPLES[model.describe().model_id], missing=False)


def _snapshot(inputs, replacements):
    tables = tuple(table.model_copy(update={"rows": replacements.get(table.table_id, table.rows)})
                   for table in inputs.tables)
    return InputSnapshot.model_validate({**inputs.model_dump(), "tables": tables})


def _check_eligibility(definition, assess, context):
    result = assess(context).get(definition.output_id)
    available = result is not None and result.value is not None
    return CheckOutcome(
        rule_id=definition.required_check_ids[0], rule_version="1", severity="blocking",
        status="pass" if available else "fail",
        observed="Eligible calculation inputs" if available else None,
        expected="Eligible calculation inputs",
        explanation=None if available else (result.reason if result else "Calculation output is absent"),
        input_ids=definition.required_input_ids, output_ids=(definition.output_id,),
    )


def _evaluate(model, inputs, assumptions, mutate=None):
    descriptor = model.describe()
    context = RuleContext(inputs, assumptions)

    @cache
    def calculate():
        return model.calculate(context.inputs, context.assumptions)

    def assess(_context):
        # The fixture binds preconditions to production eligibility. The runner
        # checks table presence before it calls any bound rule.
        return {result.output_id: result for result in calculate().outputs}

    rules = tuple(
        Rule(definition.required_check_ids[0], definition.required_input_ids,
             (definition.output_id,), partial(_check_eligibility, definition, assess))
        for definition in descriptor.outputs
    )
    checks = evaluate_stage(descriptor, rules, "precondition", context)
    candidate = calculate()
    if mutate is not None:
        candidate = mutate(candidate)
    outputs = resolve_outputs(descriptor, candidate, checks, inputs=inputs)
    return descriptor, outputs, candidate, checks


def _verify(case, inputs, assumptions, missing=(), *, unknown=()):
    model, reference, _ = case
    descriptor, outputs, candidate, checks = _evaluate(model, inputs, assumptions)
    production = {result.output_id: result.value for result in candidate.outputs}
    trace = candidate.trace
    expected_checks = {}
    for output, check in zip(outputs, checks, strict=True):
        absent = output.output_id in missing
        # The verifier skips null candidates. Compare independent availability explicitly.
        expected = reference.calculations[output.output_id](inputs, assumptions)
        assert (expected is None) == (production[output.output_id] is None) == (output.value is None) == absent
        assert check.output_ids == (output.output_id,)
        if output.output_id in unknown:
            expected_checks[check.rule_id] = "unknown"
            assert check.explanation == "Required input table is absent"
        else:
            expected_checks[check.rule_id] = "fail" if absent else "pass"
    assert {check.rule_id: check.status for check in checks} == expected_checks

    final, evidence, _ = verify_outputs(descriptor, inputs, assumptions, outputs, trace, checks, reference)
    assert {item.output_id: item.status for item in final} == {
        item.output_id: "withheld" if item.output_id in missing else "verified" for item in outputs
    }
    assert {item.output_id: item.status for item in evidence} == {
        item.output_id: "unavailable" if item.output_id in missing else "match" for item in outputs
    }
    return final, trace


@pytest.mark.parametrize("first_path", ["up", "flat", "down"])
def test_price_metrics_use_signed_returns_and_frozen_units(case, first_path):
    _, reference, run = case
    _, left, *_ = run.inputs.tables
    level = {"up": "120", "flat": "100", "down": "80"}[first_path]
    closes = tuple(row.model_copy(update={"value": Decimal(level)})
                   if row.observation_date != START else row for row in left.rows)
    inputs = _snapshot(run.inputs, {left.table_id: closes})
    outputs, trace = _verify(case, inputs, run.assumptions)
    expected = {"momentum": Decimal(level) - 100, "realized_volatility": 2 * abs(Decimal(level) - 100)}
    expected.update(left_momentum=expected["momentum"], left_volatility=expected["realized_volatility"],
                    right_momentum=Decimal(10), right_volatility=Decimal(20),
                    momentum_spread=expected["momentum"] - 10, volatility_spread=expected["realized_volatility"] - 20)
    assert reference.version == "1"
    for item in outputs:
        unit, bound = ("percentage_points", "0.00000002") if item.output_id.endswith("_spread") else (
            "percent", "0.00000001"
        )
        tolerance = reference.tolerances[item.output_id]
        assert (item.unit, tolerance.unit, tolerance.absolute, tolerance.relative, tolerance.scale) == (
            unit, unit, Decimal(bound), None, 0,
        )
        assert item.value == expected[item.output_id]
        assert reference.calculations[item.output_id](inputs, run.assumptions) == expected[item.output_id]
    for entry in trace:
        assert entry.substitutions[0].period_end == START
        assert entry.substitutions[1].period_end == END


def test_shuffle_holiday_older_session_and_late_revisions_do_not_change_window(case):
    _, _, run = case
    schedule, left, *_ = run.inputs.tables
    first, last = left.rows[0], left.rows[-1]
    holiday = first.model_copy(update={
        "record_id": "holiday", "observation_date": min(HOLIDAYS), "value": Decimal(1),
    })
    older = schedule.rows[0].model_copy(update={
        "record_id": "older-session", "observation_date": START - timedelta(days=4),
    })
    revised = (
        last.model_copy(update={"record_id": "late-publication", "published_at": utc(END, 23),
                                "vintage_at": utc(END, 21), "value": Decimal(1)}),
        last.model_copy(update={"record_id": "late-vintage", "vintage_at": utc(END, 23),
                                "value": Decimal(2)}),
    )
    inputs = _snapshot(run.inputs, {
        "sessions": (*reversed(schedule.rows), older),
        left.table_id: (*reversed(left.rows), holiday, *revised),
    })
    outputs, trace = _verify(case, inputs, run.assumptions)
    assert outputs[0].value == run.outputs[0].value
    assert trace[0].source_record_ids[:64] == tuple(row.record_id for row in schedule.rows)
    assert trace[0].source_record_ids[64:] == tuple(row.record_id for row in left.rows)


def test_revision_at_decision_cutoff_replaces_older_close(case):
    _, _, run = case
    _, left, *_ = run.inputs.tables
    revision = left.rows[-1].model_copy(update={
        "record_id": "eligible-revision", "vintage_at": run.inputs.cutoff.decision_at,
        "value": Decimal(90),
    })
    inputs = _snapshot(run.inputs, {left.table_id: (revision, *left.rows)})
    outputs, trace = _verify(case, inputs, run.assumptions)
    assert "eligible-revision" in trace[0].source_record_ids
    assert left.rows[-1].record_id not in trace[0].source_record_ids
    if outputs[0].output_id.endswith("momentum"):
        assert outputs[0].value == Decimal(-10)


@pytest.mark.parametrize("problem", ["short_schedule", "missing_close", "gap", "conflict", "late",
                                     "early_evaluation", "unknown", "estimate", "unit", "zero", "negative"])
def test_window_exclusions_compare_production_and_reference_availability(case, problem):
    _, reference, run = case
    schedule, *legs = run.inputs.tables
    target = legs[-1]
    index = 12
    rows = list(target.rows)
    close = rows[index]
    inputs = run.inputs
    if problem == "short_schedule":
        inputs = _snapshot(inputs, {"sessions": schedule.rows[1:]})
    elif problem == "missing_close":
        inputs = _snapshot(inputs, {target.table_id: rows[:-1]})
    elif problem == "gap":
        inputs = _snapshot(inputs, {target.table_id: rows[:index] + rows[index + 3:]})
    elif problem == "conflict":
        # Equal publication times are allowed under distinct vintage keys.
        rows.append(close.model_copy(update={
            "record_id": "conflicting-close", "vintage_at": close.published_at, "value": Decimal(1),
        }))
    elif problem == "early_evaluation":
        inputs = inputs.model_copy(update={"cutoff": inputs.cutoff.model_copy(
            update={"evaluated_at": utc(END, 20)})})
    else:
        updates = {
            "late": {"published_at": utc(END, 23)},
            "unknown": {"context": close.context.model_copy(update={"vintage_coverage": "unknown"})},
            "estimate": {"category": "estimate"},
            "unit": {"context": close.context.model_copy(update={"unit": "percent"})},
            "zero": {"value": Decimal(0)},
            "negative": {"value": Decimal(-1)},
        }
        rows[index] = close.model_copy(update=updates[problem])
    if problem not in {"short_schedule", "missing_close", "gap", "early_evaluation"}:
        inputs = _snapshot(inputs, {target.table_id: rows})
    missing = RIGHT_AND_SPREADS if len(legs) == 2 and problem not in {
        "short_schedule", "early_evaluation"
    } else reference.calculations
    _verify(case, inputs, run.assumptions, missing)


@pytest.mark.parametrize("problem", ["basis", "revision", "effective_date", "no_cutoff", "wrong_schema"])
def test_invalid_assumptions_and_cutoff_withhold_all_outputs(case, problem):
    _, reference, run = case
    inputs, assumptions = run.inputs, run.assumptions
    if problem in {"basis", "revision"}:
        key = {"basis": "price_basis", "revision": "schedule_revision"}[problem]
        fields = tuple(item for item in assumptions.assumptions if item.assumption_id != key)
        if problem == "basis":
            fields += (text_assumption(key, "dividend_adjusted", "Wrong price-return basis"),)
        assumptions = assumptions.model_copy(update={"assumptions": fields})
    elif problem == "effective_date":
        assumptions = assumptions.model_copy(update={"effective_date": END + timedelta(days=1)})
    elif problem == "no_cutoff":
        inputs = inputs.model_copy(update={"cutoff": None})
    else:
        inputs = inputs.model_copy(update={"schema_id": "other.inputs"})
    _verify(case, inputs, assumptions, reference.calculations)


def test_reference_rejects_unsupported_assumption_and_input_schema_versions(case):
    _, reference, run = case
    for calculate in reference.calculations.values():
        assert calculate(run.inputs, run.assumptions.model_copy(update={"version": "2"})) is None
        assert calculate(run.inputs.model_copy(update={"schema_version": "2"}), run.assumptions) is None


def test_foundation_cannot_verify_against_a_different_reference_version(case):
    model, reference, run = case
    descriptor, outputs, candidate, checks = _evaluate(model, run.inputs, run.assumptions)
    descriptor = descriptor.model_copy(update={"reference_version": "2"})
    final, evidence, _ = verify_outputs(
        descriptor, run.inputs, run.assumptions, outputs, candidate.trace, checks, reference,
    )
    assert {item.status for item in final} == {"unverified"}
    assert {item.status for item in evidence} == {"unavailable"}


@pytest.mark.parametrize(("method", "mutant", "target"), [
    (1, "divisor", "realized_volatility"),
    (0, "observation_date", "momentum"),
    (2, "spread_direction", "momentum_spread"),
])
def test_foundation_rejects_mutated_candidate(method, mutant, target):
    model, factory = MODELS[method]
    reference = factory()
    run = build_run(EXAMPLES[model.describe().model_id], missing=False)
    inputs = run.inputs
    if mutant == "observation_date":
        # A one-session endpoint error must be visible in the candidate value.
        _, closes = inputs.tables
        previous = closes.rows[-2].model_copy(update={"value": Decimal(90)})
        assert previous.observation_date == SESSIONS[-2]
        inputs = _snapshot(inputs, {closes.table_id: (*closes.rows[:-2], previous, closes.rows[-1])})

    def mutate(candidate):
        values = []
        for output in candidate.outputs:
            if output.output_id == target:
                value = {
                    "divisor": lambda value=output.value: value * (Decimal(62) / Decimal(63)).sqrt(),
                    "observation_date": lambda: 100 * (previous.value / closes.rows[0].value - 1),
                    "spread_direction": lambda value=output.value: -value,
                }[mutant]()
                output = output.model_copy(update={"value": value})
            values.append(output)
        return candidate.model_copy(update={"outputs": tuple(values)})

    descriptor, outputs, candidate, checks = _evaluate(model, inputs, run.assumptions, mutate)
    final, evidence, _ = verify_outputs(
        descriptor, inputs, run.assumptions, outputs, candidate.trace, checks, reference,
    )
    assert all(check.status == "pass" for check in checks)
    for result, comparison in zip(final, evidence, strict=True):
        if result.output_id == target:
            assert (result.status, result.value, comparison.status) == ("withheld", None, "mismatch")
            assert result.reason == "Independent comparison mismatched"
        else:
            assert (result.status, comparison.status) == ("verified", "match")


@pytest.mark.parametrize(("absence", "state"), [("table", "unknown"), ("close", "fail")])
def test_right_input_absence_preserves_verified_left(absence, state):
    model, factory = MODELS[2]
    reference = factory()
    run = build_run(EXAMPLES[model.describe().model_id], missing=False)
    right = run.inputs.tables[-1]
    if absence == "table":
        inputs = run.inputs.model_copy(update={"tables": run.inputs.tables[:-1]})
    else:
        inputs = _snapshot(run.inputs, {right.table_id: right.rows[:-1]})

    unknown = RIGHT_AND_SPREADS if state == "unknown" else ()
    outputs, _ = _verify((model, reference, run), inputs, run.assumptions, RIGHT_AND_SPREADS, unknown=unknown)
    assert {output.output_id: output.value for output in outputs if output.status == "verified"} == {
        "left_momentum": Decimal(20), "left_volatility": Decimal(40),
    }


@pytest.mark.parametrize("problem", ["leg_version", "calendar"])
def test_pair_requires_both_legs_at_the_pinned_method_and_calendar(problem):
    model, factory = MODELS[2]
    reference = factory()
    run = build_run(EXAMPLES[model.describe().model_id], missing=False)
    inputs, assumptions = run.inputs, run.assumptions
    if problem == "leg_version":
        assumptions = assumptions.model_copy(update={"assumptions": tuple(
            item.model_copy(update={"value": "etf_momentum@2, etf_realized_volatility@1"})
            if item.assumption_id == "leg_methods" else item for item in assumptions.assumptions
        )})
        missing = reference.calculations
    else:
        schedule = inputs.tables[0]
        other = tuple(row.model_copy(update={
            "entity_id": "other_calendar", "record_id": f"other.{row.record_id}",
        }) for row in schedule.rows)
        inputs = _snapshot(inputs, {"sessions": schedule.rows + other})
        assumptions = assumptions.model_copy(update={"assumptions": (
            *assumptions.assumptions,
            text_assumption("left_calendar", schedule.rows[0].entity_id, "Left listing"),
            text_assumption("right_calendar", "other_calendar", "Right listing"),
        )})
        missing = {"momentum_spread", "volatility_spread"}
    _verify((model, reference, run), inputs, assumptions, missing)


@pytest.mark.parametrize(("mutation", "status", "evidence_status"), [
    ("boundary", "verified", "match"),
    ("outside", "withheld", "mismatch"),
    ("unit", "unverified", "unavailable"),
])
def test_verifier_applies_frozen_tolerance_in_the_output_unit(case, mutation, status, evidence_status):
    model, reference, run = case
    descriptor, outputs, candidate, checks = _evaluate(model, run.inputs, run.assumptions)
    index = next((i for i, output in enumerate(outputs) if output.output_id == "momentum_spread"), 0)
    target = outputs[index]
    bound = reference.tolerances[target.output_id].absolute
    if mutation == "unit":
        wrong_unit = "percentage_points" if target.unit == "percent" else "percent"
        changed = target.model_copy(update={"unit": wrong_unit})
    else:
        change = bound if mutation == "boundary" else bound + Decimal("0.000000001")
        changed = target.model_copy(update={"value": target.value + change})
    candidates = (*outputs[:index], changed, *outputs[index + 1:])
    final, evidence, _ = verify_outputs(
        descriptor, run.inputs, run.assumptions, candidates, candidate.trace, checks, reference,
    )
    assert (final[index].status, evidence[index].status) == (status, evidence_status)
