from sqlalchemy import Column, String, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class ContentBrief(BaseModel):
    """
    Captures marketing campaign parameters and inputs that feed into the AI reasoning stage.
    """
    __tablename__ = "content_briefs"

    project_id = Column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    topic = Column(Text, nullable=False) # e.g. "Tips follow up leads iklan properti agar tidak dingin"
    target_audience = Column(String(200), nullable=False) # e.g. "Property Sales & Developer Marketing Manager"
    content_pillar = Column(String(100), default="educational", nullable=False) # educational, authority, direct_offer, case_study
    tone_of_voice = Column(String(100), default="professional_authoritative", nullable=False)
    primary_platform = Column(String(50), default="instagram", nullable=False)
    key_takeaway = Column(Text, nullable=True)
    metadata_json = Column(JSON, default=dict, nullable=False)

    # Relationships
    project = relationship("Project", back_populates="briefs")
    contents = relationship("Content", back_populates="brief", cascade="all, delete-orphan")
    jobs = relationship("GenerationJob", back_populates="brief")
