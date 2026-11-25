"""Wire round trips for dated factor examples."""

from datetime import date, datetime
from decimal import Decimal

import pytest
from fixtures.factor_examples import EXAMPLES, UNKNOWN_DFII10_AVAILABILITY, build_run
from qopenbb_data.modeling.contracts import ModelRun


@pytest.mark.parametrize("model_id", [
    "etf_momentum", "etf_realized_volatility", "real_yield_regime",
    "issuer_fcf_yield", "proxy_comparison", "timing_study",
])
@pytest.mark.parametrize("missing", [False, True], ids=["valid", "missing-or-partial"])
def test_factor_example_round_trip(model_id, missing):
    example = EXAMPLES[model_id]
    run = build_run(example, missing)
    restored = ModelRun.model_validate_json(run.model_dump_json())
    assert restored == run
    assert restored.inputs.fingerprint() == run.inputs.fingerprint()
    assert restored.descriptor.fingerprint() == run.descriptor.fingerprint()
    assert restored.descriptor.model_id == model_id
    assert (restored.descriptor.method_version, restored.descriptor.rule_set_version,
            restored.descriptor.reference_version) == ("1", "1", "1")
    assert restored.descriptor.entity_types == (example.entity_type,)
    assert restored.inputs.provenance.origin == "user_supplied"
    assert restored.inputs.cutoff.session_timezone == "America/New_York"
    assert restored.inputs.cutoff.cutoff_at == restored.inputs.cutoff.decision_at
    assert restored.inputs.cutoff.decision_at < restored.inputs.cutoff.evaluated_at
    assert tuple(table.table_id for table in restored.inputs.tables) == restored.descriptor.input_ids
    for table in restored.inputs.tables:
        assert table.keys == ("entity_id", "metric_id", "observation_date", "vintage_at")
        assert all(restored.inputs.cutoff.is_eligible(row) for row in table.rows)
    assert {item.output_id for item in restored.outputs if item.status == "withheld"} == (
        set(example.withheld) if missing else set()
    )

    for output, expected, check in zip(restored.outputs, example.outputs, restored.checks, strict=True):
        assert (output.output_id, output.unit, output.value_type) == (
            expected.output_id, expected.unit, expected.value_type,
        )
        assert output.check_ids == (check.rule_id,)
        if output.status == "withheld":
            assert output.value is None
            assert output.reason == check.explanation == example.withheld[output.output_id]
            assert check.status == "fail"
            continue

        assert output.status == "unverified"
        assert check.status == "pass"
        entry, = (entry for entry in restored.trace if entry.output_id == output.output_id)
        assert output.trace_ids == (entry.trace_id,)
        assert entry.source_record_ids
        assert entry.assumption_ids
        if expected.absolute_tolerance is None:
            assert type(output.value) is str
            assert output.value == expected.value
            assert check.tolerance is None
        else:
            assert isinstance(output.value, Decimal)
            assert check.tolerance.unit == output.unit
            assert check.tolerance.absolute == Decimal(expected.absolute_tolerance)
            overrides = example.partial_values if missing else {}
            expected_value = Decimal(overrides.get(output.output_id, expected.value))
            assert abs(output.value - expected_value) <= check.tolerance.absolute


def test_pair_missing_right_close_preserves_both_left_results():
    run = build_run(EXAMPLES["proxy_comparison"], missing=True)
    assert {output.output_id: output.value for output in run.outputs} == {
        "left_momentum": Decimal(20), "right_momentum": None, "momentum_spread": None,
        "left_volatility": Decimal(40), "right_volatility": None, "volatility_spread": None,
    }
    sessions, left, right = run.inputs.tables
    assert (len(sessions.rows), len(left.rows), len(right.rows)) == (64, 64, 63)
    assert left.rows[-1].observation_date == date(2024, 4, 3)
    assert right.rows[-1].observation_date == date(2024, 4, 2)
    assert date(2024, 3, 29) not in {row.observation_date for row in sessions.rows}

    assumption_values = {item.assumption_id: item.value for item in run.assumptions.assumptions}
    assert assumption_values["schedule_revision"] == "fixture_us_listing.2024r1"
    assert assumption_values["leg_methods"] == "etf_momentum@1, etf_realized_volatility@1"


