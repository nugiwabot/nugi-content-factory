from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class AssetResponse(BaseModel):
    id: str
    project_id: str
    content_id: Optional[str] = None
    asset_type: str
    file_path: str
    file_url: Optional[str] = None
    mime_type: str
    width: Optional[int] = None
    height: Optional[int] = None
    file_size_bytes: Optional[int] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
