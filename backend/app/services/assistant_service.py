"""
Nugi Assistant Service.

Satu lapisan percakapan untuk aplikasi "Nugi Assistant": chatbot pribadi yang
memahami bisnis freelance Nugi (nugi.biz.id / freelance-nugi-software-engineer)
dan bisa membantu pekerjaan freelance — menjawab pertanyaan, menulis copy,
artikel, proposal, menjawab keberatan klien, hingga membuat konten visual
(massal) dengan engine produksi yang sudah ada.

Desain: SATU panggilan LLM berstruktur untuk memilih intent, lalu route ke
kemampuan yang sudah terbukti jalan (generate_full_package, batch, renderer).
Tidak ada framework multi-agent. Provider gagal => error terlihat (bukan mock).
"""

import json
from typing import Any, Dict, List, Optional

from app.core.logging import logger
from app.providers.factory import ProviderFactory
from app.knowledge.source import KnowledgeSource

from app.schemas.editorial_agent import (
    AgentChatResponse,
    QuickSuggestion,
    UserBriefInput,
)

CONTENT_PREFIXES = [
    "bikinkan konten tentang", "buatkan konten tentang", "buat konten tentang",
    "bikin konten tentang", "bikinkan post tentang", "buatkan post tentang",
    "bikin postingan tentang", "bikinkan konten", "buatkan konten",
    "bikin konten", "buat konten", "buat postingan", "bikin postingan",
    "buat poster", "bikin poster", "buatkan postingan",
    "tolong buatkan konten tentang", "tolong buatkan konten",
]

INTRO_TEXT = (
    "Halo Mas Nugi! Saya **Asisten Nugi** — asisten pribadi untuk pekerjaan "
    "freelance software engineering kamu.\n\n"
    "Saya memahami bisnis, layanan, harga, dan materi yang ada di repo "
    "`freelance-nugi-software-engineer` + website nugi.biz.id. Saya bisa:\n"
    "• Menjawab pertanyaan seputar bisnis & layanan (paket, harga, alur kerja)\n"
    "• Membantu menulis: copy website, artikel SEO, case study, proposal/SOW\n"
    "• Membantu persiapan sales: discovery, jawab keberatan, follow-up\n"
    "• Membuat **1 konten visual** 1080×1350 siap posting (IG/LinkedIn)\n"
    "• Memandu pembuatan **konten massal** (tab Bulk)\n"
    "• Membantu pekerjaan teknis yang relevan (alur leads, integrasi WA, dll.)\n\n"
    "Coba ketik salah satu contoh di bawah ini:"
)

WELCOME_SUGGESTIONS = [
    QuickSuggestion(label="Jelaskan layanan & harga", prompt="Jelaskan layanan freelance Nugi, paket harga, dan cara kerja dari awal sampai handover secara ringkas."),
    QuickSuggestion(label="Draft proposal developer", prompt="Bantu saya membuat draft proposal singkat untuk developer perumahan yang ingin merapikan distribusi leads tim sales-nya."),
    QuickSuggestion(label="Artikel SEO distribusi leads", prompt="Buat draft artikel SEO: 'Cara otomatis membagi leads iklan ke WhatsApp sales'."),
    QuickSuggestion(label="Jawab keberatan harga", prompt="Klien bilang investasinya Rp5 juta kemahalan. Tolong bantu saya menjawab dengan tenang dan persuasif."),
    QuickSuggestion(label="Konten IG 1 postingan", prompt="Buatkan konten tentang kenapa leads iklan properti hangus karena respon lambat."),
]

SYSTEM_PREFIX = """Kamu adalah "Asisten Nugi", asisten pribadi untuk Nugi — seorang freelance software engineer dan pemilik studio (nugi.biz.id). Kamu membantu seluruh pekerjaan freelance-nya.

IDENTITAS BISNIS (dari knowledge, jangan mengarang):
"""

