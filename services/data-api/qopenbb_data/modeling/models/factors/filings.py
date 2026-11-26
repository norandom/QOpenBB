"""Resolve point-in-time fiscal cash flows for issuer free cash flow yield."""

from collections import defaultdict
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Context, Decimal, localcontext
from zoneinfo import ZoneInfo

from ...contracts import EvaluationCutoff, Observation
from .sessions import latest_observed_rows

_OPERATING = "operating_cash_flow"
_CAPEX = "capital_expenditures"
_NEGATIVE_OUTFLOW = "cash_outflow_negative"
_POSITIVE_SPENDING = "spending_positive"
_QUARTERLY = frozenset({"quarterly", "standalone_quarter"})
_ANNUAL = frozenset({"annual"})
_YEAR_DAYS = frozenset({364, 365, 366, 371})
_QUARTERS_PER_YEAR = 4
_MIN_QUARTER_DAYS = 84
_MAX_QUARTER_DAYS = 98


@dataclass(frozen=True)
class CashFlows:
    issuer_id: str
    currency: str
    scale: int
    rows: tuple[Observation, ...]

    @property
    def operating_cash_flow(self) -> Decimal:
        return _component_total(self.rows[::2])

    @property
    def capex_spending(self) -> Decimal:
        return _component_total(self.rows[1::2])

    @property
    def period_start(self) -> date:
        start = self.rows[0].context.period_start
        assert start is not None
        return start

    @property
    def period_end(self) -> date:
        return self.rows[-1].observation_date


class _CoverageMissing(ValueError):
    """The trailing period lacks eligible evidence for some required cash flows."""


@dataclass(frozen=True)
class _FiscalPeriod:
    start: date
    end: date
    rows: tuple[Observation, ...]


def _is_year_to_date(row: Observation) -> bool:
    context = row.context
    for marker in (context.frequency, context.fiscal_period, context.basis):
        normalized = (marker or "").lower().replace("-", "_").replace(" ", "_")
        if "ytd" in normalized.split("_") or "year_to_date" in normalized:
            return True
    return False


def _premature_publication(row: Observation, end: date, cutoff: EvaluationCutoff) -> bool:
    # Fiscal intervals have day precision and use the evaluation's session time zone.
    return (row.published_at is not None
            and row.published_at.astimezone(ZoneInfo(cutoff.session_timezone)).date() < end)


def _filing_eligible(row: Observation, end: date, cutoff: EvaluationCutoff) -> bool:
    return (row.category != "estimate" and cutoff.is_eligible(row)
            and not _premature_publication(row, end, cutoff))


def _revision_key(row: Observation) -> tuple[datetime, datetime]:
    assert row.published_at is not None
    return row.vintage_at or row.published_at, row.published_at


def _active_revisions(rows: list[Observation], end: date,
                      cutoff: EvaluationCutoff) -> list[Observation]:
    # Rank within a filing and fiscal end before looking at duration. An amendment
    # can correct the label or interval of previously reported standalone flows.
    retained = []
    by_source: dict[str, list[Observation]] = {}
    for row in rows:
        source = row.source_record_id
        if source is None or not _filing_eligible(row, end, cutoff):
            retained.append(row)
            continue
        previous = by_source.get(source)
        if previous is None or _revision_key(row) > _revision_key(previous[0]):
            by_source[source] = [row]
        elif _revision_key(row) == _revision_key(previous[0]):
            previous.append(row)
    return retained + [row for revision in by_source.values() for row in revision]


def _latest_filing_rows(rows: list[Observation], end: date, cutoff: EvaluationCutoff,
                        label: str) -> list[Observation] | str:
    filed = []
    premature_metrics = set()
    for row in rows:
        if row.category != "estimate" and _premature_publication(row, end, cutoff):
            if cutoff.is_eligible(row):
                premature_metrics.add(row.metric_id)
        else:
            filed.append(row)
    latest = latest_observed_rows(filed, cutoff, label)
    metrics = set() if isinstance(latest, str) else {row.metric_id for row in latest}
    if premature_metrics - metrics:
        raise ValueError(f"{label} published before its fiscal period ended on {end}")
    return latest


