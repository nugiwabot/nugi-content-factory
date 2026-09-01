from typing import List, Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from app.models.content import Content
from app.schemas.content import ContentResponse
from app.schemas.generation import GenerationRequest, GenerationResponse
from app.services.orchestration_service import OrchestrationService
from app.core.errors import NotFoundError

router = APIRouter(prefix="/content", tags=["Content"])
orchestration_service = OrchestrationService()


@router.get("", response_model=List[ContentResponse])
def list_content(
    project_id: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Lists generated marketing content items with assets and QA results."""
    query = db.query(Content).options(
        joinedload(Content.assets),
        joinedload(Content.qa_results)
    )
    if project_id:
        query = query.filter(Content.project_id == project_id)
    if status:
        query = query.filter(Content.status == status)

    return query.order_by(Content.created_at.desc()).all()


@router.get("/{content_id}", response_model=ContentResponse)
def get_content(content_id: str, db: Session = Depends(get_db)):
    """Retrieves single content item by ID."""
    content = db.query(Content).options(
        joinedload(Content.assets),
        joinedload(Content.qa_results)
    ).filter(Content.id == content_id).first()
    if not content:
        raise NotFoundError("Content", content_id)
    return content


@router.post("/generate", response_model=GenerationResponse, status_code=status.HTTP_201_CREATED)
def generate_content(payload: GenerationRequest, db: Session = Depends(get_db)):
    """
    Triggers end-to-end content production pipeline:
    Reasoning (LLM) ➔ Background (Image) ➔ Deterministic Render (Pillow) ➔ QA Validation ➔ Persistence.
    """
    result = orchestration_service.generate_single_content(
        db=db,
        project_id=payload.project_id,
        topic=payload.topic,
        target_audience=payload.target_audience,
        content_pillar=payload.content_pillar,
        tone_of_voice=payload.tone_of_voice,
        brief_id=payload.brief_id,
        brand_profile_id=payload.brand_profile_id,
        llm_provider_type=payload.llm_provider,
        image_provider_type=payload.image_provider
    )
    return result
