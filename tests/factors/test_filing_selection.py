"""Point-in-time issuer cash-flow periods and their source filings."""

from datetime import date, timedelta
from decimal import Decimal, Inexact, localcontext
from itertools import pairwise

import pytest
from fixtures.factor_inputs import END, company_inputs, cutoff, row, utc
from qopenbb_data.modeling.models.factors.filings import resolve_cash_flows

NEGATIVE = "cash_outflow_negative"
POSITIVE = "spending_positive"
DECISION = date(2025, 6, 25)
WEEK_ENDS = tuple(date.fromisoformat(day) for day in (
    "2024-03-30", "2024-06-29", "2024-09-28", "2024-12-28", "2025-03-29",
))


def period(start, end, *, frequency="quarterly", sign=NEGATIVE, ocf="15", capex="-5"):
    context = {
        "published_at": utc(end + timedelta(days=30), 17),
        "source_record_id": f"filing.{start}.{end}",
        "currency": "USD", "scale": 6, "quantity": "flow", "frequency": frequency,
        "period_start": start, "period_end": end, "consolidation_scope": "issuer_consolidated",
    }
    return (
        row("fixture_company", "operating_cash_flow", end, ocf, "currency", **context),
        row("fixture_company", "capital_expenditures", end, capex, "currency", basis=sign, **context),
    )


def quarters(ends=WEEK_ENDS):
    return tuple(item for before, end in pairwise(ends)
                 for item in period(before + timedelta(days=1), end))


def variant(item, suffix, *, context=None, **updates):
    return item.model_copy(update={
        "record_id": f"{item.record_id}.{suffix}",
        "context": item.context.model_copy(update=context or {}),
        **updates,
    })


def assert_unavailable(rows, day, reason, *, decision=DECISION, sign=NEGATIVE):
    with pytest.raises(ValueError, match=reason) as caught:
        resolve_cash_flows(rows, cutoff(decision), sign)
    assert day.isoformat() in str(caught.value)


def test_frozen_annual_filing_retains_original_evidence():
    rows = company_inputs(False)[0].rows
    result = resolve_cash_flows(rows[::-1], cutoff(END), NEGATIVE)
    assert (result.issuer_id, result.currency, result.scale) == ("fixture_company", "USD", 6)
    assert (result.operating_cash_flow, result.capex_spending) == (Decimal(60), Decimal(20))
    assert result.rows == rows
    assert all(selected is expected for selected, expected in zip(result.rows, rows, strict=True))


@pytest.mark.parametrize("ends", [
    WEEK_ENDS,
    WEEK_ENDS[:-1] + (date(2025, 4, 5),),
    tuple(date.fromisoformat(day) for day in (
        "2023-09-30", "2023-12-31", "2024-03-31", "2024-06-30", "2024-09-30",
    )),
], ids=["52-weeks", "53-weeks", "leap-calendar"])
def test_rolling_quarters_follow_reported_dates_in_order(ends):
    rows = quarters(ends)
    result = resolve_cash_flows(rows[::-1], cutoff(DECISION), NEGATIVE)
    assert result.rows == rows
    assert (result.operating_cash_flow, result.capex_spending) == (Decimal(60), Decimal(20))


@pytest.mark.parametrize("end", [date(2025, 3, 29), date(2025, 4, 5)])
def test_annual_fallback_supports_week_based_fiscal_year(end):
    annual = period(date(2024, 3, 31), end, frequency="annual")
    result = resolve_cash_flows(quarters(WEEK_ENDS[:-1] + (end,))[-4:] + annual,
                                cutoff(DECISION), NEGATIVE)
    assert result.rows == annual


def test_same_end_annual_cannot_replace_a_different_inferred_span():
    rows = quarters()
    annual = period(date(2024, 3, 30), WEEK_ENDS[-1], frequency="annual")
    assert resolve_cash_flows(annual + rows, cutoff(DECISION), NEGATIVE).rows == rows
    broken = rows[:-1] + (variant(rows[-1], "no-sign", context={"basis": None}),)
    assert_unavailable(annual + broken, WEEK_ENDS[-1], "span|convention|basis")


def test_newer_partial_period_uses_the_previous_complete_annual_window():
    annual = company_inputs(False)[0].rows
    newest = quarters()[-2:]
    result = resolve_cash_flows(annual + newest, cutoff(DECISION), NEGATIVE)
    assert result.rows == annual
    assert (result.period_start, result.period_end) == (date(2023, 1, 1), date(2023, 12, 31))


