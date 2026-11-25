"""Timing reference evidence through the foundation and independently dated snapshots."""

from datetime import date, timedelta
from decimal import Decimal

import pytest
from fixtures.factor_examples import EXAMPLES, build_run
from qopenbb_data.modeling.contracts import CheckOutcome
from qopenbb_data.modeling.models.factors.diagnostics import TimingStudyModel
from qopenbb_data.modeling.validation.outputs import resolve_outputs
from qopenbb_data.modeling.validation.rules import Rule, RuleContext, evaluate_stage
from qopenbb_data.modeling.verification.factors.timing_reference import (
    rebuild_timing,
    timing_reference,
)
from qopenbb_data.modeling.verification.reference import verify_outputs

EXAMPLE = EXAMPLES["timing_study"]


def update_rows(run, index, rows):
    tables = list(run.inputs.tables)
    tables[index] = tables[index].model_copy(update={"rows": tuple(rows)})
    return run.model_copy(update={"inputs": run.inputs.model_copy(update={"tables": tuple(tables)})})


def availability_rule(definition):
    rule_id, = definition.required_check_ids

    def evaluate(context):
        candidate = TimingStudyModel().calculate(context.inputs, context.assumptions)
        result = next(item for item in candidate.outputs if item.output_id == definition.output_id)
        return CheckOutcome(
            rule_id=rule_id, rule_version="1", severity="blocking",
            status="pass" if result.value is not None else "fail", explanation=result.reason,
            observed="defined" if result.value is not None else "undefined", expected="defined",
            input_ids=definition.required_input_ids, output_ids=(definition.output_id,),
        )

    return Rule(rule_id, definition.required_input_ids, (definition.output_id,), evaluate)


def compare(run, mutant=None):
    model = TimingStudyModel()
    descriptor = model.describe()
    bindings = tuple(availability_rule(definition) for definition in descriptor.outputs)
    checks = evaluate_stage(descriptor, bindings, "precondition", RuleContext(run.inputs, run.assumptions))
    candidate = model.calculate(run.inputs, run.assumptions)
    reference = timing_reference()
    table_ids = {table.table_id for table in run.inputs.tables}
    for definition, check in zip(descriptor.outputs, checks, strict=True):
        expected = reference.calculations[definition.output_id](run.inputs, run.assumptions)
        if set(definition.required_input_ids) - table_ids:
            assert check.status == "unknown"
        else:
            assert check.status == ("pass" if expected is not None else "fail")
    if mutant:
        candidate = candidate.model_copy(update={"outputs": tuple(
            item.model_copy(update={"value": mutant[item.output_id]}) if item.output_id in mutant else item
            for item in candidate.outputs
        )})
    outputs = resolve_outputs(descriptor, candidate, checks, inputs=run.inputs)
    final, evidence, _ = verify_outputs(
        descriptor, run.inputs, run.assumptions, outputs, candidate.trace, checks, reference,
    )
    return {result.output_id: (result.status, proof.status, check.status)
            for result, proof, check in zip(final, evidence, checks, strict=True)}


def raw(run):
    study = rebuild_timing(run.inputs, run.assumptions)
    assert study is not None
    return study


@pytest.mark.parametrize(("mutant", "value"), [
    ("rising_hit_rate", "0.4"),  # Pooled regimes: two winners in five outcomes.
    ("rising_hit_rate", "0.5"),  # Dropped tie: one winner in two nonzero outcomes.
    ("falling_slugging", str(Decimal(11) / Decimal("4.5"))),  # Pooled mean win / mean loss.
])
def test_foundation_rejects_score_mutations(mutant, value):
    run = build_run(EXAMPLE, False)
    assert set(compare(run).values()) == {("verified", "match", "pass")}
    results = compare(run, {mutant: Decimal(value)})
    assert results.pop(mutant) == ("withheld", "mismatch", "pass")
    assert set(results.values()) == {("verified", "match", "pass")}


