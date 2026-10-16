"""Preserve the acquisition lock without upgrading candidates to runtime evidence."""

from datetime import date
from typing import Annotated, Literal

from pydantic import Field, field_validator, model_validator

from .contracts import Contract, Image, Revision, Text, Token


class CandidateSource(Contract):
    tag: Token
    tag_object: Revision
    revision: Revision
    status: Literal[
        "selected, unvalidated; existing acquisition revision retained until validation selects replacement",
        "selected, unvalidated; adaptation checkout based on this release",
    ]
    evidence: Literal["sources/api-release.json"]


class WorkspaceSource(Contract):
    repository: Literal["https://github.com/norandom/openbb-workspace.git"]
    upstream: Literal["https://github.com/OpenBB-finance/workspace.git"]
    revision: Revision
    branch_at_acquisition: Token
    build_variant: Literal["full"]
    local_checkout: Literal["vendor/workspace"]
    adaptations: Text


class DataSource(Contract):
    repository: Literal["https://github.com/norandom/openbb-data-api.git"]
    upstream: Literal["https://github.com/openbq-org/OpenBB.git"]
    revision: Revision
    branch_at_acquisition: Token
    note: Text
    local_checkout: Literal["vendor/data-api"]
    adaptations: Text
    candidate_release: CandidateSource


class AcquisitionImages(Contract):
    status: Text
    identifiers: list[Image]


class DependencyInventory(Contract):
    status: Text
    inventory: Literal["sources/packages.json"]


class NoticeInventory(Contract):
    inventory: Literal["sources/notices.json"]


class SourceLock(Contract):
    schema_version: Annotated[int, Field(strict=True, ge=2, le=2)]
    status: Literal["acquisition candidate only; no validated compatible runtime or image release"]
    workspace: WorkspaceSource
    data_api: DataSource
    checked_on: str
    validated_release: None
    images: AcquisitionImages
    dependency_set: DependencyInventory
    notices: NoticeInventory
    release_constraints: Literal["sources/constraints.json"]

    @field_validator("checked_on")
    @classmethod
    def calendar_date(cls, value: str) -> str:
        if date.fromisoformat(value).isoformat() != value:
            raise ValueError("ISO date required")
        return value

    @model_validator(mode="after")
    def acquisition_only(self) -> "SourceLock":
        if self.images.identifiers:
            raise ValueError("acquisition lock cannot claim validated images")
        return self
