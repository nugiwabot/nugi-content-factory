from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class JobResponse(BaseModel):
    id: str
    project_id: str
    brief_id: Optional[str] = None
    job_type: str
    status: str
    progress_percentage: int
    error_message: Optional[str] = None
    job_payload: Dict[str, Any] = {}
    job_result: Dict[str, Any] = {}
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


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
