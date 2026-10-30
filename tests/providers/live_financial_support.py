"""Compare actual API quantities with the same successful upstream observations."""
import asyncio
import json
import os
from contextlib import contextmanager
from copy import deepcopy
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import urlencode

import pytest
from test_runtime import get

ROOT = Path(__file__).resolve().parents[2]


def require(condition, check):
    if not condition:
        pytest.fail(check, pytrace=False)


def equal(actual, expected, check):
    if isinstance(expected, (int, float)) and not isinstance(expected, bool):
        require(isinstance(actual, (int, float)) and not isinstance(actual, bool), check)
    require(actual == expected, check)


class SourceCapture:
    """Observe successful callback output without changing it or keeping signed URLs."""

    def __init__(self, monkeypatch, provider):
        from openbb_core.provider.utils import helpers

        self.provider = provider
        self.receipts = []
        self.started = datetime.now(UTC)
        self.attempts = 0
        original = helpers.amake_request

        async def request(*args, **kwargs):
            self.attempts += 1
            require(self.attempts <= (2 if provider == "fred" else 1), "network budget exceeded")
            callback = kwargs["response_callback"]

            async def observe(response, session):
                receipt = {"status": response.status, "received_at": datetime.now(UTC).isoformat()}
                self.receipts.append(receipt)
                payload = await callback(response, session)
                receipt["payload"] = deepcopy(payload)
                return payload

            kwargs["response_callback"] = observe
            kwargs.setdefault("timeout", 15)
            return await original(*args, **kwargs)

        monkeypatch.setattr(helpers, "amake_request", request)

    def source_rows(self):
        require(len(self.receipts) == 1, "one FMP source receipt required")
        payload = self.receipts[0].get("payload")
        if isinstance(payload, dict):
            payload = payload.get("historical")
        require(isinstance(payload, list) and bool(payload), "actual nonempty FMP observations required")
        return payload


def call(app, path, parameters):
    status, raw = asyncio.run(get(app, path, urlencode(parameters).encode(), raw=True))
    try:
        body = json.loads(raw) if raw else {}
    except (TypeError, ValueError):
        pytest.fail("API did not return JSON", pytrace=False)
    require(isinstance(body, dict), "API result envelope")
    return status, body


@contextmanager
def evidence(case, capture):
    record = {"status": None, "common": None, "comparisons": []}
    try:
        yield record
    except (Exception, pytest.fail.Exception) as error:  # noqa: BLE001 - Discard unsafe provider/validation exception text.
        failure = str(error) if type(error) is pytest.fail.Exception else "acceptance validation error"
        write_evidence(case, capture, record["status"], record["common"], record["comparisons"], failure)
        pytest.fail(failure, pytrace=False)
    else:
        write_evidence(case, capture, record["status"], record["common"], record["comparisons"])


def success(status, body, provider):
    if status == 200:
        return
    known = {"authentication", "entitlement", "throttling", "timeout", "upstream", "missing_data", "invalid_response"}
    code = body.get("code")
    code = code if code in known else "uncategorized"
    pytest.fail("required " + provider + " endpoint blocked: " + code, pytrace=False)


def metadata(body, capture, parameters):
    from openbb_core.provider.standard_models.financial_metadata import (
        FinancialResultMetadata,
    )

    result = body["extra"]["results_metadata"]["__qopenbb_financial__"]
    parsed = FinancialResultMetadata.model_validate(result)
    require(parsed.provider == capture.provider, "selected provider provenance")
    require(capture.started <= parsed.retrieved_at <= datetime.now(UTC), "actual UTC acquisition time")
    require(parsed.bounds.returned_count == len(body["results"]), "returned-count provenance")
    require(not parsed.point_in_time_safe and parsed.vintage_query_supported is None, "unknown vintage safety")
    require(bool(parsed.source.endpoint) and bool(parsed.limitations), "endpoint and limitations")
    for name, value in parameters.items():
        if name != "provider":
            key = {"start_date": "observation_start", "end_date": "observation_end"}.get(name, name) if capture.provider == "fred" else name
            equal(parsed.effective_query.get(key), value, "effective query " + name)
    require(all(field.definition for field in parsed.fields.values()), "field definitions")
    return result


def validate_rows(app, path, provider, body):
    from openbb_core.provider.registry_map import RegistryMap
    from pydantic import TypeAdapter

    descriptor = app.openapi()["paths"][path]["get"]["x-qopenbb-financial"]
    model = RegistryMap().original_models[descriptor["dataset"]][provider]["data"]
    # Validation receives a copy because native models may normalize numeric fields.
    TypeAdapter(list[model]).validate_python(deepcopy(body["results"]))


def pairs(rows, source_rows, mapping, date_field=None):
    compared = []
    for index, row in enumerate(rows):
        candidates = source_rows
        if date_field:
            candidates = [raw for raw in candidates if raw.get("date") == row.get(date_field)]
        elif row.get("symbol"):
            candidates = [raw for raw in candidates if raw.get("symbol") == row["symbol"]]
        require(bool(candidates), "source observation identity/date")
        raw = candidates[0] if date_field or row.get("symbol") else candidates[index]
        for field, source in mapping.items():
            expected = raw.get(source)
            equal(row.get(field), expected, "source/API field " + field)
            compared.append({"field": field, "source_field": source, "value": expected,
                             "date": raw.get("date"), "symbol": raw.get("symbol")})
    return compared


def unit(common, field, unit, origin=None, basis=None):
    details = common["fields"][field]
    equal(details["unit"], unit, "financial unit " + field)
    equal(details["scale"], 1, "financial scale " + field)
    if origin:
        equal(details["value_origin"], origin, "value origin " + field)
    if basis:
        equal(details["period_basis"], basis, "period basis " + field)


def unknown_valuation_bases(common, field):
    bases = common["fields"][field]["financial_basis"]
    require(set(bases) == {"share_count", "debt", "cash", "lease", "minority_interest",
                           "forecast_period", "market_date"}, "declared valuation input bases")
    require(all(value is None for value in bases.values()), "unknown valuation conventions retained")


def write_evidence(case, capture, status, common=None, comparisons=None, failure=None):
    """Export selected source values only; raw remote error text never becomes evidence."""
    output = Path(os.environ.get("QOPENBB_LIVE_EVIDENCE_DIR", ROOT / "artifacts/live-financial-checks/run"))
    output.mkdir(parents=True, exist_ok=True)
    document = {"case": case, "provider": capture.provider, "http_status": status,
                "source_receipts": [{key: value for key, value in receipt.items() if key != "payload"}
                                    for receipt in capture.receipts],
                "comparisons": comparisons or [], "financial_metadata": common,
                "failure": failure, "peer_set_basis": "Illustrative MSFT/AAPL/GOOGL listings; no curated valuation comparables."}
    text = json.dumps(document, indent=2, allow_nan=False)
    # Success payloads may carry public company URLs; selected values avoid those fields.
    for name in ("FMP_API_KEY", "FRED_API_KEY"):
        secret = os.environ.get(name)
        require(not secret or secret not in text, "credential-free evidence")
    (output / (case + ".json")).write_text(text + "\n", encoding="utf-8")
