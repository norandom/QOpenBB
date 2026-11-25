"""Synthetic dated inputs for factor contract examples."""

import itertools
from datetime import UTC, date, datetime, timedelta

from qopenbb_data.modeling.contracts import (
    EvaluationCutoff,
    Observation,
    ObservationTable,
)

START = date(2024, 1, 2)
HOLIDAYS = {date(2024, 1, 15), date(2024, 2, 19), date(2024, 3, 29)}
SESSIONS = tuple(
    day for offset in range(100)
    if (day := START + timedelta(days=offset)).weekday() < 5 and day not in HOLIDAYS
)[:64]
END = SESSIONS[-1]
KEYS = ("entity_id", "metric_id", "observation_date", "vintage_at")


def utc(day, hour):
    return datetime(day.year, day.month, day.day, hour, tzinfo=UTC)


def cutoff(day):
    return EvaluationCutoff(
        observation_date=day, decision_at=utc(day, 22),
        evaluated_at=utc(day + timedelta(days=30), 16),
        session_timezone="America/New_York",
    )


def table(table_id, grain, rows):
    return ObservationTable(table_id=table_id, grain=grain, keys=KEYS, nullable=False, rows=rows)


def row(entity, metric, day, value, unit, *, published_at, vintage_at=None,
        source_record_id=None, **context):
    return Observation(
        record_id=f"{entity}.{metric}.{day}", entity_id=entity, metric_id=metric,
        observation_date=day, value=value, context=dict(unit=unit, **context),
        category="raw", published_at=published_at, vintage_at=vintage_at,
        source_record_id=source_record_id,
    )


def schedule():
    return table("sessions", "One expected close per synthetic listing session", [
        row("fixture_us_listing", "session", day, "1", "session",
            published_at=utc(date(2023, 12, 1), 15))
        for day in SESSIONS
    ])


def prices(table_id, proxy, jump_close, missing):
    return table(table_id, "One split-adjusted USD close per proxy, session and vintage", [
        row(proxy, "close", day, "100" if day == START else jump_close, "price",
            published_at=utc(day, 21), currency="USD", quantity="stock",
            basis="split_adjusted_dividends_excluded")
        for day in SESSIONS if not (missing and day == END)
    ])


def yields(missing, *, unknown_availability=False):
    return table("dfii10", "One DFII10 level per observation date and vintage", [
        row("DFII10", "real_yield", day, value, "percent",
            published_at=utc(day, 21), vintage_at=utc(day, 21), quantity="rate",
            basis="treasury_constant_maturity",
            vintage_coverage="unknown" if unknown_availability and day == END else "known")
        for day, value in ((START, "1.50"), (END, "1.75")) if not (missing and day == END)
    ])


def company_inputs(missing):
    issuer = "fixture_company"
    statement_end = date(2023, 12, 31)
    statement_context = {
        "published_at": utc(date(2024, 2, 12), 17),
        "currency": "USD", "scale": 6, "quantity": "flow", "frequency": "annual",
        "period_start": date(2023, 1, 1), "period_end": statement_end,
        "consolidation_scope": "issuer_consolidated", "source_record_id": "synthetic_annual_filing_2023",
    }
    flows = table("cash_flows", "One annual filing amount per issuer, metric and vintage", [
        row(issuer, "operating_cash_flow", statement_end, "60", "currency", **statement_context),
        row(issuer, "capital_expenditures", statement_end, "-20", "currency",
            basis="cash_outflow_negative", **statement_context),
    ])
    market_value = row(
        issuer, "equity_market_value", END, "800", "currency", published_at=utc(END, 21),
        currency="USD", scale=6, quantity="stock", consolidation_scope="issuer_consolidated",
    )
    return flows, table("market_value", "One consolidated equity value per issuer and session",
                        () if missing else (market_value,))


# Returns use adjacent, nonoverlapping open-to-open intervals.
STUDY_DATES = tuple(date(2024, 6, day) for day in (3, 4, 5, 6, 7, 10, 11))


def study_inputs(missing):
    interpretations = ("rising", "rising", "rising", "falling", "falling")
    candidates = tuple(zip(STUDY_DATES[:-2], interpretations, strict=True))
    signals = table("dated_signals", "One momentum signal per proxy and decision session", [
        row("fixture_left", "momentum", day, "20", "percent", published_at=utc(day, 21))
        for day, _ in candidates
    ])
    regimes = table("dated_regimes", "One DFII10 endpoint change per decision session", [
        row("DFII10", "endpoint_change", day, "0.25" if regime == "rising" else "-0.25",
            "percentage_points", published_at=utc(day, 21), vintage_at=utc(day, 21))
        for day, regime in candidates
    ])
    intervals = itertools.pairwise(STUDY_DATES[1:])
    return_rows = [
        row(entity, "forward_return", end, value, "percent", published_at=utc(end, 15),
            period_start=start, period_end=end, basis="open_to_open")
        for (start, end), exposed in zip(intervals, ("10", "0", "-5", "-4", "12"), strict=True)
        for entity, value in (("fixture_left", exposed), ("fixture_benchmark", "0"))
        if not (missing and entity == "fixture_benchmark" and end == STUDY_DATES[4])
    ]
    return signals, regimes, table(
        "forward_returns", "One open-to-open return per entity and outcome end date", return_rows,
    )
