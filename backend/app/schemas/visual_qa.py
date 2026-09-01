from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class VisualQAResult(BaseModel):
    """
    Automated Visual Quality Assurance evaluation result (Phase 3D-3).
    Evaluates:
    - Multi-Category Pass: Technical Pass, Design Pass, Editorial Pass, Brand Pass.
    - Safezone & Crop Resilience: Safezone Pass, Critical Element Pass, Text Bounding Box Pass, Profile Grid Pass.
    - Non-Regression Pass: Adherence to approved NugiProperti Editorial Design DNA.
    """
    score: int = Field(..., ge=0, le=100, description="Overall design quality score (0 to 100)")
    readability: str = Field(default="EXCELLENT", description="EXCELLENT, GOOD, POOR")
    hierarchy: str = Field(default="STRONG", description="STRONG, ACCEPTABLE, WEAK")
    composition: str = Field(default="BALANCED", description="BALANCED, CROWDED, SPARSE")
    branding: str = Field(default="COMPLIANT", description="COMPLIANT, INCOMPLETE, NON_COMPLIANT")
    
    # Phase 3D-2 & 3D-3 Category Assessment Passes
    technical_pass: bool = Field(default=True, description="Dimension, render integrity, image asset valid")
    design_pass: bool = Field(default=True, description="Contrast, text backplate, typography size, vignette")
    editorial_pass: bool = Field(default=True, description="Headline impact, zero CTA on articles, information hierarchy")
    brand_pass: bool = Field(default=True, description="Logo in safezone, NugiProperti signature, color compliance")
    overall_quality: str = Field(default="EXCELLENT", description="EXCELLENT, GOOD, ACCEPTABLE, NEEDS_IMPROVEMENT")

    # Phase 3D-3 Explicit Safezone & Bounding-Box Passes
    safezone_pass: bool = Field(default=True, description="Master safezone compliance (all critical elements within [76, 135, 1004, 1215])")
    safezone_critical_element_pass: bool = Field(default=True, description="All critical text and branding elements inside safezone")
    text_bounding_box_pass: bool = Field(default=True, description="All rendered text bounding boxes validated")
    profile_grid_pass: bool = Field(default=True, description="Resilient to Instagram 3:4 profile grid crop (~34px side crops)")
    content_readability_pass: bool = Field(default=True, description="WCAG AAA contrast and typography readability pass")
    non_regression_pass: bool = Field(default=True, description="Conforms strictly to approved NugiProperti Design DNA")

    safe_area_compliant: bool = Field(default=True, description="Backward compatible safe area flag")
    contrast_ratio_compliant: bool = Field(default=True, description="WCAG AAA / High contrast met")
    safezone_bounds: Dict[str, Any] = Field(
        default_factory=lambda: {
            "top": 135,
            "bottom": 1215,
            "height": 1080,
            "left_crop_3_4": 34,
            "right_crop_3_4": 34,
            "grid_3_4_width": 1012,
            "grid_3_4_height": 1350,
            "safezone_left": 34,
            "safezone_right": 1046,
            "safezone_content_left": 76,
            "safezone_content_right": 1004,
            "width": 1080,
            "height": 1350
        }
    )
    critical_element_bounding_boxes: Dict[str, Dict[str, int]] = Field(
        default_factory=dict,
        description="Measured pixel bounding boxes of critical rendered elements (left, top, right, bottom)"
    )
    
    issues: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)
