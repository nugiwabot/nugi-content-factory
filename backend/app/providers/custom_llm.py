import json
import time
import httpx
from typing import Dict, Any, Optional
from app.providers.base import LLMProvider, LLMContentOutput
from app.core.config import settings
from app.core.errors import ProviderError
from app.core.logging import logger


class CustomLLMProvider(LLMProvider):
    """
    Custom HTTP REST Endpoint LLM Provider.
    Allows connecting arbitrary internal microservices, self-hosted LLMs, or custom gateways.
    Fails loudly with ProviderError when the endpoint errors.
    """
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None
    ):
        self.api_key = (api_key or settings.LLM_API_KEY or "").strip()
        self.base_url = (base_url or settings.LLM_BASE_URL or "http://localhost:8080").rstrip("/")
        self.model = model or settings.LLM_MODEL or "custom-model"
        self.custom_headers = headers or {}

    @property
    def provider_name(self) -> str:
        return f"CustomLLMProvider({self.base_url})"

    def generate_content(
        self,
        topic: str,
        target_audience: str,
        content_pillar: str,
        tone_of_voice: str,
        brand_context: Optional[Dict[str, Any]] = None
    ) -> LLMContentOutput:
        start_time = time.time()

        try:
            req_headers = {
                "Content-Type": "application/json",
                **self.custom_headers
            }
            if self.api_key:
                req_headers["Authorization"] = f"Bearer {self.api_key}"

            payload = {
                "topic": topic,
                "target_audience": target_audience,
                "content_pillar": content_pillar,
                "tone_of_voice": tone_of_voice,
                "brand_context": brand_context,
                "model": self.model
            }

            endpoint_url = self.base_url if "/generate" in self.base_url else f"{self.base_url}/generate"
            with httpx.Client(timeout=30.0) as client:
                response = client.post(endpoint_url, headers=req_headers, json=payload)
                response.raise_for_status()
                data = response.json()

            latency_ms = int((time.time() - start_time) * 1000)

            return LLMContentOutput(
                headline=data.get("headline", topic.upper()),
                hook_text=data.get("hook_text", f"Insight seputar {topic}."),
                body_caption=data.get("body_caption", f"Pembahasan mengenai {topic}."),
                hashtags=data.get("hashtags", "#Properti #NugiProperti"),
                call_to_action=data.get("call_to_action", "Hubungi kami untuk info selengkapnya."),
                visual_concept_prompt=data.get(
                    "visual_concept_prompt",
                    "Cinematic architectural photography of modern luxury real estate"
                ),
                raw_response=data,
                provider=self.provider_name,
                model=self.model,
                latency_ms=latency_ms
            )

        except Exception as e:
            if isinstance(e, ProviderError):
                raise
            logger.error(f"{self.provider_name} failed: {str(e)}")
            raise ProviderError(self.provider_name, f"Custom LLM request failed: {str(e)}") from e

    def complete(
        self,
        system: str,
        user: str,
        response_format: Optional[str] = None,
        max_tokens: int = 2000
    ) -> str:
        try:
            req_headers = {
                "Content-Type": "application/json",
                **self.custom_headers
            }
            if self.api_key:
                req_headers["Authorization"] = f"Bearer {self.api_key}"

            payload = {
                "system": system,
                "user": user,
                "model": self.model,
                "response_format": response_format,
                "max_tokens": max_tokens
            }

            endpoint_url = self.base_url if "/complete" in self.base_url else f"{self.base_url}/complete"
            with httpx.Client(timeout=60.0) as client:
                response = client.post(endpoint_url, headers=req_headers, json=payload)
                response.raise_for_status()
                data = response.json()

            if isinstance(data, dict) and "text" in data:
                return data["text"]
            if isinstance(data, dict) and "content" in data:
                return data["content"]
            return data if isinstance(data, str) else json.dumps(data)
        except Exception as e:
            if isinstance(e, ProviderError):
                raise
            logger.error(f"{self.provider_name} complete() failed: {str(e)}")
            raise ProviderError(self.provider_name, f"Custom LLM complete() failed: {str(e)}") from e
