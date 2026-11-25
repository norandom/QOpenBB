"""Exercise consumer compatibility on signed requests and disposable saved runs."""

import asyncio
import json
import os
from copy import deepcopy
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from urllib.parse import urlencode

import pytest
from qopenbb_ci.financial_compat_cases import compare_cases
from qopenbb_ci.financial_compat_replay import _consumer_path
from qopenbb_ci.modeling_bundle import _verify_source
from qopenbb_ci.modeling_bundle import main as bundle_main
from qopenbb_data.modeling.service import bootstrap
from qopenbb_data.modeling.service.execution import ExecutionLimits
from qopenbb_data.modeling.service.orchestrator import MethodBinding
from qopenbb_data.modeling.validation.rules import Rule
from qopenbb_data.modeling.verification.reference import Reference
from test_model_identity import CURRENT, assertion
from test_orchestration import (
    TestMethod,
    calculated,
    dimensions,
    expected,
    failed_precondition,
    partial_method,
)
from test_orchestration import request as evaluation_request

ROOT = Path(__file__).resolve().parents[2]
BASELINE = ROOT / "contracts/modeling/v1"
CONSUMER = ROOT / "contracts/consumers/financial-modeling/saved-output.v1.json"
EXPECTATIONS = CONSUMER.with_name("saved-output.cases.v1.json")


def exchange(app, path, *, payload=None, query=None, owner="case-owner"):
    async def call():
        events = []
        sent = False
        token = assertion(claims={"sub": owner})

        async def receive():
            nonlocal sent
            if sent:
                await asyncio.Future()
            sent = True
            body = b"" if payload is None else json.dumps(payload).encode()
            return {"type": "http.request", "body": body}

        async def send(event):
            events.append(event)

        await app(
            {
                "type": "http",
                "asgi": {"version": "3.0", "spec_version": "2.4"},
                "method": "GET" if payload is None else "POST",
                "path": "/modeling/v1" + path,
                "root_path": "",
                "query_string": urlencode(query or {}).encode(),
                "headers": [(b"authorization", f"Bearer {token}".encode())],
                "scheme": "http",
                "server": ("localhost", 80),
                "client": ("localhost", 1),
                "http_version": "1.1",
            },
            receive,
            send,
        )
        return {"status": events[0]["status"], "body": json.loads(events[-1]["body"])}

    return asyncio.run(asyncio.wait_for(call(), 15))


def payload_for(value):
    day = "2024-01-02"
    context = {
        "unit": "amount",
        "currency": "USD",
        "scale": 3,
        "quantity": "flow",
        "basis": "nominal",
        "period_start": "2024-01-01",
        "period_end": day,
        "frequency": "daily",
    }
    rows = [
        {
            "record_id": key,
            "entity_id": key,
            "metric_id": "test-value",
            "observation_date": day,
            "context": context,
            "value": amount,
            "category": "raw",
        }
        for key, amount in (("present", value), ("missing", None))
    ]
    snapshot = {
        "schema_id": "test-observations",
        "provenance": {
            "origin": "user_supplied",
            "source": "test-fixture",
            "query": [],
            "retrieved_at": "2024-01-03T00:00:00Z",
        },
        "tables": [
            {
                "table_id": "observations",
                "grain": "one test value per entity and observation date",
                "keys": ["entity_id", "observation_date"],
                "nullable": True,
                "rows": rows,
            }
        ],
    }
    return evaluation_request(inputs=snapshot).model_dump(mode="json")


def make_app(patch, *, partial=False, verified=True, unit=None):
    method = partial_method() if partial else TestMethod()
    if unit is not None:
        descriptor = method.describe()
        output = descriptor.outputs[0].model_copy(update={"unit": unit})
        method.descriptor = descriptor.model_copy(update={"outputs": (output,)})
    rules = (Rule("quality", (), ("blocked",), failed_precondition),) if partial else ()
    binding = MethodBinding(
        ExecutionLimits(10, 1, 1, measure_dimensions=dimensions),
        rules=rules,
        calculate=calculated,
        reference=Reference("1", {"value": expected}, {}) if verified else None,
    )
    # The adopted registry has no production methods. Register a fixture through
    # the same entry point the installed methods use.
    with patch.context() as registration:
        registration.setattr(bootstrap, "_INSTALLED_METHODS", ((method, binding),))
        return bootstrap.create_app()


def read_widget(app, run_id, *, output_id="value", stale=False, owner="case-owner"):
    query = {"run_id": run_id, "output_id": output_id}
    if stale:
        query["expected_run_id"] = "different-selection"
    return exchange(app, "/widget-results", query=query, owner=owner)


