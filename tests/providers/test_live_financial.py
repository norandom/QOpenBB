"""Opt-in real financial inputs; synthetic edge tests remain separate acceptance evidence."""
import os
from datetime import date, timedelta
from pathlib import Path

import pytest
from live_financial_support import (
    ROOT,
    ResearchRequestBlocked,
    ResearchRunState,
    SourceCapture,
    call,
    equal,
    evidence,
    error_code,
    metadata,
    pairs,
    require,
    research_run_state,
    success,
    unit,
    unknown_valuation_bases,
    validate_rows,
    write_evidence,
)
from research_input_cases import COMPANIES, company_cases, research_case

live_only = pytest.mark.skipif(
    os.environ.get("QOPENBB_LIVE_ACCEPTANCE") != "1", reason="real provider acceptance is opt-in")

STATEMENT = {"symbol": "symbol", "period_ending": "date", "fiscal_period": "period", "reported_currency": "reportedCurrency"}
CASES = [
    ("search", "/equity/search", {"query": "Microsoft", "limit": 5}, {"symbol": "symbol", "name": "name", "currency": "currency"}),
    ("peers", "/equity/compare/peers", {"symbol": "MSFT", "limit": 5}, {"symbol": "symbol", "name": "companyName"}),
    *[("profile-" + symbol, "/equity/profile", {"symbol": symbol},
       {"symbol": "symbol", "name": "companyName", "currency": "currency", "last_price": "price"})
      for symbol in ("MSFT", "AAPL", "GOOGL")],
    ("prices", "/equity/price/historical", {"symbol": "MSFT", "start_date": "2025-01-02", "end_date": "2025-01-31"},
     {"date": "date", "open": "open", "high": "high", "low": "low", "close": "close", "volume": "volume", "change": "change"}),
    *[("income-" + period, "/equity/fundamental/income", {"symbol": "MSFT", "period": period, "limit": 2},
       {**STATEMENT, "revenue": "revenue", "consolidated_net_income": "netIncome",
        "weighted_average_basic_shares_outstanding": "weightedAverageShsOut",
        "weighted_average_diluted_shares_outstanding": "weightedAverageShsOutDil"})
      for period in ("annual", "quarter")],
    ("balance", "/equity/fundamental/balance", {"symbol": "MSFT", "period": "annual", "limit": 2},
     {**STATEMENT, "total_assets": "totalAssets", "total_liabilities": "totalLiabilities", "total_common_equity": "totalStockholdersEquity"}),
    ("cash", "/equity/fundamental/cash", {"symbol": "MSFT", "period": "annual", "limit": 2},
     {**STATEMENT, "net_cash_from_operating_activities": "netCashProvidedByOperatingActivities", "cash_at_end_of_period": "cashAtEndOfPeriod"}),
    ("metrics", "/equity/fundamental/metrics", {"symbol": "MSFT", "period": "annual", "limit": 2},
     {"period_ending": "date", "fiscal_period": "period", "currency": "reportedCurrency", "enterprise_value": "enterpriseValue", "ev_to_ebitda": "evToEBITDA"}),
    ("ratios", "/equity/fundamental/ratios", {"symbol": "MSFT", "period": "annual", "limit": 2},
     {"period_ending": "date", "fiscal_period": "period", "currency": "reportedCurrency", "price_to_earnings": "priceToEarningsRatio", "net_profit_margin": "netProfitMargin"}),
    ("enterprise", "/equity/fundamental/enterprise_values", {"symbol": "MSFT", "period": "annual", "limit": 2},
     {"date": "date", "stock_price": "stockPrice", "number_of_shares": "numberOfShares", "market_cap": "marketCapitalization",
      "cash_and_cash_equivalents": "minusCashAndCashEquivalents", "total_debt": "addTotalDebt", "enterprise_value": "enterpriseValue"}),
]


@pytest.fixture(scope="module")
def live_app():
    if not all(os.environ.get(name) for name in ("FMP_API_KEY", "FRED_API_KEY")):
        pytest.skip("live provider credentials are not configured")
    import qopenbb_data.app as application
    import qopenbb_data.config as configuration

    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(application, "CATALOG", ROOT / "contracts")
        patch.setattr(configuration, "COVERAGE", ROOT / "docs/reference/provider-coverage.json")
        yield application.create_app()


def financial_meaning(case, rows, common, parameters):
    if case.startswith("income"):
        basis = "annual" if parameters["period"] == "annual" else "discrete_quarter"
        unit(common, "revenue", "currency", "provider_observation", basis)
        unit(common, "weighted_average_basic_shares_outstanding", "shares", basis=basis)
        require(all(row["fiscal_period"] == "FY" if basis == "annual" else
                    row["fiscal_period"] in {"Q1", "Q2", "Q3", "Q4"} for row in rows), "reported fiscal period")
    elif case == "balance":
        unit(common, "total_assets", "currency", "provider_observation", "instant")
    elif case == "cash":
        unit(common, "net_cash_from_operating_activities", "currency", basis="annual")
        unit(common, "cash_at_end_of_period", "currency", basis="instant")
    elif case == "prices":
        unit(common, "close", "currency/share", "provider_observation", "daily")
        require(all(parameters["start_date"] <= row["date"] <= parameters["end_date"] for row in rows), "bounded price dates")
        require(common["fields"]["close"]["currency"] is None, "price currency not inferred")
    elif case == "peers":
        require(all(row["source_symbol"] == "MSFT" and row["candidate_basis"] == "provider_suggestion"
                    for row in rows), "provider peer suggestions retain their basis")
    elif case.startswith("profile"):
        unit(common, "last_price", "currency/share", "provider_observation")
        equal(common["fields"]["last_price"]["currency_field"], "currency", "profile trading currency basis")
    elif case in {"metrics", "ratios", "enterprise"}:
        field = {"metrics": "ev_to_ebitda", "ratios": "price_to_earnings", "enterprise": "enterprise_value"}[case]
        unit(common, field, "currency" if case == "enterprise" else "multiple", "provider_calculation")
        unknown_valuation_bases(common, field)
        if case == "enterprise":
            unit(common, "number_of_shares", "shares", "provider_observation")


