"""Compare actual API quantities with the same successful upstream observations."""
import asyncio
import json
import os
from contextlib import contextmanager
from copy import deepcopy
from dataclasses import dataclass, field
from datetime import UTC, date, datetime
from pathlib import Path
from urllib.parse import urlencode

import pytest
from test_runtime import get

ROOT = Path(__file__).resolve().parents[2]
ERROR_CODES = {"authentication", "entitlement", "throttling", "timeout", "upstream",
               "missing_data", "invalid_response", "internal_error", "invalid_parameters"}
OUTCOMES = {"verified", "historical_only", "unverified", "unavailable", "access_blocked",
            "semantically_unsuitable", "failed"}
QUERY_FIELDS = {"provider", "symbol", "query", "period", "limit", "ttm", "start_date",
                "end_date", "interval", "adjustment", "beta", "use_cache"}


class ResearchRequestBlocked(RuntimeError):
    """Deny transport with a stable reason, without retaining remote exception text."""

    def __init__(self, reason):
        self.reason = reason
        super().__init__(reason)


@dataclass
class ResearchRunState:
    """One serial research invocation; baseline captures never receive this state."""

    attempts: int = 0
    blocked_providers: dict[str, str] = field(default_factory=dict)
    enterprise_dates: dict[str, str | None] = field(default_factory=dict)
    blocked_endpoints: dict[tuple[str, str], str] = field(default_factory=dict)
    enterprise_observations: dict[str, dict] = field(default_factory=dict)
    outcomes: dict[str, dict] = field(default_factory=dict)

    def before_request(self, provider, endpoint=None):
        reason = self.blocked_providers.get(provider) or self.blocked_endpoints.get((provider, endpoint))
        if reason:
            raise ResearchRequestBlocked(reason)
        if self.attempts >= 51:
            raise ResearchRequestBlocked("request_ceiling")
        self.attempts += 1

    def block_provider(self, provider, reason):
        require(reason in {"authentication", "throttling"}, "provider stop category")
        self.blocked_providers.setdefault(provider, reason)

    def record_error(self, provider, code, endpoint=None):
        if code in {"authentication", "throttling"}:
            self.block_provider(provider, code)
        elif code == "entitlement" and endpoint:
            self.blocked_endpoints.setdefault((provider, endpoint), code)

    def record_enterprise_date(self, symbol, value, *, listing_id=None, case_id=None, receipt_ref=None):
        try:
            observed = date.fromisoformat(value).isoformat()
        except (TypeError, ValueError):
            self.enterprise_dates.setdefault(symbol, None)
            return
        previous = self.enterprise_observations.get(symbol)
        require(not previous or previous["listing_id"] == listing_id, "same-listing EV observation")
        if not self.enterprise_dates.get(symbol) or observed > self.enterprise_dates[symbol]:
            self.enterprise_dates[symbol] = observed
            self.enterprise_observations[symbol] = {"date": observed, "listing_id": listing_id,
                                                     "case_id": case_id, "receipt_ref": receipt_ref}

    def enterprise_reference(self, symbol, listing_id):
        observation = self.enterprise_observations.get(symbol)
        if observation and listing_id and observation["listing_id"] == listing_id:
            return deepcopy(observation)
        return None

    def record_outcome(self, case_id, status, *, reason=None, missing_proof=None,
                       owner="market-data-integrations", prerequisite=None, query=None):
        require(status in OUTCOMES, "research outcome category")
        require(case_id not in self.outcomes, "retain original case outcome")
        require(status == "verified" or bool(reason and missing_proof and owner), "missing evidence explanation")
        self.outcomes[case_id] = {"status": status, "reason": reason, "missing_proof": missing_proof,
                                  "owner": owner, "prerequisite": prerequisite, "query": safe_query(query)}


_RESEARCH_STATE = pytest.StashKey[ResearchRunState]()


@pytest.fixture(scope="session")
def research_run_state(request):
    # Fixture aliases create distinct FixtureDefs; the session owns the one budget.
    if _RESEARCH_STATE not in request.session.stash:
        request.session.stash[_RESEARCH_STATE] = ResearchRunState()
    return request.session.stash[_RESEARCH_STATE]


def require(condition, check):
    if not condition:
        pytest.fail(check, pytrace=False)


def equal(actual, expected, check):
    if isinstance(expected, (int, float)) and not isinstance(expected, bool):
        require(isinstance(actual, (int, float)) and not isinstance(actual, bool), check)
    require(actual == expected, check)


