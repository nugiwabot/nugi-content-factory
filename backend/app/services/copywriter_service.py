import json
from typing import Optional, Dict, Any

from app.core.logging import logger
from app.providers.factory import ProviderFactory
from app.providers.retry import call_with_retry


class CopywriterService:
    """
    LLM-driven copywriting layer. Produces headline, subheadline, highlight words, and
    caption informed by brand context and selected skills. Returns None to signal that the
    deterministic template services should be used (no live LLM / mock provider).
    """

    @staticmethod
    def generate_editorial_copy(
        topic: str,
        content_type: str,
        target_audience: str,
        core_insight: str,
        cta_policy: str,
        cta_text: Optional[str],
        skill_context: Optional[str] = None,
        brand_context: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        llm = ProviderFactory.get_llm_provider()
        if llm.provider_name == "MockLLMProvider":
            return None

        system_prompt = (
            "Anda adalah Copywriter Senior & Content Strategist untuk brand NugiProperti. "
            "Tulis konten edukasi/marketing properti berbahasa Indonesia yang elegan, spesifik, dan mendorong aksi.\n"
            "WAJIB ikuti gaya & aturan berikut (jika tersedia di bawah):\n\n"
            f"{skill_context or ''}\n\n"
            f"{brand_context or ''}\n\n"
            "Keluarkan HANYA JSON murni (tanpa markdown fence) dengan key:\n"
            '{"headline": "judul visual 2-4 kata ALL CAPS", '
            '"subheadline": "1 kalimat pendukung", '
            '"highlight_words": ["kata","yang","di-highlight"], '
            '"caption": "caption Instagram lengkap dengan struktur Hook, Problem, Explanation, Solution, Takeaway"}'
        )

        user_prompt = (
            f"Topik: {topic}\n"
            f"Jenis Konten: {content_type}\n"
            f"Target Audiens: {target_audience}\n"
            f"Core Insight: {core_insight}\n"
            f"Kebijakan CTA: {cta_policy}\n"
            f"Teks CTA: {cta_text or '-'}"
        )

        try:
            raw = call_with_retry(
                llm.complete,
                system=system_prompt,
                user=user_prompt,
                response_format="json",
                max_tokens=1500
            )
        except Exception as e:
            # Real provider infrastructure failures must surface, never silently
            # degrade to deterministic templates.
            logger.error(f"CopywriterService LLM provider failed: {str(e)}")
            raise

        try:
            raw = raw.strip()
            if raw.startswith("```"):
                raw = raw.split("```", 1)[1].rsplit("```", 1)[0].strip()
                if raw.startswith("json"):
                    raw = raw[4:].strip()
            data = json.loads(raw)
        except Exception as e:
            logger.warning(f"CopywriterService LLM parse failed: {str(e)}. Falling back to templates.")
            return None

        headline = (data.get("headline") or "").strip()
        subheadline = (data.get("subheadline") or "").strip()
        highlight_words = data.get("highlight_words") or []
        caption = (data.get("caption") or "").strip()

        if not headline or len(headline) < 3 or not caption:
            return None

        return {
            "headline": headline,
            "subheadline": subheadline,
            "highlight_words": highlight_words if isinstance(highlight_words, list) else [],
            "caption": caption
        }
