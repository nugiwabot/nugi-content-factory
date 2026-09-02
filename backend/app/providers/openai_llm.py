import json
import time
import httpx
from typing import Dict, Any, Optional
from app.providers.base import LLMProvider, LLMContentOutput
from app.core.config import settings
from app.core.errors import ProviderError
from app.core.logging import logger


class OpenAILLMProvider(LLMProvider):
    """
    Generic OpenAI-Compatible LLM Provider Adapter.
    Supports official OpenAI, LocalAI, vLLM, Ollama, DeepSeek, Groq, or any compatible REST endpoint.
    Fails loudly with ProviderError when credentials are missing or the API errors.
    """
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None
    ):
        self.api_key = (api_key or settings.OPENAI_API_KEY or settings.LLM_API_KEY or "").strip()
        self.base_url = (base_url or settings.OPENAI_BASE_URL or settings.LLM_BASE_URL or "https://api.openai.com/v1").rstrip("/")
        self.model = model or settings.OPENAI_MODEL or settings.LLM_MODEL or "gpt-4o-mini"

    @property
    def provider_name(self) -> str:
        return f"OpenAILLMProvider({self.model})"

    def _local_endpoint(self) -> bool:
        return "localhost" in self.base_url or "127.0.0.1" in self.base_url

    def _require_api_key(self) -> None:
        if not self.api_key and not self._local_endpoint():
            raise ProviderError(
                self.provider_name,
                "OpenAI API key is not configured. Add it in Settings > LLM Provider before generating."
            )

    def generate_content(
        self,
        topic: str,
        target_audience: str,
        content_pillar: str,
        tone_of_voice: str,
        brand_context: Optional[Dict[str, Any]] = None
    ) -> LLMContentOutput:
        start_time = time.time()
        self._require_api_key()

        try:
            system_prompt = (
                "Anda adalah AI Content Strategist & Copywriter Senior untuk brand NugiProperti. "
                "Tugas Anda adalah merumuskan konten edukasi / marketing properti bernilai tinggi dalam bahasa Indonesia yang elegan. "
                "Format output WAJIB berupa JSON murni dengan key:\n"
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
                "Content-Type": "application/json"
            }
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"

            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.7,
                "response_format": {"type": "json_object"}
            }

            endpoint_url = f"{self.base_url}/chat/completions"
            with httpx.Client(timeout=30.0) as client:
                response = client.post(endpoint_url, headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()

            content_text = data["choices"][0]["message"]["content"]
            parsed_json = json.loads(content_text)
            tokens_used = data.get("usage", {}).get("total_tokens")
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
            if isinstance(e, ProviderError):
                raise
            logger.error(f"{self.provider_name} request failed: {str(e)}")
            raise ProviderError(self.provider_name, f"OpenAI-compatible LLM request failed: {str(e)}") from e

    def complete(
        self,
        system: str,
        user: str,
        response_format: Optional[str] = None,
        max_tokens: int = 2000
    ) -> str:
        self._require_api_key()

        try:
            payload: Dict[str, Any] = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": user}
                ],
                "temperature": 0.7,
                "max_tokens": max_tokens
            }
            if response_format == "json":
                payload["response_format"] = {"type": "json_object"}

            headers = {"Content-Type": "application/json"}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"

            endpoint_url = f"{self.base_url}/chat/completions"
            with httpx.Client(timeout=60.0) as client:
                response = client.post(endpoint_url, headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            if isinstance(e, ProviderError):
                raise
            logger.error(f"{self.provider_name} complete() failed: {str(e)}")
            raise ProviderError(self.provider_name, f"OpenAI-compatible LLM complete() failed: {str(e)}") from e
