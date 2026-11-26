"""Index versioned contract objects whose changes can cross repository boundaries."""

_BUNDLE = "contracts/modeling/v1/"
_CONSUMER = "contracts/consumers/financial-modeling/saved-output.v1.json"
CONTRACT_DOCUMENTS = frozenset(
    {
        _BUNDLE + name
        for name in ("openapi.json", "widgets.json", "apps.json", "descriptors.json")
    }
    | {_CONSUMER}
)
_HTTP_METHODS = frozenset(
    {"get", "put", "post", "delete", "options", "head", "patch", "trace"}
)


def _identity(kind: str, name: str) -> str:
    if not isinstance(name, str) or not name.strip():
        raise ValueError("missing identity name")
    return f"{kind}:{name}"


def _versioned_identity(kind: str, name: str, version: str) -> str:
    if not isinstance(version, str) or not version.strip():
        raise ValueError("missing identity version")
    return f"{_identity(kind, name)}@{version}"


def _add(index: dict, key: str, value: object) -> None:
    if key in index:
        raise ValueError(f"duplicate contract identity: {key}")
    index[key] = value


def _describe(document: dict) -> dict:
    result = {}
    if not isinstance(document["models"], list):
        raise TypeError("invalid model descriptors")
    for model in document["models"]:
        key = _versioned_identity("model", model["model_id"], model["method_version"])
        _add(result, key, model)
        if not isinstance(model["rules"], list):
            raise TypeError("invalid rule descriptors")
        for rule in model["rules"]:
            rule_id = _versioned_identity("rule", rule["rule_id"], rule["version"])
            _add(result.setdefault(rule_id, {}), key, rule)
    return result


def _operations(document: dict) -> dict:
    result = {}
    shared = {key: value for key, value in document.items() if key != "paths"}
    for route, definition in document["paths"].items():
        route_contract = {
            key: value for key, value in definition.items() if key not in _HTTP_METHODS
        }
        for method, operation in definition.items():
            if method in _HTTP_METHODS:
                key = _identity("operation", operation["operationId"])
                _add(result, key, (route, method, operation, route_contract, shared))
    return result


def _apps(document: list) -> dict:
    result = {}
    for app in document:
        for tab in app["tabs"].values():
            for widget in tab["layout"]:
                key = _identity("widget", widget["i"])
                result.setdefault(key, []).append(app)
    return result


def identities(path: str, document: dict | list) -> dict:
    if path == _BUNDLE + "apps.json":
        if not isinstance(document, list):
            raise TypeError("invalid app document")
        return _apps(document)
    if not isinstance(document, dict):
        raise TypeError("invalid contract document")
    if path == _BUNDLE + "openapi.json":
        return _operations(document)
    if path == _BUNDLE + "descriptors.json":
        return _describe(document)
    if path == _CONSUMER:
        return {
            _identity("consumer", document["consumer_id"]): document,
            _identity("widget", document["widget_id"]): document,
            _identity("operation", document["operation"]["id"]): document,
        }
    return {_identity("widget", key): value for key, value in document.items()}
