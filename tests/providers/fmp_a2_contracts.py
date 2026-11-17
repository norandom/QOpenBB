"""Unregistered A2 native characterization models; retained FMP 1.6.1 declarations.

Archive/member/license hashes and MIT notice: fixtures/fmp_batch_a/source_manifest.json.
Corrections preserve public field unions while fixing zero and UTC information loss.
"""
import re
from datetime import date as dateType, datetime, timedelta, timezone
from typing import ClassVar, Literal
from pydantic import ConfigDict, Field, field_validator, model_validator
from openbb_core.provider.utils.descriptions import DATA_DESCRIPTIONS
from openbb_core.provider.standard_models.financial_annotations import (
    FinancialDataAnnotation, FinancialFieldTemplate, FinancialQueryAnnotation, ProceduralBounds, ResponsePolicy,
)
from openbb_core.provider.standard_models.historical_market_cap import HistoricalMarketCapData, HistoricalMarketCapQueryParams
from openbb_core.provider.standard_models.share_statistics import ShareStatisticsData, ShareStatisticsQueryParams
from openbb_core.provider.standard_models.equity_quote import EquityQuoteData, EquityQuoteQueryParams
from openbb_core.provider.standard_models.income_statement_growth import IncomeStatementGrowthData, IncomeStatementGrowthQueryParams
from openbb_core.provider.standard_models.balance_sheet_growth import BalanceSheetGrowthData, BalanceSheetGrowthQueryParams
from openbb_core.provider.standard_models.cash_flow_growth import CashFlowStatementGrowthData, CashFlowStatementGrowthQueryParams

class SingleSymbol:
    @model_validator(mode='before')
    @classmethod
    def normalize_symbol(cls, values):
        if not isinstance(values, dict):
            return values
        values = dict(values)
        value = values.get('symbol')
        if not isinstance(value, str) or re.search(r'[\x00-\x1f\x7f]',value):
            raise ValueError('One symbol is required')
        value = value.strip().upper()
        if not re.fullmatch(r'[A-Z0-9^][A-Z0-9.^_/-]{0,49}',value):
            raise ValueError('One symbol is required')
        values['symbol']=value
        return values

class Periodic:
    @field_validator('period',mode='before',check_fields=False)
    @classmethod
    def period_alias(cls,value):
        return 'quarter' if value=='quarterly' else value

def query_annotation(mode, **cap):
    return FinancialQueryAnnotation(provider_policy='explicit',procedural_bounds=ProceduralBounds(max_symbols=1),response_policy=ResponsePolicy(mode=mode,**cap),runtime_properties=['bounds','effective_query','retrieved_at'])

class FmpHistoricalMarketCapQueryParams(SingleSymbol,HistoricalMarketCapQueryParams):
    model_config = ConfigDict(extra='forbid')
    financial_query_annotation: ClassVar = query_annotation('clip',max_rows=5000)
    symbol: str = Field(max_length=50,description='One provider listing identity; maximum 50 characters.')
    start_date: dateType | None = Field(default=None,description='ISO calendar date; omitted start resolves at acquisition to effective end minus 365 days. Ordered range at most 366 days.')
    end_date: dateType | None = Field(default=None,description='ISO calendar date; omitted end resolves at acquisition to UTC today. Ordered range at most 366 days; fixed upstream limit 5000.')

    @field_validator('start_date','end_date',mode='before')
    @classmethod
    def iso_calendar(cls,value):
        if value is None or type(value) is dateType:
            return value
        if not isinstance(value,str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}',value):
            raise ValueError('ISO calendar date required')
        return dateType.fromisoformat(value)

    @model_validator(mode='after')
    def ordered_window(self):
        if self.start_date is not None and self.end_date is not None:
            validate_cap_window(self.start_date,self.end_date)
        return self

def validate_cap_window(start,end):
    if not 0 <= (end-start).days <= 366:
        raise ValueError('Ordered date window at most 366 days required')

def resolve_cap_dates(query,today=None):
    """Resolve defaults only at acquisition; callers may inject the observed UTC day."""
    end=query.end_date or today or datetime.now(timezone.utc).date()
    start=query.start_date or end-timedelta(days=365)
    validate_cap_window(start,end)
    return start,end