def test_newer_rolling_window_wins_only_once_its_filing_is_complete():
    rows = quarters((date(2023, 12, 30),) + WEEK_ENDS)
    amendment = tuple(variant(item, "amendment", published_at=utc(DECISION, 19))
                      for item in rows[-2:])
    reports = rows[:-1] + amendment
    earlier = cutoff(DECISION).model_copy(update={"evaluated_at": utc(DECISION, 18)})
    previous = resolve_cash_flows(reports, earlier, NEGATIVE)
    latest = resolve_cash_flows(reports, cutoff(DECISION), NEGATIVE)
    assert previous.rows == rows[:-2]
    assert (previous.period_start, previous.period_end) == (date(2023, 12, 31), WEEK_ENDS[-2])
    assert latest.rows == rows[2:-2] + amendment
    assert (latest.period_start, latest.period_end) == (date(2024, 3, 31), WEEK_ENDS[-1])


def test_same_source_revision_reclassifies_only_its_own_reporting_period():
    ends = (date(2023, 6, 24), date(2023, 9, 23), date(2023, 12, 30)) + WEEK_ENDS
    rows = quarters(ends)
    shared_id = "quarter_history_filing"
    earlier_quarters = rows[:6] + tuple(variant(item, "shared", source_record_id=shared_id)
                                        for item in rows[6:10])
    revised_q2 = tuple(variant(
        item, "ytd_revision", published_at=utc(DECISION, 19),
        context={"frequency": "year_to_date", "period_start": date(2024, 3, 31)},
    ) for item in earlier_quarters[-2:])
    reports = earlier_quarters + rows[10:] + revised_q2
    earlier = cutoff(DECISION).model_copy(update={"evaluated_at": utc(DECISION, 18)})
    assert resolve_cash_flows(reports, earlier, NEGATIVE).rows == reports[6:14]
    result = resolve_cash_flows(reports, cutoff(DECISION), NEGATIVE)
    assert result.rows == earlier_quarters[:8]
    assert (result.period_start, result.period_end) == (date(2023, 6, 25), WEEK_ENDS[1])


@pytest.mark.parametrize(("ocf", "capex"), [("61", "-20"), ("60", "-21"), ("61", "-21")])
def test_same_span_totals_must_reconcile_at_the_cutoff(ocf, capex):
    rows = quarters()
    end = WEEK_ENDS[-1]
    annual = period(date(2024, 3, 31), end, frequency="annual", ocf="60", capex="-20")
    revised = tuple(variant(item, "revised", published_at=utc(DECISION, 19), value=Decimal(value))
                    for item, value in zip(annual, (ocf, capex), strict=True))
    reports = company_inputs(False)[0].rows + rows + annual + revised
    earlier = cutoff(DECISION).model_copy(update={"evaluated_at": utc(DECISION, 18)})
    assert resolve_cash_flows(reports, earlier, NEGATIVE).rows == rows
    assert_unavailable(reports, end, "annual.*quarter.*totals|totals.*conflict")


@pytest.mark.parametrize("partial", ["annual", "quarter"])
@pytest.mark.parametrize(("missing_metric", "ocf", "capex", "conflicting_metric"), [
    ("capital_expenditures", "75", "-20", "operating_cash_flow"),
    ("operating_cash_flow", "60", "-25", "capital_expenditures"),
])
def test_each_full_component_reconciles_with_the_other_component_missing(
    partial, missing_metric, ocf, capex, conflicting_metric
):
    start, end = date(2024, 3, 31), WEEK_ENDS[-1]
    quarter_rows = quarters()
    agreed = period(start, end, frequency="annual", ocf="60", capex="-20")
    disagreed = period(start, end, frequency="annual", ocf=ocf, capex=capex)
    if partial == "annual":
        agreed = tuple(item for item in agreed if item.metric_id != missing_metric)
        disagreed = tuple(item for item in disagreed if item.metric_id != missing_metric)
        selected = quarter_rows
    else:
        quarter_rows = tuple(item for item in quarter_rows
                             if (item.observation_date, item.metric_id) != (WEEK_ENDS[2], missing_metric))
        selected = agreed

    earlier = company_inputs(False)[0].rows
    reports = earlier + quarter_rows + disagreed
    assert_unavailable(reports, end, f"totals conflict.*{conflicting_metric}")
    result = resolve_cash_flows(earlier + quarter_rows + agreed, cutoff(DECISION), NEGATIVE)
    assert (result.period_start, result.period_end) == (start, end)
    assert (result.operating_cash_flow, result.capex_spending) == (Decimal(60), Decimal(20))
    assert all(actual is expected for actual, expected in zip(result.rows, selected, strict=True))


def test_complementary_partial_representations_cannot_supply_one_trailing_result():
    start, end = date(2024, 3, 31), WEEK_ENDS[-1]
    quarterly_capex = quarters()[1::2]
    annual_ocf = period(start, end, frequency="annual", ocf="60")[:1]
    assert_unavailable(quarterly_capex + annual_ocf, end, "Incomplete")


