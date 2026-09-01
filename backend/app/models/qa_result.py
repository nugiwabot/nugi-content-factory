from sqlalchemy import Column, String, Float, Boolean, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class QAResult(BaseModel):
    """
    Stores automated deterministic quality checks for typography, contrast, and layout bounds.
    """
    __tablename__ = "qa_results"

    content_id = Column(String(36), ForeignKey("contents.id", ondelete="CASCADE"), nullable=False, index=True)

    status = Column(String(30), default="PASSED", nullable=False) # PASSED, FAILED, WARNING
    contrast_score = Column(Float, nullable=True) # Estimated contrast ratio
    text_overflow_detected = Column(Boolean, default=False, nullable=False)
    headline_length_chars = Column(Float, nullable=True)
    body_length_chars = Column(Float, nullable=True)
    
    issues_json = Column(JSON, default=list, nullable=False)
    recommendations_json = Column(JSON, default=list, nullable=False)

    # Relationships
    content = relationship("Content", back_populates="qa_results")
