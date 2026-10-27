"""Independent financial checks for offline historical gallery projections."""
from copy import deepcopy
from datetime import date, datetime
from decimal import Decimal, localcontext
import hashlib
import json
import math
from pathlib import Path
import statistics

import pytest

from qopenbb_ci.gallery_cli import canonical, load_inputs, main, source_record, verified_raw
from qopenbb_ci.gallery_projection import project_data

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = json.loads((ROOT / "contracts/gallery/chart-state.json").read_text())
DATA = json.loads((ROOT / "contracts/gallery/data.json").read_text())


@pytest.fixture
def inputs():
    prices = {symbol: [{"symbol": symbol, "date": day, "close": close, "volume": volume}
                       for day, close, volume in (("2024-09-30", 100, 10), ("2024-10-31", 101, 20),
                         ("2024-11-29", 102, 30), ("2024-12-31", 103, 40),
                         ("2025-01-02", 104, 50), ("2025-01-31", 105, 60))]
              for symbol in CONTRACT["companies"]}
    income = []
    for year, quarters in ((2022, range(1, 5)), (2023, range(1, 5)), (2024, range(1, 5)), (2025, [1])):
        for quarter in quarters:
            income.append({"symbol": "AAPL", "reportedCurrency": "USD", "fiscalYear": str(year),
                           "period": f"Q{quarter}", "date": f"{year}-{quarter * 3:02}-25",
                           "revenue": 100_000_000_000 + quarter * 1_000_000_000,
                           "costOfRevenue": 60_000_000_000 + quarter * 1_000_000_000,
                           "grossProfit": 40_000_000_000, "operatingExpenses": 10_000_000_000,
                           "operatingIncome": 30_000_000_000, "totalOtherIncomeExpensesNet": -100_000_000,
                           "incomeBeforeTax": 29_900_000_000, "incomeTaxExpense": 4_900_000_000,
                           "netIncome": 25_000_000_000, "eps": 1.23})
    return prices, income, [{"id": "fmp-prices-" + s} for s in prices] + [{"id": "fmp-income-AAPL"}]


def test_projection_matches_independent_decimal_returns_sd_activity(inputs):
    prices, income, sources = inputs
    data = project_data(CONTRACT, *inputs)["datasets"]
    with localcontext() as context:
        context.prec = 50
        january = [Decimal(100) * (Decimal(104) / 103 - 1), Decimal(100) * (Decimal(105) / 104 - 1)]
        for row in data["monthly-returns"]["results"]:
            assert row["return202501"] == pytest.approx(float(Decimal(100) * (Decimal(105) / 103 - 1)), abs=1e-12)
        relation = data["january-relationships"]["results"][0]
        assert relation["volatilityPct"] == pytest.approx(float(abs(january[1] - january[0]) / Decimal(2).sqrt()), abs=1e-12)
        assert relation["meanDollarActivity"] == (104 * 50 + 105 * 60) / 2
        daily = [r["dailyReturnPct"] for r in data["daily-returns"]["results"] if r["symbol"] == "AAPL"]
        for actual, previous, current in zip(daily, prices["AAPL"], prices["AAPL"][1:]):
            assert actual == pytest.approx(100 * (current["close"] / previous["close"] - 1), abs=1e-12)
    assert data["monthly-returns"]["metadata"]["observationStart"] == "2024-10-31"
    assert data["income-levels"]["metadata"]["observationEnd"] == "2025-03-25"
    assert data["income-bridge"]["results"][3]["movement"] == -0.1
    assert sum(r["movement"] for r in data["income-bridge"]["results"]) == pytest.approx(25)


def test_missing_values_remain_missing_and_volatility_requires_two_observations(inputs):
    prices, _, _ = inputs
    prices["AAPL"][3]["close"] = None
    prices["AAPL"][4]["close"] = None
    projected = project_data(CONTRACT, *inputs)["datasets"]
    relation = projected["january-relationships"]["results"][0]
    assert relation["januaryReturnPct"] is None
    assert relation["volatilityPct"] is None
    assert relation["meanDollarActivity"] == 105 * 60
    assert projected["january-prices"]["results"][0]["AAPL"] is None
    assert all(r["dailyReturnPct"] is None for r in projected["daily-returns"]["results"]
               if r["symbol"] == "AAPL" and r["month"] == "2025-01")


@pytest.mark.parametrize("mutation", ["missing-quarter", "identity", "currency", "duplicate", "nonfinite", "histogram"])
def test_invalid_financial_inputs_fail_explicitly(inputs, mutation):
    prices, income, sources = inputs
    if mutation == "missing-quarter":
        income.pop()
    elif mutation == "identity":
        income[0]["netIncome"] += 1
    elif mutation == "currency":
        income[0]["reportedCurrency"] = "EUR"
    elif mutation == "duplicate":
        prices["AAPL"].append(prices["AAPL"][0])
    elif mutation == "nonfinite":
        prices["AAPL"][0]["close"] = float("inf")
    else:
        prices["AAPL"][-1]["close"] = 200
    with pytest.raises(ValueError):
        project_data(CONTRACT, prices, income, sources)


