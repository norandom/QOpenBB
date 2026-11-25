"""Decision-time evidence, chronological exposures and timing-study coverage."""

from datetime import date, timedelta
from decimal import Decimal, Inexact, localcontext

import pytest
from fixtures.factor_examples import EXAMPLES, build_run
from fixtures.factor_inputs import STUDY_DATES, utc
from qopenbb_data.modeling.models.factors.study_groups import build_study_groups

JUN_3, JUN_4, JUN_5, JUN_6, JUN_7, JUN_10, JUN_11 = STUDY_DATES


@pytest.fixture
def run():
    return build_run(EXAMPLES["timing_study"], missing=False)


def _build(run, **rows_by_table):
    tables = tuple(type(table)(
        table_id=table.table_id, grain=table.grain, keys=(*table.keys, "published_at"),
        nullable=True, rows=rows_by_table.get(table.table_id, table.rows),
    ) for table in run.inputs.tables)
    inputs = run.inputs.model_copy(update={"tables": tables})
    return build_study_groups(inputs, run.assumptions)


def _row(row, suffix="", *, context=None, **update):
    return row.model_copy(update={
        "record_id": f"{row.record_id}{suffix}",
        "context": row.context.model_copy(update=context or {}),
        **update,
    })


def _group(study, regime):
    return next(group for group in study.groups if group.regime == regime)


def _exclusions(interval):
    return {exclusion.scope: exclusion for exclusion in interval.exclusions}


def test_joins_contiguous_session_intervals_and_coverage_in_date_order(run):
    study = _build(run, **{table.table_id: table.rows[::-1] for table in run.inputs.tables})

    assert (study.plan.start, study.plan.end, study.plan.universe, study.plan.benchmark) == (
        JUN_4, JUN_11, "fixture_left", "fixture_benchmark",
    )
    assert tuple((item.decision_date, item.start, item.end) for item in study.intervals) == (
        (JUN_3, JUN_4, JUN_5), (JUN_4, JUN_5, JUN_6), (JUN_5, JUN_6, JUN_7),
        (JUN_6, JUN_7, JUN_10), (JUN_7, JUN_10, JUN_11),
    )
    assert [item.strategy_return for item in study.intervals] == [10, 0, -5, -4, 12]
    assert [item.benchmark_relative_return for item in study.intervals] == [10, 0, -5, -4, 12]
    assert all(item.position == "long" and item.exclusions == () for item in study.intervals)
    rising, falling = _group(study, "rising"), _group(study, "falling")
    assert rising.partition == falling.partition == "out_of_sample"
    assert rising.intervals == study.intervals[:3]
    assert falling.intervals == study.intervals[3:]
    assert (rising.eligible_count, rising.excluded_count, falling.eligible_count) == (3, 0, 2)
    first = study.intervals[0]
    assert (first.signal_row.observation_date, first.regime_row.observation_date,
            first.asset_row.observation_date, first.benchmark_row.observation_date) == (
        JUN_3, JUN_3, JUN_5, JUN_5,
    )


def test_missing_schedule_withholds_before_selecting_rows(run):
    assumptions = run.assumptions.model_copy(update={"assumptions": tuple(
        item for item in run.assumptions.assumptions if item.assumption_id != "study_schedule"
    )})
    with pytest.raises(ValueError, match="study_schedule"):
        build_study_groups(run.inputs, assumptions)


@pytest.mark.parametrize("when", [
    utc(JUN_3, 22) + timedelta(seconds=1), utc(JUN_4, 14), utc(JUN_4, 15),
])
@pytest.mark.parametrize("timestamp", ["published_at", "vintage_at"])
def test_prior_decision_cutoff_excludes_late_signal_and_regime(run, when, timestamp):
    signals, regimes, _ = run.inputs.tables
    changes = {timestamp: when}
    study = _build(run, dated_signals=(_row(signals.rows[0], **changes), *signals.rows[1:]),
                   dated_regimes=(_row(regimes.rows[0], **changes), *regimes.rows[1:]))
    first = study.intervals[0]
    assert first.position is first.strategy_return is first.benchmark_relative_return is None
    assert first.regime is first.signal_row is first.regime_row is None
    assert {scope: item.code for scope, item in _exclusions(first).items()} == {
        "signal": "unavailable", "regime": "unavailable",
    }
    unknown = _group(study, None)
    assert unknown.excluded_count == 1
    assert unknown.exclusion_counts == {("signal", "unavailable"): 1, ("regime", "unavailable"): 1}
    assert study.intervals[1].strategy_return == 0


