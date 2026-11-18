"""Executable synthetic contract freeze; no Fetcher or transport is loaded."""
import ast
import hashlib
import json
import re
import sys
import types
from datetime import date, datetime
from pathlib import Path
from typing import Any, Literal
from urllib.parse import urlsplit

import pydantic
from pydantic import BaseModel, ConfigDict, Field, create_model, model_validator, field_validator

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
BASE = ROOT.parent
CORE = BASE / 'data-api/openbb_platform/core/openbb_core'
RECOVERED = BASE / 'evidence/foundation/recovered'
NAMES = {'company_news': 'CompanyNews', 'company_filings': 'CompanyFilings',
         'earnings_call_transcript': 'EarningsCallTranscript'}


def load_models():
    for suffix in ['', '.provider', '.provider.abstract', '.provider.utils', '.provider.standard_models']:
        key = 'openbb_core' + suffix
        module = types.ModuleType(key)
        module.__path__ = [str(CORE.joinpath(*suffix.strip('.').split('.')))] if suffix else [str(CORE)]
        sys.modules[key] = module
    models = {}
    for name, stem in NAMES.items():
        tree = ast.parse((RECOVERED / f'{name}.py').read_text())
        tree.body = [n for n in tree.body if not (
            isinstance(n, ast.ImportFrom) and n.module.startswith('openbb_core')
            and not ('standard_models' in n.module or 'descriptions' in n.module)
        ) and not (isinstance(n, ast.ClassDef) and n.name.endswith('Fetcher'))]
        ns = {'__name__': f'fixture_{name}'}
        exec(compile(tree, str(RECOVERED / f'{name}.py'), 'exec'), ns)
        models[name] = (ns[f'FMP{stem}QueryParams'], ns[f'FMP{stem}Data'])
    return models


def civil_date(v):
    if isinstance(v, date) and not isinstance(v, datetime):
        return v
    if isinstance(v, str) and re.fullmatch(r'[0-9]{4}-[0-9]{2}-[0-9]{2}', v):
        return date.fromisoformat(v)
    raise ValueError('A native date or ISO YYYY-MM-DD string is required')


class Query(BaseModel):
    model_config = ConfigDict(extra='forbid')
    symbol: str = Field(min_length=1, max_length=50)

    @model_validator(mode='before')
    @classmethod
    def explicit_null(cls, v):
        if any(x is None for x in v.values()):
            raise ValueError('Explicit null is not omission')
        return v

    @field_validator('start_date', 'end_date', mode='before', check_fields=False)
    @classmethod
    def civil_bound(cls, v):
        return civil_date(v)

    @field_validator('symbol')
    @classmethod
    def listing(cls, v):
        if ',' in v or any(c.isspace() for c in v):
            raise ValueError('Exactly one listing required')
        return v.upper()

    @model_validator(mode='after')
    def window(self):
        start, end = getattr(self, 'start_date', None), getattr(self, 'end_date', None)
        if bool(start) != bool(end):
            raise ValueError('Dates must be paired')
        max_days = 365 if self.__class__.__name__ == 'FrozenCompanyFilingsQuery' else 31
        if start and (end < start or (end-start).days >= max_days):
            raise ValueError('Invalid inclusive window')
        return self


def queries():
    news = create_model('FrozenCompanyNewsQuery', __base__=Query,
        start_date=(date | None, None), end_date=(date | None, None),
        page=(int, Field(0, strict=True, ge=0, le=99)),
        limit=(int, Field(10, strict=True, ge=1, le=50)))
    filings = create_model('FrozenCompanyFilingsQuery', __base__=Query,
        start_date=(date, ...), end_date=(date, ...),
        page=(int, Field(0, strict=True, ge=0, le=99)),
        limit=(int, Field(20, strict=True, ge=1, le=100)))
    transcript = create_model('FrozenEarningsCallTranscriptQuery', __base__=Query,
        year=(int, Field(..., strict=True, ge=1900, le=2100)),
        quarter=(int, Field(..., strict=True, ge=1, le=4)))
    return dict(zip(NAMES, [news, filings, transcript]))


