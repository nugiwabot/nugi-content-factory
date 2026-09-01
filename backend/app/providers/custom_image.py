import base64
import time
import httpx
from typing import Optional, Dict, Any
from app.providers.base import ImageProvider, ImageGenerationOutput
from app.providers.mock_image import MockImageProvider
from app.core.config import settings
from app.core.logging import logger


class CustomImageProvider(ImageProvider):
    """
    Custom Image Generation API Provider Adapter.
    Supports Stable Diffusion WebUI (/sdapi/v1/txt2img), ComfyUI, or custom REST image services.
    """
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None
    ):
        self.api_key = (api_key or settings.IMAGE_API_KEY or "").strip()
        self.base_url = (base_url or settings.IMAGE_BASE_URL or "http://localhost:7860").rstrip("/")
        self.model = model or settings.IMAGE_MODEL or "custom-diffusion"
        self._fallback_provider = MockImageProvider()

    @property
    def provider_name(self) -> str:
        return f"CustomImageProvider({self.base_url})"

    def generate_background(
        self,
        prompt: str,
        width: int = 1080,
        height: int = 1080,
        style_preset: Optional[str] = None
    ) -> ImageGenerationOutput:
        start_time = time.time()

        try:
            headers = {"Content-Type": "application/json"}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"

            # Standard txt2img payload compatible with SD WebUI
            payload = {
                "prompt": prompt,
                "negative_prompt": "text, watermark, typography, blurry, low quality, logo",
                "width": width,
                "height": height,
                "steps": 25,
                "cfg_scale": 7.5
            }

            endpoint = f"{self.base_url}/sdapi/v1/txt2img" if "sdapi" not in self.base_url else self.base_url
            with httpx.Client(timeout=90.0) as client:
                response = client.post(endpoint, headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()

            if "images" in data and len(data["images"]) > 0:
                image_b64 = data["images"][0]
                image_bytes = base64.b64decode(image_b64)
            elif "image" in data:
                image_bytes = base64.b64decode(data["image"])
            else:
                raise ValueError("Unrecognized response payload structure from custom image provider.")

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
