import io
from PIL import Image
from app.schemas.compositing import (
    VisualConceptSpecification,
    CompositionPlan,
    LayerSpecification,
    LayerType,
    BlendMode,
    ColorGradeSpecification,
    VisualVariant
)
from app.schemas.editorial_agent import ContentType, TextSafeRegion, UserBriefInput
from app.schemas.design_spec import DesignSpecification, CompositionType, CTAStrategy
from app.rendering.compositing_engine import ProfessionalCompositingEngine
from app.services.asset_compositor_service import AssetCompositorService
from app.services.creative_director_service import CreativeDirectorService
from app.services.content_generation_agent import ContentGenerationAgent


def test_visual_concept_specification():
    concept = VisualConceptSpecification(
        content_type=ContentType.PROPERTY_PROBLEM,
        visual_story="Leads boncos akibat waktu respon lambat",
        focal_subject="Sales manager properti memeriksa laptop di sales gallery",
        background_description="Maket arsitektural properti mewah di latar belakang",
        lighting_direction="Directional side light dari kanan",
        color_mood="Obsidian navy dan rose red",
        negative_space_region=TextSafeRegion.FULL_BOTTOM
    )
    assert concept.content_type == ContentType.PROPERTY_PROBLEM
    assert concept.compositing_required is True
    assert concept.negative_space_region == TextSafeRegion.FULL_BOTTOM


def test_blend_modes_execution():
    engine = ProfessionalCompositingEngine()
    base = Image.new("RGBA", (200, 200), (20, 30, 50, 255))
    overlay = Image.new("RGBA", (200, 200), (245, 158, 11, 180))

    for mode in [BlendMode.NORMAL, BlendMode.MULTIPLY, BlendMode.SCREEN, BlendMode.ADD, BlendMode.OVERLAY, BlendMode.SOFT_LIGHT]:
        blended = engine.apply_blend_mode(base, overlay, mode, opacity=0.8)
        assert blended is not None
        assert blended.size == (200, 200)


def test_color_grading_and_vignette():
    engine = ProfessionalCompositingEngine()
    test_img = Image.new("RGBA", (400, 400), (40, 60, 90, 255))
    grade = ColorGradeSpecification(
        exposure=0.1,
        contrast=1.2,
        saturation=1.1,
        temperature=0.15, # warm gold
        vignette_strength=0.5
    )
    graded = engine.apply_color_grading(test_img, grade)
    assert graded is not None
    assert graded.size == (400, 400)


def test_isolated_subject_generation():
    subj = AssetCompositorService.generate_isolated_subject(
        subject_desc="Modern architectural student residence facade",
        width=400,
        height=600
    )
    assert subj.image_bytes is not None
    assert subj.has_alpha is True
    assert subj.width == 400
    assert subj.height == 600


def test_13_layer_compositing_engine():
    engine = ProfessionalCompositingEngine()
    concept = VisualConceptSpecification(
        content_type=ContentType.PROPERTY_INSIGHT,
        visual_story="Akselerasi tol modern mendongkrak capital gain",
        focal_subject="Jalur tol layang dan perumahan modern",
        background_description="Panorama kota mandiri di waktu senja",
        lighting_direction="Golden hour sunset",
        color_mood="Slate navy dan sunset gold",
        negative_space_region=TextSafeRegion.FULL_BOTTOM
    )
    design_spec = DesignSpecification(
        composition_type=CompositionType.HERO_IMAGE_EDITORIAL,
        headline="KENAPA HARGA RUMAH DI DEKAT TOL BISA NAIK LEBIH CEPAT?",
        highlight_words=["HARGA RUMAH", "NAIK LEBIH CEPAT"],
        subheadline="Aksesibilitas dan infrastruktur melipatgandakan capital gain kawasan.",
        cta_strategy=CTAStrategy.CTA_NONE,
        width=1080,
        height=1350
    )
    plan = AssetCompositorService.build_composition_plan(concept)

    rendered_bytes, meta = engine.composite_full_artwork(
        concept=concept,
        design_spec=design_spec,
        plan=plan
    )
    assert rendered_bytes is not None
    assert "ProfessionalCompositingEngine" in meta["engine"]
    assert meta["layers_count"] == 13
    assert meta["width"] == 1080
    assert meta["height"] == 1350

    img = Image.open(io.BytesIO(rendered_bytes))
    assert img.size == (1080, 1350)


def test_three_visual_variants_generation():
    brief = UserBriefInput(
        topic="Kenapa leads iklan properti banyak tapi closing tetap rendah?",
        target_audience="Developer & Marketing Properti"
    )
    agent = ContentGenerationAgent()
    pkg = agent.generate_full_package(brief=brief)

    assert len(pkg.variants) == 3
    assert pkg.variants[0]["variant_name"] == "Variant A: Cinematic Hero"
    assert pkg.variants[1]["variant_name"] == "Variant B: Minimalist Authority"
    assert pkg.variants[2]["variant_name"] == "Variant C: Layered Composite"
    assert pkg.concept_spec is not None
    assert pkg.visual_qa.score >= 85


def test_modular_regenerate_with_compositing():
    agent = ContentGenerationAgent()
    brief = UserBriefInput(
        topic="3 Kesalahan fatal follow up leads properti",
        target_audience="Sales Manager"
    )
    pkg = agent.generate_full_package(brief=brief)

    # Regenerate Headline with compositing
    rehead_pkg = agent.regenerate_headline(pkg, custom_topic="5 Kesalahan fatal tim sales properti")
    assert rehead_pkg.editorial_spec.headline is not None
    assert rehead_pkg.rendered_asset_path is not None

    # Regenerate Visual Concept with compositing
    reart_pkg = agent.regenerate_visual_art(pkg, archetype_override=CompositionType.HERO_IMAGE_EDITORIAL)
    assert reart_pkg.art_direction_spec.archetype == CompositionType.HERO_IMAGE_EDITORIAL
