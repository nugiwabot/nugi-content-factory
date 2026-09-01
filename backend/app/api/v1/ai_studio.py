from typing import Optional, Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.schemas.editorial_agent import (
    UserBriefInput, 
    ContentPackage, 
    AgentChatRequest, 
    AgentChatResponse
)
from app.schemas.design_spec import DesignSpecification, CompositionType
from app.services.content_generation_agent import ContentGenerationAgent
from app.rendering.editorial_renderer import EditorialRenderer
from app.services.visual_qa import VisualQAService
from app.providers.factory import ProviderFactory

router = APIRouter(prefix="/ai-studio", tags=["AI Content & Art Direction Studio"])
agent = ContentGenerationAgent()
renderer = EditorialRenderer()


@router.post("/chat", response_model=AgentChatResponse)
def handle_agentic_chat_endpoint(
    req: AgentChatRequest,
    db: Session = Depends(get_db)
):
    """
    Conversational Copilot Endpoint.
    Analyzes user intent, provides consulting / greetings, or orchestrates end-to-end content generation.
    """
    return agent.handle_conversational_chat(req=req, db=db)


class RegenerateHeadlineRequest(BaseModel):
    package: ContentPackage
    custom_topic: Optional[str] = None


class RegenerateCaptionRequest(BaseModel):
    package: ContentPackage


class RegenerateVisualRequest(BaseModel):
    package: ContentPackage
    archetype_override: Optional[CompositionType] = None


@router.post("/generate", response_model=ContentPackage)
def generate_editorial_content(
    brief: UserBriefInput,
    db: Session = Depends(get_db)
):
    """
    Transforms a user brief into a complete editorial content package
    (Content Strategy + Headline + Caption + Art Direction + Render + QA + DB Save).
    """
    return agent.generate_full_package(brief=brief, db=db)


@router.post("/regenerate/headline", response_model=ContentPackage)
def regenerate_headline_endpoint(req: RegenerateHeadlineRequest):
    """Regenerates only the headline and highlight words without altering caption or visual prompt."""
    return agent.regenerate_headline(current_pkg=req.package, custom_topic=req.custom_topic)


@router.post("/regenerate/caption", response_model=ContentPackage)
def regenerate_caption_endpoint(req: RegenerateCaptionRequest):
    """Regenerates only the Instagram article caption."""
    return agent.regenerate_caption(current_pkg=req.package)


@router.post("/regenerate/visual", response_model=ContentPackage)
def regenerate_visual_endpoint(req: RegenerateVisualRequest):
    """Regenerates visual art direction, Flux prompt, and background composition."""
    return agent.regenerate_visual_art(current_pkg=req.package, archetype_override=req.archetype_override)


@router.post("/render")
def render_custom_spec(spec: DesignSpecification):
    """Directly renders a modified DesignSpecification and returns updated QA."""
    rendered_bytes, meta = renderer.render(spec)
    storage = ProviderFactory.get_storage_provider()
    filename = f"studio_custom_{spec.width}x{spec.height}.png"
    asset_path = storage.save(data=rendered_bytes, filename=filename, subfolder="generated")
    visual_qa = VisualQAService.evaluate_design(spec, meta)

    return {
        "asset_path": asset_path,
        "asset_url": f"/api/v1/assets/download?path={asset_path}",
        "render_metadata": meta,
        "visual_qa": visual_qa.model_dump()
    }