def test_fully_evidenced_component_conflict_blocks_fallback_from_two_partial_representations():
    start, end = date(2024, 3, 31), WEEK_ENDS[-1]
    quarter_ocf = quarters()[::2]
    annual_ocf = period(start, end, frequency="annual", ocf="75")[:1]
    earlier = company_inputs(False)[0].rows
    assert_unavailable(earlier + quarter_ocf + annual_ocf, end, "totals conflict.*operating_cash_flow")


def test_present_invalid_line_cannot_be_treated_as_missing_when_other_totals_agree():
    start, end = date(2024, 3, 31), WEEK_ENDS[-1]
    ocf, capex = period(start, end, frequency="annual", ocf="60", capex="-20")
    invalid = variant(capex, "invalid", value=None)
    assert_unavailable(quarters() + (ocf, invalid), end, "capital_expenditures amount")


def test_annual_fallback_cannot_cut_through_an_observed_quarter_before_a_gap():
    end = date(2025, 4, 5)
    rows = quarters(WEEK_ENDS[:-1] + (end,))
    partial = rows[:2] + rows[4:]
    same_span = period(date(2024, 3, 31), end, frequency="annual")
    different_span = period(date(2024, 4, 7), end, frequency="annual")
    assert resolve_cash_flows(partial + same_span, cutoff(DECISION), NEGATIVE).rows == same_span
    assert_unavailable(company_inputs(False)[0].rows + partial + different_span,
                       end, "annual.*boundar|annual.*overlap")


def test_contradictory_complete_window_cannot_fall_back_to_prior_window():
    rows = quarters((date(2023, 12, 30),) + WEEK_ENDS)
    bad_latest = variant(rows[-1], "conflicting_sign", value=Decimal(5))
    assert_unavailable(rows[:-1] + (bad_latest,), WEEK_ENDS[-1], "capex sign")


def test_late_end_and_unknown_or_estimated_rows_do_not_pin_the_window():
    annual = company_inputs(False)[0].rows
    later = quarters()[:2]
    unknown = tuple(variant(item, "unknown", published_at=None) for item in later)
    estimates = tuple(variant(item, "estimate", category="estimate") for item in later)
    decision = WEEK_ENDS[1] + timedelta(days=7)
    assert resolve_cash_flows(annual + later + unknown + estimates, cutoff(decision), NEGATIVE).rows == annual
    assert resolve_cash_flows(annual + unknown + estimates, cutoff(DECISION), NEGATIVE).rows == annual


@pytest.mark.parametrize("change", ["publication", "vintage"])
def test_amended_pair_enters_only_once_published_and_vintage_is_available(change):
    rows = quarters()
    amended = tuple(variant(
        item, "amended", source_record_id="amended_filing", value=Decimal(-3),
        **{f"{change}_at" if change == "vintage" else "published_at": utc(DECISION, 19)},
    ) for item in rows[-2:])
    earlier = cutoff(DECISION).model_copy(update={"evaluated_at": utc(DECISION, 18)})
    assert resolve_cash_flows(rows + amended, earlier, NEGATIVE).rows == rows
    result = resolve_cash_flows(amended + rows, cutoff(DECISION), NEGATIVE)
    assert result.rows == rows[:-2] + amended
    assert (result.operating_cash_flow, result.capex_spending) == (Decimal(42), Decimal(18))


def test_partial_amendment_cannot_mix_with_prior_vintage():
    rows = quarters()
    amendment = variant(rows[-1], "amended", source_record_id="amended_filing",
                        published_at=utc(DECISION, 19))
    assert_unavailable(rows + (amendment,), WEEK_ENDS[-1], "vintage|filing")


@pytest.mark.parametrize(("updates", "reason"), [
    ({"source_record_id": "another_filing"}, "filing"),
    ({"source_record_id": None}, "filing"),
    ({"context": {"consolidation_scope": "parent_only"}}, "scope"),
    ({"context": {"currency": "EUR"}}, "currency"),
    ({"context": {"scale": 3}}, "scale"),
    ({"context": {"accounting_standard": "ifrs"}}, "accounting"),
    ({"value": None}, "amount|value"),
], ids=["filing", "no-filing-id", "scope", "currency", "scale", "standard", "no-amount"])
def test_cash_flow_lines_must_agree_within_each_filing(updates, reason):
    rows = quarters()
    assert_unavailable(rows[:-1] + (variant(rows[-1], "changed", **updates),), WEEK_ENDS[-1], reason)