def test_selects_eligible_vintages_ignoring_estimates_and_late_revisions(run):
    signals, regimes, returns = run.inputs.tables
    signal = _row(signals.rows[0], ".at_decision", vintage_at=utc(JUN_3, 22),
                  published_at=utc(JUN_3, 22), value=Decimal(30))
    late = _row(signal, ".late", vintage_at=utc(JUN_4, 15))
    estimate = _row(signal, ".estimate", category="estimate", value=Decimal(-1),
                    published_at=utc(JUN_3, 22) - timedelta(minutes=1))
    unknown = _row(signal, ".unknown", context={"vintage_coverage": "unknown"},
                   value=Decimal(-1), published_at=utc(JUN_3, 22) - timedelta(minutes=2))
    regime = _row(regimes.rows[0], ".revised", vintage_at=utc(JUN_3, 22),
                  published_at=utc(JUN_3, 22), value=Decimal(0))
    asset = _row(returns.rows[0], ".revised", vintage_at=utc(JUN_11, 22), value=Decimal("7.5"))
    late_asset = _row(asset, ".late", vintage_at=utc(JUN_11, 23), value=Decimal(-80))
    study = _build(run, dated_signals=(*signals.rows, late, estimate, unknown, signal),
                   dated_regimes=(*regimes.rows, regime),
                   forward_returns=(*returns.rows, late_asset, asset))

    first = study.intervals[0]
    assert (first.signal_row, first.regime_row, first.asset_row) == (signal, regime, asset)
    assert first.regime == "flat"
    assert first.strategy_return == Decimal("7.5")
    assert _group(study, "flat").eligible_count == 1


@pytest.mark.parametrize(("scope", "table_index", "row_index"), [
    ("signal", 0, 0), ("regime", 1, 0), ("asset_return", 2, 0), ("benchmark_return", 2, 1),
])
def test_conflicting_values_at_latest_eligible_revision_are_excluded(run, scope, table_index, row_index):
    table = run.inputs.tables[table_index]
    original = _row(table.rows[row_index], vintage_at=table.rows[row_index].published_at)
    other = _row(original, ".conflict", published_at=original.published_at + timedelta(minutes=1),
                 value=Decimal(2))
    rows = (*table.rows[:row_index], original, *table.rows[row_index + 1:], other)
    first = _build(run, **{table.table_id: rows}).intervals[0]
    exclusion = _exclusions(first)[scope]
    assert exclusion.code == "conflict"
    assert set(exclusion.record_ids) == {original.record_id, other.record_id}
    if scope in ("regime", "benchmark_return"):
        assert first.strategy_return == 10
    else:
        assert first.strategy_return is None


@pytest.mark.parametrize(("scope", "table_index", "row_index", "context"), [
    ("signal", 0, 0, {"unit": "ratio"}),
    ("signal", 0, 0, {"basis": "unadjusted"}),
    ("regime", 1, 0, {"scale": 2}),
    ("regime", 1, 0, {"currency": "USD"}),
    ("asset_return", 2, 0, {"basis": "close_to_close"}),
    ("asset_return", 2, 0, {"scale": -2}),
    ("benchmark_return", 2, 1, {"unit": "ratio"}),
])
def test_incompatible_financial_context_is_excluded(run, scope, table_index, row_index, context):
    table = run.inputs.tables[table_index]
    rows = list(table.rows)
    rows[row_index] = _row(rows[row_index], context=context)
    first = _build(run, **{table.table_id: rows}).intervals[0]
    assert _exclusions(first)[scope].code == "invalid"


@pytest.mark.parametrize(("offset", "expected"), [(-1, None), (0, 10)])
def test_return_publication_can_begin_at_end_open(run, offset, expected):
    returns = run.inputs.tables[2].rows
    published = utc(JUN_5, 14) + timedelta(microseconds=offset)
    first = _build(run, forward_returns=(
        _row(returns[0], published_at=published), *returns[1:],
    )).intervals[0]
    assert first.strategy_return == expected
    if expected is None:
        assert first.asset_row is None
        assert _exclusions(first)["asset_return"].code == "unavailable"
    else:
        assert first.asset_row.published_at == published
        assert first.exclusions == ()


