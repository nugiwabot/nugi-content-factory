import pytest

from app.core.config import settings
from app.core.errors import ProviderError
from app.providers.factory import ProviderFactory
from app.providers.anthropic_llm import AnthropicLLMProvider
from app.providers.custom_image import CustomImageProvider
from app.providers.custom_llm import CustomLLMProvider
from app.providers.flux_image import FluxImageProvider
from app.providers.google_llm import GoogleLLMProvider
from app.providers.openai_image import OpenAIImageProvider
from app.providers.openai_llm import OpenAILLMProvider
from app.providers.openrouter_llm import OpenRouterLLMProvider
from app.providers.mock_llm import MockLLMProvider
from app.providers.mock_image import MockImageProvider
from app.providers.retry import call_with_retry

DEAD_ENDPOINT = "http://127.0.0.1:1/v1"


def test_mock_llm_still_works_explicitly():
    provider = ProviderFactory.get_llm_provider("mock")
    assert isinstance(provider, MockLLMProvider)


def test_mock_image_still_works_explicitly():
    provider = ProviderFactory.get_image_provider("mock")
    assert isinstance(provider, MockImageProvider)


def test_mock_disabled_in_production(monkeypatch):
    monkeypatch.setattr(settings, "APP_ENV", "production")
    monkeypatch.setattr(settings, "LLM_PROVIDER", "mock")
    monkeypatch.setattr(settings, "IMAGE_PROVIDER", "mock")
    with pytest.raises(ProviderError):
        ProviderFactory.get_llm_provider("mock")
    with pytest.raises(ProviderError):
        ProviderFactory.get_image_provider("mock")


@pytest.mark.parametrize("provider_cls", [
    OpenRouterLLMProvider,
    OpenAILLMProvider,
    AnthropicLLMProvider,
    GoogleLLMProvider,
])
def test_real_llm_providers_raise_when_key_missing(provider_cls):
    provider = provider_cls(api_key="", base_url="https://api.example.com/v1", model="test-model")
    with pytest.raises(ProviderError):
        provider.generate_content(
            topic="Test topic", target_audience="A", content_pillar="B", tone_of_voice="C"
        )
    with pytest.raises(ProviderError):
        provider.complete(system="s", user="u")


def test_flux_raises_when_key_missing():
    provider = FluxImageProvider(api_key="", base_url=DEAD_ENDPOINT)
    with pytest.raises(ProviderError):
        provider.generate_background(prompt="test", width=512, height=512)


def test_openai_image_raises_when_key_missing():
    provider = OpenAIImageProvider(api_key="", base_url="https://api.example.com/v1")
    with pytest.raises(ProviderError):
        provider.generate_background(prompt="test", width=512, height=512)


def test_custom_image_raises_on_unreachable_endpoint():
    provider = CustomImageProvider(base_url=DEAD_ENDPOINT)
    with pytest.raises(ProviderError):
        provider.generate_background(prompt="test", width=512, height=512)


def test_network_failure_raises_instead_of_mock(monkeypatch):
    # Flux with a key but an unreachable endpoint must raise, never return mock bytes.
    monkeypatch.setattr(settings, "FLUX_API_KEY", "sk-test-fake")
    provider = FluxImageProvider(base_url=DEAD_ENDPOINT)
    with pytest.raises(ProviderError):
        provider.generate_background(prompt="test", width=512, height=512)


def test_openrouter_unreachable_endpoint_raises(monkeypatch):
    monkeypatch.setattr(settings, "OPENROUTER_API_KEY", "sk-test-fake")
    provider = OpenRouterLLMProvider(base_url=DEAD_ENDPOINT)
    with pytest.raises(ProviderError):
        provider.generate_content(
            topic="t", target_audience="a", content_pillar="p", tone_of_voice="v"
        )


def test_call_with_retry_succeeds_after_transient_failure():
    calls = {"n": 0}

    def flaky():
        calls["n"] += 1
        if calls["n"] < 3:
            raise ProviderError("P", "temporary HTTP 500")
        return "ok"

    result = call_with_retry(flaky, attempts=3, delay_seconds=0)
    assert result == "ok"
    assert calls["n"] == 3


def test_call_with_retry_gives_up_and_raises():
    def always_fails():
        raise ProviderError("P", "temporary HTTP 500")

    with pytest.raises(ProviderError):
        call_with_retry(always_fails, attempts=2, delay_seconds=0)


def test_call_with_retry_never_retries_config_errors():
    calls = {"n": 0}

    def config_error():
        calls["n"] += 1
        raise ProviderError("P", "API key is not configured.")

    with pytest.raises(ProviderError):
        call_with_retry(config_error, attempts=3, delay_seconds=0)
    assert calls["n"] == 1
