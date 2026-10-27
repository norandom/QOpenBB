"""Project fixed historical observations into the reviewed gallery column contract."""
from copy import deepcopy
from decimal import Decimal, localcontext


MONTHS = ("2024-10", "2024-11", "2024-12", "2025-01")
BILLION = Decimal(10**9)
RETROSPECTIVE = "Retrieved retrospectively; not a January 2025 point-in-time vintage."
PRICE_LIMIT = "Quoted close price changes, not total returns; provider price basis not independently verified."
FUNDAMENTAL_LIMIT = "Reported fiscal quarters; amounts scaled from original USD without intermediate rounding."
COMPONENTS = (("costOfRevenue", "Cost of revenue"), ("grossProfit", "Gross profit"))
LEVELS = (("revenue", "Revenue"), ("grossProfit", "Gross profit"),
          ("operatingIncome", "Operating income"), ("incomeBeforeTax", "Income before tax"),
          ("netIncome", "Net income"))
RECIPES = {
    "january-prices": ("Selected equities: January 2025 daily closes (USD/share)",
                       "Chronological provider close; trading dates retained; no forward fill."),
    "monthly-returns": ("Selected equities: October 2024-January 2025 price returns (%)",
                        "100 * (last close in month / last close before month - 1)."),
    "daily-returns": ("Selected equities: October 2024-January 2025 daily price returns (%)",
                      "100 * (close / previous trading-day close - 1); repeated raw observations."),
    "january-relationships": ("Selected equities: January 2025 volatility, return and activity",
                              "Sample SD of January daily returns (n-1); January compounded price return; mean(close * volume)."),
    "revenue-components": ("Apple (AAPL) FY2024 quarterly revenue components (USD bn)",
                           "Cost of revenue and gross profit / 1e9; disjoint components sum to revenue. Normalized charts divide each by their sum."),
    "latest-revenue-components": ("Apple (AAPL) FY2025 Q1 revenue components (USD bn)",
                                  "Cost of revenue and gross profit / 1e9; disjoint components sum to revenue."),
    "seasonal-revenue": ("Apple (AAPL) FY2022-FY2024 quarterly revenue (USD bn)",
                         "Reported revenue / 1e9; common Q1-Q4 categories across fiscal years."),
    "revenue-hierarchy": ("Apple (AAPL) FY2024 revenue hierarchy (USD bn)",
                          "Cost/gross leaves / 1e9; fiscal year and quarter parents derived by sum, never duplicated as leaves."),
    "income-bridge": ("Apple (AAPL) FY2025 Q1 revenue to net income (USD bn)",
                       "(revenue - cost - operating expenses + signed other income/expense - tax) / 1e9 = net income / 1e9."),
    "revenue-flow": ("Apple (AAPL) FY2024 derived revenue allocation (USD bn)",
                     "Sum quarterly revenue -> quarter -> disjoint cost/gross components; divide original USD by 1e9."),
    "income-levels": ("Apple (AAPL) FY2025 Q1 reported income levels (USD bn)",
                       "Reported revenue, gross profit, operating income, pretax income and net income / 1e9; overlapping levels."),
    "income-combinations": ("Apple (AAPL) FY2024 Q1-FY2025 Q1 revenue, net income and basic EPS",
                            "Revenue and net income / 1e9; reported basic EPS remains USD/share on the custom right axis."),
}


def number(value):
    if value is None:
        return None
    result = Decimal(str(value))
    if not result.is_finite():
        raise ValueError("non-finite financial input")
    return result


def ratio(current, previous):
    return None if current is None or previous in (None, 0) else 100 * (current / previous - 1)


def price_series(rows, symbol):
    selected = sorted(rows, key=lambda row: row["date"])
    dates = [row["date"] for row in selected]
    if len(dates) != len(set(dates)):
        raise ValueError("duplicate trading date")
    if any(row.get("symbol") != symbol or not "2024-09-30" <= row["date"] <= "2025-01-31"
           for row in selected):
        raise ValueError("price symbol/window differs from frozen capture")
    return [{"date": row["date"], "close": number(row.get("close")),
             "volume": number(row.get("volume"))} for row in selected]


def return_rows(series, symbol, company):
    result = []
    previous = None
    for row in series:
        if row["date"][:7] in MONTHS:
            result.append({"date": row["date"], "month": row["date"][:7], "symbol": symbol,
                           "company": company, "dailyReturnPct": ratio(row["close"], previous)})
        previous = row["close"]
    return result


