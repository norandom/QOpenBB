"""Timing-study candidate values and scope-specific trace evidence."""

from datetime import date, timedelta
from decimal import Decimal, Inexact, localcontext
from itertools import batched, pairwise

import pytest
from fixtures.factor_examples import EXAMPLES, build_run, text_assumption
from fixtures.factor_inputs import STUDY_DATES, cutoff, row, utc
from qopenbb_data.modeling.models.factors.diagnostics import TimingStudyModel
from qopenbb_data.modeling.models.protocol import CandidateResult

MODEL = TimingStudyModel()
EXAMPLE = EXAMPLES["timing_study"]


@pytest.fixture
def run():
    return build_run(EXAMPLE, missing=False)


def _calculate(run, *, edit=None, remove=None, append=None, assumptions=None):
    tables = []
    for table in run.inputs.tables:
        rows = tuple(
            item.model_copy(update={"value": Decimal(edit[item.record_id])})
            if edit and item.record_id in edit else item
            for item in table.rows if not remove or item.record_id not in remove
        )
        tables.append(table.model_copy(update={"rows": rows + tuple((append or {}).get(table.table_id, ()))}))
    return MODEL.calculate(run.inputs.model_copy(update={"tables": tuple(tables)}), assumptions or run.assumptions)


def _outputs(result):
    return {output.output_id: output for output in result.outputs}


def _values(result):
    return {key: output.value for key, output in _outputs(result).items()}


def _entries(result, output_id):
    return tuple(entry for entry in result.trace if entry.output_id == output_id)


def _intermediates(result, output_id):
    return {item.name: item.value for entry in _entries(result, output_id) for item in entry.intermediate_values}


def _assumptions(run, key, value):
    items = tuple(item for item in run.assumptions.assumptions if item.assumption_id != key)
    if value is not None:
        items += (text_assumption(key, value, "Test the supplied timing-study configuration"),)
    return run.assumptions.model_copy(update={"assumptions": items})


def test_frozen_descriptor():
    assert MODEL.describe() == EXAMPLE.descriptor()


@pytest.mark.parametrize("missing", [False, True])
def test_frozen_results_and_trace(missing):
    run = build_run(EXAMPLE, missing=missing)
    result = _calculate(run)
    assert CandidateResult.model_validate_json(result.model_dump_json()) == result
    outputs = _outputs(result)
    for expected in run.outputs:
        actual = outputs[expected.output_id]
        if expected.value is None:
            assert actual.value is None
            assert "loser" in actual.reason and "2 eligible" in actual.reason
        else:
            assert actual.value == pytest.approx(expected.value, abs=Decimal("1e-27"))
    assert all(_entries(result, key) for key in outputs)
    rising = _intermediates(result, "rising_slugging")
    assert rising["hit_rate_denominator"] == (2 if missing else 3)
    assert rising["excluded_count"] == int(missing)
    assert rising["tie_count"] == 1
    assert rising["mean_winner"] == 10
    if missing:
        assert "absolute_mean_loser" not in rising
        assert any("missing benchmark return" in entry.expression
                   for entry in _entries(result, "rising_slugging"))
    else:
        assert rising["absolute_mean_loser"] == 5
    falling = _intermediates(result, "falling_slugging")
    assert falling["mean_winner"] == 12 and falling["absolute_mean_loser"] == 4
    assert any("out_of_sample" in entry.expression for entry in _entries(result, "rising_hit_rate"))


@pytest.mark.parametrize(("edit_index", "value", "hit_rate", "reason"), [
    (0, "0", Decimal(0), "winner"),
    (4, "0", Decimal(1) / 3, "loser"),
])
def test_rising_slugging_withholds_only_the_missing_side(run, edit_index, value, hit_rate, reason):
    rows = run.inputs.tables[2].rows
    outputs = _outputs(_calculate(run, edit={rows[edit_index].record_id: value}))
    assert outputs["rising_hit_rate"].value == pytest.approx(hit_rate, abs=Decimal("1e-27"))
    assert outputs["rising_slugging"].value is None
    assert reason in outputs["rising_slugging"].reason
    assert outputs["falling_slugging"].value == 3
    assert outputs["study_drawdown"].value is not None


