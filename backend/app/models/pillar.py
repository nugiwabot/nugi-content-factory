from sqlalchemy import Column, String, Float, JSON, Text, Integer
from app.models.base import BaseModel


class ContentPillar(BaseModel):
    """
    A topical content pillar tied to a business goal. Seeded from Nugi's brand strategy
    (60-25-15 mix) and the Content Pillars framework (Awareness/Trust/LeadGen/Nurture/Conversion).
    """
    __tablename__ = "content_pillars"

    key = Column(String(80), nullable=False, unique=True, index=True)
    name = Column(String(150), nullable=False)
    business_goal = Column(String(50), default="Awareness", nullable=False)
    ratio = Column(Float, default=0.0, nullable=False)
    mapped_content_types = Column(JSON, default=list, nullable=False)
    sub_topics = Column(JSON, default=list, nullable=False)
    example_angles = Column(JSON, default=list, nullable=False)
    prompt_guidance = Column(Text, nullable=True)
    sort_order = Column(Integer, default=0, nullable=False)
