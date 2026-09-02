from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models.project import Project
from app.models.content import Content
from app.services import batch_generation_service
from app.services.batch_generation_service import BatchGenerationService


def _setup_db(tmp_path):
    db_file = tmp_path / "test_batch.db"
    engine = create_engine(f"sqlite:///{db_file}", connect_args={"check_same_thread": False}, future=True)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine, expire_on_commit=False, future=True)
    return engine, Session


def _count_content(session):
    return session.query(Content).count()


def test_batch_resume_does_not_duplicate_content(tmp_path, monkeypatch):
    engine, Session = _setup_db(tmp_path)
    monkeypatch.setattr(batch_generation_service, "SessionLocal", Session)

    session = Session()
    project = Project(name="Batch Reliability Test", slug="batch-reliability-test")
    session.add(project)
    session.commit()
    project_id = project.id

    items = [
        {"topic": "Kenapa leads properti dingin?", "pillar": "PROBLEM_EDUCATION"},
        {"topic": "5 kesalahan follow up sales properti", "pillar": "PROOF"},
    ]

    run = BatchGenerationService.create_run(session, project_id, "bulk", "goal test", items)
    run_id = run.id
    session.close()

    # First full execution.
    BatchGenerationService.execute_batch(run_id)
    session = Session()
    assert _count_content(session) == 2
    assert session.query(Content).filter(Content.id.like("b%")).count() == 2
    session.close()

    # Re-running a completed batch must not duplicate anything.
    BatchGenerationService.execute_batch(run_id)
    session = Session()
    assert _count_content(session) == 2
    session.close()

    # Simulate a crash: one item was persisted but never marked COMPLETED.
    session = Session()
    from app.models.batch import BatchItem
    item = session.query(BatchItem).filter(BatchItem.batch_run_id == run_id).order_by(BatchItem.sort_order).first()
    item.status = "RUNNING"
    session.commit()
    session.close()

    BatchGenerationService.execute_batch(run_id)
    session = Session()
    # Same 2 contents; the resumed item was upserted, not duplicated.
    assert _count_content(session) == 2
    assert session.query(Content).filter(Content.id.like("b%")).count() == 2
    run = session.query(type(run)).filter(type(run).id == run_id).first()
    assert run.status == "COMPLETED"
    assert run.completed_items == run.total_items
    assert "estimated_cost_usd" in (run.summary or {})
    session.close()
