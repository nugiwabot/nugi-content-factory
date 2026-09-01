from sqlalchemy import Column, String, Text
from app.models.base import BaseModel


class BrandContext(BaseModel):
    """
    Global brand compliance & voice guidance injected into every generation:
    positioning, messaging pillars, forbidden claims, and customer language.
    """
    __tablename__ = "brand_contexts"

    key = Column(String(80), nullable=False, unique=True, index=True)
    name = Column(String(150), nullable=False)
    content = Column(Text, nullable=False)