def safe_link(v):
    if v is None or v == '':
        return None
    if not isinstance(v, str) or any(c.isspace() or ord(c) < 32 or 127 <= ord(c) <= 159 for c in v) or '\\' in v:
        raise ValueError('Unsafe link')
    parts = urlsplit(v)
    if parts.scheme.lower() not in ('http', 'https') or not parts.hostname or parts.username or parts.password:
        raise ValueError('Unsafe link')
    try:
        parts.port
    except ValueError as exc:
        raise ValueError('Unsafe port') from exc
    return v


def precise_date(v):
    if v is None or isinstance(v, (datetime, date)):
        return v
    if isinstance(v, str) and len(v) == 10:
        return date.fromisoformat(v)
    return datetime.fromisoformat(v.replace('Z', '+00:00'))


class Row(BaseModel):
    model_config = ConfigDict(extra='forbid')
    symbol: str
    content_status: Literal['partial', 'metadata_only', 'completeness_unknown', 'full']

    @field_validator('date', 'accepted_date', mode='before', check_fields=False)
    @classmethod
    def timestamp_precision(cls, v):
        return precise_date(v)


class News(Row):
    date: datetime
    title: str
    source: str | None = None
    publisher: str | None = None
    author: str | None = None
    excerpt: str | None = None
    body: str | None = None
    url: str
    symbols: str | None = None
    images: Any | None = None


class Filing(Row):
    @field_validator('filing_date', mode='before')
    @classmethod
    def civil_filing_date(cls, v):
        return civil_date(v)

    filing_date: date
    accepted_date: datetime | date | None = None
    report_type: str | None = None
    cik: str | None = None
    filing_url: str | None = None
    report_url: str


class Transcript(Row):
    year: int = Field(strict=True, ge=1900, le=2100)
    quarter: str = Field(pattern=r'^Q[1-4]$')
    date: date
    event_datetime: datetime | None = None
    content: str


ROWS = dict(zip(NAMES, [News, Filing, Transcript]))
ALIASES = {
 'company_news': {'symbol':'symbol', 'date':'publishedDate', 'title':'title', 'source':'site',
                  'publisher':'publisher', 'excerpt':'text', 'url':'url', 'symbols':'symbol', 'images':'image'},
 'company_filings': {'symbol':'symbol', 'filing_date':'filingDate', 'accepted_date':'acceptedDate',
                     'report_type':'formType', 'cik':'cik', 'filing_url':'link', 'report_url':'finalLink'},
 'earnings_call_transcript': {'symbol':'symbol', 'year':'year', 'quarter':'period', 'date':'date', 'content':'content'}}
ENDPOINTS = dict(zip(NAMES, ['news/stock', 'sec-filings-search/symbol', 'earning-call-transcript']))


