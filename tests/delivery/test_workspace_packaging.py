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