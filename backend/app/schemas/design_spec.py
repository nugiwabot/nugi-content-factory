from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict
from app.schemas.visual_prompt import VisualPromptSpecification


class CompositionType(str, Enum):
    """Professional Editorial Composition Archetypes."""
    HERO_IMAGE_EDITORIAL = "HERO_IMAGE_EDITORIAL"  # 60-80% visual dominance, cinematic gradient, layered typography
    SPLIT_EDITORIAL = "SPLIT_EDITORIAL"            # 50/50 clean split between image and typography
    CINEMATIC_OVERLAY = "CINEMATIC_OVERLAY"        # Full-bleed imagery with sophisticated directional overlay
    DATA_EDITORIAL = "DATA_EDITORIAL"              # Prominent numeric data callout + metric highlight box
    LIST_EDITORIAL = "LIST_EDITORIAL"              # High-impact numbered listicle without infographic clutter
    MINIMAL_EDITORIAL = "MINIMAL_EDITORIAL"        # Editorial opinion / quote on minimalist dark canvas
    PROPERTY_SHOWCASE = "PROPERTY_SHOWCASE"        # Hero property photography + location + price + specs pills


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
    and Phase 3A EditorialRenderer.
    """
    template_id: str = Field(default="01_PROPERTY_PROBLEM", description="Template identifier for backward compatibility")
    composition_type: CompositionType = Field(
        default=CompositionType.HERO_IMAGE_EDITORIAL,
        description="Active editorial composition archetype"
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
        description="Gradient overlay strategy"
    )

    width: int = Field(default=1080, description="Canvas width in pixels")
    height: int = Field(default=1350, description="Canvas height in pixels (1350 portrait 4:5 or 1080 square)")

    # Core Text Contents
    headline: str = Field(..., min_length=5, description="Primary headline text")
    highlight_words: List[str] = Field(default_factory=list, description="Specific terms to highlight in accent colors")
    subheadline: Optional[str] = Field(default=None, description="Supporting explanatory editorial copy")
    badge_text: Optional[str] = Field(default=None, description="Category / eyebrow badge pill text")

    # Structured Data & Editorial Elements
    bullet_points: List[str] = Field(default_factory=list, description="Numbered or bulleted list items")
    metric_value: Optional[str] = Field(default=None, description="Highlighted metric (e.g. '+300% Speed', '85%')")
    metric_label: Optional[str] = Field(default=None, description="Metric description label")
    cta_text: Optional[str] = Field(default=None, description="Call to action button or footer text")
    author_name: Optional[str] = Field(default=None, description="Optional author / commentator attribution")

    # Property Showcase Specifics
    property_location: Optional[str] = Field(default=None, description="Location tag (e.g. 'Jatinangor, Sumedang')")
    property_price: Optional[str] = Field(default=None, description="Price highlight (e.g. 'Rp 1,85 Miliar')")
    property_features: List[str] = Field(default_factory=list, description="Key architectural features (e.g. ['16 Kamar', 'Yield 12%'])")

    # Visual Direction & Flux Prompts
    focal_point_position: str = Field(default="center", description="top, bottom, left, right, center")
    negative_space_requirement: str = Field(default="bottom", description="top, bottom, left, right")
    visual_prompt_spec: Optional[VisualPromptSpecification] = Field(default=None, description="Flux prompt specification")

    # Branding & Visuals
    brand_name: str = Field(default="NugiProperti", description="Display brand name watermark")
    show_logo: bool = Field(default=True, description="Whether to composite the brand logo")
    background_type: str = Field(default="gradient", description="gradient, image, solid")
    background_image_path: Optional[str] = Field(default=None, description="Path to background visual asset")
    accent_color_hex: Optional[str] = Field(default=None, description="Override accent color")

    custom_metadata: Dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(from_attributes=True)
