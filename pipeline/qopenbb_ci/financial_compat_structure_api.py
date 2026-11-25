"""Compare the exported HTTP surface and bind saved-output consumer manifests."""

import re

from .financial_compat_structure_schema import (
    MISSING,
    compare_document_schema,
    delta,
    same,
)

_INPUT_COMPONENTS = {"EvaluationRequest", "InputSnapshot"}
_OUTPUT_COMPONENTS = {
    "AppDiscovery",
    "ModelDescriptor",
    "ModelListing",
    "ModelRun",
    "RuleDescriptor",
    "SafeError",
    "WidgetDiscovery",
    "WidgetProjection",
}
_HTTP_METHODS = {"get", "put", "post", "delete", "options", "head", "patch", "trace"}


def _rest(old: dict, new: dict, path: str, handled: set[str]) -> list[str]:
    return delta(
        {key: value for key, value in old.items() if key not in handled},
        {key: value for key, value in new.items() if key not in handled},
        path,
        kind="unknown",
    )


def index_parameters(parameters: list) -> dict:
    indexed = {}
    for parameter in parameters:
        key = (parameter["in"], parameter["name"])
        if key in indexed:
            raise ValueError("duplicate OpenAPI parameter")
        indexed[key] = parameter
    return indexed


def _compare_parameters(old: list, new: list, path: str) -> list[str]:
    before, after = index_parameters(old), index_parameters(new)
    issues = []
    for key in sorted(before.keys() | after.keys()):
        location = f"{path}/parameters/{'/'.join(key)}"
        if key not in after:
            issues.append(f"incompatible: {location} removed")
        elif key not in before:
            item = after[key]
            # Optional parameters are independent only for the exporter’s scalar query form.
            if (
                key[0] != "query"
                or item.get("required", False) is not False
                or item.keys() - {"name", "in", "required", "schema", "description"}
                or item["schema"].get("type") != "string"
                or item["schema"].keys() - {"type", "description", "title", "examples"}
            ):
                issues.append(f"incompatible: {location} addition is unproven")
        else:
            previous, current = before[key], after[key]
            was_required = previous.get("required", False)
            is_required = current.get("required", False)
            if not isinstance(was_required, bool) or not isinstance(is_required, bool):
                issues.append(f"unknown: {location}/required must be a JSON boolean")
            elif (key[0] == "path" and is_required is not True) or (
                not was_required and is_required
            ):
                issues.append(f"incompatible: {location}/required changed")
            issues.extend(
                compare_document_schema(
                    previous["schema"], current["schema"], f"{location}/schema", "input"
                )
            )
            issues.extend(
                _rest(
                    previous,
                    current,
                    location,
                    {"schema", "required", "description", "example", "examples"},
                )
            )
    return issues


def _body(old: dict, new: dict, path: str, direction: str) -> list[str]:
    issues = _rest(old, new, path, {"description", "content", "required"})
    if direction == "output" and any(
        not isinstance(response.get("description"), str) for response in (old, new)
    ):
        issues.append(f"unknown: {path}/description must be a string")
    was_required, is_required = old.get("required", False), new.get("required", False)
    if not isinstance(was_required, bool) or not isinstance(is_required, bool):
        issues.append(f"unknown: {path}/required must be a JSON boolean")
    elif was_required != is_required and (direction != "input" or is_required):
        issues.append(f"incompatible: {path}/required changed")
    before, after = old.get("content", {}), new.get("content", {})
    if before.keys() != after.keys():
        return issues + [f"incompatible: {path}/content media types changed"]
    for media in sorted(before):
        location = f"{path}/content/{media}"
        issues.extend(
            compare_document_schema(
                before[media]["schema"],
                after[media]["schema"],
                f"{location}/schema",
                direction,
            )
        )
        issues.extend(
            _rest(
                before[media], after[media], location, {"schema", "example", "examples"}
            )
        )
    return issues


