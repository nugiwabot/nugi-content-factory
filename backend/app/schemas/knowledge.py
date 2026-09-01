from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class SkillOut(BaseModel):
    id: str
    name: str
    description: str
    category: str
    source: str
    file_path: Optional[str] = None
    enabled: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PillarOut(BaseModel):
    id: str
    key: str
    name: str
    business_goal: str
    ratio: float
    mapped_content_types: List[str]
    sub_topics: List[str]
    example_angles: List[str]
    prompt_guidance: Optional[str] = None
    sort_order: int

    model_config = ConfigDict(from_attributes=True)


class PillarUpdate(BaseModel):
    name: Optional[str] = None
    business_goal: Optional[str] = None
    ratio: Optional[float] = None
    mapped_content_types: Optional[List[str]] = None
    sub_topics: Optional[List[str]] = None
    example_angles: Optional[List[str]] = None
    prompt_guidance: Optional[str] = None


class BrandContextOut(BaseModel):
    id: str
    key: str
    name: str
    content: str

    model_config = ConfigDict(from_attributes=True)


class SeedResult(BaseModel):
    skills: int
    pillars: int
    brand: int


class UploadResult(BaseModel):
    skills: List[SkillOut]
    count: int
