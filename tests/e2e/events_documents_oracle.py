"""Independent comparison of private same-send wire captures and visible observations."""

import argparse
from collections import Counter
from datetime import datetime
from decimal import Decimal, InvalidOperation
import gzip
import hashlib
import json
from pathlib import Path
import re

from events_documents_guard import schedule

FIELDS = {"eps_actual": "epsActual", "eps_consensus": "epsEstimated",
          "revenue_actual": "revenueActual", "revenue_consensus": "revenueEstimated"}
DOCUMENTS = {
    "filings": {"symbol": "symbol", "filing_date": "filingDate", "accepted_date": "acceptedDate",
                "report_type": "formType", "cik": "cik", "filing_url": "link", "report_url": "finalLink"},
    "news": {"symbol": "symbol", "date": "publishedDate", "title": "title", "source": "site",
             "publisher": "publisher", "excerpt": "text", "url": "url"},
    "transcript": {"symbol": "symbol", "year": "year", "quarter": "period", "content": "content"},
}
SAFE_CODES = {"authentication", "entitlement", "throttling", "timeout", "missing_data",
              "invalid_response", "upstream", "internal_error", "invalid_parameters"}


class Discrepancy(AssertionError):
    """Only predefined comparison labels may enter public diagnostics."""


def check(condition, label):
    if not condition:
        raise Discrepancy(label)


def decode(body):
    def reject_constant(_):
        raise Discrepancy("invalid JSON number")

    return json.loads(body, parse_float=Decimal, parse_constant=reject_constant)


def decode_provider(body):
    # The transport exposes compressed bytes when the installed client disables decompression.
    return decode(gzip.decompress(body) if body.startswith(b"\x1f\x8b") else body)


def numeric(value):
    check(type(value) in (int, Decimal), "wire value type")
    return Decimal(value)


def matching_calendar(source, symbol):
    check(isinstance(source, list), "provider calendar shape")
    return [row for row in source if row["symbol"].upper() == symbol]


def compare_calendar(source, installed, visible, symbol):
    matches = matching_calendar(source, symbol)
    check(len(installed) == min(250, len(matches)), "listing count")
    coverage = dict.fromkeys(FIELDS, 0)
    expected = []
    for ordinal, (raw, normal) in enumerate(zip(matches, installed)):
        day = raw["date"]
        check(normal["report_date"] == day and normal["symbol"] == symbol, "provider installed row")
        check(normal.get("last_updated") == raw.get("lastUpdated"), "provider installed update date")
        for field, origin in FIELDS.items():
            before, after = raw.get(origin), normal.get(field)
            if before is None or after is None:
                check(before is after, "provider installed missing value")
            else:
                check(numeric(before) == numeric(after), "provider installed value")
        expected.append((ordinal, day, normal))
    check(len(expected) == len(visible), "issuer row count")
    for (ordinal, day, normal), shown in zip(expected, visible):
        check((ordinal, day) == (shown["ordinal"], shown["date"]), "display row identity")
        if "updated" in shown:
            check(shown["updated"] == (normal.get("last_updated") or "Unknown"), "display update date")
        for field in FIELDS:
            value, text = normal.get(field), shown["fields"][field]
            if value is None:
                check(text == "Missing", "display missing value")
            else:
                check(bool(re.fullmatch(r"-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?", text)), "display value format")
                check(numeric(value) == Decimal(text), "display value")
                coverage[field] += 1
    return coverage



LABELS = {"eps_actual": "Actual EPS", "eps_consensus": "Estimated EPS",
          "revenue_actual": "Actual revenue", "revenue_consensus": "Estimated revenue"}


def plot_position(chart, value, mark):
    """Recover the physical data coordinate from the chart's painted axis labels."""
    ticks = sorted((Decimal(tick["value"]), Decimal(str(tick["y"]))) for tick in chart["ticks"])
    check(len(ticks) >= 2, "calendar chart axis labels")
    low, high = ticks[0], ticks[-1]
    check(low[0] < high[0] and low[1] > high[1], "calendar chart axis scale")
    y = low[1] + (numeric(value) - low[0]) * (high[1] - low[1]) / (high[0] - low[0])
    actual_plot = (mark["top"] + mark["bottom"] + 1) / 2
    if chart["display"] == "bar" and value != 0:
        actual_plot = mark["top"] if value > 0 else mark["bottom"] + 1
    check(abs(y - Decimal(str(actual_plot))) <= 4, "calendar chart plotted value")


