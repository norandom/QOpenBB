"""Follow generated Workspace discovery through the signed internal listener."""

from urllib.parse import urlencode

from test_model_identity import assertion
from test_model_listener import exchange, internal_listener
from test_orchestration import OWNER, request
from test_orchestration import inputs as snapshot_fixture
from test_orchestration import service as evaluation_fixture

snapshot = snapshot_fixture
evaluations = evaluation_fixture


def test_widget_discovery_reopens_the_same_private_result(
    evaluations, snapshot, tmp_path
):
    run = evaluations().evaluate(request(inputs=snapshot), OWNER)
    directory = tmp_path / "runs"
    original = {p.name: p.read_bytes() for p in directory.iterdir()}
    with internal_listener(directory) as origin:
        base = origin + "/modeling/v1"
        owner = assertion(claims={"sub": OWNER.subject})
        for path in ("/widgets.json", "/apps.json", "/widget-results"):
            assert exchange(base + path)[0] == 401
        status, catalog = exchange(base + "/widgets.json", owner)
        assert status == 200
        (widget,) = catalog.values()
        status, apps = exchange(base + "/apps.json", owner)
        assert status == 200 and len(apps) == 1
        endpoint = base + "/" + widget["endpoint"].lstrip("/")
        assert exchange(endpoint, owner)[0] == 422
        url = endpoint + "?" + urlencode({"run_id": run.run_id, "output_id": "value"})
        assert exchange(url, assertion(claims={"sub": "other"}))[0] == 404
        status, output = exchange(url, owner)
        assert status == 200
        (row,) = output[widget["data"]["dataKey"]]
        assert row["status"] == "verified" and row["freshness"] == "saved"
        assert row["display_text"] == run.model_dump(mode="json")["outputs"][0]["value"]
        assert exchange(base + f"/runs/{run.run_id}/outputs/value", owner) == (
            200,
            output,
        )
        status, previous = exchange(url + "&expected_run_id=" + "a" * 32, owner)
        assert status == 200 and previous["results"][0]["freshness"] == "stale"
        assert (
            exchange(url + "&expected_run_id=" + run.run_id, owner)[1]["results"][0][
                "freshness"
            ]
            == "matched"
        )
    assert {p.name: p.read_bytes() for p in directory.iterdir()} == original
