"""Bounded direct FMP observations; these probes do not accept a native DCF route."""
import asyncio
import json
import math
import os
import socket
from urllib.parse import parse_qs, urlencode, urlsplit

import pytest
from live_financial_support import (
    ResearchRunState,
    SourceCapture,
    error_code,
    research_run_state,
    write_evidence,
)

DOCUMENTATION_CHECKED = "2026-11-06"
CUSTOM_PARAMETER = {"documented": True, "name": "beta", "value": 1.0, "unit": "dimensionless"}
PROBES = (
    ("dcf-standard", "dcf", "discounted-cash-flow", "dcf-advanced"),
    ("dcf-custom-defaults", "custom_dcf", "custom-discounted-cash-flow", "custom-dcf-advanced"),
    ("dcf-custom-beta", "custom_dcf", "custom-discounted-cash-flow", "custom-dcf-advanced"),
)
ASSUMPTION_FIELDS = (
    "beta", "wacc", "riskFreeRate", "marketRiskPremium", "costOfEquity", "costOfDebt",
    "taxRate", "longTermGrowthRate", "revenueGrowth", "ebitdaPercentage", "ebitPercentage",
    "depreciationAndAmortizationPercentage", "capitalExpenditurePercentage",
    "receivablesPercentage", "inventoriesPercentage", "payablePercentage",
)
DETAIL_FIELDS = ("date", "year", "currency", "reportedCurrency", "symbol", "dcf",
                 "equityValuePerShare", "equityValue", "freeCashFlow", "terminalValue")


def finite_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def forecast_year(value):
    return ((isinstance(value, int) and not isinstance(value, bool) and 1000 <= value <= 9999)
            or (isinstance(value, str) and len(value) == 4 and value.isdecimal()))


def observation_template(document):
    return {
        "source_integration": {
            "native_api": "absent_in_inspected_source", "widget": "absent_in_inspected_source",
            "scope": "current fork and retained openbb_fmp-1.6.1 archive; generic transport exists",
            "direct_transport": "get_data_many",
        },
        "documented_capability": {"status": "documented", "reference": document,
                                  "checked_at": DOCUMENTATION_CHECKED,
                                  "source": "official FMP documentation referenced by approved design",
                                  "design_reference": ".kiro/specs/analyst-workspace/research-input-design.md#dcf-and-macro-feasibility",
                                  "custom_test_parameter": dict(CUSTOM_PARAMETER) if "custom" in document else None},
        "observed_access": {"status": "unverified", "reason": "not_attempted"},
        "assumption_coverage": {"status": "unverified", "fields": [],
                                "missing_model_detail": list(ASSUMPTION_FIELDS)},
        "custom_input_behavior": {"status": "unverified", "reason": "binding_not_tested"},
        "value_origin": "provider_calculation", "valuation_label": "provider_valuation",
        "valuation_date": None, "valuation_date_reason": "provider_date_not_supplied",
        "forecast_years": [], "currency": None, "currency_reason": "dcf_currency_not_supplied",
        "response_fields": [], "observations": [], "provider_acquired_at": None,
        "house_dcf": "unverified", "sensitivity_support": "unverified",
        "consequences": {
            "ia_c": "house method and sensitivity contracts require separate verification",
            "ia_b": "direct DCF availability does not establish native financial input readiness",
            "macro": "DGS10 and provider beta do not establish issuer WACC or borrowing cost",
        },
    }


