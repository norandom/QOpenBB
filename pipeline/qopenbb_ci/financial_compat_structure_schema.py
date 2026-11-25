"""Prove a limited set of directional changes in exported modeling schemas."""

import json

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError

ANNOTATIONS = {"title", "description", "example", "examples", "$comment"}
MISSING = object()
_VALUE_CONSTRAINTS = {
    "type",
    "enum",
    "const",
    "minLength",
    "maxLength",
    "pattern",
    "format",
    "minimum",
    "maximum",
    "exclusiveMinimum",
    "exclusiveMaximum",
    "multipleOf",
    "minItems",
    "maxItems",
    "uniqueItems",
    "minProperties",
    "maxProperties",
}
_SCHEMA_MAPS = {"properties", "patternProperties", "$defs", "dependentSchemas"}
_SCHEMA_LISTS = {"allOf", "anyOf", "oneOf", "prefixItems"}
_SCHEMA_CHILDREN = {
    "items",
    "additionalProperties",
    "not",
    "if",
    "then",
    "else",
    "contains",
    "propertyNames",
    "unevaluatedItems",
    "unevaluatedProperties",
}
_OBJECT_KEYWORDS = {
    "type",
    "properties",
    "required",
    "additionalProperties",
    "$defs",
    "$schema",
    "default",
}


def same(old: object, new: object) -> bool:
    if old is MISSING or new is MISSING:
        return old is new
    # Python equality conflates JSON booleans and numbers, including inside enums.
    return json.dumps(old, sort_keys=True) == json.dumps(new, sort_keys=True)


def literals(value: list) -> set[str]:
    return {json.dumps(item, sort_keys=True) for item in value}


def delta(old: object, new: object, path: str, *, kind: str) -> list[str]:
    """Locate every changed member in an opaque contract document."""
    if same(old, new):
        return []
    if isinstance(old, dict) and isinstance(new, dict):
        return [
            issue
            for key in sorted(old.keys() | new.keys())
            for issue in delta(
                old.get(key, MISSING), new.get(key, MISSING), f"{path}/{key}", kind=kind
            )
        ]
    if isinstance(old, list) and isinstance(new, list) and len(old) == len(new):
        return [
            issue
            for index, (before, after) in enumerate(zip(old, new, strict=True))
            for issue in delta(before, after, f"{path}/{index}", kind=kind)
        ]
    return [f"{kind}: {path} changed"]


def schema_shape(schema: object, *, embedded_prefix: str = "") -> object:
    if not isinstance(schema, dict):
        return schema
    result = {}
    for key, value in schema.items():
        if key in _SCHEMA_MAPS and isinstance(value, dict):
            result[key] = {
                name: schema_shape(item, embedded_prefix=embedded_prefix)
                for name, item in value.items()
            }
        elif key in _SCHEMA_LISTS and isinstance(value, list):
            result[key] = [
                schema_shape(item, embedded_prefix=embedded_prefix) for item in value
            ]
        elif key in _SCHEMA_CHILDREN:
            result[key] = schema_shape(value, embedded_prefix=embedded_prefix)
        elif key == "$ref" and embedded_prefix and isinstance(value, str):
            result[key] = (
                "#" + value.removeprefix(embedded_prefix)
                if value.startswith(embedded_prefix)
                else value
            )
        elif key not in ANNOTATIONS:
            result[key] = value
    return result


def _reference_scope(
    node: object, prefix: str, definitions: dict, *, monotone: bool = True
) -> bool:
    if isinstance(node, list):
        return all(
            _reference_scope(item, prefix, definitions, monotone=monotone)
            for item in node
        )
    if not isinstance(node, dict):
        return True
    if node.keys() & {
        "$id",
        "$dynamicRef",
        "$dynamicAnchor",
        "$anchor",
        "$recursiveRef",
    }:
        return False
    if "$ref" in node:
        reference = node["$ref"]
        if not monotone or not reference.startswith(prefix):
            return False
        target = reference.removeprefix(prefix)
        if (
            "/" in target
            or target.replace("~1", "/").replace("~0", "~") not in definitions
        ):
            return False
    for key in node.keys() & _SCHEMA_MAPS:
        if not all(
            _reference_scope(item, prefix, definitions, monotone=monotone)
            for item in node[key].values()
        ):
            return False
    for key in node.keys() & (_SCHEMA_LISTS | _SCHEMA_CHILDREN):
        positive = monotone and key not in {"not", "if", "oneOf", "contains"}
        if not _reference_scope(node[key], prefix, definitions, monotone=positive):
            return False
    return True


def compare_document_schema(
    old: object,
    new: object,
    path: str,
    direction: str,
    *,
    ref_prefix: str = "#/$defs/",
) -> list[str]:
    if same(old, new):
        return []
    if not isinstance(old, dict) or not isinstance(new, dict):
        return [f"unknown: {path} expected a schema object"]
    for schema in (old, new):
        try:
            Draft202012Validator.check_schema(schema)
        except SchemaError:
            return [f"unknown: {path} invalid JSON Schema"]
    before, after = schema_shape(old), schema_shape(new)
    if same(before, after):
        return []
    if not all(
        _reference_scope(schema, ref_prefix, schema.get("$defs", {}))
        for schema in (before, after)
    ):
        return [f"unknown: {path} schema uses an unsupported reference scope"]
    return compare_schema(before, after, path, direction)


