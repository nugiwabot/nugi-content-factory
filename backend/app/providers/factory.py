from typing import Optional, Dict, Any
from app.core.config import settings
from app.core.errors import ProviderError
from app.providers.base import LLMProvider, ImageProvider, StorageProvider, ComputeProvider
from app.providers.mock_llm import MockLLMProvider
from app.providers.mock_image import MockImageProvider
from app.providers.mock_compute import MockComputeProvider
from app.providers.local_storage import LocalStorageProvider


class ProviderFactory:
    """
    Modular Provider Factory.
    Decouples core business logic from specific AI vendors (OpenRouter, OpenAI, Anthropic, Google, Flux, RunPod, etc.).
    Supports dynamic instantiation with runtime overrides and graceful mock fallbacks.
    """

    @staticmethod
    def get_llm_provider(
        provider_type: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None
    ) -> LLMProvider:
        cfg = config or {}
        p_type = (provider_type or cfg.get("provider") or settings.LLM_PROVIDER).lower()

        if p_type == "mock":
            if settings.is_production and not settings.is_testing:
                raise ProviderError(
                    "MockLLMProvider",
                    "Mock LLM provider is disabled in production. Configure a real provider in Settings > LLM Provider."
                )
            return MockLLMProvider()

        elif p_type == "openrouter":
            from app.providers.openrouter_llm import OpenRouterLLMProvider
            return OpenRouterLLMProvider(
                api_key=cfg.get("api_key"),
                base_url=cfg.get("base_url"),
                model=cfg.get("model")
            )

        elif p_type == "openai":
            from app.providers.openai_llm import OpenAILLMProvider
            return OpenAILLMProvider(
                api_key=cfg.get("api_key"),
                base_url=cfg.get("base_url"),
                model=cfg.get("model")
            )

        elif p_type == "anthropic":
            from app.providers.anthropic_llm import AnthropicLLMProvider
            return AnthropicLLMProvider(
                api_key=cfg.get("api_key"),
                base_url=cfg.get("base_url"),
                model=cfg.get("model")
            )

        elif p_type == "google":
            from app.providers.google_llm import GoogleLLMProvider
            return GoogleLLMProvider(
                api_key=cfg.get("api_key"),
                base_url=cfg.get("base_url"),
                model=cfg.get("model")
            )

        elif p_type == "custom":
            from app.providers.custom_llm import CustomLLMProvider
            return CustomLLMProvider(
                api_key=cfg.get("api_key"),
                base_url=cfg.get("base_url"),
                model=cfg.get("model")
            )

        raise ProviderError(
            provider=p_type,
            message=f"LLM Provider '{p_type}' is not supported. Options: 'mock', 'openrouter', 'openai', 'anthropic', 'google', 'custom'."
        )

    @staticmethod
    def get_image_provider(
        provider_type: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None
    ) -> ImageProvider:
        cfg = config or {}
        p_type = (provider_type or cfg.get("provider") or settings.IMAGE_PROVIDER).lower()

        if p_type == "mock":
            if settings.is_production and not settings.is_testing:
                raise ProviderError(
                    "MockImageProvider",
                    "Mock image provider is disabled in production. Configure a real provider in Settings > Image Provider."
                )
            return MockImageProvider()

        elif p_type == "flux":
            from app.providers.flux_image import FluxImageProvider
            return FluxImageProvider(
                api_key=cfg.get("api_key"),
                model=cfg.get("model"),
                base_url=cfg.get("base_url") or cfg.get("endpoint_url")
            )

        elif p_type in ["openrouter", "openai"]:
            from app.providers.openai_image import OpenAIImageProvider
            return OpenAIImageProvider(
                api_key=cfg.get("api_key"),
                base_url=cfg.get("base_url") or cfg.get("endpoint_url"),
                model=cfg.get("model")
            )

        elif p_type == "custom":
            from app.providers.custom_image import CustomImageProvider
            return CustomImageProvider(
                api_key=cfg.get("api_key"),
                base_url=cfg.get("base_url") or cfg.get("endpoint_url"),
                model=cfg.get("model")
            )

        raise ProviderError(
            provider=p_type,
            message=f"Image Provider '{p_type}' is not supported. Options: 'mock', 'flux', 'openai', 'openrouter', 'custom'."
        )

    @staticmethod
    def get_compute_provider(
        provider_type: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None
    ) -> ComputeProvider:
        cfg = config or {}
        p_type = (provider_type or cfg.get("provider") or settings.COMPUTE_PROVIDER).lower()

        if p_type == "mock":
            return MockComputeProvider()

        elif p_type == "local":
            from app.providers.local_compute import LocalComputeProvider
            return LocalComputeProvider()

        elif p_type == "runpod":
            from app.providers.runpod_compute import RunPodComputeProvider
            return RunPodComputeProvider(
                api_key=cfg.get("api_key"),
                endpoint_id=cfg.get("endpoint_id"),
                base_url=cfg.get("base_url")
            )

        raise ProviderError(
            provider=p_type,
            message=f"Compute Provider '{p_type}' is not supported. Options: 'local', 'runpod', 'mock'."
        )

    @staticmethod
    def get_storage_provider(
        provider_type: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None
    ) -> StorageProvider:
        cfg = config or {}
        p_type = (provider_type or cfg.get("provider") or settings.STORAGE_PROVIDER).lower()

        if p_type == "local":
            return LocalStorageProvider(base_dir=cfg.get("base_dir"))

        raise ProviderError(
            provider=p_type,
            message=f"Storage Provider '{p_type}' is not supported. Options: 'local'."
        )
