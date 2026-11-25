"""DFII10 regime classification and point-in-time endpoint evidence."""

from datetime import timedelta
from decimal import Decimal, Inexact, localcontext

import pytest
from fixtures.factor_examples import EXAMPLES, UNKNOWN_DFII10_AVAILABILITY, build_run
from fixtures.factor_inputs import END, SESSIONS, START, utc
from qopenbb_data.modeling.models.factors.real_yield import RealYieldModel

EXAMPLE = EXAMPLES["real_yield_regime"]


@pytest.fixture
def run():
    return build_run(EXAMPLE, missing=False)


def calculate(run, *rows, reverse_calendar=False):
    sessions, yields = run.inputs.tables
    if reverse_calendar:
        sessions = sessions.model_copy(update={"rows": sessions.rows[::-1]})
    # Include publication time so tied vintage timestamps can carry distinct evidence.
    yields = type(yields)(table_id=yields.table_id, grain=yields.grain,
                         keys=(*yields.keys, "published_at"), nullable=True, rows=rows)
    inputs = run.inputs.model_copy(update={"tables": (sessions, yields)})
    return RealYieldModel().calculate(inputs, run.assumptions)


def test_descriptor_matches_frozen_example():
    assert RealYieldModel().describe() == EXAMPLE.descriptor()


def test_only_exact_endpoints_are_needed_and_match_frozen_trace(run):
    first, last = run.inputs.tables[1].rows
    result = calculate(run, last, first, reverse_calendar=True)
    assert [(item.output_id, item.value) for item in result.outputs] == [
        (item.output_id, item.value) for item in run.outputs
    ]
    assert result.trace == run.trace


@pytest.mark.parametrize("example", [EXAMPLE, UNKNOWN_DFII10_AVAILABILITY],
                         ids=["missing", "unknown"])
def test_frozen_withholding_reasons(example):
    run = build_run(example, missing=True)
    result = RealYieldModel().calculate(run.inputs, run.assumptions)
    assert {item.output_id: item.reason for item in result.outputs} == example.withheld
    assert all(item.value is None for item in result.outputs)
    assert result.trace == ()


@pytest.mark.parametrize(("first_value", "last_value", "regime", "change"), [
    ("-1.10", "-0.90", "rising", "0.20"),
    ("0", "-0.05", "falling", "-0.05"),
    ("-0.25", "-0.25", "flat", "0"),
    ("1", "1.0000000000000000000000000000000000001", "rising", "1e-37"),
])
def test_sign_and_percentage_points_ignore_ambient_context(
    run, first_value, last_value, regime, change
):
    first, last = run.inputs.tables[1].rows
    with localcontext(prec=1, Emin=-1, Emax=1) as ctx:
        ctx.traps[Inexact] = True
        result = calculate(run, first.model_copy(update={"value": Decimal(first_value)}),
                           last.model_copy(update={"value": Decimal(last_value)}))
    assert [item.value for item in result.outputs] == [regime, Decimal(change)]


def test_unrepresentable_change_withholds_classification_and_change(run):
    first, last = run.inputs.tables[1].rows
    result = calculate(run, first.model_copy(update={"value": Decimal("-9e37")}),
                       last.model_copy(update={"value": Decimal("9e37")}))
    regime, change = result.outputs
    assert regime.value is None and regime.reason == change.reason
    assert change.value is None
    assert str(START) in change.reason and str(END) in change.reason
    assert "financial decimal range" in change.reason
    assert not result.trace


def variant(row, suffix, *, context=None, **updates):
    return row.model_copy(update={
        "record_id": f"{row.record_id}.{suffix}",
        "context": row.context.model_copy(update=context or {}),
        **updates,
    })


def test_mixed_versions_preserve_newest_eligible_observation(run):
    first, last = run.inputs.tables[1].rows
    variants = (
        variant(last, "late", vintage_at=utc(END + timedelta(days=1), 15), value=Decimal(-5)),
        variant(last, "estimate", category="estimate", vintage_at=utc(END, 22)),
        variant(last, "unconfirmed", context={"vintage_coverage": None},
                vintage_at=utc(END, 22), published_at=utc(END, 20), value=Decimal(-7)),
        variant(last, "older", vintage_at=utc(END, 19), value=Decimal(-1)),
    )
    assert calculate(run, *variants, last, first) == calculate(run, first, last)


@pytest.mark.parametrize(("updates", "context", "reason"), [
    ({"published_at": utc(END, 23)}, {}, "after cutoff"),
    ({"published_at": None}, {}, "Unknown historical availability"),
    ({}, {"vintage_coverage": None}, "Unknown historical availability"),
    ({}, {"vintage_coverage": "unavailable"}, "Unknown historical availability"),
    ({"category": "estimate"}, {}, "only estimates"),
    ({"value": None}, {}, "finite"),
    ({}, {"unit": "ratio"}, "percent"),
    ({}, {"quantity": "stock"}, "rate"),
    ({}, {"currency": "USD"}, "currency"),
    ({}, {"scale": 2}, "scale"),
    ({}, {"basis": "other"}, "treasury_constant_maturity"),
])
def test_invalid_endpoint_withholds_both_outputs(run, updates, context, reason):
    first, last = run.inputs.tables[1].rows
    result = calculate(run, first, variant(last, "invalid", context=context, **updates))
    assert [item.output_id for item in result.outputs] == ["regime", "change"]
    assert all(item.value is None and str(END) in item.reason and reason.lower() in item.reason.lower()
               for item in result.outputs)
    assert result.trace == ()


def test_nearby_and_unrelated_rows_cannot_replace_missing_start(run):
    first, last = run.inputs.tables[1].rows
    result = calculate(run, last, variant(first, "interior", observation_date=SESSIONS[1]),
                       variant(first, "another_series", entity_id="DGS10"),
                       variant(first, "another_metric", metric_id="endpoint_change"))
    assert all(item.value is None and str(START) in item.reason for item in result.outputs)


def test_equal_revision_duplicates_are_deterministic_and_conflicts_are_withheld(run):
    first, last = run.inputs.tables[1].rows
    same = variant(last, "duplicate", published_at=utc(END, 20))
    bad = variant(last, "conflict", published_at=utc(END, 20), value=Decimal(3))
    assert calculate(run, last, same, first) == calculate(run, first, same, last)
    result = calculate(run, last, bad, first)
    assert all(item.value is None and str(END) in item.reason and "conflicting" in item.reason.lower()
               for item in result.outputs)
    assert result.trace == ()


def test_single_day_measurement_preserves_both_dates(run):
    first, last = run.inputs.tables[1].rows
    last = variant(last, "dated_level", context={"period_start": END, "period_end": END})
    result = calculate(run, first, last)
    assert result.outputs[0].value == "rising"
    value = result.trace[0].substitutions[-1]
    assert value.period_start == value.period_end == END
