"""Check saved research story calculations without importing the modeling runtime."""

from datetime import UTC, date, datetime, timedelta
from decimal import Decimal
from hashlib import sha256
from itertools import pairwise
from json import dumps
from statistics import stdev

START = "2026-08-17"
END = "2026-11-13"
REVISION = "nyse-arca.2026r1"
CALENDAR = "NYSE_ARCA"
DECISION = "2026-11-14T04:59:59Z"
PRICE_BASIS = "split_adjusted_dividends_excluded"
OUTPUTS = {
    "left_momentum": "percent", "right_momentum": "percent", "momentum_spread": "percentage_points",
    "left_volatility": "percent", "right_volatility": "percent", "volatility_spread": "percentage_points",
}


class PreflightFailure(ValueError):
    """A verification requirement failed."""


def require(condition, message):
    if not condition:
        raise PreflightFailure(message)


def digest(value, *, sorted_keys=True, ascii_only=True):
    return sha256(dumps(value, sort_keys=sorted_keys, ensure_ascii=ascii_only,
                        separators=(",", ":")).encode()).hexdigest()


def unique_by(items, field):
    indexed = {item[field]: item for item in items}
    require(len(indexed) == len(items), f"Duplicate {field}")
    return indexed


def timestamp(value):
    require(isinstance(value, str), "Missing UTC timestamp")
    result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    require(result.utcoffset() == timedelta(0), "Expected UTC timestamp")
    return result


def number(value):
    require(isinstance(value, str), "Expected financial decimal on the wire")
    result = Decimal(value)
    require(result.is_finite(), "Expected finite financial decimal")
    return result


def close_to(actual, expected, label):
    require(abs(number(actual) - expected) <= Decimal("1e-24"), f"Numerical mismatch for {label}")


def schedule_days():
    first = date.fromisoformat(START)
    days = (first + timedelta(days=i) for i in range((date.fromisoformat(END) - first).days + 1))
    return [day.isoformat() for day in days if day.weekday() < 5 and day.isoformat() != "2026-09-07"]


def check_binding(run, request, source):
    descriptor, snapshot = run["descriptor"], run["inputs"]
    acquisition = request["acquisition"]
    require(all(descriptor[key] == request[key] for key in ("model_id", "method_version")),
            "Run model binding differs from selection")
    saved, supplied = run["assumptions"], request["assumptions"]
    require(all(saved[key] == supplied[key] for key in ("effective_date", "version"))
            and len(saved["assumptions"]) == len(supplied["assumptions"])
            and all(all(actual[key] == value for key, value in expected.items())
                    for actual, expected in zip(saved["assumptions"], supplied["assumptions"])),
            "Run assumptions differ from selection")
    actual, expected = snapshot["cutoff"], acquisition["cutoff"]
    require(all(actual[key] == expected[key] for key in ("observation_date", "session_timezone"))
            and all(timestamp(actual[key]) == timestamp(expected[key]) for key in ("decision_at", "evaluated_at")),
            "Run cutoff differs from selection")
    require(snapshot["schema_id"] == f"{request['model_id']}.inputs" and snapshot["schema_version"] == "1",
            "Unexpected snapshot schema")
    provenance = snapshot["provenance"]
    require(provenance["source"] == source and provenance["origin"] == "service_acquired"
            and provenance["acquisition_id"], "Missing service source provenance")
    query = dict(provenance["query"])
    require(len(query) == len(provenance["query"]) and query["dataset_id"] == acquisition["dataset_id"]
            and all(query.get(key) == value for key, value in acquisition["parameters"]),
            "Saved provenance differs from acquisition parameters")
    tables = unique_by(snapshot["tables"], "table_id")
    sessions = tables["sessions"]["rows"]
    require([row["observation_date"] for row in sessions] == schedule_days(), "Exchange dates differ")
    for row in sessions:
        expected = f"{REVISION}.{row['observation_date']}"
        require(row["record_id"] == expected and row["source_record_id"] == f"NYSE.{expected}"
                and row["entity_id"] == CALENDAR and row["metric_id"] == "session"
                and row["context"]["basis"] == "regular_session" and number(row["value"]) == 1
                and timestamp(row["published_at"]) <= timestamp(DECISION), "Invalid schedule marker")
    return tables, provenance, query


