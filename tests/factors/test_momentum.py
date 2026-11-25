"""ETF momentum calculations and frozen evidence."""

from dataclasses import replace
from decimal import Decimal, localcontext

import pytest
from fixtures.factor_examples import EXAMPLES, build_run
from fixtures.factor_inputs import END, START, prices, schedule
from qopenbb_data.modeling.models.factors.method_inputs import price_window
from qopenbb_data.modeling.models.factors.momentum import MomentumModel

EXAMPLE = EXAMPLES["etf_momentum"]


@pytest.fixture
def model():
    return MomentumModel()


def test_descriptor_matches_frozen_example(model):
    assert model.describe().model_dump(mode="json") == EXAMPLE.descriptor().model_dump(mode="json")


def test_varying_prices_match_frozen_result_and_trace(model):
    run = build_run(EXAMPLE, missing=False)

    result = model.calculate(run.inputs, run.assumptions)

    assert len(result.outputs) == 1
    assert result.outputs[0].output_id == "momentum"
    assert result.outputs[0].value == run.outputs[0].value
    assert tuple(entry.model_dump(mode="json") for entry in result.trace) == tuple(
        entry.model_dump(mode="json") for entry in run.trace
    )


@pytest.mark.parametrize(("first", "interior", "last", "expected"), [
    ("100", "100", "100", "0"),
    ("100", "150", "100", "0"),
    ("120", "150", "100", "-16.666666666666666666666666666666666667"),
    ("1", "2", "1.0000000000000000000000000000000000001", "0.00000000000000000000000000000000001"),
])
def test_endpoint_return_is_independent_of_interior_prices_and_ambient_precision(
    model, first, interior, last, expected
):
    run = build_run(EXAMPLE, missing=False)
    sessions, closes = run.inputs.tables
    values = (first, *((interior,) * (len(closes.rows) - 2)), last)
    rows = tuple(
        row.model_copy(update={"value": Decimal(value)})
        for row, value in zip(closes.rows, values, strict=True)
    )
    inputs = run.inputs.model_copy(
        update={"tables": (sessions, closes.model_copy(update={"rows": rows}))}
    )

    with localcontext(prec=6):
        result = model.calculate(inputs, run.assumptions)

    assert result.outputs[0].value == Decimal(expected)


def test_unrepresentable_return_is_withheld_with_endpoint_dates(model):
    closes = prices("closes", "fixture_left", "1", False)
    first = closes.rows[0].model_copy(update={"value": Decimal("1e-38")})
    closes = closes.model_copy(update={"rows": (first, *closes.rows[1:])})
    run = build_run(replace(EXAMPLE, tables=lambda _: (schedule(), closes)), missing=False)

    result = model.calculate(run.inputs, run.assumptions)

    assert result.outputs[0].value is None
    reason = result.outputs[0].reason
    assert str(START) in reason and str(END) in reason
    assert "exceeds financial decimal range" in reason
    assert result.trace == ()


def test_missing_close_preserves_dated_reason(model):
    run = build_run(EXAMPLE, missing=True)
    with pytest.raises(ValueError, match="2024-04-03") as error:
        price_window(run.inputs, run.assumptions, EXAMPLE.model_id)

    result = model.calculate(run.inputs, run.assumptions)

    assert len(result.outputs) == 1
    assert result.outputs[0].output_id == "momentum"
    assert result.outputs[0].value is None
    assert result.outputs[0].reason == str(error.value)
    assert result.trace == ()