def _operation(old: dict, new: dict, path: str) -> list[str]:
    issues = _rest(
        old,
        new,
        path,
        {
            "responses",
            "requestBody",
            "parameters",
            "description",
            "summary",
            "operationId",
        },
    )
    if old.get("operationId") != new.get("operationId"):
        issues.append(f"incompatible: {path}/operationId changed")
    issues.extend(
        _compare_parameters(old.get("parameters", []), new.get("parameters", []), path)
    )
    if ("requestBody" in old) != ("requestBody" in new):
        issues.append(f"incompatible: {path}/requestBody presence changed")
    elif "requestBody" in old:
        issues.extend(
            _body(
                old["requestBody"], new["requestBody"], f"{path}/requestBody", "input"
            )
        )
    before, after = old["responses"], new["responses"]
    for code in sorted(before.keys() | after.keys()):
        location = f"{path}/responses/{code}"
        if code not in before or code not in after:
            issues.append(f"incompatible: {location} response status changed")
        else:
            issues.extend(_body(before[code], after[code], location, "output"))
    return issues


def _routes(old: dict, new: dict, path: str) -> list[str]:
    issues = []
    for route in sorted(old.keys() | new.keys()):
        location = f"{path}/{route.lstrip('/')}"
        if route not in new:
            issues.append(f"incompatible: {location} route removed")
        elif route not in old:
            issues.append(f"unknown: {location} new route may alter routing")
        else:
            issues.extend(_path_item(old[route], new[route], location))
    return issues


def _path_item(old: dict, new: dict, path: str) -> list[str]:
    issues = _rest(old, new, path, _HTTP_METHODS | {"description", "summary"})
    for method in sorted((old.keys() | new.keys()) & _HTTP_METHODS):
        location = f"{path}/{method}"
        if method not in new:
            issues.append(f"incompatible: {location} operation removed")
        elif method not in old:
            issues.append(f"unknown: {location} new operation")
        else:
            issues.extend(_operation(old[method], new[method], location))
    return issues


def _servers(old: list, new: list) -> list[str]:
    if same(old, new):
        return []
    # Preserve the original default server and introduce only distinct literal version paths.
    if old and same(old, new[: len(old)]):
        urls = [entry["url"] for entry in new]
        if len(set(urls)) == len(urls) and all(
            entry.keys() == {"url"}
            and re.fullmatch(r"/modeling/v[1-9][0-9]*", entry["url"])
            for entry in new[len(old) :]
        ):
            return []
    return [
        "incompatible: openapi.json/servers changed without retaining the original binding"
    ]


def _info(old: object, new: object) -> list[str]:
    issues = []
    for label, info in (("baseline", old), ("candidate", new)):
        location = f"{label}/openapi.json/info"
        fields = info if isinstance(info, dict) else {}
        if not isinstance(fields.get("title"), str):
            issues.append(f"unknown: {location}/title must be a string")
        version = fields.get("version")
        if not isinstance(version, str) or not version.strip():
            issues.append(f"unknown: {location}/version must be nonblank text")
    if isinstance(old, dict) and isinstance(new, dict):
        issues.extend(
            _rest(
                old,
                new,
                "openapi.json/info",
                {
                    "title",
                    "description",
                    "summary",
                    "version",
                },
            )
        )
    return issues


def compare_api(old: dict, new: dict) -> list[str]:
    issues = _rest(old, new, "openapi.json", {"paths", "components", "servers", "info"})
    issues.extend(_info(old.get("info"), new.get("info")))
    issues.extend(_servers(old["servers"], new["servers"]))
    issues.extend(_routes(old["paths"], new["paths"], "openapi.json/paths"))
    previous, current = old["components"], new["components"]
    issues.extend(_rest(previous, current, "openapi.json/components", {"schemas"}))
    before, after = previous["schemas"], current["schemas"]
    for name in sorted(before.keys() | after.keys()):
        direction = (
            "input"
            if name in _INPUT_COMPONENTS
            else "output"
            if name in _OUTPUT_COMPONENTS
            else "both"
        )
        issues.extend(
            compare_document_schema(
                before.get(name, MISSING),
                after.get(name, MISSING),
                f"openapi.json/components/schemas/{name}",
                direction,
                ref_prefix=f"#/components/schemas/{name}/$defs/",
            )
        )
    return issues
