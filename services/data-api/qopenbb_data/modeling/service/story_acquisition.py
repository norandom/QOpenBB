"""Acquire retrieved price histories and DFII10 context for the story schedule."""

from collections.abc import Callable
from datetime import UTC, datetime, time, timedelta
from decimal import Decimal, InvalidOperation
from uuid import uuid4
from zoneinfo import ZoneInfo

from ..contracts import AssumptionSet, EvaluationCutoff, InputSnapshot, Observation, ObservationTable
from ..contracts.common import parse_financial_date
from ..contracts.inputs import FinancialContext, SourceProvenance
from ..models.factors.sessions import PRICE_BASIS
from .acquisition import AcquisitionError, _fred_row, _object
from .acquisition_http import FredHistoryEmpty
from .ports import AcquisitionRequest
from .story_schedule import CALENDAR_ID, story_sessions

_PAIR = "story.etf_pair"
_YIELD = "story.dfii10"
_STORY_METHODS = {("proxy_comparison", "2"): _PAIR, ("real_yield_regime", "1"): _YIELD}
_ROUTE = "/api/v1/equity/price/historical"
_CALENDAR_KEYS = {"calendar_id", "schedule_revision"}
_PAIR_KEYS = _CALENDAR_KEYS | {"left_proxy", "right_proxy"}
_ZONE = "America/New_York"
_FRED_ROUTE = "/api/v1/economy/fred_series"
_YIELD_CONTEXT = FinancialContext(
    unit="percent", quantity="rate", basis="treasury_constant_maturity", frequency="Daily",
    vintage_coverage="unavailable",
    vintage_limitation="The current FRED response does not establish cutoff-eligible historical availability.",
)
# Listing qualification establishes USD for each admitted ETF. The route reports currency/share.
_PRICE = FinancialContext(unit="price", basis=PRICE_BASIS, currency="USD", vintage_coverage="unknown")


def _parameters(request: AcquisitionRequest) -> dict[str, str]:
    pair = request.dataset_id == _PAIR
    keys = _PAIR_KEYS if pair else _CALENDAR_KEYS
    params = dict(request.parameters)
    if len(request.parameters) != len(keys) or params.keys() != keys:
        raise AcquisitionError("invalid_request")
    if pair and (params["left_proxy"] not in {"DBC", "GLD"} or params["right_proxy"] not in {"XLK", "VGT"}):
        raise AcquisitionError("invalid_request")
    cutoff = request.cutoff
    local_decision = cutoff.decision_at.astimezone(ZoneInfo(_ZONE))
    # The wire accepts the final local second at client timestamp precision.
    if (params["calendar_id"] != CALENDAR_ID or cutoff.session_timezone != _ZONE
            or local_decision.time().replace(microsecond=0) != time(23, 59, 59)
            or cutoff.evaluated_at < cutoff.decision_at):
        raise AcquisitionError("invalid_request")
    return params


def validate_story_binding(
    key: tuple[str, str], request: AcquisitionRequest, assumptions: AssumptionSet, *,
    story_calendar: Callable[[EvaluationCutoff, str, str], None] | None = None,
) -> None:
    """Bind the two story datasets to their exact installed method and selection."""
    expected_dataset = _STORY_METHODS.get(key)
    if expected_dataset is None and request.dataset_id not in (_PAIR, _YIELD):
        return
    if request.dataset_id != expected_dataset:
        raise AcquisitionError("invalid_request")
    params = _parameters(request)
    expected = params
    if expected_dataset == _PAIR:
        expected = params | {
            "price_basis": PRICE_BASIS, "leg_methods": "etf_momentum@1, etf_realized_volatility@1",
            "left_calendar": CALENDAR_ID, "right_calendar": CALENDAR_ID,
        }
    actual = {item.assumption_id: item.value for item in assumptions.assumptions if item.value_type == "text"}
    if (actual != expected or len(assumptions.assumptions) != len(expected)
            or assumptions.version != "1" or assumptions.effective_date > request.cutoff.observation_date):
        raise AcquisitionError("invalid_request")
    if story_calendar is None:
        _schedule(request.cutoff, params)
    else:
        try:
            story_calendar(request.cutoff, params["calendar_id"], params["schedule_revision"])
        except ValueError:
            raise AcquisitionError("invalid_request") from None


def _receipt_time(meta, earliest):
    stamp = meta["retrieved_at"]
    when = datetime.fromisoformat(stamp)
    if ("T" not in stamp or when.utcoffset() != timedelta(0) or when > datetime.now(UTC)
            or when < earliest):
        raise ValueError("Invalid provider receipt timestamp.")
    return when


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
    return _receipt_time(meta, earliest)


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
    sessions = _schedule(cutoff, params)
    # A closed day has no scheduled ending session. Request a bounded history to
    # retain real receipts while leaving the empty schedule for the model to diagnose.
    start = min((row.observation_date for row in sessions.rows),
                default=cutoff.observation_date - timedelta(days=7))
    query = {"dataset_id": _PAIR, **params}
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


