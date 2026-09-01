from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class AssetSummary(BaseModel):
    id: str
    asset_type: str
    file_path: str
    file_url: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class QAResultSummary(BaseModel):
    id: str
    status: str
    contrast_score: Optional[float] = None
    issues_json: List[str] = []
    recommendations_json: List[str] = []

    model_config = ConfigDict(from_attributes=True)


class ContentResponse(BaseModel):
    id: str
    project_id: str
    brief_id: Optional[str] = None
    brand_profile_id: Optional[str] = None
    headline: str
    hook_text: Optional[str] = None
    body_caption: str
    hashtags: Optional[str] = None
    call_to_action: Optional[str] = None
    visual_concept_prompt: Optional[str] = None
    status: str
    revision_count: int
    metadata_json: Dict[str, Any] = {}
    created_at: datetime
    updated_at: datetime

    assets: List[AssetSummary] = []
    qa_results: List[QAResultSummary] = []

    model_config = ConfigDict(from_attributes=True)
