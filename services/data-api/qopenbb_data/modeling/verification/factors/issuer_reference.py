"""Version 1 independent scalar reference for issuer FCF yield."""

from collections import defaultdict
from datetime import date, datetime
from decimal import Context, Decimal, localcontext
from zoneinfo import ZoneInfo

from ...contracts import (
    AssumptionSet,
    EvaluationCutoff,
    InputSnapshot,
    Observation,
    Tolerance,
)
from ...contracts.common import parse_decimal
from ..reference import Reference

_OPERATING = "operating_cash_flow"
_CAPEX = "capital_expenditures"
_YEAR_DAYS = {364, 365, 366, 371}
_QUARTER_KINDS = {"quarterly", "standalone_quarter"}
_CAPEX_MULTIPLIER = {"cash_outflow_negative": -1, "spending_positive": 1}


def _revision(row: Observation) -> datetime:
    assert row.published_at is not None
    return row.vintage_at or row.published_at


def _observable(row: Observation, cutoff: EvaluationCutoff) -> bool:
    published = row.published_at
    return (row.category != "estimate" and published is not None
            and row.observation_date <= cutoff.observation_date
            and row.context.vintage_coverage not in {"unknown", "unavailable"}
            and max(published, _revision(row)) <= min(cutoff.decision_at, cutoff.evaluated_at))


def _published_on_or_after(row: Observation, end: date, zone: ZoneInfo) -> bool:
    assert row.published_at is not None
    return row.published_at.astimezone(zone).date() >= end


def _money_basis(row: Observation) -> tuple[str | None, int, str | None]:
    context = row.context
    return context.currency, context.scale, context.consolidation_scope


def _cash_basis(row: Observation) -> tuple[str | None, int, str | None, str | None]:
    return (*_money_basis(row), row.context.accounting_standard)


def _year_to_date(row: Observation) -> bool:
    for marker in (row.context.frequency, row.context.fiscal_period, row.context.basis):
        label = (marker or "").lower().replace("-", "_").replace(" ", "_")
        if "ytd" in label.split("_") or "year_to_date" in label:
            return True
    return False


def _period_lines(rows: list[Observation], end: date, kinds: set[str],
                  zone: ZoneInfo) -> tuple[Observation, ...]:
    # Amendments can change the interval label. Resolve each source filing first.
    sources = defaultdict(list)
    premature = set()
    for row in rows:
        if _published_on_or_after(row, end, zone):
            sources[row.source_record_id].append(row)
        elif row.context.frequency in kinds and not _year_to_date(row):
            premature.add(row.metric_id)
    candidates = []
    for source, versions in sources.items():
        newest = max((_revision(row), row.published_at) for row in versions)
        candidates.extend(row for row in versions
                          if (source is None or (_revision(row), row.published_at) == newest)
                          and row.context.frequency in kinds and not _year_to_date(row))
    vintage = max(map(_revision, candidates), default=None)
    lines = tuple(row for row in candidates if _revision(row) == vintage)
    selected = {row.metric_id for row in lines}
    if premature - selected:
        raise ValueError("Filing predates fiscal close")
    original = {row.metric_id for versions in sources.values() for row in versions
                if row.context.frequency in kinds and not _year_to_date(row)}
    if lines and original - selected:
        raise ValueError("Incomplete newer filing")
    return lines


def _span(lines: tuple[Observation, ...], end: date, *, annual: bool) -> date:
    starts = {row.context.period_start for row in lines}
    if len(starts) != 1 or any(row.context.period_end != end or row.observation_date != end for row in lines):
        raise ValueError("Unreconciled fiscal dates")
    start = starts.pop()
    if start is None:
        raise ValueError("Unknown fiscal start")
    days = (end - start).days + 1
    if (annual and days not in _YEAR_DAYS) or (not annual and not 84 <= days <= 98):
        raise ValueError("Invalid fiscal duration")
    return start


def _check_filing(lines: tuple[Observation, ...], convention: str) -> None:
    if len({row.metric_id for row in lines}) != len(lines):
        raise ValueError("Duplicate filing line")
    identities = {(row.source_record_id, row.published_at, row.vintage_at, _cash_basis(row)) for row in lines}
    if len(identities) != 1 or not lines[0].source_record_id:
        raise ValueError("Mixed or missing filing identity")
    for row in lines:
        context = row.context
        if (row.value is None or not row.value.is_finite() or context.currency is None
                or (context.unit, context.quantity, context.consolidation_scope) !=
                ("currency", "flow", "issuer_consolidated")):
            raise ValueError("Incomparable cash flow")
        if row.metric_id == _CAPEX and (context.basis != convention
                                      or row.value * _CAPEX_MULTIPLIER[convention] < 0):
            raise ValueError("Invalid capex sign")


def _quarters(by_end: dict[date, list[Observation]], end: date, convention: str,
              zone: ZoneInfo) -> tuple[Observation, ...]:
    fiscal_end = end
    windows = []
    for position in range(4):
        lines = _period_lines(by_end.get(end, []), end, _QUARTER_KINDS, zone)
        if not lines:
            return ()
        start = _span(lines, end, annual=False)
        _check_filing(lines, convention)
        windows.append(lines)
        if position < 3:
            if start == date.min:
                return ()
            end = date.fromordinal(start.toordinal() - 1)
    if (fiscal_end - start).days + 1 not in _YEAR_DAYS:
        raise ValueError("Quarters do not span a fiscal year")
    trailing = tuple(row for lines in reversed(windows) for row in lines)
    if len({_cash_basis(row) for row in trailing}) != 1:
        raise ValueError("Incomparable quarters")
    return trailing