def evidence_for_outputs(run, units, *, verified=True):
    outputs = unique_by(run["outputs"], "output_id")
    references = unique_by(run["verification"], "output_id")
    checks = unique_by(run["checks"], "rule_id")
    traces = unique_by(run["trace"], "trace_id")
    require(set(outputs) == set(units) == set(references), "Unexpected output or reference coverage")
    require(not run["exceptions"], "Unexpected verification exception")
    evidence = {}
    fingerprints = {
        name: digest(run[field], sorted_keys=False, ascii_only=False)
        for name, field in (("input", "inputs"), ("assumption", "assumptions"), ("descriptor", "descriptor"))
    }
    for key, output in outputs.items():
        ref = references[key]
        items = [checks[rule] for rule in output["check_ids"]]
        entries = [traces[trace] for trace in output["trace_ids"]]
        require(all(ref[f"{name}_fingerprint"] == value for name, value in fingerprints.items())
                and ref["reference_version"] == run["descriptor"]["reference_version"]
                and ref["output_fingerprint"] == digest({"output": output, "checks": items, "trace": entries}),
                f"Reference fingerprints differ for {key}")
        require(output["unit"] == units[key] and items, f"Missing units or checks for {key}")
        require(all(key in item["output_ids"] for item in items), f"Check binding differs for {key}")
        if verified:
            require(output["status"] == "verified" and ref["status"] == "match"
                    and all(item["status"] == "pass" for item in items)
                    and len(entries) == 1 and entries[0]["output_id"] == key,
                    f"Missing verified trace, check or independent match for {key}")
        evidence[key] = {
            "value": output["value"], "unit": output["unit"], "status": output["status"],
            "reference": ref["status"], "reference_version": ref["reference_version"],
            "output_sha256": ref["output_fingerprint"],
            "checks": [{"id": item["rule_id"], "status": item["status"]} for item in items],
        }
    return outputs, traces, checks, evidence


def records(trace, rows):
    require(trace["source_record_ids"] == [row["record_id"] for row in rows], "Trace source records differ")


def substitutions(trace, rows):
    require(len(trace["substitutions"]) == len(rows), "Trace substitutions differ")
    for item, row in zip(trace["substitutions"], rows):
        require(item["name"] == row["record_id"] and item["period_end"] == row["observation_date"]
                and item["unit"] == row["context"]["unit"] and item["currency"] == row["context"]["currency"]
                and item["scale"] == row["context"]["scale"]
                and number(item["value"]) == number(row["value"]), "Trace endpoint differs from saved row")


def risk_trace(trace, returns, days):
    values = unique_by(trace["intermediate_values"], "name")
    require(len(values) == 66, "Expected 63 dated returns and three risk parameters")
    for (start, end), value in zip(pairwise(days), returns):
        item = values[f"simple_return.{end}"]
        require((item["period_start"], item["period_end"], item["unit"]) == (start, end, "ratio"),
                "Return trace dates or unit differ")
        close_to(item["value"], value, "adjacent simple return")
    for key, value in (("return_count", 63), ("sample_divisor", 62), ("annualization_sessions", 252)):
        require(values[key]["unit"] == "count" and number(values[key]["value"]) == value,
                "Risk trace parameters differ")


def verify_leg(side, symbol, tables, query, traces, outputs):
    rows = sorted(tables[f"{side}_closes"]["rows"], key=lambda row: row["observation_date"])
    days = schedule_days()
    require([row["observation_date"] for row in rows] == days, f"{symbol} close coverage differs")
    require(f"{side}_error" not in query and f"{side}_retrieved_at" in query, f"{symbol} receipt missing")
    receipt = timestamp(query[f"{side}_retrieved_at"])
    require(receipt >= timestamp(f"{END}T21:00:00Z"), f"{symbol} receipt precedes final close")
    closes = []
    for row, day in zip(rows, days):
        identifier = f"fmp:{symbol}:{day}:close"
        context = row["context"]
        require((row["record_id"], row["source_record_id"]) == (identifier, identifier)
                and (row["entity_id"], row["metric_id"], row["category"]) == (symbol, "close", "provider")
                and (context["unit"], context["currency"], context["basis"], context["scale"])
                == ("price", "USD", PRICE_BASIS, 0)
                and row["published_at"] is None and row["vintage_at"] is None, f"Invalid {symbol} FMP close")
        value = number(row["value"])
        require(value > 0, f"Nonpositive {symbol} close")
        closes.append(value)
    returns = [end / start - 1 for start, end in pairwise(closes)]
    momentum = (closes[-1] / closes[0] - 1) * 100
    volatility = stdev(returns) * Decimal(252).sqrt() * 100
    for metric, value in (("momentum", momentum), ("volatility", volatility)):
        output_id = f"{side}_{metric}"
        trace = traces[outputs[output_id]["trace_ids"][0]]
        records(trace, tables["sessions"]["rows"] + rows)
        substitutions(trace, [rows[0], rows[-1]])
        close_to(outputs[output_id]["value"], value, output_id)
    risk_trace(trace, returns, days)
    return {
        "symbol": symbol, "row_count": len(rows), "return_count": len(returns),
        "retrieved_at": receipt.isoformat(), "row_sha256": digest(rows),
        "return_trace_sha256": digest(trace["intermediate_values"]),
    }, (momentum, volatility), rows