def source_units(normal, metadata, field):
    properties = metadata.get(field, {})
    unit = properties.get("unit") or ("currency_per_share" if field.startswith("eps") else "currency")
    unit = {"currency_per_share": "Currency per share", "currency": "Monetary amount"}.get(unit, unit)
    currency = normal.get(properties["currency_field"]) if properties.get("currency_field") else properties.get("currency")
    scale = properties.get("scale")
    return f"{unit} · Currency {currency or 'Unknown'} · Source scale {scale if scale is not None else 'Unknown'}"


def compare_marks(installed, token_rows, visible, metadata):
    for row in visible:
        ordinal = row["ordinal"]
        normal, tokens = installed[ordinal], token_rows[ordinal]
        charts = {chart["measure"]: chart for chart in row["charts"]}
        present = {measure for measure in ("eps", "revenue")
                   if any(key.startswith(measure) and normal.get(key) is not None for key in FIELDS)}
        check(set(charts) == present and len(charts) == len(row["charts"]), "calendar measure coverage")
        for field in FIELDS:
            value = normal.get(field)
            check(row["fieldUnits"][field] == source_units(normal, metadata, field), "calendar source units")
            if value is not None:
                check(row["fields"][field] == tokens[field], "calendar displayed exact token")
        for measure, chart in charts.items():
            check(chart["display"] in ("bar", "point"), "calendar chart display")
            axis = "EPS per share" if measure == "eps" else "Revenue (monetary amount)"
            check(chart["axisTitles"] == [axis], "calendar chart axis unit")
            fields = {category: f"{measure}_{suffix}" for category, suffix in
                      (("actual", "actual"), ("estimate", "consensus")) if normal.get(f"{measure}_{suffix}") is not None}
            marks = chart["marks"]
            check(Counter(mark["category"] for mark in marks) == Counter(fields.keys()), "calendar chart mark coverage")
            for mark in marks:
                field = fields[mark["category"]]
                check(mark["identity"] == f"Receipt {row['generation']} · ordinal {ordinal} · {field}", "calendar chart mark identity")
                check(mark["title"] == f"Report date {row['date']} · listing row {ordinal + 1}", "calendar chart mark row")
                check(mark["detail"] == f"{LABELS[field]}: {tokens[field]}", "calendar chart mark exact value")
                check(mark["units"] == row["fieldUnits"][field], "calendar chart mark units")
                x = Decimal(mark["left"] + mark["right"] + 1) / 2
                check(abs(x - chart["categories"][mark["category"]]) <= 3, "calendar chart mark category")
                plot_position(chart, normal[field], mark)

def clock(value):
    return datetime.fromisoformat(value) if value and len(value) > 10 else value


def expected_document(slot, raw):
    fields = {field: raw.get(source) for field, source in DOCUMENTS[slot].items()}
    if slot == "filings":
        fields["accepted_date"] = clock(fields["accepted_date"])
        if fields["filing_date"].endswith(" 00:00:00"):
            fields["filing_date"] = fields["filing_date"][:10]
        fields["content_status"] = "metadata_only"
    elif slot == "news":
        fields["date"] = clock(fields["date"])
        fields["content_status"] = "partial" if (fields["excerpt"] or "").strip() else "metadata_only"
    else:
        fields["date"] = raw["date"][:10]
        fields["event_datetime"] = clock(raw["date"]) if len(raw["date"]) > 10 else None
        fields["content_status"] = "completeness_unknown"
    return fields


