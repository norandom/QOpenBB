"""Bind bounded FMP events and documents without changing their financial envelope."""
from copy import deepcopy

from qopenbb_ci.catalog_financial import EXTENSION, resolve


def binding(route: str, renderer: str, company: bool, rows: int,
            dates: str | None, days: int | None, description: str) -> dict:
    return {'route': route, 'renderer': renderer, 'company': company,
            'maxReturnedRows': rows, 'dateMode': dates, 'maxInclusiveDays': days,
            'description': description}


# Limits mirror the accepted adapter validators; tests exercise emitted boundaries.
BINDINGS = {
    'fmp_historical_dividends': binding('equity/fundamental/dividends', 'table', True, 100,
        'optional_independent', None, 'Dividends for one listing. Upstream limit applies before local inclusive ex-date filtering; history completeness is unknown.'),
    'fmp_historical_splits': binding('equity/fundamental/historical_splits', 'table', True, 100,
        None, None, 'Historical splits for one listing; at most 100 rows in source order. History completeness is unknown.'),
    'fmp_calendar_earnings': binding('equity/calendar/earnings', 'table', False, 250,
        'required_pair', 7, 'Market-wide earnings calendar; both dates required, at most 7 days inclusive and 250 rows.'),
    'fmp_calendar_dividend': binding('equity/calendar/dividend', 'table', False, 250,
        'required_pair', 7, 'Market-wide dividend calendar; both dates required, at most 7 days inclusive and 250 rows.'),
    'fmp_calendar_splits': binding('equity/calendar/splits', 'table', False, 250,
        'required_pair', 7, 'Market-wide split calendar; both dates required, at most 7 days inclusive and 250 rows.'),
    'fmp_company_news': binding('news/company', 'company_documents', True, 50,
        'optional_pair', 31, 'Stock news excerpts for one listing. Omit both dates or supply a pair spanning at most 31 days inclusive; page 0-99, limit 1-50. Completeness is unknown.'),
    'fmp_earnings_call_transcript': binding('equity/fundamental/transcript', 'company_documents', True, 1,
        None, None, 'One transcript for the exact listing, year 1900-2100 and quarter 1-4. Empty means unavailable; completeness is unknown.'),
    'fmp_company_filings': binding('equity/fundamental/filings', 'company_documents', True, 100,
        'required_pair', 365, 'Filing metadata for one listing. Both dates required, at most 365 days inclusive; page 0-99, limit 1-100. Linked documents are not retrieved.'),
}

def validate_bindings(inventory: dict) -> None:
    """A partial Batch B catalog cannot silently omit an accepted dataset."""
    paths = {'/api/v1/' + value['route']: key for key, value in BINDINGS.items()}
    selected = [d for d in inventory['datasets'] if d['id'] in BINDINGS or d['path'] in paths]
    if not selected:
        return
    if {d['id'] for d in selected} != set(BINDINGS) or len(selected) != len(BINDINGS):
        raise ValueError('Missing or extra Batch B mapping')
    for dataset in selected:
        if dataset['provider'] != 'fmp' or paths.get(dataset['path']) != dataset['id']:
            raise ValueError('Invalid Batch B provider or route')


def controls(widget: dict, query: dict, defaults: dict, policy: dict) -> list:
    params = widget.get('params', [])
    native = {p['paramName']: p for p in params}
    if len(native) != len(params):
        raise ValueError('Duplicate native Batch B query control')
    properties = query['properties']
    if properties.keys() - native.keys():
        raise ValueError('Missing native Batch B query control')
    result = [{'paramName': 'provider', 'value': 'fmp', 'show': False,
               'options': [{'label': 'FMP', 'value': 'fmp'}]}]
    # JSON object key order changes on canonical round trips; UI control order does not.
    for name, source in native.items():
        if name not in properties:
            continue
        schema = properties[name]
        param = deepcopy(source)
        label = name.replace('_', ' ').capitalize()
        param.update(label=label, description=control_description(name, schema, policy))
        param.update(optional=name not in query.get('required', []),
                     validationSchema=deepcopy(schema), multiSelect=False, multiple=False)
        if name in defaults:
            param['value'] = defaults[name]
        elif 'default' in schema:
            param['value'] = schema['default']
        else:
            param['value'] = None
        result.append(param)
    return result


def project(widget: dict, dataset: dict, schema: dict) -> None:
    if dataset['id'] not in BINDINGS:
        return
    selected = BINDINGS[dataset['id']]
    route, renderer, company = (selected[key] for key in ('route', 'renderer', 'company'))
    expected = route.replace('/', '_') + '_fmp_obb'
    if widget['widgetId'] != expected:
        raise ValueError('Unexpected Batch B widget ID')
    descriptor = schema['paths'][dataset['path']]['get'][EXTENSION]
    if set(descriptor['variants']) != {'fmp'}:
        raise ValueError('Foreign Batch B financial variant')
    variant = descriptor['variants']['fmp']
    query = resolve(schema, variant['query_schema'])
    policy = query_policy(selected, query)
    widget['params'] = controls(widget, query, dataset['parameters'], policy)
    widget['queryPolicy'] = policy
    widget['description'] = selected['description']
    widget['type'] = renderer
    widget['financialContract'] = deepcopy(descriptor)
    widget['data']['scope'] = 'listing' if company else 'market'
    # Refreshes of licensed data must follow an explicit query or user action.
    widget.update(refetchInterval=False, refetchOnWindowFocus=False, refetchOnReconnect=False)



def query_policy(selected: dict, query: dict) -> dict:
    dates = None if selected['dateMode'] is None else {
        'startParameter': 'start_date', 'endParameter': 'end_date',
        'mode': selected['dateMode'], 'inclusive': True, 'ordered': True,
        'maxInclusiveDays': selected['maxInclusiveDays'],
        'application': 'local_ex_date_filter_after_upstream_limit'
        if selected['dateMode'] == 'optional_independent' else 'upstream_window',
    }
    return {'schemaVersion': 1, 'maxRequests': 1,
            'maxReturnedRows': selected['maxReturnedRows'],
            'returnedRowsLimitParameter': 'limit' if 'limit' in query['properties'] else None,
            'maxSymbols': 1 if selected['company'] else 0,
            'rejectExplicitNull': True, 'dateWindow': dates,
            'parameters': deepcopy(query['properties']),
            'required': list(query.get('required', [])),
            'completeness': 'unknown', 'preserveSourceOrder': True}


def control_description(name: str, schema: dict, policy: dict) -> str:
    if name == 'symbol':
        return 'Exactly one listing symbol; comma-separated lists and whitespace are rejected.'
    if name in ('start_date', 'end_date'):
        window = policy['dateWindow']
        modes = {'required_pair': 'Both dates required.',
                 'optional_pair': 'Omit both dates or supply both.',
                 'optional_independent': 'Each date optional; local ex-date filter applies after upstream limit.'}
        cap = window['maxInclusiveDays']
        return modes[window['mode']] + (' At most ' + str(cap) + ' days inclusive.' if cap else '') + ' Start must not follow end.'
    if 'minimum' in schema and 'maximum' in schema:
        default = ' Default ' + str(schema['default']) + '.' if 'default' in schema else ''
        return name.replace('_', ' ').capitalize() + ': integer ' + str(schema['minimum']) + '-' + str(schema['maximum']) + '.' + default
    return schema.get('description') or name.replace('_', ' ').capitalize() + '.'