@pytest.mark.live
@live_only
@pytest.mark.parametrize("case,path,parameters,mapping", CASES, ids=[case[0] for case in CASES])
def test_real_fmp_observations_reach_native_api(live_app, monkeypatch, case, path, parameters, mapping):
    capture = SourceCapture(monkeypatch, "fmp")
    with evidence(case, capture) as record:
        status, body = call(live_app, "/api/v1" + path, {"provider": "fmp", **parameters})
        record["status"] = status
        success(status, body, "FMP")
        rows = body.get("results")
        require(isinstance(rows, list) and bool(rows), "real nonempty API rows")
        if parameters.get("symbol") and case not in {"peers", "prices"}:
            require(all(row["symbol"] == parameters["symbol"] for row in rows), "requested listing identity")
        validate_rows(live_app, "/api/v1" + path, "fmp", body)
        record["common"] = common = metadata(body, capture, parameters)
        date_field = "period_ending" if "period_ending" in mapping else "date" if "date" in mapping else None
        source_rows = capture.source_rows()
        require(len(rows) == min(len(source_rows), parameters.get("limit", len(source_rows))), "bounded source row preservation")
        record["comparisons"] = pairs(rows, source_rows, mapping, date_field)
        if case not in {"search", "peers"}:
            require(any(isinstance(item["value"], (int, float)) for item in record["comparisons"]), "actual financial quantities required")
        financial_meaning(case, rows, common, parameters)


@pytest.mark.live
@live_only
def test_real_fred_named_usd_ten_year_rate(live_app, monkeypatch):
    from openbb_fred.utils import rate_limiter

    # Acceptance has a fixed two-request budget; entitlement failures must not retry.
    monkeypatch.setattr(rate_limiter, "MAX_RETRIES", 0)
    capture = SourceCapture(monkeypatch, "fred")
    parameters = {"symbol": "DGS10", "start_date": "2025-01-02", "end_date": "2025-01-31", "limit": 31, "use_cache": False}
    with evidence("fred-DGS10", capture) as record:
        status, body = call(live_app, "/api/v1/economy/fred_series", {"provider": "fred", **parameters})
        record["status"] = status
        success(status, body, "FRED")
        validate_rows(live_app, "/api/v1/economy/fred_series", "fred", body)
        record["common"] = common = metadata(body, capture, parameters)
        record["comparisons"] = fred_values(body, capture, common)


def fred_values(body, capture, common):
    require(len(capture.receipts) == 2, "FRED actual observations and series metadata")
    observations = capture.receipts[0]["payload"]["observations"]
    source = capture.receipts[1]["payload"]["seriess"][0]
    equal(source["id"], "DGS10", "independent macro series identity")
    require("10-Year" in source["title"], "named USD ten-year Treasury context")
    rows = body["results"]
    require(bool(rows), "real FRED observations required")
    require(len(rows) == len(observations), "FRED missing observations retained")
    comparisons = []
    for row in rows:
        raw = next(item for item in observations if item["date"] == row["date"])
        value = None if raw["value"] == "." else float(raw["value"])
        equal(row["DGS10"], value, "FRED date/value preservation")
        provenance = common["observation_provenance"]["DGS10"][row["date"]]
        equal(provenance, {name: raw.get(name) for name in ("realtime_start", "realtime_end")}, "FRED real-time observation interval")
        comparisons.append({"date": row["date"], "source_field": "value", "field": "DGS10", "value": value})
    details = common["fields"]["DGS10"]
    for field, source_field in (("unit", "units"), ("source_unit", "units"), ("source_frequency", "frequency"),
                                ("effective_frequency", "frequency"), ("seasonal_adjustment", "seasonal_adjustment")):
        equal(details[field], source[source_field], "FRED source semantics " + field)
    equal(details["unit"], "Percent", "FRED rate unit; no decimal-rate conversion")
    equal(details["value_origin"], "provider_observation", "FRED observation origin")
    require(details["aggregation"] is None and details["requested_transform"] is None, "no implicit FRED alignment transform")
    return comparisons


@pytest.mark.live
@live_only
def test_missing_and_invalid_inputs_stop_before_provider_io(live_app, monkeypatch):
    capture = SourceCapture(monkeypatch, "fmp")
    for parameters in ({"symbol": "MSFT"}, {"provider": "fmp"},
                       {"provider": "fmp", "symbol": "MSFT", "limit": -1}):
        status, _ = call(live_app, "/api/v1/equity/fundamental/balance", parameters)
        require(status in {400, 422}, "missing/invalid financial input rejected")
    require(capture.attempts == 0, "invalid input has no provider request")