def normalized(name, rows, query):
    q = queries()[name].model_validate(query)
    if not isinstance(rows, list):
        raise ValueError('Expected acquisition list')
    if not rows:
        raise ValueError('Empty acquisition: unavailable, not a fabricated document')
    if name == 'earnings_call_transcript' and len(rows) != 1:
        raise ValueError('Duplicate transcript coordinates')
    out = []
    for raw in rows:
        identity = raw.get('symbol')
        if not isinstance(identity, str) or identity.upper() != q.symbol:
            raise ValueError('Foreign or absent company linkage')
        mapped = {key: raw[source] for key, source in ALIASES[name].items() if source in raw}
        mapped['symbol'] = q.symbol
        if name == 'company_news':
            text = raw.get('text')
            if text is not None and not isinstance(text, str):
                raise ValueError('Nontext excerpt')
            if not isinstance(raw.get('title'), str) or not raw['title'].strip():
                raise ValueError('Missing headline')
            mapped['content_status'] = 'partial' if text and text.strip() else 'metadata_only'
            mapped['author'], mapped['body'] = None, None
            mapped['symbols'] = q.symbol
        elif name == 'company_filings':
            if 'cik' in raw and raw['cik'] is not None and not isinstance(raw['cik'], str):
                raise ValueError('CIK must retain lexical identity')
            if raw.get('acceptedDate') == '':
                mapped['accepted_date'] = None
            mapped['content_status'] = 'metadata_only'
        else:
            # Stable examples identify quarter as Q1..Q4 in period. Never infer it
            # from the event date: the event may follow the financial period.
            period = raw.get('period')
            quarter = int(period[1]) if isinstance(period, str) and period in ('Q1','Q2','Q3','Q4') else None
            if type(raw.get('year')) is not int or quarter is None:
                raise ValueError('Strict coordinates required')
            if 'quarter' in raw and (type(raw['quarter']) is not int or raw['quarter'] != quarter):
                raise ValueError('Conflicting coordinates')
            mapped['quarter'] = f'Q{quarter}'
            supplied_date = precise_date(raw.get('date'))
            mapped['event_datetime'] = supplied_date if isinstance(supplied_date, datetime) else None
            mapped['date'] = supplied_date.date() if isinstance(supplied_date, datetime) else supplied_date
            if (raw['year'], quarter) != (q.year, q.quarter):
                raise ValueError('Mismatched period')
            if not isinstance(raw.get('content'), str) or not raw['content'].strip():
                raise ValueError('Blank transcript')
            mapped['content_status'] = 'completeness_unknown'
        for key in ['url', 'filing_url', 'report_url']:
            if key in mapped:
                mapped[key] = safe_link(mapped[key])
        out.append(ROWS[name].model_validate(mapped).model_dump(mode='json'))
    return out[:getattr(q, 'limit', 1)]


def sample(name, timestamp='2026-01-02T16:35:42'):
    common = {'symbol':'AAPL'}
    if name == 'company_news':
        return dict(common, publishedDate=timestamp, title='Synthetic result', site='Example Wire',
                    publisher='Example Publisher', text='  Literal <b>excerpt</b>\n', url='https://example.test/news/1')
    if name == 'company_filings':
        return dict(common, filingDate='2026-01-02', acceptedDate=timestamp, formType='10-Q',
                    cik='0000320193', link='https://example.test/filing-index.html',
                    finalLink='https://example.test/report.htm')
    return dict(common, year=2026, period='Q1', date=timestamp, content='  Operator: Hello\n\nCEO: <b>Literal</b>\t\n')


def query(name):
    if name == 'earnings_call_transcript':
        return {'symbol':'aapl', 'year':2026, 'quarter':1}
    if name == 'company_filings':
        return {'symbol':'aapl', 'start_date':'2026-01-01', 'end_date':'2026-01-31'}
    return {'symbol':'aapl'}


def capture(model, raw):
    try:
        return {'serialized': model.model_validate(raw).model_dump(mode='json')}
    except ValueError as exc:
        return {'errors': [{'type':e['type'], 'loc':list(e['loc'])} for e in exc.errors()]}


