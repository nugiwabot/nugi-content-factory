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
    Supports direct and asynchronous task polling (BFL API standard).
    Gracefully falls back to MockImageProvider if API credentials fail or are offline.
    """
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None
    ):
        self.api_key = (api_key or settings.FLUX_API_KEY or "").strip()
        
        # Normalize base URL
        raw_base = (base_url or settings.FLUX_BASE_URL or "https://api.bfl.ml/v1").rstrip("/")
        if not raw_base.endswith("/v1") and not raw_base.endswith(".ai") and not raw_base.endswith(".ml"):
            raw_base = f"{raw_base}/v1"
        self.base_url = raw_base

        self.model = model or settings.FLUX_MODEL or "flux-1.1-pro"
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
                "x-key": self.api_key,
                "Content-Type": "application/json"
            }
            payload = {
                "prompt": prompt,
                "width": width,
                "height": height,
                "prompt_upsampling": False,
                "seed": 42
            }

            # Build endpoint URL (handles https://bfl.ai/v1/{model} or https://api.bfl.ml/v1/{model})
            if "/v1" in self.base_url:
                endpoint = f"{self.base_url}/{self.model}"
            else:
                endpoint = f"{self.base_url}/v1/{self.model}"

            logger.info(f"Calling Flux API endpoint: {endpoint} with model: {self.model}")
            
            with httpx.Client(timeout=60.0) as client:
                resp = client.post(endpoint, json=payload, headers=headers)
                if resp.status_code not in (200, 201, 202):
                    logger.warning(f"Flux API returned status {resp.status_code}: {resp.text}. Falling back to mock.")
                    return self._fallback_provider.generate_background(prompt, width, height, style_preset)
                
                res_data = resp.json()

                # Check if result contains direct sample URL or async task ID
                image_url = res_data.get("result", {}).get("sample") or res_data.get("sample")
                task_id = res_data.get("id")
                polling_url = res_data.get("polling_url")

                # If asynchronous task, poll for result (up to 30 seconds)
                if not image_url and (task_id or polling_url):
                    poll_endpoint = polling_url or f"{self.base_url}/get_result?id={task_id}"
                    logger.info(f"Polling Flux generation task: {poll_endpoint}")
                    for _ in range(15):
                        time.sleep(2.0)
                        poll_resp = client.get(poll_endpoint, headers=headers)
                        if poll_resp.status_code == 200:
                            p_data = poll_resp.json()
                            p_status = p_data.get("status")
                            if p_status == "Ready":
                                image_url = p_data.get("result", {}).get("sample") or p_data.get("sample")
                                break
                            elif p_status in ("Error", "Failed"):
                                logger.warning(f"Flux task failed with status {p_status}: {p_data}")
                                break

                if not image_url:
                    logger.warning("No sample image URL resolved from Flux API response. Falling back to mock.")
                    return self._fallback_provider.generate_background(prompt, width, height, style_preset)

                # Download image binary
                img_resp = client.get(image_url)
                if img_resp.status_code != 200:
                    logger.warning("Failed to fetch image binary from Flux URL. Falling back to mock.")
                    return self._fallback_provider.generate_background(prompt, width, height, style_preset)

                latency_ms = int((time.time() - start_time) * 1000)
                logger.info(f"Successfully generated image via Flux API ({len(img_resp.content)} bytes, {latency_ms}ms)")
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