def research_findings(case, rows, common):
    """Raw equality is one dimension; unresolved methods never become model inputs."""
    dataset = case["dataset"]
    findings = [{"dimension": "source_api_equality", "status": "verified"}]
    company = next(company for company in COMPANIES if company["symbol"] == case["company_symbol"])
    if dataset in {"search", "profile", "peers"}:
        findings.append({"dimension": "listing_identity", "observations": [{key: row.get(key) for key in
                         ("symbol", "name", "listing_id", "exchange", "exchange_short_name", "stock_exchange", "currency", "candidate_basis")} for row in rows],
                         "sample_candidate_basis": company["candidate_basis"], "rationale": company["rationale"],
                         "material_differences": company["differences"],
                         "reporting_currency": None, "reporting_currency_reason": "Requires statements; listing currency is trading currency"})
    for field in case["field_mapping"]:
        details = common["fields"][field]
        findings.append({"field": field, "definition": details["definition"], "unit": details["unit"],
                         "period_basis": details["period_basis"], "value_origin": details["value_origin"],
                         "availability": details["availability"]})
        if not any(row.get(field) is not None for row in rows):
            findings.append({"dimension": "required_field", "field": field, "status": "unavailable",
                             "reason": "No supplied nonnull observation", "missing_proof": "Observed source value",
                             "owner": "market-data-integrations"})
    if dataset not in {"search", "peers", "profile"}:
        findings.extend([
            {"dimension": "currency_unit_compatibility", "status": "unverified",
             "reason": "Source units are retained; cross-company reporting/trading currencies and periods are not reconciled",
             "missing_proof": "Same-basis currency, unit and fiscal-calendar compatibility", "owner": "financial-modeling",
             "material_differences": company["differences"]},
            {"dimension": "house_input_adequacy", "status": "unverified",
             "reason": "Raw preservation does not establish an approved house-method input",
             "missing_proof": "Approved house definitions and input contract", "owner": "financial-modeling",
             "house_calculation": False},
        ])
    if dataset in {"income", "balance", "cash", "metrics", "ratios"}:
        findings.append({"dimension": "reporting_basis", "status": "unverified",
                         "observations": [{key: row.get(key) for key in
                                           ("period_ending", "fiscal_year", "fiscal_period", "reported_currency", "currency")} for row in rows],
                         "actual_start_date": None, "actual_duration": None, "ytd_convention": None,
                         "restatement_basis": None, "reason": "Fiscal labels do not establish actual duration, YTD or restatement history",
                         "share_measure_note": "Income weighted-average shares and EV provider share counts are distinct measures",
                         "missing_proof": "Source duration, cumulative-flow and restatement conventions",
                         "owner": "market-data-integrations"})
    if dataset in {"income", "cash"}:
        findings.append({"dimension": "cash_conversion_method", "status": "unverified",
                         "reason": "Numerator, denominator, capex sign, leases and accounting adjustments remain undefined",
                         "missing_proof": "Approved cash-conversion and adjusted-earnings input contract",
                         "owner": "financial-modeling",
                         "provider_supplied_outputs": [field for field in ("ebitda", "operating_cash_flow", "free_cash_flow") if field in case["field_mapping"]],
                         "house_calculation": False})
    if dataset in {"metrics", "ratios", "enterprise", "prices", "profile"}:
        findings.append({"dimension": "market_share_alignment", "status": "unverified",
                         "reason": "Price, currency, share-count type/date, debt and cash timing are not reconciled",
                         "missing_proof": "Same-listing currency, market-date and share-basis reconciliation",
                         "owner": "financial-modeling", "ev_reference": case.get("ev_reference"),
                         "share_count_type": None, "share_count_date": None,
                         "adjustment": case["parameters"].get("adjustment"),
                         "price_dates": [row.get("date") for row in rows] if dataset == "prices" else []})
    if dataset == "enterprise":
        findings.append({"dimension": "enterprise_to_equity_bridge", "status": "unverified",
                         "reason": "Supplied market cap, cash and debt do not establish a complete bridge",
                         "missing_proof": "Minority, preferred, lease and other-claim definitions and aligned dates",
                         "owner": "financial-modeling", "minority_claims": None, "preferred_claims": None,
                         "lease_claims": None, "other_claims": None, "house_calculation": False})
    if dataset in {"metrics", "ratios"}:
        findings.append({"dimension": "peer_aggregate_eligibility", "status": "unverified",
                         "reason": "Numeric provider outputs do not prove positive denominators, trailing/forward or fiscal/currency compatibility",
                         "missing_proof": "Verified same-basis denominators and approved peer membership/aggregation method",
                         "owner": "financial-modeling", "accepted_peer_aggregate_input": False,
                         "denominator_validity": None, "house_recalculated": False})
    return findings


def research_financial_meaning(case, rows, common):
    dataset, parameters = case["dataset"], case["parameters"]
    if dataset == "cash":
        basis = "annual" if parameters["period"] == "annual" else "discrete_quarter"
        unit(common, "net_cash_from_operating_activities", "currency", "provider_observation", basis)
        unit(common, "cash_at_end_of_period", "currency", basis="instant")
        unit(common, "free_cash_flow", "currency", "provider_calculation", basis)
    else:
        financial_meaning(dataset, rows, common, parameters)
    if dataset in {"metrics", "ratios"}:
        equal(parameters.get("ttm", "exclude"), "exclude", "periodic provider outputs requested")
        equal(common["effective_query"].get("ttm"), "exclude", "periodic metadata selection")
    return research_findings(case, rows, common)


def research_receipt(case):
    output = Path(os.environ.get("QOPENBB_LIVE_EVIDENCE_DIR", ROOT / "artifacts/live-financial-checks/run"))
    return str(output / (case["case_id"] + ".json"))