def compare_documents(slot, source, installed, query):
    size = 1 if slot == "transcript" else query["limit"]
    if slot == "transcript":
        check(len(source) <= 1, "duplicate provider transcript")
    check(isinstance(source, list) and len(installed) == min(size, len(source)), "document count")
    for raw, normal in zip(source, installed):
        check(raw["symbol"].upper() == query["symbol"], "document issuer")
        if slot == "transcript":
            check(raw["year"] == query["year"] and raw["period"] == f"Q{query['quarter']}", "document period")
        expected_fields = expected_document(slot, raw)
        expected_fields["symbol"] = query["symbol"]
        for field, expected in expected_fields.items():
            observed = normal.get(field)
            if field in ("accepted_date", "event_datetime") or slot == "news" and field == "date":
                observed = clock(observed)
            check(observed == expected, "provider installed document field")
    return len(installed)


def envelope(body, slot, dataset, upstream, query):
    meta = body["extra"]["results_metadata"]["__qopenbb_financial__"]
    check(meta["provider"] == "fmp" and meta["dataset"] == dataset and
          meta["source"]["endpoint"] == upstream, "installed provenance")
    check({key: value for key, value in meta["effective_query"].items() if value is not None and key != "provider"}
          == query, "installed effective tuple")
    check(bool(datetime.fromisoformat(meta["retrieved_at"]).utcoffset() is not None), "installed retrieval time")
    rows = body["results"]
    check(meta["bounds"]["returned_count"] == len(rows), "installed returned count")
    return rows, meta


CONTROLLED_GROUPS = {
    "empty-calendar": ["calendar"], "restore-calendar": ["calendar"],
    "timeout-news": ["news"], "retry-news": ["news"], "no-issuer": ["calendar", "filings", "transcript", "news"],
    **{f"{theme}-{stage}": ["calendar", "filings", "transcript", "news"]
       for theme in ("light", "dark") for stage in ("away", "back")},
}
CONTROLLED_SCENARIOS = {
    "empty-transcript", "partial-conclusion", "denied-input", "mismatched-transcript",
    "clipped-calendar", "duplicate-report-dates", "zero-and-missing-marks",
    "literal-and-safe-document-details", "save-fresh-authenticated-reopen-safe-export",
    "empty-market-calendar", "disappearing-calendar-invoker", "invalid-bounds-no-request",
    "typed-timeout-same-query-retry", "stable-neighbors",
    "light-keyboard-focus-and-supersession", "dark-keyboard-focus-and-supersession",
    "empty-issuer-filter", "pending-and-insufficient-conclusions",
}


