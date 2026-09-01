from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
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


class ComputeJobOutput(BaseModel):
    """Normalized output from remote or local compute provider."""
    job_id: str
    status: str = "COMPLETED"  # PENDING, RUNNING, COMPLETED, FAILED
    result: Optional[Dict[str, Any]] = None
    output_files: List[str] = Field(default_factory=list)
    execution_time_ms: Optional[int] = None
    error_message: Optional[str] = None


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

    def test_connection(self) -> Dict[str, Any]:
        """Tests connectivity and authentication with provider endpoint."""
        try:
            out = self.generate_content(
                topic="Test Connectivity",
                target_audience="Test",
                content_pillar="Test",
                tone_of_voice="Professional"
            )
            return {
                "status": "SUCCESS",
                "provider": self.provider_name,
                "latency_ms": out.latency_ms or 50,
                "message": f"Successfully connected to {self.provider_name}"
            }
        except Exception as e:
            return {
                "status": "FAILED",
                "provider": self.provider_name,
                "message": str(e)
            }


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

    def test_connection(self) -> Dict[str, Any]:
        """Tests connectivity and authentication with image provider endpoint."""
        try:
            out = self.generate_background(
                prompt="Modern minimalist architectural glass facade",
                width=512,
                height=512
            )
            return {
                "status": "SUCCESS",
                "provider": self.provider_name,
                "latency_ms": out.latency_ms or 100,
                "message": f"Successfully generated test image with {self.provider_name}"
            }
        except Exception as e:
            return {
                "status": "FAILED",
                "provider": self.provider_name,
                "message": str(e)
            }


class ComputeProvider(ABC):
    """
    Abstract Interface for optional remote compute workloads
    (e.g., video rendering, video analysis, transcription, heavy media processing, local inference).
    RunPod or custom workers implement this interface.
    """

    @property
    @abstractmethod
    def provider_name(self) -> str:
        pass

    @abstractmethod
    def submit_job(
        self,
        task_type: str,
        payload: Dict[str, Any],
        timeout_s: int = 300
    ) -> ComputeJobOutput:
        """Submits a workload job to the compute provider."""
        pass

    @abstractmethod
    def get_job_status(self, job_id: str) -> ComputeJobOutput:
        """Polls the status of an asynchronous compute job."""
        pass

    @abstractmethod
    def cancel_job(self, job_id: str) -> bool:
        """Cancels a running compute job."""
        pass

    def test_connection(self) -> Dict[str, Any]:
        """Tests connectivity with compute provider endpoint."""
        try:
            out = self.submit_job(
                task_type="ping",
                payload={"test": True},
                timeout_s=10
            )
            return {
                "status": "SUCCESS",
                "provider": self.provider_name,
                "message": f"Compute provider {self.provider_name} ready."
            }
        except Exception as e:
            return {
                "status": "FAILED",
                "provider": self.provider_name,
                "message": str(e)
            }


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
