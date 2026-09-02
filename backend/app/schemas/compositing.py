import uuid
from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict

from app.schemas.editorial_agent import ContentType, TextSafeRegion
from app.schemas.design_spec import CompositionType, CTAStrategy


class BlendMode(str, Enum):
    """Supported Blend Modes for Layer Compositing."""
    NORMAL = "normal"
    MULTIPLY = "multiply"
    SCREEN = "screen"
    ADD = "add"
    OVERLAY = "overlay"
    SOFT_LIGHT = "soft_light"


class LayerType(str, Enum):
    """13-Layer Logical Compositing Stack."""
    CANVAS = "canvas"                     # Layer 0
    BACKGROUND = "background"             # Layer 1
    ATMOSPHERE = "atmosphere"             # Layer 2
    ARCHITECTURE = "architecture"         # Layer 3
    MAIN_SUBJECT = "main_subject"         # Layer 4
    SUPPORTING_OBJECTS = "supporting"     # Layer 5
    FOREGROUND = "foreground"             # Layer 6
    LIGHTING_EFFECTS = "lighting"         # Layer 7
    SHADOWS = "shadows"                   # Layer 8
    DEPTH_EFFECTS = "depth"               # Layer 9
    GRAPHIC_ELEMENTS = "graphics"         # Layer 10
    TYPOGRAPHY = "typography"             # Layer 11
    BRAND_IDENTITY = "branding"           # Layer 12


class ColorGradeSpecification(BaseModel):
    """Color Grading and Cinematic Tone Mapping Parameters."""
    preset_name: str = Field(default="CINEMATIC_TWILIGHT", description="Preset name: CINEMATIC_TWILIGHT, PREMIUM_GOLD, TECH_CYAN, WARM_ARCHITECTURAL")
    exposure: float = Field(default=0.0, ge=-1.0, le=1.0, description="Exposure shift (-1.0 to 1.0)")
    contrast: float = Field(default=1.12, ge=0.5, le=2.0, description="Contrast multiplier (0.5 to 2.0)")
    saturation: float = Field(default=0.95, ge=0.0, le=2.0, description="Color saturation (0.0 to 2.0)")
    temperature: float = Field(default=0.05, ge=-1.0, le=1.0, description="Warm (+) vs Cool (-) Kelvin tone bias")
    tint: float = Field(default=0.0, ge=-1.0, le=1.0, description="Magenta (+) vs Green (-) tint")
    highlights: float = Field(default=0.0, ge=-1.0, le=1.0, description="Highlight recovery/boost")
    shadows: float = Field(default=-0.05, ge=-1.0, le=1.0, description="Shadow depth adjustment")
    vignette_strength: float = Field(default=0.35, ge=0.0, le=1.0, description="Corner vignette intensity (0.0 to 1.0)")

    model_config = ConfigDict(from_attributes=True)


