import app.main as main_module
from app.core.config import settings


def _mask(key: str) -> str:
    if len(key) <= 8:
        return "****"
    return f"{key[:4]}...{key[-4:]}"


def test_get_providers_returns_masked_key(client, monkeypatch):
    monkeypatch.setattr(type(settings), "save_persistent_settings", lambda self, data: None)
    monkeypatch.setattr(settings, "LLM_PROVIDER", "openai")
    monkeypatch.setattr(settings, "LLM_API_KEY", "sk-super-secret-value-123")
    monkeypatch.setattr(settings, "OPENAI_API_KEY", "sk-super-secret-value-123")

    r = client.get("/api/v1/settings/providers")
    assert r.status_code == 200
    body = r.text
    assert "sk-super-secret-value-123" not in body
    assert _mask("sk-super-secret-value-123") in body


def test_post_masked_key_preserves_stored_secret(client, monkeypatch):
    monkeypatch.setattr(type(settings), "save_persistent_settings", lambda self, data: None)
    monkeypatch.setattr(settings, "LLM_PROVIDER", "openai")
    monkeypatch.setattr(settings, "LLM_API_KEY", "sk-original-secret-999")
    monkeypatch.setattr(settings, "OPENAI_API_KEY", "sk-original-secret-999")

    masked = _mask("sk-original-secret-999")
    r = client.post("/api/v1/settings/providers", json={"llm": {"provider": "openai", "api_key": masked}})
    assert r.status_code == 200
    assert settings.LLM_API_KEY == "sk-original-secret-999"


def test_post_new_key_updates_secret(client, monkeypatch):
    monkeypatch.setattr(type(settings), "save_persistent_settings", lambda self, data: None)
    monkeypatch.setattr(settings, "LLM_PROVIDER", "openai")
    monkeypatch.setattr(settings, "LLM_API_KEY", "sk-old-key")
    monkeypatch.setattr(settings, "OPENAI_API_KEY", "sk-old-key")

    r = client.post("/api/v1/settings/providers", json={"llm": {"provider": "openai", "api_key": "sk-brand-new-key-abc"}})
    assert r.status_code == 200
    assert settings.LLM_API_KEY == "sk-brand-new-key-abc"
    assert "sk-brand-new-key-abc" not in r.text


def test_post_updates_provider_model(client, monkeypatch):
    monkeypatch.setattr(type(settings), "save_persistent_settings", lambda self, data: None)
    monkeypatch.setattr(settings, "LLM_PROVIDER", "openai")
    monkeypatch.setattr(settings, "IMAGE_PROVIDER", "flux")

    r = client.post("/api/v1/settings/providers", json={
        "llm": {"provider": "openai", "base_url": "https://ai.sumopod.com/v1",
                "api_key": "sk-real-key-123", "model": "gemini/gemini-3.5-flash-lite"},
        "image": {"provider": "flux", "endpoint_url": "https://api.bfl.ai/v1",
                  "api_key": "bfl-real-key-456", "model": "flux-pro-1.1"}
    })
    assert r.status_code == 200
    data = r.json()
    assert data["llm"]["model"] == "gemini/gemini-3.5-flash-lite"
    assert data["image"]["model"] == "flux-pro-1.1"
    assert settings.OPENAI_MODEL == "gemini/gemini-3.5-flash-lite"
    assert settings.FLUX_MODEL == "flux-pro-1.1"
    assert settings.OPENAI_BASE_URL == "https://ai.sumopod.com/v1"


def test_docs_disabled_in_production(monkeypatch):
    monkeypatch.setattr(settings, "APP_ENV", "production")
    app = main_module.create_app()
    assert app.docs_url is None
    assert app.redoc_url is None
    assert app.openapi_url is None


def test_docs_enabled_in_testing():
    app = main_module.create_app()
    assert app.docs_url == "/docs"
