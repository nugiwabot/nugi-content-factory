from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from app.templates.registry import TemplateRegistry
from app.templates.spec import TemplateSpecification
from app.schemas.design_spec import DesignSpecification
from app.schemas.visual_qa import VisualQAResult
from app.rendering.template_renderer import TemplateRenderer
from app.services.visual_qa import VisualQAService
from app.providers.factory import ProviderFactory

router = APIRouter(prefix="/templates", tags=["Templates & Design Brain"])
renderer = TemplateRenderer()


@router.get("", response_model=List[TemplateSpecification])
def list_templates():
    """Lists all 6 data-driven template specifications."""
    return TemplateRegistry.list_all()


@router.get("/{template_id}", response_model=TemplateSpecification)
def get_template(template_id: str):
    """Retrieves specific template specification by ID."""
    return TemplateRegistry.get(template_id)


@router.post("/render")
def render_template(spec: DesignSpecification):
    """
    Renders a 1080x1350/1080x1080 graphic from DesignSpecification,
    evaluates automated Visual QA, and persists the generated asset.
    """
    # 1. Render Graphic via Deterministic Template Engine
    rendered_bytes, meta = renderer.render_spec(spec)

    # 2. Persist to Storage Provider
    storage = ProviderFactory.get_storage_provider()
    filename = f"{spec.template_id.lower()}_{int(meta['render_latency_ms'])}_{spec.width}x{spec.height}.png"
    asset_path = storage.save(
        data=rendered_bytes,
        filename=filename,
        subfolder="templates"
    )

    # 3. Evaluate Visual QA
    qa_result = VisualQAService.evaluate_design(spec, meta)

    return {
        "success": True,
        "template_id": spec.template_id,
        "asset_path": asset_path,
        "asset_url": f"/api/v1/assets/download?path={asset_path}",
        "render_metadata": meta,
        "visual_qa": qa_result.model_dump()
    }
