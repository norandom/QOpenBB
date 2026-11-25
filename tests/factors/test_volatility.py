"""Acceptance tests for the 63-session ETF realized-volatility method."""

from decimal import Decimal, localcontext
from itertools import pairwise

import pytest
from fixtures.factor_examples import EXAMPLES, build_run
from qopenbb_data.modeling.models.factors.method_inputs import price_window
from qopenbb_data.modeling.models.factors.volatility import VolatilityModel

EXAMPLE = EXAMPLES["etf_realized_volatility"]


def test_descriptor_matches_frozen_contract():
    assert VolatilityModel().describe() == EXAMPLE.descriptor()


def test_varying_prices_match_frozen_trace_and_sample_volatility():
    run = build_run(EXAMPLE, missing=False)

    with localcontext() as context:
        context.prec = 6
        candidate = VolatilityModel().calculate(run.inputs, run.assumptions)
        assert context.prec == 6

    output, = candidate.outputs
    expected, = EXAMPLE.outputs
    assert output.output_id == expected.output_id
    assert abs(output.value - Decimal(expected.value)) <= Decimal(expected.absolute_tolerance)
    assert candidate.trace == run.trace


def test_flat_prices_produce_zero_volatility():
    run = build_run(EXAMPLE, missing=False)
    sessions, closes = run.inputs.tables
    flat_closes = closes.model_copy(update={
        "rows": tuple(row.model_copy(update={"value": Decimal(100)}) for row in closes.rows),
    })
    inputs = run.inputs.model_copy(update={"tables": (sessions, flat_closes)})

    candidate = VolatilityModel().calculate(inputs, run.assumptions)

    output, = candidate.outputs
    trace, = candidate.trace
    assert output.value == Decimal(0)
    assert len(trace.intermediate_values) == 66
    assert all(item.value == Decimal(0) for item in trace.intermediate_values[:63])


def test_identical_repeating_returns_produce_zero_volatility():
    run = build_run(EXAMPLE, missing=False)
    sessions, closes = run.inputs.tables
    rows = tuple(
        type(row).model_validate({**row.model_dump(), "value": Decimal(3 ** (63 - index))})
        for index, row in enumerate(closes.rows)
    )
    inputs = run.inputs.model_copy(update={
        "tables": (sessions, closes.model_copy(update={"rows": rows})),
    })

    candidate = VolatilityModel().calculate(inputs, run.assumptions)

    output, = candidate.outputs
    assert output.value == Decimal(0)
    assert output.reason is None
    trace, = candidate.trace
    dated_returns = trace.intermediate_values[:-3]
    assert len(dated_returns) == 63
    expected_return = Decimal("-0." + "6" * 37 + "7")
    for item, (previous, current) in zip(dated_returns, pairwise(rows), strict=True):
        assert item.name == f"simple_return.{current.observation_date}"
        assert item.value == expected_return
        assert (item.period_start, item.period_end) == (previous.observation_date, current.observation_date)


def test_missing_close_preserves_dated_precondition_failure():
    run = build_run(EXAMPLE, missing=True)

    candidate = VolatilityModel().calculate(run.inputs, run.assumptions)

    output, = candidate.outputs
    assert output.output_id == EXAMPLE.outputs[0].output_id
    assert output.value is None
    with pytest.raises(ValueError, match=r"2024-04-03 missing close") as failure:
        price_window(run.inputs, run.assumptions, EXAMPLE.model_id)
    assert output.reason == str(failure.value)
    assert candidate.trace == ()


@pytest.mark.parametrize(
    ("first", "subsequent", "field"),
    [
        ("0.01", "1E+37", "simple return"),
        ("1", "9E+37", "annualized volatility"),
    ],
    ids=["return-overflow", "volatility-overflow"],
)
def test_out_of_range_calculation_is_withheld(first, subsequent, field):
    run = build_run(EXAMPLE, missing=False)
    sessions, closes = run.inputs.tables
    rows = tuple(
        type(row).model_validate({
            **row.model_dump(), "value": Decimal(first if index == 0 else subsequent),
        })
        for index, row in enumerate(closes.rows)
    )
    inputs = run.inputs.model_copy(update={
        "tables": (sessions, closes.model_copy(update={"rows": rows})),
    })

    candidate = VolatilityModel().calculate(inputs, run.assumptions)

    output, = candidate.outputs
    assert output.value is None
    assert candidate.trace == ()
    expected_date = rows[1 if field == "simple return" else -1].observation_date
    assert f"{expected_date} {field}" in output.reason
    assert "financial decimal range" in output.reason


def test_nonzero_volatility_below_contract_magnitude_is_withheld():
    run = build_run(EXAMPLE, missing=False)
    sessions, closes = run.inputs.tables
    # Equal price increments give slightly decreasing simple returns as their denominators rise.
    rows = tuple(
        type(row).model_validate({**row.model_dump(), "value": f"1.{index:037d}"})
        for index, row in enumerate(closes.rows)
    )
    inputs = run.inputs.model_copy(update={
        "tables": (sessions, closes.model_copy(update={"rows": rows})),
    })

    candidate = VolatilityModel().calculate(inputs, run.assumptions)

    output, = candidate.outputs
    assert output.value is None
    assert candidate.trace == ()
    assert f"{rows[-1].observation_date} annualized volatility" in output.reason
    assert "financial decimal range" in output.reason
