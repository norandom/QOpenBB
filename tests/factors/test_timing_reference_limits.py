"""Exercise the raw timing verifier at the snapshot's observation limit."""

from datetime import date, timedelta
from decimal import Decimal
from itertools import batched, pairwise

from fixtures.factor_examples import EXAMPLES, build_run, text_assumption
from fixtures.factor_inputs import cutoff, row, table, utc
from qopenbb_data.modeling.contracts import AssumptionSet, InputSnapshot
from qopenbb_data.modeling.verification.factors.timing_reference import rebuild_timing


def test_full_snapshot_with_chunked_calendar_and_extreme_returns():
    run = build_run(EXAMPLES["timing_study"], False)
    days = [date(2010, 1, 1) + timedelta(days=index) for index in range(5002)]
    calendar = (f"{day}T14:00:00+00:00/{day}T22:00:00+00:00" for day in reversed(days))
    settings = [
        item for item in run.assumptions.assumptions
        if item.assumption_id not in {"study_schedule", "study_dates"}
    ]
    settings.append(text_assumption("study_dates", f"{days[1]}/{days[-1]}", "Full snapshot path"))
    for index, chunk in enumerate(batched(calendar, 70), 1):
        key = "study_schedule" if index == 1 else f"study_schedule.{index}"
        settings.append(text_assumption(key, ";".join(chunk), "Dated calendar chunk"))
    signals = tuple(
        row("fixture_left", "momentum", day, "1", "percent", published_at=utc(day, 21))
        for day in days[:-2]
    )
    returns = tuple(
        row("fixture_left", "forward_return", end, "1" + "0" * 37 if index < 2500 else "-50", "percent",
            published_at=utc(end, 15), period_start=start, period_end=end, basis="open_to_open")
        for index, (start, end) in enumerate(pairwise(days[1:]))
    )
    inputs = InputSnapshot(
        schema_id=run.inputs.schema_id, cutoff=cutoff(days[-1]), provenance=run.inputs.provenance,
        tables=(table("dated_signals", "Decision-day signals", signals),
                table("forward_returns", "Realized ending-session returns", returns)),
    )
    assumptions = AssumptionSet(version="1", effective_date=days[0], assumptions=settings)
    study = rebuild_timing(inputs, assumptions)
    assert study is not None
    assert len(study.intervals) == 5000
    assert study.intervals[0].start == days[1]
    assert study.intervals[-1].end == days[-1]
    assert study.groups[None].excluded_count == 5000
    assert study.values["study_drawdown"] == Decimal(100)
