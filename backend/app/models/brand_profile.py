from sqlalchemy import Column, String, Text, JSON
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class BrandProfile(BaseModel):
    """
    Stores brand guidelines, color palettes, typography, and default voice for deterministic rendering.
    """
    __tablename__ = "brand_profiles"

    name = Column(String(100), nullable=False, unique=True, index=True)
    tagline = Column(String(200), nullable=True)
    primary_color = Column(String(20), default="#0f172a", nullable=False) # Hex
    secondary_color = Column(String(20), default="#38bdf8", nullable=False)
    accent_color = Column(String(20), default="#10b981", nullable=False)
    font_family = Column(String(50), default="sans-serif", nullable=False)
    logo_path = Column(String(255), nullable=True)
    default_target_audience = Column(String(200), nullable=True)
    default_cta_text = Column(String(200), nullable=True)
    metadata_json = Column(JSON, default=dict, nullable=False)

    # Relationships
    projects = relationship("Project", back_populates="brand_profile")
    contents = relationship("Content", back_populates="brand_profile")
