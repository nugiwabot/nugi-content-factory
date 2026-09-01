from sqlalchemy import Column, String, Integer, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class GenerationJob(BaseModel):
    """
    Tracks state machine lifecycle for async and batch content generation pipelines.
    """
    __tablename__ = "generation_jobs"

    project_id = Column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    brief_id = Column(String(36), ForeignKey("content_briefs.id", ondelete="SET NULL"), nullable=True)
    
    job_type = Column(String(50), default="single_content_generation", nullable=False)
    status = Column(String(30), default="QUEUED", nullable=False, index=True) # QUEUED, RUNNING, COMPLETED, FAILED, CANCELLED
    progress_percentage = Column(Integer, default=0, nullable=False)
    
    error_message = Column(Text, nullable=True)
    job_payload = Column(JSON, default=dict, nullable=False)
    job_result = Column(JSON, default=dict, nullable=False)

    # Relationships
    project = relationship("Project", back_populates="jobs")
    brief = relationship("ContentBrief", back_populates="jobs")
    logs = relationship("GenerationLog", back_populates="job", cascade="all, delete-orphan")
