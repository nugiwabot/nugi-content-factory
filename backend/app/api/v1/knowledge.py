from typing import List

from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, Body
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.skill import KnowledgeSkill
from app.models.pillar import ContentPillar
from app.models.brand_context import BrandContext
from app.schemas.knowledge import (
    SkillOut,
    PillarOut,
    PillarUpdate,
    BrandContextOut,
    SeedResult,
    UploadResult
)
from app.services.knowledge_service import KnowledgeService
from app.core.errors import NotFoundError
from app.core.logging import logger

router = APIRouter(prefix="/knowledge", tags=["Knowledge Base"])


@router.get("/skills", response_model=List[SkillOut])
def list_skills(db: Session = Depends(get_db)):
    """Lists all knowledge skills (seeded + uploaded)."""
    return db.query(KnowledgeSkill).order_by(KnowledgeSkill.source, KnowledgeSkill.name).all()


@router.post("/upload", response_model=UploadResult)
async def upload_skill(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Uploads a single skill.md / .md file or a .zip containing multiple .md files."""
    filename = file.filename or "skill.md"
    data = await file.read()

    if filename.lower().endswith(".zip"):
        skills = KnowledgeService.ingest_zip(db, data)
    elif filename.lower().endswith((".md", ".markdown")):
        content = data.decode("utf-8", errors="replace")
        skills = [KnowledgeService.ingest_file(db, filename, content)]
    else:
        raise HTTPException(status_code=400, detail="Hanya menerima file .md atau .zip berisi file .md.")

    logger.info(f"Uploaded knowledge: {len(skills)} skill(s) from '{filename}'.")
    return UploadResult(skills=skills, count=len(skills))


@router.delete("/skills/{skill_id}")
def delete_skill(skill_id: str, db: Session = Depends(get_db)):
    skill = db.query(KnowledgeSkill).filter(KnowledgeSkill.id == skill_id).first()
    if not skill:
        raise NotFoundError("KnowledgeSkill", skill_id)
    db.delete(skill)
    db.commit()
    return {"success": True, "deleted": skill_id}


@router.get("/pillars", response_model=List[PillarOut])
def list_pillars(db: Session = Depends(get_db)):
    return db.query(ContentPillar).order_by(ContentPillar.sort_order).all()


@router.put("/pillars/{pillar_id}", response_model=PillarOut)
def update_pillar(pillar_id: str, payload: PillarUpdate, db: Session = Depends(get_db)):
    pillar = db.query(ContentPillar).filter(ContentPillar.id == pillar_id).first()
    if not pillar:
        raise NotFoundError("ContentPillar", pillar_id)

    data = payload.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(pillar, field, value)
    db.commit()
    db.refresh(pillar)
    return pillar


@router.get("/brand", response_model=List[BrandContextOut])
def list_brand_contexts(db: Session = Depends(get_db)):
    return db.query(BrandContext).order_by(BrandContext.key).all()


@router.post("/seed", response_model=SeedResult)
def seed_knowledge(db: Session = Depends(get_db)):
    """Re-runs idempotent knowledge seeding."""
    return KnowledgeService.seed_defaults(db)


@router.get("/source")
def get_knowledge_source():
    """Returns external business-knowledge source status (read-only path)."""
    from app.knowledge.source import KnowledgeSource
    return KnowledgeSource.status()


@router.post("/source")
def set_knowledge_source(path: str = Body(..., embed=True)):
    """Sets and re-indexes the external business-knowledge source path."""
    from app.knowledge.source import KnowledgeSource
    try:
        KnowledgeSource.set_source_path(path)
        KnowledgeSource.refresh()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return KnowledgeSource.status()


@router.post("/source/rescan")
def rescan_knowledge_source():
    """Re-reads the external business-knowledge repository from disk."""
    from app.knowledge.source import KnowledgeSource
    KnowledgeSource.refresh()
    return KnowledgeSource.status()
