"""Financial renderer bindings retain installed routes and existing widget IDs."""
from copy import deepcopy
import json
from pathlib import Path

import pytest

from qopenbb_ci.catalog_renderers import bind_renderers, frontend_bindings


ROOT = Path(__file__).resolve().parents[2]


def catalog():
    return {name: json.loads((ROOT / "contracts" / name).read_text()) for name in
            ("datasets.json", "routes.json", "widgets.json", "apps.json", "catalog-report.json")}


def test_binding_keeps_existing_catalog_and_resolves_every_app_widget():
    outputs = catalog()
    before = deepcopy(outputs)
    bound = bind_renderers(outputs)
    assert outputs == before
    assert bound["widgets.json"] == before["widgets.json"]
    assert bound["apps.json"] == before["apps.json"]
    bindings = bound["renderers.json"]["bindings"]
    assert len(bindings) == 3
    assert {entry["dataset"] for entry in bindings} == {"company-profile", "annual-income", "gdp"}
    assert {entry["widget"] for entry in bindings} == set(before["widgets.json"])
    for entry in bindings:
        route = next(item for item in before["routes.json"]["routes"]
                     if item["dataset"] == entry["dataset"])
        assert entry["operationId"] == route["operationId"]
        assert entry["path"] == route["path"]
        assert entry["defaults"]["plugin"] == "Datagrid"
    assert bound["catalog-report.json"]["renderer_status"] == "bound"
    assert frontend_bindings(bound) == bound["renderers.json"]


@pytest.mark.parametrize("mutation", ["missing-widget", "provider", "path", "operation", "app", "dataset"])
def test_inconsistent_renderer_mapping_is_rejected(mutation):
    outputs = catalog()
    profile = "equity_profile_fmp_obb"
    if mutation == "missing-widget":
        outputs["widgets.json"].pop(profile)
    elif mutation == "provider":
        outputs["datasets.json"]["datasets"][0]["provider"] = "unknown"
    elif mutation == "path":
        outputs["widgets.json"][profile]["endpoint"] = "/wrong"
    elif mutation == "operation":
        outputs["routes.json"]["routes"][0]["operationId"] = "wrong"
    elif mutation == "app":
        tab = next(iter(outputs["apps.json"][0]["tabs"].values()))
        tab["layout"][0]["i"] = "unknown"
    else:
        outputs["datasets.json"]["datasets"].append(deepcopy(outputs["datasets.json"]["datasets"][0]))
    with pytest.raises(ValueError):
        bind_renderers(outputs)


def test_dynamic_fred_columns_are_explicit_and_no_financial_sum_is_default():
    bound = bind_renderers(catalog())
    bindings = bound["renderers.json"]["bindings"]
    fred = next(entry for entry in bindings if entry["dataset"] == "gdp")
    assert fred["defaults"]["columns"] == "all-declared"
    assert fred["schema_id"] == "qopenbb.fred-series.v1"
    for entry in bindings:
        assert entry["defaults"]["aggregate"] == "unique"
        assert entry["defaults"]["group_by"] == []
        assert entry["defaults"]["split_by"] == []


def test_frontend_mirror_requires_renderer_binding_before_runtime_access(tmp_path):
    from qopenbb_ci.catalog_cli import parser, run
    args = parser().parse_args([
        "--image", "unused", "--source", "unused", "--source-lock", "unused",
        "--inventory", "unused", "--output", str(tmp_path / "output"),
        "--work", str(tmp_path / "work"), "--workspace-bindings", str(tmp_path / "bindings.json"),
    ])
    with pytest.raises(ValueError, match="requires --bind-renderers"):
        run(args)


def test_frontend_mirror_rejects_changed_binding():
    bound = bind_renderers(catalog())
    bound["renderers.json"]["bindings"][0]["schema_id"] = "unreviewed"
    with pytest.raises(ValueError, match="binding differs"):
        frontend_bindings(bound)