def verify_comparison(run, request):
    tables, provenance, query = check_binding(run, request, "fmp")
    require(set(tables) == {"sessions", "left_closes", "right_closes"}, "Unexpected comparison tables")
    for side in ("left", "right"):
        failure = query.get(f"{side}_error")
        if failure:
            code = failure if failure in {"entitlement", "missing_data", "timeout", "throttling",
                                           "invalid_response", "upstream"} else "unknown"
            raise PreflightFailure(f"{side} FMP input blocked ({code})")
    outputs, traces, _, evidence = evidence_for_outputs(run, OUTPUTS)
    left, left_values, left_rows = verify_leg("left", query["left_proxy"], tables, query, traces, outputs)
    right, right_values, right_rows = verify_leg("right", query["right_proxy"], tables, query, traces, outputs)
    receipt = timestamp(provenance["retrieved_at"])
    require(receipt == max(timestamp(leg["retrieved_at"]) for leg in (left, right))
            and receipt <= datetime.now(UTC), "Run receipt differs from leg receipts")
    for name, lhs, rhs in zip(("momentum_spread", "volatility_spread"), left_values, right_values):
        close_to(outputs[name]["value"], lhs - rhs, name)
        trace = traces[outputs[name]["trace_ids"][0]]
        records(trace, tables["sessions"]["rows"] + left_rows + right_rows)
        substitutions(trace, [left_rows[0], left_rows[-1], right_rows[0], right_rows[-1]])
    spread = number(outputs["momentum_spread"]["value"])
    verdict = "supported" if spread > 0 else "not supported"
    spread_outcome = "commodity_outperformance" if spread > 0 else "technology_outperformance" if spread < 0 else "tie"
    return {
        "run_id": run["run_id"], "source": "fmp", "availability_basis": "retrieved_history",
        "price_basis": PRICE_BASIS, "retrieved_at": receipt.isoformat(), "legs": [left, right],
        "outputs": evidence, "verdict": verdict, "spread_outcome": spread_outcome,
        "session_sha256": digest(tables["sessions"]["rows"]),
    }


def eligible_endpoint(rows, day, cutoff):
    candidates = []
    for row in rows:
        if (row["observation_date"] != day or row["value"] is None
                or row["category"] != "provider" or row["context"]["vintage_coverage"] != "known"
                or row["published_at"] is None):
            continue
        publication = timestamp(row["published_at"])
        vintage = timestamp(row["vintage_at"]) if row["vintage_at"] else publication
        if max(publication, vintage) <= cutoff:
            candidates.append(((publication, vintage), row))
    if not candidates:
        return None
    latest = max(times for times, _ in candidates)
    selected = [row for times, row in candidates if times == latest]
    require(len({number(row["value"]) for row in selected}) == 1, f"Conflicting DFII10 levels on {day}")
    return min(selected, key=lambda row: row["record_id"])


def verify_context(run, request):
    tables, provenance, query = check_binding(run, request, "fred")
    require(set(tables) == {"sessions", "dfii10"}, "Unexpected macro tables")
    require(query.get("symbol") == "DFII10" and query.get("start_date") == START
            and query.get("end_date") == END and query.get("provider") == "fred",
            "DFII10 acquisition bounds differ")
    rows = tables["dfii10"]["rows"]
    unique_by(rows, "record_id")
    for row in rows:
        require(row["entity_id"] == "DFII10" and row["metric_id"] == "real_yield"
                and START <= row["observation_date"] <= END and row["context"]["unit"] == "percent"
                and row["context"]["basis"] == "treasury_constant_maturity",
                "Invalid DFII10 row identity or context")
    first, last = (eligible_endpoint(rows, day, timestamp(DECISION)) for day in (START, END))
    eligible = first is not None and last is not None
    outputs, traces, checks, evidence = evidence_for_outputs(
        run, {"regime": "classification", "change": "percentage_points"}, verified=eligible,
    )
    receipt = timestamp(provenance["retrieved_at"])
    require(receipt <= datetime.now(UTC), "DFII10 receipt follows verification time")
    context = {
        "run_id": run["run_id"], "source": "fred", "retrieved_at": receipt.isoformat(),
        "session_sha256": digest(tables["sessions"]["rows"]), "rows_sha256": digest(rows),
        "row_count": len(rows), "outputs": evidence,
    }
    if eligible:
        delta = number(last["value"]) - number(first["value"])
        close_to(outputs["change"]["value"], delta, "DFII10 change")
        regime = "rising" if delta > 0 else "falling" if delta < 0 else "flat"
        require(outputs["regime"]["value"] == regime, "DFII10 regime classification differs")
        for output in outputs.values():
            trace = traces[output["trace_ids"][0]]
            records(trace, tables["sessions"]["rows"] + [first, last])
            substitutions(trace, [first, last])
        return context | {"context_status": "verified", "endpoints": [
            {key: row[key] for key in ("observation_date", "value", "published_at", "vintage_at")}
            for row in (first, last)
        ]}

    require(last is None, "The November 13 withholding must identify an unavailable ending endpoint")
    for output in outputs.values():
        require(output["value"] is None and output["status"] == "withheld"
                and not output["trace_ids"] and evidence[output["output_id"]]["reference"] == "unavailable"
                and any(checks[key]["severity"] == "blocking" and checks[key]["status"] == "fail"
                        and "DFII10 endpoint" in (checks[key]["explanation"] or "")
                        and END in (checks[key]["explanation"] or "") for key in output["check_ids"]),
                "Macro output lacks a dated blocking DFII10 endpoint check")
    return context | {"context_status": "withheld", "unavailable_endpoint": END}