def exercise(app, payload, *, partial=False, stale=False):
    evaluation = exchange(app, "/evaluations", payload=payload)
    result = {"evaluation": evaluation}
    if evaluation["status"] != 200 or not isinstance(
        evaluation["body"].get("run_id"), str
    ):
        return result
    run_id = evaluation["body"]["run_id"]
    result["run"] = exchange(app, "/runs/" + run_id)
    result["widget"] = read_widget(app, run_id, stale=stale)
    if partial:
        result["blocked_widget"] = read_widget(app, run_id, output_id="blocked")
    return result


@pytest.fixture(scope="module")
def baseline():
    return {
        path.name: json.loads(path.read_bytes()) for path in BASELINE.glob("*.json")
    }


@dataclass(frozen=True)
class Candidate:
    directory: Path
    consumer_file: Path
    manifest_bytes: bytes
    consumer_bytes: bytes

    def documents(self):
        return {
            path.name: json.loads(path.read_bytes())
            for path in self.directory.glob("*.json")
        }


def verify_candidate_for_exercise(directory, consumer):
    manifest = (directory / "manifest.json").read_bytes()
    consumer_bytes = consumer.read_bytes()
    revision = json.loads(manifest)["source_revision"]
    assert (
        bundle_main(
            [
                "check",
                "--revision",
                revision,
                "--output",
                str(directory),
                "--consumer",
                str(consumer),
            ]
        )
        == 0
    )
    source_consumer = consumer
    if not consumer.is_relative_to(ROOT):
        env = os.environ | {"GIT_NO_LAZY_FETCH": "1", "GIT_NO_REPLACE_OBJECTS": "1"}
        source_consumer = ROOT / _consumer_path(revision, consumer_bytes, env)
    # Equal exports can come from revisions that differ in runtime behavior.
    _verify_source(revision, source_consumer, consumer_bytes)
    assert (directory / "manifest.json").read_bytes() == manifest
    assert consumer.read_bytes() == consumer_bytes
    return Candidate(directory, consumer, manifest, consumer_bytes)


@pytest.fixture(scope="module")
def selected_candidate():
    directory = Path(os.environ.get("QOPENBB_MODEL_COMPAT_BUNDLE", BASELINE)).resolve()
    consumer = Path(os.environ.get("QOPENBB_MODEL_COMPAT_CONSUMER", CONSUMER)).resolve()
    return verify_candidate_for_exercise(directory, consumer)


@pytest.fixture(scope="module")
def runtime_settings(tmp_path_factory):
    with pytest.MonkeyPatch.context() as patch:
        test_imports = str(Path(__file__).resolve().parent)
        existing_paths = os.environ.get("PYTHONPATH")
        patch.setenv(
            "PYTHONPATH", os.pathsep.join(filter(None, (test_imports, existing_paths)))
        )
        patch.setenv("QFM_IDENTITY_CURRENT_KID", "active")
        patch.setenv("QFM_IDENTITY_CURRENT_SECRET", CURRENT)
        patch.delenv("QFM_IDENTITY_PREVIOUS_KID", raising=False)
        patch.delenv("QFM_IDENTITY_PREVIOUS_SECRET", raising=False)
        run_dir = tmp_path_factory.mktemp("financial-compat") / "runs"
        patch.setenv("QOPENBB_MODEL_RUN_DIR", str(run_dir))
        yield patch


@pytest.fixture(scope="module")
def exercised_cases(selected_candidate, runtime_settings):
    app = make_app(runtime_settings)
    cases = {
        name: exercise(app, payload_for(value))
        for name, value in (("negative", "-10.125"), ("zero", "0"), ("missing", None))
    }
    partial = make_app(runtime_settings, partial=True)
    cases["partial"] = exercise(partial, payload_for("2.5"), partial=True)
    unverified = make_app(runtime_settings, verified=False)
    cases["stale_unverified"] = exercise(unverified, payload_for("0.1"), stale=True)
    cases["invalid_request"] = {"evaluation": exchange(app, "/evaluations", payload={})}
    negative = cases["negative"].get("run", {}).get("body", {})
    if run_id := negative.get("run_id"):
        cases["wrong_owner"] = {
            "run": exchange(app, "/runs/" + run_id, owner="different-owner"),
            "widget": read_widget(app, run_id, owner="different-owner"),
        }
    return {"version": 1, "cases": cases}


