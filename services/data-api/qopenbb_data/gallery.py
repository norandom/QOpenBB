"""Validate packaged historical observations and append native discovery catalogs."""
from copy import deepcopy
from datetime import date, datetime
import json
import math
from pathlib import Path
import re

SNAPSHOT_ID = "fmp-historical-2025-01-v1"
_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]*\Z")
_SOURCE_KEYS = {"id", "provider", "endpoint", "parameters", "retrievedAt", "sha256", "limitations"}
_METADATA_KEYS = {"id", "title", "sourceIds", "observationStart", "observationEnd", "columns",
                  "transformation", "limitations"}


def _require(condition: bool, reason: str) -> None:
    if not condition:
        raise ValueError("invalid packaged gallery: " + reason)


def _object(value: object, keys: set[str] | None = None) -> dict:
    _require(isinstance(value, dict), "expected object")
    _require(keys is None or set(value) == keys, "object fields differ")
    return value


def _identifier(value: object) -> str:
    _require(isinstance(value, str) and bool(_ID.fullmatch(value)), "invalid identifier")
    return value


def _text(value: object) -> str:
    _require(isinstance(value, str) and bool(value.strip()), "expected nonempty text")
    return value


def _strings(value: object) -> list[str]:
    _require(isinstance(value, list) and all(isinstance(item, str) for item in value), "expected text list")
    return value


