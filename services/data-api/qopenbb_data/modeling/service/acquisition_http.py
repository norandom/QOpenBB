"""Stdlib HTTP worker for cancellable data API acquisition."""

import asyncio
import sys
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import HTTPRedirectHandler, ProxyHandler, Request, build_opener

MAX_RESPONSE_BYTES = 2 * 1024 * 1024


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
    if process.returncode == 3:
        raise ValueError("Data API response exceeds the byte limit.")
    if process.returncode:
        raise OSError("Data API request failed.")
    return body


def _read(url: str) -> bytes:
    opener = build_opener(ProxyHandler({}), _NoRedirect())
    request = Request(url, headers={"Accept": "application/json", "Accept-Encoding": "identity"})
    with opener.open(request, timeout=30) as response:
        if response.status != 200:
            raise OSError("Unexpected data API status.")
        return response.read(MAX_RESPONSE_BYTES + 1)


def _main() -> int:
    try:
        body = _read(sys.argv[1])
    except HTTPError as error:
        return 2 if error.code == 404 else 1
    except (OSError, ValueError):
        return 1
    if len(body) > MAX_RESPONSE_BYTES:
        return 3
    sys.stdout.buffer.write(body)
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
