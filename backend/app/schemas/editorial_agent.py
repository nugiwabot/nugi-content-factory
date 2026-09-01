from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict

from app.schemas.design_spec import CompositionType, CTAStrategy, DesignSpecification
from app.schemas.visual_qa import VisualQAResult


class ContentType(str, Enum):
    """Controlled Content Types for Property / Real Estate Domain (Phase 3D-1)."""
    PROPERTY_EDUCATION = "PROPERTY_EDUCATION"    # Educational article explaining concepts/mechanisms
    PROPERTY_PROBLEM = "PROPERTY_PROBLEM"        # Dilemma or friction experienced by developers/sales
    PROPERTY_INSIGHT = "PROPERTY_INSIGHT"        # Market data and high-level strategic perspective
    PROPERTY_LISTICLE = "PROPERTY_LISTICLE"      # Numbered actionable points or fatal mistakes
    NUMBER_LIST = "NUMBER_LIST"                  # Numbered actionable points alias
    PROPERTY_CASE_STUDY = "PROPERTY_CASE_STUDY"  # Real proof and transformation results
    CASE_STUDY = "CASE_STUDY"                    # Case study alias
    DATA_EDITORIAL = "DATA_EDITORIAL"            # Institutional data & yield analysis
    PROPERTY_OPINION = "PROPERTY_OPINION"        # Industry commentary, stance, or quote
    OPINION = "OPINION"                          # Opinion alias
    PROPERTY_SHOWCASE = "PROPERTY_SHOWCASE"      # Unit/architectural highlight (Rukost, villa, house)
    SOFT_SELLING = "SOFT_SELLING"                # Aspirational lifestyle narrative
    PROPERTY_SALES_OFFER = "PROPERTY_SALES_OFFER"# Direct conversion offer (Audit, survey, consultation)
    DIRECT_OFFER = "DIRECT_OFFER"                # Direct offer alias


class TextSafeRegion(str, Enum):
    """Explicit negative space regions reserved for typography."""
    TOP_LEFT = "TOP_LEFT"
    TOP_RIGHT = "TOP_RIGHT"
    CENTER_LEFT = "CENTER_LEFT"
    CENTER_RIGHT = "CENTER_RIGHT"
    BOTTOM_LEFT = "BOTTOM_LEFT"
    BOTTOM_RIGHT = "BOTTOM_RIGHT"
    FULL_TOP = "FULL_TOP"
    FULL_BOTTOM = "FULL_BOTTOM"


class EditorialContentSpecification(BaseModel):
    """
    Structured output from Content Strategy and Copywriting Engine.
    Represents the complete intellectual and editorial framing of a post.
    """
    content_type: ContentType = Field(..., description="Classified property content type")
    target_audience: str = Field(..., description="Specific target persona (e.g. Developer, Sales Manager, Property Investor)")
    audience_problem: str = Field(..., description="Underlying friction, bottleneck, or misconception")
    core_insight: str = Field(..., description="The fundamental realization or takeaway")
    editorial_angle: str = Field(..., description="Unique narrative viewpoint for the piece")

    # Display Headline & Typography Layer
    headline: str = Field(..., min_length=8, description="Primary visual headline (2-4 lines)")
    subheadline: str = Field(..., min_length=10, description="Concise supporting statement on graphic")
    highlight_words: List[str] = Field(default_factory=list, description="Specific terms to highlight in accent color")
    
    # Instagram Caption / Article Body
    caption: str = Field(..., description="Full structured article caption (Hook, Problem, Explanation, Solution, Takeaway)")
    key_points: List[str] = Field(default_factory=list, description="Key bullet points or numbered takeaways")
    
    # Composition & CTA Strategy
    suggested_archetype: CompositionType = Field(
        default=CompositionType.HERO_IMAGE_EDITORIAL,
        description="Recommended visual archetype based on content intent"
    )
    cta_policy: CTAStrategy = Field(
        default=CTAStrategy.CTA_NONE,
        description="Enforced CTA rule: CTA_NONE for editorial, CTA_REQUIRED for sales offer"
    )
    cta_text: Optional[str] = Field(default=None, description="CTA button text if policy permits")

    # Optional Structured Metrics / Property Data
    metric_value: Optional[str] = Field(default=None, description="Metric value for case study / data (e.g. '+300%')")
    metric_label: Optional[str] = Field(default=None, description="Metric label tag")
    property_location: Optional[str] = Field(default=None, description="Property location for showcase")
    property_price: Optional[str] = Field(default=None, description="Property price for showcase")
    property_features: List[str] = Field(default_factory=list, description="Property features for showcase")

    model_config = ConfigDict(from_attributes=True)


