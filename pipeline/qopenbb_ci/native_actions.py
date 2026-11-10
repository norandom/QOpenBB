"""Route native actions to accepted consumers without retaining private output."""
from pathlib import Path

from .compose_runtime import start, StartRequest
from .compose_lifecycle import recreate, stop, load, inventory
from .compose_readiness import wait_health
from .container_command import resolve_executable
from .native_environment import checked_path, validate_output, run_command
from .runtime_descriptor import public_projection


def required_inputs(args):
    fields = {'doctor': (), 'start': ('session_path', 'workspace_image', 'data_image'),
              'recreate': ('session_path',), 'stop': ('session_path',),
              'verify': ('session_path',),
              'build': ('build_selection', 'stage', 'archive', 'sdk_python', 'engine_container')}
    missing = [name.replace('_', '-') for name in fields[args.action] if not getattr(args, name)]
    if missing:
        raise ValueError('required inputs: ' + ', '.join('--' + name for name in missing))


def consumer_environment(config):
    return {**config.environment, 'PYTHONPATH': str(config.repository / 'pipeline')}


def build(config, args):
    stage = validate_output(args.stage)
    archive = validate_output(args.archive)
    sdk = resolve_executable(str(args.sdk_python))
    if archive.exists() or archive.with_suffix('.export.json').exists() or archive.with_suffix('.load.json').exists():
        raise ValueError('Build archive and reports must be new')
    archive.parent.mkdir(parents=True, exist_ok=True)
    service = 'foundation-smoke' if args.build_selection == 'foundation' else args.build_selection
    base = [str(config.tools['python']), '-B', '-m', 'qopenbb_ci.image_cli']
    command = [*base, 'export', '--stage', str(stage), '--archive', str(archive),
               '--report', str(archive.with_suffix('.export.json')), '--service', service,
               '--sdk-python', str(sdk), '--dagger-cli', str(config.tools['dagger_cli']),
               '--engine-container', args.engine_container, '--lock', str(config.repository / 'sources.lock.json'),
               '--policy', str(config.repository / 'contracts/sources.json'),
               '--tools', str(config.repository / 'pipeline/tools.lock.json')]
    environment = consumer_environment(config)
    result = run_command(command, config.repository, environment, 3600)
    if result.returncode == 0:
        result = run_command([*base, 'load', '--archive', str(archive), '--report',
                              str(archive.with_suffix('.load.json'))], config.repository, environment, 300)
    return {'action': 'build', 'service': service, 'exit': result.returncode,
            'archive': str(archive)}, result.returncode


def verification_source(config, requested):
    source = checked_path(requested or config.repository)
    # Resolve from the repository, independent of the caller's current directory.
    files = [path.relative_to(config.repository) for path in (config.repository / 'verification').glob('*.ts')]
    files += [Path('verification/package.json'), Path('verification/pnpm-lock.yaml'),
              Path('tests/e2e/infrastructure.spec.mts')]
    for relative in files:
        if (source / relative).read_bytes() != (config.repository / relative).read_bytes():
            raise ValueError('Verification snapshot differs from reviewed source')
    if not (source / 'verification/node_modules/@playwright/test/cli.js').is_file():
        raise ValueError('Locked native verification dependencies required')
    return source


def verify(config, args):
    runtime = load(config, args.session_path)
    containers, networks = inventory(runtime)
    if runtime.descriptor.phase != 'ready' or set(containers) != {'workspace', 'data-api'} or not networks:
        raise ValueError('Verification requires a ready owned image pair')
    if any(item.get('State', {}).get('Running') is not True
           or item.get('State', {}).get('Health', {}).get('Status') != 'healthy'
           for item in containers.values()):
        raise ValueError('Verification requires running and healthy owned services')
    wait_health(runtime)
    source = verification_source(config, args.verification_source)
    environment = {**consumer_environment(config),
        'QOPENBB_VERIFICATION_ROOT': str(config.artifacts / 'verification'),
        'QOPENBB_RUNTIME_PYTHON': str(config.tools['python'])}
    if not environment.get('PLAYWRIGHT_BROWSERS_PATH'):
        raise ValueError('Explicit browser cache required')
    commands = [[str(config.tools['python']), '-B', str(config.repository / 'verification/runner.py'),
                 'tests/delivery/test_verification.py::test_synthetic_provider_observation'],
                [str(config.tools['node']), str(source / 'verification/node_modules/@playwright/test/cli.js'),
                 'test', '--config', str(source / 'verification/playwright.config.ts')]]
    codes = []
    for command in commands:
        result = run_command(command, config.repository, environment, 300)
        codes.append(result.returncode)
        if result.returncode:
            break
    return {'action': 'verify', 'scope': 'synthetic infrastructure only',
            'financial_acceptance': 'unverified', 'exit': codes[-1]}, codes[-1]


def dispatch(config, args):
    if args.action == 'start':
        descriptor = start(StartRequest(config, args.session_path, args.workspace_image, args.data_image))
        return public_projection(descriptor), 0
    if args.action == 'recreate':
        return public_projection(recreate(config, args.session_path)), 0
    if args.action == 'stop':
        return stop(config, args.session_path), 0
    if args.action == 'build':
        return build(config, args)
    return verify(config, args)