def report(directory):
    plan_path = directory / "plan.json"
    if not plan_path.exists():
        plan_path = Path(__file__).with_name("events-documents-plan.json")
    plan = decode(plan_path.read_bytes())
    run = decode((directory / "observations.json").read_bytes())
    ledger = decode((directory / "provider" / "ledger.json").read_bytes())
    requests = run["requests"]
    live = run["mode"] == "live"
    upstream_schedule = schedule(plan)
    expected = Counter((stage, slot) for stage, slots in plan["groups"].items() for slot in slots)
    if not live:
        expected.update((stage, slot) for stage, slots in CONTROLLED_GROUPS.items() for slot in slots)
        check(set(run["scenarios"]) == CONTROLLED_SCENARIOS, "controlled scenario coverage")
        check(not run["network"]["fixtureExternal"] and not run["network"]["errors"], "controlled browser network")
        cancelled = {f"{stage}/{slot}": 1 for stage, slots in CONTROLLED_GROUPS.items()
                     if stage.endswith("-away") for slot in slots}
        check(run["network"]["abortedData"] == sum(cancelled.values()) and run["network"]["abortedSlots"] == cancelled,
              "controlled supersession cancellations")
        check(run["network"]["httpErrors"] == {"listing/news/403": 1, "timeout-news/news/400": 1},
              "controlled HTTP failures")
        console = run["network"]["consoleErrors"]
        check(set(console) <= {"expected-fixture-http-403", "expected-fixture-http-400", "blocked-cross-origin-resource"},
              "controlled browser console")
    check(not run["issues"] and run["browserRequests"] == len(requests), "browser diagnostic counts")
    check(Counter((entry["stage"], entry["slot"]) for entry in requests) == expected, "browser request schedule")
    check(ledger["denials"] == 0, "guard denial")
    check(ledger["count"] == (sum(map(len, plan["groups"].values())) if live else 0), "guard send count")
    sends = {entry["number"]: entry for entry in ledger["entries"]}
    check(len(sends) == ledger["count"], "guard send identity")
    check(not live or {entry["receipt"] for entry in requests} == sends.keys(), "same-send coverage")
    installed = {}
    blocked = Counter()
    empty = Counter()
    documents = Counter()
    if not live:
        retry = [entry["query"] for entry in requests if entry["stage"] in ("timeout-news", "retry-news")]
        check(len(retry) == 2 and retry[0] == retry[1], "controlled same-query retry")
    for entry in requests:
        number = entry["index"]
        slot, stage, status = (entry[k] for k in ("slot", "stage", "status"))
        wire_bytes = (directory / f"{number}.installed").read_bytes()
        body = decode(wire_bytes) if status != 204 else {}
        raw = None
        if live:
            send = sends[entry["receipt"]]
            check((send["stage"], send["slot"]) == (stage, slot), "same-send tuple")
            check((send["endpoint"], send["effective_query"]) == upstream_schedule[stage][slot], "upstream effective tuple")
            if send["sha256"]:
                contents = (directory / "provider" / f"{send['number']}.provider").read_bytes()
                check(hashlib.sha256(contents).hexdigest() == send["sha256"], "provider capture hash")
                if send["status"] == 200:
                    raw = decode_provider(contents)
        if not live and stage.endswith("-away"):
            check(entry["done"] and entry.get("documentCount") is None, "superseded display exclusion")
            if stage == "dark-away" and slot == "news":
                check(status == 400 and body.get("code") == "timeout", "superseded failure fixture")
            else:
                check(status == 200, "superseded success fixture")
                envelope(body, slot, *plan["slots"][slot], entry["query"])
            continue
        if status != 200:
            code = body.get("code")
            if status == 204:
                check(not live or raw == [], "upstream empty response")
                empty[slot] += 1
            else:
                blocked[code if code in SAFE_CODES else "permission_denied" if not live and status == 403 else "unavailable"] += 1
            continue
        rows, meta = envelope(body, slot, *plan["slots"][slot], entry["query"])
        if raw is None:
            check(not live, "successful request missing raw provider response")
        if raw is not None:
            source_rows = matching_calendar(raw, entry["query"]["symbol"]) if slot == "calendar" else raw
            clipped = len(source_rows) > (250 if slot == "calendar" else entry["query"].get("limit", 1))
            check(bool(meta["bounds"].get("truncated")) == clipped, "source clipping")
        token_rows = json.loads(wire_bytes, parse_int=str, parse_float=str)["results"] if slot == "calendar" else []
        installed[number] = (rows, raw, meta, token_rows)
        if not live and stage == "listing" and slot == "transcript":
            check(entry["documentCount"] == 0 and rows[0]["quarter"] != f"Q{entry['query']['quarter']}",
                  "mismatched transcript exclusion")
            blocked["invalid_evidence"] += 1
            continue
        if not live and slot == "calendar" and stage == "calendar":
            check(meta["bounds"]["truncated"] is True and len(rows) == 250, "controlled clipped listing")
        if slot != "calendar":
            check(entry["documentCount"] == len(rows), "display document count")
            documents[slot] += compare_documents(slot, raw, rows, entry["query"]) if live else len(rows)
    coverage = Counter()
    final_coverage = {}
    calendar_views = []
    chart_marks = Counter()
    microsoft_views = []
    final_stage = "reopen" if "reopen" in plan["groups"] else "launch"
    final_inputs = {entry["slot"]: entry["status"] == 200 and (entry.get("documentCount") or 0) > 0
                    for entry in requests if entry["stage"] == final_stage and entry["slot"] != "calendar"}
    for display in run["calendar"]:
        receipt = display["index"]
        if receipt not in installed:
            check(display["rows"] == [], "calendar rows after error")
            continue
        rows, raw, meta, token_rows = installed[receipt]
        check(display["listingCount"] == len(rows) and display["clipped"] == bool(meta["bounds"].get("truncated")),
              "display listing scope")
        check(display["retrievedAt"] == meta["retrieved_at"], "display retrieval time")
        if raw is None:
            raw = [{"symbol": row["symbol"], "date": row["report_date"], "lastUpdated": row.get("last_updated"),
                    **{origin: row.get(field) for field, origin in FIELDS.items()}} for row in rows]
        counts = compare_calendar(raw, rows, display["rows"], display["symbol"])
        compare_marks(rows, token_rows, display["rows"], meta["fields"])
        chart_marks.update(mark["identity"].rsplit(" · ", 1)[-1]
                           for row in display["rows"] for chart in row["charts"] for mark in chart["marks"])
        coverage.update(counts)
        stage = next(entry["stage"] for entry in requests if entry["index"] == receipt)
        calendar_views.append({"stage": stage, "symbol": display["symbol"], "rows": len(display["rows"]),
                               "numeric_fields": counts, "missing_labels": {
                                   field: sum(row["fields"][field] == "Missing" for row in display["rows"])
                                   for field in FIELDS}})
        if live and "symbols" not in plan and stage in ("calendar", "reopen"):
            check(display["symbol"] == "MSFT" and all(counts.values()), "Microsoft calendar figure coverage")
            microsoft_views.append({"stage": stage, "source_rows": len(raw), "listing_rows": len(rows),
                                    "source_ordinals": [i for i, row in enumerate(raw) if row["symbol"].upper() == "MSFT"]})
        if stage == final_stage:
            final_coverage = counts
    final_inputs["calendar"] = any(final_coverage.values())
    supplemental = {}
    if live and "symbols" not in plan:
        check({view["stage"] for view in microsoft_views} == {"calendar", "reopen"}, "Microsoft edit and reopen proof")
        supplemental["microsoft_calendar"] = microsoft_views
    if live and final_stage == "launch":
        check(run["seedAborts"] > 0 and run["scenarios"] == ["native-catalog-seeded-through-workspace-controls"],
              "four-input proof seed")
        check(set(final_coverage) == FIELDS.keys() and all(final_coverage.values()), "four-input chart coverage")
        supplemental = {"calendar_views": calendar_views, "seed_aborts": run["seedAborts"],
                        "conclusions": run["conclusions"]}
    if live and "symbols" in plan and final_stage == "reopen":
        check(run["seedAborts"] > 0 and set(run["scenarios"]) == {
            "native-catalog-seeded-through-workspace-controls", "save-and-export-choices",
            "fresh-authenticated-reopen-choices"}, "supplemental preparation and persistence")
        check(any(view["symbol"] == plan["symbols"]["launch"] and all(
            view["missing_labels"][field] for field in ("eps_consensus", "revenue_consensus"))
            for view in calendar_views), "supplemental live missing estimates")
        check(set(final_coverage) == FIELDS.keys() and all(final_coverage.values()),
              "supplemental reopened live chart fields")
        supplemental = {"calendar_views": calendar_views, "seed_aborts": run["seedAborts"],
                        "conclusions": run["conclusions"]}
    controlled = {}
    if not live:
        check(blocked == {"invalid_evidence": 1, "permission_denied": 1, "timeout": 1}, "controlled failure counts")
        check(empty == {"calendar": 1, "filings": 1, "transcript": 2, "news": 1}, "controlled empty counts")
        controlled = {"controlled_scenarios": run["scenarios"], "controlled_network": run["network"]}
    return {**controlled, **supplemental, "mode": run["mode"], "browser": run["browser"], "browser_requests": len(requests),
            "provider_sends": ledger["count"], "provider_statuses": dict(Counter(
                str(entry["status"] or "transport_unobserved") for entry in sends.values())),
            "provider_schedule": [{"stage": entry["stage"], "slot": entry["slot"]} for entry in sends.values()],
            "coverage": dict(coverage), "chart_marks": dict(chart_marks),
            "final_calendar_coverage": final_coverage, "final_inputs": final_inputs,
            "document_rows": dict(documents), "empty": dict(empty), "blocked": dict(blocked)}