def inspect_rows(observation, rows, custom):
    from datetime import date

    selected = []
    for row in rows:
        selected.append({field: (None if isinstance(value, float) and not math.isfinite(value) else value)
                         for field, value in row.items() if field in DETAIL_FIELDS + ASSUMPTION_FIELDS
                         and (value is None or isinstance(value, (str, int, float, bool)))})
    observation["observations"] = selected
    observation["response_fields"] = sorted({field for row in rows for field in row
                                             if isinstance(field, str) and field.isidentifier()
                                             and not any(part in field.lower() for part in
                                                         ("key", "token", "secret", "password", "header", "url", "account", "cookie"))})
    assumptions = [field for field in ASSUMPTION_FIELDS if any(row.get(field) is not None for row in selected)]
    observation["assumption_coverage"] = {
        "status": "observed" if assumptions else "unavailable", "fields": assumptions,
        "missing_model_detail": [field for field in ASSUMPTION_FIELDS if field not in assumptions],
        "conventions": "provider fields retained; undocumented units and methodology remain unknown",
    }
    dates = []
    for row in selected:
        try:
            dates.append(date.fromisoformat(row.get("date")).isoformat())
        except (TypeError, ValueError):
            pass
    if dates and len(set(dates)) == 1 and len(dates) == len(selected):
        observation.update(valuation_date=dates[0], valuation_date_reason=None)
    currencies = [row.get("currency") for row in selected]
    if (currencies and all(isinstance(item, str) and len(item) == 3 and item.isalpha() for item in currencies)
            and len(set(currencies)) == 1):
        observation.update(currency=currencies[0], currency_reason=None)
    observation["forecast_years"] = [row["year"] for row in selected if forecast_year(row.get("year"))]
    field = "equityValuePerShare" if custom else "dcf"
    usable = bool(selected) and all(row.get("symbol") == "MSFT" and finite_number(row.get(field))
                                   and (not custom or forecast_year(row.get("year"))) for row in selected)
    return usable


def beta_binding(observation, baseline):
    rows, previous = observation["observations"], baseline["observations"]
    identity = lambda row: (row.get("symbol"), str(row.get("year")))
    matches = bool(rows) and {identity(row) for row in rows} == {identity(row) for row in previous}
    echoed = matches and all(row.get("symbol") == "MSFT" and forecast_year(row.get("year"))
                             and finite_number(row.get("beta")) and row["beta"] == 1.0 for row in rows)
    if echoed:
        observation["custom_input_behavior"] = {
            "status": "echoed", "input": {"beta": 1.0, "unit": "dimensionless"},
            "issuer_year_binding": [{"symbol": row["symbol"], "year": row["year"]} for row in rows],
            "reason": "specific input echo only; model effect and sensitivity remain unverified",
        }
    else:
        observation["custom_input_behavior"] = {"status": "unverified", "reason": "issuer_year_beta_binding_unknown"}
    return echoed


def direct_probe(monkeypatch, state, probe, query, *, unexecuted=None, baseline=None):
    from openbb_fmp.utils.helpers import get_data_many

    case, branch, endpoint, document = probe
    observation = observation_template(document)
    status, reason, http_status = "unverified", unexecuted, None
    usable = False
    with monkeypatch.context() as patch:
        capture = SourceCapture(patch, "fmp", state, endpoint=branch, kind="direct_provider")
        if reason:
            status = "access_blocked" if reason in {"authentication", "throttling", "entitlement"} else "unverified"
            observation["observed_access"] = {"status": status, "reason": reason, "attempted": False}
        else:
            try:
                acquired = asyncio.run(get_data_many(
                    "https://financialmodelingprep.com/stable/" + endpoint + "?" + urlencode(query),
                    with_provenance=True, typed_errors=True, method="GET", timeout=15,
                    headers={"apikey": os.environ["FMP_API_KEY"]}, allow_redirects=False))
                observation["provider_acquired_at"] = acquired.retrieved_at.isoformat()
                rows = capture.source_rows()
                usable = inspect_rows(observation, rows, branch == "custom_dcf")
                observation["observed_access"] = {"status": "verified", "attempted": True,
                                                  "reason": "direct_provider_response_observed"}
                status, reason = ("verified", None) if usable else ("semantically_unsuitable", "unusable_provider_valuation")
                if baseline is not None and not beta_binding(observation, baseline):
                    status, reason = "unverified", "issuer_year_beta_binding_unknown"
            except Exception as error:  # Only classified codes survive; remote messages are discarded.
                reason = error_code(error)
                state.record_error("fmp", reason, branch)
                status = ("access_blocked" if reason in {"authentication", "throttling", "entitlement"}
                          else "unavailable" if reason == "missing_data" else "failed")
                observation["observed_access"] = {"status": status, "reason": reason,
                                                  "attempted": bool(capture.attempts)}
        if capture.receipts:
            http_status = capture.receipts[-1].get("status")
        observation["status_class"] = f"{http_status // 100}xx" if http_status else "unexecuted" if not capture.attempts else "transport_failure"
        state.record_outcome(case, status, reason=reason,
                             missing_proof=None if status == "verified" else "usable dated provider valuation and specific documented input binding",
                             owner="analyst-workspace-ia-c", prerequisite="dcf-custom-defaults" if baseline is not None or case == "dcf-custom-beta" else None,
                             query=query)
        write_evidence(case, capture, http_status, query=query, observation=observation,
                       failure=reason if status != "verified" and capture.attempts else None)
    return observation, usable


