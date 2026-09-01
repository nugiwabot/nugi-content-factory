from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class BriefBase(BaseModel):
    project_id: str
    title: str = Field(..., min_length=2, max_length=200)
    topic: str = Field(..., min_length=5)
    target_audience: str = Field(..., min_length=3)
    content_pillar: str = Field(default="educational")
    tone_of_voice: str = Field(default="professional_authoritative")
    primary_platform: str = Field(default="instagram")
    key_takeaway: Optional[str] = None
    metadata_json: Dict[str, Any] = Field(default_factory=dict)


class BriefCreate(BriefBase):
    pass


class BriefResponse(BriefBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
