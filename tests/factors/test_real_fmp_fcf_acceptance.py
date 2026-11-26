"""Verify captured FMP observations through the signed installed FCF listener."""

import json
from datetime import UTC, datetime, time
from decimal import Decimal, localcontext
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest
from qopenbb_data.modeling.contracts import AssumptionSet, InputSnapshot
from test_model_identity import assertion
from test_model_listener import exchange, internal_listener

EVIDENCE = (
    Path(__file__).resolve().parents[2] / "verification" / "financial-real-inputs"
)


def load_file(name):
    return json.loads((EVIDENCE / name).read_text())


def load(name):
    return load_file(f"aapl-{name}.json")


REGISTRY = load_file("journey-inputs.json")
CASES = REGISTRY["cases"]


def registered_case(case):
    entry = CASES[case]
    return load_file(entry["request"]), load_file(entry["expected"])[
        entry["expected_key"]
    ]


@pytest.fixture(scope="module")
def run_dir(tmp_path_factory):
    return tmp_path_factory.mktemp("real-fmp-fcf")


def test_capture_reconciles_with_requests_and_independent_decimal_oracle():
    capture = load("fmp-capture")
    flow = capture["cash_flow"]["selected"]
    historical = capture["market_value"]["selected"]
    quote = capture["quote"]["selected"]
    for case in ("quote", "strict"):
        flows, cap = load(f"{case}-request")["inputs"]["tables"]
        operating, capital = flows["rows"]
        (denominator,) = cap["rows"]
        assert (
            operating["observation_date"] == capital["observation_date"] == flow["date"]
        )
        assert denominator["observation_date"] == historical["date"]
        market = quote if case == "quote" else historical
        assert Decimal(operating["value"]) == flow["operatingCashFlow"]
        assert Decimal(capital["value"]) == flow["capitalExpenditure"]
        assert Decimal(denominator["value"]) == market["marketCap"]
    fcf = flow["operatingCashFlow"] + flow["capitalExpenditure"]
    assert fcf == flow["freeCashFlow"] == 136_056_000_000
    with localcontext() as context:
        context.prec = 70
        value = (Decimal(100 * fcf) / Decimal(quote["marketCap"])).quantize(
            Decimal("1e-37")
        )
    assert value == Decimal(load("expected")["quote"]["value"])


def test_quote_timing_and_currency_are_explicit():
    capture = load("fmp-capture")
    quote = capture["quote"]["selected"]
    profile = capture["profile"]["selected"]
    assert (quote["symbol"], quote["exchange"]) == (
        profile["symbol"],
        profile["exchange"],
    )
    assert quote["marketCap"] == profile["marketCap"]
    assert profile["cik"] == capture["cash_flow"]["selected"]["cik"]
    request = load("quote-request")
    inputs = InputSnapshot.model_validate(request["inputs"])
    (market,) = inputs.tables[1].rows
    quote_time = datetime.fromtimestamp(quote["timestamp"], UTC)
    quote_retrieval = datetime.fromisoformat(capture["quote"]["retrieved_at"])
    session_zone = ZoneInfo(inputs.cutoff.session_timezone)
    assert market.published_at == inputs.cutoff.decision_at == quote_time
    assert market.observation_date == quote_time.astimezone(session_zone).date()
    assert quote_retrieval.astimezone(session_zone).date() > market.observation_date
    assert (
        inputs.cutoff.evaluated_at == inputs.provenance.retrieved_at >= quote_retrieval
    )
    assert market.context.currency == profile["currency"] == "USD"
    assert market.context.vintage_coverage is None
    assert not inputs.cutoff.is_eligible(
        market.model_copy(update={"published_at": quote_retrieval})
    )