def replay_source(directory):
    plan = decode(Path(__file__).with_name("events-documents-plan.json").read_bytes())
    run = decode((directory / "observations.json").read_bytes())
    ledger = decode((directory / "provider" / "ledger.json").read_bytes())
    check(run["mode"] == "live" and ledger["count"] == 15 and not ledger["denials"], "replay source verification")
    request, = [entry for entry in run["requests"] if (entry["stage"], entry["slot"]) == ("launch", "calendar")]
    send, = [entry for entry in ledger["entries"] if entry["number"] == request["receipt"]]
    check((send["stage"], send["slot"]) == ("launch", "calendar"), "replay source identity")
    check((send["endpoint"], send["effective_query"]) == schedule(plan)["launch"]["calendar"], "replay source tuple")
    check(send["status"] == request["status"] == 200, "replay source HTTP status")
    provider = (directory / "provider" / f"{send['number']}.provider").read_bytes()
    check(hashlib.sha256(provider).hexdigest() == send["sha256"], "replay source hash")
    return directory / f"{request['index']}.installed", provider, send["number"]


def report_replay(root, source):
    path, provider, receipt = replay_source(source)
    captured = path.read_bytes()
    check((root / "replay-calendar.installed").read_bytes() == captured, "replay staged capture")
    run = decode((root / "observations.json").read_bytes())
    ledger = decode((root / "provider" / "ledger.json").read_bytes())
    check(run["mode"] == "controlled" and run["replay"] and not run["issues"] and not run["network"]["errors"],
          "replay browser diagnostics")
    check(not ledger["count"] and not ledger["denials"], "replay provider ledger")
    calendars = {entry["index"]: entry for entry in run["requests"] if entry["slot"] == "calendar"}
    check([entry["query"]["symbol"] for entry in calendars.values()] == ["AAPL", "0151.HK", "GMGMF"],
          "replay listing acquisitions")
    source_rows = decode(captured)["results"]
    raw = decode_provider(provider)
    observed = []
    for display in run["calendar"]:
        entry = calendars[display["index"]]
        symbol = entry["query"]["symbol"]
        mounted = (root / f"{entry['index']}.installed").read_bytes()
        rows, meta = envelope(decode(mounted), "calendar", "equity/calendar/earnings", "earnings-calendar", entry["query"])
        check(rows == matching_calendar(source_rows, symbol), "scoped replay captured values")
        check(symbol == display["symbol"] and display["listingCount"] == len(rows) and not display["clipped"],
              "replay listing scope")
        check(display["retrievedAt"] == meta["retrieved_at"], "replay retrieval time")
        tokens = json.loads(mounted, parse_int=str, parse_float=str)["results"]
        counts = compare_calendar(raw, rows, display["rows"], symbol)
        compare_marks(rows, tokens, display["rows"], meta["fields"])
        observed.extend(replay_row(symbol, row, counts) for row in display["rows"])
    expected = Counter((symbol, mode) for symbol in ("0151.HK", "GMGMF") for mode in ("bar", "point"))
    check(Counter((row["symbol"], row["charts"].get("eps")) for row in observed) == expected
          and all(row["charts"].get("revenue") == row["charts"].get("eps") for row in observed),
          "replay listings and chart displays")
    return {"replay_receipt": receipt, "replay_browser": run["browser"], "replay_rows": observed,
            "replay_retrieved_at": decode(captured)["extra"]["results_metadata"]["__qopenbb_financial__"]["retrieved_at"], "replay_provider_count": len(raw),
            "replay_normalized_count": len(source_rows), "capture_sha256": hashlib.sha256(provider).hexdigest()}


def replay_row(symbol, row, counts):
    return {"symbol": symbol, "ordinal": row["ordinal"], "report_date": row["date"], "updated": row["updated"],
            "charts": {chart["measure"]: chart["display"] for chart in row["charts"]}, "fields": counts,
            "exact_values": row["fields"], "units": row["fieldUnits"],
            "missing": [field for field, value in row["fields"].items() if value == "Missing"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("private_directory", type=Path)
    args = parser.parse_args()
    try:
        print(json.dumps(report(args.private_directory), sort_keys=True))
    except Discrepancy as error:
        print(json.dumps({"outcome": "discrepancy", "check": str(error)}))
        return 1
    except (OSError, ValueError, TypeError, KeyError, InvalidOperation):
        print(json.dumps({"outcome": "invalid private evidence"}))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