def test_group_of_ties_retains_denominator_and_discloses_both_missing_sides(run):
    rows = run.inputs.tables[2].rows
    result = _calculate(run, edit={rows[0].record_id: "0", rows[4].record_id: "0"})
    outputs = _outputs(result)
    assert outputs["rising_hit_rate"].value == 0
    assert "winner" in outputs["rising_slugging"].reason
    assert "loser" in outputs["rising_slugging"].reason
    rising = _intermediates(result, "rising_slugging")
    assert rising["tie_count"] == rising["hit_rate_denominator"] == 3


def test_missing_regime_benchmark_and_flat_coverage(run):
    regimes = run.inputs.tables[1].rows
    returns = run.inputs.tables[2].rows
    remove = {regimes[0].record_id, *(item.record_id for item in returns[1::2])}
    result = _calculate(run, edit={regimes[1].record_id: "0"}, remove=remove)
    outputs = _outputs(result)
    assert outputs["study_drawdown"].value == Decimal("8.8")
    for key in ("rising_hit_rate", "rising_slugging", "falling_hit_rate", "falling_slugging"):
        assert outputs[key].value is None and "0 eligible" in outputs[key].reason
        values = _intermediates(result, key)
        assert values["hit_rate_denominator"] == 0
        assert values["flat.excluded_count"] == values["unknown.excluded_count"] == 1
        assert any("missing benchmark return" in entry.expression for entry in _entries(result, key))
    allowed = {item.record_id for item in (*run.inputs.tables[0].rows, *returns[::2])}
    entries = _entries(result, "study_drawdown")
    assert {record for entry in entries for record in entry.source_record_ids} == allowed
    assert all("dated_regimes" not in entry.input_ids and "benchmark" not in entry.assumption_ids
               for entry in entries)



def test_flat_coverage_discloses_outcome_statistics_and_original_rows(run):
    signals, regimes, returns = (table.rows for table in run.inputs.tables)
    result = _calculate(run, edit={item.record_id: "0" for item in regimes})
    expected = {
        "flat.eligible_count": 5, "flat.excluded_count": 0, "flat.hit_rate_denominator": 5,
        "flat.winner_count": 2, "flat.loser_count": 2, "flat.tie_count": 1,
        "flat.mean_winner": 11, "flat.absolute_mean_loser": Decimal("4.5"),
    }
    for key, output in _outputs(result).items():
        if key == "study_drawdown":
            assert output.value == Decimal("8.8")
            assert all(".coverage." not in entry.trace_id for entry in _entries(result, key))
            continue
        assert output.value is None and "0 eligible" in output.reason
        assert expected.items() <= _intermediates(result, key).items()
        entries = [entry for entry in _entries(result, key) if ".coverage.flat" in entry.trace_id]
        assert {ref for entry in entries for ref in entry.source_record_ids} == {
            item.record_id for item in (*signals, *regimes, *returns)
        }
        assert all(entry.input_ids == ("dated_signals", "dated_regimes", "forward_returns")
                   for entry in entries)
        means = [value for entry in entries for value in entry.intermediate_values
                 if value.name in {"flat.mean_winner", "flat.absolute_mean_loser"}]
        assert len(means) == 2 and all(value.unit == "percentage_points" for value in means)


@pytest.mark.parametrize("estimate", [False, True])
def test_unknown_coverage_cites_rejected_regime_without_scoring_its_outcome(run, estimate):
    regime = run.inputs.tables[1].rows[0]
    invalid = regime.model_copy(update={"category": "estimate"} if estimate else {
        "context": regime.context.model_copy(update={"unit": "percent"}),
    })
    result = _calculate(run, remove={regime.record_id}, append={"dated_regimes": (invalid,)})
    outputs = _outputs(result)
    assert outputs["rising_hit_rate"].value == 0
    assert outputs["study_drawdown"].value == Decimal("8.8")
    assert len({entry.trace_id for entry in result.trace}) == len(result.trace)
    for key in ("rising_hit_rate", "rising_slugging", "falling_hit_rate", "falling_slugging"):
        entries = [entry for entry in _entries(result, key) if ".coverage.unknown" in entry.trace_id]
        reason = "regime.unavailable" if estimate else "regime.invalid"
        assert any(reason in entry.expression for entry in entries)
        assert {ref for entry in entries for ref in entry.source_record_ids} == {regime.record_id}
        assert all("dated_regimes" in entry.input_ids for entry in entries)
        values = _intermediates(result, key)
        assert values["unknown.excluded_count"] == 1
        assert "unknown.hit_rate_denominator" not in values
        assert "unknown.winner_count" not in values and "unknown.mean_winner" not in values
    assert all(regime.record_id not in entry.source_record_ids
               for entry in _entries(result, "study_drawdown"))


