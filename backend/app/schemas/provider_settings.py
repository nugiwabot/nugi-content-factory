from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field


class LLMConfigSchema(BaseModel):
    provider: str = Field(default="openrouter", description="LLM provider: openrouter, openai, anthropic, google, custom, mock")
    base_url: Optional[str] = Field(default=None, description="Custom API Base URL")
    api_key: Optional[str] = Field(default=None, description="API Key (masked in responses)")
    model: Optional[str] = Field(default=None, description="Model identifier")


class ImageConfigSchema(BaseModel):
    provider: str = Field(default="flux", description="Image provider: flux, openrouter, openai, custom, mock")
    endpoint_url: Optional[str] = Field(default=None, description="Endpoint Base URL")
    api_key: Optional[str] = Field(default=None, description="API Key (masked in responses)")
    model: Optional[str] = Field(default=None, description="Model identifier")


class ComputeConfigSchema(BaseModel):
    provider: str = Field(default="local", description="Compute provider: local, runpod, mock")
    endpoint_id: Optional[str] = Field(default=None, description="RunPod Endpoint ID or worker URL")
    api_key: Optional[str] = Field(default=None, description="Compute API Key (masked in responses)")
    worker_config: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Worker hardware/timeout configuration")


class ProviderSettingsResponse(BaseModel):
    llm: LLMConfigSchema
    image: ImageConfigSchema
    compute: ComputeConfigSchema
    supported_llm_providers: List[str] = ["openrouter", "openai", "anthropic", "google", "custom", "mock"]
    supported_image_providers: List[str] = ["flux", "openrouter", "openai", "custom", "mock"]
    supported_compute_providers: List[str] = ["local", "runpod", "mock"]


class ProviderSettingsUpdateRequest(BaseModel):
    llm: Optional[LLMConfigSchema] = None
    image: Optional[ImageConfigSchema] = None
    compute: Optional[ComputeConfigSchema] = None


class TestProviderRequest(BaseModel):
    category: str = Field(..., description="Provider category: 'llm', 'image', or 'compute'")
    provider: Optional[str] = None
    base_url: Optional[str] = None
    endpoint_url: Optional[str] = None
    endpoint_id: Optional[str] = None
    api_key: Optional[str] = None
    model: Optional[str] = None


class TestProviderResponse(BaseModel):
    status: str = "SUCCESS"  # SUCCESS, FAILED, WARNING
    category: str
    provider: str
    latency_ms: Optional[int] = None
    message: str
    details: Optional[Dict[str, Any]] = None
