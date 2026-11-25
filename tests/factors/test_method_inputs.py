"""Integration of the frozen snapshots with the factor methods' input selection."""

import pytest
from fixtures.factor_examples import EXAMPLES, build_run
from pydantic import ValidationError
from qopenbb_data.modeling.models.factors.method_inputs import price_window
from qopenbb_data.modeling.models.protocol import CandidateOutput


@pytest.mark.parametrize("case", ["schema", "cutoff", "basis", "effective_date", "ambiguous_proxy"])
def test_invalid_calculation_context_fails_explicitly(case):
    run = build_run(EXAMPLES["etf_momentum"], False)
    inputs, assumptions = run.inputs, run.assumptions
    if case == "schema":
        inputs = inputs.model_copy(update={"schema_id": "other.inputs"})
    elif case == "cutoff":
        inputs = inputs.model_copy(update={"cutoff": None})
    elif case == "basis":
        assumptions = assumptions.model_copy(update={"assumptions": assumptions.assumptions[:1]})
    elif case == "effective_date":
        assumptions = assumptions.model_copy(update={"effective_date": inputs.cutoff.evaluated_at.date()})
    else:
        sessions, prices = inputs.tables
        other = prices.rows[0].model_copy(update={"entity_id": "other_etf", "record_id": "other"})
        inputs = inputs.model_copy(update={"tables": (sessions, prices.model_copy(
            update={"rows": (*prices.rows, other)}))})
    with pytest.raises(ValueError, match="schema|cutoff|price_basis|effective|one entity"):
        price_window(inputs, assumptions, "etf_momentum")


def test_only_withheld_candidate_can_carry_a_reason():
    with pytest.raises(ValidationError, match="missing candidate value"):
        CandidateOutput(output_id="momentum", value="1", reason="missing close")
    missing = CandidateOutput(output_id="momentum", value=None, reason="missing close")
    assert CandidateOutput.model_validate_json(missing.model_dump_json()) == missing


def test_result_decimal_rounds_at_the_wire_boundary():
    from decimal import Decimal

    from qopenbb_data.modeling.models.factors.method_inputs import result_decimal

    assert result_decimal(Decimal("0." + "3" * 60)) == Decimal("0." + "3" * 38)
    assert result_decimal(Decimal("1e-38")) == Decimal("1e-38")
    for value in ("1e-39", "1e38", "9" * 38 + ".9"):
        with pytest.raises(ValueError, match="decimal range"):
            result_decimal(Decimal(value))


def test_trace_preserves_supplied_measurement_period():
    from datetime import timedelta

    from qopenbb_data.modeling.models.factors.method_inputs import substitution

    run = build_run(EXAMPLES["etf_momentum"], False)
    row = run.inputs.tables[1].rows[-1]
    start = row.observation_date - timedelta(days=2)
    end = row.observation_date - timedelta(days=1)
    context = row.context.model_copy(update={"period_start": start, "period_end": end})
    value = substitution(row.model_copy(update={"context": context}))
    assert (value.period_start, value.period_end) == (start, end)