GROUNDING_RULES = """

ATURAN WAJIB:
1. Jawab BAHASA INDONESIA yang natural, ringkas, dan profesional.
2. Gunakan HANYA fakta bisnis yang ada di KONTEKS di atas (layanan, harga, paket, ICP, positioning, dll). JANGAN mengarang layanan, harga, angka, klaim, nama klien, atau kemampuan.
3. JANGAN mengarang angka/statistik riset apa pun. Jika butuh angka, pakai yang tertulis di KONTEKS, atau katakan "berdasarkan pengalaman / tergantung data kantor".
4. Bagian "KONTEKS INTERNAL PRIVAT" hanya untuk percakapan pribadi dengan Nugi. Jangan pernah menyarankan menyalin isinya ke konten publik.
5. Jika tidak tahu / tidak ada di konteks: katakan jujur dan tawarkan langkah berikutnya.

TUGAS: Tentukan maksud pesan user lalu balas sesuai format JSON berikut (HANYA JSON, tanpa markdown):
- Jika user meminta MEMBUAT KONTEN VISUAL (poster/feed IG/LinkedIn/konten visual): {"intent":"generate","topic":"topik konten 1 kalimat","target_audience":"audiens","reply":"kalimat konfirmasi singkat"}
- Jika user meminta konten MASSAL/banyak sekaligus (mis. "buat 30 konten", "konten massal"): {"intent":"bulk","topic":"tema besar","reply":"penjelasan singkat bahwa untuk konten massal gunakan tab Bulk, plus 3 contoh topik yang bisa dipakai"}
- Jika lainnya (tanya layanan, minta artikel/copy/proposal/keberatan/dll): {"intent":"answer","reply":"jawaban lengkap sesuai konteks"}
"""


