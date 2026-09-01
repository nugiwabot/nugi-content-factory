from typing import List, Dict, Any
from fastapi import APIRouter
from app.schemas.design_spec import DesignSpecification, CompositionType, CTAStrategy
from app.rendering.editorial_renderer import EditorialRenderer
from app.services.visual_qa import VisualQAService
from app.providers.factory import ProviderFactory

router = APIRouter(prefix="/editorial", tags=["Editorial Visual Engine"])
editorial_renderer = EditorialRenderer()


@router.get("/compositions")
def list_composition_archetypes():
    """Lists the 7 Professional Editorial Composition Archetypes."""
    return [
        {
            "id": CompositionType.HERO_IMAGE_EDITORIAL.value,
            "name": "Hero Image Editorial",
            "visual_dominance": "60–80%",
            "best_for": "Property insights, educational articles, market analysis",
            "default_cta": "CTA_NONE",
            "description": "Large cinematic image with directional bottom gradient and layered high-contrast typography."
        },
        {
            "id": CompositionType.SPLIT_EDITORIAL.value,
            "name": "Split Editorial",
            "visual_dominance": "45–55%",
            "best_for": "Comparison, before/after, problem-solution",
            "default_cta": "CTA_NONE",
            "description": "Clean 50/50 vertical division between photographic visual and structured dark typography block."
        },
        {
            "id": CompositionType.CINEMATIC_OVERLAY.value,
            "name": "Cinematic Overlay",
            "visual_dominance": "100% Full-Bleed",
            "best_for": "Emotional property stories, major market perspectives, thought leadership",
            "default_cta": "CTA_NONE",
            "description": "Full-bleed architectural imagery with subtle dark directional vignette."
        },
        {
            "id": CompositionType.DATA_EDITORIAL.value,
            "name": "Data Editorial",
            "visual_dominance": "40%",
            "best_for": "Market data, statistics, ROI metrics, case studies",
            "default_cta": "CTA_NONE",
            "description": "Massive numeric callout with gold/cyan accent glow, headline, and supporting commentary."
        },
        {
            "id": CompositionType.LIST_EDITORIAL.value,
            "name": "List Editorial",
            "visual_dominance": "30–50%",
            "best_for": "Crucial mistakes, tactical step-by-step guides, 5 key points",
            "default_cta": "CTA_NONE",
            "description": "Structured numbered pill items with clean typography and zero infographic clutter."
        },
        {
            "id": CompositionType.MINIMAL_EDITORIAL.value,
            "name": "Minimal Editorial",
            "visual_dominance": "Minimal / Grid",
            "best_for": "Opinion, quotes, executive commentary",
            "default_cta": "CTA_NONE",
            "description": "Deep obsidian canvas with subtle architectural line grid, large quotation styling, and author attribution."
        },
        {
            "id": CompositionType.PROPERTY_SHOWCASE.value,
            "name": "Property Showcase",
            "visual_dominance": "50–60%",
            "best_for": "House, villa, apartment, student housing (Rukost)",
            "default_cta": "CTA_OPTIONAL",
            "description": "Hero photography, location badge, architectural specs pills, price highlight, and optional booking button."
        }
    ]


@router.post("/render")
def render_editorial_graphic(spec: DesignSpecification):
    """
    Renders an editorial visual asset using the Editorial Visual Engine.
    Executes layout compositing, directional gradient overlays, Visual QA evaluation, and persistence.
    """
    # 1. Render Graphic via Editorial Engine
    rendered_bytes, meta = editorial_renderer.render(spec)

    # 2. Persist to Disk Storage
    storage = ProviderFactory.get_storage_provider()
    filename = f"editorial_{spec.composition_type.value.lower()}_{int(meta['render_latency_ms'])}_{spec.width}x{spec.height}.png"
    asset_path = storage.save(
        data=rendered_bytes,
        filename=filename,
        subfolder="editorial"
    )

    # 3. Evaluate Visual QA
    qa_result = VisualQAService.evaluate_design(spec, meta)

    return {
        "success": True,
        "composition_type": spec.composition_type.value,
        "asset_path": asset_path,
        "asset_url": f"/api/v1/assets/download?path={asset_path}",
        "render_metadata": meta,
        "visual_qa": qa_result.model_dump()
    }
