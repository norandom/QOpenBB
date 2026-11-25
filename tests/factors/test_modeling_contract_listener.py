"""Validate actual HTTP responses against the modeling contract adopted by Workspace."""

import json
from pathlib import Path
from urllib.parse import urlencode

from jsonschema import Draft202012Validator
from test_model_identity import assertion
from test_model_listener import exchange, internal_listener
from test_orchestration import OWNER, request
from test_orchestration import inputs as snapshot_fixture
from test_orchestration import service as evaluation_fixture

snapshot = snapshot_fixture
evaluations = evaluation_fixture
BUNDLE = Path(__file__).resolve().parents[2] / "contracts/modeling/v1"


def test_adopted_documents_accept_saved_output_evidence(evaluations, snapshot, tmp_path):
    def validate(name, body):
        schema = json.loads((BUNDLE / f"{name}.schema.json").read_bytes())
        Draft202012Validator(schema, format_checker=Draft202012Validator.FORMAT_CHECKER).validate(body)

    evaluation = request(inputs=snapshot)
    validate("evaluation-request", evaluation.model_dump(mode="json"))
    run = evaluations().evaluate(evaluation, OWNER)
    with internal_listener(tmp_path / "runs") as origin:
        base = origin + "/modeling/v1"
        token = assertion(claims={"sub": OWNER.subject})
        for route, schema in [
            ("/models", "model-listing"),
            (f"/runs/{run.run_id}", "model-run"),
            ("/widget-results?" + urlencode({"run_id": run.run_id, "output_id": "value"}), "widget-projection"),
        ]:
            status, result = exchange(base + route, token)
            assert status == 200
            validate(schema, result)
        for route in ("models", "widgets.json", "apps.json"):
            status, result = exchange(f"{base}/{route}", token)
            assert status == 200
            name = "descriptors.json" if route == "models" else route
            assert result == json.loads((BUNDLE / name).read_bytes())
        status, body = exchange(f"{base}/runs/{run.run_id}", assertion(claims={"sub": "other"}))
        assert status == 404
        validate("safe-error", body)
