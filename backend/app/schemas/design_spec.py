from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict
from app.schemas.visual_prompt import VisualPromptSpecification


# Instagram Safezone Logical Layout Constraints (Phase 3D-2)
# Master Canvas: 1080 × 1350 px (4:5 Aspect Ratio)
# Instagram 3:4 Profile Grid Center Area: 1012 × 1350 px (Crops ~34 px on left and right)
# Instagram 1:1 Square Feed Crop: 1080 × 1080 px (Crops 135 px on top and bottom)
# CRITICAL: 100% INVISIBLE logical bounds in final output
CANVAS_WIDTH = 1080
CANVAS_HEIGHT = 1350
GRID_3_4_WIDTH = 1012
GRID_3_4_HEIGHT = 1350
GRID_3_4_CROP_SIDE = 34  # 34 px on left and 34 px on right

SAFEZONE_TOP = 135
SAFEZONE_BOTTOM = 1215
SAFEZONE_HEIGHT = 1080

SAFEZONE_LEFT = 34         # Outer cut line on left for 3:4 grid
SAFEZONE_RIGHT = 1046      # Outer cut line on right for 3:4 grid (1080 - 34)
SAFEZONE_WIDTH = 1012      # Width of 3:4 grid safezone

SAFEZONE_CONTENT_LEFT = 76  # Inner content margin (ensures 42px breathing room inside 3:4 grid)
SAFEZONE_CONTENT_RIGHT = 1004 # (1080 - 76)


class CompositionType(str, Enum):
    """Professional Editorial Composition Archetypes."""
    HERO_IMAGE_EDITORIAL = "HERO_IMAGE_EDITORIAL"  # 60-80% visual dominance, cinematic gradient, layered typography
    SPLIT_EDITORIAL = "SPLIT_EDITORIAL"            # 50/50 clean split between image and typography
    CINEMATIC_OVERLAY = "CINEMATIC_OVERLAY"        # Full-bleed imagery with sophisticated directional overlay
    DATA_EDITORIAL = "DATA_EDITORIAL"              # Prominent numeric data callout + metric highlight box
    LIST_EDITORIAL = "LIST_EDITORIAL"              # High-impact numbered listicle without infographic clutter
    MINIMAL_EDITORIAL = "MINIMAL_EDITORIAL"        # Editorial opinion / quote on minimalist dark canvas
    PROPERTY_SHOWCASE = "PROPERTY_SHOWCASE"        # Hero property photography + location + price + specs pills


class EditorialLayoutPreset(str, Enum):
    """Dynamic Layout Algorithm Presets (Phase 3D-2)."""
    LAYOUT_HERO_BOTTOM_TEXT = "LAYOUT_HERO_BOTTOM_TEXT"
    LAYOUT_SPLIT_ASYMMETRIC = "LAYOUT_SPLIT_ASYMMETRIC"
    LAYOUT_CINEMATIC_OVERLAY = "LAYOUT_CINEMATIC_OVERLAY"
    LAYOUT_SPOTLIGHT_HEADLINE = "LAYOUT_SPOTLIGHT_HEADLINE"
    LAYOUT_METRIC_DOMINANT = "LAYOUT_METRIC_DOMINANT"
    LAYOUT_QUOTE_EDITORIAL = "LAYOUT_QUOTE_EDITORIAL"
    LAYOUT_PROPERTY_SHOWCASE = "LAYOUT_PROPERTY_SHOWCASE"


class CTAStrategy(str, Enum):
    """Strict Business Rules for CTA rendering."""
    CTA_NONE = "CTA_NONE"          # No CTA button (Educational, Insight, Opinion, Listicle, Case Study)
    CTA_OPTIONAL = "CTA_OPTIONAL"  # CTA rendered only if provided (Showcase)
    CTA_REQUIRED = "CTA_REQUIRED"  # CTA must be prominently rendered (Direct Offer / Lead Gen)


class ImageStrategy(str, Enum):
    """How the visual asset is placed on canvas."""
    full_bleed = "full_bleed"
    split_top = "split_top"
    split_bottom = "split_bottom"
    card_embedded = "card_embedded"
    abstract_geometry = "abstract_geometry"
    none = "none"