def _period(rows: list[Observation], end: date, cutoff: EvaluationCutoff,
            frequencies: frozenset[str], label: str) -> _FiscalPeriod:
    active = _active_revisions(rows, end, cutoff)
    candidates = [row for row in active
                  if row.context.frequency in frequencies and not _is_year_to_date(row)]
    latest = _latest_filing_rows(candidates, end, cutoff, label)
    if isinstance(latest, str):
        raise _CoverageMissing(f"{latest} for {end}")

    metrics = {row.metric_id for row in latest}
    if any(row.metric_id not in metrics and row.context.frequency in frequencies
           and not _is_year_to_date(row) and _filing_eligible(row, end, cutoff) for row in rows):
        raise ValueError(f"Incomplete cash-flow filing at the latest vintage for {end}")

    starts = {row.context.period_start for row in latest}
    if len(starts) != 1 or any(row.context.period_end != end or row.observation_date != end for row in latest):
        raise ValueError(f"Conflicting or missing {label} period dates for {end}")
    start = starts.pop()
    if start is None:
        raise ValueError(f"Missing {label} period start for {end}")
    days = (end - start).days + 1
    if frequencies == _QUARTERLY and not _MIN_QUARTER_DAYS <= days <= _MAX_QUARTER_DAYS:
        raise ValueError(f"Invalid standalone quarter period {start} to {end}")
    if frequencies == _ANNUAL and days not in _YEAR_DAYS:
        raise ValueError(f"Incomplete annual fiscal period {start} to {end}")
    return _FiscalPeriod(start, end, tuple(latest))


def _require_comparable(first: Observation, second: Observation, end: date) -> None:
    for field, label in (("currency", "currency"), ("scale", "scale"),
                         ("consolidation_scope", "consolidation scope"),
                         ("accounting_standard", "accounting standard")):
        if getattr(first.context, field) != getattr(second.context, field):
            raise ValueError(f"Cash-flow {label} differs for {end}")


def _filing_rows(period: _FiscalPeriod, capex_sign: str) -> tuple[Observation, ...]:
    end = period.end
    operating = [row for row in period.rows if row.metric_id == _OPERATING]
    spending = [row for row in period.rows if row.metric_id == _CAPEX]
    if len(operating) > 1 or len(spending) > 1:
        raise ValueError(f"Conflicting cash-flow lines at the latest filing vintage for {end}")
    for row in period.rows:
        if not row.source_record_id:
            raise ValueError(f"Missing source filing ID for {end}")
        if row.context.unit != "currency" or row.context.quantity != "flow":
            raise ValueError(f"{row.metric_id} requires a currency flow for {end}")
        if row.context.currency is None:
            raise ValueError(f"Missing cash-flow currency for {end}")
        if row.context.consolidation_scope != "issuer_consolidated":
            raise ValueError(f"Cash-flow scope must be issuer_consolidated for {end}")
        if row.value is None or not row.value.is_finite():
            raise ValueError(f"Missing or nonfinite {row.metric_id} amount for {end}")
        if row.metric_id == _CAPEX:
            if row.context.basis != capex_sign:
                raise ValueError(f"Missing or mismatched capex sign convention evidence for {end}")
            if (capex_sign == _NEGATIVE_OUTFLOW and row.value > 0
                    or capex_sign == _POSITIVE_SPENDING and row.value < 0):
                raise ValueError(f"Cash-flow capex sign contradicts the reported convention for {end}")
    if not operating or not spending:
        return (*operating, *spending)
    ocf, capex = operating[0], spending[0]
    if ocf.source_record_id != capex.source_record_id:
        raise ValueError(f"Mixed source filing IDs for {end}")
    if (ocf.published_at, ocf.vintage_at) != (capex.published_at, capex.vintage_at):
        raise ValueError(f"Mixed filing publication or vintage timestamps for {end}")
    _require_comparable(ocf, capex, end)
    return ocf, capex


def _quarter_rows(by_end: dict[date, list[Observation]], end: date,
                  cutoff: EvaluationCutoff, capex_sign: str) -> tuple[Observation, ...]:
    trailing_end = end
    filings = []
    for position in range(_QUARTERS_PER_YEAR):
        period = _period(by_end.get(end, []), end, cutoff, _QUARTERLY, "standalone quarter filing")
        filings.append(_filing_rows(period, capex_sign))
        if position + 1 < _QUARTERS_PER_YEAR:
            if period.start == date.min:
                raise _CoverageMissing(f"Incomplete preceding standalone quarter for {end}")
            end = date.fromordinal(period.start.toordinal() - 1)
    if (trailing_end - period.start).days + 1 not in _YEAR_DAYS:
        raise ValueError(f"Invalid trailing fiscal year from {period.start} to {trailing_end}")
    rows = tuple(row for filing in reversed(filings) for row in filing)
    for row in rows[1:]:
        _require_comparable(rows[0], row, row.observation_date)
    return rows


