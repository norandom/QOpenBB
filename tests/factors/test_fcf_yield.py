"""Issuer FCF yield from dated filings and consolidated market value."""

from datetime import timedelta
from decimal import Decimal, localcontext

import pytest
from fixtures.factor_examples import EXAMPLES, build_run
from qopenbb_data.modeling.models.factors.fcf_yield import FcfYieldModel

EXAMPLE = EXAMPLES["issuer_fcf_yield"]


def calculate(run, *, flows=None, market=None):
    cash_table, equity_table = run.inputs.tables
    if flows is not None:
        cash_table = cash_table.model_copy(update={"rows": tuple(flows)})
    if market is not None:
        equity_table = equity_table.model_copy(update={"rows": tuple(market)})
    inputs = run.inputs.model_copy(update={"tables": (cash_table, equity_table)})
    return FcfYieldModel().calculate(inputs, run.assumptions)


def test_frozen_issuer_yield_descriptor_and_trace():
    run = build_run(EXAMPLE, False)
    assert FcfYieldModel().describe() == EXAMPLE.descriptor()
    with localcontext(prec=2, Emax=2):
        candidate = calculate(run)
    assert candidate.outputs[0].value == Decimal(5)
    assert candidate.trace == run.trace


@pytest.mark.parametrize(("ocf", "expected"), [("20", "0"), ("-60", "-10"), ("20.8", "0.1")])
def test_numerator_sign_and_percent_units(ocf, expected):
    run = build_run(EXAMPLE, False)
    cash, capex = run.inputs.tables[0].rows
    candidate = calculate(run, flows=(cash.model_copy(update={"value": Decimal(ocf)}), capex))
    assert candidate.outputs[0].value == Decimal(expected)


@pytest.mark.parametrize(("fields", "context"), [
    ({"value": Decimal(0)}, {}), ({"value": Decimal(-1)}, {}),
    ({"category": "estimate"}, {}), ({"published_at": None}, {}),
    ({}, {"vintage_coverage": "unknown"}), ({}, {"currency": "EUR"}),
    ({}, {"consolidation_scope": "share_class"}), ({}, {"scale": 3}),
    ({}, {"quantity": "flow"}), ({}, {"unit": "price"}),
    ({"entity_id": "another_issuer"}, {}), ({"metric_id": "enterprise_value"}, {}),
])
def test_bad_denominator_withholds_dated_yield(fields, context):
    run = build_run(EXAMPLE, False)
    row, = run.inputs.tables[1].rows
    changed = row.model_copy(update={**fields, "context": row.context.model_copy(update=context)})
    result = calculate(run, market=(changed,))
    output, = result.outputs
    assert output.value is None and str(run.inputs.cutoff.observation_date) in output.reason
    assert result.trace == ()


def test_missing_market_value_matches_frozen_reason():
    run = build_run(EXAMPLE, True)
    candidate = calculate(run)
    assert candidate.outputs[0].reason == EXAMPLE.withheld["fcf_yield"]


def test_only_eligible_same_day_market_value_enters_trace():
    run = build_run(EXAMPLE, False)
    row, = run.inputs.tables[1].rows
    late = row.model_copy(update={"record_id": "late", "vintage_at": run.inputs.cutoff.evaluated_at,
                                  "value": Decimal(400)})
    prior = row.model_copy(update={"record_id": "prior", "observation_date": row.observation_date - timedelta(days=1)})
    result = calculate(run, market=(late, row, prior))
    assert result.outputs[0].value == Decimal(5)
    assert result.trace == run.trace
    assert calculate(run, market=(late, prior)).outputs[0].value is None


def test_conflicting_same_revision_market_values_withhold():
    run = build_run(EXAMPLE, False)
    row, = run.inputs.tables[1].rows
    conflict = row.model_copy(update={"record_id": "conflict", "value": Decimal(400)})
    for pair in ((row, conflict), (conflict, row)):
        result = calculate(run, market=pair)
        assert result.outputs[0].value is None
        assert "conflict" in result.outputs[0].reason.lower()