def unexecuted_research_case(monkeypatch, state, case, reason, prerequisite=None):
    causal = state.outcomes.get(prerequisite, {})
    if causal.get("status") == "access_blocked":
        reason = causal["reason"]
        prerequisite = causal.get("prerequisite") or prerequisite
    elif state.blocked_providers.get("fmp"):
        reason = state.blocked_providers["fmp"]
        prerequisite = next((case_id for case_id, outcome in state.outcomes.items()
                             if outcome["status"] == "access_blocked" and outcome["reason"] == reason
                             and not outcome.get("prerequisite")), prerequisite)
    status = "access_blocked" if reason in {"authentication", "throttling", "entitlement"} else "unverified"
    state.record_outcome(case["case_id"], status, reason=reason,
                         missing_proof="Successful native observations after required prerequisite",
                         prerequisite=prerequisite, query=case["parameters"])
    with monkeypatch.context() as patch:
        capture = SourceCapture(patch, "fmp", state, endpoint=case["dataset"])
        write_evidence(case["case_id"], capture, None, query=case["parameters"])
    return None


def profile_listing_identity(case, rows):
    """Only the selected discovery row supplies exchange label/code equivalence."""
    reference = case["listing_reference"]
    observed = {field: reference[field] for field in ("exchange", "exchange_short_name") if reference.get(field)}
    profile_exchange = rows[0].get("stock_exchange") if len(rows) == 1 else None
    matched = [field for field, value in observed.items() if value == profile_exchange]
    established = len(rows) == 1 and bool(rows[0].get("name")) and bool(matched)
    return {"dimension": "profile_listing_identity", "status": "verified" if established else "unverified",
            "listing_id": reference["listing_id"], "discovery_exchanges": observed,
            "profile_exchange": profile_exchange, "matched_discovery_fields": matched,
            "reason": None if established else "unresolved_listing_exchange",
            "missing_proof": None if established else "Unambiguous profile identity and exchange matching an observed discovery label/code, or independently verified equivalence",
            "owner": "market-data-integrations", "prerequisite": case["identity_prerequisite"]}


def execute_research_case(app, monkeypatch, state, case):
    """Each request owns one capture; failure leaves its immutable receipt and permits gap recording."""
    endpoint = case["dataset"]
    stopped = state.blocked_providers.get("fmp") or state.blocked_endpoints.get(("fmp", endpoint))
    if stopped or state.attempts >= 51:
        return unexecuted_research_case(monkeypatch, state, case, stopped or "request_ceiling")
    with monkeypatch.context() as patch:
        capture = SourceCapture(patch, "fmp", state, endpoint=endpoint)
        try:
            with evidence(case["case_id"], capture, query=case["parameters"]) as record:
                try:
                    parameters = case["parameters"]
                    status, body = call(app, "/api/v1" + case["route"], {"provider": "fmp", **parameters})
                    record["status"] = status
                    success(status, body, "FMP", run_state=state, endpoint=endpoint)
                    rows = body.get("results")
                    require(isinstance(rows, list) and bool(rows), "real nonempty API rows")
                    if endpoint not in {"search", "peers", "prices"}:
                        require(all(row.get("symbol") == case["company_symbol"] for row in rows), "requested listing identity")
                    validate_rows(app, "/api/v1" + case["route"], "fmp", body)
                    record["common"] = common = metadata(body, capture, parameters)
                    source = capture.source_rows()
                    require(len(rows) == min(len(source), parameters.get("limit", len(source))), "bounded source row preservation")
                    mapping = case["field_mapping"]
                    date_field = "period_ending" if "period_ending" in mapping else "date" if "date" in mapping else None
                    record["comparisons"] = pairs(rows, source, mapping, date_field)
                    record["comparisons"].extend(research_financial_meaning(case, rows, common))
                    identity = profile_listing_identity(case, rows) if endpoint == "profile" else None
                    if identity:
                        record["comparisons"].append(identity)
                    if identity and identity["status"] != "verified":
                        state.record_outcome(case["case_id"], identity["status"], reason=identity["reason"],
                                             missing_proof=identity["missing_proof"], prerequisite=identity["prerequisite"], query=parameters)
                    else:
                        state.record_outcome(case["case_id"], "verified", query=parameters)
                except (Exception, pytest.fail.Exception) as error:
                    reason = error_code(error)
                    reason = next((item["code"] for item in capture.receipts if item.get("code")), reason)
                    state.record_outcome(case["case_id"], "access_blocked" if reason in
                                         {"authentication", "throttling", "entitlement"} else "failed",
                                         reason=reason if reason != "uncategorized" else "acceptance validation error",
                                         missing_proof="Successful source-preserving native input validation", query=case["parameters"])
                    raise
        except (Exception, pytest.fail.Exception):
            return None
    if state.outcomes[case["case_id"]]["status"] != "verified":
        return None
    return {"rows": rows, "common": common, "receipt_ref": research_receipt(case)}


def resolved_listing(rows, symbol):
    candidates = [row for row in rows if row.get("symbol") == symbol and row.get("name")
                  and row.get("listing_id", "").startswith("fmp:symbol:")
                  and (row.get("exchange_short_name") or row.get("exchange"))]
    return candidates[0] if len(candidates) == 1 else None


