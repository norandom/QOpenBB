"""Freeze deployment inputs without running Compose or inspecting operator files."""

from ipaddress import ip_address
import json
import re
from urllib.parse import urlsplit

from .contracts import Image
from .catalog import freeze_routes


SERVICE_INPUTS = {
    'workspace': ('WORKSPACE_IMAGE', 3000, ['PUBLIC_URL']),
    'data-api': ('DATA_API_IMAGE', 6900, ['FMP_API_KEY', 'FRED_API_KEY', 'OPENBB_API_AUTH']),
    'agent': ('AGENT_IMAGE', 7777, ['ANTHROPIC_API_KEY', 'ANTHROPIC_MODEL']),
    'excel': ('EXCEL_IMAGE', 80, []),
}
DATASETS = [
    {'id': 'company-profile', 'provider': 'fmp', 'path': '/api/v1/equity/profile',
     'parameters': {'provider': 'fmp', 'symbol': 'AAPL'}},
    {'id': 'annual-income', 'provider': 'fmp', 'path': '/api/v1/equity/fundamental/income',
     'parameters': {'provider': 'fmp', 'symbol': 'AAPL', 'period': 'annual', 'limit': 1}},
    {'id': 'gdp', 'provider': 'fred', 'path': '/api/v1/economy/fred_series',
     'parameters': {'provider': 'fred', 'symbol': 'GDP'}},
]


def service_contract(name: str) -> dict:
    image, port, environment = SERVICE_INPUTS[name]
    result = {'image': image, 'port': port, 'publish': [], 'binds': [],
              'environment': environment, 'depends_on': []}
    if name == 'workspace':
        result.update(publish=['0.0.0.0:23003:3000'], binds=['./data/workspace:/data'],
                      depends_on=['data-api'])
    if name == 'excel':
        result['profile'] = 'excel'
    return result


def runtime_contract() -> dict:
    routes = [{'prefix': prefix, 'target': target, 'strip_prefix': strip, 'stream': stream}
              for prefix, target, strip, stream in (
                  ('/api', 'workspace', False, False), ('/data', 'data-api', True, False),
                  ('/agent', 'agent', True, True), ('/excel', 'excel', True, False))]
    return {'schema_version': 1, 'services': {name: service_contract(name) for name in SERVICE_INPUTS},
            'routes': routes}


def validate_contracts(*, runtime: dict, datasets: dict, routes: dict,
                       openapi: dict | None = None) -> None:
    """Installed contracts require the caller's explicit served-schema identity."""
    if not exact_contract(runtime, runtime_contract()):
        raise ValueError('runtime contract differs from approved topology')
    status = datasets.get('status')
    if status not in {'provisional', 'installed'} or routes.get('status') != status:
        raise ValueError('dataset and route contract status mismatch')
    if not exact_contract(datasets, {'schema_version': 1, 'status': status, 'datasets': DATASETS}):
        raise ValueError('dataset contract differs from approved inventory')
    if status == 'installed':
        if openapi is None:
            raise ValueError('installed routes require an explicit served OpenAPI schema')
        try:
            expected = freeze_routes(openapi, datasets)
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError('invalid installed route schema') from exc
    else:
        expected = {'schema_version': 1, 'status': 'provisional', 'routes': [
            {'dataset': d['id'], 'method': 'GET', 'path': d['path']} for d in DATASETS]}
    if not exact_contract(routes, expected):
        raise ValueError('route contract differs from explicit schema or provisional inventory')


def public_origin(value: str) -> tuple[str, str]:
    """Only configured origin determines advertised URLs and forwarded protocol."""
    try:
        parsed = urlsplit(value)
        host, port = parsed.hostname, parsed.port
        if not host or parsed.scheme not in {'http', 'https'} or parsed.username is not None:
            raise ValueError
        if parsed.password is not None or parsed.path not in {'', '/'} or '?' in value or '#' in value:
            raise ValueError
        if re.search(r'[\s\\%]', value) or host in SERVICE_INPUTS or host.endswith('.internal'):
            raise ValueError
        try:
            address = ip_address(host)
        except ValueError:
            address = None
        if address is not None:
            local = address.is_loopback
            if not local and not address.is_global:
                raise ValueError
        else:
            local = host == 'localhost'
            labels = host.split('.')
            if not local and (len(labels) < 2 or any(not re.fullmatch(
                    r'[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?', label) for label in labels)):
                raise ValueError
        if parsed.scheme == 'http' and not local:
            raise ValueError
        if port is not None and port < 1:
            raise ValueError
    except (ValueError, TypeError):
        raise ValueError('PUBLIC_URL must be an absolute local HTTP or public HTTPS origin') from None
    return value.rstrip('/'), parsed.scheme


def required(values: dict[str, str], name: str) -> str:
    value = values.get(name, '')
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f'missing configuration: {name}')
    return value


def image_reference(value: str, name: str, production: bool) -> None:
    if any(word in value.lower() for word in ('placeholder', 'parser-only', 'inactive', '.invalid')):
        raise ValueError(f'real image required: {name}')
    if production:
        try:
            Image(digest=value, architecture='linux/amd64')
        except ValueError:
            raise ValueError(f'immutable image required: {name}') from None
    elif not development_image(value):
        raise ValueError(f'invalid image: {name}')


def validate_configuration(values: dict[str, str], *, selected: set[str],
                           production: bool = False) -> dict:
    """Selected services alone require images and credentials; inactive ones are absent."""
    if not {'workspace', 'data-api'} <= selected or not selected <= SERVICE_INPUTS.keys():
        raise ValueError('select workspace and data-api plus supported optional services')
    origin, scheme = public_origin(required(values, 'PUBLIC_URL'))
    if values.get('OPENBB_API_AUTH', 'false') != 'false':
        raise ValueError('OPENBB_API_AUTH must be false')
    services = {name: configured_service(name, values, origin, production)
                for name in SERVICE_INPUTS if name in selected}
    urls = {'FRONTENDURL': origin, 'PROURL': origin, 'SELFURL': origin + '/api',
            'DATA_URL': origin + '/data'}
    for name in ('agent', 'excel'):
        if name in selected:
            urls[name.upper() + '_URL'] = origin + '/' + name
    return {'services': services, 'urls': urls, 'forwarded_scheme': scheme,
            'routes': [route for route in runtime_contract()['routes'] if route['target'] in selected]}


def configured_service(name: str, values: dict[str, str], origin: str, production: bool) -> dict:
    spec = service_contract(name)
    variable = spec['image']
    spec['image'] = required(values, variable)
    image_reference(spec['image'], variable, production)
    environment = {}
    for key in spec['environment']:
        if key == 'PUBLIC_URL':
            environment[key] = origin
        elif key == 'OPENBB_API_AUTH':
            environment[key] = 'false'
        else:
            environment[key] = required(values, key)
    spec['environment'] = environment
    return spec


def development_image(value: str) -> bool:
    reference = value
    if '@' not in value:
        repository, separator, tag = value.rpartition(':')
        if not separator or not re.fullmatch(r'[A-Za-z0-9_][A-Za-z0-9_.-]{0,127}', tag):
            return False
        reference = repository + '@sha256:' + '0' * 64
    try:
        Image(digest=reference, architecture='linux/amd64')
        return True
    except ValueError:
        return False


def exact_contract(actual: dict, expected: dict) -> bool:
    try:
        return json.dumps(actual, sort_keys=True, allow_nan=False) == json.dumps(expected, sort_keys=True)
    except (TypeError, ValueError):
        return False