class LayerSpecification(BaseModel):
    """Metadata and execution parameters for a single compositing layer."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    layer_type: LayerType = Field(..., description="Logical layer type in the 13-layer stack")
    z_index: int = Field(default=0, ge=0, le=12, description="Stack order (0 to 12)")
    source: str = Field(default="generated", description="Asset source: generated, pillow_draw, asset_path, mask")
    
    # Positioning and Geometry
    x: int = Field(default=0, description="X coordinate on 1080 canvas")
    y: int = Field(default=0, description="Y coordinate on 1350 canvas")
    width: int = Field(default=1080, description="Layer width")
    height: int = Field(default=1350, description="Layer height")
    
    # Alpha & Blending
    opacity: float = Field(default=1.0, ge=0.0, le=1.0, description="Layer opacity")
    blend_mode: BlendMode = Field(default=BlendMode.NORMAL, description="Layer blending mode")
    blur_radius: float = Field(default=0.0, ge=0.0, description="Gaussian blur radius")
    
    # Shading and Lighting
    shadow_config: Optional[Dict[str, Any]] = Field(default=None, description="Contact/drop shadow parameters")
    color_adjustment: Optional[Dict[str, Any]] = Field(default=None, description="Layer-specific color grading overrides")
    safe_area: bool = Field(default=True, description="Strictly inside safe margin")
    generated_by: str = Field(default="CompositingEngine", description="Generator identity")

    model_config = ConfigDict(from_attributes=True)


class VisualConceptSpecification(BaseModel):
    """
    Comprehensive Art Direction Specification defining the multi-layer visual story,
    focal subject, environmental depth, lighting match, and asset plan.
    """
    concept_id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    content_type: ContentType = Field(..., description="Domain content type")
    visual_story: str = Field(..., description="Narrative visual story (e.g. leads friction, transit growth, cashflow yield)")
    
    # Layered Scene Descriptions
    focal_subject: str = Field(..., description="Primary focal element (e.g. Sales person reviewing leads / Modern Rukost)")
    supporting_subjects: List[str] = Field(default_factory=list, description="Secondary objects (e.g. unread message notification, metric pill)")
    background_description: str = Field(..., description="Far background environment (e.g. luxury property facade, toll interchange)")
    midground_description: str = Field(default="", description="Midground architectural depth")
    foreground_description: str = Field(default="", description="Foreground framing or negative space scrim")
    
    # Art Direction & Camera
    composition_strategy: str = Field(default="Hero focal subject biased right with clean typography negative space on left/bottom")
    camera_direction: str = Field(default="Low-angle eye-level, architectural 35mm lens perspective")
    perspective: str = Field(default="3-point architectural perspective")
    lighting_direction: str = Field(default="Directional side light from upper-right with warm ambient fill")
    lighting_intensity: float = Field(default=0.85, ge=0.0, le=1.0)
    shadow_direction: str = Field(default="Soft diagonal falloff toward bottom-left")
    atmosphere: str = Field(default="Cinematic twilight, low-key lighting with subtle atmospheric haze")
    color_mood: str = Field(default="Obsidian navy, dark slate, and warm champagne amber highlights")
    depth_strategy: str = Field(default="3-plane depth separation (sharp subject, soft distant architectural bokeh)")
    
    # Text Placement
    negative_space_region: TextSafeRegion = Field(default=TextSafeRegion.FULL_BOTTOM)
    text_safe_region: TextSafeRegion = Field(default=TextSafeRegion.FULL_BOTTOM)
    
    # Multi-Asset & Compositing Directives
    asset_requirements: List[str] = Field(default_factory=list, description="List of required asset layers")
    compositing_required: bool = Field(default=True, description="Whether multi-layer compositing is executed")
    typography_strategy: str = Field(default="Bold editorial headline with colored word highlights and high WCAG AAA contrast")
    graphic_elements: List[str] = Field(default_factory=list, description="Subtle geometric lines, dividers, or badges")
    quality_requirements: Dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(from_attributes=True)


class SubjectAsset(BaseModel):
    """Isolated subject asset metadata."""
    asset_id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    asset_name: str
    image_bytes: Optional[bytes] = None
    mask_bytes: Optional[bytes] = None
    has_alpha: bool = True
    width: int = 1080
    height: int = 1350


class BackgroundAsset(BaseModel):
    """Background environment asset metadata."""
    asset_id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    image_bytes: Optional[bytes] = None
    prompt_used: str = ""
    width: int = 1080
    height: int = 1350


class ReferenceAsset(BaseModel):
    """Reference asset metadata for future style conditioning."""
    ref_id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    ref_type: str = "style_reference"
    url_or_path: str = ""


class CompositionPlan(BaseModel):
    """Assembled 13-layer compositing blueprint."""
    plan_id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    concept_id: str
    layers: List[LayerSpecification] = Field(default_factory=list)
    color_grade: ColorGradeSpecification = Field(default_factory=ColorGradeSpecification)
    depth_enabled: bool = True
    lighting_match_enabled: bool = True

    model_config = ConfigDict(from_attributes=True)


class VisualVariant(BaseModel):
    """One of 1-3 generated visual art direction variants."""
    variant_id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    variant_name: str = Field(..., description="e.g. 'Variant A: Cinematic Hero', 'Variant B: Deep Minimalist'")
    concept: VisualConceptSpecification
    composition_plan: CompositionPlan
    rendered_asset_path: Optional[str] = None
    rendered_asset_url: Optional[str] = None
    visual_qa_score: Optional[int] = Field(default=None, description="Real QA score, only populated after a render exists")

    model_config = ConfigDict(from_attributes=True)