class FMPShareStatisticsQueryParams(SingleSymbol,ShareStatisticsQueryParams):
    model_config = ConfigDict(extra='forbid')
    financial_query_annotation: ClassVar = query_annotation('provider')
    symbol: str = Field(max_length=50,description='One provider listing identity; maximum 50 characters.')

class FMPEquityQuoteQueryParams(SingleSymbol,EquityQuoteQueryParams):
    model_config = ConfigDict(extra='forbid')
    financial_query_annotation: ClassVar = query_annotation('provider')
    symbol: str = Field(max_length=50,description='One provider listing identity; maximum 50 characters.')

class FMPIncomeStatementGrowthQueryParams(SingleSymbol,Periodic,IncomeStatementGrowthQueryParams):
    model_config = ConfigDict(extra='forbid')
    financial_query_annotation: ClassVar = query_annotation('clip',limit_parameter='limit')
    symbol: str = Field(max_length=50,description='One provider listing identity; maximum 50 characters.')
    period: Literal['annual','quarter'] = Field(default='annual',description='Fiscal frequency; quarterly aliases quarter. Duration/denominator and restatement conventions unknown.')
    limit: int = Field(default=20,ge=1,le=100,strict=True,description='Maximum returned rows; one request; replaces archived implicit 5.')

class FMPBalanceSheetGrowthQueryParams(SingleSymbol,Periodic,BalanceSheetGrowthQueryParams):
    model_config = ConfigDict(extra='forbid')
    financial_query_annotation: ClassVar = query_annotation('clip',limit_parameter='limit')
    symbol: str = Field(max_length=50,description='One provider listing identity; maximum 50 characters.')
    period: Literal['annual','quarter'] = Field(default='annual',description='Fiscal frequency; quarterly aliases quarter. Duration/denominator and restatement conventions unknown.')
    limit: int = Field(default=20,ge=1,le=100,strict=True,description='Maximum returned rows; one request; replaces archived implicit 5.')

class FMPCashFlowStatementGrowthQueryParams(SingleSymbol,Periodic,CashFlowStatementGrowthQueryParams):
    model_config = ConfigDict(extra='forbid')
    financial_query_annotation: ClassVar = query_annotation('clip',limit_parameter='limit')
    symbol: str = Field(max_length=50,description='One provider listing identity; maximum 50 characters.')
    period: Literal['annual','quarter'] = Field(default='annual',description='Fiscal frequency; quarterly aliases quarter. Duration/denominator and restatement conventions unknown.')
    limit: int = Field(default=20,ge=1,le=100,strict=True,description='Maximum returned rows; one request; replaces archived implicit 5.')


class FmpHistoricalMarketCapData(HistoricalMarketCapData):
    """FMP Historical Market Cap Data."""
    model_config = ConfigDict(extra='ignore')
    __alias_dict__ = {'market_cap': 'marketCap'}

class FMPShareStatisticsData(ShareStatisticsData):
    """FMP Share Statistics Data."""
    model_config = ConfigDict(extra='ignore')
    __alias_dict__ = {'url': 'source'}
    url: str | None = Field(default=None, description='URL to the source document, if available.')

class FMPEquityQuoteData(EquityQuoteData):
    """FMP Equity Quote Data."""
    model_config = ConfigDict(extra='ignore')
    __alias_dict__ = {'ma50': 'priceAvg50', 'ma200': 'priceAvg200', 'last_timestamp': 'timestamp', 'high': 'dayHigh', 'low': 'dayLow', 'last_price': 'price', 'change_percent': 'changePercentage', 'prev_close': 'previousClose'}
    ma50: float | None = Field(default=None, description='50 day moving average price.')
    ma200: float | None = Field(default=None, description='200 day moving average price.')
    market_cap: float | None = Field(default=None, description='Market cap of the company.')

