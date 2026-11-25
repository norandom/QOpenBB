from datetime import date

import pytest
from fixtures.factor_examples import EXAMPLES, build_run
from qopenbb_data.modeling.models.factors.study_schedule import study_plan


@pytest.fixture
def run():
    return build_run(EXAMPLES["timing_study"], False)


def test_plan_keeps_decision_before_first_return_and_accepts_session_gaps(run):
    plan = study_plan(run.inputs, run.assumptions)
    assert plan.sessions[0].day == date(2024, 6, 3)
    assert plan.sessions[1].day == plan.start == date(2024, 6, 4)
    assert plan.sessions[-1].day == plan.end == date(2024, 6, 11)
    assert plan.sessions[0].decision_at < plan.sessions[1].opens_at
    assert (plan.universe, plan.benchmark, plan.partition) == (
        "fixture_left", "fixture_benchmark", "out_of_sample",
    )


@pytest.mark.parametrize(("key", "value"), [
    ("study_schedule", None), ("schedule_revision", None), ("benchmark", None),
    ("study_schedule", "2024-06-03T09:30/2024-06-03T16:00"),
    ("study_dates", "2024-06-03/2024-06-11"), ("study_dates", "2024-06-04/2024-06-09"),
    ("study_dates", "2024-06-11/2024-06-04"), ("position_rule", "unversioned"),
    ("partition", "pooled"), ("drawdown_basis", "unspecified"), ("horizon", "monthly"),
])
def test_undefined_configuration_fails_closed(run, key, value):
    assumptions = tuple(
        item.model_copy(update={"value": value}) if item.assumption_id == key else item
        for item in run.assumptions.assumptions if item.assumption_id != key or value is not None
    )
    with pytest.raises(ValueError):
        study_plan(run.inputs, run.assumptions.model_copy(update={"assumptions": assumptions}))


def test_assumptions_must_apply_by_first_decision(run):
    with pytest.raises(ValueError, match="effective"):
        study_plan(run.inputs, run.assumptions.model_copy(update={"effective_date": date(2024, 6, 4)}))


def test_split_schedule_matches_single_field_and_rejects_missing_chunk(run):
    schedule = next(item for item in run.assumptions.assumptions if item.assumption_id == "study_schedule")
    first, rest = schedule.value.split(";", 1)
    others = tuple(item for item in run.assumptions.assumptions if item != schedule)
    half = schedule.model_copy(update={"value": first})
    tail = schedule.model_copy(update={"assumption_id": "study_schedule.2", "value": rest})
    split = run.assumptions.model_copy(update={"assumptions": (*others, tail, half)})
    assert study_plan(run.inputs, split).sessions == study_plan(run.inputs, run.assumptions).sessions
    gap = tail.model_copy(update={"assumption_id": "study_schedule.3"})
    with pytest.raises(ValueError, match="numbered consecutively"):
        study_plan(run.inputs, split.model_copy(update={"assumptions": (*others, half, gap)}))