def monthly_row(series, symbol, company):
    result = {"symbol": symbol, "company": company}
    for month in MONTHS:
        inside = [row for row in series if row["date"][:7] == month]
        before = [row for row in series if row["date"][:7] < month]
        result["return" + month.replace("-", "")] = ratio(
            inside[-1]["close"] if inside else None, before[-1]["close"] if before else None)
    return result


def relationship(series, daily, monthly):
    returns = [r["dailyReturnPct"] for r in daily
               if r["month"] == "2025-01" and r["dailyReturnPct"] is not None]
    sd = None
    if len(returns) >= 2:
        mean = sum(returns) / len(returns)
        sd = (sum((r - mean) ** 2 for r in returns) / (len(returns) - 1)).sqrt()
    activity = [r["close"] * r["volume"] for r in series
                if r["date"][:7] == "2025-01" and r["close"] is not None and r["volume"] is not None]
    return {"symbol": monthly["symbol"], "company": monthly["company"], "volatilityPct": sd,
            "januaryReturnPct": monthly["return202501"],
            "meanDollarActivity": sum(activity) / len(activity) if activity else None}


def project_prices(prices, companies):
    daily, monthly, relations, by_symbol = [], [], [], {}
    for symbol, company in companies.items():
        series = price_series(prices[symbol], symbol)
        observations = return_rows(series, symbol, company)
        month = monthly_row(series, symbol, company)
        by_symbol[symbol] = {row["date"]: row["close"] for row in series}
        daily.extend(observations)
        monthly.append(month)
        relations.append(relationship(series, observations, month))
    dates = sorted({date for series in by_symbol.values() for date in series if date[:7] == "2025-01"})
    january = [{"date": date, **{symbol: series.get(date) for symbol, series in by_symbol.items()}}
               for date in dates]
    return {"january-prices": january, "monthly-returns": monthly,
            "daily-returns": sorted(daily, key=lambda row: (row["date"], list(companies).index(row["symbol"]))),
            "january-relationships": relations}


def fiscal_rows(rows):
    selected = {}
    for row in rows:
        key = (str(row.get("fiscalYear")), row.get("period"))
        if key[0] in ("2022", "2023", "2024") or key == ("2025", "Q1"):
            if key in selected or row.get("symbol") != "AAPL" or row.get("reportedCurrency") != "USD":
                raise ValueError("duplicate fiscal period or wrong company/currency")
            selected[key] = row
    expected = {(str(year), f"Q{q}") for year in range(2022, 2025) for q in range(1, 5)} | {("2025", "Q1")}
    if set(selected) != expected:
        raise ValueError("missing required fiscal quarter")
    for row in selected.values():
        validate_income(row)
    return selected


def validate_income(row):
    r = {field: number(row[field]) for field in
         ("revenue", "costOfRevenue", "grossProfit", "operatingExpenses", "operatingIncome",
          "totalOtherIncomeExpensesNet", "incomeBeforeTax", "incomeTaxExpense", "netIncome", "eps")}
    if any(value is None for value in r.values()):
        raise ValueError("missing required income amount")
    if not (r["revenue"] - r["costOfRevenue"] == r["grossProfit"]
            and r["grossProfit"] - r["operatingExpenses"] == r["operatingIncome"]
            and r["operatingIncome"] + r["totalOtherIncomeExpensesNet"] == r["incomeBeforeTax"]
            and r["incomeBeforeTax"] - r["incomeTaxExpense"] == r["netIncome"]):
        raise ValueError("income identity does not reconcile in original USD")


def scaled(row, field):
    return number(row[field]) / BILLION


def project_income(rows):
    fiscal = fiscal_rows(rows)
    quarters = [fiscal[("2024", f"Q{q}")] for q in range(1, 5)]
    latest = fiscal[("2025", "Q1")]
    components, hierarchy, flow = [], [], []
    for row in quarters:
        quarter = row["period"]
        components.append({"fiscalQuarter": quarter, **{field: scaled(row, field) for field, _ in COMPONENTS}})
        flow.append({"source": "FY2024 revenue", "target": quarter, "value": scaled(row, "revenue")})
        for field, label in COMPONENTS:
            hierarchy.append({"fiscalYear": "FY2024", "fiscalQuarter": quarter,
                              "component": label, "amount": scaled(row, field)})
            flow.append({"source": quarter, "target": quarter + " " + label, "value": scaled(row, field)})
    movements = (("revenue", "Revenue", 1), ("costOfRevenue", "Cost of revenue", -1),
                 ("operatingExpenses", "Operating expenses", -1),
                 ("totalOtherIncomeExpensesNet", "Other income/expense", 1), ("incomeTaxExpense", "Income tax", -1))
    return {
        "revenue-components": components,
        "latest-revenue-components": [{"component": label, "amount": scaled(latest, field)} for field, label in COMPONENTS],
        "seasonal-revenue": [{"fiscalQuarter": f"Q{q}", **{
            f"revenueFY{year}": scaled(fiscal[(str(year), f"Q{q}")], "revenue")
            for year in range(2022, 2025)}} for q in range(1, 5)],
        "revenue-hierarchy": hierarchy,
        "income-bridge": [{"stage": label, "movement": sign * scaled(latest, field)} for field, label, sign in movements],
        "revenue-flow": flow,
        "income-levels": [{"level": label, "amount": scaled(latest, field)} for field, label in LEVELS],
        "income-combinations": [{"fiscalQuarter": f"FY{row['fiscalYear']} {row['period']}",
                                 "revenue": scaled(row, "revenue"), "netIncome": scaled(row, "netIncome"),
                                 "basicEps": number(row["eps"])} for row in [*quarters, latest]],
    }