def test_missing_benchmark_preserves_wealth_and_withholds_undefined_slugging():
    run = build_run(EXAMPLE, True)
    study = raw(run)
    assert study.partition == "out_of_sample"
    rising = study.groups["rising"]
    assert (rising.eligible_count, rising.excluded_count, rising.ties) == (2, 1, 1)
    assert study.values["rising_slugging"] is None
    assert study.values["study_drawdown"] == Decimal("8.8")
    assert compare(run)["rising_slugging"] == ("withheld", "unavailable", "fail")


@pytest.mark.parametrize("minutes", [0, 1])
def test_signal_at_or_after_return_open_is_excluded(minutes):
    run = build_run(EXAMPLE, False)
    first, *rest = run.inputs.tables[0].rows
    start = run.inputs.tables[2].rows[0].context.period_start
    late = first.model_copy(update={"published_at": first.published_at.replace(
        year=start.year, month=start.month, day=start.day, hour=14,
    ) + timedelta(minutes=minutes)})
    run = update_rows(run, 0, (late, *rest))
    study = raw(run)
    assert (study.groups["rising"].eligible_count, study.groups["rising"].ties) == (2, 1)
    assert study.intervals[0].exclusions == (("signal", "unavailable"),)
    assert study.values["study_drawdown"] is None
    results = compare(run, {"rising_hit_rate": Decimal(1) / 3})
    assert results["rising_hit_rate"] == ("withheld", "mismatch", "pass")
    assert results["study_drawdown"] == ("withheld", "unavailable", "fail")


def test_latest_known_correction_to_interval_invalidates_overlapping_exposures():
    run = build_run(EXAMPLE, False)
    rows = run.inputs.tables[2].rows
    revised = rows[2]
    revised = revised.model_copy(update={
        "record_id": "corrected_span", "vintage_at": revised.published_at + timedelta(hours=1),
        "context": revised.context.model_copy(update={"period_start": rows[0].context.period_start}),
    })
    run = update_rows(run, 2, (*reversed(rows), revised))
    study = raw(run)
    assert [item.strategy for item in study.intervals[:2]] == [None, None]
    assert all(("asset_return", "invalid_interval") in item.exclusions for item in study.intervals[:2])
    assert study.values["study_drawdown"] is None
    assert compare(run)["study_drawdown"] == ("withheld", "unavailable", "fail")


def test_cash_uses_zero_strategy_return_even_without_asset_and_regime():
    run = build_run(EXAMPLE, False)
    signal, *rest = run.inputs.tables[0].rows
    run = update_rows(run, 0, (signal.model_copy(update={"value": Decimal(0)}), *rest))
    run = update_rows(run, 1, run.inputs.tables[1].rows[1:])
    run = update_rows(run, 2, run.inputs.tables[2].rows[1:])
    study = raw(run)
    assert study.intervals[0].position == "cash"
    assert study.groups[None].excluded_count == 1
    assert study.values["study_drawdown"] == Decimal("8.8")
    assert compare(run)["study_drawdown"] == ("verified", "match", "pass")

def test_absent_required_table_is_unknown_but_drawdown_can_verify():
    run = build_run(EXAMPLE, False)
    signals, _, returns = run.inputs.tables
    run = run.model_copy(update={"inputs": run.inputs.model_copy(update={"tables": (signals, returns)})})
    study = raw(run)
    assert all(value is None for key, value in study.values.items() if key != "study_drawdown")
    results = compare(run)
    assert results.pop("study_drawdown") == ("verified", "match", "pass")
    assert set(results.values()) == {("withheld", "unavailable", "unknown")}


def test_present_table_without_benchmark_fails_scores_but_preserves_drawdown():
    run = build_run(EXAMPLE, False)
    run = update_rows(run, 2, [row for row in run.inputs.tables[2].rows if row.entity_id == "fixture_left"])
    study = raw(run)
    assert study.groups["rising"].eligible_count == 0
    assert all(value is None for key, value in study.values.items() if key != "study_drawdown")
    results = compare(run)
    assert results.pop("study_drawdown") == ("verified", "match", "pass")
    assert set(results.values()) == {("withheld", "unavailable", "fail")}


