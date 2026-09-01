from app.core.config import Settings


def test_settings_defaults():
    settings = Settings()
    assert settings.APP_NAME == "Nugi Content Factory"
    assert settings.LLM_PROVIDER == "mock"
    assert settings.IMAGE_PROVIDER == "mock"
    assert settings.STORAGE_PROVIDER == "local"
    assert len(settings.cors_origins) > 0


def test_storage_path_resolution(tmp_path):
    settings = Settings(STORAGE_BASE_DIR=str(tmp_path / "custom_storage"))
    resolved = settings.storage_path
    assert resolved.exists()
    assert resolved.is_dir()
