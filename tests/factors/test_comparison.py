"""Ordered proxy comparison and point-in-time leg evidence."""

from datetime import timedelta
from decimal import Decimal, localcontext

import pytest
from fixtures.factor_examples import EXAMPLES, build_run, text_assumption
from fixtures.factor_inputs import END, SESSIONS, START, utc
from qopenbb_data.modeling.contracts import Assumption, InputSnapshot
from qopenbb_data.modeling.models.factors.comparison import ProxyComparisonModel
from qopenbb_data.modeling.models.factors.momentum import MomentumModel

EXAMPLE = EXAMPLES["proxy_comparison"]
OUTPUT_IDS = tuple(item.output_id for item in EXAMPLE.outputs)
SPREADS = ("momentum_spread", "volatility_spread")


@pytest.fixture
def model():
    return ProxyComparisonModel()


@pytest.fixture
def run():
    return build_run(EXAMPLE, missing=False)


def _assumptions(run, **updates):
    existing = {item.assumption_id: item for item in run.assumptions.assumptions}
    for key, value in updates.items():
        if value is None:
            del existing[key]
        elif isinstance(value, Assumption):
            existing[key] = value
        else:
            existing[key] = text_assumption(key, value, "Synthetic comparison binding")
    return run.assumptions.model_copy(update={"assumptions": tuple(existing.values())})


def _inputs(run, *tables):
    return InputSnapshot(**(run.inputs.model_dump() | {"tables": tables}))


def _rows(table, rows):
    return table.model_copy(update={"rows": tuple(rows)})


def _values(result):
    return tuple(item.value for item in result.outputs)


def _outputs(result):
    return {item.output_id: item for item in result.outputs}


def _traces(result):
    return {entry.output_id: entry for entry in result.trace}


def test_descriptor_matches_frozen_example(model):
    assert model.describe() == EXAMPLE.descriptor()


def test_ordered_comparison_and_reversed_pair(model, run):
    result = model.calculate(run.inputs, run.assumptions)
    assert tuple(item.output_id for item in result.outputs) == OUTPUT_IDS
    assert _values(result) == tuple(Decimal(expected.value) for expected in EXAMPLE.outputs)
    assert tuple(entry.output_id for entry in result.trace) == OUTPUT_IDS

    sessions, left, right = run.inputs.tables
    reversed_inputs = _inputs(run, sessions, right.model_copy(update={"table_id": "left_closes"}),
                              left.model_copy(update={"table_id": "right_closes"}))
    reversed_pair = _assumptions(run, left_proxy="fixture_right", right_proxy="fixture_left")
    reversed_result = model.calculate(reversed_inputs, reversed_pair)
    assert _values(reversed_result) == tuple(map(Decimal, (10, 20, -10, 20, 40, -20)))
    assert _traces(reversed_result)["left_momentum"].substitutions[0].name == right.rows[0].record_id


def test_trace_names_selected_schedule_and_price_revisions(model, run):
    sessions, left, right = run.inputs.tables
    changed_session = sessions.rows[-1].model_copy(update={
        "record_id": "selected_session_revision", "vintage_at": utc(END, 18),
        "published_at": utc(END, 18),
    })
    selected = right.rows[-1].model_copy(update={
        "record_id": "selected_price_revision", "vintage_at": utc(END, 22),
        "published_at": utc(END, 22), "value": Decimal(115),
    })
    late = selected.model_copy(update={
        "record_id": "late_price_revision", "vintage_at": utc(END, 23),
        "published_at": utc(END, 23), "value": Decimal(140),
    })
    inputs = _inputs(run, _rows(sessions, (changed_session, *reversed(sessions.rows))),
                     left, _rows(right, (late, *reversed(right.rows), selected)))
    result = model.calculate(inputs, run.assumptions)
    assert _values(result)[:3] == (Decimal(20), Decimal(15), Decimal(5))
    trace = _traces(result)
    expected_schedule = tuple(row.record_id for row in sessions.rows[:-1]) + (changed_session.record_id,)
    expected_right = tuple(row.record_id for row in right.rows[:-1]) + (selected.record_id,)
    expected_left = tuple(row.record_id for row in left.rows)
    for expected in EXAMPLE.outputs:
        entry = trace[expected.output_id]
        assert entry.trace_id == entry.formula_id == expected.output_id
        assert entry.formula_version == "1"
        assert entry.expression == expected.expression
        assert entry.input_ids == expected.input_ids
        assert entry.check_ids == (expected.rule_id,)
        references = {"schedule_revision", "price_basis", "leg_methods"}
        if "left_closes" in entry.input_ids:
            references.add("left_proxy")
        if "right_closes" in entry.input_ids:
            references.add("right_proxy")
        assert set(entry.assumption_ids) == references
    assert trace["right_momentum"].source_record_ids == expected_schedule + expected_right
    assert trace["momentum_spread"].source_record_ids == expected_schedule + expected_left + expected_right
    assert trace["right_momentum"].substitutions[-1].value == Decimal(115)
    assert trace["right_momentum"].substitutions[-1].period_end == END
    assert trace["right_volatility"].intermediate_values[62].period_end == END