def build(models):
    contracts = {}
    for name, (oldq, oldrow) in models.items():
        source = RECOVERED / f'{name}.py'
        contracts[name] = {
            'scope':'synthetic offline freeze; runtime corrections remain in tasks 3.6-3.8 and 4.2',
            'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
            'standard_sha256': hashlib.sha256((CORE / f'provider/standard_models/{name}.py').read_bytes()).hexdigest(),
            'stable_endpoint':ENDPOINTS[name], 'maximum_calls':1,
            'retained': {'aliases':oldrow.__alias_dict__,
                         'query_validation':oldq.model_json_schema(mode='validation'),
                         'row_validation':oldrow.model_json_schema(mode='validation'),
                         'row_serialization':oldrow.model_json_schema(mode='serialization')},
            'expected': {'source_aliases':ALIASES[name],
                         'query_validation':queries()[name].model_json_schema(mode='validation'),
                         'query_serialization':queries()[name].model_json_schema(mode='serialization'),
                         'row_validation':ROWS[name].model_json_schema(mode='validation'),
                         'row_serialization':ROWS[name].model_json_schema(mode='serialization')},
            'wire_parameters': ({'symbols':'symbol','from':'start_date','to':'end_date','page':'page','limit':'limit'}
                                if name == 'company_news' else
                                {'symbol':'symbol','from':'start_date','to':'end_date','page':'page','limit':'limit'}
                                if name == 'company_filings' else
                                {'symbol':'symbol','year':'year','quarter':'quarter'}),
            'compatibility_changes': {
                'company_news':['preserve all standard fields including symbols and images',
                                'add symbol, publisher, content_status; author is never inferred from publisher',
                                'source nullable for unknown attribution; url remains required'],
                'company_filings':['accepted_date preserves date/datetime precision instead of inherited date truncation',
                                   'add content_status; report_url remains required'],
                'earnings_call_transcript':['retain standard quarter string and civil date',
                                            'add event_datetime for supplied precise time and content_status']
            }[name],
            'source_attribution': {'provider':'fmp', 'field_origins':ALIASES[name],
                                   'publisher_is_author':False, 'timezone_when_unsupplied':'unknown'},
            'content_status_rules': {'partial':'nonblank supplied excerpt; never full article',
                                     'metadata_only':'filing metadata or headline without nonblank excerpt',
                                     'completeness_unknown':'nonblank transcript without explicit full-content evidence',
                                     'full':'requires explicit source evidence; none in these three contracts'},
            'time_rules': {'filing_date':'civil date', 'timestamp':'preserve supplied clock and offset',
                           'naive_timestamp':'retain naive; timezone unknown',
                           'date_only':'retain civil date; do not synthesize midnight'},
            'procedural': {'validate_all_before_limit':True, 'preserve_source_order':True,
                           'completeness':'unknown', 'strict_single_symbol':True,
                           'empty_acquisition':'unavailable', 'no_images_or_link_fetch':True}}
    examples = []
    for name in NAMES:
        timestamps = ['2026-01-02T00:00:00-05:00', '2026-01-02T16:35:42',
                      '2026-01-02T16:35:42-05:00', '2026-01-02T21:35:42Z']
        if name != 'company_news':
            timestamps.insert(0, '2026-01-02')
        for timestamp in timestamps:
            raw = sample(name, timestamp)
            baseline = dict(raw)
            if name == 'earnings_call_transcript':
                baseline['period'] = 'Q1'
            examples.append({'model':name, 'raw':raw, 'query':query(name),
                             'observed_baseline':capture(models[name][1], baseline),
                             'expected':normalized(name, [raw], query(name))})
    return contracts, examples


