from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class PlanRequest(BaseModel):
    goal: str
    count: int = 5
    project_id: Optional[str] = None


class BatchRunRequest(BaseModel):
    project_id: Optional[str] = None
    mode: str = "bulk"  # plan | bulk
    goal: Optional[str] = None
    lines: Optional[List[str]] = None       # bulk mode input
    items: Optional[List[Dict[str, Any]]] = None  # plan mode (already planned items)
    count: Optional[int] = 5


class BatchItemOut(BaseModel):
    id: str
    topic: str
    pillar: Optional[str] = None
    content_type: Optional[str] = None
    headline: Optional[str] = None
    caption: Optional[str] = None
    asset_path: Optional[str] = None
    asset_url: Optional[str] = None
    status: str
    error: Optional[str] = None
    sort_order: int

    model_config = ConfigDict(from_attributes=True)


class BatchRunOut(BaseModel):
    id: str
    project_id: str
    mode: str
    goal: Optional[str] = None
    status: str
    job_id: Optional[str] = None
    total_items: int
    completed_items: int
    summary: Dict[str, Any] = {}
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BatchRunDetailOut(BatchRunOut):
    items: List[BatchItemOut] = []