class SourceCapture:
    """Observe successful callback output without changing it or keeping signed URLs."""

    def __init__(self, monkeypatch, provider, run_state=None, *, endpoint=None, kind="native_api"):
        from openbb_core.provider.utils import helpers

        self.provider = provider
        require(kind in {"native_api", "direct_provider"}, "evidence integration kind")
        require(not run_state or bool(endpoint), "research endpoint branch required")
        self.run_state, self.endpoint, self.kind = run_state, endpoint, kind
        self.receipts = []
        self.started = datetime.now(UTC)
        self.attempts = 0
        original = helpers.amake_request

        async def request(*args, **kwargs):
            budget = 2 if provider == "fred" and kind == "native_api" else 1
            require(self.attempts < budget, "network budget exceeded")
            if run_state:
                run_state.before_request(provider, endpoint)
            self.attempts += 1
            attempt_receipt = {"status": None, "received_at": None}
            if run_state:
                self.receipts.append(attempt_receipt)
            callback = kwargs["response_callback"]

            async def observe(response, session):
                receipt = attempt_receipt if run_state else {}
                receipt.update(status=response.status, received_at=datetime.now(UTC).isoformat())
                if not run_state:
                    self.receipts.append(receipt)
                code = {401: "authentication", 403: "entitlement", 429: "throttling"}.get(response.status)
                if run_state and code:
                    run_state.record_error(provider, code, endpoint)
                    receipt["code"] = code
                payload = await callback(response, session)
                receipt["payload"] = deepcopy(payload)
                return payload

            kwargs["response_callback"] = observe
            if not run_state:
                kwargs.setdefault("timeout", 15)
                return await original(*args, **kwargs)
            kwargs["timeout"] = 15
            try:
                return await asyncio.wait_for(original(*args, **kwargs), timeout=15)
            except Exception as error:  # noqa: BLE001 - Only stable codes survive the observer.
                code = error_code(error)
                if code == "uncategorized" and attempt_receipt.get("code") in ERROR_CODES:
                    code = attempt_receipt["code"]
                attempt_receipt["code"] = code
                run_state.record_error(provider, code, endpoint)
                raise

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
def evidence(case, capture, *, query=None):
    record = {"status": None, "common": None, "comparisons": [], "observation": None}
    try:
        yield record
    except (Exception, pytest.fail.Exception) as error:  # noqa: BLE001 - Discard unsafe provider/validation exception text.
        failure = error_code(error)
        if failure == "uncategorized":
            failure = next((receipt["code"] for receipt in capture.receipts
                            if receipt.get("code") in ERROR_CODES), failure)
        failure = failure if failure != "uncategorized" else "acceptance validation error"
        write_evidence(case, capture, record["status"], record["common"], record["comparisons"], failure,
                       query=query, observation=record["observation"])
        pytest.fail(failure, pytrace=False)
    else:
        write_evidence(case, capture, record["status"], record["common"], record["comparisons"],
                       query=query, observation=record["observation"])


def success(status, body, provider, *, run_state=None, endpoint=None):
    if status == 200:
        return
    code = body.get("code")
    code = code if code in ERROR_CODES else "uncategorized"
    if run_state:
        run_state.record_error(provider.lower(), code, endpoint)
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
    used = set()
    for row in rows:
        candidates = [(ordinal, raw) for ordinal, raw in enumerate(source_rows) if ordinal not in used]
        if date_field:
            candidates = [(ordinal, raw) for ordinal, raw in candidates
                          if serialized_date(raw.get("date")) == serialized_date(row.get(date_field))]
        if row.get("symbol"):
            candidates = [(ordinal, raw) for ordinal, raw in candidates
                          if "symbol" not in raw or raw["symbol"] == row["symbol"]]
        require(bool(candidates), "source observation identity/date")
        ordinal, raw = candidates[0]
        used.add(ordinal)
        for field, source in mapping.items():
            aliases = {"calendarYear": ("fiscalYear", "calendarYear"),
                       "fiscalYear": ("fiscalYear", "calendarYear"),
                       "fillingDate": ("filingDate", "fillingDate"),
                       "filingDate": ("filingDate", "fillingDate")}
            source = next((key for key in aliases.get(source, (source,)) if key in raw), source)
            expected = raw.get(source)
            normalized, rule = ((expected, None) if row.get(field) == expected
                                else normalized_value(field, expected))
            if rule == "integer_fiscal_year":
                require(type(row.get(field)) is int, "integer fiscal-year normalization")
            equal(row.get(field), normalized, "source/API field " + field)
            compared.append({"field": field, "source_field": source, "value": expected,
                             "source_state": "absent" if source not in raw else "null" if expected is None else "value",
                             "api_present": field in row, "source_ordinal": ordinal,
                             "normalization": rule, "date": raw.get("date"), "symbol": raw.get("symbol")})
    return compared


