from typing import List, Optional

from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.batch import BatchRun, BatchItem
from app.schemas.batch import (
    PlanRequest,
    BatchRunRequest,
    BatchRunOut,
    BatchRunDetailOut
)
from app.services.agent_planner_service import AgentPlannerService
from app.services.batch_generation_service import BatchGenerationService
from app.core.errors import NotFoundError, ValidationError

router = APIRouter(prefix="/batch", tags=["Batch Content Generation"])


@router.post("/plan")
def plan_batch(req: PlanRequest, db: Session = Depends(get_db)):
    """Autonomously plans a list of content briefs from a single goal."""
    return AgentPlannerService.plan_from_goal(
        db=db,
        goal=req.goal,
        count=req.count,
        project_id=req.project_id
    )


@router.post("/run", response_model=BatchRunOut)
def run_batch(
    req: BatchRunRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Creates and starts a batch generation run in the background."""
    project_id = req.project_id
    if not project_id:
        raise ValidationError("project_id wajib diisi untuk menjalankan batch.")

    if req.mode == "bulk":
        lines = req.lines or []
        if not any(line.strip() for line in lines):
            raise ValidationError("Mode bulk memerlukan minimal satu baris topik.")
        plan = AgentPlannerService.build_briefs_from_lines(lines)
        items = plan["items"]
        goal = req.goal or ("Bulk generation dari " + str(len(items)) + " topik")
    else:
        items = req.items or []
        if not items:
            raise ValidationError("Mode plan memerlukan daftar items hasil planning.")
        goal = req.goal or ("Batch plan dengan " + str(len(items)) + " item")

    run = BatchGenerationService.create_run(
        db=db,
        project_id=project_id,
        mode=req.mode,
        goal=goal,
        items=items
    )
    background_tasks.add_task(BatchGenerationService.execute_batch, run.id)
    return run


@router.get("/runs", response_model=List[BatchRunOut])
def list_batch_runs(project_id: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(BatchRun)
    if project_id:
        query = query.filter(BatchRun.project_id == project_id)
    return query.order_by(BatchRun.created_at.desc()).all()


@router.get("/runs/{run_id}", response_model=BatchRunDetailOut)
def get_batch_run(run_id: str, db: Session = Depends(get_db)):
    run = db.query(BatchRun).filter(BatchRun.id == run_id).first()
    if not run:
        raise NotFoundError("BatchRun", run_id)
    items = db.query(BatchItem).filter(BatchItem.batch_run_id == run.id).order_by(BatchItem.sort_order).all()
    return BatchRunDetailOut(
        id=run.id,
        project_id=run.project_id,
        mode=run.mode,
        goal=run.goal,
        status=run.status,
        job_id=run.job_id,
        total_items=run.total_items,
        completed_items=run.completed_items,
        summary=run.summary or {},
        created_at=run.created_at,
        updated_at=run.updated_at,
        items=items
    )


@router.post("/runs/{run_id}/resume", response_model=BatchRunOut)
def resume_batch(
    run_id: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Resumes a FAILED/interrupted batch run without regenerating completed items."""
    run = db.query(BatchRun).filter(BatchRun.id == run_id).first()
    if not run:
        raise NotFoundError("BatchRun", run_id)
    background_tasks.add_task(BatchGenerationService.execute_batch, run.id)
    return run
