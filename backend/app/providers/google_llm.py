import json
import time
import httpx
from typing import Dict, Any, Optional
from app.providers.base import LLMProvider, LLMContentOutput
from app.providers.mock_llm import MockLLMProvider
from app.core.config import settings
from app.core.logging import logger


class GoogleLLMProvider(LLMProvider):
    """
    Google Gemini Direct API Provider Adapter.
    Supports Gemini 1.5 Pro, Gemini 1.5 Flash, Gemini 2.0 Flash via Google Generative Language REST API.
    """
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None
    ):
        self.api_key = (api_key or settings.GOOGLE_API_KEY or settings.LLM_API_KEY or "").strip()
        self.base_url = (base_url or "https://generativelanguage.googleapis.com/v1beta").rstrip("/")
        self.model = model or settings.GOOGLE_MODEL or "gemini-1.5-flash"
        self._fallback_provider = MockLLMProvider()

    @property
    def provider_name(self) -> str:
        return f"GoogleLLMProvider({self.model})"

    def generate_content(
        self,
        topic: str,
        target_audience: str,
        content_pillar: str,
        tone_of_voice: str,
        brand_context: Optional[Dict[str, Any]] = None
    ) -> LLMContentOutput:
        start_time = time.time()

        if not self.api_key:
            logger.info(f"{self.provider_name}: API Key not configured. Falling back to MockLLMProvider.")
            return self._fallback_provider.generate_content(
                topic, target_audience, content_pillar, tone_of_voice, brand_context
            )

        try:
            system_prompt = (
                "Anda adalah AI Content Strategist & Copywriter Senior untuk brand NugiProperti. "
                "Tugas Anda adalah merumuskan konten edukasi / marketing properti bernilai tinggi dalam bahasa Indonesia yang elegan. "
                "Format output WAJIB berupa JSON murni dengan key: "
                "headline, hook_text, body_caption, hashtags, call_to_action, visual_concept_prompt."
            )

            user_prompt = (
                f"Topik: {topic}\n"
                f"Target Audience: {target_audience}\n"
                f"Pilar Konten: {content_pillar}\n"
                f"Tone of Voice: {tone_of_voice}\n"
                f"Konteks Brand: {brand_context or 'NugiProperti - Otoritas Konten & Pertumbuhan Properti'}"
            )

            endpoint_url = f"{self.base_url}/models/{self.model}:generateContent?key={self.api_key}"
            payload = {
                "system_instruction": {
                    "parts": [{"text": system_prompt}]
                },
                "contents": [
                    {"role": "user", "parts": [{"text": user_prompt}]}
                ],
                "generationConfig": {
                    "response_mime_type": "application/json",
                    "temperature": 0.7
                }
            }

            with httpx.Client(timeout=30.0) as client:
                response = client.post(endpoint_url, json=payload)
                response.raise_for_status()
                data = response.json()

            content_text = data["candidates"][0]["content"]["parts"][0]["text"]
            parsed_json = json.loads(content_text)
            tokens_used = data.get("usageMetadata", {}).get("totalTokenCount")
            latency_ms = int((time.time() - start_time) * 1000)

            return LLMContentOutput(
                headline=parsed_json.get("headline", topic.upper()),
                hook_text=parsed_json.get("hook_text", f"Insight penting seputar {topic}."),
                body_caption=parsed_json.get("body_caption", f"Pembahasan mendalam mengenai {topic}."),
                hashtags=parsed_json.get("hashtags", "#Properti #NugiProperti"),
                call_to_action=parsed_json.get("call_to_action", "Simpan postingan ini untuk referensi Anda."),
                visual_concept_prompt=parsed_json.get(
                    "visual_concept_prompt",
                    "Cinematic architectural photography of modern luxury property with dramatic twilight lighting"
                ),
                raw_response=data,
                tokens_used=tokens_used,
                latency_ms=latency_ms
            )

        except Exception as e:
            logger.warning(f"{self.provider_name} request failed: {str(e)}. Falling back to MockLLMProvider.")
            return self._fallback_provider.generate_content(
                topic, target_audience, content_pillar, tone_of_voice, brand_context
            )