def test_packaged_six_equity_references_and_distribution_totals():
    # References were calculated separately with 40-digit Decimal from retained source bytes.
    expected = {
        "AAPL": (-5.758326012299337, 1.9239270038199813, 14007968186.4935),
        "MSFT": (-1.527876631079478, 2.108834364235506, 9896272643.898),
        "NVDA": (-10.589023754561025, 5.370270938777041, 39405474739.2885),
        "AMZN": (8.336751903003783, 1.3865920214442524, 7460241891.906),
        "GOOGL": (7.776016904384575, 1.7176418638540534, 4894250817.973),
        "META": (17.705931581014842, 1.760061869604419, 10169287740.3135),
    }
    relationships = {r["symbol"]: r for r in DATA["datasets"]["january-relationships"]["results"]}
    daily = DATA["datasets"]["daily-returns"]["results"]
    assert len(daily) == 6 * 84
    for symbol in CONTRACT["companies"]:
        rows = [r for r in daily if r["symbol"] == symbol]
        assert len(rows) == 84
        january = [r["dailyReturnPct"] for r in rows if r["month"] == "2025-01"]
        assert len(january) == 20
        assert relationships[symbol]["volatilityPct"] == pytest.approx(statistics.stdev(january), rel=1e-12)
        compounded = 100 * (math.prod(1 + r / 100 for r in january) - 1)
        assert relationships[symbol]["januaryReturnPct"] == pytest.approx(compounded, abs=1e-11)
    for symbol, values in expected.items():
        actual = relationships[symbol]
        assert [actual[k] for k in ("januaryReturnPct", "volatilityPct", "meanDollarActivity")] == pytest.approx(values, rel=1e-12)
    apple = [r["dailyReturnPct"] for r in daily if r["symbol"] == "AAPL"]
    bins = CONTRACT["charts"]["histogram"]["state"]["chartModel"]["chartOptions"]["histogram"]["series"]["bins"]
    counts = [sum(lower <= x < upper or (i == len(bins) - 1 and x == upper) for x in apple)
              for i, (lower, upper) in enumerate(bins)]
    assert sum(counts) == 84
    assert min(apple) == pytest.approx(-4.040021860680203)
    assert max(apple) == pytest.approx(3.6543983294179066)
    quartiles = statistics.quantiles(apple, n=4, method="inclusive")
    assert len(quartiles) == 3 and min(apple) <= quartiles[0] <= quartiles[2] <= max(apple)


def test_packaged_income_reconciliation_hierarchy_and_flow():
    datasets = DATA["datasets"]
    components = datasets["revenue-components"]["results"]
    hierarchy = datasets["revenue-hierarchy"]["results"]
    flow = datasets["revenue-flow"]["results"]
    assert [round((r["costOfRevenue"] + r["grossProfit"]) * 1e9) for r in components] == [119575000000, 90753000000, 85777000000, 94930000000]
    for component in components:
        quarter = component["fiscalQuarter"]
        total = component["costOfRevenue"] + component["grossProfit"]
        assert sum(r["amount"] for r in hierarchy if r["fiscalQuarter"] == quarter) == pytest.approx(total)
        assert sum(r["value"] for r in flow if r["source"] == quarter) == pytest.approx(total)
        assert sum(r["value"] for r in flow if r["target"] == quarter) == pytest.approx(total)
        assert component["costOfRevenue"] / total + component["grossProfit"] / total == pytest.approx(1)
    bridge = datasets["income-bridge"]["results"]
    assert len(bridge) == 5
    assert round(sum(Decimal(str(r["movement"])) for r in bridge) * 10**9) == 36330000000
    levels = datasets["income-levels"]["results"]
    assert [r["level"] for r in levels] == ["Revenue", "Gross profit", "Operating income", "Income before tax", "Net income"]
    assert round(levels[-1]["amount"] * 1e9) == 36330000000
    assert datasets["income-levels"]["metadata"]["observationEnd"] == "2024-12-28"
    assert datasets["seasonal-revenue"]["metadata"]["observationStart"] == "2021-12-25"


