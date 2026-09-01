from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class VisualPromptSpecification(BaseModel):
    """
    Structured specification for generating visual backgrounds via Flux.
    Directs the image model to produce ONLY pure photography/background assets
    with explicit awareness of text negative space and focal point positioning.
    Never prompts for text, typography, logos, or UI elements.
    """
    subject: str = Field(
        default="Modern luxury property architecture",
        description="Core visual subject (e.g. contemporary residential building, commercial hub, student residence)"
    )
    environment: Optional[str] = Field(
        default="Surrounded by tropical greenery and manicured urban landscaping",
        description="Surrounding setting and context"
    )
    architecture: Optional[str] = Field(
        default="Minimalist modern tropical architecture, clean glass facades, natural stone textures",
        description="Architectural style, materials, and structural details"
    )
    camera_perspective: Optional[str] = Field(
        default="Eye-level low-angle wide shot, architectural medium focal length",
        description="Camera shot type, lens angle, and perspective"
    )
    lighting: Optional[str] = Field(
        default="Subtle warm golden hour sunlight, soft diffused ambient glow, gentle interior illumination",
        description="Lighting scheme and highlights"
    )
    time_of_day: Optional[str] = Field(
        default="Sunset golden hour",
        description="Time of day (golden hour, twilight, bright morning daylight)"
    )
    mood: Optional[str] = Field(
        default="Sophisticated, serene, prestigious, high-end investment feel",
        description="Emotional tone and aesthetic atmosphere"
    )
    color_atmosphere: Optional[str] = Field(
        default="Cinematic muted obsidian navy, warm champagne gold highlights, natural slate tones",
        description="Color palette direction for the image"
    )
    depth: Optional[str] = Field(
        default="Clear depth separation with sharp architectural foreground and soft cinematic bokeh background",
        description="Depth of field and spatial layering"
    )
    negative_space: Optional[str] = Field(
        default="Preserve clean dark negative space on the bottom half for editorial text layering",
        description="Explicit negative space direction for text readability"
    )
    focal_point_position: str = Field(
        default="top",
        description="Focal point bias: top, bottom, left, right, center"
    )
    photographic_style: str = Field(
        default="Cinematic 35mm architectural editorial photography, 8k resolution, authentic textures",
        description="Photographic medium and realism quality"
    )
    negative_prompt: str = Field(
        default="text, words, letters, typography, watermark, logo, banner, poster, frame, UI elements, blurry, distorted, cartoon, low quality, oversaturated",
        description="Negative prompt tokens to strictly avoid visual pollution"
    )

    model_config = ConfigDict(from_attributes=True)

    def build_flux_prompt(self, negative_space_bias: Optional[str] = None) -> str:
        """
        Constructs the final Flux prompt string integrating composition and negative space constraints.
        """
        ns_clause = self.negative_space
        if negative_space_bias:
            ns_clause = f"Preserve clean uncluttered negative space on the {negative_space_bias} for editorial typography overlay"

        components = [
            self.photographic_style,
            self.subject,
            self.architecture,
            self.environment,
            self.camera_perspective,
            self.lighting,
            self.time_of_day,
            self.mood,
            self.color_atmosphere,
            self.depth,
            ns_clause,
            "no text, no letters, no words, no watermark, no logo, pure photographic background asset"
        ]

        # Filter out empty or None components and join
        valid_parts = [c.strip() for c in components if c and c.strip()]
        return ", ".join(valid_parts)