def run_company_journey(app, monkeypatch, state, symbol):
    cases = company_cases(symbol)
    discovery = execute_research_case(app, monkeypatch, state, cases[0])
    listing = resolved_listing(discovery["rows"], symbol) if discovery else None
    profile = None
    if listing:
        cases[1]["listing_reference"] = listing
        cases[1]["identity_prerequisite"] = cases[0]["case_id"]
        profile = execute_research_case(app, monkeypatch, state, cases[1])
    else:
        unexecuted_research_case(monkeypatch, state, cases[1], "unresolved_listing", cases[0]["case_id"])
    for case in cases[2:]:
        if not listing or not profile:
            unexecuted_research_case(monkeypatch, state, case, "unresolved_listing", cases[1]["case_id"])
            continue
        result = execute_research_case(app, monkeypatch, state, case)
        if result and case["dataset"] == "enterprise":
            for row in result["rows"]:
                state.record_enterprise_date(symbol, row.get("date"), listing_id=listing["listing_id"],
                                             case_id=case["case_id"], receipt_ref=result["receipt_ref"])
    reference = state.enterprise_reference(symbol, listing["listing_id"]) if listing and profile else None
    price = research_case(symbol, "prices", {"symbol": symbol, "interval": "1d", "adjustment": "splits_only"})
    if not reference or not reference.get("case_id") or not reference.get("receipt_ref"):
        prerequisite = cases[-1]["case_id"] if listing and profile else cases[1]["case_id"]
        unexecuted_research_case(monkeypatch, state, price, "missing_successful_same_listing_ev", prerequisite)
    else:
        latest = date.fromisoformat(reference["date"])
        price["parameters"].update(start_date=(latest - timedelta(days=7)).isoformat(), end_date=latest.isoformat())
        price["ev_reference"] = reference
        execute_research_case(app, monkeypatch, state, price)
    return {"listing": listing, "profile": profile, "ev_reference": reference}


@pytest.fixture(scope="module")
def research_app():
    if not os.environ.get("FMP_API_KEY"):
        pytest.skip("FMP research credentials are not configured; native access remains unverified")
    import qopenbb_data.app as application
    import qopenbb_data.config as configuration
    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(application, "CATALOG", ROOT / "contracts")
        patch.setattr(configuration, "COVERAGE", ROOT / "docs/reference/provider-coverage.json")
        yield application.create_app()


PERIODIC_CASES = [(dataset, selection) for dataset in ("metrics", "ratios")
                  for selection in ("default-annual", "explicit-quarter")]


class PeriodicRunState(ResearchRunState):
    """Share four FMP attempts across the selected cases, including failures."""

    def before_request(self, provider, endpoint=None):
        if provider != "fmp" or endpoint not in {"metrics", "ratios"}:
            raise ResearchRequestBlocked("periodic_scope")
        if self.attempts >= 4:
            raise ResearchRequestBlocked("request_ceiling")
        super().before_request(provider, endpoint)


@pytest.fixture(scope="session")
def periodic_run_state():
    return PeriodicRunState()


def periodic_case(dataset, selection):
    parameters = {"symbol": "MSFT", "limit": 1}
    if selection == "explicit-quarter":
        parameters.update(period="quarter", ttm="exclude")
    return research_case("MSFT", dataset, parameters, "periodic-" + selection)


@pytest.mark.live
@live_only
@pytest.mark.parametrize("dataset,selection", PERIODIC_CASES,
                         ids=[dataset + "-" + selection for dataset, selection in PERIODIC_CASES])
def test_real_periodic_query_provenance(research_app, monkeypatch, periodic_run_state, dataset, selection):
    case = periodic_case(dataset, selection)
    before = periodic_run_state.attempts
    result = execute_research_case(research_app, monkeypatch, periodic_run_state, case)
    require(result is not None, "periodic source/native validation; inspect immutable receipt")
    require(periodic_run_state.attempts == before + 1, "one request per periodic case")
    equal(result["common"]["effective_query"], {
        "symbol": "MSFT", "limit": 1, "period": "quarter" if selection == "explicit-quarter" else "annual",
        "ttm": "exclude",
    }, "validated default/explicit periodic query")


@pytest.mark.live
@live_only
@pytest.mark.parametrize("symbol", [company["symbol"] for company in COMPANIES])
def test_research_company_inputs(research_app, monkeypatch, research_run_state, symbol):
    result = run_company_journey(research_app, monkeypatch, research_run_state, symbol)
    required = [case["case_id"] for case in company_cases(symbol)] + ["research-" + symbol + "-prices"]
    require(bool(result["listing"] and result["profile"]), "same-listing discovery/profile identity required")
    require(all(research_run_state.outcomes[case]["status"] == "verified" for case in required),
            "required research input failed or remained unexecuted; inspect receipts")


@pytest.mark.live
@live_only
def test_research_provider_peer_suggestions(research_app, monkeypatch, research_run_state):
    case = research_case("MSFT", "peers", {"symbol": "MSFT", "limit": 5})
    result = execute_research_case(research_app, monkeypatch, research_run_state, case)
    require(result is not None, "provider suggestions require successful native evidence")


def test_research_declared_request_matrix():
    from research_input_cases import COMPANIES, company_cases

    identifiers = []
    for company in COMPANIES:
        cases = company_cases(company["symbol"])
        assert [case["dataset"] for case in cases[:2]] == ["search", "profile"]
        financial = cases[2:]
        assert len(financial) == 12
        assert {case["dataset"] for case in financial} == {"income", "balance", "cash", "metrics", "ratios", "enterprise"}
        for case in financial:
            assert case["parameters"]["limit"] == (2 if case["parameters"]["period"] == "annual" else 4)
            if case["dataset"] in {"metrics", "ratios"}:
                assert case["parameters"]["ttm"] == "exclude"
            identifiers.append(case["case_id"])
        assert company["rationale"] and company["differences"]
    assert len(identifiers) == len(set(identifiers))


