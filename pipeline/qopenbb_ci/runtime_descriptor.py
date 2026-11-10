"""Versioned private runtime contract shared by lifecycle and browser consumers."""
import json
from pathlib import Path, PureWindowsPath
from typing import Annotated, Literal
from urllib.parse import urlsplit

from pydantic import BaseModel, ConfigDict, Field, model_validator

from . import session_files

Digest = Annotated[str, Field(pattern=r'^sha256:[a-f0-9]{64}$')]
HexDigest = Annotated[str, Field(pattern=r'^[a-f0-9]{64}$')]
Nonempty = Annotated[str, Field(min_length=1)]
Service = Literal['workspace', 'data-api']


class DescriptorError(ValueError):
    """A sanitized contract failure that never includes private input."""


class Contract(BaseModel):
    model_config = ConfigDict(extra='forbid', strict=True, frozen=True)


def absolute_path(value):
    if not (Path(value).is_absolute() or PureWindowsPath(value).is_absolute()):
        raise ValueError('absolute path required')
    if '\x00' in value or '..' in value.replace('\\', '/').split('/'):
        raise ValueError('unsafe path')
    return value


class Credentials(Contract):
    email: Nonempty
    password: Nonempty


class ImageIdentity(Contract):
    manifest_digest: Digest | None
    config_digest: Digest


class Connection(Contract):
    endpoint: Nonempty
    identity: Nonempty


class Resource(Contract):
    id: HexDigest
    labels: dict[str, str]


class Resources(Contract):
    containers: dict[Service, Resource]
    networks: list[Resource]


class State(Contract):
    host_path: Nonempty
    daemon_path: Nonempty | None
    mount_identity: Nonempty | None
    verified: bool

    @model_validator(mode='after')
    def check_mapping(self):
        absolute_path(self.host_path)
        if self.verified and not (self.daemon_path and self.mount_identity):
            raise ValueError('verified mapping requires identities')
        return self


class HashedFile(Contract):
    path: Nonempty
    sha256: HexDigest

    @model_validator(mode='after')
    def check_path(self):
        absolute_path(self.path)
        return self


class Compose(Contract):
    project_directory: Nonempty
    files: Annotated[list[HashedFile], Field(min_length=1)]
    environment_file: HashedFile

    @model_validator(mode='after')
    def check_directory(self):
        absolute_path(self.project_directory)
        return self


class RuntimeDescriptor(Contract):
    schema_version: Literal[1]
    session_id: Annotated[str, Field(pattern=r'^[a-f0-9]{32}$')]
    backend: Literal['compose']
    phase: Literal['prepared', 'starting', 'ready', 'recreating', 'failed', 'stopped']
    name: Nonempty
    origin: str | None
    container: HexDigest | None
    credentials: Credentials | None
    images: dict[Service, Digest]
    image_metadata: dict[Service, ImageIdentity]
    packaged_image_only: Literal[True]
    source_overlay: None
    release_image_verified: Literal[False]
    project: Nonempty
    connection: Connection
    resources: Resources
    state: State
    compose: Compose

    @model_validator(mode='before')
    @classmethod
    def reject_coerced_literals(cls, value):
        if not isinstance(value, dict) or type(value.get('schema_version')) is not int:
            raise ValueError('version must be integer')
        for name in ['packaged_image_only', 'release_image_verified']:
            if type(value.get(name)) is not bool:
                raise ValueError('acceptance flags must be boolean')
        return value

    @model_validator(mode='after')
    def check_identity(self):
        if self.name != 'qopenbb-browser-' + self.session_id or self.project != self.name:
            raise ValueError('session identity mismatch')
        services = {'workspace', 'data-api'}
        if set(self.images) != services or set(self.image_metadata) != services:
            raise ValueError('exact image pair required')
        for service in services:
            if self.images[service] != self.image_metadata[service].config_digest:
                raise ValueError('image identity mismatch')
        self.check_origin()
        self.check_resources()
        if self.phase == 'ready':
            self.check_ready()
        return self

    def check_origin(self):
        if self.origin is None:
            return
        parsed = urlsplit(self.origin)
        if (parsed.scheme != 'http' or parsed.hostname != '127.0.0.1'
                or parsed.username is not None or parsed.password is not None
                or parsed.path or parsed.query or parsed.fragment or not parsed.port
                or self.origin != f'http://127.0.0.1:{parsed.port}'):
            raise ValueError('loopback origin required')

    def check_resources(self):
        expected = {'com.docker.compose.project': self.project,
                    'org.qopenbb.session': self.session_id}
        for service, resource in self.resources.containers.items():
            self.check_labels(resource, {**expected, 'com.docker.compose.service': service})
        for resource in self.resources.networks:
            self.check_labels(resource, expected)
        workspace = self.resources.containers.get('workspace')
        if self.container is not None and (workspace is None or workspace.id != self.container):
            raise ValueError('workspace container mismatch')

    @staticmethod
    def check_labels(resource, expected):
        if any(resource.labels.get(key) != value for key, value in expected.items()):
            raise ValueError('resource ownership mismatch')

    def check_ready(self):
        if not (self.origin and self.container and self.credentials and self.state.verified
                and set(self.resources.containers) == {'workspace', 'data-api'}
                and self.resources.networks):
            raise ValueError('ready facts incomplete')


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise DescriptorError('Invalid runtime descriptor')
        result[key] = value
    return result


def parse_descriptor(payload: bytes) -> RuntimeDescriptor:
    try:
        raw = json.loads(payload, object_pairs_hook=_unique_object)
        return RuntimeDescriptor.model_validate(raw)
    except (ValueError, TypeError, RecursionError):
        raise DescriptorError('Invalid runtime descriptor') from None


def read_private(path: Path) -> RuntimeDescriptor:
    return parse_descriptor(session_files.read_private(path))


def replace_private(path: Path, descriptor: RuntimeDescriptor) -> None:
    if not isinstance(descriptor, RuntimeDescriptor):
        raise DescriptorError('Invalid runtime descriptor')
    payload = descriptor.model_dump_json().encode('utf-8')
    parse_descriptor(payload)
    session_files.replace_private(path, payload)


def public_projection(descriptor: RuntimeDescriptor) -> dict:
    descriptor = parse_descriptor(descriptor.model_dump_json().encode('utf-8'))
    return {key: getattr(descriptor, key) for key in
            ['schema_version', 'session_id', 'backend', 'phase', 'name', 'origin',
             'images', 'packaged_image_only', 'source_overlay', 'release_image_verified']}
