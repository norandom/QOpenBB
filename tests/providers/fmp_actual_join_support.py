"""Offline transport and public SDK emission around the installed native runtime."""
import inspect
import datetime
import json
from collections import OrderedDict
from datetime import date
from pathlib import Path
from typing import Annotated, Any, Literal, Optional, Union

from fastapi import Query as FastAPIQuery
from openbb_core.app.model.field import OpenBBField
from openbb_core.app.static.container import Container
from openbb_core.app.static.package_builder.method_definition import MethodDefinition
from openbb_core.app.static.utils.decorators import exception_handler, validate
from openbb_core.app.static.utils.filters import filter_inputs

ROOT = Path(__file__).resolve().parents[2]
EXPECTED = {
    'AnalystEstimates': ('analyst_estimates', 'estimates/historical'),
    'PriceTarget': ('price_target', 'estimates/price_target'),
    'PriceTargetConsensus': ('price_target_consensus', 'estimates/consensus'),
    'RevenueBusinessLine': ('revenue_business_line', 'fundamental/revenue_per_segment'),
    'RevenueGeographic': ('revenue_geographic', 'fundamental/revenue_per_geography'),
    'HistoricalMarketCap': ('historical_market_cap', 'historical_market_cap'),
    'ShareStatistics': ('share_statistics', 'ownership/share_statistics'),
    'EquityQuote': ('equity_quote', 'price/quote'),
    'IncomeStatementGrowth': ('income_statement_growth', 'fundamental/income_growth'),
    'BalanceSheetGrowth': ('balance_sheet_growth', 'fundamental/balance_growth'),
    'CashFlowStatementGrowth': ('cash_flow_growth', 'fundamental/cash_growth'),
}
# Batch B (task 4.1) registers these eight further FMP fetchers; the registry stays an exact set,
# so any other addition still fails. Their own join is test_fmp_batch_b_installed_join.py.
LATER_BATCHES = {
    'HistoricalDividends', 'HistoricalSplits', 'CalendarEarnings', 'CalendarDividend',
    'CalendarSplits', 'CompanyNews', 'EarningsCallTranscript', 'CompanyFilings',
}
BASELINE = {
    'EquityInfo': 'profile', 'IncomeStatement': 'fundamental/income',
    'BalanceSheet': 'fundamental/balance', 'CashFlowStatement': 'fundamental/cash',
    'EquitySearch': 'search', 'EquityPeers': 'compare/peers',
    'EquityHistorical': 'price/historical', 'KeyMetrics': 'fundamental/metrics',
    'FinancialRatios': 'fundamental/ratios', 'EnterpriseValues': 'fundamental/enterprise_values',
}


def public_method(runner, path):
    command = runner.command_map.get_command(path)
    params = MethodDefinition.format_params(path, dict(inspect.signature(command).parameters), command)
    source = 'class Public(Container):\n'
    source += MethodDefinition.build_command_method_signature('execute', params, Any, path)
    source += MethodDefinition.build_command_method_body(path, command, params)
    namespace = dict(globals())
    exec(source, namespace)
    return namespace['Public'](runner).execute


class Response:
    def __init__(self, payload, status=200):
        self.payload, self.status, self.headers = payload, status, {'Retry-After': '17'}

    async def json(self):
        return self.payload


async def get(app, path, query=b''):
    messages = []
    async def receive():
        return {'type': 'http.request', 'body': b'', 'more_body': False}
    async def send(message):
        messages.append(message)
    await app({'type': 'http', 'asgi': {'version': '3.0', 'spec_version': '2.4'},
               'http_version': '1.1', 'method': 'GET', 'scheme': 'http',
               'path': path, 'raw_path': path.encode(), 'root_path': '',
               'query_string': query, 'headers': [], 'client': ('127.0.0.1', 1234),
               'server': ('test', 80)}, receive, send)
    status = next(m['status'] for m in messages if m['type'] == 'http.response.start')
    return status, json.loads(b''.join(m.get('body', b'') for m in messages))


def result_fields(document, schema, rows=False):
    if '$ref' in schema:
        schema = document['components']['schemas'][schema['$ref'].split('/')[-1]]
    if 'results' in schema.get('properties', {}):
        yield from result_fields(document, schema['properties']['results'], True)
    elif rows and schema.get('type') == 'array':
        yield from result_fields(document, schema['items'], True)
    elif rows and 'properties' in schema:
        yield set(schema['properties'])
    for kind in ('allOf', 'anyOf', 'oneOf'):
        for branch in schema.get(kind, []):
            yield from result_fields(document, branch, rows)
