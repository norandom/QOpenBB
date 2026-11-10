"""Acceptance-only aiohttp send admission, embedded before the packaged API starts.

This instruments attempted sends, not provider-billed requests. The controller must
stop and verify the owned API exited before extracting this sole ledger for reopen.
Never use this helper as a production quota service or reset a failed run.
"""

import hashlib
import inspect
import json
import os
from pathlib import Path
import re
import threading
from urllib.parse import parse_qsl, urlsplit

VERSION = 1
MAXIMA = {"fmp": 80, "fred": 16}
LEDGER = "/tmp/qopenbb-financial-budget.json"
DENIALS = ("destination", "ledger", "persistence", "exhausted", "process")


class BudgetDenied(RuntimeError):
    """Fixed messages deliberately exclude request and filesystem details."""


def denied(category):
    raise BudgetDenied("financial budget denied: " + category) from None


def counts_checked(counts):
    if not isinstance(counts, dict) or counts.keys() != MAXIMA.keys():
        denied("ledger")
    if any(type(counts[k]) is not int or not 0 <= counts[k] <= MAXIMA[k] for k in MAXIMA):
        denied("ledger")
    return dict(counts)


def checked_snapshot(text, run, minimum):
    """Validate an extracted stopped-container record; no fresh allowance fallback."""
    try:
        record = json.loads(text)
        valid = (set(record) == {"version", "run", "phase", "pid", "maxima", "counts", "denials"}
                 and type(record["version"]) is int and record["version"] == VERSION and record["run"] == run
                 and record["phase"] in ("initial", "reopen") and record["maxima"] == MAXIMA
                 and type(record["pid"]) is int and record["pid"] > 0
                 and set(record["denials"]) == set(DENIALS)
                 and all(type(n) is int and n >= 0 for n in record["denials"].values()))
        if not valid:
            denied("ledger")
        counts = counts_checked(record["counts"])
        prior = counts_checked(minimum)
        if any(counts[k] < prior[k] for k in MAXIMA):
            denied("ledger")
        return record
    except (ValueError, TypeError, KeyError):
        denied("ledger")


def destination(req):
    """Exact upstream scope, including redirects; credentials are never retained."""
    try:
        raw = req.url.geturl() if hasattr(req.url, "geturl") else str(req.url)
        url = urlsplit(raw)
        if (req.method != "GET" or url.scheme != "https" or url.port not in (None, 443)
                or url.username or url.password or url.fragment or getattr(req, "proxy", None)):
            denied("destination")
        pairs = parse_qsl(url.query, keep_blank_values=True, strict_parsing=True)
        query = dict(pairs)
        if len(query) != len(pairs):
            denied("destination")
        if url.hostname == "financialmodelingprep.com" and fmp_query(url.path, query):
            return "fmp"
        if url.hostname == "api.stlouisfed.org" and fred_query(url.path, query):
            return "fred"
    except (ValueError, AttributeError):
        pass
    denied("destination")


def fmp_query(path, query):
    """Freeze selected company, annual/quarterly and bounded search acquisitions."""
    if not query.get("apikey"):
        return False
    if path in ("/stable/search-name", "/stable/search-symbol"):
        return (set(query) == {"query", "limit", "apikey"}
                and query["query"] in ("Microsoft", "MSFT", "Apple", "AAP", "AAPL")
                and query["limit"] in ("5", "10", "20", "100"))
    if path == "/stable/profile":
        return set(query) == {"symbol", "apikey"} and query["symbol"] in ("AAPL", "MSFT")
    return (path == "/stable/income-statement"
            and set(query) == {"symbol", "period", "limit", "apikey"}
            and query["symbol"] in ("AAPL", "MSFT")
            and query["period"] in ("annual", "quarter") and query["limit"] in ("5", "10"))


def fred_query(path, query):
    if query.get("series_id") != "GDP" or query.get("file_type") != "json" or not query.get("api_key"):
        return False
    base = {"series_id", "file_type", "api_key"}
    if path == "/fred/series":
        return set(query) == base
    allowed = base | {"observation_start", "observation_end", "limit", "frequency", "aggregation_method", "units"}
    return (path == "/fred/series/observations" and set(query) <= allowed
            and all(fred_value(k, v) for k, v in query.items() if k not in base))


def fred_value(key, value):
    if key in ("observation_start", "observation_end"):
        return re.fullmatch(r"\d{4}-\d{2}-\d{2}", value) is not None
    return value in {"limit": ("100000",), "frequency": ("q",),
                     "aggregation_method": ("eop",), "units": ("lin",)}.get(key, ())


