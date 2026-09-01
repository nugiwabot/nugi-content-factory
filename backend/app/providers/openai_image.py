import base64
import time
import httpx
from typing import Optional
from app.providers.base import ImageProvider, ImageGenerationOutput
from app.providers.mock_image import MockImageProvider
from app.core.config import settings
from app.core.logging import logger


class OpenAIImageProvider(ImageProvider):
    """
    OpenAI-Compatible & OpenRouter Image Generation Provider.
    Supports DALL-E 3, DALL-E 2, and compatible /images/generations endpoints.
    """
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None
    ):
        self.api_key = (api_key or settings.OPENAI_API_KEY or settings.IMAGE_API_KEY or "").strip()
        self.base_url = (base_url or settings.IMAGE_BASE_URL or "https://api.openai.com/v1").rstrip("/")
        self.model = model or settings.IMAGE_MODEL or "dall-e-3"
        self._fallback_provider = MockImageProvider()

    @property
    def provider_name(self) -> str:
        return f"OpenAIImageProvider({self.model})"

    def generate_background(
        self,
        prompt: str,
        width: int = 1080,
        height: int = 1080,
        style_preset: Optional[str] = None
    ) -> ImageGenerationOutput:
        start_time = time.time()

        if not self.api_key and "localhost" not in self.base_url:
            logger.info(f"{self.provider_name}: API Key not configured. Falling back to MockImageProvider.")
            return self._fallback_provider.generate_background(prompt, width, height, style_preset)

        try:
            # Map dimensions to standard supported sizes
            size = "1024x1024"
            if width == 1080 and height == 1350:
                size = "1024x1792" if "dall-e-3" in self.model else "1024x1024"

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }

            payload = {
                "model": self.model,
                "prompt": prompt,
                "n": 1,
                "size": size,
                "response_format": "b64_json"
            }

            endpoint_url = f"{self.base_url}/images/generations"
            with httpx.Client(timeout=60.0) as client:
                response = client.post(endpoint_url, headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()

            image_b64 = data["data"][0]["b64_json"]
            image_bytes = base64.b64decode(image_b64)
            latency_ms = int((time.time() - start_time) * 1000)

            return ImageGenerationOutput(
                image_bytes=image_bytes,
                format="PNG",
                width=width,
                height=height,
                prompt_used=prompt,
                latency_ms=latency_ms
            )

        except Exception as e:
            logger.warning(f"{self.provider_name} generation failed: {str(e)}. Falling back to MockImageProvider.")
            return self._fallback_provider.generate_background(prompt, width, height, style_preset)
