from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class SemanticZone(BaseModel):
    """Defines a logical zone in the canvas layout."""
    zone_id: str
    semantic_position: str # top_left, top_center, top_right, center, bottom_center, bottom_left, bottom_right
    alignment: str = "left" # left, center, right
    required: bool = True
    max_lines: Optional[int] = None
    default_text: Optional[str] = None
    style_variant: Optional[str] = None # e.g. badge, display, headline, body, cta_pill, card


class CanvasSpec(BaseModel):
    width: int = 1080
    height: int = 1350
    aspect_ratio: str = "4:5"
    safe_margin_x: int = 64
    safe_margin_y: int = 80


class BackgroundRule(BaseModel):
    type: str = "gradient" # gradient, image, solid
    scrim_opacity: float = 0.85
    overlay_color: str = "#070b14"
    blur_radius: int = 0


class TemplateSpecification(BaseModel):
    """
    Data-driven template specification.
    Machine-readable by both AI Agent reasoning engines and Deterministic Pillow Renderer.
    """
    template_id: str
    name: str
    purpose: str
    target_audience: str
    content_type: str
    canvas: CanvasSpec = Field(default_factory=CanvasSpec)
    zones: List[SemanticZone] = Field(default_factory=list)
    accent_scheme: str = "cyan" # cyan, gold, emerald, rose, indigo
    background_rules: BackgroundRule = Field(default_factory=BackgroundRule)
    custom_rules: Dict[str, Any] = Field(default_factory=dict)