class VisualArtDirectionSpecification(BaseModel):
    """
    Structured output from Creative Director Engine.
    Defines the exact visual concept, lighting, camera perspective, negative space, and Flux prompt.
    """
    archetype: CompositionType = Field(..., description="Selected editorial visual archetype")
    subject: str = Field(..., description="Core architectural/business visual subject")
    environment: str = Field(..., description="Setting, context, and background atmosphere")
    camera_perspective: str = Field(..., description="Camera shot type, lens angle, and framing")
    composition: str = Field(..., description="Visual composition guidelines")
    lighting: str = Field(..., description="Lighting scheme, mood, and color tone")
    mood: str = Field(..., description="Emotional tone (e.g. prestigious, serene, urgent)")
    color_atmosphere: str = Field(..., description="Dominant color palette and ambient tone")
    
    # Negative Space & Text Placement Intelligence
    negative_space_location: TextSafeRegion = Field(
        default=TextSafeRegion.FULL_BOTTOM,
        description="Designated low-detail area for headline overlay"
    )
    focal_point: str = Field(default="center", description="Visual anchor position (left, right, top, bottom, center)")
    depth: str = Field(default="Cinematic depth of field with foreground focus", description="Depth layering")
    background_treatment: str = Field(default="photographic", description="photographic, gradient, architectural_grid")
    
    # Pure Photography Prompt (Zero Text / Zero Logo)
    image_prompt: str = Field(..., description="Constructed prompt for Flux or Mock image generator")
    negative_prompt: str = Field(
        default="text, words, letters, typography, watermark, logo, banner, poster, frame, UI elements, cartoon, low quality",
        description="Negative prompt tokens"
    )
    text_safe_region: TextSafeRegion = Field(default=TextSafeRegion.FULL_BOTTOM)
    accent_color_hex: str = Field(default="#38bdf8", description="Primary accent color HEX")
    visual_symbolism: Optional[str] = Field(default=None, description="Conceptual visual metaphor")

    model_config = ConfigDict(from_attributes=True)


class UserBriefInput(BaseModel):
    """User input brief for the AI Content & Art Direction Agent."""
    topic: str = Field(..., min_length=3, description="Topic or question (e.g. 'Kenapa leads properti banyak tapi closing rendah?')")
    target_audience: Optional[str] = Field(default="Developer & Marketing Properti", description="Target audience persona")
    content_type_override: Optional[ContentType] = Field(default=None, description="Optional forced content type")
    key_information: Optional[str] = Field(default=None, description="Optional specific context or data points")
    property_details: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Optional property details (price, location, specs)")
    project_id: Optional[str] = Field(default=None, description="Optional project workspace UUID")


class ContentPackage(BaseModel):
    """Complete structured editorial content package."""
    content_id: Optional[str] = None
    project_id: Optional[str] = None
    topic: str
    content_type: ContentType
    editorial_spec: EditorialContentSpecification
    art_direction_spec: VisualArtDirectionSpecification
    design_spec: DesignSpecification
    concept_spec: Optional[Dict[str, Any]] = None
    variants: List[Dict[str, Any]] = Field(default_factory=list)
    active_variant: Optional[str] = "Variant A: Cinematic Hero"
    rendered_asset_path: Optional[str] = None
    rendered_asset_url: Optional[str] = None
    visual_qa: Optional[VisualQAResult] = None

    model_config = ConfigDict(from_attributes=True)