def _foreign_row(table, minute, category):
    published_at = utc(END, 22) + timedelta(minutes=minute)
    return table.rows[-1].model_copy(update={
        "entity_id": "foreign_entity", "record_id": f"foreign.{table.table_id}",
        "published_at": published_at, "vintage_at": published_at, "category": category,
    })


@pytest.mark.parametrize("table_index", (0, 2), ids=("calendar", "close"))
@pytest.mark.parametrize(("minute", "category"), [(1, "raw"), (0, "estimate")])
def test_ineligible_foreign_entities_leave_values_and_selected_ids_unchanged(
    model, run, table_index, minute, category,
):
    baseline = model.calculate(run.inputs, run.assumptions)
    tables = list(run.inputs.tables)
    original = tables[table_index]
    foreign = _foreign_row(original, minute, category)
    tables[table_index] = _rows(original, (foreign, *original.rows))

    result = model.calculate(_inputs(run, *tables), run.assumptions)

    assert _values(result) == tuple(Decimal(item.value) for item in EXAMPLE.outputs)
    assert result.trace == baseline.trace
    assert all(foreign.record_id not in entry.source_record_ids for entry in result.trace)


@pytest.mark.parametrize("table_index", (0, 2), ids=("calendar", "close"))
def test_observed_foreign_entities_at_the_cutoff_affect_binding(model, run, table_index):
    tables = list(run.inputs.tables)
    original = tables[table_index]
    foreign = _foreign_row(original, 0, "raw")
    tables[table_index] = _rows(original, (*original.rows, foreign))

    result = model.calculate(_inputs(run, *tables), run.assumptions)

    if table_index == 0:
        assert _values(result) == (None,) * 6
        assert "right_calendar requires an explicit calendar binding" in _outputs(result)["right_momentum"].reason
        assert result.trace == ()
    else:
        assert _values(result) == (Decimal(20), None, None, Decimal(40), None, None)
        assert "foreign_entity" in _outputs(result)["right_momentum"].reason
        assert result.trace == tuple(
            entry for entry in model.calculate(run.inputs, run.assumptions).trace
            if entry.output_id.startswith("left_")
        )


def test_unavailable_bound_sessions_are_retained_to_prevent_backfill(model, run):
    sessions, left, right = run.inputs.tables
    unavailable = sessions.rows[12].model_copy(update={
        "published_at": utc(END, 22) + timedelta(minutes=1),
    })
    older = sessions.rows[0].model_copy(update={
        "record_id": "older_session", "observation_date": START - timedelta(days=1),
    })
    sessions = _rows(sessions, (older, *sessions.rows[:12], unavailable, *sessions.rows[13:]))
    result = model.calculate(_inputs(run, sessions, left, right), run.assumptions)

    assert _values(result) == (None,) * 6
    assert f"{unavailable.observation_date} schedule session available after cutoff" in (
        _outputs(result)["left_momentum"].reason
    )