def run_dcf_probes(monkeypatch, state):
    """One ordered journey; preflight does not consume the observer's request budget."""
    observations, baseline, baseline_usable = {}, None, False
    for index, probe in enumerate(PROBES):
        query = {"symbol": "MSFT"}
        if index == 2:
            query["beta"] = 1.0
        reason = ("missing_fmp_credentials" if not os.environ.get("FMP_API_KEY") else
                  state.blocked_providers.get("fmp") or state.blocked_endpoints.get(("fmp", probe[1])) or
                  ("request_ceiling" if state.attempts >= 51 else None))
        if index == 2 and not reason:
            reason = ("unusable_custom_baseline" if not baseline_usable else
                      "documented_beta_binding_unknown" if not CUSTOM_PARAMETER["documented"] else None)
        item, usable = direct_probe(monkeypatch, state, probe, query, unexecuted=reason,
                                    baseline=baseline if index == 2 else None)
        observations[probe[0]] = item
        if index == 1:
            baseline, baseline_usable = item, usable
    return observations


@pytest.mark.live
@pytest.mark.skipif(os.environ.get("QOPENBB_LIVE_ACCEPTANCE") != "1", reason="direct provider feasibility is opt-in")
def test_live_msft_dcf_feasibility(monkeypatch, research_run_state):
    run_dcf_probes(monkeypatch, research_run_state)
    if not os.environ.get("FMP_API_KEY"):
        pytest.skip("FMP credential missing; all direct cases recorded unverified")
    incomplete = [case for case, *_ in PROBES if research_run_state.outcomes[case]["status"] != "verified"]
    if incomplete:
        pytest.fail("direct feasibility remains unverified: " + ", ".join(incomplete), pytrace=False)


@pytest.fixture
def offline_dcf(monkeypatch, tmp_path):
    from openbb_core.provider.utils import helpers

    monkeypatch.setenv("FMP_API_KEY", "synthetic-dcf-credential")
    monkeypatch.delenv("FRED_API_KEY", raising=False)
    monkeypatch.delenv("QOPENBB_LIVE_ACCEPTANCE", raising=False)
    monkeypatch.setenv("QOPENBB_LIVE_EVIDENCE_DIR", str(tmp_path))
    calls = []
    responses = []

    def forbidden(*args, **kwargs):
        raise AssertionError("offline DCF checks cannot use network")

    async def transport(url, **kwargs):
        calls.append((url, kwargs))
        status, payload = responses.pop(0)

        class Response:
            headers = {}

            async def json(self):
                return payload

        response = Response()
        response.status = status
        return await kwargs["response_callback"](response, None)

    monkeypatch.setattr(socket.socket, "connect", forbidden)
    monkeypatch.setattr(helpers, "amake_request", transport)
    return calls, responses, tmp_path


def standard_row(**changes):
    return {"symbol": "MSFT", "date": "2026-11-05", "dcf": 123.5, **changes}


def custom_row(**changes):
    return {"symbol": "MSFT", "year": "2030", "equityValuePerShare": 234.5,
            "beta": 1.2, "wacc": 8.4, **changes}


def receipts(directory):
    return {path.stem: json.loads(path.read_text()) for path in directory.glob("*.json")}


