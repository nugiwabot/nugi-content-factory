from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class Project(BaseModel):
    """
    Groups marketing content, assets, and briefs under a specific property project or business workspace.
    """
    __tablename__ = "projects"

    name = Column(String(150), nullable=False, index=True)
    slug = Column(String(160), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    brand_profile_id = Column(String(36), ForeignKey("brand_profiles.id", ondelete="SET NULL"), nullable=True)

    # Relationships
    brand_profile = relationship("BrandProfile", back_populates="projects")
    briefs = relationship("ContentBrief", back_populates="project", cascade="all, delete-orphan")
    contents = relationship("Content", back_populates="project", cascade="all, delete-orphan")
    jobs = relationship("GenerationJob", back_populates="project", cascade="all, delete-orphan")
    assets = relationship("Asset", back_populates="project", cascade="all, delete-orphan")