class AssistantService:
    """Personal freelance assistant built on the production engine."""

    @staticmethod
    def welcome_response() -> AgentChatResponse:
        return AgentChatResponse(
            reply=INTRO_TEXT,
            action_type="CHAT",
            content_package=None,
            quick_suggestions=WELCOME_SUGGESTIONS,
        )

    @staticmethod
    def _is_greeting(msg: str) -> bool:
        greetings = [
            "halo", "hai", "hei", "hello", "hi", "selamat pagi", "selamat siang",
            "selamat sore", "selamat malam", "tes", "test", "bisa bantu saya",
            "kamu siapa", "bantu saya", "apa kabar", "kamu bisa apa",
            "assalamualaikum", "pagi", "siang", "malam",
        ]
        lower = msg.lower()
        for g in greetings:
            if lower == g or lower.startswith(g + " ") or lower.startswith(g + "?"):
                return True
        return False

    @staticmethod
    def _extract_topic(msg: str) -> str:
        """Falls back to extracting a topic when the LLM isn't available."""
        clean = msg.strip()
        for prefix in CONTENT_PREFIXES:
            if clean.lower().startswith(prefix):
                return clean[len(prefix):].strip(" .,:;\"'")
        return clean

    @staticmethod
    def _is_generate_like(msg: str) -> bool:
        lower = msg.lower()
        return any(k in lower for k in [
            "buat konten", "bikin konten", "buatkan konten", "poster", "postingan",
            "konten ig", "konten instagram", "konten linkedin", "feed ",
            "buat visual", "konten visual", "buatkan poster",
        ])

    @staticmethod
    def _is_bulk_like(msg: str) -> bool:
        lower = msg.lower()
        return any(k in lower for k in ["massal", "banyak konten", "30 konten", "bulk", "10 konten", "50 konten", "semua konten"])

    @staticmethod
    def _build_context(msg: str, private: bool = True) -> str:
        """Retrieves business knowledge relevant to the message."""
        try:
            return KnowledgeSource.assistant_context(msg, private_limit=4 if private else 0)
        except Exception as e:
            logger.warning(f"Assistant knowledge context failed: {e}")
            return ""

    @staticmethod
    def _call_llm(msg: str, context: str) -> Dict[str, Any]:
        """One structured LLM call; raises on real provider failure."""
        from app.services.copywriter_service import CopywriterService  # noqa: F401 (mirror parse style)
        llm = ProviderFactory.get_llm_provider()
        if "mock" in llm.provider_name.lower():
            return {}

        system = SYSTEM_PREFIX + (context[:15000] if context else "(tidak ada konteks)") + GROUNDING_RULES
        raw = llm.complete(system=system, user=f"Pesan user:\n{msg}", response_format="json", max_tokens=1200)
        raw = (raw or "").strip()
        if raw.startswith("```"):
            raw = raw.split("```", 1)[1].rsplit("```", 1)[0].strip()
            if raw.startswith("json"):
                raw = raw[4:].strip()
        data = json.loads(raw) if raw else {}
        if not isinstance(data, dict):
            data = {}
        return data

    @staticmethod
    def _deterministic_answer(msg: str) -> AgentChatResponse:
        """Deterministic fallback used only when no live LLM is configured."""
        if AssistantService._is_bulk_like(msg):
            return AgentChatResponse(
                reply=(
                    "Untuk konten massal, buka tab **Bulk** di atas, tempel banyak "
                    "topik (satu per baris), lalu klik **Generate Batch**. Sistem akan "
                    "membuat konten per topik sekaligus."
                ),
                action_type="CHAT",
                content_package=None,
            )
        if AssistantService._is_generate_like(msg):
            topic = AssistantService._extract_topic(msg)
            if topic:
                return AssistantService._generate_one(topic, None)
        return AssistantService.welcome_response()

    @staticmethod
    def _generate_one(topic: str, project_id: Optional[str], db: Any = None) -> AgentChatResponse:
        from app.services.content_generation_agent import ContentGenerationAgent
        from app.services.knowledge_service import KnowledgeService

        agent = ContentGenerationAgent()
        brief = UserBriefInput(topic=topic, project_id=project_id)

        skill_context = ""
        brand_context = ""
        if db is not None:
            try:
                brand_context = KnowledgeService.get_brand_context(db)
                skill_context = KnowledgeService.retrieve_relevant_skills(db, brief.topic)
            except Exception as e:
                logger.warning(f"Knowledge retrieval skipped: {str(e)}")

        pkg = agent.generate_full_package(
            brief=brief,
            db=db,
            skill_context=skill_context,
            brand_context=brand_context,
        )
        headline = pkg.editorial_spec.headline
        reply_text = (
            f"Tentu Mas Nugi! Saya telah merancang konten visual bertema "
            f"**\"{headline}\"**.\n\n"
            f"• **Target audiens:** {pkg.editorial_spec.target_audience}\n"
            f"• **Format:** {pkg.content_type.value}\n"
            f"• **QA visual:** {pkg.visual_qa.score if pkg.visual_qa else 'n/a'}/100\n\n"
            f"Poster high-res 1080×1350 dan caption sudah tersedia di bawah. "
            f"Silakan unduh gambar atau salin caption."
        )
        return AgentChatResponse(
            reply=reply_text,
            action_type="GENERATE",
            content_package=pkg,
        )

    @staticmethod
    def respond(req: Any, db: Any = None) -> AgentChatResponse:
        """
        Main entry point for /ai-studio/chat. Returns an AgentChatResponse.
        """
        msg = (req.message or "").strip()
        if not msg:
            return AssistantService.welcome_response()

        lower = msg.lower()
        active_pkg = getattr(req, "active_package", None)

        # 1) Revision commands on the currently active content package.
        from app.services.content_generation_agent import ContentGenerationAgent
        if active_pkg is not None:
            agent = ContentGenerationAgent()
            if "ubah headline" in lower or "ganti headline" in lower or "headline lain" in lower:
                updated = agent.regenerate_headline(active_pkg)
                return AgentChatResponse(reply=f"Headline diperbarui: **\"{updated.editorial_spec.headline}\"**.", action_type="REVISE_HEADLINE", content_package=updated)
            if "ubah visual" in lower or "ganti visual" in lower or "visual lain" in lower or "ubah gambar" in lower or "ganti gambar" in lower:
                updated = agent.regenerate_visual_art(active_pkg)
                return AgentChatResponse(reply="Visual telah diperbarui dan dirender ulang.", action_type="REVISE_VISUAL", content_package=updated)
            if "tulis ulang caption" in lower or "ganti caption" in lower or "caption lain" in lower:
                updated = agent.regenerate_caption(active_pkg)
                return AgentChatResponse(reply="Caption telah ditulis ulang.", action_type="REVISE_CAPTION", content_package=updated)

        # 2) Greeting -> capability intro (no LLM needed).
        if AssistantService._is_greeting(msg):
            return AssistantService.welcome_response()

        # 3) Knowledge-grounded LLM routing.
        context = AssistantService._build_context(msg)
        try:
            decision = AssistantService._call_llm(msg, context)
        except Exception as e:
            # Real provider failure must surface, not silently become mock content.
            logger.error(f"AssistantService LLM provider failed: {e}")
            raise

        intent = str(decision.get("intent") or "").lower()

        if intent == "generate":
            topic = (decision.get("topic") or AssistantService._extract_topic(msg)).strip()
            if topic:
                return AssistantService._generate_one(topic, getattr(req, "project_id", None), db)
            return AssistantService.welcome_response()

        if intent == "bulk":
            reply = decision.get("reply") or (
                "Untuk konten massal, buka tab **Bulk** di atas lalu tempel banyak topik "
                "(satu per baris) dan klik Generate Batch."
            )
            return AgentChatResponse(reply=reply, action_type="CHAT", content_package=None)

        # intent == "answer" or unknown
        reply = str(decision.get("reply") or "").strip()
        if reply:
            return AgentChatResponse(reply=reply, action_type="CHAT", content_package=None)

        # No usable LLM decision (mock/offline or empty) -> deterministic behavior.
        return AssistantService._deterministic_answer(msg)