def test_eligible_market_value_revision_supersedes_original():
    run = build_run(EXAMPLE, False)
    row, = run.inputs.tables[1].rows
    revision = row.model_copy(update={"record_id": "revised", "vintage_at": run.inputs.cutoff.decision_at,
                                       "value": Decimal(400)})
    for order in ((row, revision), (revision, row)):
        result = calculate(run, market=order)
        assert result.outputs[0].value == Decimal(10)
        assert result.trace[0].source_record_ids[-1] == revision.record_id
        assert row.record_id not in result.trace[0].source_record_ids


def test_positive_spending_convention_matches_cash_outflow_magnitude():
    run = build_run(EXAMPLE, False)
    cash, capex = run.inputs.tables[0].rows
    item, = run.assumptions.assumptions
    run = run.model_copy(update={"assumptions": run.assumptions.model_copy(update={
        "assumptions": (item.model_copy(update={"value": "spending_positive"}),)})})
    capex = capex.model_copy(update={"value": Decimal(20), "context": capex.context.model_copy(
        update={"basis": "spending_positive"})})
    assert calculate(run, flows=(cash, capex)).outputs[0].value == Decimal(5)


def test_large_cash_flows_preserve_small_positive_difference():
    run = build_run(EXAMPLE, False)
    cash, capex = run.inputs.tables[0].rows
    rows = (cash.model_copy(update={"value": Decimal("1." + "0" * 36 + "1")}),
            capex.model_copy(update={"value": Decimal(-1)}))
    with localcontext(prec=2):
        result = calculate(run, flows=rows)
    assert result.outputs[0].value == Decimal("1e-38")  # The result 1.25e-38 rounds at wire scale 38.


def test_unrepresentable_yield_is_withheld_with_date():
    run = build_run(EXAMPLE, False)
    row, = run.inputs.tables[1].rows
    result = calculate(run, market=(row.model_copy(update={"value": Decimal("1e-38")}),))
    assert result.outputs[0].value is None and str(row.observation_date) in result.outputs[0].reason
    assert result.trace == ()


def test_rolling_year_preserves_all_four_filing_pairs_and_the_denominator():
    from datetime import date

    run = build_run(EXAMPLE, False)
    cash, capex = run.inputs.tables[0].rows
    ends = [date(2022, 12, 31), date(2023, 3, 31), date(2023, 6, 30),
            date(2023, 9, 30), date(2023, 12, 31)]
    rows = []
    for i, end in enumerate(ends[1:]):
        for source, amount in ((cash, Decimal(11 + i)), (capex, Decimal(-3))):
            context = source.context.model_copy(update={
                "period_start": ends[i] + timedelta(days=1), "period_end": end, "frequency": "quarterly",
            })
            rows.append(source.model_copy(update={
                "record_id": f"{source.metric_id}.Q{i + 1}", "source_record_id": f"filing.Q{i + 1}",
                "observation_date": end, "value": amount, "context": context,
            }))
    candidate = calculate(run, flows=reversed(rows))
    assert candidate.outputs[0].value == Decimal("4.75")
    trace, = candidate.trace
    assert trace.source_record_ids[:-1] == tuple(row.record_id for row in rows)
    assert [v.value for v in trace.intermediate_values] == [Decimal(12), Decimal(38)]
    assert [v.period_start for v in trace.substitutions[:-1]] == [row.context.period_start for row in rows]


def test_same_day_row_must_measure_market_value_on_that_day():
    run = build_run(EXAMPLE, False)
    row, = run.inputs.tables[1].rows
    stale = row.model_copy(update={"context": row.context.model_copy(update={
        "period_end": row.observation_date - timedelta(days=1)})})
    result = calculate(run, market=(stale,))
    assert result.outputs[0].value is None and str(row.observation_date) in result.outputs[0].reason


def test_future_publication_cannot_be_substituted_for_missing_equity_value():
    run = build_run(EXAMPLE, False)
    row, = run.inputs.tables[1].rows
    next_day = row.model_copy(update={"published_at": run.inputs.cutoff.decision_at + timedelta(days=1)})
    result = calculate(run, market=(next_day,))
    assert result.outputs[0].value is None and str(row.observation_date) in result.outputs[0].reason
