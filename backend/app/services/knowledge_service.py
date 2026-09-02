import io
import json
import re
import zipfile
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from sqlalchemy.orm import Session

from app.models.skill import KnowledgeSkill
from app.models.pillar import ContentPillar
from app.models.brand_context import BrandContext
from app.core.logging import logger


DEFAULT_PILLARS = [
    {
        "key": "PROBLEM_EDUCATION",
        "name": "Problem & Education",
        "business_goal": "Awareness",
        "ratio": 0.6,
        "mapped_content_types": ["PROPERTY_EDUCATION", "PROPERTY_PROBLEM", "PROPERTY_INSIGHT", "PROPERTY_LISTICLE", "PROPERTY_OPINION"],
        "sub_topics": ["Kebocoran leads iklan properti", "Tips follow-up sales", "Perbandingan manual vs otomasi"],
        "example_angles": ["Kenapa leads banyak tapi closing nol?", "3 kesalahan follow-up yang membunuh konversi"],
        "prompt_guidance": "Konten edukatif yang membangun kesadaran dan kepercayaan. Tanpa CTA jualan langsung.",
        "sort_order": 1
    },
    {
        "key": "PROOF",
        "name": "Proof of Work & Demo",
        "business_goal": "Trust",
        "ratio": 0.25,
        "mapped_content_types": ["PROPERTY_CASE_STUDY", "DATA_EDITORIAL", "PROPERTY_SHOWCASE"],
        "sub_topics": ["Studi kasus transformasi klien", "Bedah fitur CRM / automasi", "Showcase unit & yield"],
        "example_angles": ["Cara satu properti naikkan conversion rate 300%", "Rukost premium dekat kampus: yield 12%/tahun"],
        "prompt_guidance": "Bukti hasil nyata, data spesifik, dan showcase yang membangun kredibilitas.",
        "sort_order": 2
    },
    {
        "key": "OFFER",
        "name": "Direct Offer & Invitation",
        "business_goal": "Conversion",
        "ratio": 0.15,
        "mapped_content_types": ["PROPERTY_SALES_OFFER", "SOFT_SELLING"],
        "sub_topics": ["Konsultasi gratis WhatsApp", "Paket fast-track setup sistem", "Audit alur leads gratis"],
        "example_angles": ["Slot audit alur leads gratis terbatas", "Setup sistem leads 5 hari tanpa koding"],
        "prompt_guidance": "Ajakan aksi langsung (CTA wajib). Gunakan: 'Jadwalkan Sesi Audit Gratis' atau 'Konsultasi via WhatsApp'.",
        "sort_order": 3
    }
]

DEFAULT_BRAND_CONTEXT = (
    "# NugiProperti Brand Context\n"
    "Rasio konten 60-25-15: 60% Problem & Education, 25% Proof of Work & Demo, 15% Direct Offer.\n"
    "3 Pilar Pesan: (1) Eliminasi Inefisiensi, (2) Kecepatan & Responsivitas, (3) Kepemilikan & Kustomisasi.\n"
    "Forbidden claims: dilarang mengaku 'Pasti Garansi Omzet Naik 500%'; gunakan 'Menghilangkan potensi kebocoran leads 100%'. "
    "Dilarang mengaku punya 50 programmer; posisikan jujur sebagai Agile Solution Architect & AI Operator."
)


def _knowledge_dir() -> Path:
    import sys
    from app.core.config import settings
    candidates: List[Path] = []
    if getattr(sys, "frozen", False):
        meipass = Path(getattr(sys, "_MEIPASS", "."))
        candidates.append(meipass / "backend" / "knowledge")
        candidates.append(meipass / "knowledge")
    candidates += [
        Path(__file__).resolve().parents[2] / "knowledge",
        Path.cwd() / "knowledge",
        Path.cwd() / "backend" / "knowledge",
        settings.user_data_dir / "knowledge",
    ]
    for c in candidates:
        if (c / "skills").exists() or (c / "brand").exists() or (c / "pillars").exists():
            return c
    return candidates[0]


def _parse_frontmatter(text: str) -> Tuple[str, str, str]:
    """Returns (name, description, body) from a markdown file with --- frontmatter."""
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?", text, re.DOTALL)
    if not m:
        return "", "", text.strip()

    fm = m.group(1)
    body = text[m.end():].strip()

    name = ""
    description = ""
    for key in ("name", "description"):
        km = re.search(rf"^{key}\s*:\s*(.+?)\s*$", fm, re.MULTILINE)
        if km:
            val = km.group(1).strip().strip('"').strip("'")
            if key == "name":
                name = val
            else:
                description = val
    return name, description, body


def _load_pillars() -> List[Dict]:
    pillars_file = _knowledge_dir() / "pillars" / "pillars.json"
    try:
        if pillars_file.exists():
            return json.loads(pillars_file.read_text(encoding="utf-8"))
    except Exception as e:
        logger.warning(f"Failed to load pillars.json: {str(e)}. Using defaults.")
    return DEFAULT_PILLARS


def _tokenize(text: str) -> List[str]:
    return [t for t in re.findall(r"[a-zA-Z0-9]+", (text or "").lower()) if len(t) > 2]