def test_research_unresolved_identity_records_all_dependents(monkeypatch, tmp_path):
    from live_financial_support import ResearchRunState
    from research_input_cases import company_cases

    monkeypatch.setenv("QOPENBB_LIVE_EVIDENCE_DIR", str(tmp_path))
    executed = []
    def unresolved(app, patch, state, case):
        executed.append(case["dataset"])
        state.record_outcome(case["case_id"], "verified", query=case["parameters"])
        return {"rows": [{"symbol": "OTHER"}]}
    monkeypatch.setattr(__import__(__name__), "execute_research_case", unresolved)
    state = ResearchRunState()
    run_company_journey(None, monkeypatch, state, "MSFT")
    assert executed == ["search"]
    required = [case["case_id"] for case in company_cases("MSFT")][1:] + ["research-MSFT-prices"]
    assert all(state.outcomes[case]["status"] != "verified" for case in required)
    assert all(state.outcomes[case]["missing_proof"] for case in required)
    assert state.attempts == 0


@pytest.fixture
def research_offline_app(monkeypatch, tmp_path):
    import qopenbb_data.app as application
    import qopenbb_data.config as configuration
    monkeypatch.setattr(application, "CATALOG", ROOT / "contracts")
    monkeypatch.setattr(configuration, "COVERAGE", ROOT / "docs/reference/provider-coverage.json")
    for name in ("SOURCE", "GENERATION"):
        monkeypatch.setenv("QOPENBB_DATA_" + name + "_REVISION", "1" * 40)
    monkeypatch.setenv("FMP_API_KEY", "fixture-native-fmp")
    monkeypatch.setenv("OPENBB_API_AUTH", "false")
    monkeypatch.setenv("QOPENBB_LIVE_EVIDENCE_DIR", str(tmp_path))
    return application.create_app()


@pytest.fixture
def research_fake_provider(monkeypatch):
    """Exercise the original response callback, fetcher and native API without network access."""
    from copy import deepcopy
    from urllib.parse import parse_qs, urlsplit
    from research_input_cases import MAPPINGS

    controls = {"requests": [], "failures": {}, "missing_ev": False, "bad_identity": False,
                "mutate": None}
    endpoints = {"search-name": "search", "profile": "profile", "stock-peers": "peers",
                 "income-statement": "income", "balance-sheet-statement": "balance",
                 "cash-flow-statement": "cash", "key-metrics": "metrics", "ratios": "ratios",
                 "enterprise-values": "enterprise", "historical-price-eod/full": "prices"}

    async def request(url, **kwargs):
        parsed = urlsplit(url)
        dataset = endpoints[parsed.path.removeprefix("/stable/")]
        parameters = {key: values[0] for key, values in parse_qs(parsed.query).items() if key != "apikey"}
        controls["requests"].append((dataset, parameters))
        symbol = parameters.get("symbol") or next(company["symbol"] for company in COMPANIES if company["name"] == parameters["query"])
        period = parameters.get("period", "annual")
        raw = {source: -7 for source in MAPPINGS[dataset].values()}
        raw.update(symbol=symbol, date="2025-06-30" if period == "annual" else "2025-09-30",
                   period="FY" if period == "annual" else "Q1", fiscalYear="2025",
                   reportedCurrency="USD", currency="USD", filingDate="2025-10-15",
                   exchange="NASDAQ", exchangeShortName="NASDAQ", companyName=symbol + " Corporation", name=symbol + " Corporation")
        if dataset == "search" and controls["bad_identity"]:
            raw["symbol"] = "OTHER"
        if dataset == "enterprise" and controls["missing_ev"]:
            raw.pop("date")
        if dataset == "prices":
            raw["date"] = parameters["to"]
        if dataset == "balance":
            raw["minorityInterest"] = None
            raw.pop("preferredStock")
        payload = [raw]
        if dataset in {"income", "balance", "cash", "metrics", "ratios", "enterprise"}:
            payload.append({**raw, **{"revenue": 0, "capitalExpenditure": 0, "enterpriseValue": 0}})
        if controls["mutate"]:
            controls["mutate"](dataset, period, payload)
        response_status = controls["failures"].get((dataset, period), controls["failures"].get(dataset, 200))
        class Response:
            status = response_status
            headers = {}
            async def json(self):
                return deepcopy(payload)
        return await kwargs["response_callback"](Response(), None)

    monkeypatch.setattr("openbb_core.provider.utils.helpers.amake_request", request)
    return controls


def test_periodic_live_selection_offline_capture_and_ceiling(
    research_offline_app, research_fake_provider, monkeypatch, tmp_path,
):
    import json

    state = PeriodicRunState()
    for dataset, selection in PERIODIC_CASES:
        test_real_periodic_query_provenance(research_offline_app, monkeypatch, state, dataset, selection)
        case = periodic_case(dataset, selection)
        receipt = json.loads((tmp_path / (case["case_id"] + ".json")).read_text())
        assert receipt["query"] == case["parameters"]
        assert receipt["financial_metadata"]["effective_query"]["ttm"] == "exclude"
        assert len(receipt["source_receipts"]) == 1 and receipt["failure"] is None
        assert any(item.get("source_field") for item in receipt["comparisons"])
        assert "ttm_metadata" not in {item.get("dimension") for item in receipt["comparisons"]}
        assert next(item for item in receipt["comparisons"] if item.get("dimension") == "reporting_basis")["status"] == "unverified"
    assert state.attempts == len(research_fake_provider["requests"]) == 4
    assert [query for _, query in research_fake_provider["requests"]] == [
        {"symbol": "MSFT", "period": period, "limit": "1"}
        for _ in ("metrics", "ratios") for period in ("annual", "quarter")]
    with pytest.raises(ResearchRequestBlocked, match="request_ceiling"):
        state.before_request("fmp", "metrics")
    with pytest.raises(ResearchRequestBlocked, match="periodic_scope"):
        PeriodicRunState().before_request("fred", "DGS10")
    assert state.attempts == 4


