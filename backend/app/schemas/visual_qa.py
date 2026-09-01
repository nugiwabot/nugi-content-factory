from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


class VisualQAResult(BaseModel):
    """
    Automated Visual Quality Assurance evaluation result.
    Serves as design intelligence feedback for deterministic rendering and future vision agents.
    """
    score: int = Field(..., ge=0, le=100, description="Overall design quality score (0 to 100)")
    readability: str = Field(default="EXCELLENT", description="EXCELLENT, GOOD, POOR")
    hierarchy: str = Field(default="STRONG", description="STRONG, ACCEPTABLE, WEAK")
    composition: str = Field(default="BALANCED", description="BALANCED, CROWDED, SPARSE")
    branding: str = Field(default="COMPLIANT", description="COMPLIANT, INCOMPLETE, NON_COMPLIANT")
    
    safe_area_compliant: bool = Field(default=True)
    contrast_ratio_compliant: bool = Field(default=True)
    
    issues: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)