def change_assumption(run, key, value):
    assumptions = tuple(
        item.model_copy(update={"value": value}) if item.assumption_id == key else item
        for item in run.assumptions.assumptions
    )
    return run.model_copy(update={"assumptions": run.assumptions.model_copy(update={"assumptions": assumptions})})


@pytest.mark.parametrize(("key", "value"), [
    ("position_rule", "always_long"), ("horizon", "two_sessions"),
    ("benchmark", ""), ("partition", "pooled"), ("drawdown_basis", "regime_only"),
    ("study_dates", "2024-06-03/2024-06-11"), ("study_schedule", "2024-06-03T14:00/2024-06-03T22:00"),
])
def test_unsupported_assumptions_withhold_reference(key, value):
    run = change_assumption(build_run(EXAMPLE, False), key, value)
    assert rebuild_timing(run.inputs, run.assumptions) is None
    assert all(callback(run.inputs, run.assumptions) is None
               for callback in timing_reference().calculations.values())


@pytest.mark.parametrize("case", ["evaluation", "version", "effective_date"])
def test_historical_cutoff_and_versions_gate_the_path(case):
    run = build_run(EXAMPLE, False)
    if case == "evaluation":
        cutoff = run.inputs.cutoff
        cutoff = cutoff.model_copy(update={"evaluated_at": cutoff.decision_at - timedelta(hours=9)})
        run = run.model_copy(update={"inputs": run.inputs.model_copy(update={"cutoff": cutoff})})
        assert set(compare(run).values()) == {("withheld", "unavailable", "fail")}
    else:
        updates = {"version": "2"} if case == "version" else {"effective_date": run.inputs.cutoff.observation_date}
        run = run.model_copy(update={"assumptions": run.assumptions.model_copy(update=updates)})
    assert rebuild_timing(run.inputs, run.assumptions) is None


@pytest.mark.parametrize("case", ["late_vintage", "unknown", "before_ending_open"])
def test_unrealized_or_unavailable_return_revisions_cannot_override_an_observed_return(case):
    run = build_run(EXAMPLE, False)
    original, *others = run.inputs.tables[2].rows
    changed = {"record_id": "excluded_revision", "value": Decimal(-99)}
    if case == "late_vintage":
        changed["vintage_at"] = run.inputs.cutoff.decision_at + timedelta(seconds=1)
    elif case == "unknown":
        changed["vintage_at"] = original.published_at + timedelta(minutes=1)
        changed["context"] = original.context.model_copy(update={"vintage_coverage": "unknown"})
    else:
        changed["vintage_at"] = original.published_at + timedelta(minutes=1)
        changed["published_at"] = original.published_at - timedelta(hours=2)
    run = update_rows(run, 2, (original.model_copy(update=changed), *others, original))
    study = raw(run)
    assert study.intervals[0].strategy == Decimal(10)
    assert study.values["study_drawdown"] == Decimal("8.8")
    assert set(compare(run).values()) == {("verified", "match", "pass")}


@pytest.mark.parametrize("output_id", ["rising_slugging", "study_drawdown"])
def test_frozen_tolerance_boundary(output_id):
    run = build_run(EXAMPLE, False)
    output = next(item for item in EXAMPLE.outputs if item.output_id == output_id)
    limit = Decimal(output.absolute_tolerance)
    baseline = Decimal(output.value)
    assert compare(run, {output_id: baseline + limit})[output_id] == ("verified", "match", "pass")
    assert compare(run, {output_id: baseline + limit * Decimal("1.01")})[output_id] == (
        "withheld", "mismatch", "pass",
    )