def test_fcf_trace_preserves_filing_period_and_currency_scale():
    run = build_run(EXAMPLES["issuer_fcf_yield"], missing=False)
    trace, = run.trace
    cash_flow, capex, market_value = trace.substitutions
    assert (cash_flow.period_start, cash_flow.period_end) == (date(2023, 1, 1), date(2023, 12, 31))
    assert capex.value == Decimal(-20)
    assert market_value.period_end == date(2024, 4, 3)
    assert all((item.currency, item.scale) == ("USD", 6) for item in trace.substitutions)
    assert {row.source_record_id for row in run.inputs.tables[0].rows} == {"synthetic_annual_filing_2023"}
    assert run.outputs[0].value == (cash_flow.value + capex.value) * 100 / market_value.value


def test_timing_groups_keep_ties_and_require_pre_return_decisions():
    valid = build_run(EXAMPLES["timing_study"], missing=False)
    partial = build_run(EXAMPLES["timing_study"], missing=True)
    rising, _, falling, _, drawdown = valid.outputs
    assert (rising.value, falling.value, drawdown.value) == (
        Decimal("0.3333333333333333333333333333"), Decimal("0.5"), Decimal("8.8"),
    )
    assert partial.outputs[0].value == Decimal("0.5")
    assert partial.outputs[1].status == "withheld"
    assert partial.outputs[-1].status == "unverified"
    assert partial.outputs[-1].value == Decimal("8.8")
    drawdown_trace, = (entry for entry in partial.trace if entry.output_id == "study_drawdown")
    assert all(record_id.startswith("fixture_left.") for record_id in drawdown_trace.source_record_ids)
    signals, regimes, returns = valid.inputs.tables
    proxy_returns = [row for row in returns.rows if row.entity_id == "fixture_left"]
    for signal, regime, outcome in zip(signals.rows, regimes.rows, proxy_returns, strict=True):
        return_start = datetime.fromisoformat(f"{outcome.context.period_start}T14:00:00+00:00")
        assert signal.published_at == regime.published_at < return_start


def test_volatility_trace_freezes_all_adjacent_simple_returns():
    run = build_run(EXAMPLES["etf_realized_volatility"], missing=False)
    restored = ModelRun.model_validate_json(run.model_dump_json())
    entry, = restored.trace
    closes = restored.inputs.tables[1].rows
    returns = [item for item in entry.intermediate_values if item.unit == "ratio"]
    assert len(returns) == 63
    assert [item.value for item in returns] == [Decimal("0.2")] + [Decimal(0)] * 62
    assert [(item.period_start, item.period_end) for item in returns] == list(
        zip((row.observation_date for row in closes[:-1]),
            (row.observation_date for row in closes[1:]), strict=True)
    )
    assert {item.name: item.value for item in entry.intermediate_values if item.unit == "count"} == {
        "return_count": 63, "sample_divisor": 62, "annualization_sessions": 252,
    }


def test_dfii10_unknown_historical_availability_withholds_both_outputs():
    run = build_run(UNKNOWN_DFII10_AVAILABILITY, missing=True)
    restored = ModelRun.model_validate_json(run.model_dump_json())
    assert restored == run
    first, last = restored.inputs.tables[1].rows
    assert (first.observation_date, last.observation_date) == (date(2024, 1, 2), date(2024, 4, 3))
    assert (first.value, last.value) == (Decimal("1.50"), Decimal("1.75"))
    assert last.context.vintage_coverage == "unknown"
    assert restored.inputs.cutoff.is_eligible(first)
    assert not restored.inputs.cutoff.is_eligible(last)
    assert {output.output_id: (output.status, output.value) for output in restored.outputs} == {
        "regime": ("withheld", None), "change": ("withheld", None),
    }
    reason = "Unknown historical availability for DFII10 endpoint on 2024-04-03"
    assert all(output.reason == reason for output in restored.outputs)
    assert all(check.status == "fail" and check.explanation == reason for check in restored.checks)
