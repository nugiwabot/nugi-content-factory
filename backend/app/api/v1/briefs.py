from typing import List, Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.brief import ContentBrief
from app.models.project import Project
from app.schemas.brief import BriefCreate, BriefResponse
from app.core.errors import NotFoundError

router = APIRouter(prefix="/briefs", tags=["Content Briefs"])


@router.get("", response_model=List[BriefResponse])
def list_briefs(project_id: Optional[str] = None, db: Session = Depends(get_db)):
    """Lists content briefs, optionally filtered by project_id."""
    query = db.query(ContentBrief)
    if project_id:
        query = query.filter(ContentBrief.project_id == project_id)
    return query.order_by(ContentBrief.created_at.desc()).all()


@router.post("", response_model=BriefResponse, status_code=status.HTTP_201_CREATED)
def create_brief(payload: BriefCreate, db: Session = Depends(get_db)):
    """Creates a new marketing content brief."""
    project = db.query(Project).filter(Project.id == payload.project_id).first()
    if not project:
        raise NotFoundError("Project", payload.project_id)

    brief = ContentBrief(
        project_id=payload.project_id,
        title=payload.title,
        topic=payload.topic,
        target_audience=payload.target_audience,
        content_pillar=payload.content_pillar,
        tone_of_voice=payload.tone_of_voice,
        primary_platform=payload.primary_platform,
        key_takeaway=payload.key_takeaway,
        metadata_json=payload.metadata_json
    )
    db.add(brief)
    db.commit()
    db.refresh(brief)
    return brief


@router.get("/{brief_id}", response_model=BriefResponse)
def get_brief(brief_id: str, db: Session = Depends(get_db)):
    """Retrieves content brief by ID."""
    brief = db.query(ContentBrief).filter(ContentBrief.id == brief_id).first()
    if not brief:
        raise NotFoundError("ContentBrief", brief_id)
    return brief
