"""Provision packaged Workspace Apps into the bootstrap administrator's account."""

import fcntl
from http.client import HTTPConnection, HTTPException
import json
import os
from pathlib import Path
import sys
import tempfile
from urllib.parse import urlsplit
from uuid import UUID

from provision_render import ProvisionError, app_template_id, make_dashboard, seed_id


SOURCES = "/api/pro/data-connectors/api-source"
DASHBOARDS = "/api/pro/dash/sync"


def request(path, *, data=None, token=None):
    # A fixed local transport avoids proxy settings and credential-bearing redirects.
    connection = HTTPConnection("127.0.0.1", int(os.environ.get("PORT", "3000")), timeout=30)
    headers = {"Accept": "application/json"}
    if data is not None:
        headers["Content-Type"] = "application/json"
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        connection.request("POST" if data is not None else "GET", path,
                           json.dumps(data) if data is not None else None, headers)
        response = connection.getresponse()
        if not 200 <= response.status < 300:
            message = f"Workspace route {path} returned HTTP {response.status}"
            if path == "/api/pro/login" and response.status in (400, 401, 403):
                message += ". Supply the current bootstrap administrator login in the deployment environment"
            if path == "/api/pro/login" and response.status == 429:
                message += ". Wait a minute for the login limit to reset and rerun setup"
            raise ProvisionError(message)
        return json.load(response)
    except (OSError, HTTPException, UnicodeError, ValueError):
        raise ProvisionError(f"Could not read a JSON response from Workspace route {path}") from None
    finally:
        connection.close()


def bootstrap_values(data_dir):
    return dict(line.split("=", 1) for line in
                  (data_dir / "secrets.env").read_text(encoding="utf-8").splitlines()
                  if "=" in line)


def login(values):
    email = values.get("OPENBB_ADMIN_EMAIL")
    password = values.get("OPENBB_ADMIN_PASSWORD")
    if not email or not password:
        raise ProvisionError("Workspace bootstrap credentials are unavailable")
    result = request("/api/pro/login", data={
        "email": email, "password": password, "source": "pro", "remember": False,
    })
    if not result.get("access_token") or not result.get("uuid"):
        raise ProvisionError("The Workspace bootstrap administrator did not receive a session")
    return str(UUID(result["uuid"])), result["access_token"]


def source_for(token, owner, url):
    sources = request(SOURCES, token=token)
    for source in sources:
        if source["url"].rstrip("/") != url or source.get("vendorApp"):
            continue
        if source.get("endpointHeaders"):
            raise ProvisionError(
                "The existing QOpenBB data connection has custom headers or query parameters. "
                "Use an unmodified connection for the bundled /data endpoint before rerunning setup"
            )
        return source

    source_id = seed_id(owner, "data-source")
    names = {source["name"] for source in sources}
    name = "QOpenBB Data"
    suffix = 2
    while name in names:
        name = f"QOpenBB Data ({suffix})"
        suffix += 1
    if any(source["id"] == source_id for source in sources):
        raise ProvisionError("The QOpenBB data connection has a different URL in Workspace")
    request(f"{SOURCES}/{source_id}", token=token,
            data={"name": name, "url": url, "endpointHeaders": []})
    for source in request(SOURCES, token=token):
        if source["id"] == source_id and source["url"].rstrip("/") == url:
            return source
    raise ProvisionError("Workspace did not persist the QOpenBB data connection")


def save_apps(token, owner, bundled, previously_seeded):
    owned = request(DASHBOARDS + "/owned", token=token)["owned"]
    contents = {key: item["content"] for key, item in owned.items() if item.get("content")}
    roots = [(key, item) for key, item in contents.items() if item.get("isRoot")]
    root_id, root = roots[0] if roots else (seed_id(owner, "root"), None)
    if root is None:
        root = {"index": root_id, "name": "root", "isRoot": True,
                "isFolder": True, "children": [], "data": {"name": "root"}}
    known = {item.get("data", {}).get("templateId") for item in contents.values()}
    updates = {}
    for template, catalog, source in bundled:
        name = template["name"]
        dashboard_id = seed_id(owner, "app/" + name)
        if name in previously_seeded or dashboard_id in contents or app_template_id(source, name) in known:
            continue
        updates[dashboard_id] = make_dashboard(template, dashboard_id, catalog, source, root_id)
    if not updates:
        return 0
    new_root = {**root, "children": list(dict.fromkeys([*root["children"], *updates]))}
    request(DASHBOARDS, token=token, data={"items": {**updates, root_id: new_root}})
    saved = request(DASHBOARDS + "/owned", token=token)["owned"]
    saved_children = saved.get(root_id, {}).get("content", {}).get("children", [])
    if any(key not in saved or key not in saved_children for key in updates):
        raise ProvisionError("Workspace did not persist all seeded dashboards")
    return len(updates)


