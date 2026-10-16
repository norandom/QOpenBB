"""Compare caller-supplied artifacts with a separately captured expected context."""

from typing import TypeVar

from pydantic import ValidationError

from .contracts import Acceptance, Backup, Contract, ExpectedContext, Identity, Release
from .source_contract import SourceLock


T = TypeVar("T", bound=Contract)
SAFE_FIELDS = set("input expected evidence schema_version release_id run_id revisions qopenbb workspace data_api agent "
                  "images data-api excel digest architecture lock_hashes source tools dependencies "
                  "contract_hashes model provider name identity required_checks capability requirements "
                  "evidence_class record_id status command timestamp exit_code result artifacts path "
                  "sha256 profiles required_configuration state_compatibility format restore_from "
                  "acceptance_refs backup_id captured_at state_format archive services_stopped "
                  "private_configuration_ref restore_compatibility repository upstream revision "
                  "branch_at_acquisition build_variant local_checkout adaptations note candidate_release "
                  "tag tag_object evidence checked_on validated_release identifiers dependency_set "
                  "inventory notices release_constraints".split())
EXCEL_CHECKPOINT = {
    "workspace": {"4.3", "4.7"}, "data_api": {"5.1", "5.6"},
    "anthropic": {"12.1", "12.2", "12.5"},
}
RELEASE_CHECKPOINT = {
    **EXCEL_CHECKPOINT, "workspace": {"4.1", "4.2", "4.3", "4.7"},
    "linux": {"3.3", "9.4"}, "recovery": {"8.2", "8.4"},
}


def safe_path(parts: tuple[str | int, ...]) -> str:
    return ".".join(str(part) if isinstance(part, int) or part in SAFE_FIELDS else "<field>"
                    for part in parts) or "$"


class InvalidContract(Exception):
    def __init__(self, issues: list[dict[str, str]]) -> None:
        self.issues = issues


def parse(model: type[T], payload: object, prefix: str) -> T:
    try:
        return model.model_validate(payload)
    except ValidationError as error:
        issues = [{"path": prefix + "." + safe_path(item["loc"]), "code": item["type"]}
                  for item in error.errors(include_input=False, include_context=False, include_url=False)]
        raise InvalidContract(issues) from None


def issue(path: str, code: str) -> dict[str, str]:
    return {"path": path, "code": code}


def match_identity(actual: Identity, expected: Identity, prefix: str) -> list[dict[str, str]]:
    return compare(actual.model_dump(), expected.model_dump(), (prefix, "identity"))


def compare(actual: object, expected: object, path: tuple[str | int, ...]) -> list[dict[str, str]]:
    if isinstance(actual, dict) and isinstance(expected, dict):
        issues = []
        for key in sorted(actual.keys() | expected.keys()):
            if key not in actual or key not in expected:
                issues.append(issue(safe_path(path + (key,)), "identity_field_mismatch"))
            else:
                issues.extend(compare(actual[key], expected[key], path + (key,)))
        return issues
    return [] if actual == expected else [issue(safe_path(path), "identity_mismatch")]


def evidence_gate(manifest: Release, context: ExpectedContext,
                  records: list[Acceptance]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    ids = [record.record_id for record in records]
    if len(ids) != len(set(ids)):
        issues.append(issue("evidence.record_id", "duplicate_record"))
    if set(ids) != set(manifest.acceptance_refs):
        issues.append(issue("input.acceptance_refs", "evidence_reference_mismatch"))
    for index, record in enumerate(records):
        issues.extend(match_identity(record.identity, context.identity, f"evidence.{index}"))
    for index, check in enumerate(context.required_checks):
        matching = [record for record in records if record.capability == check.capability
                    and record.evidence_class == check.evidence_class
                    and set(check.requirements) <= set(record.requirements)]
        if len(matching) != 1 or matching[0].status != "passed" or matching[0].exit_code != 0:
            issues.append(issue(f"expected.required_checks.{index}", "required_evidence_unverified"))
    return issues


def checkpoint_gate(context: ExpectedContext, required: dict[str, set[str]]) -> list[dict[str, str]]:
    issues = []
    for capability, criteria in required.items():
        checks = [check for check in context.required_checks if check.capability == capability
                  and check.evidence_class in ("live", "manual")]
        covered = set().union(*(set(check.requirements) for check in checks))
        if not criteria <= covered:
            issues.append(issue("expected.required_checks", "actual_checkpoint_required"))
    if not {"workspace", "data-api", "agent"} <= context.identity.images.keys():
        issues.append(issue("expected.identity.images", "agent_checkpoint_images_required"))
    if context.identity.model is None:
        issues.append(issue("expected.identity.model", "actual_anthropic_model_required"))
    return issues


def evaluate(scope: str, payload: object, expected: object | None,
             evidence: list[object]) -> dict[str, object]:
    model = {"source": SourceLock, "manifest": Release, "backup": Backup,
             "acceptance": Acceptance, "excel": Release, "release": Release}[scope]
    summaries: list[dict[str, str]] = []
    try:
        artifact = parse(model, payload, "input")
        if isinstance(artifact, Acceptance):
            summaries.append(record_summary(artifact, "input"))
        issues: list[dict[str, str]] = []
        if isinstance(artifact, SourceLock):
            return report(scope, issues, False)
        context = parse(ExpectedContext, expected, "expected")
        issues.extend(match_identity(artifact.identity, context.identity, "input"))
        if scope in ("excel", "release") and isinstance(artifact, Release):
            records = [parse(Acceptance, record, f"evidence.{index}")
                       for index, record in enumerate(evidence)]
            summaries = [record_summary(record, f"evidence.{index}")
                         for index, record in enumerate(records)]
            issues.extend(evidence_gate(artifact, context, records))
            required = dict(EXCEL_CHECKPOINT if scope == "excel" else RELEASE_CHECKPOINT)
            if scope == "release" and "excel" in artifact.profiles:
                required["excel"] = {"6.1", "6.2", "6.3", "6.4"}
            issues.extend(checkpoint_gate(context, required))
            if scope == "release" and artifact.status != "release":
                issues.append(issue("input.status", "promoted_release_required"))
        return report(scope, issues, scope in ("excel", "release") and not issues, summaries)
    except InvalidContract as error:
        return report(scope, error.issues, False, summaries)


def record_summary(record: Acceptance, path: str) -> dict[str, str]:
    return {"path": path, "status": record.status, "evidence_class": record.evidence_class}


def report(scope: str, issues: list[dict[str, str]], accepted: bool,
           checks: list[dict[str, str]] | None = None) -> dict[str, object]:
    return {"schema_version": 1, "scope": scope, "valid": not issues,
            "runtime_accepted": accepted, "issues": issues, "checks": checks or []}