def test_cash_returns_are_zero_even_without_asset_rows(run):
    signals, _, returns = (table.rows for table in run.inputs.tables)
    edit = {signals[0].record_id: "0", signals[1].record_id: "-1", returns[1].record_id: "3"}
    result = _calculate(run, edit=edit, remove={returns[0].record_id, returns[2].record_id})
    assert _values(result)["study_drawdown"] == Decimal("8.8")
    assert _values(result)["rising_hit_rate"] == 0
    path = _intermediates(result, "study_drawdown")
    assert path["initial_wealth"] == path["initial_peak"] == 1
    assert path[f"strategy_return.{STUDY_DATES[2]}"] == path[f"strategy_return.{STUDY_DATES[3]}"] == 0


@pytest.mark.parametrize(("first", "second", "expected"), [
    ("-25", "100", "25"),
    ("-100", "99999999999999999999999999999999999999", "100"),
    ("-0.00000000000000000000000000000000000001", "100", "0.00000000000000000000000000000000000001"),
])
def test_drawdown_includes_initial_peak_and_handles_total_loss(run, first, second, expected):
    returns = run.inputs.tables[2].rows
    edits = {item.record_id: value for item, value in
             zip(returns[::2], (first, second, "0", "0", "0"), strict=True)}
    with localcontext(prec=1, Emin=-1, Emax=1) as context:
        context.traps[Inexact] = True
        result = _calculate(run, edit=edits)
    assert _values(result)["study_drawdown"] == Decimal(expected)
    dated = [item for entry in _entries(result, "study_drawdown") for item in entry.intermediate_values
             if item.name.startswith("strategy_return.")]
    assert [item.value for item in dated][:2] == [Decimal(first), Decimal(second)]
    assert [(item.period_start, item.period_end) for item in dated] == list(pairwise(STUDY_DATES[1:]))


@pytest.mark.parametrize("scope", ["signal", "asset_return", "asset_overlap", "benchmark_overlap"])
def test_gaps_and_overlaps_are_isolated_by_scope(run, scope):
    signals, _, returns = (table.rows for table in run.inputs.tables)
    remove, append = set(), {}
    if scope == "signal":
        remove.add(signals[1].record_id)
    elif scope == "asset_return":
        remove.add(returns[2].record_id)
    else:
        original = returns[2 if scope == "asset_overlap" else 3]
        overlapping = original.model_copy(update={
            "record_id": original.record_id + ".overlap",
            "vintage_at": utc(STUDY_DATES[3], 16),
            "context": original.context.model_copy(update={"period_start": STUDY_DATES[1]}),
        })
        append["forward_returns"] = (overlapping,)
    result = _calculate(run, remove=remove, append=append)
    outputs = _outputs(result)
    drawdown = outputs["study_drawdown"]
    if scope == "benchmark_overlap":
        assert drawdown.value == Decimal("8.8")
        assert all(overlapping.record_id not in entry.source_record_ids
                   for entry in _entries(result, "study_drawdown"))
    else:
        assert drawdown.value is None
        assert "incomplete" in drawdown.reason
        assert any("missing" in entry.expression or "invalid_interval" in entry.expression
                   for entry in _entries(result, "study_drawdown"))
    assert outputs["falling_slugging"].value == 3
    assert _intermediates(result, "rising_hit_rate")["excluded_count"] == (2 if append else 1)


@pytest.mark.parametrize(("key", "value"), [
    ("benchmark", None),
    ("position_rule", None),
    ("drawdown_basis", "regime_only"),
    ("horizon", "two_sessions"),
    ("partition", "mixed"),
    ("study_schedule", None),
    ("study_dates", "2024-06-11/2024-06-04"),
])
def test_invalid_study_configuration_explains_withholding(run, key, value):
    result = _calculate(run, assumptions=_assumptions(run, key, value))
    assert len(result.outputs) == 5
    assert all(output.value is None and key in output.reason for output in result.outputs)


