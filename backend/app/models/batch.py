from sqlalchemy import Column, String, Integer, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class BatchRun(BaseModel):
    """
    Tracks a multi-content generation run (mode 'plan' or 'bulk') executed in the background.
    """
    __tablename__ = "batch_runs"

    project_id = Column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    mode = Column(String(20), default="plan", nullable=False)  # plan | bulk
    goal = Column(Text, nullable=True)
    status = Column(String(30), default="QUEUED", nullable=False)  # QUEUED, RUNNING, COMPLETED, FAILED, CANCELLED
    job_id = Column(String(36), nullable=True, index=True)
    total_items = Column(Integer, default=0, nullable=False)
    completed_items = Column(Integer, default=0, nullable=False)
    summary = Column(JSON, default=dict, nullable=False)

    items = relationship("BatchItem", back_populates="batch_run", cascade="all, delete-orphan")


class BatchItem(BaseModel):
    """
    A single generated poster + caption within a batch run.
    """
    __tablename__ = "batch_items"

    batch_run_id = Column(String(36), ForeignKey("batch_runs.id", ondelete="CASCADE"), nullable=False, index=True)
    topic = Column(String(500), nullable=False)
    pillar = Column(String(80), nullable=True)
    content_type = Column(String(80), nullable=True)
    headline = Column(String(255), nullable=True)
    caption = Column(Text, nullable=True)
    asset_path = Column(String(255), nullable=True)
    asset_url = Column(String(500), nullable=True)
    status = Column(String(30), default="PENDING", nullable=False)  # PENDING, RUNNING, COMPLETED, FAILED
    error = Column(Text, nullable=True)
    sort_order = Column(Integer, default=0, nullable=False)

    batch_run = relationship("BatchRun", back_populates="items")
