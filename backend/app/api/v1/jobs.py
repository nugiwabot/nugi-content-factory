from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.job import GenerationJob
from app.schemas.job import JobResponse
from app.core.errors import NotFoundError

router = APIRouter(prefix="/jobs", tags=["Generation Jobs"])


@router.get("", response_model=List[JobResponse])
def list_jobs(project_id: Optional[str] = None, db: Session = Depends(get_db)):
    """Lists generation jobs."""
    query = db.query(GenerationJob)
    if project_id:
        query = query.filter(GenerationJob.project_id == project_id)
    return query.order_by(GenerationJob.created_at.desc()).all()


@router.get("/{job_id}", response_model=JobResponse)
def get_job(job_id: str, db: Session = Depends(get_db)):
    """Polls status, progress, and result of a generation job."""
    job = db.query(GenerationJob).filter(GenerationJob.id == job_id).first()
    if not job:
        raise NotFoundError("GenerationJob", job_id)
    return job