def test_unavailable_close_of_bound_proxy_retains_dated_reason(model, run):
    sessions, left, right = run.inputs.tables
    foreign = _foreign_row(right, 1, "raw")
    unavailable = right.rows[-1].model_copy(update={"published_at": foreign.published_at})
    right = _rows(right, (*right.rows[:-1], foreign, unavailable))
    result = model.calculate(_inputs(run, sessions, left, right), run.assumptions)

    assert _values(result) == (Decimal(20), None, None, Decimal(40), None, None)
    assert f"{END} close available after cutoff" in _outputs(result)["right_momentum"].reason
    assert "foreign_entity" not in _outputs(result)["right_momentum"].reason


@pytest.mark.parametrize(("field", "actual"), [("method_version", "2"), ("model_id", "different")])
def test_delegated_descriptor_must_match_pinned_method(model, run, monkeypatch, field, actual):
    describe = MomentumModel.describe

    def mismatched_descriptor(self):
        return describe(self).model_copy(update={field: actual})

    monkeypatch.setattr(MomentumModel, "describe", mismatched_descriptor)
    result = model.calculate(run.inputs, run.assumptions)

    assert _values(result) == (None, None, None, Decimal(40), Decimal(20), Decimal(20))
    assert all("etf_momentum@1" in output.reason and str(END) in output.reason for output in result.outputs[:3])
    assert tuple(_traces(result)) == OUTPUT_IDS[3:]


@pytest.mark.parametrize("shifted", ("none", "start", "interior"))
def test_mixed_calendars_preserve_complete_legs_and_withhold_spreads(model, run, shifted):
    sessions, left, right = run.inputs.tables
    reconciliation = {
        "none": {},
        "start": {START: START - timedelta(days=1)},
        "interior": {SESSIONS[9]: SESSIONS[9] - timedelta(days=1)},
    }[shifted]
    other = tuple(row.model_copy(update={
        "entity_id": "fixture_other_listing", "record_id": f"other.{row.record_id}",
        "observation_date": reconciliation.get(row.observation_date, row.observation_date),
    }) for row in sessions.rows)
    shifted_right = tuple(row.model_copy(update={
        "observation_date": reconciliation.get(row.observation_date, row.observation_date),
    }) for row in right.rows)
    inputs = _inputs(run, _rows(sessions, sessions.rows + other), left, _rows(right, shifted_right))
    assumptions = _assumptions(run, left_calendar="fixture_us_listing",
                              right_calendar="fixture_other_listing")

    result = model.calculate(inputs, assumptions)

    assert _values(result) == (Decimal(20), Decimal(10), None, Decimal(40), Decimal(20), None)
    for spread in SPREADS:
        reason = _outputs(result)[spread].reason
        assert "calendar" in reason and "fixture_us_listing" in reason and "fixture_other_listing" in reason
    trace = _traces(result)
    assert set(trace) == set(OUTPUT_IDS) - set(SPREADS)
    right_trace = trace["right_momentum"]
    assert right_trace.source_record_ids[:64] == tuple(row.record_id for row in other)
    assert "right_calendar" in right_trace.assumption_ids
    assert "left_calendar" in trace["left_momentum"].assumption_ids
    assert right_trace.intermediate_values[0].period_start == reconciliation.get(START, START)
    assert right_trace.intermediate_values[0].period_end == END


@pytest.mark.parametrize("binding", [None, "absent", "invalid_type"])
def test_one_calendar_binding_failure_preserves_the_other_leg(model, run, binding):
    sessions, left, right = run.inputs.tables
    other = tuple(row.model_copy(update={
        "entity_id": "fixture_other_listing", "record_id": f"other.{row.record_id}",
    }) for row in sessions.rows)
    inputs = _inputs(run, _rows(sessions, sessions.rows + other), left, right)
    assumptions = _assumptions(run, left_calendar="fixture_us_listing")
    if binding == "invalid_type":
        binding = Assumption(assumption_id="right_calendar", value_type="integer", value=1,
                             origin="method_default", rationale="Invalid binding type")
    if binding is not None:
        assumptions = _assumptions(run, left_calendar="fixture_us_listing", right_calendar=binding)
    result = model.calculate(inputs, assumptions)

    assert _values(result) == (Decimal(20), None, None, Decimal(40), None, None)
    for output_id in ("right_momentum", "right_volatility", *SPREADS):
        reason = _outputs(result)[output_id].reason
        assert "right" in reason.lower() and "calendar" in reason and str(END) in reason


