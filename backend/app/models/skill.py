from sqlalchemy import Column, String, Text, Boolean
from app.models.base import BaseModel


class KnowledgeSkill(BaseModel):
    """
    A distilled knowledge entry (marketing SKILL.md, content-creator skill, or pillar framework)
    injected into the agent's LLM prompt when relevant to the generation topic.
    """
    __tablename__ = "knowledge_skills"

    name = Column(String(150), nullable=False, index=True)
    description = Column(Text, nullable=False)
    category = Column(String(80), default="general", nullable=False)
    content = Column(Text, nullable=False)
    source = Column(String(20), default="seeded", nullable=False)  # seeded | uploaded
    file_path = Column(String(255), nullable=True)
    enabled = Column(Boolean, default=True, nullable=False)
