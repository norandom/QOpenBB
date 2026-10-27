"""Generate offline gallery assets from explicitly identified retained captures."""
import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
from urllib.parse import urlsplit

from qopenbb_ci.gallery_projection import RETROSPECTIVE, project_data
from qopenbb_ci.gallery_templates import build_catalog


CONTRACT_SHA256 = "c54619720b96fed6c29c09fc1e1f866867a2f9707f875bf1341360dc4a383d79"


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def canonical(value):
    return (json.dumps(value, ensure_ascii=False, allow_nan=False, separators=(",", ":")) + "\n").encode()


def verified_raw(root, relative, expected):
    path = root / relative.replace("\\", "/")
    payload = path.read_bytes()
    if hashlib.sha256(payload).hexdigest() != expected:
        raise ValueError("retained source SHA-256 mismatch")
    rows = json.loads(payload)
    if not isinstance(rows, list) or not rows:
        raise ValueError("retained source must be a nonempty row array")
    return rows


def source_record(source_id, provenance, parameters):
    timestamp = provenance["retrieved_at_utc"]
    if datetime.fromisoformat(timestamp).tzinfo is None:
        raise ValueError("source retrieval timestamp must retain timezone")
    endpoint = provenance["endpoint"]
    url = urlsplit(endpoint)
    if (url.scheme != "https" or url.netloc != "financialmodelingprep.com" or url.query or url.fragment
            or url.path not in ("/stable/historical-price-eod/full", "/stable/income-statement")):
        raise ValueError("unexpected or credential-bearing source endpoint")
    return {"id": source_id, "provider": "FMP", "endpoint": endpoint, "parameters": parameters,
            "retrievedAt": timestamp, "sha256": provenance["raw_sha256"], "limitations": [RETROSPECTIVE]}


def load_inputs(contract_path, sources_path, fundamentals_path, root):
    if hashlib.sha256(contract_path.read_bytes()).hexdigest() != CONTRACT_SHA256:
        raise ValueError("chart-state fixture differs from reviewed HG0 contract")
    contract = read_json(contract_path)
    provenance = read_json(sources_path)
    prices, sources = {}, []
    for item in provenance["prices"]:
        symbol = item["symbol"]
        if symbol not in contract["companies"] or symbol in prices:
            raise ValueError("unexpected or duplicate price symbol")
        parameters = {key: item["parameters"][key] for key in ("symbol", "from", "to")}
        if parameters != {"symbol": symbol, "from": "2024-09-30", "to": "2025-01-31"}:
            raise ValueError("price capture parameters differ from frozen window")
        prices[symbol] = verified_raw(root, item["raw_path"], item["raw_sha256"])
        sources.append(source_record("fmp-prices-" + symbol, item, parameters))
    if set(prices) != set(contract["companies"]):
        raise ValueError("missing required equity source")
    fundamentals = read_json(fundamentals_path)
    parameters = {key: fundamentals["parameters"][key] for key in ("symbol", "period", "limit")}
    if parameters != {"symbol": "AAPL", "period": "quarter", "limit": "40"}:
        raise ValueError("income source differs from reviewed capture")
    income = verified_raw(root, fundamentals["source_raw_path"], fundamentals["raw_sha256"])
    sources.append(source_record("fmp-income-AAPL", fundamentals, parameters))
    order = {"fmp-prices-" + symbol: index for index, symbol in enumerate(contract["companies"])}
    sources.sort(key=lambda source: order.get(source["id"], len(order)))
    return contract, prices, income, sources


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chart-state", type=Path, required=True)
    parser.add_argument("--sources", type=Path, required=True)
    parser.add_argument("--fundamentals", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)
    try:
        contract, prices, income, sources = load_inputs(args.chart_state, args.sources, args.fundamentals, args.root)
        outputs = {"data.json": project_data(contract, prices, income, sources), "catalog.json": build_catalog(contract)}
        encoded = {name: canonical(value) for name, value in outputs.items()}
        args.output.mkdir(parents=True, exist_ok=True)
        for name, payload in encoded.items():
            (args.output / name).write_bytes(payload)
            print(name + " sha256=" + hashlib.sha256(payload).hexdigest())
    except (OSError, KeyError, TypeError, ValueError) as exc:
        parser.exit(1, "Gallery generation failed: " + str(exc) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
