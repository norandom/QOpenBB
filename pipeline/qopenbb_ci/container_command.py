"""Resolved executable and argument-array contract shared by container consumers."""
from pathlib import Path
import os
import shutil
from collections.abc import Mapping, Sequence


def resolve_executable(value: str) -> Path:
    candidate = Path(value) if Path(value).is_absolute() else Path(shutil.which(value) or value)
    if not candidate.is_file():
        raise ValueError(f'Required executable not found: {value}')
    candidate = candidate.resolve(strict=True)
    if candidate.suffix.lower() in {'.cmd', '.bat', '.ps1', '.sh'}:
        raise ValueError(f'A real executable is required, not a shell wrapper: {candidate}')
    if os.name == 'nt' and candidate.suffix.lower() != '.exe':
        raise ValueError(f'A Windows .exe is required: {candidate}')
    return candidate


def container_command(arguments: Sequence[str], environment: Mapping[str, str] | None = None) -> list[str]:
    env = os.environ if environment is None else environment
    selected = env.get('QOPENBB_CONTAINER_CLI')
    if not selected and os.name == 'nt':
        raise ValueError('Set QOPENBB_CONTAINER_CLI to the real podman.exe path')
    executable = resolve_executable(selected or 'docker')
    return [str(executable), *arguments]


def compose_command(arguments: Sequence[str], environment: Mapping[str, str] | None = None) -> list[str]:
    env = os.environ if environment is None else environment
    if os.name == 'nt':
        provider = env.get('PODMAN_COMPOSE_PROVIDER')
        if not provider:
            raise ValueError('Set PODMAN_COMPOSE_PROVIDER to the real docker-compose.exe path')
        resolve_executable(provider)
    return container_command(['compose', *arguments], env)