def serialized_date(value):
    return value.isoformat() if isinstance(value, (date, datetime)) else value


def normalized_value(field, value):
    if field == "fiscal_year" and isinstance(value, str) and len(value) == 4 and value.isdecimal():
        return int(value), "integer_fiscal_year"
    if isinstance(value, (date, datetime)):
        return value.isoformat(), "iso_date_serialization"
    return value, None


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


def error_code(error):
    """Inspect typed categories only; never stringify remote exceptions."""
    from openbb_core.provider.utils.financial_errors import FinancialError

    if isinstance(error, ResearchRequestBlocked):
        return error.reason
    if isinstance(error, TimeoutError):
        return "timeout"
    if isinstance(error, FinancialError):
        return error.code.value
    return "uncategorized"


def safe_query(parameters):
    return safe_evidence({key: value for key, value in (parameters or {}).items() if key in QUERY_FIELDS})


def safe_evidence(value):
    """Discard private transport/account fields even if attached to a selected observation."""
    if isinstance(value, dict):
        forbidden = ("key", "token", "secret", "password", "authorization", "cookie", "header", "url")
        # Accounting field names carry financial meaning; account identity uses explicit keys.
        private_accounts = {"account", "accounts", "accountid", "accountids", "accountidentifier",
                            "accountidentifiers", "accountnumber", "accountnumbers", "accountname",
                            "accountemail", "accountholder", "accountowner", "accountdetails",
                            "accountidentity", "provideraccount", "brokerageaccount", "privateaccount"}
        return {key: safe_evidence(item) for key, item in value.items()
                if key.lower().replace("_", "") not in private_accounts
                and not any(part in key.lower().replace("_", "") for part in forbidden)}
    if isinstance(value, (list, tuple)):
        return [safe_evidence(item) for item in value]
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    if isinstance(value, str):
        secrets = [os.environ.get(name) for name in ("FMP_API_KEY", "FRED_API_KEY")]
        if "://" in value or any(secret and secret in value for secret in secrets):
            return "[redacted]"
    return value


def write_evidence(case, capture, status, common=None, comparisons=None, failure=None, *, query=None, observation=None):
    """Export selected source values only; raw remote error text never becomes evidence."""
    output = Path(os.environ.get("QOPENBB_LIVE_EVIDENCE_DIR", ROOT / "artifacts/live-financial-checks/run"))
    output.mkdir(parents=True, exist_ok=True)
    require(bool(case) and all(character.isalnum() or character in "-_" for character in case), "safe evidence case ID")
    document = {"case": case, "kind": capture.kind, "provider": capture.provider, "http_status": status,
                "query": safe_query(query), "retrieved_at": datetime.now(UTC).isoformat(),
                "source_receipts": [{key: value for key, value in receipt.items() if key in {"status", "received_at", "code"}}
                                    for receipt in capture.receipts],
                "comparisons": comparisons or [],
                "failure": failure if failure in ERROR_CODES | {"request_ceiling", "acceptance validation error"} else
                "acceptance validation error" if failure else None}
    if capture.kind == "native_api":
        document["financial_metadata"] = common
        if not capture.run_state:
            document["peer_set_basis"] = "Illustrative MSFT/AAPL/GOOGL listings; no curated valuation comparables."
    else:
        document["observation"] = observation
    if capture.run_state:
        document["run_attempts"] = capture.run_state.attempts
        document["endpoint"] = capture.endpoint
        document["case_outcome"] = capture.run_state.outcomes.get(case)
    text = json.dumps(safe_evidence(document), indent=2, allow_nan=False)
    # Success payloads may carry public company URLs; selected values avoid those fields.
    for name in ("FMP_API_KEY", "FRED_API_KEY"):
        secret = os.environ.get(name)
        require(not secret or secret not in text, "credential-free evidence")
    # Research evidence is immutable within a run, including a failed observation.
    with (output / (case + ".json")).open("x" if capture.run_state else "w", encoding="utf-8") as stream:
        stream.write(text + "\n")
