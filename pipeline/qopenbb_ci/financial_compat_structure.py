"""Check structural and declared financial compatibility of 9.1 payloads."""

from jsonschema import Draft202012Validator
from referencing import Registry
from referencing.exceptions import Unresolvable

from .financial_compat_structure_api import compare_api
from .financial_compat_structure_binding import check_binding
from .financial_compat_structure_schema import (
    compare_document_schema,
    delta,
    same,
    schema_shape,
)

_INPUT_SCHEMAS = {"evaluation-request.schema.json", "input-snapshot.schema.json"}
_COMPONENTS = {
    "apps.schema.json": "AppDiscovery",
    "evaluation-request.schema.json": "EvaluationRequest",
    "input-snapshot.schema.json": "InputSnapshot",
    "model-descriptor.schema.json": "ModelDescriptor",
    "model-listing.schema.json": "ModelListing",
    "model-run.schema.json": "ModelRun",
    "rule-descriptor.schema.json": "RuleDescriptor",
    "safe-error.schema.json": "SafeError",
    "widget-projection.schema.json": "WidgetProjection",
    "widgets.schema.json": "WidgetDiscovery",
}
_PAYLOADS = _COMPONENTS.keys() | {
    "openapi.json",
    "descriptors.json",
    "widgets.json",
    "apps.json",
}


def _methods(document: dict) -> dict:
    if not isinstance(document["models"], list):
        raise TypeError("models must be an array")
    methods = {}
    for method in document["models"]:
        identity = (method["model_id"], method["method_version"])
        if not all(isinstance(value, str) and value.strip() for value in identity):
            raise ValueError("invalid model or method version")
        if identity in methods:
            raise ValueError("duplicate model and method version")
        methods[identity] = method
    return methods


def _rule_versions(methods: dict) -> list[str]:
    rules, sets = {}, {}
    issues = []
    for (model_id, _), method in methods.items():
        model_path = f"descriptors.json/models/{model_id}"
        rule_set = method["rules"]
        set_key = (model_id, method["rule_set_version"])
        seen = set()
        for rule in rule_set:
            rule_id, version = rule["rule_id"], rule["version"]
            if rule_id in seen:
                issues.append(
                    f"unknown: {model_path}/rules/{rule_id} appears more than once"
                )
            seen.add(rule_id)
            key = (model_id, rule_id, version)
            location = f"{model_path}/rules/{rule_id}/{version}"
            issues.extend(
                delta(rules.setdefault(key, rule), rule, location, kind="incompatible")
            )
        previous = sets.setdefault(set_key, rule_set)
        if not same(previous, rule_set):
            issues.append(
                f"incompatible: {model_path}/rule_set_version/{set_key[1]} reused with different rules"
            )
    return issues


def _descriptors(old_bundle: dict, new_bundle: dict) -> list[str]:
    old, new = old_bundle["descriptors.json"], new_bundle["descriptors.json"]
    before, after = _methods(old), _methods(new)
    path = "descriptors.json"
    issues = delta(
        {key: value for key, value in old.items() if key != "models"},
        {key: value for key, value in new.items() if key != "models"},
        path,
        kind="unknown",
    )
    schema_name = "model-descriptor.schema.json"
    pinned = Draft202012Validator(old_bundle[schema_name], registry=Registry())
    published = Draft202012Validator(new_bundle[schema_name], registry=Registry())
    for key in sorted(before.keys() | after.keys()):
        location = f"{path}/models/{'/'.join(key)}"
        if key not in after:
            issues.append(f"incompatible: {location} original method version removed")
        elif key in before:
            issues.extend(delta(before[key], after[key], location, kind="incompatible"))
        elif not pinned.is_valid(after[key]):
            issues.append(
                f"unknown: {location} new method does not match the pinned descriptor schema"
            )
        if key in after and not published.is_valid(after[key]):
            issues.append(
                f"unknown: {location} does not match the candidate descriptor schema"
            )
    if not issues:
        issues.extend(_rule_versions(after))
    return issues


