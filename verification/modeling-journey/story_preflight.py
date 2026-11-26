"""Exercise entitled research story inputs through an isolated Workspace candidate."""

import json
import os
import re
import sys
from datetime import UTC, datetime
from decimal import Context, InvalidOperation, localcontext
from ipaddress import ip_address
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, ProxyHandler, Request, build_opener

from story_preflight_evidence import (
    CALENDAR, DECISION, END, REVISION, START, PreflightFailure, digest, require,
    verify_comparison, verify_context,
)

ROOT = Path(__file__).resolve().parents[2]
PAIRS = (("DBC", "XLK"), ("GLD", "XLK"), ("DBC", "VGT"))
API = "/modeling/v1"
MAX_BYTES = 8 * 1024 * 1024


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, msg, headers, newurl):
        return None


class Candidate:
    def __init__(self, origin):
        parsed = urlsplit(origin)
        require(parsed.scheme == "http" and not parsed.username and not parsed.password
                and not parsed.query and not parsed.fragment and parsed.path in ("", "/")
                and parsed.port and ip_address(parsed.hostname).is_loopback,
                "STORY_ORIGIN must use a loopback IP and explicit HTTP port")
        self.origin = origin.rstrip("/")
        self.opener = build_opener(ProxyHandler({}), NoRedirect())
        self.token = None

    def exchange(self, path, payload=None, *, error_expected=None):
        headers = {"Accept": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        if payload is not None:
            headers["Content-Type"] = "application/json"
        request = Request(self.origin + path, data=None if payload is None else json.dumps(payload).encode(),
                          headers=headers)
        try:
            with self.opener.open(request, timeout=45) as response:
                raw = response.read(MAX_BYTES + 1)
                require(len(raw) <= MAX_BYTES, "Candidate response exceeds verification bounds")
                require(error_expected is None, "Candidate accepted a negative acquisition request")
                return json.loads(raw)
        except HTTPError as exc:
            with exc:
                raw = exc.read(MAX_BYTES + 1)
            if exc.code == error_expected:
                require(len(raw) <= MAX_BYTES, "Candidate error exceeds verification bounds")
                return json.loads(raw)
            safe_codes = {"acquisition_unavailable", "entitlement", "missing_data", "timeout", "invalid_response"}
            try:
                code = json.loads(raw).get("code")
            except (ValueError, AttributeError):
                code = None
            suffix = f" ({code})" if isinstance(code, str) and code in safe_codes else ""
            raise PreflightFailure(f"Candidate returned HTTP {exc.code}{suffix} for {path}") from None

    def saved_run(self, request):
        submitted = self.exchange(f"{API}/evaluations", request)
        run_id = submitted["run_id"]
        require(re.fullmatch(r"[A-Za-z0-9._-]{1,160}", run_id) and run_id not in (".", ".."),
                "Unexpected modeling run ID")
        saved = self.exchange(f"{API}/runs/{run_id}")
        require(digest(saved) == digest(submitted), "Reopened run differs from submission")
        return saved


def selection(candidate):
    apps = candidate.exchange("/data/apps.json")
    matches = [item for item in apps if item.get("name") == "Commodities versus Technology"]
    require(len(matches) == 1, "Packaged research story is missing or duplicated")
    widgets = matches[0]["tabs"]["Research"]["layout"]
    require(len(widgets) == 1 and widgets[0]["i"] == "research_story", "Packaged renderer binding differs")
    chosen = widgets[0]["state"]["storage"]["researchStory"]["selection"]
    require(chosen == {"commodity_symbol": PAIRS[0][0], "technology_symbol": PAIRS[0][1],
                       "observation_date": END}, "Packaged research story default selection differs")
    return chosen


def request_for(name, cutoff, pair=PAIRS[0]):
    fixtures = ROOT / "contracts/consumers/research-stories/runs.v1.json"
    payload = json.loads(fixtures.read_bytes())["requests"][name]
    replacements = {"schedule_revision": REVISION, "left_proxy": pair[0], "right_proxy": pair[1]}
    for item in payload["assumptions"]["assumptions"]:
        key = item["assumption_id"]
        if key in replacements:
            item["value"] = replacements[key]
    payload["assumptions"]["effective_date"] = "2026-01-01"
    acquisition = payload["acquisition"]
    acquisition["parameters"] = [[key, replacements.get(key, value)] for key, value in acquisition["parameters"]]
    acquisition["cutoff"] = cutoff.copy()
    return payload


def check_rejections(candidate, cutoff):
    reversed_roles = request_for("comparison", cutoff)
    for item in reversed_roles["assumptions"]["assumptions"]:
        if item["assumption_id"] == "left_proxy":
            item["value"] = "XLK"
        elif item["assumption_id"] == "right_proxy":
            item["value"] = "DBC"
    wrong_dataset = request_for("comparison", cutoff)
    wrong_dataset["acquisition"]["dataset_id"] = "story.dfii10"
    for request in (reversed_roles, wrong_dataset):
        rejection = candidate.exchange(f"{API}/evaluations", request, error_expected=422)
        require(rejection.get("fields") == [{"path": ["acquisition"], "code": "unsupported_acquisition"}],
                "Unexpected rejection for unsupported acquisition")


def run_preflight(candidate, evidence):
    token = candidate.exchange("/api/pro/login", {
        "email": os.environ["OPENBB_ADMIN_EMAIL"], "password": os.environ["OPENBB_ADMIN_PASSWORD"],
    })["access_token"]
    require(isinstance(token, str) and token, "Workspace login did not return a bearer token")
    candidate.token = token
    evidence["catalog_selection"] = selection(candidate)
    cutoff = {"observation_date": END, "decision_at": DECISION,
              "evaluated_at": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
              "session_timezone": "America/New_York"}
    evidence["cutoff"] = cutoff
    check_rejections(candidate, cutoff)
    evidence["rejected_acquisitions"] = ["reversed_assumptions", "wrong_dataset"]
    for pair in PAIRS:
        request = request_for("comparison", cutoff, pair)
        saved = candidate.saved_run(request)
        evidence["comparisons"].append(verify_comparison(saved, request))
    request = request_for("regime", cutoff)
    context = verify_context(candidate.saved_run(request), request)
    evidence["dfii10"] = context
    require(context["context_status"] == "withheld", "Expected the qualified November 13 withheld outcome")
    reports = evidence["comparisons"]
    require(all(report["session_sha256"] == context["session_sha256"] for report in reports),
            "Saved runs must share the same schedule")
    require(len({report["run_id"] for report in [*reports, context]}) == 4, "Saved run IDs are not distinct")


def main():
    path = Path(os.environ["STORY_EVIDENCE"])
    evidence = {
        "schema_version": 1, "status": "failed", "calendar_id": CALENDAR,
        "schedule_revision": REVISION, "start_date": START, "end_date": END, "comparisons": [],
    }
    try:
        with localcontext(Context(prec=70)):
            run_preflight(Candidate(os.environ["STORY_ORIGIN"]), evidence)
        evidence["status"] = "passed"
    except PreflightFailure as exc:
        evidence["failure"] = str(exc)
    except (KeyError, TypeError, ValueError, InvalidOperation, OSError, AttributeError) as exc:
        evidence["failure"] = f"Invalid candidate configuration, transport or wire data ({type(exc).__name__})"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(evidence, indent=2) + "\n")
    if evidence["status"] == "failed":
        print(evidence["failure"], file=sys.stderr)
        return 1
    print(f"Research story preflight passed. Evidence written to {path}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