def _date(value: object) -> date:
    _require(isinstance(value, str) and bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", value)), "invalid ISO date")
    return date.fromisoformat(value)


def _unique(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        _require(key not in result, "duplicate JSON field")
        result[key] = value
    return result


def _finite(value: str) -> float:
    number = float(value)
    _require(math.isfinite(number), "nonfinite number")
    return number


def _read(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_unique,
                      parse_float=_finite, parse_constant=_finite)


def _envelope(value: object, fields: set[str]) -> dict:
    result = _object(value, fields | {"schemaVersion", "snapshotId"})
    _require(type(result["schemaVersion"]) is int and result["schemaVersion"] == 1, "schema version")
    _require(result["snapshotId"] == SNAPSHOT_ID, "snapshot identity")
    return result


def _sources(value: object) -> set[str]:
    _require(isinstance(value, list) and bool(value), "sources missing")
    ids = set()
    for item in value:
        source = _object(item, _SOURCE_KEYS)
        identity = _identifier(source["id"])
        _require(identity not in ids, "duplicate source identity")
        ids.add(identity)
        _text(source["provider"])
        _text(source["endpoint"])
        _object(source["parameters"])
        retrieved = datetime.fromisoformat(_text(source["retrievedAt"]))
        _require(retrieved.tzinfo is not None, "source timestamp requires timezone")
        _require(isinstance(source["sha256"], str) and bool(re.fullmatch(r"[0-9a-f]{64}", source["sha256"])),
                 "source hash")
        _strings(source["limitations"])
    return ids


def _columns(value: object) -> dict[str, str]:
    _require(isinstance(value, list) and bool(value), "columns missing")
    columns = {}
    for item in value:
        column = _object(item, {"field", "type", "unit", "label"})
        field = _identifier(column["field"])
        _require(field not in columns, "duplicate column")
        _require(column["type"] in ("string", "date", "number"), "column type")
        _text(column["unit"])
        _text(column["label"])
        columns[field] = column["type"]
    return columns


def _rows(value: object, columns: dict[str, str]) -> None:
    _require(isinstance(value, list), "expected rows")
    for item in value:
        row = _object(item, set(columns))
        for field, kind in columns.items():
            cell = row[field]
            if cell is None:
                continue
            if kind == "number":
                try:
                    finite = type(cell) in (int, float) and math.isfinite(cell)
                except OverflowError:
                    finite = False
                _require(finite, "numeric cell type")
            else:
                _require(isinstance(cell, str), "text cell type")
                if kind == "date":
                    _date(cell)


def _datasets(value: object, source_ids: set[str]) -> dict:
    datasets = _object(value)
    _require(bool(datasets), "datasets missing")
    for identity, item in datasets.items():
        _identifier(identity)
        dataset = _object(item, {"results", "metadata"})
        metadata = _object(dataset["metadata"], _METADATA_KEYS)
        _require(metadata["id"] == identity, "dataset identity")
        _text(metadata["title"])
        sources = _strings(metadata["sourceIds"])
        _require(bool(sources) and set(sources) <= source_ids, "dataset source reference")
        _require(_date(metadata["observationStart"]) <= _date(metadata["observationEnd"]), "observation order")
        _text(metadata["transformation"])
        _strings(metadata["limitations"])
        _rows(dataset["results"], _columns(metadata["columns"]))
    return datasets


def _widgets(value: object, datasets: dict) -> dict:
    widgets = _object(value)
    _require(bool(widgets), "widgets missing")
    for identity, item in widgets.items():
        _identifier(identity)
        widget = _object(item)
        _require(identity.startswith("qopenbb_gallery_") and widget.get("widgetId") == identity, "widget identity")
        _require(widget.get("type") == "table", "native table required")
        endpoint = widget.get("endpoint")
        _require(isinstance(endpoint, str) and endpoint.startswith("/gallery/data/"), "dataset endpoint")
        dataset_id = endpoint.removeprefix("/gallery/data/")
        _require(dataset_id in datasets, "widget dataset reference")
        data = _object(widget.get("data"))
        _require(data.get("dataKey") == "results", "data key")
        definitions = _object(data.get("table")).get("columnsDefs")
        _require(isinstance(definitions, list) and all(isinstance(item, dict) for item in definitions), "table columns")
        columns = _columns(datasets[dataset_id]["metadata"]["columns"])
        _require([item.get("field") for item in definitions] == list(columns), "table column references")
        for definition, kind in zip(definitions, columns.values()):
            types = {"string": ("text",), "date": ("date", "dateString"), "number": ("number",)}
            _require(definition.get("cellDataType") in types[kind], "table column type")
    return widgets


def _apps(value: object, widgets: dict) -> list:
    _require(isinstance(value, list), "expected apps")
    identities = set()
    for item in value:
        app = _object(item)
        name = _text(app.get("name"))
        # Workspace template identity uses the connector plus this ASCII slug.
        slug = re.sub(r"[^a-z0-9_-]+", "", re.sub(r"\s", "-", name.lower().strip()))
        _require(bool(slug) and slug not in identities, "duplicate app identity")
        identities.add(slug)
        tabs = _object(app.get("tabs"))
        _require(bool(tabs), "app tabs missing")
        for tab in tabs.values():
            layout = _object(tab).get("layout")
            _require(isinstance(layout, list), "expected app layout")
            for entry in layout:
                identity = _object(entry).get("i")
                _require(isinstance(identity, str) and identity in widgets, "app widget reference")
        groups = app.get("groups", [])
        _require(isinstance(groups, list), "expected app groups")
        for group in groups:
            ids = _strings(_object(group).get("widgetIds", []))
            _require(set(ids) <= widgets.keys(), "group widget reference")
    return value


class Gallery:
    def __init__(self, widgets: dict, apps: list, datasets: dict):
        self._widgets, self._apps, self._datasets = widgets, apps, datasets

    def widgets(self) -> dict:
        return deepcopy(self._widgets)

    def apps(self) -> list:
        return deepcopy(self._apps)

    def dataset(self, identity: str) -> dict:
        # Request identifiers only select already validated in-memory assets.
        return deepcopy(self._datasets[identity])


def load_gallery(catalog: Path) -> Gallery:
    data = _envelope(_read(catalog / "gallery/data.json"), {"sources", "datasets"})
    addition = _envelope(_read(catalog / "gallery/catalog.json"), {"widgets", "apps"})
    datasets = _datasets(data["datasets"], _sources(data["sources"]))
    canonical_widgets = _object(_read(catalog / "widgets.json"))
    widgets = _widgets(addition["widgets"], datasets)
    _require(not canonical_widgets.keys() & widgets.keys(), "duplicate widget identity")
    composed = {**canonical_widgets, **widgets}
    canonical_apps = _read(catalog / "apps.json")
    _require(isinstance(canonical_apps, list) and isinstance(addition["apps"], list) and bool(addition["apps"]),
             "expected canonical and gallery apps")
    apps = _apps(canonical_apps + addition["apps"], composed)
    return Gallery(composed, apps, datasets)
