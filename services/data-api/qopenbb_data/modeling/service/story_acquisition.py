"""Acquire independently dated price histories for the qualified NYSE Arca ETF roles."""

from datetime import UTC, datetime, time, timedelta
from decimal import Decimal, InvalidOperation
from uuid import uuid4
from zoneinfo import ZoneInfo

from ..contracts import InputSnapshot, Observation, ObservationTable
from ..contracts.common import parse_financial_date
from ..contracts.inputs import FinancialContext, SourceProvenance
from ..models.factors.sessions import PRICE_BASIS
from .acquisition import AcquisitionError
from .story_schedule import CALENDAR_ID, REVISION, story_sessions

_DATASET = "story.etf_pair"
_ROUTE = "/api/v1/equity/price/historical"
_KEYS = {"left_proxy", "right_proxy", "calendar_id", "schedule_revision"}
# Listing qualification establishes USD for each admitted ETF. The route reports currency/share.
_PRICE = FinancialContext(unit="price", basis=PRICE_BASIS, currency="USD", vintage_coverage="unknown")


def _parameters(request, *, installed=True):
    params = dict(request.parameters)
    if (len(request.parameters) != len(_KEYS) or params.keys() != _KEYS
            or params["left_proxy"] not in {"DBC", "GLD"} or params["right_proxy"] not in {"XLK", "VGT"}
            or params["calendar_id"] != CALENDAR_ID or (installed and params["schedule_revision"] != REVISION)
            or request.cutoff.session_timezone != "America/New_York"):
        raise AcquisitionError("invalid_request")
    return params


def validate_story_binding(key, request, assumptions):
    comparison = key == ("proxy_comparison", "2")
    if comparison != (request.dataset_id == _DATASET):
        raise AcquisitionError("invalid_request")
    if comparison:
        expected = _parameters(request, installed=False) | {
            "price_basis": PRICE_BASIS, "leg_methods": "etf_momentum@1, etf_realized_volatility@1",
            "left_calendar": CALENDAR_ID, "right_calendar": CALENDAR_ID,
        }
        actual = {item.assumption_id: item.value for item in assumptions.assumptions if item.value_type == "text"}
        if any(actual.get(k) != v for k, v in expected.items()):
            raise AcquisitionError("invalid_request")


def _receipt(payload, query, count, earliest):
    meta = payload["extra"]["results_metadata"]["__qopenbb_financial__"]
    field = meta["fields"]["close"]
    bounds = meta["bounds"]
    if (payload.get("provider") != "fmp" or meta["provider"] != "fmp"
            or meta["dataset"] != "equity/price/historical"
            or meta["source"]["endpoint"] != "historical-price-eod/full"
            or meta["effective_query"] != query or meta["point_in_time_safe"] is not False
            or not isinstance(bounds["returned_count"], Decimal) or bounds["returned_count"] != count
            or (bounds.get("truncated") is not None and bounds["truncated"] is not False)
            or field["unit"] != "currency/share" or not isinstance(field["scale"], Decimal) or field["scale"] != 1
            or field.get("currency") not in (None, "USD")
            or field["value_origin"] != "provider_observation"):
        raise ValueError("Unexpected FMP history metadata.")
    stamp = meta["retrieved_at"]
    when = datetime.fromisoformat(stamp)
    if ("T" not in stamp or when.utcoffset() != timedelta(0) or when > datetime.now(UTC)
            or when < earliest):
        raise ValueError("Invalid FMP receipt timestamp.")
    return when


def _rows(results, symbol, start, end, checkpoint):
    observations = []
    for raw in results:
        checkpoint()
        day = parse_financial_date(raw["date"])
        if raw.get("symbol", symbol) != symbol or not start <= day <= end:
            raise ValueError("Unexpected FMP observation.")
        value = raw["close"]
        if value is not None and (not isinstance(value, Decimal) or not value.is_finite() or value <= 0):
            raise ValueError("Invalid FMP closing price.")
        identity = f"fmp:{symbol}:{day}:close"
        observations.append(Observation(
            record_id=identity, source_record_id=identity, entity_id=symbol, metric_id="close",
            observation_date=day, context=_PRICE, value=value, category="provider",
        ))
    return tuple(observations)


