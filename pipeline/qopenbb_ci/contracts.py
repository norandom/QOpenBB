"""Strict artifact boundaries; validation does not attest that a procedure ran."""

from datetime import datetime, timezone
from ipaddress import IPv6Address
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, field_validator, model_validator


Token = Annotated[str, StringConstraints(pattern=r"^[a-zA-Z0-9][a-zA-Z0-9._-]{0,127}$")]
Revision = Annotated[str, StringConstraints(pattern=r"^[0-9a-f]{40}$")]
Hash = Annotated[str, StringConstraints(pattern=r"^sha256:[0-9a-f]{64}$")]
Requirement = Annotated[str, StringConstraints(pattern=r"^[1-9][0-9]*\.[1-9][0-9]*$")]
Version = Annotated[int, Field(strict=True, ge=1, le=1)]
Service = Literal["workspace", "data-api", "agent", "excel"]
EvidenceClass = Literal["fixture", "live", "manual"]
Text = Annotated[str, StringConstraints(min_length=1, max_length=4096)]

# Component separators follow distribution/reference's registry and repository grammar.
_DOMAIN_COMPONENT = r"[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?"
_REGISTRY_HOST = rf"(?:{_DOMAIN_COMPONENT}(?:\.{_DOMAIN_COMPONENT})*|\[[a-fA-F0-9:]+\])"
_REPOSITORY_COMPONENT = r"[a-z0-9]+(?:(?:[._]|__|-+)[a-z0-9]+)*"
_IMAGE_DIGEST = (rf"^{_REGISTRY_HOST}(?::[0-9]+)?/{_REPOSITORY_COMPONENT}"
                 rf"(?:/{_REPOSITORY_COMPONENT})*@sha256:[0-9a-f]{{64}}$")


class Contract(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)


class Image(Contract):
    digest: Annotated[str, StringConstraints(pattern=_IMAGE_DIGEST)]
    architecture: Literal["linux/amd64", "linux/arm64"]

    @field_validator("digest")
    @classmethod
    def valid_repository(cls, value: str) -> str:
        name = value.split("@", 1)[0]
        if len(name) > 255:
            raise ValueError("repository name exceeds image-reference limit")
        registry = name.split("/", 1)[0]
        if registry.startswith("["):
            IPv6Address(registry[1:registry.index("]")])
        return value


class Revisions(Contract):
    qopenbb: Revision
    workspace: Revision
    data_api: Revision
    agent: Revision | None = None


class LockHashes(Contract):
    source: Hash
    tools: Hash
    dependencies: Hash


class Model(Contract):
    provider: Literal["anthropic"]
    name: Token


class Identity(Contract):
    release_id: Token
    run_id: Token
    revisions: Revisions
    images: Annotated[dict[Service, Image], Field(min_length=1)]
    lock_hashes: LockHashes
    contract_hashes: Annotated[dict[Token, Hash], Field(min_length=1)]
    model: Model | None = None

    @model_validator(mode="after")
    def agent_revision(self) -> "Identity":
        if "agent" in self.images and self.revisions.agent is None:
            raise ValueError("agent source revision required")
        return self


class Artifact(Contract):
    path: Annotated[str, StringConstraints(pattern=r"^artifacts/[a-zA-Z0-9._/-]+$")]
    sha256: Hash

    @field_validator("path")
    @classmethod
    def sanitized_path(cls, value: str) -> str:
        if any(part in ("", ".", "..") or part.startswith(".env")
               or part in ("secrets", "credentials") for part in value.split("/")):
            raise ValueError("sanitized artifact path required")
        return value


class Archive(Artifact):
    path: Annotated[str, StringConstraints(pattern=r"^(artifacts|backups)/[a-zA-Z0-9._/-]+$")]


def utc_timestamp(value: str) -> str:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None or parsed.utcoffset() != timezone.utc.utcoffset(parsed):
        raise ValueError("UTC timestamp required")
    return value


class CheckRequirement(Contract):
    capability: Token
    requirements: Annotated[list[Requirement], Field(min_length=1)]
    evidence_class: EvidenceClass


class ExpectedContext(Contract):
    schema_version: Version
    identity: Identity
    required_checks: list[CheckRequirement]

    @model_validator(mode="after")
    def unique_checks(self) -> "ExpectedContext":
        keys = [(check.capability, check.evidence_class) for check in self.required_checks]
        if len(keys) != len(set(keys)):
            raise ValueError("duplicate check requirement")
        return self


class Acceptance(CheckRequirement):
    schema_version: Version
    record_id: Token
    status: Literal["passed", "failed", "skipped", "unverified"]
    identity: Identity
    command: Text
    timestamp: str
    exit_code: Annotated[int, Field(strict=True, ge=0, le=255)] | None
    result: Text
    artifacts: Annotated[list[Artifact], Field(min_length=1)]

    _timestamp = field_validator("timestamp")(utc_timestamp)

    @model_validator(mode="after")
    def passing_exit(self) -> "Acceptance":
        if self.status == "passed" and self.exit_code != 0:
            raise ValueError("passed evidence requires successful exit")
        return self


class StateCompatibility(Contract):
    format: Token
    restore_from: Annotated[list[Token], Field(min_length=1)]


class Release(Contract):
    schema_version: Version
    status: Literal["candidate", "release"]
    identity: Identity
    profiles: list[Literal["excel"]]
    required_configuration: list[Annotated[str, StringConstraints(pattern=r"^[A-Z][A-Z0-9_]*$")]]
    state_compatibility: StateCompatibility
    acceptance_refs: list[Token]

    @model_validator(mode="after")
    def selected_images(self) -> "Release":
        images = set(self.identity.images)
        if not {"workspace", "data-api"} <= images:
            raise ValueError("selected checkpoint requires workspace and data-api images")
        if ("excel" in self.profiles) != ("excel" in images):
            raise ValueError("Excel profile and image selection must agree")
        for values in (self.profiles, self.required_configuration, self.acceptance_refs):
            if len(values) != len(set(values)):
                raise ValueError("duplicate selection")
        return self


class Backup(Contract):
    schema_version: Version
    backup_id: Token
    identity: Identity
    captured_at: str
    state_format: Token
    archive: Archive
    services_stopped: bool
    private_configuration_ref: Annotated[str, StringConstraints(pattern=r"^private:[a-zA-Z0-9._-]+$")]
    restore_compatibility: Annotated[list[Token], Field(min_length=1)]

    _captured_at = field_validator("captured_at")(utc_timestamp)

    @model_validator(mode="after")
    def consistent_snapshot(self) -> "Backup":
        if not self.services_stopped:
            raise ValueError("stopped services required")
        if self.state_format not in self.restore_compatibility:
            raise ValueError("source format must be restorable")
        return self
