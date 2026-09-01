import json
import time
import httpx
from typing import Dict, Any, Optional
from app.providers.base import LLMProvider, LLMContentOutput
from app.providers.mock_llm import MockLLMProvider
from app.core.config import settings
from app.core.logging import logger


class AnthropicLLMProvider(LLMProvider):
    """
    Anthropic-Compatible Messages API Provider.
    Supports Claude 3.5 Sonnet, Claude 3 Opus, Claude 3 Haiku, or compatible proxies.
    """
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None
    ):
        self.api_key = (api_key or settings.ANTHROPIC_API_KEY or settings.LLM_API_KEY or "").strip()
        self.base_url = (base_url or settings.ANTHROPIC_BASE_URL or "https://api.anthropic.com/v1").rstrip("/")
        self.model = model or settings.ANTHROPIC_MODEL or "claude-3-5-sonnet-20241022"
        self._fallback_provider = MockLLMProvider()

    @property
    def provider_name(self) -> str:
        return f"AnthropicLLMProvider({self.model})"

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
                "Format output WAJIB berupa JSON murni tanpa markdown wrapper dengan key:\n"
                "{\n"
                '  "headline": "Judul visual 2-4 baris huruf besar",\n'
                '  "hook_text": "Kalimat pembuka singkat sub-banner",\n'
                '  "body_caption": "Artikel lengkap Instagram dengan struktur: Hook, Problem, Explanation, Solution, Takeaway",\n'
                '  "hashtags": "#HashtagProperti #NugiProperti",\n'
                '  "call_to_action": "CTA text jika diperlukan",\n'
                '  "visual_concept_prompt": "Prompt visual arsitektur murni tanpa teks untuk generator gambar"\n'
                "}"
            )

            user_prompt = (
                f"Topik: {topic}\n"
                f"Target Audience: {target_audience}\n"
                f"Pilar Konten: {content_pillar}\n"
                f"Tone of Voice: {tone_of_voice}\n"
                f"Konteks Brand: {brand_context or 'NugiProperti - Otoritas Konten & Pertumbuhan Properti'}"
            )

            headers = {
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            }

            payload = {
                "model": self.model,
                "max_tokens": 1200,
                "system": system_prompt,
                "messages": [
                    {"role": "user", "content": user_prompt}
                ]
            }

            endpoint_url = f"{self.base_url}/messages"
            with httpx.Client(timeout=30.0) as client:
                response = client.post(endpoint_url, headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()

            content_text = data["content"][0]["text"]
            # Clean markdown codeblocks if present
            if content_text.startswith("```json"):
                content_text = content_text.split("```json", 1)[1].rsplit("```", 1)[0].strip()
            elif content_text.startswith("```"):
                content_text = content_text.split("```", 1)[1].rsplit("```", 1)[0].strip()

            parsed_json = json.loads(content_text)
            tokens_used = (data.get("usage", {}).get("input_tokens", 0) + data.get("usage", {}).get("output_tokens", 0))
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
