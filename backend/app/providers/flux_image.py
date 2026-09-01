import time
import httpx
from typing import Optional, Dict, Any
from app.providers.base import ImageProvider, ImageGenerationOutput
from app.providers.mock_image import MockImageProvider
from app.core.config import settings
from app.core.logging import logger
from app.core.errors import ProviderError


class FluxImageProvider(ImageProvider):
    """
    Flux / Black Forest Labs API Image Provider Adapter.
    Generates pure visual background assets from VisualPromptSpecification.
    Gracefully falls back to MockImageProvider if API credentials are unavailable or network fails.
    """
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None
    ):
        self.api_key = api_key or settings.FLUX_API_KEY
        self.base_url = (base_url or settings.FLUX_BASE_URL).rstrip("/")
        self.model = model or settings.FLUX_MODEL
        self._fallback_provider = MockImageProvider()

    @property
    def provider_name(self) -> str:
        return f"FluxImageProvider({self.model})"

    def generate_background(
        self,
        prompt: str,
        width: int = 1080,
        height: int = 1350,
        style_preset: Optional[str] = None
    ) -> ImageGenerationOutput:
        start_time = time.time()

        # 1. Fallback check: if no API key is provided, gracefully delegate to MockImageProvider
        if not self.api_key:
            logger.info("FLUX_API_KEY not configured. Falling back gracefully to MockImageProvider.")
            return self._fallback_provider.generate_background(
                prompt=prompt,
                width=width,
                height=height,
                style_preset=style_preset
            )

        # 2. Live Flux API invocation
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "prompt": prompt,
                "width": width,
                "height": height,
                "prompt_upsampling": False,
                "seed": 42
            }

            # POST /flux-pro-1.1 or configured endpoint
            endpoint = f"{self.base_url}/{self.model}"
            logger.info(f"Calling Flux API endpoint: {endpoint}")
            
            with httpx.Client(timeout=45.0) as client:
                resp = client.post(endpoint, json=payload, headers=headers)
                if resp.status_code != 200:
                    logger.warning(f"Flux API returned status {resp.status_code}: {resp.text}. Falling back to mock.")
                    return self._fallback_provider.generate_background(prompt, width, height, style_preset)
                
                res_data = resp.json()
                image_url = res_data.get("result", {}).get("sample") or res_data.get("sample")
                if not image_url:
                    logger.warning("No sample image URL returned from Flux. Falling back to mock.")
                    return self._fallback_provider.generate_background(prompt, width, height, style_preset)

                # Download image binary
                img_resp = client.get(image_url)
                if img_resp.status_code != 200:
                    logger.warning("Failed to fetch image binary from Flux URL. Falling back to mock.")
                    return self._fallback_provider.generate_background(prompt, width, height, style_preset)

                latency_ms = int((time.time() - start_time) * 1000)
                return ImageGenerationOutput(
                    image_bytes=img_resp.content,
                    format="PNG",
                    width=width,
                    height=height,
                    prompt_used=prompt,
                    latency_ms=latency_ms
                )

        except Exception as e:
            logger.warning(f"Flux API invocation failed: {str(e)}. Falling back gracefully to MockImageProvider.")
            return self._fallback_provider.generate_background(
                prompt=prompt,
                width=width,
                height=height,
                style_preset=style_preset
            )
