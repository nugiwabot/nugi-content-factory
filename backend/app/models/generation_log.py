from sqlalchemy import Column, String, Integer, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class GenerationLog(BaseModel):
    """
    Detailed audit log tracking provider interactions, prompt tokens, and latency.
    """
    __tablename__ = "generation_logs"

    job_id = Column(String(36), ForeignKey("generation_jobs.id", ondelete="CASCADE"), nullable=True, index=True)
    content_id = Column(String(36), ForeignKey("contents.id", ondelete="CASCADE"), nullable=True, index=True)

    provider_type = Column(String(50), nullable=False) # LLM, ImageGenerator, Renderer
    provider_name = Column(String(50), nullable=False) # MockLLMProvider, MockImageProvider, FluxProvider
    model_name = Column(String(100), nullable=False)
    
    prompt_text = Column(Text, nullable=True)
    response_payload = Column(JSON, default=dict, nullable=False)
    latency_ms = Column(Integer, nullable=True)
    status = Column(String(30), default="SUCCESS", nullable=False) # SUCCESS, FAILED
    error_details = Column(Text, nullable=True)

    # Relationships
    job = relationship("GenerationJob", back_populates="logs")
    content = relationship("Content", back_populates="logs")