def test_packaged_envelope_provenance_and_selected_columns_only():
    assert set(DATA) == {"schemaVersion", "snapshotId", "sources", "datasets"}
    assert DATA["schemaVersion"] == 1 and DATA["snapshotId"] == CONTRACT["snapshotId"]
    assert set(DATA["datasets"]) == set(CONTRACT["datasets"])
    for dataset_id, dataset in DATA["datasets"].items():
        assert set(dataset) == {"results", "metadata"}
        metadata = dataset["metadata"]
        assert set(metadata) == {"id", "title", "sourceIds", "observationStart", "observationEnd", "columns", "transformation", "limitations"}
        assert metadata["columns"] == CONTRACT["datasets"][dataset_id]["columns"]
        assert metadata["sourceIds"]
        assert isinstance(metadata["transformation"], str) and all(isinstance(x, str) for x in metadata["limitations"])
        date.fromisoformat(metadata["observationStart"])
        date.fromisoformat(metadata["observationEnd"])
        assert all(list(row) == [c["field"] for c in metadata["columns"]] for row in dataset["results"])
    assert len(DATA["sources"]) == 7
    for source in DATA["sources"]:
        assert set(source) == {"id", "provider", "endpoint", "parameters", "retrievedAt", "sha256", "limitations"}
        assert datetime.fromisoformat(source["retrievedAt"]).tzinfo is not None
        assert len(source["sha256"]) == 64 and isinstance(source["limitations"], list)
    assert DATA["sources"][-1]["retrievedAt"] == "2026-10-20T14:06:05.149732+00:00"
    payload = canonical(DATA).decode().lower()
    for excluded in ("raw_path", "apikey", "api_key", "accepteddate", "vwap", "cik", "artifacts/", "artifacts\\"):
        assert excluded not in payload


def test_source_hash_timezone_and_endpoint_guards(tmp_path):
    raw = tmp_path / "rows.json"
    raw.write_text('[{"close":1}]')
    sha = hashlib.sha256(raw.read_bytes()).hexdigest()
    assert verified_raw(tmp_path, "rows.json", sha) == [{"close": 1}]
    with pytest.raises(ValueError, match="SHA-256"):
        verified_raw(tmp_path, "rows.json", "0" * 64)
    source = {"retrieved_at_utc": "2026-10-20T14:06:05+00:00", "raw_sha256": sha,
              "endpoint": "https://financialmodelingprep.com/stable/income-statement"}
    assert source_record("test", source, {})["sha256"] == sha
    source["retrieved_at_utc"] = "2026-10-20T14:06:05"
    with pytest.raises(ValueError, match="timezone"):
        source_record("test", source, {})
    source["retrieved_at_utc"] += "+00:00"
    source["endpoint"] += "?apikey=credential"
    with pytest.raises(ValueError, match="endpoint"):
        source_record("test", source, {})


def test_cli_rejects_unreviewed_fixture_before_reading_sources(tmp_path):
    fixture = tmp_path / "chart-state.json"
    fixture.write_text("{}")
    with pytest.raises(ValueError, match="reviewed HG0"):
        load_inputs(fixture, tmp_path / "absent", tmp_path / "absent", tmp_path)


def test_cli_serialization_is_deterministic_and_finite(inputs):
    first = canonical(project_data(CONTRACT, *inputs))
    assert first == canonical(project_data(deepcopy(CONTRACT), *deepcopy(inputs)))
    assert first.endswith(b"\n")
    with pytest.raises(ValueError):
        canonical({"value": float("nan")})


def test_portable_cli_generates_twice_and_rejects_changed_capture(inputs, tmp_path):
    prices, income, _ = inputs
    records = []
    for symbol, rows in prices.items():
        path = tmp_path / (symbol + ".json")
        path.write_bytes(canonical(rows))
        records.append({"symbol": symbol, "raw_path": path.name,
                        "raw_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                        "endpoint": "https://financialmodelingprep.com/stable/historical-price-eod/full",
                        "retrieved_at_utc": "2026-10-27T14:00:35+01:00",
                        "parameters": {"symbol": symbol, "from": "2024-09-30", "to": "2025-01-31"}})
    raw_income = tmp_path / "income.json"
    raw_income.write_bytes(canonical(income))
    provenance = tmp_path / "sources.json"
    provenance.write_bytes(canonical({"prices": records}))
    fundamental_source = tmp_path / "fundamentals.json"
    fundamental_source.write_bytes(canonical({"source_raw_path": raw_income.name,
        "raw_sha256": hashlib.sha256(raw_income.read_bytes()).hexdigest(),
        "retrieved_at_utc": "2026-10-20T14:06:05+00:00",
        "endpoint": "https://financialmodelingprep.com/stable/income-statement",
        "parameters": {"symbol": "AAPL", "period": "quarter", "limit": "40"}}))
    output = tmp_path / "output"
    args = ["--chart-state", str(ROOT / "contracts/gallery/chart-state.json"), "--sources", str(provenance),
            "--fundamentals", str(fundamental_source), "--root", str(tmp_path), "--output", str(output)]
    assert main(args) == 0
    first = {path.name: path.read_bytes() for path in output.iterdir()}
    assert main(args) == 0
    assert first == {path.name: path.read_bytes() for path in output.iterdir()}
    (tmp_path / "AAPL.json").write_text("[]")
    with pytest.raises(SystemExit) as error:
        main(args)
    assert error.value.code == 1
    assert first == {path.name: path.read_bytes() for path in output.iterdir()}
