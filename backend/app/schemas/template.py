from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class TemplateBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    platform: str = Field(default="instagram_feed")
    width: int = Field(default=1080)
    height: int = Field(default=1080)
    description: Optional[str] = None
    layout_spec: Dict[str, Any] = Field(default_factory=dict)


class TemplateCreate(TemplateBase):
    pass


class TemplateResponse(TemplateBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