class Budget:
    def __init__(self, path, run, phase):
        if not re.fullmatch(r"[A-Za-z0-9_-]{1,100}", run) or phase not in ("initial", "reopen"):
            denied("ledger")
        self.path, self.run, self.phase = Path(path), run, phase
        self.pid, self.lock = os.getpid(), threading.Lock()
        self.minimum = {"fmp": 0, "fred": 0}
        self.poisoned = False

    def initialize(self, counts):
        """Called exactly once before app import; an existing file cannot be reset."""
        if self.path.exists() or self.path.is_symlink():
            denied("ledger")
        self.minimum = counts_checked(counts)
        self._write({"version": VERSION, "run": self.run, "phase": self.phase,
                     "pid": self.pid, "maxima": MAXIMA, "counts": self.minimum,
                     "denials": dict.fromkeys(DENIALS, 0)})

    def _write(self, record):
        temporary = self.path.with_name(self.path.name + ".pending")
        try:
            with temporary.open("x", encoding="utf-8") as stream:
                os.chmod(temporary, 0o600)
                json.dump(record, stream, sort_keys=True)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary, self.path)
            if os.name != "nt":
                directory = os.open(self.path.parent, os.O_RDONLY | os.O_DIRECTORY)
                try:
                    os.fsync(directory)
                finally:
                    os.close(directory)
        except OSError:
            self.poisoned = True
            denied("persistence")

    def reserve(self, req):
        """Synchronous durable reservation completes before original send is called."""
        with self.lock:
            if os.getpid() != self.pid or self.poisoned:
                denied("process")
            try:
                record = checked_snapshot(self.path.read_text(), self.run, self.minimum)
            except OSError:
                denied("ledger")
            if record["pid"] != self.pid or record["phase"] != self.phase:
                denied("process")
            try:
                provider = destination(req)
            except BudgetDenied:
                record["denials"]["destination"] += 1
                self._write(record)
                raise
            if record["counts"][provider] >= MAXIMA[provider]:
                record["denials"]["exhausted"] += 1
                self._write(record)
                denied("exhausted")
            record["counts"][provider] += 1
            self._write(record)
            self.minimum = dict(record["counts"])

    async def send(self, original, req, connection):
        self.reserve(req)
        return await original(req, connection)


def install_guard(run, phase, counts):
    import aiohttp
    from aiohttp import ClientRequest
    if aiohttp.__version__ != "3.14.5" or getattr(ClientRequest.send, "_financial_guard", False):
        denied("process")
    if os.environ.get("OPENBB_FRED_MAX_RETRIES") != "0":
        denied("process")
    if os.environ.get("WEB_CONCURRENCY", "1") != "1":
        denied("process")
    if (os.environ.get("UVICORN_WORKERS", "1") != "1"
            or os.environ.get("UVICORN_RELOAD", "false").lower() not in ("false", "0")):
        denied("process")
    guard = Budget(LEDGER, run, phase)
    guard.initialize(counts)
    original = ClientRequest.send

    async def bounded_send(req, connection):
        return await guard.send(original, req, connection)

    bounded_send._financial_guard = True
    ClientRequest.send = bounded_send
    return guard


def bootstrap(run, phase, counts, original):
    """Return python -c source; caller hashes this private Compose entrypoint override.

    Supply the inspected uvicorn entrypoint as ['-m', 'uvicorn', *original[1:]].
    Controller must verify image entrypoint and preserve every application argument.
    """
    counts_checked(counts)
    if (original[:2] != ["-m", "uvicorn"] or "--reload" in original
            or any(arg.startswith("--reload=") for arg in original)):
        raise ValueError("Single process uvicorn invocation required")
    if "--workers" in original and original[original.index("--workers") + 1:] [:1] != ["1"]:
        raise ValueError("Single process uvicorn invocation required")
    if any(arg.startswith("--workers=") and arg != "--workers=1" for arg in original):
        raise ValueError("Single process uvicorn invocation required")
    source = Path(inspect.getfile(bootstrap)).read_text(encoding="utf-8")
    return (source + "\nimport runpy, sys\n"
            + f"install_guard({run!r}, {phase!r}, {counts!r})\n"
            + f"sys.argv = {['uvicorn', *original[2:]]!r}\n"
            + "runpy.run_module('uvicorn', run_name='__main__')\n")


def entrypoint_override(python, run, phase, counts, inspected_entrypoint):
    expected = ["uvicorn", "qopenbb_data.app:create_app", "--factory", "--host",
                "0.0.0.0", "--port", "6900", "--no-access-log"]
    if inspected_entrypoint != expected or python not in ("python", "/usr/local/bin/python"):
        raise ValueError("Inspected packaged entrypoint required")
    code = bootstrap(run, phase, counts, ["-m", "uvicorn", *expected[1:]])
    return {"entrypoint": [python, "-c", code], "command": [],
            "sha256": hashlib.sha256(code.encode()).hexdigest()}
