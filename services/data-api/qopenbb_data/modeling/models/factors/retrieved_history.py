"""Receipt-bound FMP close windows for retrospective ETF comparisons."""

from datetime import UTC, datetime, time, timedelta
from zoneinfo import ZoneInfo

from ...contracts import AssumptionSet, InputSnapshot
from .method_inputs import evaluation_cutoff, input_rows, text_assumption
from .sessions import PRICE_BASIS, PriceWindow, resolve_session_window


def receipts(inputs: InputSnapshot, assumptions: AssumptionSet) -> dict[str, datetime]:
    cutoff = evaluation_cutoff(inputs, assumptions, "proxy_comparison")
    provenance = inputs.provenance
    query = dict(provenance.query)
    if (
        provenance.origin != "service_acquired"
        or provenance.source != "fmp"
        or not provenance.acquisition_id
        or query.get("dataset_id") != "story.etf_pair"
    ):
        raise ValueError("Retrospective comparison requires a service-acquired FMP story.etf_pair snapshot")
    for key in ("left_proxy", "right_proxy", "calendar_id", "schedule_revision"):
        if query.get(key) != text_assumption(assumptions, key):
            raise ValueError(f"FMP acquisition differs from the {key} assumption")
    if query["left_proxy"] == query["right_proxy"]:
        raise ValueError("Retrospective comparison requires distinct ETFs")
    if (
        text_assumption(assumptions, "leg_methods") != "etf_momentum@1, etf_realized_volatility@1"
        or text_assumption(assumptions, "price_basis") != PRICE_BASIS
    ):
        raise ValueError("Unexpected retrospective ETF formula or price basis")
    times = {}
    for side in ("left", "right"):
        if text_assumption(assumptions, f"{side}_calendar") != query["calendar_id"]:
            raise ValueError("Both ETF legs must follow the acquired calendar")
        failure = query.get(f"{side}_error")
        if failure is not None:
            if (
                failure not in {"missing_data", "upstream", "entitlement", "invalid_response", "throttling", "timeout"}
                or f"{side}_retrieved_at" in query
                or input_rows(inputs, f"{side}_closes")
            ):
                raise ValueError(f"Inconsistent acquisition failure for {side} ETF")
            continue
        stamp = query.get(f"{side}_retrieved_at", "")
        try:
            when = datetime.fromisoformat(stamp)
        except ValueError:
            raise ValueError(f"Missing or invalid {side} FMP retrieval timestamp") from None
        if "T" not in stamp or when.utcoffset() != timedelta(0):
            raise ValueError(f"{side} retrieval time must be a UTC timestamp")
        if when.astimezone(ZoneInfo(cutoff.session_timezone)).date() < cutoff.observation_date:
            raise ValueError(f"{side} receipt predates the ending session")
        times[side] = when
    if (
        not times
        or max(times.values()) != provenance.retrieved_at
        or provenance.retrieved_at > datetime.now(UTC)
    ):
        raise ValueError("Invalid latest FMP retrieval time")
    return times


def retrieved_window(
    inputs: InputSnapshot,
    assumptions: AssumptionSet,
    side: str,
    received_at: datetime | None,
) -> PriceWindow:
    cutoff = evaluation_cutoff(inputs, assumptions, "proxy_comparison")
    calendar = text_assumption(assumptions, "calendar_id")
    window = resolve_session_window(
        input_rows(inputs, "sessions"),
        calendar_id=calendar,
        cutoff=cutoff,
        schedule_revision=text_assumption(assumptions, "schedule_revision"),
    )
    proxy = text_assumption(assumptions, f"{side}_proxy")
    failure = dict(inputs.provenance.query).get(f"{side}_error")
    if failure:
        raise ValueError(f"FMP {side} leg {proxy} on {cutoff.observation_date}: {failure}")
    if received_at is None:
        raise ValueError(f"Missing FMP receipt for {proxy}")
    ending_marker = next(row for row in input_rows(inputs, "sessions")
                         if row.record_id == window.source_record_ids[-1])
    close_hour = 13 if ending_marker.context.basis == "early_close_1300_eastern" else 16
    closing = datetime.combine(cutoff.observation_date, time(close_hour), ZoneInfo(cutoff.session_timezone))
    if received_at < closing:
        raise ValueError(f"FMP receipt for {proxy} precedes the ending session close")
    by_day = {}
    for row in input_rows(inputs, f"{side}_closes"):
        if row.observation_date not in window.session_dates:
            continue
        if (
            row.entity_id != proxy
            or row.metric_id != "close"
            or row.category != "provider"
            or not row.source_record_id
            or row.value is None
            or row.value <= 0
            or row.context.unit != "price"
            or row.context.basis != PRICE_BASIS
            or any(stamp > received_at for stamp in (row.published_at, row.vintage_at) if stamp is not None)
            or row.context.currency != "USD"
            or row.context.scale != 0
        ):
            raise ValueError(f"Invalid FMP close for {proxy} on {row.observation_date}")
        if row.observation_date in by_day:
            raise ValueError(f"Ambiguous FMP close for {proxy} on {row.observation_date}")
        by_day[row.observation_date] = row
    for day in window.session_dates:
        if day not in by_day:
            raise ValueError(f"Missing FMP close for {proxy} on {day}")
    return PriceWindow(window, proxy, tuple(by_day[day] for day in window.session_dates))
