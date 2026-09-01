from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class BrandProfileBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    tagline: Optional[str] = None
    primary_color: str = Field(default="#0f172a")
    secondary_color: str = Field(default="#38bdf8")
    accent_color: str = Field(default="#10b981")
    font_family: str = Field(default="sans-serif")
    logo_path: Optional[str] = None
    default_target_audience: Optional[str] = None
    default_cta_text: Optional[str] = None
    metadata_json: Dict[str, Any] = Field(default_factory=dict)


class BrandProfileCreate(BrandProfileBase):
    pass


class BrandProfileUpdate(BaseModel):
    name: Optional[str] = None
    tagline: Optional[str] = None
    primary_color: Optional[str] = None
    secondary_color: Optional[str] = None
    accent_color: Optional[str] = None
    font_family: Optional[str] = None
    logo_path: Optional[str] = None
    default_target_audience: Optional[str] = None
    default_cta_text: Optional[str] = None
    metadata_json: Optional[Dict[str, Any]] = None


class BrandProfileResponse(BrandProfileBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
