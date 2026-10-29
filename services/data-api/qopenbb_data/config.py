"""Server-only OpenBB settings; credentials never touch a settings file."""
import json
import os
import re
from pathlib import Path

COVERAGE = Path(__file__).with_name("provider-coverage.json")


def financial_identity() -> dict:
    """Native source/generator revisions and the separate wrapper input hash."""
    source = os.environ.get("QOPENBB_DATA_SOURCE_REVISION", "")
    generation = os.environ.get("QOPENBB_DATA_GENERATION_REVISION", "")
    image = os.environ.get("QOPENBB_DATA_IMAGE_DIGEST") or None
    runtime_hash = os.environ.get("QOPENBB_DATA_RUNTIME_SHA256") or None
    if (not re.fullmatch(r"[0-9a-f]{40}", source)
            or not re.fullmatch(r"[0-9a-f]{40}", generation)
            or (image is not None and not re.fullmatch(r"sha256:[0-9a-f]{64}", image))
            or (runtime_hash is not None and not re.fullmatch(r"[0-9a-f]{64}", runtime_hash))):
        raise ValueError("Invalid financial runtime identity")
    return {"source_revision": source, "generation_revision": generation,
            "image_digest": image, "runtime_inputs_sha256": runtime_hash}


def coverage_index() -> dict:
    try:
        return json.loads(COVERAGE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        raise ValueError("Invalid provider coverage index") from None


def configure() -> list[str]:
    if os.environ.get("OPENBB_API_AUTH", "false").lower() not in {"false", "0", ""}:
        raise ValueError("OPENBB_API_AUTH must be false for the owner-managed origin")
    os.environ["OPENBB_API_AUTH"] = "false"
    os.environ["OPENBB_DEBUG_MODE"] = "false"
    os.environ["OPENBB_DEV_MODE"] = "false"
    os.environ["OPENBB_FRED_DISK_CACHE"] = "0"
    from openbb_core.app.model.user_settings import UserSettings
    from openbb_core.app.service.user_service import UserService

    settings = UserSettings.model_construct()
    names = {"FMP_API_KEY": "fmp_api_key", "FRED_API_KEY": "fred_api_key"}
    for variable, field in names.items():
        setattr(settings.credentials, field, os.environ.get(variable) or None)
    # The selected core reads this interface on every command, even without auth.
    # Return a private copy so command defaults cannot mutate shared state.
    UserService.read_from_file = classmethod(lambda cls, path=None: settings.model_copy(deep=True))
    UserService().default_user_settings = settings
    return [name for name in names if not os.environ.get(name)]
