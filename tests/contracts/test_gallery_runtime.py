"""Packaged gallery lookup and discovery require no provider or runtime imports."""
import asyncio
import importlib.util
import json
import sys
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "services/data-api"))

from qopenbb_data.gallery import load_gallery


@pytest.fixture
def packaged(tmp_path):
    source = {"id": "prices-aapl", "provider": "FMP", "endpoint": "/historical-price-full/AAPL",
              "parameters": {"from": "2024-09-30", "to": "2025-01-31"},
              "retrievedAt": "2026-10-27T12:00:00+00:00", "sha256": "a" * 64,
              "limitations": ["Adjustment basis unverified."]}
    dataset = {"results": [{"date": "2025-01-02", "AAPL": 243.85},
                           {"date": "2025-01-03", "AAPL": None}], "metadata": {
        "id": "january-prices", "title": "Apple January 2025 close (USD/share)",
        "sourceIds": ["prices-aapl"], "observationStart": "2025-01-02",
        "observationEnd": "2025-01-31", "columns": [
            {"field": "date", "type": "date", "unit": "ISO trading date", "label": "Trading date"},
            {"field": "AAPL", "type": "number", "unit": "USD/share", "label": "Apple close"}],
        "transformation": "Selected historical observations; no rounding.",
        "limitations": ["Missing observations remain null."]}}
    widget = {"widgetId": "qopenbb_gallery_line", "name": dataset["metadata"]["title"],
              "type": "table", "endpoint": "/gallery/data/january-prices", "params": [],
              "data": {"dataKey": "results", "table": {"columnsDefs": [
                  {"field": "date", "cellDataType": "dateString"},
                  {"field": "AAPL", "cellDataType": "number"}]}}}
    app = {"name": "QOpenBB Historical Chart Gallery - January 2025", "allowCustomization": True,
           "tabs": {"Overview": {"layout": [{"i": "qopenbb_gallery_line", "state": {"chartView": {
               "enabled": True, "chartType": "line"}}}]}}}
    envelope = {"schemaVersion": 1, "snapshotId": "fmp-historical-2025-01-v1"}
    files = {"widgets.json": {"canonical": {"widgetId": "canonical", "extra": [1, 2]}},
             "apps.json": [{"name": "QOpenBB starter", "tabs": {"Data": {"layout": [{"i": "canonical"}]}}}],
             "gallery/data.json": {**envelope, "sources": [source], "datasets": {"january-prices": dataset}},
             "gallery/catalog.json": {**envelope, "widgets": {widget["widgetId"]: widget}, "apps": [app]}}
    def write():
        for name, value in files.items():
            target = tmp_path / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(json.dumps(value), encoding="utf-8")
        return tmp_path
    write()
    return SimpleNamespace(root=tmp_path, files=files, write=write, dataset=dataset, widget=widget, app=app)


def test_composes_without_mutating_canonical_order_or_content(packaged):
    before = deepcopy(packaged.files)
    gallery = load_gallery(packaged.root)
    assert list(gallery.widgets()) == ["canonical", "qopenbb_gallery_line"]
    assert gallery.widgets()["canonical"] == before["widgets.json"]["canonical"]
    assert gallery.apps() == before["apps.json"] + before["gallery/catalog.json"]["apps"]
    assert packaged.files == before
    # Callers cannot change the packaged observations or a later discovery response.
    gallery.dataset("january-prices")["results"][0]["AAPL"] = 0
    gallery.widgets().clear()
    gallery.apps().clear()
    assert gallery.dataset("january-prices") == packaged.dataset
    assert len(gallery.widgets()) == len(gallery.apps()) == 2


@pytest.mark.parametrize("unknown", ["unknown", "../widgets.json", "/etc/passwd", "january-prices.json"])
def test_lookup_only_accepts_enumerated_dataset_ids(packaged, unknown):
    gallery = load_gallery(packaged.root)
    with pytest.raises(KeyError):
        gallery.dataset(unknown)


