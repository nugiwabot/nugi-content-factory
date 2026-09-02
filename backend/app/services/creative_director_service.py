import uuid
from typing import Dict, Any, Optional, List
from app.schemas.editorial_agent import (
    EditorialContentSpecification,
    VisualArtDirectionSpecification,
    TextSafeRegion,
    ContentType
)
from app.schemas.compositing import (
    VisualConceptSpecification,
    CompositionPlan,
    VisualVariant,
    ColorGradeSpecification
)
from app.schemas.design_spec import (
    DesignSpecification,
    CompositionType,
    EditorialLayoutPreset,
    CTAStrategy,
    ImageStrategy,
    OverlayStrategy,
    SAFEZONE_TOP,
    SAFEZONE_BOTTOM
)
from app.schemas.visual_prompt import VisualPromptSpecification
from app.brand.profiles import NUGI_PROPERTI_BRAND_PROFILE
from app.services.asset_compositor_service import AssetCompositorService


class CreativeDirectorService:
    """
    Transforms Editorial Content Specifications into Cinematic Visual Concepts,
    Layered Composition Plans, and multi-variant art directions (Phase 3D-2).
    """
    @staticmethod
    def create_visual_concept(spec: EditorialContentSpecification) -> VisualConceptSpecification:
        c_type = spec.content_type
        colors = NUGI_PROPERTI_BRAND_PROFILE.colors

        if c_type == ContentType.PROPERTY_PROBLEM:
            visual_story = "Leads properti masuk dalam volume tinggi namun proses follow-up tim sales lambat dan terhenti."
            focal_subject = "Modern property marketing gallery at blue hour with dramatic central spotlight on architectural scale model"
            background_desc = "Luxury commercial real estate building interior, glass facade reflecting twilight sky"
            midground_desc = "Dark wood executive consultation table with blueprints and floorplans"
            foreground_desc = "Subtle dark glass negative space reserved for large typography"
            lighting_dir = "Dramatic central spotlight illuminating architectural subject with deep edge shadows"
            color_mood = "Obsidian navy, blue hour twilight, and alert rose red accent"
            accent_hex = colors.accent_rose
            ns_region = TextSafeRegion.FULL_BOTTOM

        elif c_type == ContentType.PROPERTY_INSIGHT:
            visual_story = "Kenaikan harga rumah berakselerasi cepat melampaui daya beli masyarakat."
            focal_subject = "Elevated highway interchange connecting sprawling modern township skyline at dusk"
            background_desc = "Expansive city masterplan horizon under twilight sky with volumetric atmosphere"
            midground_desc = "Contemporary residential developments with illuminated glass balconies"
            foreground_desc = "Deep obsidian negative space on lower safezone"
            lighting_dir = "Golden sunset directional light blending into deep twilight blue"
            color_mood = "Slate navy, deep indigo, and warm sunset gold"
            accent_hex = colors.accent_gold
            ns_region = TextSafeRegion.FULL_BOTTOM

        elif c_type in (ContentType.PROPERTY_LISTICLE, ContentType.NUMBER_LIST):
            visual_story = "Struktur kesalahan fatal yang sering dilakukan pembeli properti pertama kali."
            focal_subject = "Architectural geometric facade with vertical rhythm, modern louvers, and sharp perspective"
            background_desc = "High-end residential district at blue hour with tranquil ambient light"
            midground_desc = "Textured stone pillars and ambient illuminated entrance"
            foreground_desc = "Clean dark negative space for numbered editorial typography"
            lighting_dir = "Subtle side spotlight with soft volumetric glow"
            color_mood = "Midnight navy, slate charcoal, and warm amber gold"
            accent_hex = colors.accent_gold
            ns_region = TextSafeRegion.FULL_BOTTOM

        elif c_type in (ContentType.PROPERTY_CASE_STUDY, ContentType.CASE_STUDY, ContentType.DATA_EDITORIAL):
            visual_story = "Studi kasus transformasi empiris efisiensi respon tim sales melipatgandakan konversi 300%."
            focal_subject = "Fully occupied modern student residential apartment building with warm interior room lights"
            background_desc = "Prestigious university township campus context with landscaped boulevards"
            midground_desc = "Welcoming lobby entrance and paved parking promenade"
            foreground_desc = "Obsidian glass panel area for empirical data callout"
            lighting_dir = "Late blue hour twilight with warm tungsten window illumination"
            color_mood = "Obsidian navy, emerald growth green, and champagne gold"
            accent_hex = colors.accent_emerald
            ns_region = TextSafeRegion.FULL_BOTTOM

        elif c_type == ContentType.PROPERTY_SHOWCASE:
            visual_story = "Showcase unit rumah hunian mewah premium dekat Kota Baru Parahyangan siap huni."
            focal_subject = "Stunning 2-story contemporary tropical luxury villa facade with glass walls and lush garden"
            background_desc = "Exclusive gated residential estate under warm golden hour sunlight"
            midground_desc = "Private infinity swimming pool reflection and manicured tropical lawn"
            foreground_desc = "Clean lower safezone for property location and price badges"
            lighting_dir = "Bright warm afternoon sun with crisp architectural shadows"
            color_mood = "Warm champagne gold, natural timber textures, and obsidian slate"
            accent_hex = colors.accent_gold
            ns_region = TextSafeRegion.FULL_BOTTOM

        elif c_type in (ContentType.PROPERTY_OPINION, ContentType.OPINION):
            visual_story = "Perspektif tajam kepemimpinan mengenai transformasi digital industri properti."
            focal_subject = "Minimalist raw concrete and steel architectural monolith with dramatic diagonal shadows"
            background_desc = "Executive penthouse terrace overlooking city skyline at night"
            midground_desc = "Reflective glass curtain wall and cantilevered roofline"
            foreground_desc = "Deep monochrome obsidian negative space with large editorial quotation"
            lighting_dir = "Chiaroscuro side spotlight with deep shadows"
            color_mood = "Deep monochrome obsidian slate and electric violet"
            accent_hex = "#8b5cf6"
            ns_region = TextSafeRegion.FULL_BOTTOM

        elif c_type == ContentType.SOFT_SELLING:
            visual_story = "Gaya hidup residensial prestisius dengan fasilitas clubhouse modern dan taman asri."
            focal_subject = "Serene resort clubhouse lounge with warm ambient lighting by the water"
            background_desc = "Modern suburban neighborhood with landscaped walking paths"
            midground_desc = "Timber deck patio with tropical greenery"
            foreground_desc = "Soft gradient negative space for lifestyle narrative"
            lighting_dir = "Warm sunset golden hour fill"
            color_mood = "Warm amber, slate navy, and electric cyan"
            accent_hex = colors.accent_primary
            ns_region = TextSafeRegion.FULL_BOTTOM

        else: # PROPERTY_EDUCATION & DIRECT_OFFER / PROPERTY_SALES_OFFER
            visual_story = "Prinsip fundamental mengapa lokasi strategis belum tentu menjamin properti cepat terjual."
            focal_subject = "Modern glass pavilion property sales gallery at blue hour with dramatic central spotlight"
            background_desc = "Master-planned residential development with tranquil tree-lined avenue"
            midground_desc = "Sophisticated architectural entrance with ambient uplighting"
            foreground_desc = "Obsidian negative space for bold educational headline"
            lighting_dir = "Volumetric blue hour spotlight with soft cyan ambient fill"
            color_mood = "Obsidian navy, blue hour slate, and electric cyan"
            accent_hex = "#06b6d4"
            ns_region = TextSafeRegion.FULL_BOTTOM

        return VisualConceptSpecification(
            concept_id=str(uuid.uuid4())[:8],
            content_type=c_type,
            visual_story=visual_story,
            focal_subject=focal_subject,
            background_description=background_desc,
            midground_description=midground_desc,
            foreground_description=foreground_desc,
            lighting_direction=lighting_dir,
            color_mood=color_mood,
            negative_space_region=ns_region,
            text_safe_region=ns_region,
            asset_requirements=["background_scene", "radial_spotlight", "obsidian_backplate"],
            compositing_required=True
        )

    @staticmethod
    def create_art_direction(spec: EditorialContentSpecification) -> VisualArtDirectionSpecification:
        """Translates editorial content spec into an art direction specification (Phase 3D-2)."""
        concept = CreativeDirectorService.create_visual_concept(spec)
        colors = NUGI_PROPERTI_BRAND_PROFILE.colors

        # Brand-guided accent per content intent (Nugi Properti Editorial DNA).
        if spec.content_type == ContentType.PROPERTY_PROBLEM:
            accent_hex = colors.accent_rose
        elif spec.content_type in (ContentType.PROPERTY_INSIGHT, ContentType.PROPERTY_LISTICLE, ContentType.NUMBER_LIST, ContentType.PROPERTY_SHOWCASE):
            accent_hex = colors.accent_gold
        elif spec.content_type in (ContentType.PROPERTY_CASE_STUDY, ContentType.CASE_STUDY, ContentType.DATA_EDITORIAL):
            accent_hex = colors.accent_emerald
        elif spec.content_type in (ContentType.PROPERTY_OPINION, ContentType.OPINION):
            accent_hex = colors.accent_neon_violet
        else:
            accent_hex = colors.accent_primary

        # Phase 3D-2 Overhauled Flux Prompt Template
        image_prompt = (
            f"Cinematic editorial real estate photography of {concept.focal_subject}, {concept.background_description}. "
            f"Lighting: {concept.lighting_direction}, deep obsidian shadows toward edges, strong radial light falloff. "
            f"Atmosphere: Volumetric blue hour haze, realistic authentic architectural materials, controlled depth of field. "
            f"Composition: Premium magazine art direction, dramatic negative space reserved for large typography. "
            f"8k resolution, photorealistic, no text, no letters, no words, no watermark, no logo, no UI elements, pure background photography."
        )

        return VisualArtDirectionSpecification(
            archetype=spec.suggested_archetype,
            subject=concept.focal_subject,
            environment=concept.background_description,
            camera_perspective="35mm architectural tilt-shift, cinematic depth",
            composition=f"Layered editorial visual aligned with {spec.suggested_archetype.value}",
            lighting=concept.lighting_direction,
            mood="Authoritative, cinematic, prestigious editorial property media",
            color_atmosphere=concept.color_mood,
            negative_space_location=concept.negative_space_region,
            focal_point="top_center",
            depth="Multi-plane volumetric depth separation",
            background_treatment="photographic_cinematic",
            image_prompt=image_prompt,
            negative_prompt="text, words, letters, typography, watermark, logo, banner, poster, frame, UI elements, cartoon, 3d render, blurry, bad proportions",
            text_safe_region=concept.text_safe_region,
            accent_color_hex=accent_hex,
            visual_symbolism=f"Represents strategic authority in {spec.content_type.value}"
        )

    @staticmethod
    def generate_visual_variants(
        editorial_spec: EditorialContentSpecification,
        base_design_spec: DesignSpecification
    ) -> List[VisualVariant]:
        """Generates 3 distinct art direction variants for the studio UI."""
        variants = []

        # Variant A: Cinematic Hero (Default)
        concept_a = CreativeDirectorService.create_visual_concept(editorial_spec)
        plan_a = AssetCompositorService.build_composition_plan(concept_a, base_design_spec.accent_color_hex or "#06b6d4")
        variants.append(VisualVariant(
            variant_name="Variant A: Cinematic Hero",
            concept=concept_a,
            composition_plan=plan_a,
            visual_qa_score=None
        ))

        # Variant B: Minimalist Authority (Monochrome Obsidian)
        concept_b = CreativeDirectorService.create_visual_concept(editorial_spec)
        concept_b.color_mood = "Deep obsidian monochrome with electric violet accents"
        plan_b = AssetCompositorService.build_composition_plan(concept_b, "#8b5cf6")
        plan_b.color_grade.preset_name = "DEEP_OBSIDIAN"
        plan_b.color_grade.contrast = 1.25
        plan_b.color_grade.temperature = -0.15
        variants.append(VisualVariant(
            variant_name="Variant B: Minimalist Authority",
            concept=concept_b,
            composition_plan=plan_b,
            visual_qa_score=None
        ))

        # Variant C: Premium Gold Composite
        concept_c = CreativeDirectorService.create_visual_concept(editorial_spec)
        concept_c.color_mood = "Warm champagne gold highlights and twilight glow"
        plan_c = AssetCompositorService.build_composition_plan(concept_c, "#f59e0b")
        plan_c.color_grade.preset_name = "PREMIUM_GOLD"
        plan_c.color_grade.temperature = 0.20
        variants.append(VisualVariant(
            variant_name="Variant C: Layered Composite",
            concept=concept_c,
            composition_plan=plan_c,
            visual_qa_score=None
        ))

        return variants

    @staticmethod
    def build_design_specification(
        editorial_spec: EditorialContentSpecification,
        art_direction: VisualArtDirectionSpecification,
        width: int = 1080,
        height: int = 1350
    ) -> DesignSpecification:
        """Translates editorial and art direction specs into a DesignSpecification for the renderer."""
        badge_text_map = {
            ContentType.PROPERTY_PROBLEM: "DILEMA MARKETING",
            ContentType.PROPERTY_INSIGHT: "MARKET INTELLIGENCE",
            ContentType.PROPERTY_LISTICLE: "POIN KRUSIAL",
            ContentType.NUMBER_LIST: "POIN KRUSIAL",
            ContentType.PROPERTY_CASE_STUDY: "STUDI KASUS",
            ContentType.CASE_STUDY: "STUDI KASUS",
            ContentType.DATA_EDITORIAL: "DATA & ANALISIS",
            ContentType.PROPERTY_SHOWCASE: "PORTFOLIO UNIT",
            ContentType.PROPERTY_OPINION: "PERSPEKTIF",
            ContentType.OPINION: "PERSPEKTIF",
            ContentType.SOFT_SELLING: "PRESTIGE LIVING",
            ContentType.PROPERTY_SALES_OFFER: "SLOT TERBATAS",
            ContentType.DIRECT_OFFER: "SESI KONSULTASI",
            ContentType.PROPERTY_EDUCATION: "EDUKASI PROPERTI"
        }
        badge_text = badge_text_map.get(editorial_spec.content_type, "EDUKASI PROPERTI")
        ns_bias = "bottom" if art_direction.negative_space_location == TextSafeRegion.FULL_BOTTOM else "left"

        # Determine layout algorithm preset based on archetype
        layout_preset_map = {
            CompositionType.HERO_IMAGE_EDITORIAL: EditorialLayoutPreset.LAYOUT_HERO_BOTTOM_TEXT,
            CompositionType.SPLIT_EDITORIAL: EditorialLayoutPreset.LAYOUT_SPLIT_ASYMMETRIC,
            CompositionType.CINEMATIC_OVERLAY: EditorialLayoutPreset.LAYOUT_CINEMATIC_OVERLAY,
            CompositionType.DATA_EDITORIAL: EditorialLayoutPreset.LAYOUT_METRIC_DOMINANT,
            CompositionType.LIST_EDITORIAL: EditorialLayoutPreset.LAYOUT_SPOTLIGHT_HEADLINE,
            CompositionType.MINIMAL_EDITORIAL: EditorialLayoutPreset.LAYOUT_QUOTE_EDITORIAL,
            CompositionType.PROPERTY_SHOWCASE: EditorialLayoutPreset.LAYOUT_PROPERTY_SHOWCASE,
        }
        layout_preset = layout_preset_map.get(art_direction.archetype, EditorialLayoutPreset.LAYOUT_HERO_BOTTOM_TEXT)

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
            layout_preset=layout_preset,
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