class FMPIncomeStatementGrowthData(IncomeStatementGrowthData):
    """FMP Income Statement Growth Data."""
    model_config = ConfigDict(extra='ignore')
    __alias_dict__ = {'period_ending': 'date', 'fiscal_year': 'calendarYear', 'fiscal_period': 'period', 'growth_ebit': 'growthEBIT', 'growth_ebitda': 'growthEBITDA', 'growth_basic_earings_per_share': 'growthEPS', 'growth_gross_profit_margin': 'growthGrossProfitRatio', 'growth_consolidated_net_income': 'growthNetIncome', 'growth_diluted_earnings_per_share': 'growthEPSDiluted', 'growth_weighted_average_basic_shares_outstanding': 'growthWeightedAverageShsOut', 'growth_weighted_average_diluted_shares_outstanding': 'growthWeightedAverageShsOutDil', 'growth_research_and_development_expense': 'growthResearchAndDevelopmentExpenses', 'growth_general_and_admin_expense': 'growthGeneralAndAdministrativeExpenses', 'growth_selling_and_marketing_expense': 'growthSellingAndMarketingExpenses'}
    symbol: str = Field(description=DATA_DESCRIPTIONS.get('symbol', ''))
    reported_currency: str | None = Field(description='The currency in which the financial data is reported.', default=None)
    growth_revenue: float | None = Field(default=None, description='Growth rate of total revenue.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_cost_of_revenue: float | None = Field(default=None, description='Growth rate of cost of goods sold.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_gross_profit: float | None = Field(default=None, description='Growth rate of gross profit.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_gross_profit_margin: float | None = Field(default=None, description='Growth rate of gross profit as a percentage of revenue.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_general_and_admin_expense: float | None = Field(default=None, description='Growth rate of general and administrative expenses.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_research_and_development_expense: float | None = Field(default=None, description='Growth rate of expenses on research and development.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_selling_and_marketing_expense: float | None = Field(default=None, description='Growth rate of expenses on selling and marketing activities.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_other_expenses: float | None = Field(default=None, description='Growth rate of other operating expenses.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_operating_expenses: float | None = Field(default=None, description='Growth rate of total operating expenses.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_cost_and_expenses: float | None = Field(default=None, description='Growth rate of total costs and expenses.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_depreciation_and_amortization: float | None = Field(default=None, description='Growth rate of depreciation and amortization expenses.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_interest_income: float | None = Field(default=None, description='Growth rate of interest income.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_interest_expense: float | None = Field(default=None, description='Growth rate of interest expenses.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_net_interest_income: float | None = Field(default=None, description='Growth rate of net interest income.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_ebit: float | None = Field(default=None, description='Growth rate of Earnings Before Interest and Taxes (EBIT).', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_ebitda: float | None = Field(default=None, description='Growth rate of Earnings Before Interest, Taxes, Depreciation, and Amortization.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_operating_income: float | None = Field(default=None, description='Growth rate of operating income.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_non_operating_income_excluding_interest: float | None = Field(default=None, description='Growth rate of non-operating income excluding interest.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_total_other_income_expenses_net: float | None = Field(default=None, description='Growth rate of net total other income and expenses.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_other_adjustments_to_net_income: float | None = Field(default=None, description='Growth rate of other adjustments to net income.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_net_income_deductions: float | None = Field(default=None, description='Growth rate of net income deductions.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_income_before_tax: float | None = Field(default=None, description='Growth rate of income before taxes.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_income_tax_expense: float | None = Field(default=None, description='Growth rate of income tax expenses.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_net_income_from_continuing_operations: float | None = Field(default=None, description='Growth rate of net income from continuing operations.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_consolidated_net_income: float | None = Field(default=None, description='Growth rate of net income.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_basic_earings_per_share: float | None = Field(default=None, description='Growth rate of Earnings Per Share (EPS).', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_diluted_earnings_per_share: float | None = Field(default=None, description='Growth rate of diluted Earnings Per Share (EPS).', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_weighted_average_basic_shares_outstanding: float | None = Field(default=None, description='Growth rate of weighted average shares outstanding.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_weighted_average_diluted_shares_outstanding: float | None = Field(default=None, description='Growth rate of diluted weighted average shares outstanding.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})

class FMPBalanceSheetGrowthData(BalanceSheetGrowthData):
    """FMP Balance Sheet Growth Data."""
    model_config = ConfigDict(extra='ignore')
    __alias_dict__ = {'period_ending': 'date', 'fiscal_year': 'calendarYear', 'fiscal_period': 'period', 'currency': 'reportedCurrency', 'growth_other_total_shareholders_equity': 'growthOthertotalStockholdersEquity', 'growth_total_shareholders_equity': 'growthTotalStockholdersEquity', 'growth_total_liabilities_and_shareholders_equity': 'growthTotalLiabilitiesAndStockholdersEquity', 'growth_accumulated_other_comprehensive_income': 'growthAccumulatedOtherComprehensiveIncomeLoss', 'growth_prepaid_expenses': 'growthPrepaids'}
    symbol: str = Field(description=DATA_DESCRIPTIONS.get('symbol', ''))
    reported_currency: str | None = Field(description='The currency in which the financial data is reported.', default=None)
    growth_cash_and_cash_equivalents: float | None = Field(default=None, description='Growth rate of cash and cash equivalents.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_short_term_investments: float | None = Field(default=None, description='Growth rate of short-term investments.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_cash_and_short_term_investments: float | None = Field(default=None, description='Growth rate of cash and short-term investments.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_accounts_receivables: float | None = Field(default=None, description='Growth rate of accounts receivable.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_other_receivables: float | None = Field(default=None, description='Growth rate of other receivables.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_net_receivables: float | None = Field(default=None, description='Growth rate of net receivables.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_inventory: float | None = Field(default=None, description='Growth rate of inventory.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_other_current_assets: float | None = Field(default=None, description='Growth rate of other current assets.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_total_current_assets: float | None = Field(default=None, description='Growth rate of total current assets.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_property_plant_equipment_net: float | None = Field(description='Growth rate of net property, plant, and equipment.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_goodwill: float | None = Field(description='Growth rate of goodwill.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_intangible_assets: float | None = Field(description='Growth rate of intangible assets.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_goodwill_and_intangible_assets: float | None = Field(description='Growth rate of goodwill and intangible assets.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_long_term_investments: float | None = Field(default=None, description='Growth rate of long-term investments.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_tax_assets: float | None = Field(default=None, description='Growth rate of tax assets.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_other_non_current_assets: float | None = Field(default=None, description='Growth rate of other non-current assets.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_total_non_current_assets: float | None = Field(default=None, description='Growth rate of total non-current assets.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_other_assets: float | None = Field(default=None, description='Growth rate of other assets.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_total_assets: float | None = Field(default=None, description='Growth rate of total assets.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_account_payables: float | None = Field(default=None, description='Growth rate of accounts payable.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_other_payables: float | None = Field(default=None, description='Growth rate of other payables.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_total_payables: float | None = Field(default=None, description='Growth rate of total payables.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_accrued_expenses: float | None = Field(default=None, description='Growth rate of accrued expenses.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_prepaid_expenses: float | None = Field(default=None, description='Growth rate of prepaid expenses.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_capital_lease_obligations_current: float | None = Field(default=None, description='Growth rate of current capital lease obligations.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_short_term_debt: float | None = Field(default=None, description='Growth rate of short-term debt.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_tax_payables: float | None = Field(default=None, description='Growth rate of tax payables.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_deferred_revenue: float | None = Field(default=None, description='Growth rate of deferred revenue.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_other_current_liabilities: float | None = Field(default=None, description='Growth rate of other current liabilities.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_total_current_liabilities: float | None = Field(default=None, description='Growth rate of total current liabilities.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_deferred_revenue_non_current: float | None = Field(default=None, description='Growth rate of non-current deferred revenue.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_long_term_debt: float | None = Field(default=None, description='Growth rate of long-term debt.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_deferred_tax_liabilities_non_current: float | None = Field(default=None, description='Growth rate of non-current deferred tax liabilities.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_other_non_current_liabilities: float | None = Field(default=None, description='Growth rate of other non-current liabilities.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_total_non_current_liabilities: float | None = Field(default=None, description='Growth rate of total non-current liabilities.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_other_liabilities: float | None = Field(description='Growth rate of other liabilities.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_total_liabilities: float | None = Field(description='Growth rate of total liabilities.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_retained_earnings: float | None = Field(description='Growth rate of retained earnings.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_accumulated_other_comprehensive_income: float | None = Field(description='Growth rate of accumulated other comprehensive income/loss.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_minority_interest: float | None = Field(default=None, description='Growth rate of minority interest.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_additional_paid_in_capital: float | None = Field(default=None, description='Growth rate of additional paid-in capital.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_other_total_shareholders_equity: float | None = Field(default=None, description="Growth rate of other total stockholders' equity.", json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_total_shareholders_equity: float | None = Field(default=None, description="Growth rate of total stockholders' equity.", json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_common_stock: float | None = Field(description='Growth rate of common stock.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_preferred_stock: float | None = Field(description='Growth rate of preferred stock.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_treasury_stock: float | None = Field(default=None, description='Growth rate of treasury stock.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_total_equity: float | None = Field(default=None, description='Growth rate of total equity.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_total_liabilities_and_shareholders_equity: float | None = Field(default=None, description="Growth rate of total liabilities and stockholders' equity.", json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_total_investments: float | None = Field(default=None, description='Growth rate of total investments.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_total_debt: float | None = Field(default=None, description='Growth rate of total debt.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_net_debt: float | None = Field(default=None, description='Growth rate of net debt.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})

class FMPCashFlowStatementGrowthData(CashFlowStatementGrowthData):
    """FMP Cash Flow Statement Growth Data."""
    model_config = ConfigDict(extra='ignore')
    __alias_dict__ = {'period_ending': 'date', 'fiscal_year': 'calendarYear', 'fiscal_period': 'period', 'reported_currency': 'reportedCurrency', 'growth_acquisitions': 'growthAcquisitionsNet', 'growth_sale_and_maturity_of_investments': 'growthSalesMaturitiesOfInvestments', 'growth_net_cash_from_operating_activities': 'growthNetCashProvidedByOperatingActivities', 'growth_other_investing_activities': 'growthOtherInvestingActivities', 'growth_net_cash_from_investing_activities': 'growthNetCashUsedForInvestingActivities', 'growth_other_financing_activities': 'growthOtherFinancingActivities', 'growth_purchase_of_investment_securities': 'growthPurchasesOfInvestments', 'growth_account_receivables': 'growthAccountsReceivables', 'growth_account_payable': 'growthAccountsPayables', 'growth_purchase_of_property_plant_and_equipment': 'growthInvestmentsInPropertyPlantAndEquipment', 'growth_repayment_of_debt': 'growthDebtRepayment', 'growth_net_change_in_cash_and_equivalents': 'growthNetChangeInCash', 'growth_effect_of_exchange_rate_changes_on_cash': 'growthEffectOfForexChangesOnCash', 'growth_net_cash_from_financing_activities': 'growthNetCashUsedProvidedByFinancingActivities', 'growth_net_equity_issuance': 'growthNetStockIssuance', 'growth_common_equity_issuance': 'growthCommonStockIssued', 'growth_common_equity_repurchased': 'growthCommonStockRepurchased'}
    symbol: str = Field(description=DATA_DESCRIPTIONS.get('symbol', ''))
    reported_currency: str | None = Field(description='The currency in which the financial data is reported.', default=None)
    growth_net_income: float | None = Field(default=None, description='Growth rate of net income.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_depreciation_and_amortization: float | None = Field(default=None, description='Growth rate of depreciation and amortization.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_deferred_income_tax: float | None = Field(default=None, description='Growth rate of deferred income tax.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_stock_based_compensation: float | None = Field(default=None, description='Growth rate of stock-based compensation.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_change_in_working_capital: float | None = Field(default=None, description='Growth rate of change in working capital.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_account_receivables: float | None = Field(default=None, description='Growth rate of accounts receivables.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_inventory: float | None = Field(default=None, description='Growth rate of inventory.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_account_payable: float | None = Field(default=None, description='Growth rate of account payable.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_other_working_capital: float | None = Field(default=None, description='Growth rate of other working capital.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_other_non_cash_items: float | None = Field(default=None, description='Growth rate of other non-cash items.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_net_cash_from_operating_activities: float | None = Field(default=None, description='Growth rate of net cash provided by operating activities.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_purchase_of_property_plant_and_equipment: float | None = Field(default=None, description='Growth rate of investments in property, plant, and equipment.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_acquisitions: float | None = Field(default=None, description='Growth rate of net acquisitions.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_purchase_of_investment_securities: float | None = Field(default=None, description='Growth rate of purchases of investments.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_sale_and_maturity_of_investments: float | None = Field(default=None, description='Growth rate of sales maturities of investments.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_other_investing_activities: float | None = Field(default=None, description='Growth rate of other investing activities.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_net_cash_from_investing_activities: float | None = Field(default=None, description='Growth rate of net cash used for investing activities.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_short_term_net_debt_issuance: float | None = Field(default=None, description='Growth rate of short term net debt issuance.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_long_term_net_debt_issuance: float | None = Field(default=None, description='Growth rate of long term net debt issuance.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_net_debt_issuance: float | None = Field(default=None, description='Growth rate of net debt issuance.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_repayment_of_debt: float | None = Field(default=None, description='Growth rate of debt repayment.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_common_equity_issuance: float | None = Field(default=None, description='Growth rate of common equity issued.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_common_equity_repurchased: float | None = Field(default=None, description='Growth rate of common equity repurchased.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_net_equity_issuance: float | None = Field(default=None, description='Growth rate of net equity issuance.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_dividends_paid: float | None = Field(default=None, description='Growth rate of dividends paid.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_preferred_dividends_paid: float | None = Field(default=None, description='Growth rate of preferred dividends paid.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_other_financing_activities: float | None = Field(default=None, description='Growth rate of other financing activities.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_net_cash_from_financing_activities: float | None = Field(default=None, description='Growth rate of net cash used/provided by financing activities.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_effect_of_exchange_rate_changes_on_cash: float | None = Field(default=None, description='Growth rate of the effect of foreign exchange changes on cash.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_net_change_in_cash_and_equivalents: float | None = Field(default=None, description='Growth rate of net change in cash.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_cash_at_beginning_of_period: float | None = Field(default=None, description='Growth rate of cash at the beginning of the period.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_cash_at_end_of_period: float | None = Field(default=None, description='Growth rate of cash at the end of the period.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_operating_cash_flow: float | None = Field(default=None, description='Growth rate of operating cash flow.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_capital_expenditure: float | None = Field(default=None, description='Growth rate of capital expenditure.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_income_taxes_paid: float | None = Field(default=None, description='Growth rate of income taxes paid.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_interest_paid: float | None = Field(default=None, description='Growth rate of interest paid.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})
    growth_free_cash_flow: float | None = Field(default=None, description='Growth rate of free cash flow.', json_schema_extra={'x-unit_measurement': 'percent', 'x-frontend_multiply': 100})

RETAINED_ALIASES = {
    'historical_market_cap': dict(FmpHistoricalMarketCapData.__alias_dict__),
    'share_statistics': dict(FMPShareStatisticsData.__alias_dict__),
    'equity_quote': dict(FMPEquityQuoteData.__alias_dict__),
    'income_statement_growth': dict(FMPIncomeStatementGrowthData.__alias_dict__),
    'balance_sheet_growth': dict(FMPBalanceSheetGrowthData.__alias_dict__),
    'cash_flow_growth': dict(FMPCashFlowStatementGrowthData.__alias_dict__),
}

# Retained currency destination was undeclared; preserve reported currency instead.
FMPBalanceSheetGrowthData.__alias_dict__ = {('reported_currency' if key=='currency' else key):value for key,value in RETAINED_ALIASES['balance_sheet_growth'].items()}

class FMPShareStatisticsData(FMPShareStatisticsData):
    @field_validator('free_float',mode='before')
    @classmethod
    def normalize_percent(cls,value):
        return value / 100 if value is not None else None

class FMPEquityQuoteData(FMPEquityQuoteData):
    @field_validator('last_timestamp',mode='before')
    @classmethod
    def epoch_utc(cls,value):
        if value is None:
            return None
        if isinstance(value,datetime):
            return value
        if isinstance(value,bool):
            raise ValueError('Unix seconds required')
        return datetime.fromtimestamp(int(value),timezone.utc)

    @field_validator('change_percent',mode='after')
    @classmethod
    def normalize_percent(cls,value):
        return value / 100 if value is not None else None


# These four misspellings are present in the checked official stable example.
CASH_FLOW_SOURCE_SPELLINGS = {
    'growth_net_cash_from_operating_activities': ('growthNetCashProvidedByOperatingActivities','growthNetCashProvidedByOperatingActivites'),
    'growth_other_investing_activities': ('growthOtherInvestingActivities','growthOtherInvestingActivites'),
    'growth_net_cash_from_investing_activities': ('growthNetCashUsedForInvestingActivities','growthNetCashUsedForInvestingActivites'),
    'growth_other_financing_activities': ('growthOtherFinancingActivities','growthOtherFinancingActivites'),
}

class FMPCashFlowStatementGrowthData(FMPCashFlowStatementGrowthData):
    @model_validator(mode='before')
    @classmethod
    def documented_source_spellings(cls,values):
        values=dict(values)
        for canonical,(retained,official) in CASH_FLOW_SOURCE_SPELLINGS.items():
            supplied=[values[key] for key in (canonical,retained,official) if key in values]
            if supplied and any(value != supplied[0] for value in supplied):
                raise ValueError('Conflicting source field spellings')
            if official in values:
                values[retained]=values.pop(official)
        return values

CONTRACTS = {
    'historical_market_cap': (FmpHistoricalMarketCapQueryParams,FmpHistoricalMarketCapData),
    'share_statistics': (FMPShareStatisticsQueryParams,FMPShareStatisticsData),
    'equity_quote': (FMPEquityQuoteQueryParams,FMPEquityQuoteData),
    'income_statement_growth': (FMPIncomeStatementGrowthQueryParams,FMPIncomeStatementGrowthData),
    'balance_sheet_growth': (FMPBalanceSheetGrowthQueryParams,FMPBalanceSheetGrowthData),
    'cash_flow_growth': (FMPCashFlowStatementGrowthQueryParams,FMPCashFlowStatementGrowthData),
}

def field_template(name,dataset):
    unit=None
    origin='provider_observation'
    kwargs={}
    if dataset.endswith('growth'):
        if name.startswith('growth_'):
            unit='ratio'
            origin='provider_calculation'
        kwargs['observation_date_field']='period_ending'
        kwargs['period_basis']=('stock comparison; source denominator periods and restatement unknown' if dataset=='balance_sheet_growth' else 'flow growth; discrete versus year-to-date duration, source denominator periods and restatement unknown')
        kwargs['financial_basis']={'market_date':None}
    elif dataset=='historical_market_cap':
        if name=='market_cap':
            unit='currency'
            origin='provider_calculation'
        kwargs['observation_date_field']='date'
        kwargs['financial_basis']={'share_count':None,'market_date':'capitalization observation date; price basis unknown'}
    elif dataset=='share_statistics':
        if name in {'outstanding_shares','float_shares'}:
            unit='shares'
        if name=='free_float':
            unit='ratio'
            origin='provider_calculation'
            kwargs['source_unit']='percent'
            kwargs['requested_transform']='divide_by_100'
        kwargs['observation_date_field']='date'
        kwargs['financial_basis']={'share_count':'provider float and outstanding share counts; methodology unknown'}
    else:
        if name in {'last_price','bid','ask','open','high','low','close','prev_close','change','year_high','year_low','ma50','ma200'}:
            unit='currency/share'
            if name in {'change','ma50','ma200'}:
                origin='provider_calculation'
        elif name in {'volume','exchange_volume','last_size'}:
            unit='shares'
        elif name in {'bid_size','ask_size'}:
            unit='round_lots'
        elif name=='market_cap':
            unit='currency'
            origin='provider_calculation'
        elif name=='change_percent':
            unit='ratio'
            origin='provider_calculation'
            kwargs['source_unit']='percent'
            kwargs['requested_transform']='divide_by_100'
        elif name=='sequence_number':
            unit='count'
        if name in {'last_price','change','change_percent','last_timestamp'}:
            kwargs['observation_date_field']='last_timestamp'
        kwargs['financial_basis']={'market_date':None,'share_count':None}
        if name in {'bid_size','ask_size'}:
            kwargs['period_basis']='order size in round lots; standard describes normal lot as 100 shares, actual listing lot convention unverified'
    return FinancialFieldTemplate(unit=unit,scale=1 if unit else None,value_origin=origin,**kwargs)

for _name,(_, _row) in CONTRACTS.items():
    if _name.endswith('growth'):
        # Retained percent flags actively select a multiplying native formatter.
        # Growth fractions must remain ratios in both values and presentation.
        for _field, _info in _row.model_fields.items():
            if _field.startswith('growth_'):
                _extra = dict(_info.json_schema_extra or {})
                _extra.pop('x-frontend_multiply', None)
                _extra['x-unit_measurement'] = 'ratio'
                _info.json_schema_extra = _extra
        _row.model_rebuild(force=True)
    _row.financial_data_annotation=FinancialDataAnnotation(fields={name:field_template(name,_name) for name in _row.model_fields},runtime_properties=['fields.availability','retrieved_at','effective_query','bounds'])
