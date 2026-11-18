"""Cross-asset and macro input record: every planned input is listed and none is over-claimed.

The record states what each ETF or FRED series is, what its prices mean, how much history this
installation received and whether it may be shown. An input counts as usable in a story only when
it is verified and its display status permits showing it.
"""
import hashlib
import json
from copy import deepcopy
from pathlib import Path

import jsonschema
import pytest

ROOT = Path(__file__).resolve().parents[2]
MATRIX = json.loads((ROOT / "tests/contracts/fixtures/cross_asset_inputs/matrix.json").read_text(encoding="utf-8"))
SCHEMA = json.loads((ROOT / "schemas/cross-asset-inputs.schema.json").read_text(encoding="utf-8"))
ETFS = ["XLK", "DBC", "GLD", "XLE", "XLB", "SPY"]
SERIES = ["DFII10", "T10Y2Y", "T10YIE", "DTWEXBGS", "DCOILWTICO", "DHHNGSP", "STLFSI4", "NFCI"]
PRICE, PROFILE, FRED_SERIES = "/api/v1/equity/price/historical", "/api/v1/equity/profile", "/api/v1/economy/fred_series"
FMP_HOST, FRED_HOST = "financialmodelingprep.com", "api.stlouisfed.org"
WINDOWS = {"recent": ("2026-08-03", "2026-11-13"), "early": ("2007-01-03", "2011-12-30")}
# A fund is recorded as a fund or as unknown, never as the thing it tracks.
FUND_TYPES = {"etf", "fund", "unknown"}


def canonical_sha256(value):
    """Identity of a JSON document independent of line endings and key order."""
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def record():
    return json.loads((ROOT / "docs/reference/cross-asset-inputs.json").read_text(encoding="utf-8"))


def check(value):
    """Schema validity plus the claims a schema cannot express."""
    jsonschema.validate(value, SCHEMA)
    inputs = {item["id"]: item for item in value["inputs"]}
    assert set(inputs) == set(ETFS) | set(SERIES) and len(value["inputs"]) == 14
    for name, item in inputs.items():
        fund = name in ETFS
        assert item["provider"] == ("fmp" if fund else "fred")
        assert item["route"] == (PRICE if fund else FRED_SERIES)
        assert ("price_basis" in item) == fund
        status, verified = item["display_status"]["status"], item["verification"]["status"] == "verified"
        if item["usable_in_stories"]:
            assert verified and status in {"government-source", "provider-licensed"}
        if verified:
            assert status != "unknown" and "provenance" in item
            assert "earliest" in item["history"] and "latest" in item["history"]
        if fund:
            assert status in {"provider-licensed", "unknown"}
            assert item["identity"].get("instrument_type") in FUND_TYPES


def expected_calls():
    calls = []
    for kind, (start, end) in WINDOWS.items():
        for symbol in ETFS:
            calls.append((f"{symbol}-{kind}", symbol, "fmp", PRICE, {"provider": "fmp", "symbol": symbol,
                "start_date": start, "end_date": end, "interval": "1d", "adjustment": "splits_only"},
                [(FMP_HOST, "/stable/historical-price-eod/full")]))
    for symbol in ETFS:
        calls.append((f"{symbol}-identity", symbol, "fmp", PROFILE, {"provider": "fmp", "symbol": symbol},
                      [(FMP_HOST, "/stable/profile")]))
    for series in SERIES:
        # Each FRED series call sends observations and then metadata; the cache is bypassed.
        calls.append((f"{series}-series", series, "fred", FRED_SERIES,
                      {"provider": "fred", "symbol": series, "use_cache": False},
                      [(FRED_HOST, "/fred/series/observations"), (FRED_HOST, "/fred/series")]))
    return calls