@pytest.mark.parametrize("name", ["gallery/data.json", "gallery/catalog.json", "widgets.json", "apps.json"])
def test_missing_packaged_assets_fail_explicitly(packaged, name):
    (packaged.root / name).unlink()
    with pytest.raises(FileNotFoundError):
        load_gallery(packaged.root)


@pytest.mark.parametrize("name", ["gallery/data.json", "gallery/catalog.json"])
@pytest.mark.parametrize("field,value", [("schemaVersion", 2), ("schemaVersion", True),
                                        ("schemaVersion", 1.0), ("snapshotId", "current")])
def test_incompatible_asset_versions_are_rejected(packaged, name, field, value):
    packaged.files[name][field] = value
    with pytest.raises(ValueError):
        load_gallery(packaged.write())


@pytest.mark.parametrize("mutation", ["widget-id", "widget-collision", "app-collision", "slug-collision",
                                     "duplicate-app", "dataset-ref", "app-ref", "group-ref", "source-ref",
                                     "source-id", "metadata-id", "dataset-id", "endpoint", "data-key",
                                     "column-ref", "column-type", "column-duplicate", "row-field",
                                     "row-type", "row-date", "row-infinity", "extra-envelope", "extra-dataset",
                                     "metadata-shape", "source-shape", "columns-shape", "apps-shape",
                                     "app-ref-unhashable", "row-overflow"])
def test_malformed_or_colliding_assets_fail_closed(packaged, mutation):
    files, widget, dataset, app = packaged.files, packaged.widget, packaged.dataset, packaged.app
    data, catalog = files["gallery/data.json"], files["gallery/catalog.json"]
    if mutation == "widget-id":
        widget["widgetId"] = "another-id"
    elif mutation == "widget-collision":
        files["widgets.json"]["qopenbb_gallery_line"] = deepcopy(widget)
    elif mutation in {"app-collision", "slug-collision"}:
        files["apps.json"][0]["name"] = app["name"] + ("!!!" if mutation == "slug-collision" else "")
    elif mutation == "duplicate-app":
        catalog["apps"].append(deepcopy(app))
    elif mutation == "dataset-ref":
        widget["endpoint"] = "/gallery/data/unknown"
    elif mutation == "app-ref":
        app["tabs"]["Overview"]["layout"][0]["i"] = "unknown"
    elif mutation == "group-ref":
        app["groups"] = [{"name": "Missing", "widgetIds": ["unknown"]}]
    elif mutation == "source-ref":
        dataset["metadata"]["sourceIds"] = ["unknown"]
    elif mutation == "source-id":
        data["sources"].append(deepcopy(data["sources"][0]))
    elif mutation == "metadata-id":
        dataset["metadata"]["id"] = "other"
    elif mutation == "dataset-id":
        data["datasets"]["../private"] = data["datasets"].pop("january-prices")
    elif mutation == "endpoint":
        widget["endpoint"] += "?current=true"
    elif mutation == "data-key":
        widget["data"]["dataKey"] = "rows"
    elif mutation == "column-ref":
        widget["data"]["table"]["columnsDefs"][0]["field"] = "unknown"
    elif mutation == "column-type":
        dataset["metadata"]["columns"][0]["type"] = "unknown"
    elif mutation == "column-duplicate":
        dataset["metadata"]["columns"].append(deepcopy(dataset["metadata"]["columns"][0]))
    elif mutation == "row-field":
        dataset["results"][0]["extra"] = "unknown"
    elif mutation == "row-type":
        dataset["results"][0]["AAPL"] = True
    elif mutation == "row-date":
        dataset["results"][0]["date"] = "2025-02-30"
    elif mutation == "row-infinity":
        dataset["results"][0]["AAPL"] = float("inf")
    elif mutation == "extra-envelope":
        data["private"] = "unrelated"
    elif mutation == "extra-dataset":
        dataset["private"] = "unrelated"
    elif mutation == "metadata-shape":
        dataset["metadata"] = []
    elif mutation == "source-shape":
        data["sources"] = [None]
    elif mutation == "columns-shape":
        dataset["metadata"]["columns"] = {}
    elif mutation == "apps-shape":
        catalog["apps"] = {}
    elif mutation == "app-ref-unhashable":
        app["tabs"]["Overview"]["layout"][0]["i"] = []
    elif mutation == "row-overflow":
        dataset["results"][0]["AAPL"] = 10 ** 400
    with pytest.raises(ValueError):
        load_gallery(packaged.write())


