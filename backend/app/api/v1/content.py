from typing import List, Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from app.models.content import Content
from app.schemas.content import ContentResponse
from app.schemas.generation import GenerationRequest, GenerationResponse
from app.schemas.editorial_agent import UserBriefInput
from app.services.content_generation_agent import ContentGenerationAgent
from app.services.job_service import JobService
from app.services.knowledge_service import KnowledgeService
from app.core.errors import NotFoundError

router = APIRouter(prefix="/content", tags=["Content"])
agent = ContentGenerationAgent()


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
    Triggers the unified content production pipeline:
    Strategy ➔ Copy ➔ Art Direction ➔ Background (Image Provider) ➔
    Deterministic Render (Pillow) ➔ Visual QA ➔ Persistence.
    """
    job = JobService.create_job(
        db=db,
        project_id=payload.project_id,
        brief_id=payload.brief_id,
        job_type="single_content_generation",
        payload={"topic": payload.topic, "audience": payload.target_audience, "pillar": payload.content_pillar}
    )

    try:
        brand_context = KnowledgeService.get_brand_context(db)
        skill_context = KnowledgeService.retrieve_relevant_skills(db, payload.topic)

        brief = UserBriefInput(
            topic=payload.topic,
            target_audience=payload.target_audience,
            project_id=payload.project_id
        )
        pkg = agent.generate_full_package(
            brief=brief,
            db=db,
            skill_context=skill_context,
            brand_context=brand_context
        )

        qa_status = "PASSED" if pkg.visual_qa.score >= 85 else "WARNING"
        qa_dict = {
            "status": qa_status,
            "score": pkg.visual_qa.score,
            "issues": pkg.visual_qa.issues,
            "recommendations": pkg.visual_qa.recommendations
        }
        render_metadata = {
            "content_type": pkg.content_type.value,
            "archetype": pkg.art_direction_spec.archetype.value,
            "cta_policy": pkg.editorial_spec.cta_policy.value
        }

        result_payload = {
            "content_id": pkg.content_id,
            "asset_path": pkg.rendered_asset_path,
            "headline": pkg.editorial_spec.headline,
            "qa_status": qa_status
        }
        JobService.complete_job(db, job, result=result_payload)

        return {
            "success": True,
            "job_id": job.id,
            "content_id": pkg.content_id,
            "headline": pkg.editorial_spec.headline,
            "hook_text": pkg.editorial_spec.subheadline,
            "body_caption": pkg.editorial_spec.caption,
            "hashtags": "#Properti #NugiProperti",
            "call_to_action": pkg.editorial_spec.cta_text or "",
            "asset_path": pkg.rendered_asset_path,
            "asset_url": pkg.rendered_asset_url,
            "qa_result": qa_dict,
            "render_metadata": render_metadata
        }
    except Exception as e:
        db.rollback()
        JobService.fail_job(db, job, error_message=str(e))
        raise