def test_frozen_matrix_is_exactly_the_approved_calls_and_their_provider_sends():
    actual = [(call["id"], call["input"], call["provider"], call["route"], call["params"],
               [(send["host"], send["path"]) for send in call["sends"]]) for call in MATRIX["calls"]]
    assert actual == expected_calls() and len(actual) == 26
    assert all(call["purpose"] and all(send["purpose"] for send in call["sends"]) for call in MATRIX["calls"])
    sends = {provider: sum(len(call["sends"]) for call in MATRIX["calls"] if call["provider"] == provider)
             for provider in ("fmp", "fred")}
    assert sends == MATRIX["planned_sends"] == {"fmp": 18, "fred": 16}
    assert MATRIX["allowed_hosts"] == {"fmp": FMP_HOST, "fred": FRED_HOST}
    # A provider retry would be an unplanned send.
    assert MATRIX["runtime_environment"] == {"OPENBB_FRED_MAX_RETRIES": "0"}
    assert MATRIX["image_digest"] == "sha256:3db18506631972b3a3a176f45069cdac6574af7c35543e261ce7153b58ed25e4"


def test_matrix_routes_exist_in_the_served_contract():
    paths = json.loads((ROOT / "contracts/openapi.json").read_text(encoding="utf-8"))["paths"]
    for call in MATRIX["calls"]:
        names = {parameter["name"] for parameter in paths[call["route"]]["get"]["parameters"]}
        assert set(call["params"]) <= names, call["id"]


def test_record_lists_all_inputs_and_binds_the_frozen_matrix():
    value = record()
    check(value)
    assert value["matrix_sha256"] == canonical_sha256(MATRIX)
    assert "FRED® API" in value["notice"]


PROOF = {"status": "verified", "checked_on": "2026-11-18", "image_digest": "sha256:" + "0" * 64,
         "evidence_sha256": {"capture": "0" * 64}}
HISTORY = {"earliest": "2007-01-03", "latest": "2026-11-13"}
PROVENANCE = {"retrieved_at": "2026-11-18T12:00:00+00:00", "effective_query": {"symbol": "GLD"}}
LICENSED = {"status": "provider-licensed", "basis": "provider price history"}


def verified_gld(value):
    item = next(entry for entry in value["inputs"] if entry["id"] == "GLD")
    item.update(verification=deepcopy(PROOF), history=deepcopy(HISTORY), provenance=deepcopy(PROVENANCE),
                display_status=deepcopy(LICENSED), usable_in_stories=True)
    item["identity"]["instrument_type"] = "etf"
    return item


def test_a_complete_verified_input_is_accepted():
    value = record()
    verified_gld(value)
    check(value)


MUTATIONS = {
    "copyrighted-usable": lambda item, value: item.update(display_status={"status": "third-party-copyrighted", "basis": "copyright marker"}),
    "government-source-etf": lambda item, value: item.update(display_status={"status": "government-source", "basis": "claimed"}),
    "unverified-usable": lambda item, value: item.update(verification={"status": "unverified"}),
    "unknown-status-verified": lambda item, value: item.update(display_status={"status": "unknown", "basis": "none"}, usable_in_stories=False),
    "verified-without-evidence": lambda item, value: item["verification"].pop("evidence_sha256"),
    "verified-empty-evidence": lambda item, value: item["verification"].update(evidence_sha256={}),
    "verified-without-digest": lambda item, value: item["verification"].pop("image_digest"),
    "verified-without-date": lambda item, value: item["verification"].pop("checked_on"),
    "free-text-date": lambda item, value: item["verification"].update(checked_on="yesterday"),
    "boolean-history": lambda item, value: item["history"].update(earliest=True),
    "verified-without-history": lambda item, value: item.update(history={}),
    "verified-without-provenance": lambda item, value: item.pop("provenance"),
    "empty-basis": lambda item, value: item["display_status"].update(basis=""),
    "wrong-route": lambda item, value: item.update(route=FRED_SERIES),
    "etf-as-spot": lambda item, value: item["identity"].update(instrument_type="Spot commodity"),
    "etf-as-index": lambda item, value: item["identity"].update(instrument_type="Index"),
    "etf-as-bullion": lambda item, value: item["identity"].update(instrument_type="Gold bullion"),
    "etf-without-type": lambda item, value: item["identity"].pop("instrument_type"),
    "missing-input": lambda item, value: value["inputs"].remove(item),
    "duplicate-input": lambda item, value: value["inputs"].__setitem__(0, deepcopy(item)),
}


@pytest.mark.parametrize("mutation", sorted(MUTATIONS))
def test_record_rejects_over_claims(mutation):
    value = record()
    item = verified_gld(value)
    MUTATIONS[mutation](item, value)
    with pytest.raises((AssertionError, jsonschema.ValidationError)):
        check(value)
