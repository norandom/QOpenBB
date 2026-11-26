"""Stdlib HTTP worker for cancellable data API acquisition."""

import asyncio
import json
import sys
from urllib.error import HTTPError
from urllib.parse import urlencode, urlsplit
from urllib.request import HTTPRedirectHandler, ProxyHandler, Request, build_opener

MAX_RESPONSE_BYTES = 2 * 1024 * 1024


class ProviderDenied(PermissionError):
    """Safe classification passed across the disposable HTTP worker boundary."""

    code = "entitlement"


class ProviderRetry(OSError):
    def __init__(self, code: str):
        super().__init__("Retryable data API error.")
        self.code = code


class _NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


async def fetch(url: str, params: tuple[tuple[str, str], ...]) -> bytes:
    """Isolate blocking DNS and HTTP reads behind a killable process."""
    process = await asyncio.create_subprocess_exec(
        sys.executable, "-m", __name__, url + "?" + urlencode(params),
        stdin=asyncio.subprocess.DEVNULL,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.DEVNULL,
    )
    try:
        body, _ = await process.communicate()
    finally:
        if process.returncode is None:
            try:
                process.kill()
            except ProcessLookupError:
                pass
            await process.communicate()
    if process.returncode == 2:
        raise LookupError
    if process.returncode == 4:
        raise ProviderDenied("Data API denied access to the dataset.")
    if process.returncode in (5, 6):
        raise ProviderRetry("throttling" if process.returncode == 5 else "timeout")
    if process.returncode == 3:
        raise ValueError("Invalid data API response.")
    if process.returncode:
        raise OSError("Data API request failed.")
    return body


def _read(url: str) -> bytes:
    opener = build_opener(ProxyHandler({}), _NoRedirect())
    request = Request(url, headers={"Accept": "application/json", "Accept-Encoding": "identity"})
    with opener.open(request, timeout=30) as response:
        if response.status == 204 and urlsplit(url).path == "/api/v1/equity/price/historical":
            raise LookupError
        if response.status != 200:
            raise OSError("Unexpected data API status.")
        return response.read(MAX_RESPONSE_BYTES + 1)


def _financial_failure(error: HTTPError) -> int:
    if error.code in (401, 403, 404):
        return 2 if error.code == 404 else 4
    if urlsplit(error.url).path != "/api/v1/equity/price/historical":
        return 1
    if error.code == 429:
        return 5
    body = error.read(4097)
    if len(body) > 4096:
        return 1
    try:
        envelope = json.loads(body)
    except (ValueError, UnicodeError, RecursionError):
        return 1
    if not isinstance(envelope, dict) or envelope.get("provider") != "fmp":
        return 1
    code = envelope.get("code")
    if not isinstance(code, str):
        return 1
    return {
        (502, "authentication"): 4, (502, "entitlement"): 4, (502, "invalid_response"): 3,
        (400, "timeout"): 6, (400, "throttling"): 5,
    }.get((error.code, code), 1)


def _main() -> int:
    try:
        body = _read(sys.argv[1])
    except HTTPError as error:
        return _financial_failure(error)
    except LookupError:
        return 2
    except (OSError, ValueError):
        return 1
    if len(body) > MAX_RESPONSE_BYTES:
        return 3
    sys.stdout.buffer.write(body)
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