def test_global_evaluated_timestamp_caps_outcome_availability(run):
    cutoff = run.inputs.cutoff.model_copy(update={"evaluated_at": utc(JUN_11, 14)})
    inputs = run.inputs.model_copy(update={"cutoff": cutoff})
    study = build_study_groups(inputs, run.assumptions)
    assert study.intervals[-2].strategy_return == -4
    last = study.intervals[-1]
    assert last.position == "long" and last.strategy_return is None
    assert _exclusions(last)["asset_return"].code == "unavailable"


def test_cash_does_not_need_asset_and_benchmark_does_not_gate_path(run):
    signals, regimes, returns = (table.rows for table in run.inputs.tables)
    cash, negative = (_row(row, value=Decimal(value))
                      for row, value in zip(signals[:2], ("0", "-1"), strict=True))
    benchmark = _row(returns[1], value=Decimal(3))
    study = _build(run, dated_signals=(cash, negative, *signals[2:]),
                   dated_regimes=regimes[1:],
                   forward_returns=(benchmark, *returns[4:7], *returns[8:]))
    first, second, _, fourth, _ = study.intervals
    assert first.position == second.position == "cash"
    assert first.asset_row is second.asset_row is None
    assert first.strategy_return == second.strategy_return == 0
    assert first.benchmark_relative_return == -3
    assert first.regime is None and set(_exclusions(first)) == {"regime"}
    assert second.benchmark_relative_return is None
    assert set(_exclusions(second)) == {"benchmark_return"}
    assert fourth.position == "long" and fourth.strategy_return == -4
    assert fourth.benchmark_relative_return is None
    rising, falling = _group(study, "rising"), _group(study, "falling")
    assert rising.excluded_count == falling.excluded_count == 1
    assert rising.exclusion_counts == falling.exclusion_counts == {("benchmark_return", "missing"): 1}
    assert _group(study, None).exclusion_counts == {("regime", "missing"): 1}


def test_missing_midpath_return_leaves_a_dated_gap(run):
    returns = run.inputs.tables[2].rows
    study = _build(run, forward_returns=(*returns[:4], *returns[5:]))
    middle = study.intervals[2]
    assert (middle.start, middle.end, middle.position) == (JUN_6, JUN_7, "long")
    assert middle.strategy_return is None
    assert _exclusions(middle)["asset_return"].code == "missing"
    assert study.intervals[3].strategy_return == -4


@pytest.mark.parametrize(("period_start", "period_end", "observation_date", "affected"), [
    (JUN_3, JUN_5, JUN_5, (0,)),
    (JUN_4, JUN_6, JUN_6, (0, 1)),
    (JUN_7, date(2024, 6, 9), date(2024, 6, 9), (3,)),
    (None, JUN_5, JUN_5, (0,)),
    (JUN_5, JUN_5, JUN_5, (0,)),
    (JUN_4, JUN_5, JUN_6, (0, 1)),
])
def test_available_malformed_returns_invalidate_affected_path_intervals(
    run, period_start, period_end, observation_date, affected,
):
    returns = run.inputs.tables[2].rows
    malformed = _row(returns[0], ".malformed", observation_date=observation_date,
                     published_at=utc(JUN_11, 21), vintage_at=utc(JUN_11, 21),
                     context={"period_start": period_start, "period_end": period_end})
    study = _build(run, forward_returns=(*returns, malformed))
    assert tuple(index for index, item in enumerate(study.intervals)
                 if item.strategy_return is None) == affected
    assert all(_exclusions(study.intervals[index])["asset_return"].code == "invalid_interval"
               for index in affected)


@pytest.mark.parametrize("day_index", [0, -2])
def test_future_ending_revision_preserves_realized_returns(run, day_index):
    returns = run.inputs.tables[2].rows
    original = returns[day_index]
    future = _row(original, ".future", context={"period_end": JUN_11 + timedelta(days=1)},
                  published_at=utc(original.observation_date, 21), vintage_at=utc(JUN_11, 21))
    assert _build(run, forward_returns=(*returns, future)) == _build(run)