def _null_branch(schema: dict) -> tuple[dict, bool]:
    alternatives = schema.get("anyOf")
    if (
        schema.keys() <= ANNOTATIONS | {"anyOf"}
        and isinstance(alternatives, list)
        and len(alternatives) == 2
    ):
        branches = [
            {k: v for k, v in item.items() if k not in ANNOTATIONS}
            for item in alternatives
            if isinstance(item, dict)
        ]
        if len(branches) == 2 and {"type": "null"} in branches:
            other = next((item for item in branches if item != {"type": "null"}), {})
            if isinstance(other.get("type"), str):
                return other, True
    return schema, False


def _enum_or_type(value: object) -> set[str] | None:
    if isinstance(value, list):
        return literals(value)
    if isinstance(value, str):
        return literals([value])
    return None


def _allows_direction(old: set[str], new: set[str], direction: str) -> bool:
    return (
        direction == "input"
        and old <= new
        or direction == "output"
        and new <= old
        or old == new
    )


def _properties(old: dict, new: dict, path: str, direction: str) -> list[str]:
    before, after = old.get("properties", {}), new.get("properties", {})
    added = after.keys() - before.keys()
    simple = (old.keys() | new.keys()) <= _OBJECT_KEYWORDS | ANNOTATIONS
    old_required = set(old.get("required", []))
    new_required = set(new.get("required", []))
    findings = []
    for name in sorted(before.keys() | after.keys()):
        location = f"{path}/properties/{name}"
        if name in before and name in after:
            findings.extend(
                compare_schema(before[name], after[name], location, direction)
            )
        elif name not in added:
            findings.append(f"incompatible: {location} removed")
        elif not simple or not _can_add_field(old, new, name, new_required, direction):
            findings.append(f"incompatible: {location} addition is unproven")
    if not _allows_direction(new_required, old_required, direction):
        findings.append(
            f"incompatible: {path}/required changed "
            f"(added {sorted(new_required - old_required)}, "
            f"removed {sorted(old_required - new_required)})"
        )
    return findings


def _can_add_field(
    old: dict, new: dict, name: str, required: set, direction: str
) -> bool:
    # A newly declared input field can constrain a formerly unconstrained key.
    if direction == "input":
        return (
            old.get("additionalProperties") is False
            and name not in required
            and isinstance(new["properties"][name], dict)
            and new["properties"][name].keys() <= _VALUE_CONSTRAINTS | ANNOTATIONS
        )
    return (
        direction == "output"
        and old.get("additionalProperties", True) is True
        and name not in old.get("required", [])
        and isinstance(new["properties"][name], dict)
        and new["properties"][name].keys() <= _VALUE_CONSTRAINTS | ANNOTATIONS
    )


def _compare_children(
    old: object, new: object, key: str, path: str, direction: str
) -> list[str]:
    if key == "$defs" and isinstance(old, dict) and isinstance(new, dict):
        return [
            issue
            for name in sorted(old.keys() | new.keys())
            for issue in compare_schema(
                old.get(name, MISSING),
                new.get(name, MISSING),
                f"{path}/{name}",
                direction,
            )
        ]
    if key == "items" and isinstance(old, dict) and isinstance(new, dict):
        return compare_schema(old, new, path, direction)
    if (
        key == "prefixItems"
        and isinstance(old, list)
        and isinstance(new, list)
        and len(old) == len(new)
    ):
        return [
            issue
            for index, (before, after) in enumerate(zip(old, new, strict=True))
            for issue in compare_schema(before, after, f"{path}/{index}", direction)
        ]
    return delta(old, new, path, kind="unknown")


def _constraint(
    old: object, new: object, key: str, path: str, direction: str
) -> list[str]:
    if key in {"type", "enum"}:
        before, after = _enum_or_type(old), _enum_or_type(new)
        if (
            before is not None
            and after is not None
            and _allows_direction(before, after, direction)
        ):
            return []
    kind = (
        "incompatible"
        if key in _VALUE_CONSTRAINTS | {"default", "additionalProperties"}
        else "unknown"
    )
    return delta(old, new, path, kind=kind)


def compare_schema(old: object, new: object, path: str, direction: str) -> list[str]:
    if same(old, new):
        return []
    if not isinstance(old, dict) or not isinstance(new, dict):
        return delta(old, new, path, kind="unknown")
    old_body, old_null = _null_branch(old)
    new_body, new_null = _null_branch(new)
    if (
        (old_null or new_null)
        and isinstance(old_body.get("type"), str)
        and isinstance(new_body.get("type"), str)
    ):
        issues = compare_schema(old_body, new_body, path, direction)
        if not _allows_direction(
            {"null"} if old_null else set(), {"null"} if new_null else set(), direction
        ):
            issues.append(f"incompatible: {path} nullability changed")
        return issues
    findings = _properties(old, new, path, direction)
    for key in sorted(
        (old.keys() | new.keys()) - ANNOTATIONS - {"properties", "required"}
    ):
        before, after = old.get(key, MISSING), new.get(key, MISSING)
        if same(before, after):
            continue
        location = f"{path}/{key}"
        if key in {"$defs", "items", "prefixItems"}:
            findings.extend(_compare_children(before, after, key, location, direction))
        else:
            findings.extend(_constraint(before, after, key, location, direction))
    return findings