def observation_period(dataset_id, rows):
    if dataset_id in ("january-prices", "monthly-returns", "daily-returns", "january-relationships"):
        dates = [row["date"] for row in rows]
        return min(dates), max(dates)
    years = {"seasonal-revenue": ("2022", "2023", "2024"),
             "latest-revenue-components": ("2025",), "income-bridge": ("2025",), "income-levels": ("2025",),
             "income-combinations": ("2024", "2025")}.get(dataset_id, ("2024",))
    dates = [row["date"] for row in rows if str(row["fiscalYear"]) in years]
    return min(dates), max(dates)


def dataset_metadata(dataset_id, contract, sources, raw_rows):
    title, transformation = RECIPES[dataset_id]
    is_price = dataset_id in ("january-prices", "monthly-returns", "daily-returns", "january-relationships")
    start, end = observation_period(dataset_id, raw_rows)
    limitations = [RETROSPECTIVE, PRICE_LIMIT if is_price else FUNDAMENTAL_LIMIT]
    if dataset_id == "january-relationships":
        limitations.append("Volatility is not annualized. Mean close times volume is an activity proxy, not market capitalization or executed notional.")
    if dataset_id == "revenue-flow":
        limitations.append("Derived income allocation, not cash flow.")
    if dataset_id == "income-levels":
        limitations.append("Overlapping reported levels cannot be summed or interpreted as conversion or allocation.")
    if dataset_id == "daily-returns":
        limitations.append("Ranges are observed min/max, not OHLC or confidence limits; box quartiles interpolate at (n-1)*p with observed min/max whiskers.")
    if is_price:
        limitations.append("Missing prices remain null; missing previous close prevents return calculation. Fewer than two returns leaves volatility null.")
    return {"id": dataset_id, "title": title,
            "sourceIds": [source["id"] for source in sources if (source["id"] != "fmp-income-AAPL") == is_price],
            "observationStart": start, "observationEnd": end,
            "columns": deepcopy(contract["datasets"][dataset_id]["columns"]),
            "transformation": transformation, "limitations": limitations}


def json_numbers(value):
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, dict):
        return {key: json_numbers(item) for key, item in value.items()}
    if isinstance(value, list):
        return [json_numbers(item) for item in value]
    return value


def project_data(contract, prices, fundamentals, sources):
    with localcontext() as context:
        context.prec = 40
        projected = {**project_prices(prices, contract["companies"]), **project_income(fundamentals)}
        bins = contract["charts"]["histogram"]["state"]["chartModel"]["chartOptions"]["histogram"]["series"]["bins"]
        apple = [r["dailyReturnPct"] for r in projected["daily-returns"]
                 if r["symbol"] == "AAPL" and r["dailyReturnPct"] is not None]
        if any(not Decimal(str(bins[0][0])) <= value <= Decimal(str(bins[-1][1])) for value in apple):
            raise ValueError("Apple return outside frozen histogram edges")
        datasets = {}
        for dataset_id in contract["datasets"]:
            rows = projected[dataset_id]
            fields = [column["field"] for column in contract["datasets"][dataset_id]["columns"]]
            if any(list(row) != fields for row in rows):
                raise ValueError("projection differs from frozen column order")
            period_rows = list(fiscal_rows(fundamentals).values())
            if dataset_id in ("january-prices", "january-relationships"):
                period_rows = projected["january-prices"]
            elif dataset_id in ("monthly-returns", "daily-returns"):
                period_rows = projected["daily-returns"]
            datasets[dataset_id] = {"results": rows, "metadata": dataset_metadata(
                dataset_id, contract, sources, period_rows)}
        return json_numbers({"schemaVersion": 1, "snapshotId": contract["snapshotId"],
                             "sources": sources, "datasets": datasets})
