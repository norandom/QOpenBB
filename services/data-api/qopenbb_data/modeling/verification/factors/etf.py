"""Independent references for the version 1 ETF price methods and ordered pair."""

from collections.abc import Callable, Mapping
from datetime import date, datetime
from decimal import Context, Decimal, localcontext
from fractions import Fraction
from functools import partial
from itertools import pairwise
from statistics import variance
from types import MappingProxyType

from ...contracts import (
    AssumptionSet,
    EvaluationCutoff,
    InputSnapshot,
    Observation,
    Tolerance,
)
from ..reference import Reference, ReferenceCalculation

_BASIS = "split_adjusted_dividends_excluded"
_PAIR = "proxy_comparison"
_LEG_VERSIONS = "etf_momentum@1, etf_realized_volatility@1"
_PERCENT = Tolerance(unit="percent", absolute="0.00000001")
_POINTS = Tolerance(unit="percentage_points", absolute="0.00000002")
type _Metric = Callable[[tuple[Decimal, ...]], Decimal | None]


def _eligible(row: Observation, cutoff: EvaluationCutoff) -> bool:
    return (
        row.category != "estimate"
        and row.observation_date <= cutoff.observation_date
        and row.context.vintage_coverage not in ("unknown", "unavailable")
        and row.published_at is not None
        and max(row.published_at, _revision(row)) <= min(cutoff.decision_at, cutoff.evaluated_at)
    )


def _revision(row: Observation) -> datetime:
    assert row.published_at is not None
    return row.vintage_at or row.published_at


def _latest_by_date(
    rows: tuple[Observation, ...], cutoff: EvaluationCutoff, dates: tuple[date, ...],
) -> dict[date, list[Observation]]:
    latest: dict[date, list[Observation]] = {}
    wanted = set(dates)
    for row in rows:
        day = row.observation_date
        if day not in wanted or not _eligible(row, cutoff):
            continue
        previous = latest.get(day)
        if previous is None or _revision(row) > _revision(previous[0]):
            latest[day] = [row]
        elif _revision(row) == _revision(previous[0]):
            previous.append(row)
    return latest


def _session_dates(rows: tuple[Observation, ...], cutoff: EvaluationCutoff) -> tuple[date, ...]:
    ending = cutoff.observation_date
    dates = tuple(sorted({row.observation_date for row in rows if row.observation_date <= ending})[-64:])
    if len(dates) != 64 or dates[-1] != ending:
        return ()
    # Decide which dates are required before checking publication eligibility.
    revisions = _latest_by_date(rows, cutoff, dates)
    if len(revisions) != 64 or any(
        row.value != 1 or row.context.unit != "session"
        for candidates in revisions.values() for row in candidates
    ):
        return ()
    return dates


def _prices(
    rows: tuple[Observation, ...], cutoff: EvaluationCutoff, dates: tuple[date, ...],
) -> tuple[Decimal, ...]:
    if not dates:
        return ()
    revisions = _latest_by_date(rows, cutoff, dates)
    if len(revisions) != len(dates):
        return ()
    closes = []
    contexts = set()
    for day in dates:
        values = set()
        for row in revisions[day]:
            value = row.value
            context = row.context
            if value is None or not value.is_finite() or value <= 0:
                return ()
            if (context.unit, context.basis) != ("price", _BASIS):
                return ()
            values.add(value)
            contexts.add((context.currency, context.scale))
        if len(values) != 1 or len(contexts) != 1:
            return ()
        closes.append(values.pop())
    return tuple(closes)


def _wire_value(value: Decimal) -> Decimal | None:
    if not value or -38 <= value.adjusted() <= 37:
        # The contract supports 38 significant digits and at most 38 fractional places.
        if not value:
            return Decimal(0)
        places = min(38, 37 - value.adjusted())
        rounded = round(value, places)
        if rounded.adjusted() <= 37:
            return rounded
    return None


def _decimal(value: Fraction) -> Decimal:
    return Decimal(value.numerator) / Decimal(value.denominator)


def _momentum(closes: tuple[Decimal, ...]) -> Decimal | None:
    change = Fraction(closes[-1]) / Fraction(closes[0]) - 1
    return _wire_value(_decimal(100 * change))


def _volatility(closes: tuple[Decimal, ...]) -> Decimal | None:
    returns = tuple(current / previous - 1 for previous, current in pairwise(map(Fraction, closes)))
    # Returns must also fit the wire contract because the method discloses each in its trace.
    if any(_wire_value(_decimal(value)) is None for value in returns):
        return None
    return _wire_value(_decimal(252 * 10_000 * variance(returns)).sqrt())


