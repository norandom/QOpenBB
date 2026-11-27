from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal
import gzip
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from events_documents_guard import Guard, Rejected, schedule
from events_documents_oracle import Discrepancy, compare_calendar, decode, decode_provider

SOURCE = b'[{"symbol":"MSFT","date":"2025-07-30","revenueActual":9007199254740993,"epsActual":0},{"symbol":"MSFT","date":"2025-07-30","revenueActual":22}]'
NORMALIZED = b'[{"symbol":"MSFT","report_date":"2025-07-30","revenue_actual":9007199254740993,"eps_actual":0},{"symbol":"MSFT","report_date":"2025-07-30","revenue_actual":22}]'
PLAN = decode(Path(__file__).with_name("events-documents-plan.json").read_bytes())


def request(wire):
    from urllib.parse import urlencode
    path, query = wire
    return SimpleNamespace(url="https://financialmodelingprep.com/stable/" + path + "?" +
                           urlencode({**query, "apikey": "do-not-retain"}), method="GET")


def observations():
    return [{"ordinal": index, "date": "2025-07-30", "fields": {
        "eps_actual": "0" if index == 0 else "Missing", "eps_consensus": "Missing",
        "revenue_actual": number, "revenue_consensus": "Missing"}}
        for index, number in enumerate(("9007199254740993", "22"))]


def test_exact_values_and_duplicate_date_ordinals():
    assert compare_calendar([{"symbol": "OTHER"}] * 251 + decode(SOURCE), decode(NORMALIZED), observations(), "MSFT") == {
        "eps_actual": 1, "eps_consensus": 0, "revenue_actual": 2, "revenue_consensus": 0}
    with pytest.raises(Discrepancy, match="provider installed value"):
        compare_calendar(decode(SOURCE), decode(NORMALIZED.replace(b"993", b"992")), observations(), "MSFT")
    wrong = observations()
    wrong[0]["ordinal"] = 1
    with pytest.raises(Discrepancy, match="row identity"):
        compare_calendar(decode(SOURCE), decode(NORMALIZED), wrong, "MSFT")
    wrong = observations()
    wrong[0]["fields"]["revenue_actual"] = "9007199254740992"
    with pytest.raises(Discrepancy, match="display value"):
        compare_calendar(decode(SOURCE), decode(NORMALIZED), wrong, "MSFT")


def test_guard_rejects_early_duplicate_background_and_offline(tmp_path):
    stages = schedule(PLAN)
    phase = tmp_path / "phase"
    phase.write_text("launch")
    guard = Guard(tmp_path / "live", phase, stages, live=True)
    with pytest.raises(Rejected):
        guard.reserve(request(stages["reopen"]["news"]))
    # Both issuer changes reach the same market endpoint with only the bounded dates.
    assert stages["launch"]["calendar"] == stages["listing"]["calendar"]
    assert set(stages["launch"]["calendar"][1]) == {"from", "to"}
    first = request(stages["launch"]["calendar"])
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = [pool.submit(guard.reserve, first) for _ in range(4)]
    assert sum(future.exception() is None for future in futures) == 1
    assert guard.count == 1
    assert "do-not-retain" not in (tmp_path / "live" / "ledger.json").read_text()
    offline = Guard(tmp_path / "offline", phase, stages, live=False)
    with pytest.raises(Rejected):
        offline.reserve(first)
    assert offline.count == 0


def test_failed_send_spends_reservation_before_socket_and_full_schedule_is_enforced(tmp_path):
    import asyncio

    phase = tmp_path / "phase"
    stages = schedule(PLAN)
    guard = Guard(tmp_path / "provider", phase, stages, live=True)
    attempted = []

    async def fail_after_reservation(req, connection):
        assert guard.count == len(attempted) + 1
        attempted.append(guard.count)
        raise ConnectionError("simulated transport failure")

    for stage, slots in stages.items():
        phase.write_text(stage)
        for outgoing in slots.values():
            with pytest.raises(ConnectionError):
                asyncio.run(guard.send(fail_after_reservation, request(outgoing), None))
    assert attempted == list(range(1, 17))
    with pytest.raises(Rejected):
        asyncio.run(guard.send(fail_after_reservation, request(stages["reopen"]["transcript"]), None))
    ledger = decode((tmp_path / "provider" / "ledger.json").read_bytes())
    assert ledger["count"] == 16
    assert ledger["denials"] == 1
    assert all(entry["status"] is None for entry in ledger["entries"])


def test_provider_and_wire_tolerance_does_not_round_decimal():
    assert decode(b'{"eps":0.1234567890123456789012345678901}')["eps"] == Decimal("0.1234567890123456789012345678901")
    assert type(decode(b'9007199254740993')) is int


