"""Build read-only discovery from the validated, installed financial projection."""

import hashlib
import json
from copy import deepcopy
from datetime import date, datetime
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError, model_validator

EXTENSION = "x-qopenbb-financial"
STATES = ("documented", "retained_source", "adapted", "installed", "account_access",
          "real_data", "widget", "future_ai")
METHODS = {"get", "post", "put", "delete", "patch", "head", "options", "trace"}
FAMILY_IDS = Literal["discovery-reference", "company-intelligence", "markets",
                     "financial-analysis", "reports-documents", "funds", "expectations",
                     "news-events", "ownership", "cross-market-research", "other-assets",
                     "macro-positioning", "additional-families", "supplementary-fred",
                     "supplementary-yahoo"]
Identifier = Annotated[str, Field(pattern=r"^[A-Za-z][A-Za-z0-9_]{0,79}$")]
Digest = Annotated[str, Field(pattern=r"^[0-9a-f]{64}$")]
Revision = Annotated[str, Field(pattern=r"^[0-9a-f]{40}$")]
Image = Annotated[str, Field(pattern=r"^sha256:[0-9a-f]{64}$")]
Evidence = Annotated[str, Field(pattern=r"^(docs/|artifacts/reviewed/|vendor/)[A-Za-z0-9_./-]+$",
                                 max_length=240)]


class _Closed(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)


class _ProofIdentity(_Closed):
    source_sha256: Digest | None = None
    contract_sha256: Digest | None = None
    image_digest: Image | None = None


class _Proof(_Closed):
    checked_on: str
    evidence_path: Evidence
    identity: _ProofIdentity

    @model_validator(mode="after")
    def public_evidence(self):
        date.fromisoformat(self.checked_on)
        if ".." in self.evidence_path.split("/"):
            raise ValueError("Invalid evidence path")
        return self


class _State(_Closed):
    status: Literal["unknown", "verified", "blocked", "unsupported", "stale"] = "unknown"
    proof: _Proof | None = None

    @model_validator(mode="after")
    def proof_required(self):
        if (self.status in {"verified", "blocked", "stale"}) != (self.proof is not None):
            raise ValueError("Invalid coverage proof")
        return self


class _Dataset(_Closed):
    model: Identifier
    provider: Literal["fmp", "fred", "yfinance"]
    family: FAMILY_IDS
    states: dict[str, _State]


class _Family(_Closed):
    id: FAMILY_IDS
    provider: Literal["fmp", "fred", "yfinance"]
    label: Annotated[str, Field(min_length=1, max_length=80)]
    status: Literal["open"]
    outstanding: Annotated[str, Field(min_length=1, max_length=500)]
    documented: _State


class _Coverage(_Closed):
    schema_version: Literal[1]
    families: list[_Family]
    datasets: list[_Dataset]


class _Identity(_Closed):
    source_revision: Revision
    generation_revision: Revision
    generated_at: str
    image_digest: Image | None
    source_hashes: dict[Identifier, dict[Identifier, Digest]]

    @model_validator(mode="after")
    def utc_generation(self):
        stamp = datetime.fromisoformat(self.generated_at)
        if stamp.utcoffset() is None or stamp.utcoffset().total_seconds() != 0:
            raise ValueError("Generation requires UTC")
        return self


