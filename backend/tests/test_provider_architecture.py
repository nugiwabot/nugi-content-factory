import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.core.config import settings
from app.providers.factory import ProviderFactory
from app.providers.base import LLMProvider, ImageProvider, StorageProvider
from app.providers.mock_llm import MockLLMProvider
from app.providers.mock_image import MockImageProvider
from app.providers.openrouter_llm import OpenRouterLLMProvider
from app.providers.openai_llm import OpenAILLMProvider
from app.providers.anthropic_llm import AnthropicLLMProvider
from app.providers.google_llm import GoogleLLMProvider
from app.providers.custom_llm import CustomLLMProvider
from app.providers.flux_image import FluxImageProvider
from app.providers.openai_image import OpenAIImageProvider
from app.providers.custom_image import CustomImageProvider

client = TestClient(app)


def test_provider_factory_llm_instantiation():
    """Verify all LLM providers can be dynamically instantiated through ProviderFactory."""
    mock_p = ProviderFactory.get_llm_provider("mock")
    assert isinstance(mock_p, LLMProvider)
    assert isinstance(mock_p, MockLLMProvider)

    openrouter_p = ProviderFactory.get_llm_provider("openrouter")
    assert isinstance(openrouter_p, OpenRouterLLMProvider)

    openai_p = ProviderFactory.get_llm_provider("openai", {"base_url": "https://api.openai.com/v1", "model": "gpt-4o"})
    assert isinstance(openai_p, OpenAILLMProvider)

    anthropic_p = ProviderFactory.get_llm_provider("anthropic", {"model": "claude-3-5-sonnet"})
    assert isinstance(anthropic_p, AnthropicLLMProvider)

    google_p = ProviderFactory.get_llm_provider("google", {"model": "gemini-1.5-flash"})
    assert isinstance(google_p, GoogleLLMProvider)

    custom_p = ProviderFactory.get_llm_provider("custom", {"base_url": "http://localhost:8000/v1"})
    assert isinstance(custom_p, CustomLLMProvider)


def test_provider_factory_image_instantiation():
    """Verify all Image providers can be dynamically instantiated through ProviderFactory."""
    mock_p = ProviderFactory.get_image_provider("mock")
    assert isinstance(mock_p, ImageProvider)
    assert isinstance(mock_p, MockImageProvider)

    flux_p = ProviderFactory.get_image_provider("flux")
    assert isinstance(flux_p, FluxImageProvider)

    openai_img = ProviderFactory.get_image_provider("openai", {"model": "dall-e-3"})
    assert isinstance(openai_img, OpenAIImageProvider)

    custom_img = ProviderFactory.get_image_provider("custom", {"base_url": "http://localhost:7860"})
    assert isinstance(custom_img, CustomImageProvider)


def test_api_get_provider_settings():
    """Verify GET /api/v1/settings/providers returns structured config with masked keys."""
    resp = client.get("/api/v1/settings/providers")
    assert resp.status_code == 200
    data = resp.json()
    assert "llm" in data
    assert "image" in data
    assert "supported_llm_providers" in data
    assert "openrouter" in data["supported_llm_providers"]
    assert "flux" in data["supported_image_providers"]


def test_api_update_provider_settings(monkeypatch):
    """Verify POST /api/v1/settings/providers updates configuration at runtime."""
    monkeypatch.setattr(type(settings), "save_persistent_settings", lambda self, data: None)
    payload = {
        "llm": {
            "provider": "mock",
            "model": "mock-model"
        },
        "image": {
            "provider": "mock",
            "model": "mock-flux"
        }
    }
    resp = client.post("/api/v1/settings/providers", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["llm"]["provider"] == "mock"
    assert data["image"]["provider"] == "mock"


def test_api_test_provider_connection_mock():
    """Verify POST /api/v1/settings/providers/test tests connectivity."""
    # Test LLM
    resp_llm = client.post("/api/v1/settings/providers/test", json={
        "category": "llm",
        "provider": "mock"
    })
    assert resp_llm.status_code == 200
    assert resp_llm.json()["status"] == "SUCCESS"

    # Test Image
    resp_img = client.post("/api/v1/settings/providers/test", json={
        "category": "image",
        "provider": "mock"
    })
    assert resp_img.status_code == 200
    assert resp_img.json()["status"] == "SUCCESS"