class KnowledgeService:
    """
    Seeds, parses, ingests, and retrieves the reusable knowledge base
    (marketing skills, content-creator psychology, pillar framework, brand context).
    """

    @staticmethod
    def parse_skill_markdown(text: str, fallback_name: str = "") -> Dict[str, str]:
        name, description, body = _parse_frontmatter(text)
        return {
            "name": name or fallback_name,
            "description": description,
            "content": body or text.strip()
        }

    @staticmethod
    def seed_defaults(db: Session) -> Dict[str, int]:
        """Idempotently seeds brand contexts, pillars, and skills from the vendored knowledge directory."""
        kdir = _knowledge_dir()
        result = {"skills": 0, "pillars": 0, "brand": 0}

        # 1. Brand contexts
        brand_dir = kdir / "brand"
        existing_brand_keys = {b.key for b in db.query(BrandContext).all()}
        if brand_dir.exists():
            for f in sorted(brand_dir.glob("*.md")):
                key = f.stem
                if key in existing_brand_keys:
                    continue
                db.add(BrandContext(
                    key=key,
                    name=key.replace("-", " ").title(),
                    content=f.read_text(encoding="utf-8")
                ))
                existing_brand_keys.add(key)
                result["brand"] += 1
        if not existing_brand_keys:
            db.add(BrandContext(key="brand-context", name="Brand Context", content=DEFAULT_BRAND_CONTEXT))
            existing_brand_keys.add("brand-context")
            result["brand"] += 1

        # 2. Pillars
        existing_pillar_keys = {p.key for p in db.query(ContentPillar).all()}
        for p in _load_pillars():
            if p["key"] in existing_pillar_keys:
                continue
            db.add(ContentPillar(**p))
            existing_pillar_keys.add(p["key"])
            result["pillars"] += 1

        # 3. Skills
        skills_dir = kdir / "skills"
        existing_skill_names = {
            (s.name, s.source) for s in db.query(KnowledgeSkill).all()
        }
        if skills_dir.exists():
            for f in sorted(skills_dir.glob("*.md")):
                parsed = KnowledgeService.parse_skill_markdown(
                    f.read_text(encoding="utf-8"), fallback_name=f.stem
                )
                if not parsed["name"] or (parsed["name"], "seeded") in existing_skill_names:
                    continue
                db.add(KnowledgeSkill(
                    name=parsed["name"],
                    description=parsed["description"],
                    category="seeded",
                    content=parsed["content"],
                    source="seeded",
                    file_path=str(f)
                ))
                existing_skill_names.add((parsed["name"], "seeded"))
                result["skills"] += 1

        db.commit()
        logger.info(f"Knowledge seeded: {result}")
        return result

    @staticmethod
    def ingest_file(db: Session, filename: str, content: str) -> KnowledgeSkill:
        parsed = KnowledgeService.parse_skill_markdown(content, fallback_name=Path(filename).stem)
        if not parsed["name"]:
            parsed["name"] = Path(filename).stem

        existing = db.query(KnowledgeSkill).filter(
            KnowledgeSkill.name == parsed["name"], KnowledgeSkill.source == "uploaded"
        ).first()
        if existing:
            existing.description = parsed["description"]
            existing.content = parsed["content"]
            existing.file_path = filename
        else:
            existing = KnowledgeSkill(
                name=parsed["name"],
                description=parsed["description"],
                category="uploaded",
                content=parsed["content"],
                source="uploaded",
                file_path=filename
            )
            db.add(existing)
        db.commit()
        db.refresh(existing)
        return existing

    @staticmethod
    def ingest_zip(db: Session, data: bytes) -> List[KnowledgeSkill]:
        result: List[KnowledgeSkill] = []
        with zipfile.ZipFile(io.BytesIO(data)) as zf:
            for name in zf.namelist():
                if name.endswith("/") or not name.lower().endswith((".md", ".markdown")):
                    continue
                try:
                    content = zf.read(name).decode("utf-8", errors="replace")
                except Exception:
                    continue
                result.append(KnowledgeService.ingest_file(db, name, content))
        return result

    @staticmethod
    def retrieve_relevant_skills(db: Session, topic: str, pillar: Optional[str] = None, limit: int = 3) -> str:
        skills = db.query(KnowledgeSkill).filter(KnowledgeSkill.enabled.is_(True)).all()
        parts: List[str] = []
        if skills:
            topic_tokens = set(_tokenize(topic))
            scored: List[Tuple[int, KnowledgeSkill]] = []
            for s in skills:
                haystack = f"{s.name or ''} {s.description or ''}".lower()
                overlap = len(topic_tokens & set(_tokenize(haystack)))
                if pillar and pillar.lower() in haystack:
                    overlap += 2
                if topic.lower()[:12] in haystack:
                    overlap += 1
                scored.append((overlap, s))

            scored.sort(key=lambda x: (-x[0], x[1].name))
            chosen = [s for ov, s in scored[:limit] if ov > 0]
            if not chosen:
                chosen = [s for _, s in scored[:limit]]
            parts.append("\n\n".join([f"### SKILL: {s.name}\n{s.content}" for s in chosen]))

        # Append externally-indexed supporting docs from the business repository.
        try:
            from app.knowledge.source import KnowledgeSource
            external = KnowledgeSource.supporting_for_topic(topic, pillar, limit=limit)
            if external:
                parts.append(external)
        except Exception as e:
            logger.warning(f"External knowledge retrieval skipped: {str(e)}")

        return "\n\n".join([p for p in parts if p])

    @staticmethod
    def get_brand_context(db: Session) -> str:
        rows = db.query(BrandContext).all()
        parts: List[str] = [r.content for r in rows]
        try:
            from app.knowledge.source import KnowledgeSource
            external = KnowledgeSource.core_context()
            if external:
                parts.append("# SUMBER PENGETAHUAN BISNIS (freelance-nugi-software-engineer)\n" + external)
        except Exception as e:
            logger.warning(f"External core knowledge skipped: {str(e)}")
        return "\n\n".join([p for p in parts if p])