class OverlayStrategy(str, Enum):
    """Directional cinematic gradient overlays."""
    cinematic_gradient_bottom = "cinematic_gradient_bottom"
    cinematic_gradient_top = "cinematic_gradient_top"
    directional_vignette = "directional_vignette"
    subtle_scrim = "subtle_scrim"
    clean_split = "clean_split"


class DesignSpecification(BaseModel):
    """
    Standardized design contract consumed by both the Phase 2 TemplateRenderer
    and Phase 3A/3C/3D Editorial Compositing Engine.
    """
    template_id: str = Field(default="01_PROPERTY_PROBLEM", description="Template identifier for backward compatibility")
    composition_type: CompositionType = Field(
        default=CompositionType.HERO_IMAGE_EDITORIAL,
        description="Active editorial composition archetype"
    )
    layout_preset: EditorialLayoutPreset = Field(
        default=EditorialLayoutPreset.LAYOUT_HERO_BOTTOM_TEXT,
        description="Active layout algorithm preset"
    )
    cta_strategy: CTAStrategy = Field(
        default=CTAStrategy.CTA_NONE,
        description="CTA presence rule: CTA_NONE, CTA_OPTIONAL, CTA_REQUIRED"
    )
    image_strategy: ImageStrategy = Field(
        default=ImageStrategy.full_bleed,
        description="Visual asset placement strategy"
    )
    overlay_strategy: OverlayStrategy = Field(
        default=OverlayStrategy.cinematic_gradient_bottom,
        description="Directional gradient overlay strategy"
    )
    
    # Canvas Dimensions (Default 4:5 Instagram Portrait)
    width: int = Field(default=1080, ge=500, le=3000)
    height: int = Field(default=1350, ge=500, le=3000)

    # Core Typography
    headline: str = Field(..., min_length=3, description="Main editorial title")
    highlight_words: List[str] = Field(default_factory=list, description="Keywords to emphasize with neon accent")
    subheadline: Optional[str] = Field(default=None, description="Contextual explanation or thesis statement")
    badge_text: Optional[str] = Field(default="EDUKASI PROPERTI", description="Category eyebrow text")
    bullet_points: List[str] = Field(default_factory=list, description="Listicle / structured points")

    # Colors & Visual Assets
    accent_color_hex: Optional[str] = Field(default=None, description="Primary accent color in hex")
    accent_color: Optional[str] = Field(default=None, description="Alias for accent color")
    background_image_bytes: Optional[bytes] = Field(default=None, exclude=True, description="Optional raw background image bytes")

    # Author / Metadata (Preserved from Phase 1/2)
    author_name: Optional[str] = Field(default="NugiProperti", description="Brand / Author name")
    author_handle: Optional[str] = Field(default="@nugiproperti", description="Social media handle")
    brand_name: str = Field(default="NugiProperti", description="Primary brand name")

    # Quote specific
    quote_text: Optional[str] = Field(default=None, description="Editorial quote body")

    # Data / Case Study specific
    metric_value: Optional[str] = Field(default=None, description="E.g. '+300%', 'Rp 1.2 M', '14%'")
    metric_label: Optional[str] = Field(default=None, description="E.g. 'Pertumbuhan Konversi', 'Yield Tahunan'")

    # Property Showcase specific
    property_location: Optional[str] = Field(default=None, description="E.g. 'Jatinangor, Sumedang'")
    property_price: Optional[str] = Field(default=None, description="E.g. 'Mulai Rp 1,4 M'")
    property_features: List[str] = Field(default_factory=list, description="E.g. ['20 Kamar', 'Furnished', 'Okupansi 100%']")

    # Visual Direction & Negative Space
    focal_point_position: str = Field(default="top_center", description="Where the main subject is placed")
    negative_space_requirement: str = Field(default="bottom", description="Area reserved for clean typography")
    visual_prompt_spec: Optional[VisualPromptSpecification] = Field(default=None, description="Flux image prompt")

    # CTA Button properties
    cta_text: Optional[str] = Field(default=None, description="Button label")
    cta_url: Optional[str] = Field(default=None, description="Target destination")

    # Theme overrides
    accent_color_hex: Optional[str] = Field(default=None, description="Hex color override (e.g. #38bdf8)")
    brand_name: str = Field(default="NugiProperti")
    show_logo: bool = Field(default=True)

    model_config = ConfigDict(from_attributes=True)
