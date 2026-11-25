"""Check exercised modeling responses against the saved-output case contract."""

from hashlib import sha256
from json import dumps
from re import fullmatch
from urllib.parse import quote

from .financial_compat_cases_schema import response_checker

_SAVED = {"evaluation": 200, "run": 200, "widget": 200}
_CASES = {
    "negative": _SAVED,
    "zero": _SAVED,
    "missing": _SAVED,
    "partial": _SAVED | {"blocked_widget": 200},
    "stale_unverified": _SAVED,
    "invalid_request": {"evaluation": 422},
    "wrong_owner": {"run": 404, "widget": 404},
}


def _cases(document: dict) -> dict:
    if (
        not isinstance(document, dict)
        or type(document.get("version")) is not int
        or document["version"] != 1
        or not isinstance(document.get("cases"), dict)
    ):
        return {}
    return document["cases"]


def _matches(expected, actual) -> bool:
    if isinstance(expected, dict):
        return isinstance(actual, dict) and all(
            key in actual and _matches(value, actual[key])
            for key, value in expected.items()
        )
    if isinstance(expected, list):
        return (
            isinstance(actual, list)
            and len(expected) == len(actual)
            and all(
                _matches(left, right)
                for left, right in zip(expected, actual, strict=True)
            )
        )
    if type(expected) in (int, float) and type(actual) in (int, float):
        return actual == expected
    return type(expected) is type(actual) and actual == expected


def _check_response(case, operation, status, observed, expected, bundles, findings):
    label = f"{case} {operation}"
    if (
        not isinstance(observed, dict)
        or set(observed) != {"status", "body"}
        or type(observed["status"]) is not int
        or observed["status"] != status
        or not isinstance(observed["body"], dict)
    ):
        findings.append(f"{label}: missing response or unexpected HTTP status")
        return False
    body = observed["body"]
    valid = True
    for role, check in bundles:
        if not check(operation, status, body):
            findings.append(f"{label}: {role} response schema rejected evidence")
            valid = False
    if not isinstance(expected, dict) or not expected or not _matches(expected, body):
        findings.append(f"{label}: response differs from semantic expectations")
        valid = False
    if status >= 400:
        keys = (
            set(expected) | {"correlation_id"} if isinstance(expected, dict) else set()
        )
        if set(body) != keys:
            findings.append(f"{label}: error envelope has unexpected members")
            valid = False
    return valid


def _consumer_row(consumer: dict, body: dict) -> dict:
    operation = consumer["operation"]
    response = consumer["response"]
    if operation["id"] != "readSavedWidgetOutput" or response["data_key"] != "results":
        raise ValueError("unsupported consumer binding")
    (row,) = body["results"]
    fields = response["row_fields"]
    if not fields:
        raise ValueError("missing consumer fields")
    for field in fields:
        value = row[field["name"]]
        if value is None and field["nullable"] is True:
            continue
        if (
            field["type"] != "string"
            or not isinstance(value, str)
            or ("values" in field and value not in field["values"])
        ):
            raise ValueError("incompatible consumer field")
    return row


def _widget_matches_run(
    consumer: dict, widget: dict, run: dict, output_id: str
) -> bool:
    row = _consumer_row(consumer, widget)
    (output,) = (item for item in run["outputs"] if item["output_id"] == output_id)
    href = f"runs/{quote(run['run_id'], safe='')}"
    if (
        widget["run_id"] != run["run_id"]
        or widget["run_detail_href"] != href
        or row["run_detail_href"] != href
        or not _matches(output, row)
    ):
        return False
    scope = {
        "checks": ("rule_id", output["check_ids"]),
        "trace": ("trace_id", output["trace_ids"]),
        "exceptions": ("exception_id", output["exception_ids"]),
        "verification": ("output_id", [output_id]),
    }
    return all(
        _matches([item for item in run[group] if item[key] in ids], widget[group])
        for group, (key, ids) in scope.items()
    )


_CONTEXT_FIELDS = {
    "unit",
    "scale",
    "currency",
    "basis",
    "quantity",
    "period_start",
    "period_end",
    "frequency",
}