def test_dcf_missing_credentials_records_all_unexecuted_cases(offline_dcf, monkeypatch):
    calls, _, directory = offline_dcf
    monkeypatch.delenv("FMP_API_KEY")
    state = ResearchRunState()
    result = run_dcf_probes(monkeypatch, state)
    assert calls == [] and state.attempts == 0
    assert len(result) == len(state.outcomes) == len(receipts(directory)) == 3
    assert all(item["observed_access"]["status"] == "unverified" for item in result.values())
    assert all(item["reason"] == "missing_fmp_credentials" for item in state.outcomes.values())


def test_dcf_fmp_only_sequence_preserves_transport_and_direct_boundary(offline_dcf, monkeypatch):
    calls, responses, directory = offline_dcf
    responses.extend([(200, [standard_row()]), (200, [custom_row()]),
                      (200, [custom_row(beta=1.0)])])
    state = ResearchRunState()
    result = run_dcf_probes(monkeypatch, state)
    assert state.attempts == len(calls) == 3
    assert [urlsplit(url).path for url, _ in calls] == [
        "/stable/discounted-cash-flow", "/stable/custom-discounted-cash-flow",
        "/stable/custom-discounted-cash-flow"]
    assert [parse_qs(urlsplit(url).query) for url, _ in calls] == [
        {"symbol": ["MSFT"]}, {"symbol": ["MSFT"]}, {"symbol": ["MSFT"], "beta": ["1.0"]}]
    for _, options in calls:
        assert options["method"] == "GET" and options["timeout"] == 15
        assert options["allow_redirects"] is False
        assert options["headers"] == {"apikey": "synthetic-dcf-credential"}
    records = receipts(directory)
    assert records["dcf-custom-defaults"]["endpoint"] == records["dcf-custom-beta"]["endpoint"]
    for case, item in result.items():
        record = records[case]
        assert record["kind"] == "direct_provider" and "financial_metadata" not in record
        assert len(record["source_receipts"]) == 1
        assert record["source_receipts"][0]["status"] == 200
        assert item["source_integration"]["native_api"] == "absent_in_inspected_source"
        assert item["source_integration"]["widget"] == "absent_in_inspected_source"
        assert item["value_origin"] == "provider_calculation"
        assert item["house_dcf"] == "unverified" and item["sensitivity_support"] == "unverified"
    custom = result["dcf-custom-beta"]
    assert custom["custom_input_behavior"]["status"] == "echoed"
    assert custom["custom_input_behavior"]["input"] == {"beta": 1.0, "unit": "dimensionless"}
    assert custom["valuation_date"] is None and custom["forecast_years"] == ["2030"]
    assert custom["currency"] is None
    assert result["dcf-standard"]["valuation_date"] == "2026-11-05"
    assert all(item["currency"] is None for item in result.values())
    text = "".join(path.read_text() for path in directory.glob("*.json"))
    assert "synthetic-dcf-credential" not in text and "https://" not in text
    assert all(item["status"] == "verified" for item in state.outcomes.values())


@pytest.mark.parametrize("code,status", [("entitlement", 403), ("authentication", 401),
                                       ("throttling", 429)])
def test_dcf_access_failure_records_stops_and_preserves_receipts(offline_dcf, monkeypatch, code, status):
    calls, responses, directory = offline_dcf
    responses.extend([(200, [standard_row()]), (status, {"error": "private remote text"})])
    state = ResearchRunState()
    result = run_dcf_probes(monkeypatch, state)
    assert len(calls) == state.attempts == 2
    assert result["dcf-custom-defaults"]["observed_access"]["status"] == "access_blocked"
    assert state.outcomes["dcf-custom-beta"]["status"] == "access_blocked"
    assert state.outcomes["dcf-custom-beta"]["reason"] == code
    records = receipts(directory)
    assert records["dcf-custom-defaults"]["source_receipts"][0]["code"] == code
    assert records["dcf-custom-beta"]["source_receipts"] == []
    assert "private remote text" not in json.dumps(records)
    if code == "entitlement":
        assert state.blocked_providers == {}
        assert state.blocked_endpoints == {("fmp", "custom_dcf"): "entitlement"}
    else:
        assert state.blocked_providers == {"fmp": code}


@pytest.mark.parametrize("row", [custom_row(symbol="ORCL"), custom_row(year=None),
                                 custom_row(equityValuePerShare=None),
                                 custom_row(equityValuePerShare=float("nan"))])