def test_non_session_at_cutoff_does_not_move_the_right_window(model, run):
    sessions, left, right = run.inputs.tables
    other = tuple(row.model_copy(update={
        "entity_id": "fixture_other_listing", "record_id": f"other.{row.record_id}",
    }) for row in sessions.rows[:-1])
    inputs = _inputs(run, _rows(sessions, sessions.rows + other), left, right)
    assumptions = _assumptions(run, left_calendar="fixture_us_listing",
                              right_calendar="fixture_other_listing")
    result = model.calculate(inputs, assumptions)
    assert _values(result) == (Decimal(20), None, None, Decimal(40), None, None)
    assert "ending session is absent" in _outputs(result)["right_momentum"].reason
    assert str(END) in _outputs(result)["right_momentum"].reason


@pytest.mark.parametrize("problem", ("close", "table", "identity", "mixed_identities", "no_identity"))
def test_unavailable_right_leg_preserves_left_and_reports_dated_reasons(model, run, problem):
    sessions, left, right = run.inputs.tables
    assumptions = run.assumptions
    if problem == "close":
        right = _rows(right, right.rows[:-1])
    elif problem == "identity":
        assumptions = _assumptions(run, right_proxy="wrong_proxy")
    elif problem == "mixed_identities":
        wrong = right.rows[-1].model_copy(update={"entity_id": "wrong_proxy", "record_id": "wrong"})
        right = _rows(right, (*right.rows, wrong))
    elif problem == "no_identity":
        assumptions = _assumptions(run, right_proxy=None)
    inputs = _inputs(run, sessions, left, *(() if problem == "table" else (right,)))

    result = model.calculate(inputs, assumptions)

    assert _values(result) == (Decimal(20), None, None, Decimal(40), None, None)
    assert tuple(_traces(result)) == ("left_momentum", "left_volatility")
    for output in result.outputs:
        if output.value is None:
            assert "right" in output.reason.lower() and str(END) in output.reason
    if problem == "close":
        assert "missing close" in _outputs(result)["right_momentum"].reason
    if problem in {"identity", "mixed_identities"}:
        assert "wrong_proxy" in _outputs(result)["right_momentum"].reason


@pytest.mark.parametrize("key, value", [
    ("leg_methods", None),
    ("leg_methods", "etf_momentum@2, etf_realized_volatility@1"),
    ("schedule_revision", None),
    ("price_basis", "dividend_adjusted"),
])
def test_shared_requirements_withhold_all_values(model, run, key, value):
    result = model.calculate(run.inputs, _assumptions(run, **{key: value}))
    assert _values(result) == (None,) * len(OUTPUT_IDS)
    assert result.trace == ()
    assert all(str(END) in output.reason for output in result.outputs)
    assert key in result.outputs[0].reason


def test_volatility_failure_preserves_same_leg_momentum_and_its_spread(model, run):
    sessions, left, right = run.inputs.tables
    small_close = right.rows[30].model_copy(update={"value": Decimal("1e-38")})
    inputs = _inputs(run, sessions, left, _rows(right, (*right.rows[:30], small_close, *right.rows[31:])))
    result = model.calculate(inputs, run.assumptions)
    assert _values(result) == (Decimal(20), Decimal(10), Decimal(10), Decimal(40), None, None)
    assert tuple(_traces(result)) == OUTPUT_IDS[:4]
    for output_id in ("right_volatility", "volatility_spread"):
        reason = _outputs(result)[output_id].reason
        assert str(SESSIONS[31]) in reason and "decimal range" in reason


def test_fractional_spreads_are_independent_of_caller_precision(model, run):
    sessions, left, right = run.inputs.tables
    left_jump = Decimal("112.34567890123456789012345678901234567")
    left = _rows(left, (left.rows[0], *(
        row.model_copy(update={"value": left_jump}) for row in left.rows[1:]
    )))
    inputs = _inputs(run, sessions, left, right)
    with localcontext(prec=4):
        result = model.calculate(inputs, run.assumptions)
    assert _values(result) == tuple(map(Decimal, (
        "12.34567890123456789012345678901234567", "10", "2.34567890123456789012345678901234567",
        "24.69135780246913578024691357802469134", "20", "4.69135780246913578024691357802469134",
    )))