def _output_evidence_matches(run: dict, output: dict, evidence: dict) -> bool:
    scoped = {"output": output}
    for field, group, key in (
        ("trace_ids", "trace", "trace_id"),
        ("check_ids", "checks", "rule_id"),
    ):
        items = {item[key]: item for item in run[group]}
        scoped[group] = [items[item_id] for item_id in output[field]]
    encoded = dumps(scoped, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return evidence["output_fingerprint"] == sha256(encoded.encode("utf-8")).hexdigest()


def _check_run(run: dict, context: object) -> bool:
    if not isinstance(context, dict) or set(context) != _CONTEXT_FIELDS:
        return False
    if any(
        not _matches(context, row["context"])
        for table in run["inputs"]["tables"]
        for row in table["rows"]
    ):
        return False
    definitions = {item["output_id"]: item for item in run["descriptor"]["outputs"]}
    verification = {item["output_id"]: item for item in run["verification"]}
    shared_fingerprints = set()
    for output in run["outputs"]:
        key = output["output_id"]
        definition = definitions[key]
        evidence = verification[key]
        if (
            any(
                output[field] != definition[field]
                for field in ("unit", "value_type", "semantic_definition")
            )
            or evidence["reference_version"] != run["descriptor"]["reference_version"]
            or not _output_evidence_matches(run, output, evidence)
        ):
            return False
        shared_fingerprints.add(
            tuple(
                evidence[field]
                for field in (
                    "input_fingerprint",
                    "assumption_fingerprint",
                    "descriptor_fingerprint",
                )
            )
        )
    return len(shared_fingerprints) == 1 and all(
        fullmatch(r"[0-9a-f]{64}", item) for item in next(iter(shared_fingerprints))
    )


def _check_saved_case(case, responses, consumer, context, findings):
    try:
        consistent = _check_run(responses["run"]["body"], context)
    except (KeyError, TypeError, ValueError, IndexError):
        consistent = False
    if not consistent:
        findings.append(
            f"{case}: saved run has inconsistent financial context or verification"
        )
    run = responses["run"]["body"]
    if run != responses["evaluation"]["body"]:
        findings.append(f"{case}: saved run differs from evaluation")
    for operation, output_id in (("widget", "value"), ("blocked_widget", "blocked")):
        if operation not in responses:
            continue
        try:
            matched = _widget_matches_run(
                consumer, responses[operation]["body"], run, output_id
            )
        except (KeyError, ValueError, TypeError):
            matched = False
        if not matched:
            findings.append(
                f"{case} {operation}: widget differs from saved output or binding"
            )


def compare_cases(
    baseline: dict, candidate: dict, consumer: dict, expectations: dict, evidence: dict
) -> list[str]:
    """Return promotion-blocking findings without echoing response values."""
    expected_cases, observed_cases = _cases(expectations), _cases(evidence)
    findings = []
    if set(expected_cases) != set(_CASES):
        findings.append("Case expectations have an unsupported version or case set")
    if set(observed_cases) != set(_CASES):
        findings.append("Case evidence has an unsupported version or case set")
    bundles = (
        ("baseline", response_checker(baseline)),
        ("candidate", response_checker(candidate)),
    )
    context = (
        expectations.get("observation_context")
        if isinstance(expectations, dict)
        else None
    )
    for case, operations in _CASES.items():
        observed, expected = observed_cases.get(case), expected_cases.get(case)
        if not isinstance(observed, dict) or set(observed) != set(operations):
            findings.append(f"{case}: incomplete or unexpected exercised operations")
        if not isinstance(expected, dict) or set(expected) != set(operations) - (
            {"evaluation"}
            if "run" in operations and operations["run"] == 200
            else set()
        ):
            findings.append(f"{case}: incomplete or unexpected operation expectations")
        observed = observed if isinstance(observed, dict) else {}
        expected = expected if isinstance(expected, dict) else {}
        results = [
            _check_response(
                case,
                operation,
                status,
                observed.get(operation),
                expected.get(
                    "run" if operation == "evaluation" and status == 200 else operation
                ),
                bundles,
                findings,
            )
            for operation, status in operations.items()
        ]
        if all(results) and operations.get("run") == 200:
            _check_saved_case(case, observed, consumer, context, findings)
    return findings