@pytest.mark.parametrize("symbol", [company["symbol"] for company in COMPANIES])
def test_research_offline_full_company_journey(research_offline_app, research_fake_provider, monkeypatch, tmp_path, symbol):
    import json
    from live_financial_support import ResearchRunState

    state = ResearchRunState()
    result = run_company_journey(research_offline_app, monkeypatch, state, symbol)
    assert all(value["status"] == "verified" for value in state.outcomes.values()), state.outcomes
    assert state.attempts == len(research_fake_provider["requests"]) == 15
    datasets = [dataset for dataset, _ in research_fake_provider["requests"]]
    assert datasets[:2] == ["search", "profile"] and datasets[-3:] == ["enterprise", "enterprise", "prices"]
    assert result["listing"]["listing_id"] == "fmp:symbol:" + symbol + ":exchange:NASDAQ"
    reference = result["ev_reference"]
    assert reference["date"] == "2025-09-30" and reference["case_id"] == "research-" + symbol + "-enterprise-quarter"
    assert Path(reference["receipt_ref"]).is_file()
    price_query = research_fake_provider["requests"][-1][1]
    assert price_query == {"symbol": symbol, "from": "2025-09-23", "to": "2025-09-30"}
    receipts = {path.stem: json.loads(path.read_text()) for path in tmp_path.glob("*.json")}
    assert len(receipts) == 15
    for case in company_cases(symbol):
        receipt = receipts[case["case_id"]]
        assert receipt["case_outcome"]["status"] == "verified" and receipt["kind"] == "native_api"
        comparisons = receipt["comparisons"]
        assert {item["field"] for item in comparisons if "source_field" in item} == set(case["field_mapping"])
        if case["dataset"] in {"income", "balance", "cash", "metrics", "ratios"}:
            basis = next(item for item in comparisons if item.get("dimension") == "reporting_basis")
            assert basis["actual_duration"] is None and basis["ytd_convention"] is None
        if case["dataset"] in {"metrics", "ratios"}:
            assert receipt["financial_metadata"]["effective_query"]["ttm"] == "exclude"
            assert "ttm_metadata" not in {item.get("dimension") for item in comparisons}
        if case["dataset"] == "balance":
            minority = [item for item in comparisons if item.get("source_field") == "minorityInterest"]
            preferred = [item for item in comparisons if item.get("source_field") == "preferredStock"]
            assert {item["source_state"] for item in minority} == {"null"}
            assert {item["source_state"] for item in preferred} == {"absent"}
        if case["dataset"] == "income":
            revenue = [item for item in comparisons if item.get("source_field") == "revenue"]
            assert [(item["source_ordinal"], item["value"]) for item in revenue] == [(0, -7), (1, 0)]
    price = receipts["research-" + symbol + "-prices"]
    timing = next(item for item in price["comparisons"] if item.get("dimension") == "market_share_alignment")
    assert timing["ev_reference"] == reference and timing["status"] == "unverified"


@pytest.mark.parametrize("gap", ["missing_ev", "bad_identity"])
def test_research_offline_prerequisites_never_fetch_fallback(research_offline_app, research_fake_provider, monkeypatch, tmp_path, gap):
    import json
    from live_financial_support import ResearchRunState

    research_fake_provider[gap] = True
    state = ResearchRunState()
    run_company_journey(research_offline_app, monkeypatch, state, "MSFT")
    assert "prices" not in [dataset for dataset, _ in research_fake_provider["requests"]]
    assert state.attempts == (14 if gap == "missing_ev" else 1)
    outcome = state.outcomes["research-MSFT-prices"]
    assert outcome["status"] == "unverified" and outcome["prerequisite"] and outcome["missing_proof"]
    receipt = json.loads((tmp_path / "research-MSFT-prices.json").read_text())
    assert receipt["source_receipts"] == [] and receipt["http_status"] is None


@pytest.mark.parametrize("code,attempts", [(401, 3), (429, 3), (403, 14)])
def test_research_offline_provider_and_branch_stops(research_offline_app, research_fake_provider, monkeypatch, tmp_path, code, attempts):
    import json
    from live_financial_support import ResearchRunState

    research_fake_provider["failures"]["income"] = code
    state = ResearchRunState()
    run_company_journey(research_offline_app, monkeypatch, state, "MSFT")
    assert state.attempts == attempts
    assert state.outcomes["research-MSFT-income-annual"]["status"] == "access_blocked"
    quarter = json.loads((tmp_path / "research-MSFT-income-quarter.json").read_text())
    assert quarter["source_receipts"] == []
    assert len(state.outcomes) == 15
    if code != 403:
        run_company_journey(research_offline_app, monkeypatch, state, "ORCL")
        assert state.attempts == attempts and len(state.outcomes) == 30
    else:
        assert state.outcomes["research-MSFT-balance-quarter"]["status"] == "verified"


def test_research_offline_peer_suggestions_are_separate(research_offline_app, research_fake_provider, monkeypatch):
    from live_financial_support import ResearchRunState

    state = ResearchRunState()
    case = research_case("MSFT", "peers", {"symbol": "MSFT", "limit": 5})
    result = execute_research_case(research_offline_app, monkeypatch, state, case)
    assert result is not None
    assert all(row["candidate_basis"] == "provider_suggestion" for row in result["rows"])
    assert {company["symbol"] for company in COMPANIES} == {"MSFT", "ORCL", "ADBE"}
    assert all(company["candidate_basis"] != "provider_suggestion" for company in COMPANIES)