def test_decision_revision_changes_exposure_only_when_available_at_decision():
    run = build_run(EXAMPLE, False)
    original, *others = run.inputs.tables[0].rows
    revision = original.model_copy(update={
        "record_id": "cash_revision", "vintage_at": original.published_at + timedelta(hours=1),
        "value": Decimal(-1),
    })
    later = revision.model_copy(update={
        "record_id": "late_long_revision", "vintage_at": revision.vintage_at + timedelta(seconds=1),
        "value": Decimal(1),
    })
    run = change_assumption(update_rows(run, 0, (later, *others, revision, original)), "partition", "in_sample")
    study = raw(run)
    assert study.partition == "in_sample"
    assert study.intervals[0].position == "cash"
    assert study.intervals[0].relative == 0
    assert study.groups["rising"].ties == 2
    assert compare(run)["rising_slugging"] == ("withheld", "unavailable", "fail")


@pytest.mark.parametrize("loss", [Decimal(-100), Decimal("-1E-38")])
def test_drawdown_extremes_are_defined_at_wire_limits(loss):
    run = build_run(EXAMPLE, False)
    rows = run.inputs.tables[2].rows
    updated = [
        item.model_copy(update={"value": loss if index == 2 else Decimal(10)})
        if item.entity_id == "fixture_left" else item
        for index, item in enumerate(rows)
    ]
    run = update_rows(run, 2, updated)
    assert raw(run).values["study_drawdown"] == loss.copy_abs()
    assert compare(run)["study_drawdown"] == ("verified", "match", "pass")


@pytest.mark.parametrize("claimed_end", [date(2024, 6, 8), date(2024, 6, 11), date(2024, 6, 12)])
def test_correction_claiming_an_unrealized_end_cannot_poison_the_baseline(claimed_end):
    run = build_run(EXAMPLE, False)
    rows = run.inputs.tables[2].rows
    original = rows[0]
    revision = original.model_copy(update={
        "record_id": "future_span_correction",
        "vintage_at": original.published_at + timedelta(hours=1),
        "context": original.context.model_copy(update={
            "period_end": claimed_end,
        }),
    })
    revision = type(original).model_validate(revision.model_dump())
    revised_run = update_rows(run, 2, (*rows, revision))
    baseline = {expected.output_id: Decimal(expected.value) for expected in EXAMPLE.outputs}
    baseline["rising_hit_rate"] = Decimal("0." + "3" * 38)
    assert raw(run).values == baseline
    rebuilt = raw(revised_run)
    assert rebuilt.values == baseline
    assert set(compare(revised_run).values()) == {("verified", "match", "pass")}


@pytest.mark.parametrize("minutes_from_open", [-1, 0, 1])
def test_known_open_after_study_end_controls_revision_eligibility(minutes_from_open):
    run = change_assumption(build_run(EXAMPLE, False), "study_dates", "2024-06-04/2024-06-10")
    baseline = raw(run)
    baseline_results = compare(run)
    assert baseline.values["study_drawdown"] == Decimal("8.8")
    assert baseline_results["study_drawdown"] == ("verified", "match", "pass")

    rows = run.inputs.tables[2].rows
    original = rows[0]
    end = date(2024, 6, 11)
    publication = run.inputs.cutoff.decision_at.replace(hour=14) + timedelta(minutes=minutes_from_open)
    revision = type(original).model_validate(original.model_dump() | {
        "record_id": "out_of_window_revision",
        "published_at": publication,
        "vintage_at": publication,
        "context": original.context.model_dump() | {"period_end": end},
    })
    revised_run = update_rows(run, 2, (*rows, revision))
    rebuilt = raw(revised_run)
    assert rebuilt.intervals[-1].end == date(2024, 6, 10)
    if minutes_from_open < 0:
        assert rebuilt.values == baseline.values
        assert compare(revised_run) == baseline_results
    else:
        assert all(("asset_return", "invalid_interval") in item.exclusions for item in rebuilt.intervals)
        assert all(value is None for value in rebuilt.values.values())
        assert set(compare(revised_run).values()) == {("withheld", "unavailable", "fail")}
