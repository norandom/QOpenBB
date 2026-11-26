"""Independent calendar join and exact-rational ETF formulas for the retrieved FMP pair."""

from datetime import UTC, datetime, timedelta
from decimal import Context, localcontext
from functools import partial
from types import MappingProxyType
from zoneinfo import ZoneInfo

from ...contracts import AssumptionSet, InputSnapshot
from ..reference import Reference
from .etf import (
    _BASIS,
    _latest_by_date,
    _momentum,
    _session_dates,
    _text_assumptions,
    _volatility,
    _wire_value,
)


def _acquisition_matches(inputs, assumptions):
    source = inputs.provenance
    cutoff = inputs.cutoff
    if (
        inputs.schema_id != "proxy_comparison.inputs"
        or cutoff is None
        or assumptions.effective_date > cutoff.observation_date
        or (source.origin, source.source) != ("service_acquired", "fmp")
        or not source.acquisition_id
    ):
        return False
    query = dict(source.query)
    pins = _text_assumptions(assumptions)
    expected = {
        "dataset_id": "story.etf_pair",
        "schedule_revision": pins.get("schedule_revision"),
        "calendar_id": pins.get("calendar_id"),
        "left_proxy": pins.get("left_proxy"),
        "right_proxy": pins.get("right_proxy"),
    }
    if any(not value or query.get(key) != value for key, value in expected.items()):
        return False
    if (
        pins.get("left_calendar") != query["calendar_id"]
        or pins.get("right_calendar") != query["calendar_id"]
        or query["left_proxy"] == query["right_proxy"]
        or pins.get("price_basis") != _BASIS
        or pins.get("leg_methods") != "etf_momentum@1, etf_realized_volatility@1"
    ):
        return False
    tables = {table.table_id: table.rows for table in inputs.tables}
    stamps = []
    for side in ("left", "right"):
        stamp = query.get(f"{side}_retrieved_at")
        if f"{side}_error" in query:
            if (
                query[f"{side}_error"] not in ("missing_data", "upstream", "entitlement", "invalid_response", "throttling", "timeout")
                or tables.get(f"{side}_closes") != ()
                or stamp is not None
            ):
                return False
        elif stamp is None:
            return False
        else:
            stamps.append(stamp)
    if not stamps:
        return False
    try:
        times = [datetime.fromisoformat(stamp) for stamp in stamps]
    except ValueError:
        return False
    return (
        all("T" in stamp for stamp in stamps)
        and all(when.utcoffset() == timedelta(0) for when in times)
        and max(times) == source.retrieved_at <= datetime.now(UTC)
        and min(times).astimezone(ZoneInfo(cutoff.session_timezone)).date() >= cutoff.observation_date
    )


def _history(rows, dates, proxy, receipt):
    selected = [row for row in rows if row.observation_date in dates]
    if len(selected) != len(dates):
        return ()
    if any(
        row.metric_id != "close"
        or row.entity_id != proxy
        or row.category != "provider"
        or not row.source_record_id
        or row.value is None
        or row.value <= 0
        or any(stamp > receipt for stamp in (row.published_at, row.vintage_at) if stamp is not None)
        or (row.context.unit, row.context.basis, row.context.currency, row.context.scale)
        != ("price", _BASIS, "USD", 0)
        for row in selected
    ):
        return ()
    ordered = sorted(selected, key=lambda row: row.observation_date)
    if tuple(row.observation_date for row in ordered) != dates:
        return ()
    return tuple(row.value for row in ordered)


def _calculate(inputs: InputSnapshot, assumptions: AssumptionSet, *, side: str, metric):
    if not _acquisition_matches(inputs, assumptions):
        return None
    cutoff = inputs.cutoff
    assert cutoff is not None
    query = dict(inputs.provenance.query)
    tables = {table.table_id: table.rows for table in inputs.tables}
    schedule = tuple(
        row
        for row in tables.get("sessions", ())
        if row.metric_id == "session" and row.entity_id == query["calendar_id"]
    )
    dates = _session_dates(schedule, cutoff)
    if not dates:
        return None
    end_rows = _latest_by_date(schedule, cutoff, (dates[-1],))[dates[-1]]
    close_hour = max(13 if row.context.basis == "early_close_1300_eastern" else 16 for row in end_rows)
    with localcontext(Context(prec=160)):
        values = []
        for leg in ("left", "right") if side == "spread" else (side,):
            stamp = query.get(f"{leg}_retrieved_at")
            if stamp is None:
                return None
            local_receipt = datetime.fromisoformat(stamp).astimezone(ZoneInfo(cutoff.session_timezone))
            if local_receipt.date() == dates[-1] and local_receipt.hour < close_hour:
                return None
            closes = _history(
                tables.get(f"{leg}_closes", ()), dates, query[f"{leg}_proxy"], datetime.fromisoformat(stamp)
            )
            value = metric(closes) if closes else None
            if value is None:
                return None
            values.append(value)
        return values[0] if side != "spread" else _wire_value(values[0] - values[1])


def retrospective_reference() -> Reference:
    calculations = {}
    for name, metric in (("momentum", _momentum), ("volatility", _volatility)):
        for side in ("left", "right", "spread"):
            key = f"{name}_spread" if side == "spread" else f"{side}_{name}"
            calculations[key] = partial(_calculate, side=side, metric=metric)
    return Reference("2", MappingProxyType(calculations), MappingProxyType({}))