@pytest.fixture(scope="module")
def compare(baseline, selected_candidate):
    consumer = json.loads(CONSUMER.read_bytes())
    expectations = json.loads(EXPECTATIONS.read_bytes())

    def check(exercised, *, candidate=None):
        if candidate is None:
            candidate = selected_candidate.documents()
        return compare_cases(baseline, candidate, consumer, expectations, exercised)

    return check


def test_real_signed_responses_match_expectations(compare, exercised_cases):
    assert compare(exercised_cases) == []


def test_real_unit_change_blocks_with_unchanged_schemas(
    compare, exercised_cases, runtime_settings
):
    evidence = deepcopy(exercised_cases)
    changed_app = make_app(runtime_settings, unit="percentage")
    evidence["cases"]["negative"] = exercise(changed_app, payload_for("-10.125"))
    assert (
        evidence["cases"]["negative"]["widget"]["body"]["results"][0]["unit"]
        == "percentage"
    )
    assert compare(evidence) == [
        "negative evaluation: response differs from semantic expectations",
        "negative run: response differs from semantic expectations",
        "negative widget: response differs from semantic expectations",
    ]


@pytest.mark.parametrize(
    ("case", "operation", "field"),
    [
        ("missing", "widget", None),
        ("wrong_owner", "run", "correlation_id"),
        ("invalid_request", "evaluation", "fields"),
        ("partial", "blocked_widget", "verification"),
        ("stale_unverified", "widget", "run_detail_href"),
    ],
)
def test_incomplete_or_malformed_evidence_blocks(
    compare, exercised_cases, case, operation, field
):
    evidence = deepcopy(exercised_cases)
    item = evidence["cases"][case]
    if field is None:
        del item[operation]
    else:
        del item[operation]["body"][field]
    assert compare(evidence)


def test_candidate_response_refs_are_offline_and_all_cases_are_checked(
    compare,
    selected_candidate,
    exercised_cases,
    monkeypatch,
):
    def remote_fetch(*args):
        pytest.fail("response schema attempted network retrieval")

    monkeypatch.setattr("urllib.request.urlopen", remote_fetch)
    candidate = selected_candidate.documents()
    schema = candidate["safe-error.schema.json"]
    schema["properties"]["correlation_id"]["$ref"] = "https://example.invalid/schema"
    evidence = deepcopy(exercised_cases)
    del evidence["cases"]["negative"]["widget"]
    findings = compare(evidence, candidate=candidate)
    assert "negative widget: missing response or unexpected HTTP status" in findings
    assert "wrong_owner widget: candidate response schema rejected evidence" in findings


def test_financial_compat_cli_writes_exercised_evidence(
    selected_candidate,
    exercised_cases,
    tmp_path,
    capsys,
):
    from qopenbb_ci.financial_compat import evidence_record, main

    assert (
        verify_candidate_for_exercise(
            selected_candidate.directory, selected_candidate.consumer_file
        )
        == selected_candidate
    )
    record = evidence_record(
        selected_candidate.directory,
        selected_candidate.consumer_file,
        EXPECTATIONS,
        exercised_cases,
    )
    assert (
        record["candidate_manifest_sha256"]
        == sha256(selected_candidate.manifest_bytes).hexdigest()
    )
    assert (
        record["consumer_sha256"]
        == sha256(selected_candidate.consumer_bytes).hexdigest()
    )
    external = os.environ.get("QOPENBB_MODEL_COMPAT_EVIDENCE")
    destination = Path(external) if external else tmp_path / "modeling-evidence.json"
    destination.write_text(json.dumps(record, allow_nan=False) + "\n", encoding="utf-8")
    status = main(
        [
            "--candidate-bundle",
            str(selected_candidate.directory),
            "--candidate-consumer",
            str(selected_candidate.consumer_file),
            "--evidence",
            str(destination),
        ]
    )
    output = json.loads(capsys.readouterr().out)
    assert status == 0 and output["decision"] == "compatible", output


@pytest.mark.parametrize(
    ("field", "changed"),
    [("currency", "EUR"), ("scale", 6), ("period_start", "2023-12-31")],
)
def test_later_observation_context_must_match(compare, exercised_cases, field, changed):
    evidence = deepcopy(exercised_cases)
    for operation in ("evaluation", "run"):
        rows = evidence["cases"]["negative"][operation]["body"]["inputs"]["tables"][0][
            "rows"
        ]
        rows[1]["context"][field] = changed
    assert (
        "negative: saved run has inconsistent financial context or verification"
        in compare(evidence)
    )
