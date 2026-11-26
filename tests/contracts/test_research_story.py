"""Check synthetic story wire examples against installed modeling methods."""

import asyncio
import json
import os
import shutil
import subprocess
from datetime import datetime
from decimal import Decimal
from pathlib import Path

import pytest
from qopenbb_ci.catalog import canonical, generate
from qopenbb_ci.catalog_runtime import ASSET
from qopenbb_data.gallery import load_gallery
from qopenbb_data.modeling.contracts import ModelRun
from qopenbb_data.modeling.service.acquisition import AcquisitionError
from qopenbb_data.modeling.service.bootstrap import installed_methods
from qopenbb_data.modeling.service.evaluation import EvaluationRequest
from qopenbb_data.modeling.service.http import create_model_app
from qopenbb_data.modeling.service.identity import IdentityVerifier
from qopenbb_data.modeling.service.orchestrator import Orchestrator
from qopenbb_data.modeling.service.run_store import FileRunStore, RunStoreError

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / "contracts/consumers/research-stories"
STORY = FIXTURES / "story.v1.json"
RUN_CASES = FIXTURES / "runs.v1.json"


def test_generated_research_story_catalog(tmp_path):
    def read_contract(name):
        return json.loads((ROOT / "contracts" / name).read_text(encoding="utf-8"))

    published_apps = read_contract("apps.json")
    lock = json.loads((ROOT / "sources.lock.json").read_text(encoding="utf-8"))
    source = Path(os.environ.get("QOPENBB_DATA_SOURCE", str(ROOT / lock["data_api"]["local_checkout"])))
    output = generate(
        read_contract("openapi.json"),
        read_contract("datasets.json"),
        read_contract("widgets.json"),
        json.loads((source / ASSET).read_text(encoding="utf-8")),
        "/data",
    )
    apps_path = tmp_path / "apps.json"
    apps_path.write_bytes(canonical(output["apps.json"]))
    apps = json.loads(apps_path.read_text(encoding="utf-8"))
    frozen = json.loads(STORY.read_text(encoding="utf-8"))["catalog"]
    widget_id = frozen["widget"]["widgetId"]
    app_name = frozen["widget"]["name"]
    existing = [app for app in apps if app["name"] != app_name]
    assert existing == [app for app in published_apps if app["name"] != app_name]
    story, = [app for app in apps if app["name"] == app_name]
    assert story["description"] == (
        "Did the selected commodity proxy outperform the selected technology proxy "
        "over the 63 trading sessions ending at the observation date?"
    )
    tab, = story["tabs"].values()
    layout, = tab["layout"]
    assert layout["i"] == widget_id
    assert layout["view_order"] == frozen["view_order"]
    assert layout["state"] == {"storage": {"researchStory": frozen["default_state"]}}
    assert output["widgets.json"][widget_id] == frozen["widget"]
    (tmp_path / "widgets.json").write_bytes(canonical(output["widgets.json"]))
    shutil.copytree(ROOT / "contracts/gallery", tmp_path / "gallery")
    gallery = load_gallery(tmp_path)
    assert gallery.apps() == apps + read_contract("gallery/catalog.json")["apps"]
    assert gallery.widgets()[widget_id] == frozen["widget"]


@pytest.fixture
def wire():
    return json.loads(STORY.read_text(encoding="utf-8")) | json.loads(
        RUN_CASES.read_text(encoding="utf-8")
    )