def _schema_agreement(bundle: dict, label: str) -> list[str]:
    embedded = bundle["openapi.json"]["components"]["schemas"]
    issues = []
    for name, component in sorted(_COMPONENTS.items()):
        if name not in bundle or component not in embedded:
            issues.append(
                f"unknown: {label}/{name} or its embedded {component} schema is missing"
            )
            continue
        prefix = f"#/components/schemas/{component}"
        if not same(
            schema_shape(bundle[name]),
            schema_shape(embedded[component], embedded_prefix=prefix),
        ):
            issues.append(
                f"unknown: {label}/{name} and embedded {component} schema disagree"
            )
    return issues


def _evaluation_snapshot(bundle: dict, label: str) -> list[str]:
    api = bundle["openapi.json"]
    operation = api["paths"]["/evaluations"]["post"]
    request = operation["requestBody"]["content"]["application/json"]["schema"]
    component = "#/components/schemas/EvaluationRequest"
    location = f"{label}/openapi.json/paths/evaluations/InputSnapshot"
    if schema_shape(request) != {"$ref": component}:
        return [f"unknown: {location} request component binding changed"]
    schema = schema_shape(
        api["components"]["schemas"]["EvaluationRequest"], embedded_prefix=component
    )
    alternatives = schema["properties"]["inputs"]["anyOf"]
    if len(alternatives) != 2 or {"$ref": "#/$defs/InputSnapshot"} not in alternatives:
        return [f"unknown: {location} input snapshot binding changed"]
    snapshot = schema_shape(bundle["input-snapshot.schema.json"])
    public_definitions = snapshot.pop("$defs", {})
    snapshot.pop("$schema", None)
    definitions = schema["$defs"]
    if not same(snapshot, definitions.get("InputSnapshot")) or any(
        not same(value, definitions.get(name))
        for name, value in public_definitions.items()
    ):
        return [f"unknown: {location} disagrees with input-snapshot.schema.json"]
    return []


def _payload_deltas(old: dict, new: dict) -> list[str]:
    issues = []
    for name in sorted(old.keys() | new.keys() | _PAYLOADS):
        if name not in _PAYLOADS:
            issues.append(f"unknown: {name} unrecognized bundle payload")
        elif name not in new or name not in old:
            kind = "incompatible" if name in old else "unknown"
            issues.append(f"{kind}: {name} required bundle payload missing")
        elif name in _COMPONENTS:
            direction = "input" if name in _INPUT_SCHEMAS else "output"
            issues.extend(
                compare_document_schema(old[name], new[name], name, direction)
            )
        elif name == "openapi.json":
            issues.extend(compare_api(old[name], new[name]))
        elif name == "descriptors.json":
            issues.extend(_descriptors(old, new))
        else:
            issues.extend(delta(old[name], new[name], name, kind="incompatible"))
    return issues


def compare_structure(
    baseline: dict,
    candidate: dict,
    consumer: dict,
    candidate_consumer: dict,
) -> list[str]:
    """Return blocking findings for provider and consumer changes in parsed bundles."""
    issues = delta(consumer, candidate_consumer, "consumer", kind="incompatible")
    try:
        issues.extend(_payload_deltas(baseline, candidate))
        issues.extend(_schema_agreement(baseline, "baseline"))
        issues.extend(_schema_agreement(candidate, "candidate"))
        issues.extend(_evaluation_snapshot(baseline, "baseline"))
        issues.extend(_evaluation_snapshot(candidate, "candidate"))
    except (AttributeError, KeyError, TypeError, ValueError, Unresolvable) as error:
        issues.append(
            f"unknown: invalid or unsupported bundle structure ({type(error).__name__})"
        )
    bindings = [
        (baseline, consumer, "baseline"),
        (candidate, consumer, "candidate"),
    ]
    if not same(consumer, candidate_consumer):
        bindings.extend(
            (
                (baseline, candidate_consumer, "baseline/candidate-consumer"),
                (candidate, candidate_consumer, "candidate/candidate-consumer"),
            )
        )
    for bundle, declaration, label in bindings:
        try:
            issues.extend(check_binding(bundle, declaration, label))
        except (AttributeError, KeyError, TypeError, ValueError, IndexError) as error:
            issues.append(
                f"unknown: {label} consumer binding cannot be resolved ({type(error).__name__})"
            )
    return issues