@pytest.mark.parametrize("dataset", ["income", "balance", "cash"])
def test_research_offline_current_null_aliases_win(research_offline_app, research_fake_provider, monkeypatch, tmp_path, dataset):
    import json
    from live_financial_support import ResearchRunState

    def current_nulls(selected, period, payload):
        if selected == dataset:
            payload[0].update(fiscalYear=None, calendarYear="1999", filingDate=None, fillingDate="1999-01-01")
            payload[1].pop("fiscalYear")
            payload[1].pop("filingDate")
            payload[1].update(calendarYear="2024", fillingDate="2024-10-15")
    research_fake_provider["mutate"] = current_nulls
    state = ResearchRunState()
    case = next(case for case in company_cases("MSFT") if case["dataset"] == dataset and case["parameters"].get("period") == "annual")
    result = execute_research_case(research_offline_app, monkeypatch, state, case)
    assert result is not None
    receipt = json.loads((tmp_path / (case["case_id"] + ".json")).read_text())
    fiscal = [item for item in receipt["comparisons"] if item.get("field") == "fiscal_year" and "source_field" in item]
    filing = [item for item in receipt["comparisons"] if item.get("field") == "filing_date" and "source_field" in item]
    assert [(item["source_field"], item["source_state"], item["value"]) for item in fiscal] == [
        ("fiscalYear", "null", None), ("calendarYear", "value", "2024")]
    assert [(item["source_field"], item["source_state"]) for item in filing] == [("filingDate", "null"), ("fillingDate", "value")]


@pytest.mark.parametrize("scenario", ["annual_latest", "quarter_blocked"])
def test_research_offline_price_uses_latest_successful_ev(research_offline_app, research_fake_provider, monkeypatch, scenario):
    from live_financial_support import ResearchRunState

    if scenario == "annual_latest":
        def later_annual(dataset, period, payload):
            if dataset == "enterprise" and period == "annual":
                for row in payload:
                    row["date"] = "2025-12-31"
        research_fake_provider["mutate"] = later_annual
    else:
        research_fake_provider["failures"][("enterprise", "quarter")] = 403
    state = ResearchRunState()
    result = run_company_journey(research_offline_app, monkeypatch, state, "MSFT")
    reference = result["ev_reference"]
    assert reference["case_id"] == "research-MSFT-enterprise-annual"
    assert reference["date"] == ("2025-12-31" if scenario == "annual_latest" else "2025-06-30")
    assert state.outcomes[reference["case_id"]]["status"] == "verified"
    assert research_fake_provider["requests"][-1][0] == "prices"
    assert research_fake_provider["requests"][-1][1]["to"] == reference["date"]
    if scenario == "quarter_blocked":
        assert state.outcomes["research-MSFT-enterprise-quarter"]["status"] == "access_blocked"


@pytest.mark.parametrize("scenario,verified", [("short_exchange_conflict", False), ("missing_profile_exchange", False),
                                              ("observed_short_code_match", True)])
def test_research_offline_exchange_identity_before_success(research_offline_app, research_fake_provider, monkeypatch, tmp_path, scenario, verified):
    import json
    from live_financial_support import ResearchRunState

    def exchange_observations(dataset, period, payload):
        for row in payload:
            if dataset == "search":
                row["exchange"] = None if scenario == "short_exchange_conflict" else "Observed full exchange label"
                row["exchangeShortName"] = "NASDAQ"
            elif dataset == "profile":
                row["exchange"] = {"short_exchange_conflict": "NYSE", "missing_profile_exchange": None,
                                   "observed_short_code_match": "NASDAQ"}[scenario]
    research_fake_provider["mutate"] = exchange_observations
    state = ResearchRunState()
    result = run_company_journey(research_offline_app, monkeypatch, state, "MSFT")
    receipt = json.loads((tmp_path / "research-MSFT-profile.json").read_text())
    if verified:
        assert result["profile"] is not None and state.attempts == 15
        assert receipt["case_outcome"]["status"] == "verified"
    else:
        assert result["profile"] is None and state.attempts == 2
        assert receipt["case_outcome"]["status"] != "verified"
        assert receipt["case_outcome"]["missing_proof"]
        assert all(state.outcomes[case["case_id"]]["status"] != "verified" for case in company_cases("MSFT")[2:])
        assert state.outcomes["research-MSFT-prices"]["status"] != "verified"


@pytest.mark.parametrize("dataset,status,reason", [("search", 401, "authentication"), ("search", 429, "throttling"),
                                                  ("profile", 401, "authentication"), ("profile", 429, "throttling")])
def test_research_offline_blocked_identity_keeps_cause(research_offline_app, research_fake_provider, monkeypatch, tmp_path, dataset, status, reason):
    import json
    from live_financial_support import ResearchRunState

    research_fake_provider["failures"][dataset] = status
    state = ResearchRunState()
    run_company_journey(research_offline_app, monkeypatch, state, "MSFT")
    root_case = "research-MSFT-" + dataset
    assert state.outcomes[root_case]["status"] == "access_blocked"
    assert state.attempts == (1 if dataset == "search" else 2)
    blocked = [case["case_id"] for case in company_cases("MSFT") if case["case_id"] not in
               {"research-MSFT-search", root_case}] + ["research-MSFT-prices"]
    for case_id in blocked:
        receipt = json.loads((tmp_path / (case_id + ".json")).read_text())
        assert receipt["case_outcome"]["status"] == "access_blocked"
        assert receipt["case_outcome"]["reason"] == reason
        assert receipt["case_outcome"]["prerequisite"] == root_case
        assert receipt["source_receipts"] == [] and receipt["http_status"] is None