@pytest.fixture
def installed_story(monkeypatch, tmp_path):
    monkeypatch.syspath_prepend(str(ROOT / "tests/factors"))
    from fixtures.factor_examples import (
        EXAMPLES,
        UNKNOWN_DFII10_AVAILABILITY,
        build_run,
    )
    from test_model_http import call
    from test_model_identity import ENV, assertion

    for key, value in ENV.items():
        monkeypatch.setenv(key, value)

    def snapshot(request, variant, retrieval, leg_errors):
        params = dict(request.parameters)
        pair = request.dataset_id == "story.etf_pair"
        model = "proxy_comparison" if pair else "real_yield_regime"
        example = (
            UNKNOWN_DFII10_AVAILABILITY
            if variant == "unavailable_macro"
            else EXAMPLES[model]
        )
        base = build_run(
            example, missing=variant in {"partial_leg", "unavailable_macro"}
        ).inputs
        entities = {"fixture_us_listing": params["calendar_id"]}
        if pair:
            entities.update(
                fixture_left=params["left_proxy"], fixture_right=params["right_proxy"]
            )
        tables = []
        for table in base.tables:
            if table.table_id.removesuffix("_closes") + "_error" in leg_errors:
                tables.append(table.model_copy(update={"rows": ()}))
                continue
            rows = []
            for index, row in enumerate(table.rows):
                entity = entities.get(row.entity_id, row.entity_id)
                value = row.value
                if (
                    variant in {"tiny_negative", "tie"}
                    and table.table_id == "left_closes"
                    and index > 0
                ):
                    # The right leg gained 10%. Keep a negative spread below display precision.
                    value = Decimal(
                        "110" if variant == "tie" else "109.99999999999999999999"
                    )
                price = pair and table.table_id in {"left_closes", "right_closes"}
                rows.append(
                    row.model_copy(
                        update={
                            "entity_id": entity,
                            "record_id": f"{entity}.{row.metric_id}.{row.observation_date}",
                            "source_record_id": f"synthetic-row.{row.record_id}",
                            "value": value,
                            **(
                                {
                                    "category": "provider",
                                    "published_at": None,
                                    "vintage_at": None,
                                    "context": row.context.model_copy(
                                        update={"vintage_coverage": "unknown"}
                                    ),
                                }
                                if price
                                else {}
                            ),
                        }
                    )
                )
            tables.append(table.model_copy(update={"rows": tuple(rows)}))
        query = request.parameters
        if pair:
            query = (
                ("dataset_id", request.dataset_id),
                *query,
                *(
                    (key, value)
                    for key, value in retrieval.items()
                    if key.endswith("_retrieved_at") and value is not None
                ),
                *leg_errors.items(),
            )
        provenance = base.provenance.model_copy(
            update={
                "source": "fmp" if pair else "synthetic_research_story",
                "origin": "service_acquired",
                "query": query,
                "acquisition_id": variant,
                "retrieved_at": (
                    datetime.fromisoformat(retrieval["retrieved_at"])
                    if pair
                    else request.cutoff.evaluated_at
                ),
            }
        )
        return base.model_copy(
            update={
                "cutoff": request.cutoff,
                "tables": tuple(tables),
                "provenance": provenance,
            }
        )

    class SyntheticSource:
        variant = "comparison"
        retrieval = None
        leg_errors = None

        def acquire(self, request, *, deadline, cancel):
            assert deadline is not None
            if self.variant == "macro_service_unavailable":
                raise AcquisitionError("upstream")
            return snapshot(request, self.variant, self.retrieval, self.leg_errors)

    class ReadbackFailureStore(FileRunStore):
        fail_readback = False

        def get(self, run_id, principal):
            if self.fail_readback:
                self.fail_readback = False
                raise RunStoreError("Synthetic post-publication readback failure")
            return super().get(run_id, principal)

    registry, bindings = installed_methods()
    source = SyntheticSource()
    store = ReadbackFailureStore(tmp_path / "runs")

    def validate_synthetic_calendar(cutoff, calendar_id, revision):
        if (cutoff.observation_date.isoformat(), calendar_id, revision) != (
            "2024-04-03", "NYSE_ARCA", "synthetic-nyse-arca.2024r1",
        ):
            raise ValueError("Unknown synthetic story schedule")

    service = Orchestrator(
        registry, bindings, store, snapshot_source=source, story_calendar=validate_synthetic_calendar
    )
    app = create_model_app(service, registry, IdentityVerifier.from_env())

    def exchange(path, body=None, *, owner="fixture_analyst"):
        token = assertion(claims={"sub": owner})
        payload = json.dumps(body).encode() if body is not None else None
        return asyncio.run(call(app, path, token=token, body=payload))

    return exchange, source, store


def test_synthetic_research_story_round_trip(wire, installed_story, tmp_path):
    exchange, source, store = installed_story
    runs = {}
    errors = {}
    for name, case in wire["cases"].items():
        source.variant = name
        source.retrieval = case.get("retrieval", wire["price_evidence"]["retrieval"])
        source.leg_errors = case.get("leg_errors", {})
        request = wire["requests"][case["request"]]
        if "override_cutoff" in case:
            request = {
                **request,
                "acquisition": {
                    **request["acquisition"],
                    "cutoff": request["acquisition"]["cutoff"]
                    | case["override_cutoff"],
                },
            }
        if "override_pair" in case:
            pair = case["override_pair"]
            request = {
                **request,
                "acquisition": {
                    **request["acquisition"],
                    "parameters": [
                        [key, pair.get(key, value)]
                        for key, value in request["acquisition"]["parameters"]
                    ],
                },
                "assumptions": {
                    **request["assumptions"],
                    "assumptions": [
                        {
                            **item,
                            "value": pair.get(item["assumption_id"], item["value"]),
                        }
                        for item in request["assumptions"]["assumptions"]
                    ],
                },
            }
        typed = EvaluationRequest.model_validate(request)
        assert (
            typed.model_dump(mode="json", exclude_none=True, exclude_defaults=True)
            == request
        )
        store.fail_readback = name == "recovery"
        status, body = exchange("/evaluations", request)
        if "error" in case:
            assert status == 503
            assert {"code": body["code"], "retryable": body["retryable"]} == case[
                "error"
            ]
            errors[name] = body
            if name != "recovery":
                assert "run_id" not in body
                continue
            status, body = exchange("/runs/" + body["run_id"])
        assert status == 200, body
        run = ModelRun.model_validate(body)
        assert run.model_dump(mode="json") == body
        assert body["inputs"]["cutoff"] == request["acquisition"]["cutoff"]
        assert run.assumptions == typed.assumptions
        assert run.owner_id == "fixture_analyst"
        path = "/runs/" + run.run_id
        assert exchange(path) == (200, body)
        other_status, errors[f"{name}_cross_owner"] = exchange(
            path, owner="other_analyst"
        )
        absent_status, absent = exchange("/runs/" + "f" * 32)
        assert other_status == absent_status == 404
        assert errors[f"{name}_cross_owner"]["code"] == absent["code"] == "not_found"
        runs[name] = body

    evidence = tmp_path / "wire.json"
    evidence.write_text(json.dumps({"runs": runs, "errors": errors}), encoding="utf-8")
    subprocess.run(
        [
            "node",
            str(Path(__file__).with_suffix(".mts")),
            str(STORY),
            str(RUN_CASES),
            str(evidence),
        ],
        check=True,
        cwd=ROOT,
    )