def _check_annual_boundaries(annual: _FiscalPeriod, by_end: dict[date, list[Observation]],
                             cutoff: EvaluationCutoff) -> None:
    cursor = annual.start.toordinal()
    gaps = []
    for end in sorted(day for day in by_end if annual.start <= day <= annual.end):
        try:
            quarter = _period(by_end[end], end, cutoff, _QUARTERLY, "standalone quarter filing")
        except _CoverageMissing:
            continue
        gaps.append(quarter.start.toordinal() - cursor)
        cursor = end.toordinal() + 1
    gaps.append(annual.end.toordinal() + 1 - cursor)
    # Every gap between observed quarters and the annual boundaries must fit a
    # whole number of missing fiscal quarters, even when an interior filing is absent.
    bounds = [((gap + _MAX_QUARTER_DAYS - 1) // _MAX_QUARTER_DAYS, gap // _MIN_QUARTER_DAYS)
              for gap in gaps]
    observed_quarters = len(gaps) - 1
    missing = _QUARTERS_PER_YEAR - observed_quarters
    if (any(gap < 0 for gap in gaps) or any(low > high for low, high in bounds)
            or not sum(low for low, _ in bounds) <= missing <= sum(high for _, high in bounds)):
        raise ValueError(f"The annual filing boundaries {annual.start} to {annual.end} conflict with observed quarters")


def _select_periods(by_end: dict[date, list[Observation]], end: date,
                    cutoff: EvaluationCutoff, capex_sign: str) -> tuple[Observation, ...]:
    quarter_rows: tuple[Observation, ...] = ()
    quarter_gap = f"Incomplete standalone quarter cash-flow coverage through {end}"
    try:
        quarter_rows = _quarter_rows(by_end, end, cutoff, capex_sign)
    except _CoverageMissing as exc:
        quarter_gap = str(exc)
    quarters_complete = len(quarter_rows) == _QUARTERS_PER_YEAR * 2

    try:
        annual = _period(by_end[end], end, cutoff, _ANNUAL, "annual filing")
    except _CoverageMissing as exc:
        if quarters_complete:
            return quarter_rows
        raise _CoverageMissing(f"{quarter_gap}; {exc}") from exc

    same_span = bool(quarter_rows and annual.start == quarter_rows[0].context.period_start)
    if quarters_complete and not same_span:
        return quarter_rows

    annual_rows = _filing_rows(annual, capex_sign)
    if same_span:
        _reconcile_components(quarter_rows, annual_rows, end)
    if quarters_complete:
        return quarter_rows
    if len(annual_rows) != 2:
        raise _CoverageMissing(f"{quarter_gap}; Incomplete annual cash-flow filing for {end}")
    _check_annual_boundaries(annual, by_end, cutoff)
    return annual_rows


def _reconcile_components(quarter_rows: tuple[Observation, ...], annual_rows: tuple[Observation, ...],
                          end: date) -> None:
    # Each line can establish a full-span total independently of the other line's coverage.
    for annual in annual_rows:
        quarters = tuple(row for row in quarter_rows if row.metric_id == annual.metric_id)
        if len(quarters) != _QUARTERS_PER_YEAR:
            continue
        _require_comparable(quarters[0], annual, end)
        if _component_total(quarters) != _component_total((annual,)):
            raise ValueError(f"Same-span annual and quarter cash-flow totals conflict for {annual.metric_id} on {end}")


def _component_total(rows: tuple[Observation, ...]) -> Decimal:
    total = Decimal(0)
    # Four inputs can carry into a 39th integral place while retaining 38 fractional places.
    with localcontext(Context(prec=77)):
        for row in rows:
            assert row.value is not None
            total += row.value.copy_abs() if row.metric_id == _CAPEX else row.value
    return total


def resolve_cash_flows(rows: tuple[Observation, ...], cutoff: EvaluationCutoff,
                       capex_sign: str) -> CashFlows:
    """Return original filing rows in fiscal order, or raise a dated input error."""
    by_end: dict[date, list[Observation]] = defaultdict(list)
    known_ends = set()
    issuers = set()
    for row in rows:
        end = row.context.period_end or row.observation_date
        if row.metric_id not in (_OPERATING, _CAPEX) or end > cutoff.observation_date:
            continue
        by_end[end].append(row)
        if _filing_eligible(row, end, cutoff):
            known_ends.add(end)
            issuers.add(row.entity_id)

    if not by_end:
        raise ValueError(f"Missing cash-flow filings as of {cutoff.observation_date}")
    if not known_ends:
        end = max(by_end)
        reason = _latest_filing_rows(by_end[end], end, cutoff, "cash-flow filing")
        raise ValueError(f"{reason} for {end} as of {cutoff.observation_date}")
    end = max(known_ends)
    if len(issuers) != 1:
        raise ValueError(f"Cash-flow filings must identify a single issuer for {end}")
    if capex_sign not in (_NEGATIVE_OUTFLOW, _POSITIVE_SPENDING):
        raise ValueError(f"Unknown capex sign convention for {end}")

    latest_gap = None
    for candidate_end in sorted(known_ends, reverse=True):
        try:
            selected = _select_periods(by_end, candidate_end, cutoff, capex_sign)
        except _CoverageMissing as exc:
            if latest_gap is None:
                latest_gap = exc
        except ValueError as exc:
            raise ValueError(f"Cash flows for trailing fiscal end {candidate_end}: {exc}") from exc
        else:
            currency = selected[0].context.currency
            assert currency is not None
            return CashFlows(selected[0].entity_id, currency, selected[0].context.scale, selected)
    raise ValueError(f"Cash flows for trailing fiscal end {end}: {latest_gap}") from latest_gap
