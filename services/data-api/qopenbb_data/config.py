"""Server-only OpenBB settings; credentials never touch a settings file."""
import os


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