def _schedule(cutoff, params):
    try:
        return story_sessions(cutoff, params["calendar_id"], params["schedule_revision"])
    except ValueError:
        raise AcquisitionError("invalid_request") from None


def _yield_receipt(payload, query, count, earliest):
    meta = payload["extra"]["results_metadata"]["__qopenbb_financial__"]
    field = meta["fields"]["DFII10"]
    bounds = meta["bounds"]
    # The producer emits FRED-native aliases alongside the requested symbol.
    expected = {
        "symbol": query["symbol"], "series_id": query["symbol"],
        "observation_start": query["start_date"], "observation_end": query["end_date"],
    }
    used = _object(meta["effective_query"])
    if (payload.get("provider") != "fred" or meta["provider"] != "fred"
            or meta["dataset"] != "economy.fred_series"
            or meta["source"]["endpoint"] != "series/observations"
            or meta["point_in_time_safe"] is not False or meta.get("vintage_query_supported") is not None
            or any(used.get(key) != value for key, value in expected.items())
            or any(key in used and used[key] != query[key] for key in ("start_date", "end_date"))
            or used["use_cache"] is not False
            or any(used.get(key) is not None for key in ("units", "transform", "frequency"))
            or meta["transformations"] != []
            or not isinstance(bounds["returned_count"], Decimal) or bounds["returned_count"] != count
            or (bounds.get("truncated") is not None and bounds["truncated"] is not False)
            or field["unit"] != "Percent" or field["source_unit"] != "Percent"
            or field["source_frequency"] != "Daily" or field["effective_frequency"] != "Daily"
            or field["source"] != "fred" or field["observation_date_field"] != "date"
            or any(field.get(key) is not None for key in ("scale", "currency", "requested_transform", "aggregation"))
            or field["value_origin"] != "provider_observation"):
        raise ValueError("Unexpected FRED series metadata.")
    return _receipt_time(meta, earliest), _object(meta.get("observation_provenance", {}))


def _yield_snapshot(payload, request, sessions, query, start, checkpoint):
    results = payload["results"]
    end = request.cutoff.observation_date
    if not isinstance(results, list) or len(results) > (end - start).days + 1:
        raise ValueError("Invalid DFII10 rows.")
    earliest = datetime.combine(end, time.min, ZoneInfo(request.cutoff.session_timezone))
    when, realtime = _yield_receipt(payload, query, len(results), earliest)
    realtime = _object(realtime.get("DFII10", {}))
    acquisition_id = uuid4().hex
    rows = []
    for raw in results:
        checkpoint()
        row = _fred_row(raw, "DFII10", request, _YIELD_CONTEXT, realtime, acquisition_id, metric_id="real_yield")
        if row.observation_date < start:
            raise ValueError("Unexpected DFII10 observation date.")
        rows.append(row)
    checkpoint()
    return _yield_evidence(request, sessions, query, when, acquisition_id, tuple(rows))


def _yield_evidence(request, sessions, query, when, acquisition_id, rows):
    table = ObservationTable(
        table_id="dfii10", keys=("entity_id", "observation_date"),
        grain="One current DFII10 observation per FRED observation date.", nullable=True, rows=rows,
    )
    provenance = SourceProvenance(
        origin="service_acquired", source="fred", acquisition_id=acquisition_id, retrieved_at=when,
        query=tuple(({"dataset_id": request.dataset_id, **dict(request.parameters), **query}).items()),
    )
    return InputSnapshot(schema_id="real_yield_regime.inputs", cutoff=request.cutoff,
                         tables=(sessions, table), provenance=provenance)


async def acquire_real_yield(request, read, decode, checkpoint):
    cutoff = request.cutoff
    sessions = _schedule(cutoff, _parameters(request))
    end = cutoff.observation_date
    start = sessions.rows[0].observation_date if sessions.rows else end - timedelta(days=7)
    query = {"provider": "fred", "symbol": "DFII10", "start_date": start.isoformat(),
             "end_date": end.isoformat(), "use_cache": "false"}
    try:
        body = await read(_FRED_ROUTE, tuple(query.items()))
    except FredHistoryEmpty:
        checkpoint()
        # The empty HTTP response carries no timestamp from the provider.
        query |= {"receipt_basis": "service_received_at", "source_outcome": "missing_data"}
        return _yield_evidence(request, sessions, query, datetime.now(UTC), uuid4().hex, ())
    except OSError as error:
        code = getattr(error, "code", None)
        failure = code if code in {"entitlement", "timeout", "throttling"} else "upstream"
    else:
        try:
            return _yield_snapshot(decode(body, checkpoint), request, sessions, query, start, checkpoint)
        except (KeyError, AttributeError, TypeError, ValueError, InvalidOperation, RecursionError):
            failure = "invalid_response"
    raise AcquisitionError(failure)