def test_scope_must_match_across_fiscal_quarters():
    rows = quarters()
    changed = tuple(variant(item, "parent", context={"consolidation_scope": "parent_only"})
                    for item in rows[2:4])
    assert_unavailable(rows[:2] + changed + rows[4:], WEEK_ENDS[2], "scope")


@pytest.mark.parametrize("scope", ["parent_only", "segment"])
def test_matching_nonconsolidated_lines_do_not_establish_issuer_scope(scope):
    rows = company_inputs(False)[0].rows
    scoped = tuple(variant(item, scope, context={"consolidation_scope": scope}) for item in rows)
    assert_unavailable(scoped, rows[0].observation_date, "scope.*issuer_consolidated", decision=END)


@pytest.mark.parametrize("premature_lines", [1, 2])
def test_filing_publication_before_fiscal_end_cannot_establish_actuals(premature_lines):
    rows = company_inputs(False)[0].rows
    end = rows[0].observation_date
    # At 02:00 UTC the session's local date still precedes the fiscal end.
    premature = tuple(variant(item, "premature", published_at=utc(end, 2))
                      for item in rows[-premature_lines:])
    assert_unavailable(rows[:-premature_lines] + premature, end, "published before.*fiscal", decision=END)


def test_premature_revision_cannot_displace_a_dated_filing():
    rows = company_inputs(False)[0].rows
    end = rows[0].observation_date
    premature = tuple(variant(item, "premature", published_at=utc(end, 2),
                              vintage_at=utc(END, 17), source_record_id="premature_filing")
                      for item in rows)
    assert resolve_cash_flows(rows + premature, cutoff(END), NEGATIVE).rows == rows


def test_same_revision_conflict_is_rejected():
    rows = quarters()
    conflict = variant(rows[-1], "conflict", value=Decimal(-6))
    assert_unavailable(rows + (conflict,), WEEK_ENDS[-1], "Conflicting")


@pytest.mark.parametrize(("context", "reason"), [
    ({"frequency": "year_to_date"}, "standalone|year.to.date"),
    ({"fiscal_period": "Q1_YTD"}, "standalone|year.to.date"),
    ({"period_start": date(2024, 9, 29)}, "standalone|overlap|period"),
    ({"period_start": date(2024, 12, 30)}, "incomplete|missing|gap"),
])
def test_ytd_overlap_or_gap_cannot_supply_standalone_quarter(context, reason):
    rows = quarters()
    changed = tuple(variant(item, "changed", context=context) for item in rows[-2:])
    assert_unavailable(rows[:-2] + changed, WEEK_ENDS[-1], reason)


def test_ineligible_prior_quarter_reports_its_fiscal_end():
    rows = quarters()
    unknown = tuple(variant(item, "unknown", context={"vintage_coverage": "unknown"})
                    for item in rows[2:4])
    assert_unavailable(rows[:2] + unknown + rows[4:], WEEK_ENDS[2], "unknown historical availability")


@pytest.mark.parametrize(("basis", "amount", "sign"), [
    (None, "-5", NEGATIVE),
    (POSITIVE, "-5", NEGATIVE),
    (POSITIVE, "-5", POSITIVE),
    (NEGATIVE, "5", NEGATIVE),
    (NEGATIVE, "-5", "unknown"),
])
def test_capex_requires_evidenced_convention_and_consistent_amount(basis, amount, sign):
    end = WEEK_ENDS[-1]
    rows = period(date(2024, 3, 31), end, frequency="annual", sign=basis, capex=amount)
    assert_unavailable(rows, end, "capex.*(convention|basis|sign)", sign=sign)


def test_positive_convention_preserves_zero_spending_and_negative_operating_cash_flow():
    end = WEEK_ENDS[-1]
    rows = period(date(2024, 3, 31), end, frequency="annual", sign=POSITIVE, ocf="-5", capex="0")
    result = resolve_cash_flows(rows, cutoff(DECISION), POSITIVE)
    assert (result.operating_cash_flow, result.capex_spending) == (Decimal(-5), Decimal(0))


def test_decimal_sums_and_capex_normalization_ignore_ambient_context():
    amounts = ("9e37", "1e-38", "-9e37", "0")
    spending = ("-9e37", "-1e-38", "0", "0")
    rows = tuple(variant(item, "exact", value=Decimal(value)) for item, value in zip(
        quarters(), (value for pair in zip(amounts, spending, strict=True) for value in pair), strict=True,
    ))
    with localcontext(prec=1, Emin=-1, Emax=1) as context:
        context.traps[Inexact] = True
        result = resolve_cash_flows(rows, cutoff(DECISION), NEGATIVE)
    assert result.operating_cash_flow == Decimal("1e-38")
    assert result.capex_spending == Decimal("9" + "0" * 37 + "." + "0" * 37 + "1")
