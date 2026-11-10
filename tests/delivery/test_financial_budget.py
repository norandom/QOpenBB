"""Offline admission proofs; no provider, container, or browser traffic."""

import asyncio
import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

SOURCE = Path(__file__).with_name("financial_budget.py")


def helper():
    spec = importlib.util.spec_from_file_location("financial_budget", SOURCE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def request(url):
    from urllib.parse import urlsplit
    return SimpleNamespace(method="GET", url=urlsplit(url))


FMP = "https://financialmodelingprep.com/stable/profile?symbol=AAPL&apikey=SECRET"
FRED = "https://api.stlouisfed.org/fred/series?series_id=GDP&file_type=json&api_key=SECRET"


@pytest.mark.parametrize("suffix", [
    "profile?symbol=AAP&apikey=SECRET",
    "income-statement?symbol=AAP&period=annual&limit=5&apikey=SECRET",
    "income-statement?symbol=AAP&period=quarter&limit=10&apikey=SECRET",
])
def test_raw_aap_selection_reserves_existing_company_endpoints(tmp_path, suffix):
    m = helper()
    guard = m.Budget(tmp_path / "ledger", "approved-run", "initial")
    guard.initialize({"fmp": 24, "fred": 2})
    guard.reserve(request("https://financialmodelingprep.com/stable/" + suffix))
    assert json.loads(guard.path.read_text())["counts"] == {"fmp": 25, "fred": 2}
    assert m.MAXIMA == {"fmp": 80, "fred": 16}


@pytest.mark.parametrize("suffix", [
    "profile?symbol=TSLA&apikey=SECRET",
    "income-statement?symbol=TSLA&period=annual&limit=5&apikey=SECRET",
    "balance-sheet-statement?symbol=AAP&period=annual&limit=5&apikey=SECRET",
    "income-statement?symbol=AAP&period=annual&limit=100&apikey=SECRET",
    "income-statement?symbol=AAP&period=monthly&limit=5&apikey=SECRET",
    "profile?symbol=AAP&apikey=SECRET&limit=5",
])
def test_raw_aap_selection_preserves_destination_boundaries(tmp_path, suffix):
    m = helper()
    guard = m.Budget(tmp_path / "ledger", "approved-run", "initial")
    guard.initialize({"fmp": 24, "fred": 2})
    with pytest.raises(m.BudgetDenied, match="destination"):
        guard.reserve(request("https://financialmodelingprep.com/stable/" + suffix))
    assert json.loads(guard.path.read_text())["counts"] == {"fmp": 24, "fred": 2}


def test_ceiling_concurrency_failed_sends_and_recreation(tmp_path):
    m = helper()
    ledger = tmp_path / "ledger.json"
    guard = m.Budget(ledger, "approved-run", "initial")
    guard.initialize({"fmp": 79, "fred": 15})
    calls = []

    async def send(req, connection):
        calls.append(connection)
        raise ConnectionError("synthetic")

    async def attempt():
        with pytest.raises((ConnectionError, m.BudgetDenied)):
            await guard.send(send, request(FMP), "connection")

    async def concurrent():
        await asyncio.gather(*(attempt() for _ in range(8)))

    asyncio.run(concurrent())
    assert len(calls) == 1
    snapshot = m.checked_snapshot(ledger.read_text(), "approved-run", {"fmp": 79, "fred": 15})
    assert snapshot["counts"] == {"fmp": 80, "fred": 15}
    ledger.unlink()
    reopened = m.Budget(ledger, "approved-run", "reopen")
    reopened.initialize(snapshot["counts"])
    with pytest.raises(m.BudgetDenied):
        asyncio.run(reopened.send(send, request(FMP), "reopened"))
    assert len(calls) == 1
    with pytest.raises(ConnectionError):
        asyncio.run(reopened.send(send, request(FRED), "fred"))
    assert json.loads(ledger.read_text())["counts"] == {"fmp": 80, "fred": 16}
    assert "SECRET" not in ledger.read_text()


@pytest.mark.parametrize("url", [
    FMP.replace("financialmodelingprep.com", "financialmodelingprep.com.evil"),
    FMP.replace("https:", "http:"), FMP.replace("AAPL", "TSLA"),
    FMP + "&symbol=MSFT", FMP + "&unknown=SECRET", FMP.replace("profile", "ratios"),
    FRED.replace("GDP", "CPI"), FMP.replace(".com/", ".com:8443/"),
])
def test_destinations_and_queries_deny_before_send(tmp_path, url):
    m = helper()
    guard = m.Budget(tmp_path / "ledger", "approved-run", "initial")
    guard.initialize({"fmp": 0, "fred": 0})
    with pytest.raises(m.BudgetDenied, match="destination"):
        guard.reserve(request(url))
    assert guard.path.read_text().find("SECRET") == -1


def test_missing_malformed_persistence_and_monotonicity_fail_closed(tmp_path, monkeypatch):
    m = helper()
    guard = m.Budget(tmp_path / "ledger", "approved-run", "initial")
    with pytest.raises(m.BudgetDenied):
        guard.reserve(request(FMP))
    guard.initialize({"fmp": 0, "fred": 0})
    with pytest.raises(m.BudgetDenied):
        guard.initialize({"fmp": 0, "fred": 0})
    monkeypatch.setattr(m.os, "replace", lambda *_: (_ for _ in ()).throw(OSError("secret")))
    with pytest.raises(m.BudgetDenied, match="persistence"):
        guard.reserve(request(FMP))
    with pytest.raises(m.BudgetDenied, match="process"):
        guard.reserve(request(FMP))
    guard = m.Budget(guard.path, "approved-run", "initial")
    guard.path.write_text("{malformed SECRET")
    with pytest.raises(m.BudgetDenied, match="ledger"):
        guard.reserve(request(FMP))
    with pytest.raises(m.BudgetDenied):
        m.checked_snapshot('{}', "approved-run", {"fmp": 1, "fred": 0})


def test_redirect_and_retry_each_debit_actual_send(tmp_path):
    m = helper()
    guard = m.Budget(tmp_path / "ledger", "approved-run", "initial")
    guard.initialize({"fmp": 0, "fred": 0})
    async def send(req, connection):
        return connection
    for step in ("initial", "redirect-1", "redirect-2", "persistent-retry"):
        assert asyncio.run(guard.send(send, request(FMP), step)) == step
    assert json.loads(guard.path.read_text())["counts"]["fmp"] == 4


def test_bootstrap_requires_single_process_and_checked_snapshot(tmp_path):
    m = helper()
    with pytest.raises(ValueError):
        m.bootstrap("run", "initial", {"fmp": 0, "fred": 0}, ["-m", "uvicorn", "app:app", "--reload"])
    code = m.bootstrap("run", "initial", {"fmp": 0, "fred": 0}, ["-m", "uvicorn", "app:app", "--workers", "1"])
    assert code.index("install_guard(") < code.rindex("runpy.run_module(")
    assert "SECRET" not in code


def test_install_before_startup_and_reject_second_install(tmp_path, monkeypatch):
    import sys
    m = helper()
    calls = []

    class ClientRequest:
        async def send(self, connection):
            calls.append(connection)
            return "sent"

    monkeypatch.setitem(sys.modules, "aiohttp", SimpleNamespace(
        __version__="3.14.5", ClientRequest=ClientRequest))
    monkeypatch.setenv("OPENBB_FRED_MAX_RETRIES", "0")
    monkeypatch.setenv("WEB_CONCURRENCY", "1")
    monkeypatch.setattr(m, "LEDGER", str(tmp_path / "ledger"))
    m.install_guard("approved-run", "initial", {"fmp": 79, "fred": 0})
    req = ClientRequest()
    req.method, req.url = "GET", request(FMP).url
    assert asyncio.run(req.send("normal")) == "sent"
    with pytest.raises(m.BudgetDenied):
        asyncio.run(req.send("over-limit"))
    assert calls == ["normal"]
    with pytest.raises(m.BudgetDenied):
        m.install_guard("approved-run", "initial", {"fmp": 0, "fred": 0})


def test_exact_source_queries_and_override(tmp_path):
    m = helper()
    guard = m.Budget(tmp_path / "ledger", "approved-run", "initial")
    guard.initialize({"fmp": 0, "fred": 0})
    urls = [FMP, FMP.replace("AAPL", "MSFT"), FRED,
            "https://financialmodelingprep.com/stable/search-name?query=Microsoft&limit=20&apikey=SECRET",
            "https://financialmodelingprep.com/stable/search-symbol?query=AAP&limit=20&apikey=SECRET",
            "https://financialmodelingprep.com/stable/income-statement?symbol=MSFT&period=annual&limit=5&apikey=SECRET",
            "https://financialmodelingprep.com/stable/income-statement?symbol=AAPL&period=quarter&limit=5&apikey=SECRET",
            FRED.replace("/series?", "/series/observations?") + "&limit=100000&aggregation_method=eop"]
    for url in urls:
        guard.reserve(request(url))
    original = ["uvicorn", "qopenbb_data.app:create_app", "--factory", "--host",
                "0.0.0.0", "--port", "6900", "--no-access-log"]
    spec = m.entrypoint_override("python", "approved-run", "initial", {"fmp": 0, "fred": 0}, original)
    assert spec["entrypoint"][:2] == ["python", "-c"]
    assert spec["command"] == [] and len(spec["sha256"]) == 64
    with pytest.raises(ValueError):
        m.entrypoint_override("python", "run", "initial", {"fmp": 0, "fred": 0}, original + ["--reload"])


def test_bootstrap_installs_before_uvicorn_and_fails_before_app(tmp_path, monkeypatch):
    import runpy
    import sys
    m = helper()

    class ClientRequest:
        async def send(self, connection):
            return "synthetic"

    monkeypatch.setitem(sys.modules, "aiohttp", SimpleNamespace(
        __version__="3.14.5", ClientRequest=ClientRequest))
    monkeypatch.setenv("OPENBB_FRED_MAX_RETRIES", "0")
    monkeypatch.setenv("WEB_CONCURRENCY", "1")
    monkeypatch.setenv("UVICORN_WORKERS", "1")
    monkeypatch.setenv("UVICORN_RELOAD", "false")
    ledger = tmp_path / "ledger"
    started = []

    def start(module, run_name):
        assert module == "uvicorn" and run_name == "__main__"
        assert ClientRequest.send._financial_guard
        assert json.loads(ledger.read_text())["counts"] == {"fmp": 4, "fred": 2}
        started.append(True)

    monkeypatch.setattr(runpy, "run_module", start)
    code = m.bootstrap("run", "reopen", {"fmp": 4, "fred": 2}, ["-m", "uvicorn", "app:app"])
    code = code.replace(repr(m.LEDGER), repr(str(ledger))).replace('"' + m.LEDGER + '"', repr(str(ledger)))
    exec(compile(code, "reviewed-acceptance-bootstrap", "exec"), {})
    assert started == [True]
    monkeypatch.setenv("UVICORN_WORKERS", "2")
    with pytest.raises(RuntimeError, match="process"):
        exec(compile(code, "reviewed-acceptance-bootstrap", "exec"), {})
    assert started == [True]


def test_snapshot_wrong_run_regression_and_child_process_denied(tmp_path, monkeypatch):
    m = helper()
    guard = m.Budget(tmp_path / "ledger", "run", "initial")
    guard.initialize({"fmp": 7, "fred": 2})
    for run, minimum in [("other", {"fmp": 0, "fred": 0}), ("run", {"fmp": 8, "fred": 2})]:
        with pytest.raises(m.BudgetDenied):
            m.checked_snapshot(guard.path.read_text(), run, minimum)
    monkeypatch.setattr(m.os, "getpid", lambda: guard.pid + 1)
    with pytest.raises(m.BudgetDenied, match="process"):
        guard.reserve(request(FMP))
    assert json.loads(guard.path.read_text())["counts"] == {"fmp": 7, "fred": 2}
