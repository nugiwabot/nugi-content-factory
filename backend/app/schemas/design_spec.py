from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class DesignSpecification(BaseModel):
    """
    Standardized design contract consumed by the deterministic rendering engine.
    Ensures complete decoupling between LLM reasoning and visual pixel generation.
    """
    template_id: str = Field(default="01_PROPERTY_PROBLEM", description="Identifier of the target template")
    width: int = Field(default=1080, description="Canvas width in pixels")
    height: int = Field(default=1350, description="Canvas height in pixels (1350 portrait 4:5 or 1080 square)")
    
    # Text Contents
    headline: str = Field(..., min_length=5, description="Primary headline text")
    highlight_words: List[str] = Field(default_factory=list, description="Specific terms to highlight in accent colors")
    subheadline: Optional[str] = Field(default=None, description="Supporting explanatory copy")
    badge_text: Optional[str] = Field(default=None, description="Category / pillar badge pill text")
    
    # Template-specific contents
    bullet_points: List[str] = Field(default_factory=list, description="Numbered or bulleted list items")
    metric_value: Optional[str] = Field(default=None, description="Highlighted metric (e.g. '+300%')")
    metric_label: Optional[str] = Field(default=None, description="Metric description label")
    cta_text: Optional[str] = Field(default=None, description="Call to action button or footer text")
    
    # Branding & Visuals
    brand_name: str = Field(default="NugiProperti", description="Display brand name watermark")
    show_logo: bool = Field(default=True, description="Whether to composite the brand logo")
    background_type: str = Field(default="gradient", description="gradient, image, solid")
    background_image_path: Optional[str] = Field(default=None, description="Path to background visual asset")
    accent_color_hex: Optional[str] = Field(default=None, description="Override accent color")
    
    custom_metadata: Dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(from_attributes=True)
