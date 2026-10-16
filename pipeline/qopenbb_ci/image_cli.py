"""Portable acquisition, staging, Dagger export and archive loading commands."""

import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile
import tarfile

from qopenbb_ci.images import inspect_archive, load
from qopenbb_ci.sources import acquire
from qopenbb_ci.staging import stage, verify_stage


def read(path: Path) -> dict:
    return json.loads(path.read_text())


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    commands = result.add_subparsers(dest='command', required=True)
    acquisition = commands.add_parser('acquire')
    acquisition.add_argument('--lock', type=Path, required=True)
    acquisition.add_argument('--destination', type=Path, required=True)
    staging = commands.add_parser('stage')
    staging.add_argument('--lock', type=Path, required=True)
    staging.add_argument('--policy', type=Path, required=True)
    staging.add_argument('--workspace', type=Path, required=True)
    staging.add_argument('--data-api', type=Path, required=True)
    staging.add_argument('--destination', type=Path, required=True)
    staging.add_argument('--service', choices=['foundation-smoke', 'workspace'], default='foundation-smoke')
    staging.add_argument('--release-version')
    exporting = commands.add_parser('export')
    exporting.add_argument('--stage', type=Path, required=True)
    exporting.add_argument('--tools', type=Path, required=True)
    exporting.add_argument('--lock', type=Path, required=True)
    exporting.add_argument('--policy', type=Path, required=True)
    exporting.add_argument('--sdk-python', type=Path, required=True)
    exporting.add_argument('--service', choices=['foundation-smoke', 'workspace'], default='foundation-smoke')
    for command in [exporting, commands.add_parser('load'), commands.add_parser('inspect')]:
        command.add_argument('--archive', type=Path, required=True)
        command.add_argument('--report', type=Path, required=True)
    return result


def export(args: argparse.Namespace) -> dict:
    provenance = verify_stage(args.stage, read(args.policy), read(args.lock))
    if provenance.get('service', args.service) != args.service:
        raise ValueError('service differs from staged provenance')
    tools = read(args.tools)
    environment = {key: os.environ[key] for key in ['PATH', 'XDG_RUNTIME_DIR', 'DOCKER_HOST']
                   if key in os.environ}
    environment['_EXPERIMENTAL_DAGGER_RUNNER_HOST'] = 'docker-image://' + tools['base_images']['dagger_engine']
    environment['PYTHONPATH'] = str(Path(__file__).resolve().parents[2] / '.dagger/src')
    sdk = subprocess.check_output([str(args.sdk_python.absolute()), '-c',
                                   'import importlib.metadata;print(importlib.metadata.version("dagger-io"))'],
                                  text=True, env=environment).strip()
    if sdk != tools['tools']['dagger_python_sdk']['version']:
        raise ValueError('Dagger SDK version differs from tools lock')
    with tempfile.TemporaryDirectory(prefix='qopenbb-build-home-') as home:
        environment['HOME'] = home
        environment['DOCKER_CONFIG'] = home
        version = subprocess.check_output(['dagger', 'version'], text=True, env=environment)
        if 'dagger v' + tools['tools']['dagger_cli']['version'] + ' ' not in version:
            raise ValueError('Dagger CLI version differs from tools lock')
        subprocess.run(['dagger', 'run', '--', str(args.sdk_python.absolute()), '-m', 'qopenbb.export',
                        '--service', args.service, '--stage', str(args.stage.resolve()),
                        '--base', tools['base_images']['python'], '--archive', str(args.archive.resolve())],
                       env=environment, check=True)
    engine = verify_engine(tools['base_images']['dagger_engine'])
    return {**inspect_archive(args.archive), 'service': args.service, 'sources': provenance['sources'],
            'engine': tools['base_images']['dagger_engine'], 'engine_observed': engine,
            'sdk_version': sdk, 'base': tools['base_images']['python']}


def verify_engine(reference: str) -> dict:
    digest = reference.rsplit('@sha256:', 1)[1]
    name = 'dagger-engine-' + digest[:16]
    observed = json.loads(subprocess.check_output(['docker', 'container', 'inspect', name], text=True))[0]
    if observed['Config']['Image'] != reference or observed['Image'] != 'sha256:' + digest:
        raise ValueError('running Dagger engine differs from locked digest')
    return {'container_id': observed['Id'], 'image_id': observed['Image'],
            'configured_reference': observed['Config']['Image']}


def write_report(path: Path, result: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2) + '\n')


def main() -> int:
    args = parser().parse_args()
    try:
        if args.command == 'acquire':
            lock = read(args.lock)
            result = {key: acquire(args.destination / key, lock[key]) for key in ['workspace', 'data_api']}
        elif args.command == 'stage':
            result = stage(args.destination, {'workspace': args.workspace, 'data_api': args.data_api},
                           read(args.policy), read(args.lock), args.service, args.release_version)
        elif args.command == 'export':
            result = export(args)
        else:
            result = inspect_archive(args.archive)
            if args.command == 'load':
                result = load(args.archive, result)
        if hasattr(args, 'report'):
            write_report(args.report, result)
        else:
            print(json.dumps(result))
        return 0
    except (OSError, ValueError, KeyError, TypeError, IndexError, tarfile.TarError,
            subprocess.SubprocessError) as error:
        result = {'valid': False, 'error': type(error).__name__}
        if hasattr(args, 'report'):
            try:
                write_report(args.report, result)
            except OSError:
                result = {'valid': False, 'error': 'unwritable_report'}
        print(json.dumps(result))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