def _annual_boundaries(by_end: dict[date, list[Observation]], start: date, end: date,
                       zone: ZoneInfo) -> None:
    cursor = start.toordinal()
    gaps = []
    for quarter_end in sorted(day for day in by_end if start <= day <= end):
        lines = _period_lines(by_end[quarter_end], quarter_end, _QUARTER_KINDS, zone)
        if lines:
            quarter_start = _span(lines, quarter_end, annual=False)
            gaps.append(quarter_start.toordinal() - cursor)
            cursor = quarter_end.toordinal() + 1
    gaps.append(end.toordinal() + 1 - cursor)
    # An annual total can bridge absent quarters only if the observed intervals
    # leave room for exactly the required number of missing standalone quarters.
    counts = {0}
    for gap in gaps:
        counts = {covered + quarters for covered in counts for quarters in range(5)
                  if 84 * quarters <= gap <= 98 * quarters}
    if 5 - len(gaps) not in counts:
        raise ValueError("Annual and quarterly boundaries conflict")


def _trailing(by_end: dict[date, list[Observation]], convention: str,
              zone: ZoneInfo) -> tuple[Observation, ...]:
    for end in sorted(by_end, reverse=True):
        if not any(_published_on_or_after(row, end, zone) for row in by_end[end]):
            continue
        quarters = _quarters(by_end, end, convention, zone)
        annual = _period_lines(by_end[end], end, {"annual"}, zone)
        if not annual:
            if len(quarters) == 8:
                return quarters
            continue
        start = _span(annual, end, annual=True)
        same_span = bool(quarters and start == quarters[0].context.period_start)
        if len(quarters) == 8 and not same_span:
            return quarters
        _check_filing(annual, convention)
        if same_span:
            for total in annual:
                amounts = [row.value for row in quarters if row.metric_id == total.metric_id]
                if len(amounts) == 4 and (sum(amounts) != total.value
                                          or _cash_basis(total) != _cash_basis(quarters[0])):
                    raise ValueError("Same-period cash-flow totals conflict")
        if len(quarters) == 8:
            return quarters
        if len(annual) == 2:
            _annual_boundaries(by_end, start, end, zone)
            return annual
    return ()


def _equity(rows: tuple[Observation, ...], filing: Observation, cutoff: EvaluationCutoff) -> Decimal | None:
    day = cutoff.observation_date
    zone = ZoneInfo(cutoff.session_timezone)
    eligible = [row for row in rows if row.entity_id == filing.entity_id
                and row.metric_id == "equity_market_value" and row.observation_date == day
                and _observable(row, cutoff) and _published_on_or_after(row, day, zone)]
    if not eligible:
        return None
    latest = max(map(_revision, eligible))
    amounts = set()
    for row in eligible:
        if _revision(row) != latest:
            continue
        if (row.value is None or not row.value.is_finite() or row.value <= 0
                or (row.context.quantity, row.context.unit) != ("stock", "currency")
                or _money_basis(row) != _money_basis(filing)
                or any(bound not in (None, day) for bound in (row.context.period_start, row.context.period_end))):
            return None
        amounts.add(row.value)
    return amounts.pop() if len(amounts) == 1 else None


def _eligible_filings(rows: tuple[Observation, ...], cutoff: EvaluationCutoff,
                      zone: ZoneInfo) -> dict[date, list[Observation]]:
    by_end = defaultdict(list)
    issuers = set()
    for row in rows:
        end = row.context.period_end or row.observation_date
        if (row.metric_id in {_OPERATING, _CAPEX} and end <= cutoff.observation_date
                and _observable(row, cutoff)):
            by_end[end].append(row)
            if _published_on_or_after(row, end, zone):
                issuers.add(row.entity_id)
    return by_end if len(issuers) == 1 else {}


def _yield(inputs: InputSnapshot, assumptions: AssumptionSet) -> Decimal | None:
    cutoff = inputs.cutoff
    if (inputs.schema_id != "issuer_fcf_yield.inputs" or inputs.schema_version != "1"
            or assumptions.version != "1" or cutoff is None
            or assumptions.effective_date > cutoff.observation_date):
        return None
    convention = next((item.value for item in assumptions.assumptions if item.assumption_id == "capex_sign"
                       and item.value_type == "text" and isinstance(item.value, str)), None)
    if convention not in _CAPEX_MULTIPLIER:
        return None
    tables = {table.table_id: table.rows for table in inputs.tables}
    zone = ZoneInfo(cutoff.session_timezone)
    by_end = _eligible_filings(tables.get("cash_flows", ()), cutoff, zone)
    with localcontext(Context(prec=240)):
        try:
            filings = _trailing(by_end, convention, zone)
            if not filings:
                return None
            market = _equity(tables.get("market_value", ()), filings[0], cutoff)
            if market is None:
                return None
            spending = sum(row.value for row in filings if row.metric_id == _CAPEX) * _CAPEX_MULTIPLIER[convention]
            operating = sum(row.value for row in filings if row.metric_id == _OPERATING)
            fcf = operating - spending
            # Monetary intermediates must also fit the evidence contract.
            parse_decimal(spending)
            parse_decimal(fcf)
            percent = fcf / (market / 100)
            if percent and percent.adjusted() < -38:
                return None
            return parse_decimal(round(percent, min(38, 37 - percent.adjusted())))
        except ValueError:
            return None


def issuer_reference() -> Reference:
    """Bind the issuer percent output to reference version 1."""
    return Reference("1", {"fcf_yield": _yield},
                     {"fcf_yield": Tolerance(unit="percent", absolute=Decimal("0.00000001"))})