def test_high_magnitude_mean_and_exact_ratio_rounding_are_independent(run):
    returns = run.inputs.tables[2].rows
    edits = {
        returns[0].record_id: "99999999999999999999999999999999999999",
        returns[1].record_id: "-100",
        returns[4].record_id: "-100",
        returns[5].record_id: "99999999999999999999999999999999999998",
    }
    with localcontext(prec=1, Emin=-1, Emax=1) as context:
        context.traps[Inexact] = True
        result = _calculate(run, edit=edits)
    assert _values(result)["rising_slugging"] == 1
    assert _values(result)["rising_hit_rate"] == Decimal("0.33333333333333333333333333333333333333")
    assert _values(result)["study_drawdown"] == 100
    assert any("100000000000000000000000000000000000099" in entry.expression
               for entry in _entries(result, "rising_slugging"))


def test_ratio_below_wire_range_withholds_only_slugging(run):
    returns = run.inputs.tables[2].rows
    edits = {
        returns[0].record_id: "0.00000000000000000000000000000000000001",
        returns[4].record_id: "-2",
    }
    result = _calculate(run, edit=edits)
    outputs = _outputs(result)
    assert outputs["rising_slugging"].value is None
    assert "decimal range" in outputs["rising_slugging"].reason
    assert outputs["rising_hit_rate"].value != 0
    assert outputs["falling_slugging"].value == 3


def test_long_schedule_chunks_trace_without_losing_evidence(run):
    days = tuple(date(2024, 6, 3) + timedelta(days=offset) for offset in range(272))
    signals, regimes, forwards = _long_study_rows(days)
    tables = tuple(table.model_copy(update={"rows": rows}) for table, rows in
                   zip(run.inputs.tables, (signals, regimes, forwards), strict=True))
    inputs = run.inputs.model_copy(update={"cutoff": cutoff(days[-1]), "tables": tables})
    assumptions, schedule_keys = _long_study_assumptions(run, days)
    result = MODEL.calculate(inputs, assumptions)
    assert _values(result)["study_drawdown"] == 0
    assert _values(result)["rising_hit_rate"] == 1
    assert _intermediates(result, "rising_hit_rate")["flat.hit_rate_denominator"] == 135
    assert len({entry.trace_id for entry in result.trace}) == len(result.trace)
    for output_id, originals in (
        ("rising_hit_rate", (*signals, *regimes, *forwards)),
        ("study_drawdown", (*signals, *forwards[::2])),
    ):
        entries = _entries(result, output_id)
        assert len(entries) > 1
        assert {ref for entry in entries for ref in entry.source_record_ids} == {
            item.record_id for item in originals
        }
        assert {value.name for entry in entries for value in entry.substitutions} == {
            item.record_id for item in originals
        }
        assert schedule_keys <= {key for entry in entries for key in entry.assumption_ids}
        assert all("unused" not in entry.assumption_ids for entry in entries)
        assert all(max(len(entry.source_record_ids), len(entry.assumption_ids),
                       len(entry.substitutions), len(entry.intermediate_values)) <= 256 for entry in entries)


def _long_study_rows(days):
    signals = tuple(row("fixture_left", "momentum", day, "1", "percent", published_at=utc(day, 21))
                    for day in days[:-2])
    regimes = tuple(row("DFII10", "endpoint_change", day, "1" if index % 2 else "0", "percentage_points",
                        published_at=utc(day, 21)) for index, day in enumerate(days[:-2]))
    returns = tuple(row(entity, "forward_return", end, value, "percent", published_at=utc(end, 15),
                        period_start=start, period_end=end, basis="open_to_open")
                    for start, end in pairwise(days[1:])
                    for entity, value in (("fixture_left", "1"), ("fixture_benchmark", "0")))
    return signals, regimes, returns


def _long_study_assumptions(run, days):
    base = _assumptions(run, "study_dates", f"{days[1]}/{days[-1]}")
    chunks = batched((f"{day}T14Z/{day}T22Z" for day in days), 60)
    schedule = tuple(text_assumption("study_schedule" if i == 1 else f"study_schedule.{i}",
                                     ";".join(chunk), "Dated test opens and decision cutoffs")
                     for i, chunk in enumerate(chunks, 1))
    items = tuple(item for item in base.assumptions if item.assumption_id != "study_schedule")
    assumptions = base.model_copy(update={
        "assumptions": (*items, *schedule, text_assumption("unused", "ignored", "Unrelated scenario")),
    })
    return assumptions, {item.assumption_id for item in schedule}
