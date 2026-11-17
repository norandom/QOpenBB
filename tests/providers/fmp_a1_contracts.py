"""Dedicated native query variants and retained row declarations; never registered."""
import re
from datetime import datetime
from typing import ClassVar, Literal
from pydantic import ConfigDict, Field, field_validator
from openbb_core.provider.standard_models.financial_annotations import (
    FinancialDataAnnotation, FinancialFieldTemplate, FinancialQueryAnnotation,
    ProceduralBounds, ResponsePolicy,
)
from openbb_core.provider.standard_models.analyst_estimates import AnalystEstimatesData, AnalystEstimatesQueryParams
from openbb_core.provider.standard_models.price_target import PriceTargetData, PriceTargetQueryParams
from openbb_core.provider.standard_models.price_target_consensus import PriceTargetConsensusData, PriceTargetConsensusQueryParams
from openbb_core.provider.standard_models.revenue_business_line import RevenueBusinessLineData, RevenueBusinessLineQueryParams
from openbb_core.provider.standard_models.revenue_geographic import RevenueGeographicData, RevenueGeographicQueryParams

class SingleSymbol:
    @field_validator('symbol', mode='before', check_fields=False)
    @classmethod
    def single_symbol(cls, value):
        if not isinstance(value, str) or re.search(r'[\r\n\x00]', value):
            raise ValueError('A single symbol is required')
        value = value.strip().upper()
        if not re.fullmatch(r'[A-Z0-9^][A-Z0-9.^_/-]{0,49}', value):
            raise ValueError('A single symbol is required')
        return value

class Periodic:
    @field_validator('period', mode='before', check_fields=False)
    @classmethod
    def periodic_alias(cls, value):
        return 'quarter' if value == 'quarterly' else value

def query_annotation(mode, **cap):
    return FinancialQueryAnnotation(provider_policy='explicit',
        procedural_bounds=ProceduralBounds(max_symbols=1),
        response_policy=ResponsePolicy(mode=mode, **cap),
        runtime_properties=['bounds','effective_query','retrieved_at'])

class FMPAnalystEstimatesQueryParams(SingleSymbol, Periodic, AnalystEstimatesQueryParams):
    model_config = ConfigDict(extra='forbid')
    financial_query_annotation: ClassVar = query_annotation('clip', limit_parameter='limit')
    symbol: str = Field(description='One provider listing identity; maximum 50 characters.', max_length=50)
    period: Literal['annual','quarter'] = Field(default='annual', description='Forecast fiscal frequency; quarterly is accepted as an alias.')
    limit: int = Field(default=20, ge=1, le=100, strict=True, description='Maximum returned forecast rows; one upstream request.')
    page: int = Field(default=0, ge=0, le=10, strict=True, description='Explicit provider page; total completeness remains unknown.')

class FMPPriceTargetQueryParams(SingleSymbol, PriceTargetQueryParams):
    model_config = ConfigDict(extra='forbid')
    financial_query_annotation: ClassVar = query_annotation('clip', limit_parameter='limit')
    symbol: str = Field(description='One provider listing identity; maximum 50 characters.', max_length=50)
    limit: int = Field(default=20, ge=1, le=100, strict=True, description='Maximum news events; one upstream request and no public page.')

class FMPPriceTargetConsensusQueryParams(SingleSymbol, PriceTargetConsensusQueryParams):
    model_config = ConfigDict(extra='forbid')
    financial_query_annotation: ClassVar = query_annotation('provider')
    symbol: str = Field(description='One provider listing identity; at most one matching response.', max_length=50)

class FMPRevenueBusinessLineQueryParams(SingleSymbol, Periodic, RevenueBusinessLineQueryParams):
    model_config = ConfigDict(extra='forbid')
    financial_query_annotation: ClassVar = query_annotation('clip', max_rows=1000)
    symbol: str = Field(description='One provider listing identity; maximum 50 characters.', max_length=50)
    period: Literal['annual','quarter'] = Field(default='annual', description='Fiscal frequency; fixed structure=flat, first 1000 flattened rows, possibly splitting a fiscal period.')

class FMPRevenueGeographicQueryParams(SingleSymbol, Periodic, RevenueGeographicQueryParams):
    model_config = ConfigDict(extra='forbid')
    financial_query_annotation: ClassVar = query_annotation('clip', max_rows=1000)
    symbol: str = Field(description='One provider listing identity; maximum 50 characters.', max_length=50)
    period: Literal['annual','quarter'] = Field(default='annual', description='Fiscal frequency; fixed structure=flat, first 1000 flattened rows, possibly splitting a fiscal period.')

# Retained OpenBB FMP 1.6.1 declarations. Source hashes/notices: fixtures/fmp_batch_a/source_manifest.json.