def test_duplicate_json_keys_and_overflowing_numbers_are_rejected(packaged):
    path = packaged.root / "gallery/data.json"
    original = path.read_text()
    for content in (original[:-1] + ', "datasets": {}}', original.replace("243.85", "1e999")):
        path.write_text(content)
        with pytest.raises(ValueError):
            load_gallery(packaged.root)


def test_app_registers_local_discovery_and_read_only_dataset_before_upstream(packaged, monkeypatch):
    """Exercise the adapter with explicit framework stubs; this is not ASGI acceptance."""
    class Response:
        def __init__(self, status_code, content):
            self.status_code, self.content = status_code, content
    class App:
        def __init__(self, **kwargs):
            self.routes = []
            self.middleware = []
        def add_middleware(self, middleware, **kwargs):
            self.middleware.append((middleware, kwargs))
        def get(self, path, **kwargs):
            def register(handler):
                self.routes.append(("GET", path, handler))
                return handler
            return register
        def mount(self, path, upstream):
            self.routes.append(("MOUNT", path, upstream))
    monkeypatch.setitem(sys.modules, "fastapi", SimpleNamespace(FastAPI=App))
    monkeypatch.setitem(sys.modules, "fastapi.responses", SimpleNamespace(JSONResponse=Response))
    upstream = SimpleNamespace(openapi=lambda: {"paths": {}})
    monkeypatch.setitem(sys.modules, "openbb_core.api.rest_api", SimpleNamespace(app=upstream))
    monkeypatch.setitem(sys.modules, "qopenbb_data.config", SimpleNamespace(
        configure=list, coverage_index=dict, financial_identity=dict))
    policy = object()
    monkeypatch.setitem(sys.modules, "qopenbb_data.financial_policy", SimpleNamespace(
        FinancialProviderPolicy=policy))
    spec = importlib.util.spec_from_file_location("gallery_app_under_test", ROOT / "services/data-api/qopenbb_data/app.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.CATALOG = packaged.root
    # This gallery-only seam uses framework stubs; installed ASGI tests verify
    # financial projection and mounted error handling against the native runtime.
    document = upstream.openapi()
    monkeypatch.setattr(module, "_financial_runtime", lambda template: (template, document, {"datasets": []}))
    app = module.create_app()
    assert app.middleware == [(policy, {"document": document})]
    assert app.routes[-1] == ("MOUNT", "/", upstream)
    handlers = {path: handler for method, path, handler in app.routes if method == "GET"}
    assert asyncio.run(handlers["/widgets.json"]())["canonical"] == packaged.files["widgets.json"]["canonical"]
    assert len(asyncio.run(handlers["/apps.json"]())) == 2
    assert asyncio.run(handlers["/gallery/data/{dataset_id}"]("january-prices")) == packaged.dataset
    unknown = asyncio.run(handlers["/gallery/data/{dataset_id}"]("../private"))
    assert (unknown.status_code, unknown.content) == (404, {"detail": "Not Found"})
    assert asyncio.run(handlers["/agents.json"]()) == []
    assert asyncio.run(handlers["/healthz"]()) == {"status": "ok"}
    assert app.openapi() == {"paths": {}}
    (packaged.root / "gallery/data.json").unlink()
    with pytest.raises(FileNotFoundError):
        module.create_app()
