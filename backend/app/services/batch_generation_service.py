from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.batch import BatchRun, BatchItem
from app.models.job import GenerationJob
from app.models.project import Project
from app.core.errors import NotFoundError, ValidationError
from app.core.logging import logger
from app.schemas.editorial_agent import UserBriefInput, ContentType
from app.services.content_generation_agent import ContentGenerationAgent
from app.services.job_service import JobService
from app.services.knowledge_service import KnowledgeService


class BatchGenerationService:
    """
    Orchestrates multi-content batch runs in the background, tracking progress
    through GenerationJob and BatchRun, and persisting each result as a BatchItem.
    """

    @staticmethod
    def create_run(
        db: Session,
        project_id: str,
        mode: str,
        goal: Optional[str],
        items: List[Dict[str, Any]]
    ) -> BatchRun:
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise NotFoundError("Project", project_id)
        if not items:
            raise ValidationError("Batch requires at least one content item.")

        job = JobService.create_job(
            db=db,
            project_id=project_id,
            job_type="batch_content_generation",
            payload={"mode": mode, "goal": goal, "total": len(items)}
        )

        run = BatchRun(
            project_id=project_id,
            mode=mode,
            goal=goal,
            status="QUEUED",
            job_id=job.id,
            total_items=len(items)
        )
        db.add(run)
        db.commit()
        db.refresh(run)

        for idx, it in enumerate(items):
            db.add(BatchItem(
                batch_run_id=run.id,
                topic=it.get("topic") or "",
                pillar=it.get("pillar"),
                content_type=it.get("content_type"),
                sort_order=idx
            ))
        db.commit()
        logger.info(f"Created BatchRun {run.id} with {len(items)} items (mode={mode}).")
        return run

    @staticmethod
    def execute_batch(run_id: str) -> None:
        """Runs the batch loop in a fresh DB session (background task)."""
        db = SessionLocal()
        agent = ContentGenerationAgent()
        try:
            run = db.query(BatchRun).filter(BatchRun.id == run_id).first()
            if not run:
                return

            run.status = "RUNNING"
            db.commit()

            job = db.query(GenerationJob).filter(GenerationJob.id == run.job_id).first()
            if job:
                JobService.update_progress(db, job, 5, "RUNNING")

            brand_context = KnowledgeService.get_brand_context(db)
            items = db.query(BatchItem).filter(BatchItem.batch_run_id == run.id).order_by(BatchItem.sort_order).all()
            total = max(len(items), 1)

            for idx, item in enumerate(items):
                try:
                    item.status = "RUNNING"
                    db.commit()

                    skill_context = KnowledgeService.retrieve_relevant_skills(db, item.topic, item.pillar)
                    content_type_override = None
                    if item.content_type and item.content_type in {ct.value for ct in ContentType}:
                        content_type_override = ContentType(item.content_type)

                    brief = UserBriefInput(
                        topic=item.topic,
                        target_audience="Developer & Tim Marketing Properti",
                        content_type_override=content_type_override,
                        project_id=run.project_id
                    )

                    pkg = agent.generate_full_package(
                        brief=brief,
                        db=db,
                        skill_context=skill_context,
                        brand_context=brand_context
                    )

                    item.content_type = pkg.content_type.value
                    item.headline = pkg.editorial_spec.headline
                    item.caption = pkg.editorial_spec.caption
                    item.asset_path = pkg.rendered_asset_path
                    item.asset_url = pkg.rendered_asset_url
                    item.status = "COMPLETED"
                    item.error = None
                    db.commit()

                except Exception as e:
                    logger.exception(f"BatchItem {item.id} failed: {str(e)}")
                    item.status = "FAILED"
                    item.error = str(e)
                    db.commit()

                run.completed_items += 1
                run.status = "RUNNING"
                db.commit()

                if job:
                    progress = 5 + int(95 * run.completed_items / total)
                    JobService.update_progress(db, job, progress, "RUNNING")

            run.status = "COMPLETED"
            run.summary = {
                "mode": run.mode,
                "goal": run.goal,
                "total_items": run.total_items,
                "completed_items": run.completed_items
            }
            db.commit()

            if job:
                JobService.complete_job(db, job, result={"batch_run_id": run.id, "status": "COMPLETED"})

            logger.info(f"BatchRun {run.id} completed: {run.completed_items}/{run.total_items} items.")
        except Exception as e:
            logger.exception(f"BatchRun {run_id} failed: {str(e)}")
            db.rollback()
            run = db.query(BatchRun).filter(BatchRun.id == run_id).first()
            if run:
                run.status = "FAILED"
                run.summary = {"error": str(e)}
                db.commit()
                job = db.query(GenerationJob).filter(GenerationJob.id == run.job_id).first()
                if job:
                    JobService.fail_job(db, job, str(e))
        finally:
            db.close()
