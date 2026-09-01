import time
import httpx
import io
from PIL import Image
from typing import Optional, Dict, Any
from app.providers.base import ImageProvider, ImageGenerationOutput
from app.providers.mock_image import MockImageProvider
from app.core.config import settings
from app.core.logging import logger
from app.core.errors import ProviderError


class FluxImageProvider(ImageProvider):
    """
    Flux / Black Forest Labs API Image Provider Adapter (Phase 3D-1).
    Generates high-fidelity visual photographic assets using BFL models (e.g. flux-2-klein-9b).
    Supports direct asynchronous task polling via polling_url.
    Gracefully falls back to MockImageProvider if API credentials fail or network is offline.
    """
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None
    ):
        self.api_key = (api_key or settings.FLUX_API_KEY or "").strip()
        
        # Normalize base URL (https://bfl.ai -> https://api.bfl.ai/v1)
        raw_base = (base_url or settings.FLUX_BASE_URL or "https://api.bfl.ai/v1").rstrip("/")
        if "bfl.ai" in raw_base and "api." not in raw_base:
            raw_base = "https://api.bfl.ai/v1"
        elif not raw_base.endswith("/v1"):
            raw_base = f"{raw_base}/v1"
        self.base_url = raw_base

        self.model = model or settings.FLUX_MODEL or "flux-2-klein-9b"
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
                "x-key": self.api_key,
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # BFL requires width & height to be multiples of 32 between 256 and 1440
            req_w = min(1440, max(256, (width // 32) * 32))
            req_h = min(1440, max(256, (height // 32) * 32))

            payload = {
                "prompt": prompt,
                "width": req_w,
                "height": req_h,
                "prompt_upsampling": False,
                "seed": 42
            }

            endpoint = f"{self.base_url}/{self.model}"
            logger.info(f"Submitting task to Flux API: {endpoint} ({req_w}x{req_h})")

            with httpx.Client(timeout=60.0) as client:
                resp = client.post(endpoint, json=payload, headers=headers)
                if resp.status_code not in (200, 201, 202):
                    logger.warning(f"Flux API returned status {resp.status_code}: {resp.text}. Falling back to mock.")
                    return self._fallback_provider.generate_background(prompt, width, height, style_preset)
                
                res_data = resp.json()
                image_url = res_data.get("result", {}).get("sample") or res_data.get("sample")
                task_id = res_data.get("id")
                polling_url = res_data.get("polling_url")

                # Asynchronous polling pattern (standard in BFL)
                if not image_url and (polling_url or task_id):
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
                            elif p_status in ("Error", "Failed", "Request Moderated"):
                                logger.warning(f"Flux task ended with status {p_status}: {p_data}")
                                break

                # Download image binary if URL received
                if image_url:
                    logger.info(f"Downloading generated Flux asset from: {image_url[:80]}...")
                    dl_resp = client.get(image_url)
                    if dl_resp.status_code == 200:
                        raw_bytes = dl_resp.content
                        # Resize to exact requested (width, height)
                        img = Image.open(io.BytesIO(raw_bytes))
                        if img.size != (width, height):
                            img = img.resize((width, height), Image.Resampling.LANCZOS)
                        
                        out_buf = io.BytesIO()
                        img.save(out_buf, format="PNG")
                        final_bytes = out_buf.getvalue()

                        latency = int((time.time() - start_time) * 1000)
                        logger.info(f"Flux generation completed successfully in {latency}ms ({len(final_bytes)} bytes)")
                        return ImageGenerationOutput(
                            image_bytes=final_bytes,
                            width=width,
                            height=height,
                            latency_ms=latency,
                            model_used=self.model,
                            prompt_used=prompt
                        )

            logger.warning("Flux generation did not return an image. Falling back to mock.")
            return self._fallback_provider.generate_background(prompt, width, height, style_preset)

        except Exception as e:
            logger.warning(f"Flux generation exception: {str(e)}. Falling back gracefully to Mock.")
            return self._fallback_provider.generate_background(prompt, width, height, style_preset)
