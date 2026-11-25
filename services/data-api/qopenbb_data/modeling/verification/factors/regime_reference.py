"""Version 1 independent scalar reference for the DFII10 endpoint regime."""

from collections import defaultdict
from collections.abc import Iterable
from datetime import date
from decimal import Context, Decimal, localcontext

from ...contracts import (
    AssumptionSet,
    EvaluationCutoff,
    InputSnapshot,
    Observation,
    Tolerance,
)
from ..reference import Reference


def _latest(rows: Iterable[Observation], cutoff: EvaluationCutoff) -> tuple[Observation, ...]:
    available_at = min(cutoff.decision_at, cutoff.evaluated_at)
    eligible = [
        (row.vintage_at or row.published_at, row)
        for row in rows
        if row.category != "estimate" and row.published_at is not None
        and max(row.vintage_at or row.published_at, row.published_at) <= available_at
        and row.context.vintage_coverage not in {"unknown", "unavailable"}
    ]
    if not eligible:
        return ()
    revision = max(timestamp for timestamp, _ in eligible)
    return tuple(row for timestamp, row in eligible if timestamp == revision)


def _dates(rows: tuple[Observation, ...], cutoff: EvaluationCutoff) -> tuple[date, date] | None:
    sessions = tuple(row for row in rows if row.metric_id == "session")
    if len({row.entity_id for row in sessions}) != 1:
        return None
    calendar = defaultdict(list)
    for row in sessions:
        if row.observation_date <= cutoff.observation_date:
            calendar[row.observation_date].append(row)
    dates = sorted(calendar)[-64:]
    if len(dates) != 64 or dates[-1] != cutoff.observation_date:
        return None
    # Check the markers after fixing the dates. Dropping an unavailable marker
    # would move the starting endpoint to a different session.
    for day in dates:
        markers = _latest(calendar[day], cutoff)
        if not markers or any(row.value != 1 or row.context.unit != "session" for row in markers):
            return None
    return dates[0], dates[-1]


def _endpoint(rows: tuple[Observation, ...], day: date, cutoff: EvaluationCutoff) -> Decimal | None:
    levels = _latest(
        (row for row in rows if row.observation_date == day
         and (row.entity_id, row.metric_id) == ("DFII10", "real_yield")
         and row.context.vintage_coverage == "known"),
        cutoff,
    )
    for row in levels:
        context = row.context
        if (row.value is None or not row.value.is_finite()
                or (context.unit, context.quantity, context.basis) !=
                ("percent", "rate", "treasury_constant_maturity")
                or context.currency is not None or context.scale != 0
                or context.period_start not in (None, day) or context.period_end not in (None, day)):
            return None
    amounts = {row.value for row in levels}
    return amounts.pop() if len(amounts) == 1 else None


def _change(inputs: InputSnapshot, assumptions: AssumptionSet) -> Decimal | None:
    cutoff = inputs.cutoff
    if (inputs.schema_id != "real_yield_regime.inputs" or inputs.schema_version != "1"
            or assumptions.version != "1" or cutoff is None
            or assumptions.effective_date > cutoff.observation_date):
        return None
    if not any(item.assumption_id == "schedule_revision" and item.value_type == "text"
               and isinstance(item.value, str) and item.value.strip() for item in assumptions.assumptions):
        return None
    tables = {table.table_id: table.rows for table in inputs.tables}
    dates = _dates(tables.get("sessions", ()), cutoff)
    if dates is None:
        return None
    beginning, ending = (_endpoint(tables.get("dfii10", ()), day, cutoff) for day in dates)
    if beginning is None or ending is None:
        return None
    with localcontext(Context(prec=80)):
        change = ending - beginning
        if not change:
            return Decimal(0)
        if change.adjusted() > 37:
            return None
        change = round(change, min(38, 37 - change.adjusted()))
        return change if change.adjusted() <= 37 else None


def _regime(inputs: InputSnapshot, assumptions: AssumptionSet) -> str | None:
    change = _change(inputs, assumptions)
    if change is None:
        return None
    return "flat" if change.is_zero() else ("falling" if change.is_signed() else "rising")


def regime_reference() -> Reference:
    """Bind exact classification and the frozen percentage-point tolerance."""
    return Reference("1", {"regime": _regime, "change": _change},
                     {"change": Tolerance(unit="percentage_points", absolute=Decimal("0.00000002"))})
