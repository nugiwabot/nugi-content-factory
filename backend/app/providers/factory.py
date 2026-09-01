from typing import Optional
from app.core.config import settings
from app.core.errors import ProviderError
from app.providers.base import LLMProvider, ImageProvider, StorageProvider
from app.providers.mock_llm import MockLLMProvider
from app.providers.mock_image import MockImageProvider
from app.providers.local_storage import LocalStorageProvider


class ProviderFactory:
    """
    Factory to instantiate and inject the active LLM, Image, and Storage providers.
    """
    @staticmethod
    def get_llm_provider(provider_type: Optional[str] = None) -> LLMProvider:
        p_type = (provider_type or settings.LLM_PROVIDER).lower()
        if p_type == "mock":
            return MockLLMProvider()
        raise ProviderError(
            provider=p_type,
            message=f"LLM Provider '{p_type}' is not configured for Phase 1. Use 'mock'."
        )

    @staticmethod
    def get_image_provider(provider_type: Optional[str] = None) -> ImageProvider:
        p_type = (provider_type or settings.IMAGE_PROVIDER).lower()
        if p_type == "mock":
            return MockImageProvider()
        elif p_type == "flux":
            from app.providers.flux_image import FluxImageProvider
            return FluxImageProvider()
        raise ProviderError(
            provider=p_type,
            message=f"Image Provider '{p_type}' is not configured. Supported: 'mock', 'flux'."
        )

    @staticmethod
    def get_storage_provider(provider_type: Optional[str] = None) -> StorageProvider:
        p_type = (provider_type or settings.STORAGE_PROVIDER).lower()
        if p_type == "local":
            return LocalStorageProvider()
        raise ProviderError(
            provider=p_type,
            message=f"Storage Provider '{p_type}' is not configured for Phase 1. Use 'local'."
        )
