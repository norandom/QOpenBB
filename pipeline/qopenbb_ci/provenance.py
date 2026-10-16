"""Reject unreviewed metadata before the complete provenance file is uploaded."""

import json
from pathlib import PurePosixPath
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, StringConstraints, ValidationError, field_validator, model_validator

from qopenbb_ci.source_filter import ALLOW
from qopenbb_ci.runtime_inputs import RUNTIME_FILES

Digest = Annotated[str, StringConstraints(pattern=r'^[0-9a-f]{64}$', strict=True)]
Revision = Annotated[str, StringConstraints(pattern=r'^[0-9a-f]{40}$', strict=True)]
Repository = Annotated[str, StringConstraints(
    pattern=r'^https://github\.com/norandom/[a-zA-Z0-9_-]+\.git$', strict=True)]


class StrictBoundary(BaseModel):
    model_config = ConfigDict(extra='forbid', strict=True)


class Source(StrictBoundary):
    repository: Repository
    revision: Revision
    files: dict[str, Digest]

    @field_validator('files')
    @classmethod
    def canonical_paths(cls, files: dict[str, str]) -> dict[str, str]:
        for name in files:
            path = PurePosixPath(name)
            if (not path.parts or str(path) != name or path.is_absolute()
                    or '..' in path.parts or '\\' in name or '\0' in name):
                raise ValueError('invalid source path')
        return files


class Sources(StrictBoundary):
    workspace: Source
    data_api: Source


class Provenance(StrictBoundary):
    schema_version: Literal[1]
    service: Literal['foundation-smoke', 'workspace', 'data-api']
    sources: Sources
    smoke_sha256: Digest
    runtime_inputs: dict[str, Digest] | None = None
    release_version: Annotated[str, StringConstraints(pattern=r'^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$', strict=True)] | None = None

    @model_validator(mode='after')
    def service_metadata(self):
        if ((self.service == 'data-api') != (self.runtime_inputs is not None)
                or (self.service != 'data-api' and 'runtime_inputs' in self.model_fields_set)):
            raise ValueError('runtime inputs require data-api selection')
        if self.runtime_inputs is not None and set(self.runtime_inputs) != RUNTIME_FILES:
            raise ValueError('runtime input allowlist differs')
        if ((self.service == 'workspace') != (self.release_version is not None)
                or (self.service != 'workspace' and 'release_version' in self.model_fields_set)):
            raise ValueError('release identity requires workspace selection')
        return self

    @field_validator('schema_version', mode='before')
    @classmethod
    def integer_version(cls, value: object) -> object:
        if type(value) is not int:
            raise ValueError('schema version must be an integer')
        return value


def unique_fields(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for name, value in pairs:
        if name in result:
            raise ValueError('duplicate provenance field')
        result[name] = value
    return result


def parse_provenance(content: str) -> dict:
    try:
        result = Provenance.model_validate(json.loads(content, object_pairs_hook=unique_fields)).model_dump(exclude_none=True)
    except (ValueError, ValidationError, TypeError):
        raise ValueError('invalid staged provenance') from None
    for key, source in result['sources'].items():
        for essential in ALLOW[key]:
            present = (essential in source['files'] if essential in {'LICENSE', 'NOTICE'} else
                       any(name.startswith(essential + '/') for name in source['files']))
            if not present:
                raise ValueError('staged source lacks essential owned root')
    return result