def verify_origin_migration(token, previous_origin):
    former_base = previous_origin + "/data"
    sources = request(SOURCES, token=token)
    owned = request(DASHBOARDS + "/owned", token=token)["owned"]
    widgets = (
        widget
        for item in owned.values()
        for widget in (item.get("content") or {}).get("data", {}).get("widgets", [])
    )
    if any(source["url"].rstrip("/") == former_base for source in sources) or any(
        (widget.get("endpoint") or {}).get("url", "").startswith(former_base + "/")
        for widget in widgets
    ):
        raise ProvisionError(
            "PUBLIC_URL changed and the administrator still has a data connection or dashboard "
            "widget using the previous origin. Restore the original PUBLIC_URL or migrate those "
            "URLs to the new origin and rerun setup"
        )


def provision(data_dir):
    origin = os.environ.get("PUBLIC_URL", "").rstrip("/")
    public = urlsplit(origin)
    if (public.scheme not in {"http", "https"} or not public.hostname or public.username
            or public.password or public.path or public.query or public.fragment):
        raise ProvisionError("PUBLIC_URL must be the browser-facing HTTP(S) origin")

    receipt = data_dir / "state" / "qopenbb-apps-seeded-v1.json"
    previous = json.loads(receipt.read_text()) if receipt.exists() else {}
    apps = request("/data/apps.json")
    if not isinstance(apps, list) or not apps:
        raise ProvisionError("Workspace did not return the packaged data Apps")
    bootstrap = bootstrap_values(data_dir)
    credentials_stat = (data_dir / "secrets.env").stat()
    identities = {
        label: os.environ.get(f"QOPENBB_SETUP_{label}")
        for label in ("DATA_IMAGE", "MODEL_IMAGE", "WORKSPACE_CONTAINER", "MODEL_CONTAINER")
    }
    fingerprint = {
        "dataApps": sorted(app["name"] for app in apps), "origin": origin,
        "identities": identities, "admin": bootstrap.get("OPENBB_ADMIN_EMAIL"),
        "bootstrapMtime": credentials_stat.st_mtime_ns,
    }
    previous_origin = previous.get("fingerprint", {}).get("origin")
    if all(identities.values()) and fingerprint == previous.get("fingerprint"):
        print(f'Workspace Apps previously provisioned ({previous["count"]}).')
        return
    owner, token = login(bootstrap)
    if previous.get("owner") == owner and previous_origin and previous_origin != origin:
        verify_origin_migration(token, previous_origin)
    previously_seeded = set(previous.get("apps", [])) if previous.get("owner") == owner else set()
    modeling = request("/modeling/v1/models", token=token)
    if not isinstance(modeling.get("models"), list) or not modeling["models"]:
        raise ProvisionError("Workspace returned no registered modeling descriptors")
    catalog = request("/data/widgets.json")
    model_apps = request("/modeling/v1/apps.json", token=token)
    model_catalog = request("/modeling/v1/widgets.json", token=token)
    if not isinstance(catalog, dict) or not catalog:
        raise ProvisionError("Workspace did not return the packaged data catalog")
    if not isinstance(model_apps, list) or not model_apps or "qopenbb_saved_model_output" not in model_catalog:
        raise ProvisionError("Workspace did not return the packaged modeling catalog")
    all_apps = [*apps, *model_apps]
    if len({app["name"] for app in all_apps}) != len(all_apps):
        raise ProvisionError("The packaged catalog contains duplicate App names")
    names = {app["name"] for app in all_apps}
    created = 0
    if names - previously_seeded:
        source = source_for(token, owner, origin + "/data")
        # The modeling renderer authenticates with the active user's Workspace session.
        modeling_source = {"id": "qopenbb-modeling", "name": "QOpenBB Modeling", "url": origin + "/modeling/v1"}
        bundled = [(app, catalog, source) for app in apps]
        bundled += [(app, model_catalog, modeling_source) for app in model_apps]
        created = save_apps(token, owner, bundled, previously_seeded)
    # Preserve intentional deletions while allowing new catalog entries on upgrades.
    with tempfile.NamedTemporaryFile(mode="w", dir=receipt.parent, delete=False) as pending:
        json.dump({"owner": owner, "apps": sorted(previously_seeded | names),
                   "count": len(names), "fingerprint": fingerprint}, pending)
        pending.flush()
        os.fsync(pending.fileno())
    Path(pending.name).replace(receipt)
    print(f"Workspace Apps ready ({created} added, {len(all_apps) - created} existing). Modeling connection verified.")


def main():
    data_dir = Path(os.environ.get("DATA_DIR", "/data"))
    try:
        lock_path = data_dir / "state" / "qopenbb-setup.lock"
        with os.fdopen(os.open(lock_path, os.O_CREAT | os.O_RDWR, 0o600), "r+") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            provision(data_dir)
    except ProvisionError as error:
        sys.exit(f"Workspace provisioning failed. {error}")
    except OSError:
        sys.exit("Workspace provisioning failed. Bootstrap state is not accessible.")
    except (AttributeError, KeyError, TypeError, ValueError):
        sys.exit("Workspace provisioning failed. The released Workspace response did not match the setup contract.")


if __name__ == "__main__":
    main()
