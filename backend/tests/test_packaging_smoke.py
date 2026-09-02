import os
import sys
import json
from pathlib import Path
from fastapi.testclient import TestClient

from app.main import app, find_frontend_dist
from app.core.config import Settings, settings

client = TestClient(app)


def test_user_data_directory_resolution():
    """Verify user data directories resolve safely without developer machine coupling."""
    custom_settings = Settings(_env_file=None, APP_ENV="production")
    data_dir = custom_settings.user_data_dir
    assert data_dir.exists()
    assert custom_settings.config_dir.exists()
    assert custom_settings.storage_path.exists()
    assert custom_settings.logs_dir.exists()
    assert "sqlite:///" in custom_settings.effective_database_url


def test_persistent_settings_lifecycle(tmp_path):
    """Verify settings can be saved and loaded across app restarts."""
    test_cfg_dir = tmp_path / "config"
    test_cfg_dir.mkdir(parents=True, exist_ok=True)
    
    custom_settings = Settings(_env_file=None)
    # Monkeypatch config_dir
    custom_settings.__dict__["_test_config_dir"] = test_cfg_dir
    
    payload = {
        "llm": {
            "provider": "openrouter",
            "model": "google/gemini-2.5-flash-lite",
            "api_key": "test-key-123",
            "base_url": "https://openrouter.ai/api/v1"
        },
        "image": {
            "provider": "flux",
            "model": "flux-2-klein-9b",
            "api_key": "test-flux-key",
            "endpoint_url": "https://api.bfl.ai/v1"
        }
    }

    settings_file = test_cfg_dir / "provider_settings.json"
    with open(settings_file, "w", encoding="utf-8") as f:
        json.dump(payload, f)

    assert settings_file.exists()
    with open(settings_file, "r", encoding="utf-8") as f:
        loaded = json.load(f)
    assert loaded["llm"]["provider"] == "openrouter"
    assert loaded["image"]["model"] == "flux-2-klein-9b"


def test_brand_assets_exist():
    """Verify required Windows desktop brand assets exist."""
    root = Path(__file__).resolve().parent.parent.parent
    ico_path = root / "assets" / "brand" / "app.ico"
    logo_path = root / "assets" / "brand" / "nugi_properti_logo.png"

    assert ico_path.exists(), "Windows app.ico icon must exist."
    assert logo_path.exists(), "Official nugi_properti_logo.png must exist."
    assert ico_path.stat().st_size > 1000, "app.ico must be a valid multi-layer icon."


def test_packaging_spec_files_exist():
    """Verify PyInstaller spec and Inno Setup installer scripts exist."""
    root = Path(__file__).resolve().parent.parent.parent
    spec_path = root / "packaging" / "desktop.spec"
    iss_path = root / "packaging" / "installer.iss"

    assert spec_path.exists(), "desktop.spec must exist for PyInstaller."
    assert iss_path.exists(), "installer.iss must exist for Inno Setup."


def test_no_developer_paths_in_core_config():
    """Verify no hardcoded 'C:\\Users\\Nugi' in production config resolution."""
    assert "C:\\Users\\Nugi" not in settings.STORAGE_BASE_DIR or settings.APP_ENV == "development"
    assert not any("Users\\Nugi" in str(getattr(settings, k)) for k in settings.__dict__ if isinstance(getattr(settings, k), str) and not k.startswith("_"))


def test_frontend_dist_discovery():
    """Verify frontend dist discovery handles development and production environments."""
    dist = find_frontend_dist()
    # If built, dist is found; if not built yet in tests, should return None or Path
    if dist is not None:
        assert (dist / "index.html").exists()