def _hash(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
    return hashlib.sha256(encoded).hexdigest()


def _coverage(value: dict) -> dict:
    result = _Coverage.model_validate(value).model_dump(mode="json", exclude_none=True)
    families = {item["id"]: item for item in result["families"]}
    if len(families) != len(result["families"]):
        raise ValueError("Duplicate family")
    seen = set()
    for item in result["datasets"]:
        key = (item["model"], item["provider"])
        family = families.get(item["family"], {})
        if key in seen or family.get("provider") != item["provider"]:
            raise ValueError("Invalid coverage association")
        seen.add(key)
        if not set(item["states"]).issubset(set(STATES) - {"installed"}):
            raise ValueError("Installed state is derived")
        for state, entry in item["states"].items():
            identity = entry.get("proof", {}).get("identity", {})
            required = _proof_keys(state)
            if entry["status"] in {"verified", "blocked", "stale"} and not required.issubset(identity):
                raise ValueError("Incomplete proof identity")
    return result


def _proof_keys(state: str) -> set[str]:
    if state in {"documented"}:
        return set()
    keys = {"source_sha256"}
    if state in {"real_data", "widget", "future_ai"}:
        keys.add("contract_sha256")
    if state in {"widget", "future_ai"}:
        keys.add("image_digest")
    return keys


def _states(record: dict, current: dict) -> dict:
    result = {state: deepcopy(record.get("states", {}).get(state, {"status": "unknown"}))
              for state in STATES}
    for name, entry in result.items():
        # Retained archives and public documentation describe fixed historical sources.
        if name in {"documented", "retained_source"} or "proof" not in entry:
            continue
        identity = entry["proof"]["identity"]
        if any(current.get(key) != value for key, value in identity.items()):
            entry["status"] = "stale"
    return result


def _resolve(document: dict, value: dict) -> dict:
    seen = set()
    while "$ref" in value:
        ref = value["$ref"]
        if not isinstance(ref, str) or not ref.startswith("#/") or ref in seen:
            raise ValueError("Invalid reference")
        seen.add(ref)
        value = document
        for part in ref[2:].split("/"):
            value = value[part.replace("~1", "/").replace("~0", "~")]
        if not isinstance(value, dict):
            raise TypeError("Invalid reference target")
    return value


def _context(document: dict, value: object, schemas: dict) -> None:
    """Copy only transitively referenced components, retaining their local pointers."""
    if isinstance(value, list):
        for child in value:
            _context(document, child, schemas)
    elif isinstance(value, dict):
        if "$ref" in value:
            ref = value["$ref"]
            if not isinstance(ref, str) or not ref.startswith("#/components/schemas/"):
                raise ValueError("Invalid schema reference")
            name = ref.removeprefix("#/components/schemas/")
            if "/" in name:
                raise ValueError("Invalid schema component")
            if name not in schemas:
                target = document["components"]["schemas"][name.replace("~1", "/").replace("~0", "~")]
                schemas[name.replace("~1", "/").replace("~0", "~")] = deepcopy(target)
                _context(document, target, schemas)
        for key, child in value.items():
            if key != "$ref":
                _context(document, child, schemas)


def _parameters(document: dict, operation: dict, path_item: dict) -> list:
    merged = {}
    for value in [*path_item.get("parameters", []), *operation.get("parameters", [])]:
        item = deepcopy(_resolve(document, value))
        merged[item["in"], item["name"]] = item
    return [merged[key] for key in sorted(merged)]


def _descriptor(document: dict, path: str, method: str, operation: dict, path_item: dict) -> dict:
    projection = operation[EXTENSION]
    keys = {"schema_version", "dataset", "providers", "provider_policy", "variants",
            "metadata_location", "metadata_schema", "metadata_enforcement",
            "response_schema", "error_schema"}
    if set(projection) != keys or projection["schema_version"] != 1:
        raise ValueError("Invalid projection")
    result = deepcopy(projection)
    if (not result["providers"] or sorted(result["providers"]) != sorted(result["variants"])
            or len(set(result["providers"])) != len(result["providers"])):
        raise ValueError("Invalid projected providers")
    result["command"] = {"path": path, "method": method.upper(),
                         "operation_id": operation["operationId"]}
    result["purpose"] = operation.get("description") or operation.get("summary") or result["dataset"]
    result["parameters"] = _parameters(document, operation, path_item)
    contracts = {}
    for provider, variant in result["variants"].items():
        scoped = {"command": result["command"], "parameters": result["parameters"],
                  "responses": operation["responses"],
                  "provider_policy": result["provider_policy"], "variant": variant,
                  "metadata_schema": result["metadata_schema"],
                  "metadata_location": result["metadata_location"],
                  "response_schema": result["response_schema"],
                  "error_schema": result["error_schema"]}
        context = {}
        _context(document, scoped, context)
        contracts[provider] = _hash({"descriptor": scoped, "schemas": context})
    result["contract_sha256"] = contracts
    return result


def _catalog(document: dict, coverage: dict, identity: dict) -> dict:
    index = _coverage(coverage)
    records = {(item["model"], item["provider"]): item for item in index["datasets"]}
    datasets, schemas, installed = [], {}, {}
    for path, path_item in sorted(document.get("paths", {}).items()):
        for method, operation in sorted(path_item.items()):
            if method not in METHODS or not isinstance(operation, dict) or EXTENSION not in operation:
                continue
            descriptor = _descriptor(document, path, method, operation, path_item)
            _context(document, descriptor, schemas)
            descriptor["coverage"] = {}
            for provider in descriptor["providers"]:
                key = (descriptor["dataset"], provider)
                current = {"source_sha256": identity["source_hashes"].get(key[0], {}).get(provider),
                           "contract_sha256": descriptor["contract_sha256"][provider],
                           "image_digest": identity["image_digest"]}
                states = _states(records.get(key, {}), current)
                states["installed"] = {"status": "verified", "proof": {
                    "checked_on": identity["generated_at"][:10],
                    "evidence_path": "#/paths/" + path.replace("~", "~0").replace("/", "~1") + "/" + method,
                    "identity": {"source_revision": identity["source_revision"],
                                 "contract_sha256": current["contract_sha256"],
                                 "image_digest": identity["image_digest"]}}}
                descriptor["coverage"][provider] = states
                installed[key] = states
            datasets.append(descriptor)
    for item in index["datasets"]:
        key = (item["model"], item["provider"])
        current = {"source_sha256": identity["source_hashes"].get(key[0], {}).get(key[1])}
        item["states"] = deepcopy(installed.get(key)) if key in installed else _states(item, current)
    return {"schema_version": 1, "identity": {**identity, "schema_sha256": _hash(document)},
            "datasets": datasets, "components": {"schemas": schemas}, "coverage": index}


def build_financial_catalog(document: dict, coverage: dict, *, source_revision: str,
                            generation_revision: str, generated_at: str,
                            image_digest: str | None = None, source_hashes: dict | None = None) -> dict:
    """Return discovery after catalog validation; never register or execute commands.

    Source hashes identify individual model/provider adapters. Omitted hashes or
    image identity leave dependent historical proofs stale, without promoting
    account access from fixture, gallery or installed-schema evidence.
    """
    try:
        identity = _Identity.model_validate({
            "source_revision": source_revision, "generation_revision": generation_revision,
            "generated_at": generated_at, "image_digest": image_digest,
            "source_hashes": {} if source_hashes is None else source_hashes,
        }).model_dump(mode="json")
        return _catalog(document, coverage, identity)
    except (ValidationError, ValueError, TypeError, KeyError, AttributeError, RecursionError):
        raise ValueError("Invalid financial discovery input") from None
