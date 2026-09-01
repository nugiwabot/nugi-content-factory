from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models.job import GenerationJob
from app.core.logging import logger


class JobService:
    """
    Manages generation job lifecycle state transitions.
    """
    @staticmethod
    def create_job(
        db: Session,
        project_id: str,
        brief_id: Optional[str] = None,
        job_type: str = "single_content_generation",
        payload: Optional[Dict[str, Any]] = None
    ) -> GenerationJob:
        job = GenerationJob(
            project_id=project_id,
            brief_id=brief_id,
            job_type=job_type,
            status="QUEUED",
            progress_percentage=0,
            job_payload=payload or {}
        )
        db.add(job)
        db.commit()
        db.refresh(job)
        logger.info(f"Created GenerationJob {job.id} (Status: QUEUED)")
        return job

    @staticmethod
    def update_progress(
        db: Session,
        job: GenerationJob,
        progress: int,
        status: str = "RUNNING"
    ) -> GenerationJob:
        job.progress_percentage = progress
        job.status = status
        db.commit()
        db.refresh(job)
        return job

    @staticmethod
    def complete_job(
        db: Session,
        job: GenerationJob,
        result: Dict[str, Any]
    ) -> GenerationJob:
        job.progress_percentage = 100
        job.status = "COMPLETED"
        job.job_result = result
        db.commit()
        db.refresh(job)
        logger.info(f"Completed GenerationJob {job.id} successfully.")
        return job

    @staticmethod
    def fail_job(
        db: Session,
        job: GenerationJob,
        error_message: str
    ) -> GenerationJob:
        job.status = "FAILED"
        job.error_message = error_message
        db.commit()
        db.refresh(job)
        logger.error(f"Failed GenerationJob {job.id}: {error_message}")
        return job