def _text_assumptions(assumptions: AssumptionSet) -> dict[str, str | None]:
    return {
        item.assumption_id: item.value if item.value_type == "text" and isinstance(item.value, str) else None
        for item in assumptions.assumptions
    }


def _leg(
    tables: dict[str, tuple[Observation, ...]], pins: dict[str, str | None],
    cutoff: EvaluationCutoff, metric: _Metric, side: str,
) -> tuple[str | None, Decimal | None]:
    schedule = tables.get("sessions", ())
    table_id = f"{side}_closes" if side else "closes"
    closes = tables.get(table_id, ())
    if side:
        proxy = pins.get(f"{side}_proxy")
        calendar_key = f"{side}_calendar"
        calendar = pins.get(calendar_key) if calendar_key in pins else _single_entity(schedule, cutoff)
        entities = {row.entity_id for row in closes if _eligible(row, cutoff)}
        if not proxy or entities - {proxy}:
            return calendar, None
    else:
        proxy = _single_entity(closes)
        calendar = _single_entity(schedule)
    if not proxy or not calendar:
        return calendar, None
    dates = _session_dates(tuple(row for row in schedule if row.entity_id == calendar), cutoff)
    prices = _prices(tuple(row for row in closes if row.entity_id == proxy), cutoff, dates)
    return calendar, metric(prices) if prices else None


def _single_entity(
    rows: tuple[Observation, ...], cutoff: EvaluationCutoff | None = None,
) -> str | None:
    entities = {row.entity_id for row in rows if cutoff is None or _eligible(row, cutoff)}
    return entities.pop() if len(entities) == 1 else None


def _calculate(
    inputs: InputSnapshot, assumptions: AssumptionSet, *, model_id: str, metric: _Metric, side: str = "",
) -> Decimal | None:
    cutoff = inputs.cutoff
    if (
        inputs.schema_id != f"{model_id}.inputs" or inputs.schema_version != "1"
        or assumptions.version != "1" or cutoff is None or assumptions.effective_date > cutoff.observation_date
    ):
        return None
    pins = _text_assumptions(assumptions)
    revision = pins.get("schedule_revision")
    if not revision or not revision.strip() or pins.get("price_basis") != _BASIS:
        return None
    if model_id == _PAIR and pins.get("leg_methods") != _LEG_VERSIONS:
        return None
    tables = {
        table.table_id: tuple(row for row in table.rows if row.metric_id == (
            "session" if table.table_id == "sessions" else "close"
        ))
        for table in inputs.tables
    }
    with localcontext(Context(prec=160)):
        if side != "spread":
            return _leg(tables, pins, cutoff, metric, side)[1]
        left_calendar, left_value = _leg(tables, pins, cutoff, metric, "left")
        right_calendar, right_value = _leg(tables, pins, cutoff, metric, "right")
        if left_calendar != right_calendar or left_value is None or right_value is None:
            return None
        return _wire_value(left_value - right_value)


def _reference(
    calculations: dict[str, ReferenceCalculation], tolerances: Mapping[str, Tolerance],
) -> Reference:
    return Reference("1", MappingProxyType(calculations), MappingProxyType(tolerances))


def momentum_reference() -> Reference:
    """Return the verifier reference for etf_momentum@1."""
    return _reference(
        {"momentum": partial(_calculate, model_id="etf_momentum", metric=_momentum)},
        {"momentum": _PERCENT},
    )


def volatility_reference() -> Reference:
    """Return the verifier reference for etf_realized_volatility@1."""
    return _reference(
        {"realized_volatility": partial(_calculate, model_id="etf_realized_volatility", metric=_volatility)},
        {"realized_volatility": _PERCENT},
    )


def comparison_reference() -> Reference:
    """Return the verifier reference for proxy_comparison@1 and both pinned legs."""
    calculations = {}
    tolerances = {}
    for name, metric in (("momentum", _momentum), ("volatility", _volatility)):
        for side, output_id in (("left", f"left_{name}"), ("right", f"right_{name}"), ("spread", f"{name}_spread")):
            calculations[output_id] = partial(_calculate, model_id=_PAIR, metric=metric, side=side)
            tolerances[output_id] = _POINTS if side == "spread" else _PERCENT
    return _reference(calculations, tolerances)
