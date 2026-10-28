"""Full frontend inputs; runtime acceptance belongs to later tasks."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORKSPACE = ROOT / "vendor/workspace"


def test_frontend_uses_owned_frozen_inputs():
    frontend = (WORKSPACE / "lite/Dockerfile").read_text().split("# Backend base")[0]
    assert "bun install --frozen-lockfile" in frontend
    assert "safe-chain-verify" in frontend
    assert "SAFE_CHAIN_MINIMUM_PACKAGE_AGE_HOURS=48" in frontend
    assert "ARG OPENBB_IMAGE_VARIANT=full" in frontend
    assert "ARG VITE_RELEASE_VERSION" in frontend
    assert "terminalpro/package-lock.json" not in frontend
    assert "grep " not in frontend
    assert "COPY lite/frontend.full.env" in frontend


def test_build_fonts_are_repository_assets():
    html = (WORKSPACE / "terminalpro/index.html").read_text()
    config = (WORKSPACE / "terminalpro/vite.config.ts").read_text()
    assert "fonts.googleapis.com" not in html
    assert "fonts.gstatic.com" not in html
    assert "webfontDownload" not in config
    for name in ("Inter.var.woff2", "Roboto-VariableFont_wdth,wght.ttf"):
        assert (WORKSPACE / "terminalpro/public/assets/fonts" / name).is_file()


def test_backend_uses_locked_uv_and_readable_application_source():
    recipe = (WORKSPACE / "lite/Dockerfile").read_text()
    assert "safe-chain uv sync --locked --no-dev --no-install-project" in recipe
    assert "COPY backend/pyproject.toml backend/uv.lock ./" in recipe
    assert 'UV_PROJECT_ENVIRONMENT="/opt/.venv"' in recipe
    assert "UV_PYTHON_DOWNLOADS=never" in recipe
    for package in ("api", "routers", "utilities"):
        assert f"COPY --chown=appuser:appuser backend/{package} ./{package}" in recipe
    for removed in ("Cython", "cython", "poetry", "setup_compile", "build_ext", "backend-compile"):
        assert removed not in recipe
    assert "uvx /usr/local/bin/" in recipe


def test_embedded_valkey_preserves_protocol_and_storage_contract():
    import configparser

    recipe = (WORKSPACE / "lite/Dockerfile").read_text()
    source = "https://download.valkey.io/releases/valkey-9.0.7-jammy-x86_64.tar.gz"
    checksum = "bf0f19982dd464ea111617608a90f1a6eaad2c9c59b2e289cbc1591129f6d2e4"
    assert f"ADD --checksum=sha256:{checksum} {source} /tmp/valkey.tar.gz" in recipe.splitlines()
    assert "redis-server" not in recipe
    assert "libssl3 libsystemd0" in recipe
    assert "/usr/local/share/licenses/valkey/LICENSE" in recipe
    assert "valkey-9.0.7-jammy-x86_64/share/LICENSE" in recipe
    assert "valkey-9.0.7-jammy-x86_64/bin/valkey-cli" in recipe
    assert "EXPOSE 6379" not in recipe
    config = configparser.ConfigParser(interpolation=None)
    config.read(WORKSPACE / "lite/supervisord.conf")
    server = config["program:redis"]
    assert server["command"] == (
        "/usr/local/bin/valkey-server --dir /data/redis --save 60 1 "
        "--loglevel warning --bind 127.0.0.1 --port 6379"
    )
    assert server["user"] == "appuser"
    assert server["autostart"] == server["autorestart"] == "true"
    assert server["priority"] == "10"
