"""Compare the retained observations with fresh responses via the vendor adapters."""

import asyncio
import json
import logging
import os
from pathlib import Path

from openbb_core.provider.standard_models.financial_metadata import (
    FINANCIAL_METADATA_KEY,
)
from openbb_fmp.models.cash_flow import FMPCashFlowStatementFetcher
from openbb_fmp.models.historical_market_cap import FmpHistoricalMarketCapFetcher

EVIDENCE = Path(__file__).resolve().parent


def credential():
    if key := os.environ.get("FMP_API_KEY"):
        return key
    env_file = EVIDENCE.parents[1] / ".env"
    if env_file.is_file():
        for line in env_file.read_text().splitlines():
            if line.startswith("FMP_API_KEY="):
                return line.partition("=")[2].strip().strip("\"'")
    return ""


async def observed(fetcher, params, key):
    query = fetcher.transform_query(params)
    response = await fetcher.aextract_data(query, {"fmp_api_key": key})
    data = fetcher.transform_data(query, response)
    metadata = data.metadata[FINANCIAL_METADATA_KEY]
    assert metadata["point_in_time_safe"] is False
    print(
        f"{fetcher.__name__}: {len(data.result)} rows, retrieved {metadata['retrieved_at']}"
    )
    return data.result


async def check(key):
    capture = json.loads((EVIDENCE / "aapl-fmp-capture.json").read_text())
    cash = capture["cash_flow"]
    flows = await observed(FMPCashFlowStatementFetcher, cash["query"], key)
    expected = cash["selected"]
    (annual,) = [
        row for row in flows if row.period_ending.isoformat() == expected["date"]
    ]
    assert annual.filing_date.isoformat() == expected["filingDate"]
    assert annual.accepted_date.isoformat(sep=" ") == expected["acceptedDate"]
    assert annual.reported_currency == expected["reportedCurrency"]
    assert annual.operating_cash_flow == expected["operatingCashFlow"]
    assert annual.capital_expenditure == expected["capitalExpenditure"]
    assert annual.free_cash_flow == expected["freeCashFlow"]

    market = capture["market_value"]
    window = market["query"]
    (capitalization,) = await observed(
        FmpHistoricalMarketCapFetcher,
        {
            "symbol": window["symbol"],
            "start_date": window["from"],
            "end_date": window["to"],
        },
        key,
    )
    assert capitalization.date.isoformat() == market["selected"]["date"]
    assert capitalization.market_cap == market["selected"]["marketCap"]


if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    try:
        key = credential()
        if not key:
            raise SystemExit("FMP credential missing")
        asyncio.run(check(key))
    except Exception as error:  # noqa: BLE001 - Transport errors may carry credential-bearing URLs.
        raise SystemExit(
            f"Live FMP verification failed ({type(error).__name__})."
        ) from None
    print("Both FMP adapters reproduced the retained observations.")
