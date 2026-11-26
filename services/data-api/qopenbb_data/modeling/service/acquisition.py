"""Map allowlisted data API responses to model input snapshots."""

import asyncio
import json
import math
import re
from collections.abc import Awaitable, Callable
from datetime import UTC, datetime
from decimal import Decimal, InvalidOperation
from functools import partial
from threading import Event
from time import monotonic
from typing import Literal
from urllib.parse import urlsplit
from uuid import uuid4

from ..contracts import InputSnapshot, Observation, ObservationTable
from ..contracts.common import parse_financial_date
from ..contracts.inputs import FinancialContext, SourceProvenance, Transformation
from .acquisition_http import MAX_RESPONSE_BYTES, fetch
from .ports import AcquisitionRequest

Transport = Callable[[str, tuple[tuple[str, str], ...]], Awaitable[bytes]]
ErrorCode = Literal["invalid_request", "invalid_response", "missing_data", "timeout", "cancelled", "upstream", "entitlement"]

_DATASET = "economy.fred_series"
_ROUTE = "/api/v1/economy/fred_series"
_MAX_OBSERVATIONS = 10_000
_VINTAGE_LIMITATION = "Current observations lack publication and verified historical vintage timestamps."
_TRANSFORMATIONS = (
    Transformation(
        transformation_id="fred.wide_to_observations",
        version="1",
        description=(
            "Map the selected series column and date to one observation per date. "
            "Decode JSON numbers as decimals and preserve nulls and provider units."
        ),
    ),
)


class AcquisitionError(RuntimeError):
    """A failure category safe to expose at the service boundary."""

    def __init__(self, code: ErrorCode):
        self.code = code
        super().__init__({
            "invalid_request": "Unsupported data acquisition request.",
            "invalid_response": "Data API returned an invalid response.",
            "missing_data": "Data API returned no observations.",
            "entitlement": "Data API denied access to the dataset.",
            "timeout": "Data acquisition deadline exceeded.",
            "cancelled": "Data acquisition cancelled.",
            "upstream": "Data API request failed.",
        }[code])


class DataApiSnapshotSource:
    """Acquire economic observations from a configured data API origin."""

    def __init__(
        self, base_url: str, *, timeout_seconds: float = 30, transport: Transport | None = None
    ) -> None:
        if not _valid_origin(base_url):
            raise ValueError("Configure an HTTP or HTTPS data API origin.")
        if not math.isfinite(timeout_seconds) or not 0 < timeout_seconds <= 30:
            raise ValueError("Set the acquisition timeout above zero and at most 30 seconds.")
        self._origin = base_url.rstrip("/")
        self._timeout_seconds = timeout_seconds
        self._transport = transport if transport is not None else fetch

    def acquire(
        self, request: AcquisitionRequest, *, deadline: float | None = None, cancel: Event | None = None,
    ) -> InputSnapshot:
        """Acquire synchronously. Async service callers should use a worker thread."""
        local_deadline = monotonic() + self._timeout_seconds
        if deadline is not None:
            if not math.isfinite(deadline):
                raise AcquisitionError("invalid_request")
            local_deadline = min(deadline, local_deadline)
        _remaining(local_deadline, cancel)
        return asyncio.run(self._acquire(request, local_deadline, cancel))

    async def _acquire(
        self, request: AcquisitionRequest, deadline: float, cancel: Event | None,
    ) -> InputSnapshot:
        try:
            async with asyncio.timeout(_remaining(deadline, cancel)):
                if request.dataset_id == "story.etf_pair":
                    from .story_acquisition import acquire_story

                    return await acquire_story(
                        request, partial(self._read_response, cancel), _decode_response,
                        partial(_remaining, deadline, cancel),
                    )
                params = _fred_query(request)
                body = await self._read_response(cancel, _ROUTE, params)
                _remaining(deadline, cancel)
                retrieved_at = datetime.now(UTC)
                snapshot = _fred_snapshot(
                    body, request, params, retrieved_at, partial(_remaining, deadline, cancel),
                )
                _remaining(deadline, cancel)
                return snapshot
        except TimeoutError:
            failure = "timeout"
        except LookupError:
            failure = "missing_data"
        except (TypeError, ValueError, InvalidOperation, RecursionError):
            failure = "invalid_response"
        except OSError:
            failure = "upstream"
        raise AcquisitionError(failure)

    async def _read_response(
        self, cancel: Event | None, route: str, params: tuple[tuple[str, str], ...],
    ) -> bytes:
        if cancel is None:
            return await self._transport(self._origin + route, params)

        # Poll the thread event without leaving a blocked executor thread on timeout.
        task = asyncio.ensure_future(self._transport(self._origin + route, params))
        try:
            while not cancel.is_set():
                done, _ = await asyncio.wait((task,), timeout=0.05)
                if done and not cancel.is_set():
                    return task.result()
            raise AcquisitionError("cancelled")
        finally:
            task.cancel()
            await asyncio.gather(task, return_exceptions=True)


def _remaining(deadline: float, cancel: Event | None) -> float:
    if cancel is not None and cancel.is_set():
        raise AcquisitionError("cancelled")
    remaining = deadline - monotonic()
    if remaining <= 0:
        raise AcquisitionError("timeout")
    return remaining


def _valid_origin(base_url: str) -> bool:
    if re.search(r"[\s\\?#\x00-\x1f\x7f]", base_url):
        return False
    try:
        url = urlsplit(base_url)
        port = url.port
    except ValueError:
        return False
    return (
        url.scheme in {"http", "https"}
        and bool(url.hostname)
        and url.username is None
        and url.path in {"", "/"}
        and (port is None or port > 0)
    )