def test_capture_preserves_original_body_bytes(tmp_path):
    import hashlib
    import stat

    phase = tmp_path / "phase"
    phase.write_text("launch")
    stages = schedule(PLAN)
    directory = tmp_path / "provider"
    guard = Guard(directory, phase, stages, live=True)
    number = guard.reserve(request(stages["launch"]["calendar"]))
    guard.observe(number, 200, SOURCE)
    private = directory / f"{number}.provider"
    assert private.read_bytes() == SOURCE
    assert stat.S_IMODE(private.stat().st_mode) == 0o600
    assert stat.S_IMODE(directory.stat().st_mode) == 0o700
    assert guard.entries[0]["sha256"] == hashlib.sha256(SOURCE).hexdigest()


def chart_observations():
    from copy import deepcopy

    units = "Currency per share · Currency Unknown · Source scale Unknown"
    revenue_units = "Monetary amount · Currency Unknown · Source scale Unknown"
    wire = b'[{"eps_actual":0,"eps_consensus":null},{"eps_actual":2.75,"eps_consensus":1.25}]'
    packed = decode(wire)
    tokens = json.loads(wire, parse_float=str, parse_int=str)
    rows = []
    for ordinal, record in enumerate(tokens):
        title = f"Report date 2025-07-30 · listing row {ordinal + 1}"
        unit_map = {"eps_actual": units, "eps_consensus": units, "revenue_actual": revenue_units,
                    "revenue_consensus": revenue_units}
        fields = {field: record.get(field) or "Missing" for field in unit_map}
        actual = {"category": "actual", "left": 18, "right": 21, "top": 148 if ordinal == 0 else 38,
                  "bottom": 149, "title": title, "units": units, "detail": "Actual EPS: " + fields["eps_actual"],
                  "identity": f"Receipt 9 · ordinal {ordinal} · eps_actual"}
        chart = {"measure": "eps", "display": "bar", "marks": [actual], "axisTitles": ["EPS per share"],
                 "categories": {"actual": Decimal("20.1"), "estimate": Decimal("60.1")},
                 "ticks": [{"value": "0", "y": 150}, {"value": "3", "y": 30}]}
        if ordinal:
            estimate = deepcopy(actual)
            estimate.update(category="estimate", left=58, right=61, top=100, detail="Estimated EPS: 1.25",
                            identity=f"Receipt 9 · ordinal {ordinal} · eps_consensus")
            chart["marks"].append(estimate)
        rows.append({"ordinal": ordinal, "date": "2025-07-30", "generation": "9",
                     "fields": fields, "fieldUnits": unit_map, "charts": [chart]})
    return packed, tokens, rows


@pytest.mark.parametrize(("mutation", "reason"), [
    ("swap", "chart mark identity"),
    ("null", "chart mark coverage"),
    ("zero", "chart mark coverage"),
    ("duplicate_date", "chart mark identity"),
    ("plot_scale", "chart plotted value"),
    ("tooltip_token", "chart mark exact value"),
])
def test_chart_oracle_detects_mutations(mutation, reason):
    from copy import deepcopy
    from events_documents_oracle import compare_marks

    packed, tokens, rows = chart_observations()
    compare_marks(packed, tokens, rows, {})
    first, second = [row["charts"][0]["marks"] for row in rows]
    if mutation == "swap":
        second[0]["identity"], second[1]["identity"] = second[1]["identity"], second[0]["identity"]
    elif mutation == "null":
        first.append(deepcopy(second[1]))
    elif mutation == "zero":
        first.clear()
    elif mutation == "duplicate_date":
        first[0]["identity"] = second[0]["identity"]
    elif mutation == "plot_scale":
        second[0]["top"] += 12
    else:
        second[0]["detail"] = "Actual EPS: 2.750"
    with pytest.raises(Discrepancy, match=reason):
        compare_marks(packed, tokens, rows, {})


def test_provider_decoder_preserves_tokens_under_gzip():
    payload = b'[{"epsActual":0.123456789012345678901,"revenueActual":9007199254740993}]'
    expected = [{"epsActual": Decimal("0.123456789012345678901"), "revenueActual": 9007199254740993}]
    assert decode_provider(payload) == decode_provider(gzip.compress(payload)) == expected


def test_targeted_live_schedule_keeps_its_four_send_ceiling(tmp_path):
    plan = decode(Path(__file__).with_name("events-documents-four-input-plan.json").read_bytes())
    stages = schedule(plan)
    phase = tmp_path / "phase"
    phase.write_text("launch")
    guard = Guard(tmp_path / "captures", phase, stages, live=True)
    for number, query in enumerate(stages["launch"].values(), 1):
        assert guard.reserve(request(query)) == number
    with pytest.raises(Rejected):
        guard.reserve(request(stages["launch"]["calendar"]))
    assert guard.count == 4
