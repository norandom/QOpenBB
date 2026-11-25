"""Match the pinned Workspace consumer to the published operation and widget."""

from .financial_compat_structure_api import index_parameters
from .financial_compat_structure_schema import ANNOTATIONS, literals


def _closed_rows(consumer: dict) -> bool:
    response = consumer["response"]
    return (
        response.get("closed") is True
        or response.get("additionalProperties") is False
        or consumer.get("closed_response") is True
    )


def _resolve(document: dict, schema: dict) -> dict:
    visited = set()
    while "$ref" in schema:
        reference = schema["$ref"]
        if (
            not reference.startswith("#/")
            or schema.keys() - ANNOTATIONS != {"$ref"}
            or reference in visited
        ):
            raise ValueError("unsupported schema reference")
        visited.add(reference)
        schema = document
        for token in reference[2:].split("/"):
            schema = schema[token.replace("~1", "/").replace("~0", "~")]
    return schema


def _schema_types(schema: dict) -> set:
    if "anyOf" in schema and schema.keys() <= {
        "anyOf",
        "title",
        "description",
        "examples",
        "example",
        "$comment",
        "default",
    }:
        return set().union(*(_schema_types(branch) for branch in schema["anyOf"]))
    types = schema["type"]
    return set(types) if isinstance(types, list) else {types}


def _check_rows(document: dict, schema: dict, consumer: dict, label: str) -> list[str]:
    response = consumer["response"]
    schema = _resolve(document, schema)
    key = response["data_key"]
    rows = _resolve(document, schema["properties"][key])
    if key not in schema["required"] or rows.get("type") != "array":
        return [f"incompatible: {label}/{key} is not a required row array"]
    if "prefixItems" in rows:
        if len(rows["prefixItems"]) != 1 or rows.get("maxItems") != 1:
            return [f"unknown: {label}/{key} uses an unsupported row tuple"]
        item = rows["prefixItems"][0]
    else:
        item = rows["items"]
    row = _resolve(document, item)
    issues = []
    fields = {field["name"] for field in response["row_fields"]}
    if _closed_rows(consumer) and (
        row.get("additionalProperties") is not False
        or row.get("patternProperties")
        or row["properties"].keys() - fields
    ):
        issues.append(
            f"incompatible: {label}/{key} can return fields outside the closed consumer"
        )
    for field in response["row_fields"]:
        name = field["name"]
        location = f"{label}/{key}/{name}"
        if name not in row.get("required", []):
            issues.append(f"incompatible: {location} may be absent")
            continue
        actual = _resolve(document, row["properties"][name])
        expected = {field["type"]} | ({"null"} if field["nullable"] else set())
        if not _schema_types(actual) <= expected:
            issues.append(f"incompatible: {location} type or nullability changed")
        if "values" in field:
            values = actual.get(
                "enum", [actual["const"]] if "const" in actual else None
            )
            if values is None or not literals(values) <= literals(field["values"]):
                issues.append(f"incompatible: {location} can return unsupported values")
    return issues


def _check_query(operation: dict, expected: list, label: str) -> list[str]:
    parameters = index_parameters(operation.get("parameters", []))
    expected_by_name = {item["parameter"]: item for item in expected}
    issues = []
    for name, item in expected_by_name.items():
        actual = parameters.get(("query", name))
        if (
            actual is None
            or item["type"] not in _schema_types(actual["schema"])
            or actual.get("required", False)
            and not item["required"]
        ):
            issues.append(f"incompatible: {label}/query/{name} binding changed")
    for (place, name), parameter in parameters.items():
        if parameter.get("required", False) and (
            place != "query" or name not in expected_by_name
        ):
            issues.append(f"incompatible: {label}/{place}/{name} has no binding")
    return issues


def _check_widget(widget: dict, consumer: dict, label: str) -> list[str]:
    operation, response = consumer["operation"], consumer["response"]
    data = widget["data"]
    issues = []
    if widget["widgetId"] != consumer["widget_id"] or widget["endpoint"] != operation[
        "path"
    ].lstrip("/"):
        issues.append(f"incompatible: {label} widget endpoint or ID changed")
    if data["dataKey"] != response["data_key"]:
        issues.append(f"incompatible: {label}/dataKey binding changed")
    columns = [column["field"] for column in data["table"]["columnsDefs"]]
    if columns != [field["name"] for field in response["row_fields"]]:
        issues.append(f"incompatible: {label} widget columns changed")
    params = [(p["paramName"], not p["optional"]) for p in widget["params"]]
    if params != [(p["parameter"], p["required"]) for p in operation["query"]]:
        issues.append(f"incompatible: {label} widget query binding changed")
    controls = {
        "string": "text",
        "integer": "number",
        "number": "number",
        "boolean": "boolean",
    }
    for param, binding in zip(widget["params"], operation["query"], strict=False):
        if controls.get(binding["type"]) != param["type"]:
            issues.append(
                f"incompatible: {label}/params/{param['paramName']} widget control type changed"
            )
    return issues


def check_binding(bundle: dict, consumer: dict, label: str) -> list[str]:
    operation = consumer["operation"]
    api = bundle["openapi.json"]
    actual = api["paths"][operation["path"]][operation["method"].lower()]
    location = f"{label}/openapi.json/{operation['id']}"
    issues = []
    if (
        actual["operationId"] != operation["id"]
        or operation["base_path"].rstrip("/").split("/")[-1]
        != consumer["provider_api_version"]
        or not any(entry["url"] == operation["base_path"] for entry in api["servers"])
    ):
        issues.append(
            f"incompatible: {location} operation ID or API version binding changed"
        )
    issues.extend(_check_query(actual, operation["query"], location))
    schema = actual["responses"]["200"]["content"]["application/json"]["schema"]
    issues.extend(_check_rows(api, schema, consumer, location))
    standalone = bundle["widget-projection.schema.json"]
    issues.extend(
        _check_rows(
            standalone, standalone, consumer, f"{label}/widget-projection.schema.json"
        )
    )
    widget = bundle["widgets.json"][consumer["widget_id"]]
    issues.extend(
        _check_widget(widget, consumer, f"{label}/widgets.json/{consumer['widget_id']}")
    )
    return issues
