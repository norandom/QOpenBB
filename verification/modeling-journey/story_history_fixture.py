"""Serve two captured ETF histories with one controlled change in the closing price."""

import json
from datetime import UTC, datetime
from decimal import Decimal
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qsl, urlsplit


def history_body(histories, symbol, query):
    rows = histories[symbol]
    points = []
    for day, close in rows:
        # JSON numbers must retain the captured decimal precision.
        points.append('{"date":' + json.dumps(day) + ',"close":' + format(Decimal(close), "f") + '}')
    receipt = {
        "provider": "fmp", "dataset": "equity/price/historical",
        "retrieved_at": datetime.now(UTC).isoformat(), "effective_query": query,
        "source": {"endpoint": "historical-price-eod/full"}, "point_in_time_safe": False,
        "bounds": {"returned_count": len(rows), "truncated": False},
        "fields": {"close": {"unit": "currency/share", "scale": 1, "currency": "USD",
                             "value_origin": "provider_observation"}},
    }
    return ('{"provider":"fmp","results":[' + ",".join(points) + '],"extra":' +
            json.dumps({"results_metadata": {"__qopenbb_financial__": receipt}}) + '}').encode()


class HistoryHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlsplit(self.path)
        query = dict(parse_qsl(path.query))
        symbol = query.get("symbol")
        if path.path != "/api/v1/equity/price/historical" or query.pop("provider", None) != "fmp":
            self.send_error(404)
            return
        if symbol not in self.server.histories:
            self.send_error(404)
            return
        body = history_body(self.server.histories, symbol, query)
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 6900), HistoryHandler)
    server.histories = json.loads(Path("/controlled-history.json").read_text())
    server.serve_forever()
