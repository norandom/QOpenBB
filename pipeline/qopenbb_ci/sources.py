"""Acquire and verify the owned Git snapshot without trusting caller identity."""

from pathlib import Path
import re
import subprocess


def git(root: Path, *args: str) -> str:
    return subprocess.check_output(['git', '-C', str(root), *args], text=True,
                                   stderr=subprocess.DEVNULL).strip()


def identity(root: Path, entry: dict) -> dict:
    repository, revision = entry['repository'], entry['revision']
    if not re.fullmatch(r'https://github.com/norandom/[a-zA-Z0-9_-]+\.git', repository):
        raise ValueError('source must be an owned HTTPS Git repository')
    if not re.fullmatch(r'[0-9a-f]{40}', revision):
        raise ValueError('source must have an exact commit')
    if root.is_symlink() or git(root, 'rev-parse', '--show-toplevel') != str(root.resolve()):
        raise ValueError('source root must be the checkout root')
    if git(root, 'remote', 'get-url', 'origin') != repository:
        raise ValueError('source origin differs from lock')
    if git(root, 'rev-parse', 'HEAD') != revision:
        raise ValueError('source HEAD differs from lock')
    if git(root, 'status', '--porcelain', '--untracked-files=no'):
        raise ValueError('tracked source differs from locked commit')
    return {'repository': repository, 'revision': revision}


def acquire(destination: Path, entry: dict) -> dict:
    if destination.exists():
        raise ValueError('acquisition requires a fresh destination')
    repository, revision = entry['repository'], entry['revision']
    if not re.fullmatch(r'https://github.com/norandom/[a-zA-Z0-9_-]+\.git', repository):
        raise ValueError('source must be an owned HTTPS Git repository')
    if not re.fullmatch(r'[0-9a-f]{40}', revision):
        raise ValueError('source must have an exact commit')
    destination.mkdir(parents=True)
    git(destination, 'init', '--quiet')
    git(destination, 'remote', 'add', 'origin', repository)
    git(destination, 'fetch', '--quiet', '--depth=1', 'origin', revision)
    git(destination, 'checkout', '--quiet', '--detach', 'FETCH_HEAD')
    return identity(destination, entry)