def verify(contracts, examples, models):
    checks = 0
    def rejected(fn):
        nonlocal checks
        try:
            fn()
        except (ValueError, TypeError):
            checks += 1
        else:
            raise AssertionError('Invalid case accepted')
    for name in NAMES:
        q = query(name)
        assert set(models[name][1].model_fields) <= set(ROWS[name].model_fields)
        for field in ['url'] if name == 'company_news' else ['report_url'] if name == 'company_filings' else ['quarter','date']:
            assert ROWS[name].model_fields[field].is_required()
        checks += 2
        model = queries()[name]
        assert model(**q).symbol == 'AAPL'
        checks += 1
        for patch in [{'symbol':'AAPL,MSFT'}, {'symbol':''}, {'symbol':'A A'}, {'symbol':None},
                      {'unexpected':1}, {'symbol':['AAPL']}]:
            rejected(lambda patch=patch: model.model_validate(q | patch))
        if name == 'earnings_call_transcript':
            for key, values in {'year':[1899,2101,True,None,'2026'], 'quarter':[0,5,True,None,'1',1.5]}.items():
                for value in values:
                    rejected(lambda key=key,value=value: model.model_validate(q | {key:value}))
            for quarter in range(1,5):
                assert model(**(q | {'quarter':quarter})).quarter == quarter
                checks += 1
            for key in ['year','quarter']:
                rejected(lambda key=key: model.model_validate({k:v for k,v in q.items() if k != key}))
        else:
            cap = 50 if name == 'company_news' else 100
            for key, values in {'page':[-1,100,True,None,'0'], 'limit':[0,cap+1,True,None,'1']}.items():
                for value in values:
                    rejected(lambda key=key,value=value: model.model_validate(q | {key:value}))
            start = date(2026,1,1)
            from datetime import timedelta
            days = 31 if name == 'company_news' else 365
            window = q | {'start_date':str(start), 'end_date':str(start+timedelta(days=days-1))}
            assert model(**window)
            assert model(**(window | {'start_date':start})).start_date == start
            checks += 2
            for field in ['start_date','end_date']:
                for value in [0,1767225600,True,False,1767225600.0,'1767225600',
                              '20260101','2026-W01-4',datetime(2026,1,1),
                              '2026-01-01T00:00:00Z']:
                    rejected(lambda field=field,value=value: model.model_validate(window | {field:value}))
            for patch in [{'end_date':str(start+timedelta(days=days))}, {'end_date':'2025-12-31'},
                          {'start_date':None}, {'start_date':'2026-02-30'},
                          {'start_date':'2026-01-01T00:00:00'}]:
                rejected(lambda patch=patch: model.model_validate(window | patch))
            rejected(lambda: model.model_validate({'symbol':'AAPL', 'start_date':'2026-01-01'}))
        row = sample(name)
        date_key = 'filingDate' if name == 'company_filings' else 'publishedDate' if name == 'company_news' else 'date'
        rejected(lambda: normalized(name,[row | {date_key:'2026-02-30'}],q))
        rejected(lambda: normalized(name,[{k:v for k,v in row.items() if k != date_key}],q))
        if name != 'earnings_call_transcript':
            link_key = 'url' if name == 'company_news' else 'finalLink'
            rejected(lambda: normalized(name,[row | {link_key:'javascript:alert(1)'}],q))
            for value in ['https://example.test/\x7fpath','https://example.test/\x80path',
                          'https://example.test/\x1fpath']:
                rejected(lambda value=value: normalized(name,[row | {link_key:value}],q))
            rejected(lambda: normalized(name,[row | {link_key:None}],q))
            rejected(lambda: normalized(name,[row | {link_key:''}],q))
            rejected(lambda: normalized(name,[{k:v for k,v in row.items() if k != link_key}],q))
        for rows in [[], {}, [row | {'symbol':'MSFT'}], [row | {'symbol':None}]]:
            rejected(lambda rows=rows: normalized(name, rows, q))
        if name == 'earnings_call_transcript':
            for rows in [[row,row], [row | {'period':'Q2'}], [row | {'year':2025}],
                         [row | {'quarter':True}], [row | {'quarter':'1'}], [row | {'period':'Q5'}], [row | {'period':1}],
                         [{k:v for k,v in row.items() if k != 'period'}]]:
                rejected(lambda rows=rows: normalized(name, rows, q))
            for content in [None,'',' \n\t',42]:
                rejected(lambda content=content: normalized(name,[row | {'content':content}],q))
            rejected(lambda: normalized(name,[{k:v for k,v in row.items() if k != 'content'}],q))
        elif name == 'company_news':
            for text in [None,'',' \t\n']:
                got = normalized(name,[row | {'text':text}],q)[0]
                assert got['content_status'] == 'metadata_only' and got['excerpt'] == text
                checks += 1
            got = normalized(name,[row],q)[0]
            assert got['author'] is None and got['publisher'] != got['source']
            assert got['excerpt'] == row['text'] and got['content_status'] == 'partial'
            assert len(normalized(name,[row,row],q)) == 2
            checks += 3
            rejected(lambda: normalized(name,[row | {'text':42}],q))
            rejected(lambda: normalized(name,[row | {'title':'  '}],q))
        else:
            got = normalized(name,[row],q)[0]
            assert got['cik'] == '0000320193' and got['filing_url'] != got['report_url']
            assert got['content_status'] == 'metadata_only'
            checks += 2
            rejected(lambda: normalized(name,[row | {'cik':320193}],q))
            for value in [0,1767225600,True,False,1767225600.0,'1767225600',
                          '20260102','2026-W01-5',datetime(2026,1,2),
                          '2026-01-02T00:00:00']:
                rejected(lambda value=value: normalized(name,[row | {'filingDate':value}],q))
            assert normalized(name,[row | {'filingDate':date(2026,1,2)}],q)[0]['filing_date'] == '2026-01-02'
            checks += 1
            for value in ['https://example.test/a\x7f','https://example.test/a\x80','https://example.test/a\x1f']:
                rejected(lambda value=value: normalized(name,[row | {'link':value}],q))
            assert normalized(name,[row | {'acceptedDate':''}],q)[0]['accepted_date'] is None
            assert normalized(name,[row | {'acceptedDate':None}],q)[0]['accepted_date'] is None
            assert len(normalized(name,[row,row],q)) == 2
            checks += 3
        # Unknown source fields cannot claim completeness or become executable content.
        got = normalized(name,[row | {'content_status':'full','isComplete':True}],q)[0]
        assert got['content_status'] != 'full'
        checks += 1
        for link in ['javascript:alert(1)','data:text/plain,x','file:///x','//example.test/a',
                     'https://u:p@example.test/a','https://example.test/a\n','https:///a', 'https://example.test:bad/a',
                     'https://example.test/a\x7f','https://example.test/a\x80','https://example.test/a\x1f']:
            rejected(lambda link=link: safe_link(link))
        assert safe_link(None) is None and safe_link('') is None
        assert safe_link('http://example.test/a') == 'http://example.test/a'
        checks += 2
        if name != 'earnings_call_transcript':
            # A bad row after the requested cap must still fail the acquisition.
            rejected(lambda: normalized(name,[row,row | {'symbol':'MSFT'}], q | {'limit':1}))
    for example in examples:
        assert normalized(example['model'], [example['raw']], example['query']) == example['expected']
        observed = example['observed_baseline']
        if example['model'] == 'company_filings':
            assert observed['serialized']['accepted_date'] == '2026-01-02'
        if example['model'] == 'earnings_call_transcript':
            assert example['expected'][0]['quarter'] == 'Q1'
            assert example['expected'][0]['date'] == '2026-01-02'
            if len(example['raw']['date']) == 10:
                assert example['expected'][0]['event_datetime'] is None
            else:
                assert example['expected'][0]['event_datetime'] == example['raw']['date']
            if 'T16:' in example['raw']['date'] or 'T21:' in example['raw']['date']:
                assert observed['errors'][0]['type'] == 'date_from_datetime_inexact'
            else:
                assert observed['serialized']['date'] == '2026-01-02'
        checks += 2
    return checks


if __name__ == '__main__':
    def deny_network(event, args):
        if event in ('socket.connect', 'socket.getaddrinfo'):
            raise RuntimeError('Network is forbidden in this offline freeze')
    sys.addaudithook(deny_network)
    models = load_models()
    contracts, examples = build(models)
    if '--write' in sys.argv:
        for name, contract in contracts.items():
            (HERE / f'{name}.json').write_text(json.dumps(contract,indent=2)+'\n', encoding='utf-8')
        (HERE / 'serialization_examples.json').write_text(json.dumps(examples,indent=2)+'\n', encoding='utf-8')
    else:
        for name, contract in contracts.items():
            assert json.loads((HERE / f'{name}.json').read_text()) == contract, name
        assert json.loads((HERE / 'serialization_examples.json').read_text()) == examples
    print(json.dumps({'checks_passed':verify(contracts,examples,models), 'authenticated_calls':0,
                      'production_verified':False, 'pydantic':pydantic.__version__}))
