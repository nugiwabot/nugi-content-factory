import json
import re
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from app.core.logging import logger
from app.models.pillar import ContentPillar
from app.providers.factory import ProviderFactory
from app.schemas.editorial_agent import ContentType
from app.services.knowledge_service import KnowledgeService


class AgentPlannerService:
    """
    Turns a single goal (or a raw list of topics) into a list of content briefs,
    using the LLM with the seeded knowledge base. Falls back to deterministic
    pillar rotation when no live LLM is available.
    """

    VALID_CONTENT_TYPES = {ct.value for ct in ContentType}

    @staticmethod
    def _pillar_index(db: Session) -> Dict[str, Dict[str, Any]]:
        pillars = db.query(ContentPillar).order_by(ContentPillar.sort_order).all()
        return {p.key: {
            "key": p.key,
            "name": p.name,
            "business_goal": p.business_goal,
            "sub_topics": p.sub_topics or [],
            "example_angles": p.example_angles or [],
            "prompt_guidance": p.prompt_guidance or ""
        } for p in pillars}

    @staticmethod
    def _normalize_pillar(value: Optional[str], pillar_index: Dict[str, Dict[str, Any]]) -> str:
        if not value:
            return "PROBLEM_EDUCATION"
        v = value.strip().upper()
        for key, info in pillar_index.items():
            if v == key.upper() or v == info["name"].upper().replace(" ", "_"):
                return key
        return "PROBLEM_EDUCATION" if "PROBLEM_EDUCATION" in pillar_index else (next(iter(pillar_index), "PROBLEM_EDUCATION"))

    @classmethod
    def plan_from_goal(
        cls,
        db: Session,
        goal: str,
        count: int = 5,
        project_id: Optional[str] = None
    ) -> Dict[str, Any]:
        count = max(1, min(int(count or 5), 30))
        pillar_index = cls._pillar_index(db)
        brand_context = KnowledgeService.get_brand_context(db)
        skill_context = KnowledgeService.retrieve_relevant_skills(db, goal, limit=2)

        llm = ProviderFactory.get_llm_provider()
        items: List[Dict[str, Any]] = []

        if llm.provider_name != "MockLLMProvider":
            try:
                pillar_lines = "\n".join([
                    f"- {k}: {v['name']} (goal={v['business_goal']}) — sub-topik: {', '.join(v['sub_topics'][:3])}"
                    for k, v in pillar_index.items()
                ])
                system_prompt = (
                    "Anda adalah Content Planner untuk studio AI properti NugiProperti. "
                    "Tugas Anda: mengubah satu goal menjadi daftar brief konten yang terencana.\n\n"
                    f"PILAR KONTEN TERSEDIA:\n{pillar_lines or '- PROBLEM_EDUCATION / PROOF / OFFER'}\n\n"
                    f"PENGETAHUAN BRAND:\n{brand_context or ''}\n\n"
                    f"KEMAMPUAN PENULISAN (skill):\n{skill_context or ''}\n\n"
                    "Keluarkan HANYA JSON murni dengan format:\n"
                    '{"items":[{"topic":"...","target_audience":"...","pillar":"KEY","content_type":"PROPERTY_EDUCATION","angle":"..."}]}\n'
                    f"content_type WAJIB salah satu dari: {', '.join(sorted(cls.VALID_CONTENT_TYPES))}."
                )
                user_prompt = (
                    f"Goal: {goal}\n"
                    f"Jumlah konten yang diinginkan: {count}\n"
                    "Distribusikan pilar secara proporsional (60% edukasi/problematika, 25% bukti kerja, 15% penawaran). "
                    "Setiap item adalah satu poster + caption."
                )
                raw = llm.complete(system=system_prompt, user=user_prompt, response_format="json", max_tokens=2000)
                raw = raw.strip()
                if raw.startswith("```"):
                    raw = raw.split("```", 1)[1].rsplit("```", 1)[0].strip()
                    if raw.startswith("json"):
                        raw = raw[4:].strip()
                data = json.loads(raw)
                for it in data.get("items", [])[:count]:
                    topic = (it.get("topic") or "").strip()
                    if not topic:
                        continue
                    ct = (it.get("content_type") or "").strip().upper()
                    if ct not in cls.VALID_CONTENT_TYPES:
                        ct = None
                    items.append({
                        "topic": topic,
                        "target_audience": (it.get("target_audience") or "Developer & Tim Marketing Properti").strip(),
                        "pillar": cls._normalize_pillar(it.get("pillar"), pillar_index),
                        "content_type": ct,
                        "angle": (it.get("angle") or "").strip()
                    })
            except Exception as e:
                logger.warning(f"AgentPlannerService LLM planning failed: {str(e)}. Falling back to deterministic.")
                items = []

        # Deterministic fallback: rotate through seeded pillars, one brief per pillar.
        if not items:
            pillar_keys = [k for k in pillar_index.keys()] or ["PROBLEM_EDUCATION", "PROOF", "OFFER"]
            for i in range(count):
                key = pillar_keys[i % len(pillar_keys)]
                info = pillar_index.get(key, {})
                sub = (info.get("sub_topics") or [])
                angle = (info.get("example_angles") or [""])[0] if (info.get("example_angles") or []) else ""
                topic = goal.strip()
                items.append({
                    "topic": f"{topic} — {info.get('name', key)}" if i >= len(pillar_keys) else topic,
                    "target_audience": "Developer & Tim Marketing Properti",
                    "pillar": key,
                    "content_type": None,
                    "angle": angle
                })

        return {
            "goal": goal,
            "project_id": project_id,
            "count": len(items),
            "items": items
        }

    @staticmethod
    def build_briefs_from_lines(lines: List[str]) -> Dict[str, Any]:
        """
        Bulk mode: each line is 'topic' or 'topic;audience;pillar' (semicolon or comma separated).
        """
        items: List[Dict[str, Any]] = []
        for line in lines:
            if not line or not line.strip():
                continue
            parts = re.split(r"[;|]", line.strip())
            topic = parts[0].strip()
            if not topic:
                continue
            audience = parts[1].strip() if len(parts) > 1 and parts[1].strip() else "Developer & Tim Marketing Properti"
            pillar = parts[2].strip().upper() if len(parts) > 2 and parts[2].strip() else "PROBLEM_EDUCATION"
            items.append({
                "topic": topic,
                "target_audience": audience,
                "pillar": pillar,
                "content_type": None,
                "angle": ""
            })
        return {"items": items}
