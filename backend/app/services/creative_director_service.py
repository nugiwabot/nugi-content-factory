from typing import Dict, Any, Optional
from app.schemas.editorial_agent import (
    EditorialContentSpecification,
    VisualArtDirectionSpecification,
    TextSafeRegion,
    ContentType
)
from app.schemas.design_spec import (
    DesignSpecification,
    CompositionType,
    CTAStrategy,
    ImageStrategy,
    OverlayStrategy
)
from app.schemas.visual_prompt import VisualPromptSpecification
from app.brand.profiles import NUGI_PROPERTI_BRAND_PROFILE


class CreativeDirectorService:
    """
    Transforms Editorial Content Specifications into precise Visual Art Direction Specifications
    and constructs the final DesignSpecification contract for the deterministic rendering engine.
    """
    @staticmethod
    def create_art_direction(spec: EditorialContentSpecification) -> VisualArtDirectionSpecification:
        c_type = spec.content_type
        archetype = spec.suggested_archetype

        colors = NUGI_PROPERTI_BRAND_PROFILE.colors
        accent_hex = colors.accent_primary

        if c_type == ContentType.PROPERTY_PROBLEM:
            subject = "A modern property sales lounge at dusk, a focused sales professional reviewing incoming lead data on a laptop"
            environment = "High-end developer marketing gallery with miniature architectural scale models in the foreground"
            camera_perspective = "Low-angle medium shot, 35mm lens framing with cinematic depth"
            lighting = "Low-key cinematic twilight with warm ambient interior lamps and subtle blue monitor glow"
            mood = "Intense, focused, high-stakes business environment"
            color_atmosphere = "Deep obsidian navy and slate gray with warm amber interior highlights"
            negative_space = TextSafeRegion.FULL_BOTTOM
            focal_point = "center_right"
            accent_hex = colors.accent_rose # Rose accent for problem warning
            depth = "Sharp subject focus with soft bokeh on background scale models"

        elif c_type == ContentType.PROPERTY_INSIGHT:
            subject = "Elevated architectural panorama of a modern Indonesian urban transit and highway corridor"
            environment = "Connected residential masterplan surrounded by landscaped greenery and modern toll access interchange"
            camera_perspective = "Wide drone perspective at golden hour, crisp architectural clarity"
            lighting = "Dramatic golden hour sunlight casting long warm shadows across roads and modern buildings"
            mood = "Expansive, visionary, prestigious, high-growth atmosphere"
            color_atmosphere = "Cinematic slate navy with warm golden horizon reflections"
            negative_space = TextSafeRegion.FULL_BOTTOM
            focal_point = "top_center"
            accent_hex = colors.accent_primary # Cyan for insight
            depth = "Deep panoramic depth of field with sharp structural lines"

        elif c_type == ContentType.PROPERTY_LISTICLE:
            subject = "Clean modern architectural building facade with geometric glass windows and elegant facade louvers"
            environment = "Prestigious commercial district with minimalist urban landscaping"
            camera_perspective = "Upward vertical perspective, symmetrical architectural framing"
            lighting = "Diffused overcast twilight lighting with soft subtle edge reflections"
            mood = "Structured, authoritative, analytical, orderly"
            color_atmosphere = "Deep midnight navy, dark charcoal slate, and amber accents"
            negative_space = TextSafeRegion.FULL_BOTTOM
            focal_point = "top"
            accent_hex = colors.accent_gold # Gold for listicle
            depth = "Layered vertical planes with sharp geometric contrast"

        elif c_type == ContentType.PROPERTY_CASE_STUDY:
            subject = "Contemporary residential student apartment building (Rukost) with modern tropical facade"
            environment = "Clean campus neighborhood with manicured palm trees and paved driveway"
            camera_perspective = "Eye-level 45-degree corner shot showcasing building depth and balconies"
            lighting = "Sunset golden hour with warm glowing room lights visible through glass windows"
            mood = "Successful, thriving, verified, high-yield investment feel"
            color_atmosphere = "Dark obsidian sky with emerald and warm amber architectural lighting"
            negative_space = TextSafeRegion.FULL_BOTTOM
            focal_point = "top_right"
            accent_hex = colors.accent_emerald # Green for case study growth
            depth = "Clear foreground driveway separation and sharp building facade"

        elif c_type == ContentType.PROPERTY_SHOWCASE:
            subject = "Luxury modern student residence building (Rukost) with premium exterior finish and glass balconies"
            environment = "Quiet prestigious residential area with tropical trees and modern street lighting"
            camera_perspective = "Eye-level architectural hero shot, wide 24mm perspective"
            lighting = "Late afternoon warm sunshine highlighting natural stone textures and glass reflections"
            mood = "Exclusive, turnkey, profitable, high-end property asset"
            color_atmosphere = "Warm champagne gold, natural slate, and deep obsidian navy"
            negative_space = TextSafeRegion.FULL_BOTTOM
            focal_point = "top"
            accent_hex = colors.accent_gold
            depth = "Foreground landscape with crisp architectural building focus"

        elif c_type == ContentType.PROPERTY_OPINION:
            subject = "Minimalist abstract architectural concrete arches and glass reflections"
            environment = "Sleek contemporary corporate property boardroom terrace overlooking skyline"
            camera_perspective = "Minimalist centered composition with strong diagonal shadows"
            lighting = "Dramatic chiaroscuro side lighting with deep controlled shadows"
            mood = "Authoritative, thought-provoking, bold, forward-looking"
            color_atmosphere = "Monochrome obsidian and deep indigo slate"
            negative_space = TextSafeRegion.FULL_BOTTOM
            focal_point = "center"
            accent_hex = colors.accent_secondary # Indigo for opinion
            depth = "Architectural line geometry with deep negative space"

        else: # PROPERTY_EDUCATION & PROPERTY_SALES_OFFER
            subject = "Modern commercial property headquarters and architectural sales lounge"
            environment = "Lush tropical urban development with glass facades and illuminated reception"
            camera_perspective = "Wide low-angle perspective, cinematic framing"
            lighting = "Warm evening golden hour with soft diffused highlights"
            mood = "Trustworthy, educational, professional, prestigious"
            color_atmosphere = "Deep navy slate with sky cyan accent lighting"
            negative_space = TextSafeRegion.FULL_BOTTOM
            focal_point = "top_right"
            accent_hex = colors.accent_primary
            depth = "Sharp building exterior with cinematic bokeh background"

        # Build Pure Photography Flux Prompt
        ns_direction = "bottom half" if negative_space == TextSafeRegion.FULL_BOTTOM else "upper-left area"
        image_prompt = (
            f"Cinematic architectural photography of {subject}, {environment}, "
            f"{camera_perspective}, {lighting}, {mood}, {color_atmosphere}, {depth}. "
            f"Preserve clean uncluttered dark negative space on the {ns_direction} for editorial typography overlay. "
            f"Authentic 35mm photo textures, 8k resolution, no text, no words, no letters, no watermark, no logo, pure photographic background asset."
        )

        return VisualArtDirectionSpecification(
            archetype=archetype,
            subject=subject,
            environment=environment,
            camera_perspective=camera_perspective,
            composition=f"Visual dominance aligned with {archetype.value}, focal bias toward {focal_point}",
            lighting=lighting,
            mood=mood,
            color_atmosphere=color_atmosphere,
            negative_space_location=negative_space,
            focal_point=focal_point,
            depth=depth,
            background_treatment="photographic",
            image_prompt=image_prompt,
            negative_prompt="text, words, letters, typography, watermark, logo, banner, poster, frame, UI elements, cartoon, blurry, low quality",
            text_safe_region=negative_space,
            accent_color_hex=accent_hex,
            visual_symbolism=f"Represents strategic precision in {c_type.value}"
        )

    @staticmethod
    def build_design_specification(
        editorial_spec: EditorialContentSpecification,
        art_direction: VisualArtDirectionSpecification,
        width: int = 1080,
        height: int = 1350
    ) -> DesignSpecification:
        """Translates editorial and art direction specs into a DesignSpecification for the renderer."""
        
        # Badge Text formulation
        badge_text_map = {
            ContentType.PROPERTY_PROBLEM: "DILEMA MARKETING PROPERTI",
            ContentType.PROPERTY_INSIGHT: "MARKET INTELLIGENCE",
            ContentType.PROPERTY_LISTICLE: "POIN KRUSIAL",
            ContentType.PROPERTY_CASE_STUDY: "STUDI KASUS & HASIL",
            ContentType.PROPERTY_SHOWCASE: "PORTFOLIO UNIT",
            ContentType.PROPERTY_OPINION: "PERSPEKTIF",
            ContentType.PROPERTY_SALES_OFFER: "SLOT TERBATAS",
            ContentType.PROPERTY_EDUCATION: "EDUKASI PROPERTI"
        }
        badge_text = badge_text_map.get(editorial_spec.content_type, "EDUKASI PROPERTI")

        # Map negative space bias
        ns_bias = "bottom" if art_direction.negative_space_location == TextSafeRegion.FULL_BOTTOM else "left"

        visual_prompt_spec = VisualPromptSpecification(
            subject=art_direction.subject,
            environment=art_direction.environment,
            camera_perspective=art_direction.camera_perspective,
            lighting=art_direction.lighting,
            mood=art_direction.mood,
            color_atmosphere=art_direction.color_atmosphere,
            focal_point_position=art_direction.focal_point,
            negative_space=f"Preserve clean dark negative space on the {ns_bias} for editorial typography"
        )

        return DesignSpecification(
            composition_type=art_direction.archetype,
            cta_strategy=editorial_spec.cta_policy,
            cta_text=editorial_spec.cta_text,
            width=width,
            height=height,
            headline=editorial_spec.headline,
            highlight_words=editorial_spec.highlight_words,
            subheadline=editorial_spec.subheadline,
            badge_text=badge_text,
            bullet_points=editorial_spec.key_points,
            metric_value=editorial_spec.metric_value,
            metric_label=editorial_spec.metric_label,
            property_location=editorial_spec.property_location,
            property_price=editorial_spec.property_price,
            property_features=editorial_spec.property_features,
            focal_point_position=art_direction.focal_point,
            negative_space_requirement=ns_bias,
            visual_prompt_spec=visual_prompt_spec,
            accent_color_hex=art_direction.accent_color_hex,
            brand_name="NugiProperti",
            show_logo=True
        )
