from sqlalchemy import Column, String, Text, ForeignKey, Integer, JSON
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class Content(BaseModel):
    """
    Represents an individual generated content piece (copy + prompt + rendered assets).
    """
    __tablename__ = "contents"

    project_id = Column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    brief_id = Column(String(36), ForeignKey("content_briefs.id", ondelete="SET NULL"), nullable=True, index=True)
    brand_profile_id = Column(String(36), ForeignKey("brand_profiles.id", ondelete="SET NULL"), nullable=True)
    template_id = Column(String(36), ForeignKey("templates.id", ondelete="SET NULL"), nullable=True)

    headline = Column(String(255), nullable=False)
    hook_text = Column(String(255), nullable=True)
    body_caption = Column(Text, nullable=False)
    hashtags = Column(String(255), nullable=True)
    call_to_action = Column(String(200), nullable=True)
    visual_concept_prompt = Column(Text, nullable=True) # Background generation prompt

    status = Column(String(50), default="DRAFT", nullable=False) # DRAFT, GENERATED, QA_PASSED, APPROVED, ARCHIVED
    revision_count = Column(Integer, default=0, nullable=False)
    metadata_json = Column(JSON, default=dict, nullable=False)

    # Relationships
    project = relationship("Project", back_populates="contents")
    brief = relationship("ContentBrief", back_populates="contents")
    brand_profile = relationship("BrandProfile", back_populates="contents")
    template = relationship("Template", back_populates="contents")
    assets = relationship("Asset", back_populates="content", cascade="all, delete-orphan")
    qa_results = relationship("QAResult", back_populates="content", cascade="all, delete-orphan")
    logs = relationship("GenerationLog", back_populates="content", cascade="all, delete-orphan")