def test_bad_benchmark_interval_does_not_poison_asset_path(run):
    returns = run.inputs.tables[2].rows
    overlap = _row(returns[3], ".overlap", context={"period_start": JUN_4},
                   vintage_at=utc(JUN_6, 15))
    study = _build(run, forward_returns=(*returns, overlap))
    assert [item.strategy_return for item in study.intervals] == [10, 0, -5, -4, 12]
    assert [item.benchmark_relative_return for item in study.intervals] == [None, None, -5, -4, 12]
    for item in study.intervals[:2]:
        assert _exclusions(item)["benchmark_return"].record_ids == (overlap.record_id,)


def test_outside_universe_outside_path_and_late_malformed_returns_are_ignored(run):
    returns = run.inputs.tables[2].rows
    early = _row(returns[0], ".early", observation_date=JUN_4,
                 context={"period_start": JUN_3, "period_end": JUN_4})
    other = _row(returns[0], ".other", entity_id="different_asset", context={"period_start": JUN_3})
    wrong_metric = _row(returns[0], ".wrong", metric_id="irrelevant", context={"period_start": JUN_3})
    late = _row(returns[2], ".late", context={"period_start": JUN_4}, vintage_at=utc(JUN_11, 23))
    too_early = utc(JUN_6, 14) - timedelta(microseconds=1)
    premature = _row(returns[2], ".premature", context={"period_start": JUN_4},
                     published_at=too_early, vintage_at=too_early)
    assert _build(run, forward_returns=(*returns, early, other, wrong_metric, late, premature)) == _build(run)


def test_relative_returns_preserve_small_differences_under_ambient_decimal_context(run):
    returns = run.inputs.tables[2].rows
    asset = _row(returns[0], value=Decimal("10.000000000000000000000000000000000001"))
    benchmark = _row(returns[1], value=Decimal(10))
    with localcontext(prec=1, Emin=-1, Emax=1) as context:
        context.traps[Inexact] = True
        study = _build(run, forward_returns=(asset, benchmark, *returns[2:]))
    assert study.intervals[0].benchmark_relative_return == Decimal("1e-36")


def test_latest_eligible_revision_replaces_period_as_of_each_evaluation(run):
    returns = run.inputs.tables[2].rows
    original = returns[2]
    malformed = _row(original, ".malformed", context={"period_start": JUN_4},
                     published_at=utc(JUN_11, 15), vintage_at=utc(JUN_11, 15))
    corrected = _row(original, ".corrected", published_at=utc(JUN_11, 16),
                     vintage_at=utc(JUN_11, 16))
    malformed_again = _row(malformed, ".again", published_at=utc(JUN_11, 17),
                           vintage_at=utc(JUN_11, 17))
    evidence = (*returns, malformed_again, corrected, malformed)

    def evaluate(hour):
        cutoff = run.inputs.cutoff.model_copy(update={"evaluated_at": utc(JUN_11, hour)})
        inputs = run.inputs.model_copy(update={"cutoff": cutoff})
        return _build(run.model_copy(update={"inputs": inputs}), forward_returns=evidence)

    first = evaluate(14)
    assert [item.asset_row for item in first.intervals[:2]] == [returns[0], original]
    invalid = evaluate(15)
    assert [item.strategy_return for item in invalid.intervals[:2]] == [None, None]
    assert _exclusions(invalid.intervals[0])["asset_return"].record_ids == (malformed.record_id,)
    repaired = evaluate(16)
    assert [item.asset_row for item in repaired.intervals[:2]] == [returns[0], corrected]
    assert [item.strategy_return for item in repaired.intervals[:2]] == [10, 0]
    invalid_again = evaluate(17)
    assert [item.strategy_return for item in invalid_again.intervals[:2]] == [None, None]
    assert _exclusions(invalid_again.intervals[0])["asset_return"].record_ids == (
        malformed_again.record_id,
    )


def test_conflicting_periods_at_the_same_revision_stay_excluded(run):
    returns = run.inputs.tables[2].rows
    original = _row(returns[2], vintage_at=utc(JUN_6, 15))
    overlap = _row(original, ".overlap", context={"period_start": JUN_4},
                   published_at=utc(JUN_6, 16))
    study = _build(run, forward_returns=(*returns[:2], original, *returns[3:], overlap))
    assert [item.strategy_return for item in study.intervals] == [None, None, -5, -4, 12]
    assert all(_exclusions(item)["asset_return"].code == "invalid_interval"
               for item in study.intervals[:2])