def test_sap_receipt_bounds_and_decimal_oracle():
    assert REGISTRY["default_case"] == "sap-de-live"
    request, expected = registered_case(REGISTRY["default_case"])
    capture = load_file("sap-de-fmp-capture.json")
    inputs = InputSnapshot.model_validate(request["inputs"])
    operating, capex = inputs.tables[0].rows
    (market,) = inputs.tables[1].rows
    flow = capture["cash-flow-statement"]["selected"]
    quote = capture["quote"]["selected"]
    profile = capture["profile"]["selected"]
    assert operating.value == flow["operatingCashFlow"] == 9_156_000_000
    assert capex.value == flow["capitalExpenditure"] == -739_000_000
    assert (
        str(operating.observation_date) == str(capex.observation_date) == flow["date"]
    )
    assert market.value == quote["marketCap"] == profile["marketCap"]
    assert (
        operating.entity_id
        == capex.entity_id
        == market.entity_id
        == quote["symbol"]
        == profile["symbol"]
    )
    assert (
        operating.context.currency
        == capex.context.currency
        == market.context.currency
        == profile["currency"]
        == flow["reportedCurrency"]
        == "EUR"
    )
    assert profile["exchange"] == quote["exchange"] == "XETRA"
    quote_time = datetime.fromtimestamp(quote["timestamp"], UTC)
    quote_receipt = datetime.fromisoformat(capture["quote"]["retrieved_at"])
    assembly = max(
        datetime.fromisoformat(source["retrieved_at"]) for source in capture.values()
    )
    cutoff = inputs.cutoff
    zone = ZoneInfo(cutoff.session_timezone)
    assert market.published_at == quote_receipt
    assert (
        cutoff.decision_at
        == cutoff.evaluated_at
        == inputs.provenance.retrieved_at
        == assembly
    )
    for moment in (quote_time, quote_receipt, assembly):
        local = moment.astimezone(zone)
        assert local.date() == cutoff.observation_date == market.observation_date
        assert time(9) <= local.time() < time(17, 30)
    assert quote_time < quote_receipt <= assembly
    assert all(cutoff.is_eligible(row) for row in (operating, capex, market))
    with localcontext() as context:
        context.prec = 70
        fcf = operating.value + capex.value
        assert fcf == flow["freeCashFlow"] == 8_417_000_000
        assert (100 * fcf / market.value).quantize(Decimal("1e-37")) == Decimal(
            expected["value"]
        )


@pytest.mark.parametrize("case", (*CASES, "apple-quote-event"))
def test_installed_fcf_signed_evaluation_and_reopen(case, run_dir):
    if case == "apple-quote-event":
        request, expected = load("quote-request"), load("expected")["quote"]
    else:
        request, expected = registered_case(case)
    with internal_listener(run_dir) as origin:
        owner = assertion(claims={"sub": "fmp_acceptance_analyst"})
        status, run = exchange(
            origin + "/modeling/v1/evaluations",
            owner,
            payload=json.dumps(request).encode(),
        )
        assert status == 200, run
    (output,) = run["outputs"]
    (reference,) = run["verification"]
    (check,) = run["checks"]
    assert run["inputs"] == InputSnapshot.model_validate(request["inputs"]).model_dump(
        mode="json"
    )
    assert run["assumptions"] == AssumptionSet.model_validate(
        request["assumptions"]
    ).model_dump(mode="json")
    assert {key: output[key] for key in ("value", "unit", "status")} == {
        key: expected[key] for key in ("value", "unit", "status")
    }
    assert reference["status"] == expected["reference_status"]
    assert reference["reference_version"] == "1"
    assert check["status"] == expected["check_status"]
    assert run["trace"] == ([expected["trace"]] if expected["trace"] else [])
    if expected["status"] == "withheld":
        assert output["reason"] and not output["trace_ids"]
    with internal_listener(run_dir) as origin:
        fresh_owner = assertion(claims={"sub": "fmp_acceptance_analyst"})
        path = f"{origin}/modeling/v1/runs/{run['run_id']}"
        assert exchange(path, fresh_owner) == (200, run)
