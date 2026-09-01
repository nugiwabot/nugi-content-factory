import io
from typing import Dict, Any, Tuple, Optional, List
from PIL import Image, ImageDraw, ImageFilter

from app.schemas.compositing import (
    VisualConceptSpecification,
    CompositionPlan,
    LayerSpecification,
    LayerType,
    BlendMode,
    ColorGradeSpecification,
    SubjectAsset,
    BackgroundAsset
)
from app.schemas.editorial_agent import ContentType, TextSafeRegion
from app.providers.factory import ProviderFactory
from app.core.logging import logger


class AssetCompositorService:
    """
    Manages multi-asset planning, background generation, subject isolation,
    and composition plan construction for the 13-layer compositing engine.
    """
    @staticmethod
    def generate_isolated_subject(
        subject_desc: str,
        width: int = 500,
        height: int = 700,
        accent_color: Tuple[int, int, int] = (56, 189, 248)
    ) -> SubjectAsset:
        """
        Generates or extracts an isolated subject graphic with an RGBA alpha mask.
        In offline/mock mode, deterministically synthesizes clean architectural subject elements.
        """
        # Create transparent canvas for subject
        subj_img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(subj_img)

        # Draw aesthetic semi-transparent architectural subject silhouette
        # e.g., Geometric modern building facade cutout with glass balconies
        b_box = [20, 40, width - 20, height - 20]
        draw.rounded_rectangle(b_box, radius=18, fill=(22, 34, 56, 230), outline=accent_color, width=2)

        # Inner illuminated architectural window grid
        for wy in range(b_box[1] + 40, b_box[3] - 40, 50):
            for wx in range(b_box[0] + 30, b_box[2] - 30, 45):
                draw.rectangle([wx, wy, wx + 28, wy + 26], fill=(245, 158, 11, 160))

        # Soft edge antialiasing
        subj_img = subj_img.filter(ImageFilter.SMOOTH)

        buf = io.BytesIO()
        subj_img.save(buf, format="PNG")
        
        return SubjectAsset(
            asset_name=subject_desc[:30],
            image_bytes=buf.getvalue(),
            has_alpha=True,
            width=width,
            height=height
        )

    @staticmethod
    def build_composition_plan(
        concept: VisualConceptSpecification,
        accent_hex: str = "#38bdf8"
    ) -> CompositionPlan:
        """
        Constructs the complete 13-layer composition plan and color grade specification.
        """
        # Configure Color Grade based on concept color mood
        grade = ColorGradeSpecification(
            preset_name=concept.color_mood[:24],
            exposure=0.0,
            contrast=1.14,
            saturation=0.96,
            temperature=0.08 if "gold" in concept.color_mood.lower() else -0.05,
            vignette_strength=0.35
        )

        layers = [
            LayerSpecification(layer_type=LayerType.CANVAS, z_index=0, source="obsidian_navy"),
            LayerSpecification(layer_type=LayerType.BACKGROUND, z_index=1, source="flux_photographic"),
            LayerSpecification(layer_type=LayerType.ATMOSPHERE, z_index=2, source="twilight_haze", opacity=0.45),
            LayerSpecification(layer_type=LayerType.ARCHITECTURE, z_index=3, source="scene_depth"),
            LayerSpecification(layer_type=LayerType.MAIN_SUBJECT, z_index=4, source="isolated_subject", opacity=0.95),
            LayerSpecification(layer_type=LayerType.SUPPORTING_OBJECTS, z_index=5, source="metric_pill"),
            LayerSpecification(layer_type=LayerType.FOREGROUND, z_index=6, source="scrim_gradient", opacity=0.92),
            LayerSpecification(layer_type=LayerType.LIGHTING_EFFECTS, z_index=7, source="ambient_glow", blend_mode=BlendMode.SCREEN),
            LayerSpecification(layer_type=LayerType.SHADOWS, z_index=8, source="contact_occlusion"),
            LayerSpecification(layer_type=LayerType.DEPTH_EFFECTS, z_index=9, source="tone_mapping"),
            LayerSpecification(layer_type=LayerType.GRAPHIC_ELEMENTS, z_index=10, source="editorial_dividers"),
            LayerSpecification(layer_type=LayerType.TYPOGRAPHY, z_index=11, source="deterministic_pillow"),
            LayerSpecification(layer_type=LayerType.BRAND_IDENTITY, z_index=12, source="nugiproperti_signature"),
        ]

        return CompositionPlan(
            concept_id=concept.concept_id,
            layers=layers,
            color_grade=grade,
            depth_enabled=True,
            lighting_match_enabled=True
        )