class FMPAnalystEstimatesData(AnalystEstimatesData):
    """FMP Analyst Estimates Data."""
    __alias_dict__ = {'estimated_revenue_low': 'revenueLow', 'estimated_revenue_high': 'revenueHigh', 'estimated_revenue_avg': 'revenueAvg', 'estimated_sga_expense_low': 'sgaExpenseLow', 'estimated_sga_expense_high': 'sgaExpenseHigh', 'estimated_sga_expense_avg': 'sgaExpenseAvg', 'estimated_ebitda_low': 'ebitdaLow', 'estimated_ebitda_high': 'ebitdaHigh', 'estimated_ebitda_avg': 'ebitdaAvg', 'estimated_ebit_low': 'ebitLow', 'estimated_ebit_high': 'ebitHigh', 'estimated_ebit_avg': 'ebitAvg', 'estimated_net_income_low': 'netIncomeLow', 'estimated_net_income_high': 'netIncomeHigh', 'estimated_net_income_avg': 'netIncomeAvg', 'estimated_eps_low': 'epsLow', 'estimated_eps_high': 'epsHigh', 'estimated_eps_avg': 'epsAvg', 'number_analysts_estimated_revenue': 'numAnalystsRevenue', 'number_analysts_eps': 'numAnalystsEps'}

class FMPPriceTargetData(PriceTargetData):
    """FMP Price Target Data."""
    model_config = ConfigDict(extra='ignore')
    __alias_dict__ = {'analyst_firm': 'analystCompany', 'rating_current': 'newGrade', 'rating_previous': 'previousGrade', 'news_title': 'newsTitle', 'news_url': 'newsURL'}
    news_title: str | None = Field(default=None, description='News title of the price target.')
    news_url: str | None = Field(default=None, description='News URL of the price target.')

class FMPPriceTargetConsensusData(PriceTargetConsensusData):
    """FMP Price Target Consensus Data."""

class FMPRevenueBusinessLineData(RevenueBusinessLineData):
    """FMP Revenue By Business Line Data."""

class FMPRevenueGeographicData(RevenueGeographicData):
    """FMP Revenue Geographic Data."""

    @field_validator('period_ending', 'filing_date', mode='before', check_fields=False)
    @classmethod
    def date_validate(cls, v):
        """Return the date as a datetime object."""
        return datetime.strptime(v, '%Y-%m-%d') if v else None

# Preserve the recovered declarations separately: two archived count destinations do
# not exist in the installed standard. Correct only their canonical destinations.
RETAINED_ESTIMATE_ALIASES = dict(FMPAnalystEstimatesData.__alias_dict__)
FMPAnalystEstimatesData.__alias_dict__ = {
    key: value for key, value in RETAINED_ESTIMATE_ALIASES.items()
    if key not in {'number_analysts_estimated_revenue', 'number_analysts_eps'}
} | {'number_analyst_estimated_revenue': 'numAnalystsRevenue',
     'number_analysts_estimated_eps': 'numAnalystsEps'}

CONTRACTS = {
    'analyst_estimates': (FMPAnalystEstimatesQueryParams, FMPAnalystEstimatesData),
    'price_target': (FMPPriceTargetQueryParams, FMPPriceTargetData),
    'price_target_consensus': (FMPPriceTargetConsensusQueryParams, FMPPriceTargetConsensusData),
    'revenue_business_line': (FMPRevenueBusinessLineQueryParams, FMPRevenueBusinessLineData),
    'revenue_geographic': (FMPRevenueGeographicQueryParams, FMPRevenueGeographicData),
}


def field_template(name, dataset):
    """Declare financial meaning while keeping unavailable dates/currency unknown."""
    unit = None
    origin = 'provider_observation'
    kwargs = {}
    if dataset == 'analyst_estimates':
        if name.startswith('estimated_'):
            unit = 'currency/share' if 'eps' in name else 'currency'
            origin = 'estimate'
        elif name.startswith('number_'):
            unit = 'count'
        kwargs['financial_basis'] = {'forecast_period':'date is forecast fiscal period end; publication/vintage and duration unknown'}
        kwargs['period_basis'] = 'forecast fiscal period; annual or quarter request does not establish duration or vintage'
    elif dataset == 'price_target':
        if 'price' in name and name not in {'published_date','published_time'}:
            unit = 'currency/share'
            origin = 'provider_observation' if name == 'price_when_posted' else 'estimate'
            kwargs['currency_field'] = 'currency'
        kwargs['publication_date_field'] = 'published_date'
        kwargs['financial_basis'] = {'market_date':None}
    elif dataset == 'price_target_consensus':
        if name.startswith('target_'):
            unit = 'currency/share'
            origin = 'estimate'
        kwargs['financial_basis'] = {'market_date':None,'forecast_period':None}
    else:
        unit = 'currency' if name == 'revenue' else None
        kwargs['observation_date_field'] = 'period_ending'
        kwargs['publication_date_field'] = 'filing_date'
        kwargs['period_basis'] = 'reported fiscal period; discrete versus year-to-date duration unknown'
    return FinancialFieldTemplate(unit=unit, scale=1 if unit else None,
        value_origin=origin, **kwargs)

for _name, (_, _row) in CONTRACTS.items():
    _row.financial_data_annotation = FinancialDataAnnotation(
        fields={name: field_template(name, _name) for name in _row.model_fields},
        runtime_properties=['fields.availability','retrieved_at','effective_query','bounds'],
    )
