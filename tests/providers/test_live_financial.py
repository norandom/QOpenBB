"""Opt-in real financial inputs; synthetic edge tests remain separate acceptance evidence."""
import os

import pytest
from live_financial_support import (
    ROOT,
    SourceCapture,
    call,
    equal,
    evidence,
    metadata,
    pairs,
    require,
    success,
    unit,
    unknown_valuation_bases,
    validate_rows,
)

pytestmark = [pytest.mark.live, pytest.mark.skipif(
    os.environ.get("QOPENBB_LIVE_ACCEPTANCE") != "1", reason="real provider acceptance is opt-in")]

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


def test_missing_and_invalid_inputs_stop_before_provider_io(live_app, monkeypatch):
    capture = SourceCapture(monkeypatch, "fmp")
    for parameters in ({"symbol": "MSFT"}, {"provider": "fmp"},
                       {"provider": "fmp", "symbol": "MSFT", "limit": -1}):
        status, _ = call(live_app, "/api/v1/equity/fundamental/balance", parameters)
        require(status in {400, 422}, "missing/invalid financial input rejected")
    require(capture.attempts == 0, "invalid input has no provider request")
