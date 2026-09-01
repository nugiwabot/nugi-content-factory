from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field


class GenerationRequest(BaseModel):
    project_id: str
    topic: str = Field(..., min_length=3, description="Core topic or idea for the property content")
    target_audience: str = Field(..., min_length=3, description="Target buyer or investor persona")
    content_pillar: str = Field(default="educational", description="Content strategy pillar")
    tone_of_voice: str = Field(default="professional_authoritative", description="Voice guidelines")
    brief_id: Optional[str] = None
    brand_profile_id: Optional[str] = None
    llm_provider: Optional[str] = None
    image_provider: Optional[str] = None


class GenerationResponse(BaseModel):
    success: bool
    job_id: str
    content_id: str
    headline: str
    hook_text: Optional[str] = None
    body_caption: str
    hashtags: Optional[str] = None
    call_to_action: Optional[str] = None
    asset_path: str
    asset_url: Optional[str] = None
    qa_result: Dict[str, Any]
    render_metadata: Dict[str, Any]
