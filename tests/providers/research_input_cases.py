"""Bounded research sample and source aliases; no acquisition or financial formulas."""

COMPANIES = (
    {"symbol": "MSFT", "name": "Microsoft", "candidate_basis": "primary_company",
     "rationale": "Nonfinancial software/cloud issuer anchors the input assessment.",
     "differences": "Cloud, productivity and gaming mix; June fiscal year-end."},
    {"symbol": "ORCL", "name": "Oracle", "candidate_basis": "analyst_selected_candidate",
     "rationale": "Enterprise software and cloud provide a candidate operating comparison.",
     "differences": "Database/infrastructure mix, leverage and acquisitions; May fiscal year-end."},
    {"symbol": "ADBE", "name": "Adobe", "candidate_basis": "analyst_selected_candidate",
     "rationale": "Subscription software provides a second candidate operating comparison.",
     "differences": "Creative/document applications, acquisition and stock compensation treatment; 52/53-week fiscal calendar."},
)

STATEMENT_FIELDS = {"symbol": "symbol", "period_ending": "date", "fiscal_period": "period",
                    "fiscal_year": "fiscalYear", "filing_date": "filingDate",
                    "reported_currency": "reportedCurrency"}
PERIOD_FIELDS = {"symbol": "symbol", "period_ending": "date", "fiscal_period": "period",
                 "fiscal_year": "fiscalYear", "currency": "reportedCurrency"}
MAPPINGS = {
    "search": {"symbol": "symbol", "name": "name", "exchange": "exchange",
               "exchange_short_name": "exchangeShortName", "currency": "currency"},
    "profile": {"symbol": "symbol", "name": "companyName", "stock_exchange": "exchange",
                "currency": "currency", "last_price": "price"},
    "peers": {"symbol": "symbol", "name": "companyName", "exchange": "exchange",
              "exchange_short_name": "exchangeShortName", "currency": "currency"},
    "income": {**STATEMENT_FIELDS, "revenue": "revenue", "total_operating_income": "operatingIncome",
               "consolidated_net_income": "netIncome", "depreciation_and_amortization": "depreciationAndAmortization",
               "ebitda": "ebitda", "weighted_average_basic_shares_outstanding": "weightedAverageShsOut",
               "weighted_average_diluted_shares_outstanding": "weightedAverageShsOutDil"},
    "balance": {**STATEMENT_FIELDS, "total_assets": "totalAssets", "total_liabilities": "totalLiabilities",
                "cash_and_cash_equivalents": "cashAndCashEquivalents", "total_debt": "totalDebt",
                "short_term_debt": "shortTermDebt", "long_term_debt": "longTermDebt",
                "net_receivables": "netReceivables", "inventory": "inventory", "accounts_payable": "accountPayables",
                "total_current_assets": "totalCurrentAssets", "total_current_liabilities": "totalCurrentLiabilities",
                "capital_lease_obligations": "capitalLeaseObligations", "minority_interest": "minorityInterest",
                "preferred_stock": "preferredStock", "common_stock": "commonStock"},
    "cash": {**STATEMENT_FIELDS, "net_income": "netIncome", "depreciation_and_amortization": "depreciationAndAmortization",
             "net_cash_from_operating_activities": "netCashProvidedByOperatingActivities",
             "operating_cash_flow": "operatingCashFlow", "capital_expenditure": "capitalExpenditure",
             "purchase_of_property_plant_and_equipment": "investmentsInPropertyPlantAndEquipment",
             "change_in_working_capital": "changeInWorkingCapital",
             "change_in_account_receivables": "accountsReceivables", "change_in_inventory": "inventory",
             "change_in_account_payable": "accountsPayables", "free_cash_flow": "freeCashFlow",
             "cash_at_end_of_period": "cashAtEndOfPeriod"},
    "metrics": {**PERIOD_FIELDS, "market_cap": "marketCap", "enterprise_value": "enterpriseValue",
                "ev_to_sales": "evToSales", "ev_to_ebitda": "evToEBITDA",
                "ev_to_operating_cash_flow": "evToOperatingCashFlow", "ev_to_free_cash_flow": "evToFreeCashFlow",
                "working_capital": "workingCapital"},
    "ratios": {**PERIOD_FIELDS, "price_to_earnings": "priceToEarningsRatio",
               "price_to_book": "priceToBookRatio", "net_profit_margin": "netProfitMargin"},
    "enterprise": {"symbol": "symbol", "date": "date", "currency": "reportedCurrency", "stock_price": "stockPrice",
                   "number_of_shares": "numberOfShares", "market_cap": "marketCapitalization",
                   "cash_and_cash_equivalents": "minusCashAndCashEquivalents", "total_debt": "addTotalDebt",
                   "enterprise_value": "enterpriseValue"},
    "prices": {"date": "date", "open": "open", "high": "high", "low": "low", "close": "close", "volume": "volume"},
}
ROUTES = {"search": "/equity/search", "profile": "/equity/profile", "peers": "/equity/compare/peers",
          "prices": "/equity/price/historical", **{dataset: "/equity/fundamental/" + route for dataset, route in
          (("income", "income"), ("balance", "balance"), ("cash", "cash"), ("metrics", "metrics"),
           ("ratios", "ratios"), ("enterprise", "enterprise_values"))}}


def research_case(symbol, dataset, parameters, suffix=None):
    return {"case_id": "research-" + symbol + "-" + dataset + ("-" + suffix if suffix else ""),
            "dataset": dataset, "company_symbol": symbol, "route": ROUTES[dataset],
            "parameters": dict(parameters), "field_mapping": dict(MAPPINGS[dataset]),
            "expected_checks": ("source_equality", "dataset_semantics", "unknown_conventions")}


def company_cases(symbol):
    company = next(item for item in COMPANIES if item["symbol"] == symbol)
    cases = [research_case(symbol, "search", {"query": company["name"], "limit": 5}),
             research_case(symbol, "profile", {"symbol": symbol})]
    for dataset in ("income", "balance", "cash", "metrics", "ratios", "enterprise"):
        for period, limit in (("annual", 2), ("quarter", 4)):
            parameters = {"symbol": symbol, "period": period, "limit": limit}
            if dataset in {"metrics", "ratios"}:
                parameters["ttm"] = "exclude"
            cases.append(research_case(symbol, dataset, parameters, period))
    return cases