def _table(side, rows):
    return ObservationTable(table_id=f"{side}_closes", keys=("entity_id", "observation_date"),
                            grain="One retrieved FMP close per ETF and trading date.", nullable=True, rows=rows)


async def _read_leg(side, symbol, start, end, earliest, read, decode, checkpoint):
    query = {"symbol": symbol, "start_date": start.isoformat(), "end_date": end.isoformat(),
             "interval": "1d", "adjustment": "splits_only"}
    try:
        body = await read(_ROUTE, tuple(({"provider": "fmp"} | query).items()))
    except LookupError:
        return _table(side, ()), None, "missing_data"
    except TimeoutError:
        return _table(side, ()), None, "timeout"
    except OSError as exc:
        code = getattr(exc, "code", None)
        failure = code if code in {"entitlement", "missing_data", "timeout", "throttling"} else "upstream"
        return _table(side, ()), None, failure
    except ValueError:
        return _table(side, ()), None, "invalid_response"
    try:
        payload = decode(body, checkpoint)
        results = payload["results"]
        if not isinstance(results, list) or len(results) > 5000:
            raise ValueError("Invalid FMP rows.")
        when = _receipt(payload, query, len(results), earliest)
        rows = _rows(results, symbol, start, end, checkpoint)
        return _table(side, rows), when, None
    except (KeyError, AttributeError, TypeError, ValueError, InvalidOperation, RecursionError):
        return _table(side, ()), None, "invalid_response"


def _earliest_receipt(cutoff, sessions):
    hour = 0
    if sessions.rows:
        hour = 13 if sessions.rows[-1].context.basis == "early_close_1300_eastern" else 16
    return datetime.combine(cutoff.observation_date, time(hour), ZoneInfo(cutoff.session_timezone))


async def acquire_story(request, read, decode, checkpoint):
    params = _parameters(request)
    cutoff = request.cutoff
    try:
        sessions = story_sessions(cutoff, params["calendar_id"], params["schedule_revision"])
    except ValueError:
        raise AcquisitionError("invalid_request") from None
    # A closed day has no scheduled ending session. Request a bounded history to
    # retain real receipts while leaving the empty schedule for the model to diagnose.
    start = min((row.observation_date for row in sessions.rows),
                default=cutoff.observation_date - timedelta(days=7))
    query = {"dataset_id": _DATASET, **params}
    earliest = _earliest_receipt(cutoff, sessions)
    tables, times, failures = [sessions], [], []
    for side in ("left", "right"):
        checkpoint()
        table, when, failure = await _read_leg(
            side, params[f"{side}_proxy"], start, cutoff.observation_date, earliest, read, decode, checkpoint,
        )
        tables.append(table)
        if when is not None:
            times.append(when)
            query[f"{side}_retrieved_at"] = when.isoformat()
        if failure:
            failures.append(failure)
            query[f"{side}_error"] = failure
    checkpoint()
    if not times:
        if all(code == "timeout" for code in failures):
            raise AcquisitionError("timeout")
        if all(code == "entitlement" for code in failures):
            raise AcquisitionError("entitlement")
        if all(code == "missing_data" for code in failures):
            raise AcquisitionError("missing_data")
        raise AcquisitionError("invalid_response" if "invalid_response" in failures else "upstream")
    return InputSnapshot(schema_id="proxy_comparison.inputs", tables=tuple(tables), cutoff=cutoff,
                         provenance=SourceProvenance(origin="service_acquired", source="fmp",
                                                     acquisition_id=uuid4().hex, query=tuple(query.items()),
                                                     retrieved_at=max(times)))
