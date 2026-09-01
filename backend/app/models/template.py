from sqlalchemy import Column, String, Integer, Text, JSON
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class Template(BaseModel):
    """
    Defines layout boundaries, aspect ratios, and visual rules for deterministic rendering.
    """
    __tablename__ = "templates"

    name = Column(String(100), nullable=False, unique=True, index=True)
    platform = Column(String(50), default="instagram_feed", nullable=False) # instagram_feed, instagram_story, facebook_feed, ads_square
    width = Column(Integer, default=1080, nullable=False)
    height = Column(Integer, default=1080, nullable=False)
    description = Column(Text, nullable=True)
    
    # Layout specification stored as JSON (badge coords, text box margins, logo positioning)
    layout_spec = Column(JSON, default=dict, nullable=False)

    # Relationships
    contents = relationship("Content", back_populates="template")
