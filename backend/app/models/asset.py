from sqlalchemy import Column, String, Integer, BigInteger, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class Asset(BaseModel):
    """
    Physical rendered files and image assets associated with content.
    """
    __tablename__ = "assets"

    project_id = Column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    content_id = Column(String(36), ForeignKey("contents.id", ondelete="CASCADE"), nullable=True, index=True)

    asset_type = Column(String(50), default="rendered_final", nullable=False) # background_raw, rendered_final, logo, icon
    file_path = Column(String(500), nullable=False)
    file_url = Column(String(500), nullable=True)
    mime_type = Column(String(50), default="image/png", nullable=False)
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    file_size_bytes = Column(BigInteger, nullable=True)
    metadata_json = Column(JSON, default=dict, nullable=False)

    # Relationships
    project = relationship("Project", back_populates="assets")
    content = relationship("Content", back_populates="assets")
