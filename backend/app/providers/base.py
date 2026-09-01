from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class LLMContentOutput(BaseModel):
    """Normalized structured output from any LLM provider."""
    headline: str = Field(description="Visual headline for the graphic banner")
    hook_text: str = Field(description="Opening hook line for caption or sub-banner")
    body_caption: str = Field(description="Full Instagram/Social post copy")
    hashtags: str = Field(description="Space or comma separated hashtags")
    call_to_action: str = Field(description="Direct response CTA")
    visual_concept_prompt: str = Field(description="Prompt for image generation model")
    raw_response: Dict[str, Any] = Field(default_factory=dict)
    tokens_used: Optional[int] = None
    latency_ms: Optional[int] = None


class ImageGenerationOutput(BaseModel):
    """Normalized output from image generator provider."""
    image_bytes: bytes
    format: str = "PNG"
    width: int
    height: int
    prompt_used: str
    latency_ms: Optional[int] = None


class LLMProvider(ABC):
    """Abstract Interface for LLM reasoning and copywriting providers."""

    @property
    @abstractmethod
    def provider_name(self) -> str:
        pass

    @abstractmethod
    def generate_content(
        self,
        topic: str,
        target_audience: str,
        content_pillar: str,
        tone_of_voice: str,
        brand_context: Optional[Dict[str, Any]] = None
    ) -> LLMContentOutput:
        """Generates structured content output based on input brief."""
        pass


class ImageProvider(ABC):
    """Abstract Interface for background and visual generation providers."""

    @property
    @abstractmethod
    def provider_name(self) -> str:
        pass

    @abstractmethod
    def generate_background(
        self,
        prompt: str,
        width: int = 1080,
        height: int = 1080,
        style_preset: Optional[str] = None
    ) -> ImageGenerationOutput:
        """Generates raw background visual asset bytes."""
        pass


class StorageProvider(ABC):
    """Abstract Interface for persistent asset storage."""

    @abstractmethod
    def save(self, data: bytes, filename: str, subfolder: str = "") -> str:
        """Saves binary asset and returns internal file path or URI."""
        pass

    @abstractmethod
    def read(self, file_path: str) -> bytes:
        """Reads binary asset from storage."""
        pass

    @abstractmethod
    def exists(self, file_path: str) -> bool:
        """Checks if asset exists."""
        pass

    @abstractmethod
    def delete(self, file_path: str) -> bool:
        """Deletes asset from storage."""
        pass
