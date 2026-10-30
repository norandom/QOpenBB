"""Execute unchanged upstream widget utilities using the image's installed core."""
import importlib
import json
import sys
import types
from copy import deepcopy
from pathlib import Path


def _results(document: dict, schema: dict, seen: set) -> list[dict]:
    if not isinstance(schema, dict) or id(schema) in seen:
        raise ValueError("Invalid financial widget response")
    seen = seen | {id(schema)}
    if "$ref" in schema:
        reference = schema["$ref"]
        if not isinstance(reference, str) or not reference.startswith("#/components/schemas/"):
            raise ValueError("Invalid financial widget reference")
        name = reference.removeprefix("#/components/schemas/").replace("~1", "/").replace("~0", "~")
        try:
            return _results(document, document["components"]["schemas"][name], seen)
        except KeyError:
            raise ValueError("Unresolved financial widget reference") from None
    found = [schema["properties"]["results"]] if "results" in schema.get("properties", {}) else []
    for branch in schema.get("allOf", []):
        found.extend(_results(document, branch, seen))
    return found


def widget_schema(document: dict) -> dict:
    """Give native UI generation an inline view without changing the API contract."""
    result = deepcopy(document)
    for path in result["paths"].values():
        for operation in path.values():
            if not isinstance(operation, dict) or "x-qopenbb-financial" not in operation:
                continue
            rows = _results(result, operation["x-qopenbb-financial"]["response_schema"], set())
            if len(rows) != 1:
                raise ValueError("Financial widget requires one results schema")
            # Native utilities recognize inline envelopes, but their OBBject-name
            # heuristic cannot recognize the service's composed financial schema.
            operation["responses"]["200"]["content"]["application/json"]["schema"] = {
                "type": "object", "properties": {"results": deepcopy(rows[0])}}
            operation.setdefault("widget_config", {}).setdefault("data", {})["dataKey"] = "results"
    return result


def main() -> None:
    # A namespace loads only the two accepted utilities, without launcher extras.
    package = types.ModuleType("qopenbb_upstream")
    package.__path__ = ["/generator"]
    sys.modules[package.__name__] = package
    module = importlib.import_module("qopenbb_upstream.widgets")
    schema = json.loads(Path("/input/schema.json").read_text())
    result = module.build_json(widget_schema(schema), [])
    print("QOPENBB_CATALOG=" + json.dumps(result, sort_keys=True, allow_nan=False))


if __name__ == "__main__":
    main()