def test_dcf_unusable_baseline_never_requests_beta(offline_dcf, monkeypatch, row):
    calls, responses, directory = offline_dcf
    responses.extend([(200, [standard_row()]), (200, [row])])
    state = ResearchRunState()
    result = run_dcf_probes(monkeypatch, state)
    assert len(calls) == state.attempts == 2
    assert state.outcomes["dcf-custom-defaults"]["status"] == "semantically_unsuitable"
    assert state.outcomes["dcf-custom-beta"]["reason"] == "unusable_custom_baseline"
    assert result["dcf-custom-beta"]["custom_input_behavior"]["status"] == "unverified"
    assert receipts(directory)["dcf-custom-beta"]["source_receipts"] == []


@pytest.mark.parametrize("row", [custom_row(beta=None), custom_row(beta=1.2),
                                 custom_row(beta=1.0, year="2031"),
                                 custom_row(beta=1.0, symbol="ORCL")])
def test_dcf_unknown_binding_is_explicit_without_sensitivity_claim(offline_dcf, monkeypatch, row):
    _, responses, directory = offline_dcf
    responses.extend([(200, [standard_row()]), (200, [custom_row()]), (200, [row])])
    state = ResearchRunState()
    result = run_dcf_probes(monkeypatch, state)
    variation = result["dcf-custom-beta"]
    assert variation["custom_input_behavior"]["status"] == "unverified"
    assert variation["sensitivity_support"] == "unverified"
    assert state.outcomes["dcf-custom-beta"]["status"] != "verified"
    assert receipts(directory)["dcf-custom-beta"]["case_outcome"]["missing_proof"]


def test_dcf_documented_binding_required_before_beta_request(offline_dcf, monkeypatch):
    calls, responses, _ = offline_dcf
    responses.extend([(200, [standard_row()]), (200, [custom_row()])])
    monkeypatch.setitem(CUSTOM_PARAMETER, "documented", False)
    state = ResearchRunState()
    result = run_dcf_probes(monkeypatch, state)
    assert len(calls) == 2 and state.attempts == 2
    assert state.outcomes["dcf-custom-beta"]["reason"] == "documented_beta_binding_unknown"
    assert result["dcf-custom-beta"]["custom_input_behavior"]["status"] == "unverified"


@pytest.mark.parametrize("stop", ["authentication", "throttling", "request_ceiling"])
def test_dcf_shared_native_stop_denies_every_direct_request(offline_dcf, monkeypatch, stop):
    calls, _, directory = offline_dcf
    state = ResearchRunState()
    if stop == "request_ceiling":
        state.attempts = 51
    else:
        state.block_provider("fmp", stop)
    with pytest.raises(pytest.fail.Exception, match="direct feasibility remains unverified"):
        test_live_msft_dcf_feasibility(monkeypatch, state)
    assert calls == [] and len(state.outcomes) == 3
    assert all(item["reason"] == stop for item in state.outcomes.values())
    assert all(item["source_receipts"] == [] for item in receipts(directory).values())


def test_dcf_supplied_dates_currency_and_assumptions_keep_their_source_meaning(offline_dcf, monkeypatch):
    _, responses, _ = offline_dcf
    responses.extend([(200, [standard_row(currency="USD")]),
                      (200, [custom_row(date="2026-11-04", reportedCurrency="USD", wacc=0)]),
                      (200, [custom_row(beta=1.0, date="2026-11-04", reportedCurrency="USD", wacc=0)])])
    result = run_dcf_probes(monkeypatch, ResearchRunState())
    assert result["dcf-standard"]["currency"] == "USD"
    custom = result["dcf-custom-beta"]
    assert custom["valuation_date"] == "2026-11-04" and custom["forecast_years"] == ["2030"]
    assert custom["currency"] is None and custom["currency_reason"] == "dcf_currency_not_supplied"
    assert custom["observations"][0]["reportedCurrency"] == "USD"
    assert custom["observations"][0]["wacc"] == 0
    assert "wacc" in custom["assumption_coverage"]["fields"]
    assert custom["provider_acquired_at"] != custom["valuation_date"]