def _fred_query(request: AcquisitionRequest) -> tuple[tuple[str, str], ...]:
    if request.dataset_id != _DATASET or len(request.parameters) != 1:
        raise AcquisitionError("invalid_request")
    name, symbol = request.parameters[0]
    if (
        name != "symbol"
        or not re.fullmatch(r"[A-Za-z0-9_][-A-Za-z0-9_]{0,127}", symbol)
        or symbol.upper() in {"DATE", "__QOPENBB_FINANCIAL__"}
    ):
        raise AcquisitionError("invalid_request")
    return (
        ("provider", "fred"),
        ("symbol", symbol.upper()),
        ("end_date", request.cutoff.observation_date.isoformat()),
        ("use_cache", "false"),
    )


def _decode_response(body: bytes, checkpoint: Callable[[], float]) -> dict:
    if not isinstance(body, bytes):
        raise TypeError("Expected a JSON response body.")
    if len(body) > MAX_RESPONSE_BYTES:
        raise ValueError("Response exceeds the byte limit.")

    def number(token: str) -> Decimal:
        checkpoint()
        if len(token) > 128:
            raise ValueError("Response number exceeds the token limit.")
        return Decimal(token)

    def object_pairs(pairs: list[tuple[str, object]]) -> dict:
        checkpoint()
        obj = {}
        for index, (key, value) in enumerate(pairs):
            if index % 128 == 0:
                checkpoint()
            if key in obj:
                raise ValueError("Duplicate response property.")
            obj[key] = value
        return obj

    checkpoint()
    payload = json.loads(
        body, parse_float=number, parse_int=number, parse_constant=number,
        object_pairs_hook=object_pairs,
    )
    checkpoint()
    return _object(payload)


def _object(value: object) -> dict:
    if not isinstance(value, dict):
        raise TypeError("Expected a response object.")
    return value


def _fred_snapshot(
    body: bytes,
    request: AcquisitionRequest,
    params: tuple[tuple[str, str], ...],
    retrieved_at: datetime,
    checkpoint: Callable[[], float],
) -> InputSnapshot:
    payload = _decode_response(body, checkpoint)
    results = payload.get("results")
    if payload.get("provider") != "fred" or not isinstance(results, list) or len(results) > _MAX_OBSERVATIONS:
        raise ValueError("Invalid FRED result envelope.")
    if not results:
        raise LookupError
    symbol = dict(params)["symbol"]
    metadata = _object(_object(payload.get("extra", {})).get("results_metadata", {}))
    series = _object(metadata.get(symbol, {}))
    units = series.get("units")
    context = FinancialContext(
        unit=units if units is not None else "unknown",
        frequency=series.get("frequency"),
        seasonal_adjustment=series.get("seasonal_adjustment"),
        vintage_coverage="unavailable",
        vintage_limitation=_VINTAGE_LIMITATION,
    )
    financial_metadata = _object(metadata.get("__qopenbb_financial__", {}))
    provenance = _object(financial_metadata.get("observation_provenance", {}))
    realtime_by_date = _object(provenance.get(symbol, {}))
    acquisition_id = uuid4().hex
    checkpoint()
    table = ObservationTable(
        table_id=_DATASET,
        grain="One provider observation per series and observation date.",
        keys=("entity_id", "metric_id", "observation_date"),
        nullable=True,
        rows=(),
    )
    snapshot = InputSnapshot(
        schema_id=_DATASET,
        provenance=SourceProvenance(
            origin="service_acquired",
            source="fred",
            query=params,
            retrieved_at=retrieved_at,
            acquisition_id=acquisition_id,
        ),
        tables=(table,),
        cutoff=request.cutoff,
    )
    rows = []
    dates = set()
    for raw_row in results:
        checkpoint()
        row = _fred_row(raw_row, symbol, request, context, realtime_by_date, acquisition_id)
        if row.observation_date in dates:
            raise ValueError("Duplicate FRED observation date.")
        dates.add(row.observation_date)
        rows.append(row)
    checkpoint()
    # The validated shell fixes table identity, keys, and nullability. Each row is
    # validated once, and its unique date determines both its key and record ID.
    # The capped envelope supplies the row-count invariant for this single table.
    return snapshot.model_copy(update={"tables": (table.model_copy(update={"rows": tuple(rows)}),)})


def _fred_row(
    row: object,
    symbol: str,
    request: AcquisitionRequest,
    context: FinancialContext,
    realtime_by_date: dict,
    acquisition_id: str,
) -> Observation:
    fields = _object(row)
    if "date" not in fields or symbol not in fields:
        raise ValueError("Missing FRED observation field.")
    observation_date = parse_financial_date(fields["date"])
    value = fields[symbol]
    if observation_date > request.cutoff.observation_date or (
        value is not None and not isinstance(value, Decimal)
    ):
        raise ValueError("Invalid FRED observation.")
    realtime = _object(realtime_by_date.get(observation_date.isoformat(), {}))
    if realtime:
        context = context.model_copy(update={"vintage_limitation": _vintage_limitation(realtime)})
    return Observation(
        record_id=f"fred:{acquisition_id}:{observation_date}",
        entity_id=symbol,
        metric_id=symbol,
        observation_date=observation_date,
        context=context,
        value=value,
        category="provider",
        transformations=_TRANSFORMATIONS,
    )


def _vintage_limitation(realtime: dict) -> str:
    # FRED reports date-only real-time bounds. Assigning a time zone would fabricate availability.
    bounds = [
        f"{label} {parse_financial_date(realtime[key])}"
        for key, label in (("realtime_start", "start"), ("realtime_end", "end"))
        if realtime.get(key) is not None
    ]
    if not bounds:
        return _VINTAGE_LIMITATION
    return f"{_VINTAGE_LIMITATION} FRED real-time bounds report {', '.join(bounds)}."
