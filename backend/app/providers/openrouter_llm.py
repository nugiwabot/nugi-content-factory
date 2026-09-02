import json
import time
import httpx
from typing import Dict, Any, Optional
from app.providers.base import LLMProvider, LLMContentOutput
from app.core.config import settings
from app.core.errors import ProviderError
from app.core.logging import logger


class OpenRouterLLMProvider(LLMProvider):
    """
    OpenRouter LLM Provider Adapter.
    Enables calling OpenRouter models such as google/gemini-2.5-flash-lite for property content generation.
    Fails loudly with ProviderError when credentials are missing or the API errors.
    """
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None
    ):
        self.api_key = (api_key if api_key is not None else settings.OPENROUTER_API_KEY or "").strip()
        self.base_url = (base_url or settings.OPENROUTER_BASE_URL or "https://openrouter.ai/api/v1").rstrip("/")
        raw_model = (model or settings.OPENROUTER_MODEL or "google/gemini-2.5-flash-lite").strip()
        if "/" not in raw_model:
            if raw_model.startswith("gemini"):
                raw_model = f"google/{raw_model}"
            elif raw_model.startswith("gpt"):
                raw_model = f"openai/{raw_model}"
            elif raw_model.startswith("claude"):
                raw_model = f"anthropic/{raw_model}"
        self.model = raw_model

    @property
    def provider_name(self) -> str:
        return f"OpenRouterLLMProvider({self.model})"

    def _require_api_key(self) -> None:
        if not self.api_key:
            raise ProviderError(
                self.provider_name,
                "OpenRouter API key is not configured. Add it in Settings > LLM Provider before generating."
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
                "Authorization": f"Bearer {self.api_key}",
                "HTTP-Referer": "http://localhost:5173",
                "X-Title": "Nugi Content Factory",
                "Content-Type": "application/json"
            }

            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.7,
                "response_format": {"type": "json_object"}
            }

            endpoint = f"{self.base_url}/chat/completions"
            logger.info(f"Calling OpenRouter API: {endpoint} with model: {self.model}")

            with httpx.Client(timeout=45.0) as client:
                resp = client.post(endpoint, json=payload, headers=headers)
                if resp.status_code != 200:
                    logger.error(f"OpenRouter API returned status {resp.status_code}: {resp.text[:300]}")
                    raise ProviderError(
                        self.provider_name,
                        f"OpenRouter API returned HTTP {resp.status_code}: {resp.text[:300]}"
                    )

                res_json = resp.json()
                raw_content = res_json.get("choices", [{}])[0].get("message", {}).get("content", "{}")
                data = json.loads(raw_content)

                latency_ms = int((time.time() - start_time) * 1000)
                usage = res_json.get("usage", {})
                tokens_used = usage.get("total_tokens")

                return LLMContentOutput(
                    headline=data.get("headline", topic),
                    hook_text=data.get("hook_text", ""),
                    body_caption=data.get("body_caption", ""),
                    hashtags=data.get("hashtags", "#NugiProperti"),
                    call_to_action=data.get("call_to_action", ""),
                    visual_concept_prompt=data.get("visual_concept_prompt", ""),
                    raw_response=res_json,
                    tokens_used=tokens_used,
                    latency_ms=latency_ms
                )

        except Exception as e:
            if isinstance(e, ProviderError):
                raise
            logger.error(f"OpenRouter LLM call failed: {str(e)}")
            raise ProviderError(self.provider_name, f"OpenRouter LLM call failed: {str(e)}") from e

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

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "HTTP-Referer": "http://localhost:5173",
                "X-Title": "Nugi Content Factory",
                "Content-Type": "application/json"
            }
            endpoint = f"{self.base_url}/chat/completions"
            with httpx.Client(timeout=60.0) as client:
                resp = client.post(endpoint, json=payload, headers=headers)
                if resp.status_code != 200:
                    logger.error(f"OpenRouter complete() status {resp.status_code}: {resp.text[:300]}")
                    raise ProviderError(
                        self.provider_name,
                        f"OpenRouter complete() returned HTTP {resp.status_code}: {resp.text[:300]}"
                    )
                data = resp.json()
            return data.get("choices", [{}])[0].get("message", {}).get("content", "")
        except Exception as e:
            if isinstance(e, ProviderError):
                raise
            logger.error(f"OpenRouter complete() failed: {str(e)}")
            raise ProviderError(self.provider_name, f"OpenRouter complete() failed: {str(e)}") from e
