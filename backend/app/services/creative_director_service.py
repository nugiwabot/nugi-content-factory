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
    CTAStrategy,
    ImageStrategy,
    OverlayStrategy
)
from app.schemas.visual_prompt import VisualPromptSpecification
from app.brand.profiles import NUGI_PROPERTI_BRAND_PROFILE
from app.services.asset_compositor_service import AssetCompositorService


class CreativeDirectorService:
    """
    Transforms Editorial Content Specifications into precise Visual Concepts,
    Layered Composition Plans, and multi-variant art directions.
    """
    @staticmethod
    def create_visual_concept(spec: EditorialContentSpecification) -> VisualConceptSpecification:
        c_type = spec.content_type
        archetype = spec.suggested_archetype

        colors = NUGI_PROPERTI_BRAND_PROFILE.colors

        if c_type == ContentType.PROPERTY_PROBLEM:
            visual_story = "Leads properti masuk dalam volume tinggi namun alur follow-up sales terlambat dan bocor."
            focal_subject = "Sales manager properti memeriksa alur pesan leads di laptop dengan ekspresi fokus di ruang kerja modern"
            background_desc = "Interior marketing gallery properti mewah dengan model maket arsitektural di latar belakang"
            midground_desc = "Meja kerja kayu gelap dengan berkas masterplan dan denah lantai"
            foreground_desc = "Gradien scrim gelap sinematik di bagian bawah untuk penempatan headline kontras tinggi"
            lighting_dir = "Directional twilight light dari sisi kanan dengan ambient warm glow"
            color_mood = "Obsidian navy, slate gray, dan aksen peringatan rose red"
            accent_hex = colors.accent_rose
            ns_region = TextSafeRegion.FULL_BOTTOM

        elif c_type == ContentType.PROPERTY_INSIGHT:
            visual_story = "Akselerasi infrastruktur tol modern melipatgandakan capital gain kawasan properti."
            focal_subject = "Jalur tol layang modern yang menghubungkan kawasan hunian terpadu"
            background_desc = "Panorama lanskap masterplan kota mandiri dengan pepohonan tropis dan cakrawala senja"
            midground_desc = "Gedung-gedung hunian modern dengan fasad kaca elegan"
            foreground_desc = "Gradien scrim gelap halus untuk kontras tipografi judul"
            lighting_dir = "Golden hour sunset lighting dengan pantulan hangat pada permukaan jalan dan kaca"
            color_mood = "Slate navy, deep indigo, dan warm sunset gold"
            accent_hex = colors.accent_primary
            ns_region = TextSafeRegion.FULL_BOTTOM

        elif c_type == ContentType.PROPERTY_LISTICLE:
            visual_story = "Struktur poin-poin kesalahan krusial yang harus dihentikan dalam follow-up leads properti."
            focal_subject = "Fasad arsitektur modern bertingkat dengan garis geometris tegas dan rapi"
            background_desc = "Distrik komersial modern dengan pencahayaan senja yang tenang"
            midground_desc = "Kisi-kisi arsitektur (louvers) yang menciptakan kedalaman visual ritmis"
            foreground_desc = "Area negatif bersih untuk susunan bullet points bernomor"
            lighting_dir = "Diffused overcast evening light dengan kontras bayangan lembut"
            color_mood = "Midnight navy, slate charcoal, dan aksen warm amber gold"
            accent_hex = colors.accent_gold
            ns_region = TextSafeRegion.FULL_BOTTOM

        elif c_type == ContentType.PROPERTY_CASE_STUDY:
            visual_story = "Transformasi empiris efisiensi respon pesan leads meningkatkan konversi survey lokasi 300%."
            focal_subject = "Gedung hunian mahasiswa (Rukost) modern yang beroperasi penuh dengan kamar terisi"
            background_desc = "Kawasan kampus universitas terkemuka dengan akses jalan tertata rapi"
            midground_desc = "Area parkir dan lobby penerima tamu dengan pencahayaan interior hangat"
            foreground_desc = "Box metrik data (+300%) dan area teks judul yang jernih"
            lighting_dir = "Late afternoon golden sun dengan ambient interior warm light"
            color_mood = "Obsidian navy, emerald growth green, dan champagne gold"
            accent_hex = colors.accent_emerald
            ns_region = TextSafeRegion.FULL_BOTTOM

        elif c_type == ContentType.PROPERTY_SHOWCASE:
            visual_story = "Showcase unit aset investasi Rukost premium dengan yield sewa tinggi dan legalitas aman."
            focal_subject = "Bangunan Rukost 3 lantai arsitektur tropis modern dengan balkon kaca dan tanaman hijau"
            background_desc = "Lingkungan perumahan tenang dan asri dekat kampus ternama"
            midground_desc = "Gerbang masuk eksklusif dengan pos keamanan dan papan nama proyek"
            foreground_desc = "Pill spesifikasi unit, badge lokasi, dan penawaran harga"
            lighting_dir = "Bright warm afternoon sun dengan pencahayaan natural yang tajam"
            color_mood = "Warm champagne gold, natural stone slate, dan obsidian navy"
            accent_hex = colors.accent_gold
            ns_region = TextSafeRegion.FULL_BOTTOM

        elif c_type == ContentType.PROPERTY_OPINION:
            visual_story = "Perspektif tegas mengenai masa depan digitalisasi dan otomasi pemasaran properti."
            focal_subject = "Komposisi arsitektur minimalis modern dengan bayangan diagonal kuat"
            background_desc = "Terrace ruang rapat eksekutif menghadap cakrawala kota"
            midground_desc = "Struktur beton ekspos dan kaca reflektif"
            foreground_desc = "Aksen tanda kutip editorial raksasa dan tipografi tebal"
            lighting_dir = "Dramatic side lighting chiaroscuro"
            color_mood = "Deep monochrome obsidian slate dan accent indigo"
            accent_hex = colors.accent_secondary
            ns_region = TextSafeRegion.FULL_BOTTOM

        else: # PROPERTY_EDUCATION & PROPERTY_SALES_OFFER
            visual_story = "Prinsip fundamental membangun sistem pemasaran properti yang berkelanjutan."
            focal_subject = "Pusat pemasaran properti modern dengan arsitektur kaca terbuka"
            background_desc = "Kawasan residensial terencana dengan taman tropis dan jalan aspal mulus"
            midground_desc = "Interior ruang konsultasi dengan pencahayaan lembut"
            foreground_desc = "Gradien scrim gelap untuk hierarki teks judul"
            lighting_dir = "Warm twilight ambient light"
            color_mood = "Obsidian navy dan electric sky cyan"
            accent_hex = colors.accent_primary
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
            asset_requirements=["background_scene", "foreground_scrim", "graphic_accents"],
            compositing_required=True
        )

    @staticmethod
    def create_art_direction(spec: EditorialContentSpecification) -> VisualArtDirectionSpecification:
        """Maintains full backward compatibility with Phase 3B."""
        concept = CreativeDirectorService.create_visual_concept(spec)
        colors = NUGI_PROPERTI_BRAND_PROFILE.colors

        accent_hex = colors.accent_primary
        if spec.content_type == ContentType.PROPERTY_PROBLEM:
            accent_hex = colors.accent_rose
        elif spec.content_type in (ContentType.PROPERTY_LISTICLE, ContentType.PROPERTY_SHOWCASE):
            accent_hex = colors.accent_gold
        elif spec.content_type == ContentType.PROPERTY_CASE_STUDY:
            accent_hex = colors.accent_emerald
        elif spec.content_type == ContentType.PROPERTY_OPINION:
            accent_hex = colors.accent_secondary

        image_prompt = (
            f"Cinematic 35mm architectural photography of {concept.focal_subject}, {concept.background_desc if hasattr(concept, 'background_desc') else concept.background_description}. "
            f"Lighting: {concept.lighting_direction}. Color atmosphere: {concept.color_mood}. "
            f"Preserve clean uncluttered dark negative space on the bottom half for editorial typography. "
            f"8k resolution, authentic textures, no text, no words, no letters, no watermark, no logo, pure photographic background asset."
        )

        return VisualArtDirectionSpecification(
            archetype=spec.suggested_archetype,
            subject=concept.focal_subject,
            environment=concept.background_description,
            camera_perspective="35mm architectural medium angle, cinematic depth",
            composition=f"Layered editorial visual aligned with {spec.suggested_archetype.value}",
            lighting=concept.lighting_direction,
            mood="Authoritative, prestigious, cinematic property media feel",
            color_atmosphere=concept.color_mood,
            negative_space_location=concept.negative_space_region,
            focal_point="top_center",
            depth="3-plane depth separation",
            background_treatment="photographic_layered",
            image_prompt=image_prompt,
            negative_prompt="text, words, letters, typography, watermark, logo, banner, poster, frame, UI elements, cartoon, blurry, low quality",
            text_safe_region=concept.text_safe_region,
            accent_color_hex=accent_hex,
            visual_symbolism=f"Represents strategic precision in {spec.content_type.value}"
        )

    @staticmethod
    def generate_visual_variants(
        editorial_spec: EditorialContentSpecification,
        base_design_spec: DesignSpecification
    ) -> List[VisualVariant]:
        """
        Generates 3 distinct art direction variants for the user to choose from:
        Variant A: Cinematic Hero Editorial
        Variant B: Minimalist Authority Editorial
        Variant C: Layered Editorial Composite
        """
        variants = []

        # Variant A: Cinematic Hero (Default)
        concept_a = CreativeDirectorService.create_visual_concept(editorial_spec)
        plan_a = AssetCompositorService.build_composition_plan(concept_a, base_design_spec.accent_color_hex or "#38bdf8")
        variants.append(VisualVariant(
            variant_name="Variant A: Cinematic Hero",
            concept=concept_a,
            composition_plan=plan_a,
            visual_qa_score=100
        ))

        # Variant B: Minimalist Authority
        concept_b = CreativeDirectorService.create_visual_concept(editorial_spec)
        concept_b.color_mood = "Deep obsidian monochrome with clean architectural lines"
        plan_b = AssetCompositorService.build_composition_plan(concept_b, "#6366f1")
        plan_b.color_grade.preset_name = "DEEP_OBSIDIAN"
        plan_b.color_grade.contrast = 1.25
        plan_b.color_grade.temperature = -0.15
        variants.append(VisualVariant(
            variant_name="Variant B: Minimalist Authority",
            concept=concept_b,
            composition_plan=plan_b,
            visual_qa_score=95
        ))

        # Variant C: Layered Editorial Composite
        concept_c = CreativeDirectorService.create_visual_concept(editorial_spec)
        concept_c.color_mood = "Warm champagne gold highlights and sunset glow"
        plan_c = AssetCompositorService.build_composition_plan(concept_c, "#f59e0b")
        plan_c.color_grade.preset_name = "PREMIUM_GOLD"
        plan_c.color_grade.temperature = 0.20
        variants.append(VisualVariant(
            variant_name="Variant C: Layered Composite",
            concept=concept_c,
            composition_plan=plan_c,
            visual_qa_score=98
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
