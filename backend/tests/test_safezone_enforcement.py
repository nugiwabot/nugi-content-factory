import pytest
import io
from PIL import Image
from app.schemas.design_spec import (
    DesignSpecification,
    CompositionType,
    CTAStrategy,
    SAFEZONE_TOP,
    SAFEZONE_BOTTOM,
    SAFEZONE_HEIGHT,
    SAFEZONE_LEFT,
    SAFEZONE_RIGHT,
    SAFEZONE_CONTENT_LEFT,
    SAFEZONE_CONTENT_RIGHT,
    CANVAS_WIDTH,
    CANVAS_HEIGHT,
    GRID_3_4_WIDTH,
    GRID_3_4_CROP_SIDE
)
from app.schemas.editorial_agent import ContentType, UserBriefInput
from app.schemas.visual_qa import VisualQAResult
from app.rendering.layout import LayoutEngine
from app.rendering.compositing_engine import ProfessionalCompositingEngine
from app.services.visual_qa import VisualQAService
from app.services.content_generation_agent import ContentGenerationAgent


def test_safezone_constants_and_dimensions():
    """Validates Master Canvas and Safezone Dimension Constants."""
    assert CANVAS_WIDTH == 1080
    assert CANVAS_HEIGHT == 1350
    assert GRID_3_4_WIDTH == 1012
    assert GRID_3_4_CROP_SIDE == 34
    
    assert SAFEZONE_TOP == 135
    assert SAFEZONE_BOTTOM == 1215
    assert SAFEZONE_HEIGHT == 1080
    assert SAFEZONE_LEFT == 34
    assert SAFEZONE_RIGHT == 1046
    assert SAFEZONE_CONTENT_LEFT == 76
    assert SAFEZONE_CONTENT_RIGHT == 1004


def test_element_bounding_box_validator():
    """Validates individual bounding box checks."""
    # 1. Valid box inside content safezone [76..1004, 135..1215]
    valid_box = {"left": 76, "top": 155, "right": 250, "bottom": 190}
    is_valid, violations = LayoutEngine.validate_element_bounding_box(valid_box)
    assert is_valid is True
    assert len(violations) == 0

    # 2. Box overflowing left
    overflow_left = {"left": 40, "top": 200, "right": 300, "bottom": 260}
    is_valid, violations = LayoutEngine.validate_element_bounding_box(overflow_left)
    assert is_valid is False
    assert any("Left bound" in v for v in violations)

    # 3. Box overflowing bottom
    overflow_bottom = {"left": 76, "top": 1180, "right": 500, "bottom": 1250}
    is_valid, violations = LayoutEngine.validate_element_bounding_box(overflow_bottom)
    assert is_valid is False
    assert any("Bottom bound" in v for v in violations)


def test_debug_mode_isolation_and_production_cleanliness():
    """Ensures production rendering is clean and debug mode renders diagnostic overlay."""
    engine = ProfessionalCompositingEngine()
    spec = DesignSpecification(
        headline="LEADS IKLAN MASUK, TAPI SALES LAMBAT FOLLOW-UP?",
        subheadline="Setiap menit keterlambatan membuat calon pembeli beralih ke developer lain.",
        highlight_words=["LAMBAT FOLLOW-UP?"],
        badge_text="STRATEGI FOLLOW UP",
        cta_strategy=CTAStrategy.CTA_NONE,
        width=1080,
        height=1350
    )

    # 1. Production Mode: debug_safezone=False
    prod_bytes, prod_meta = engine.composite_full_artwork(design_spec=spec, debug_safezone=False)
    assert prod_meta["debug_safezone"] is False
    assert len(prod_bytes) > 0
    prod_img = Image.open(io.BytesIO(prod_bytes))
    assert prod_img.size == (1080, 1350)

    # 2. Debug Mode: debug_safezone=True
    debug_bytes, debug_meta = engine.composite_full_artwork(design_spec=spec, debug_safezone=True)
    assert debug_meta["debug_safezone"] is True
    assert len(debug_bytes) > 0
    debug_img = Image.open(io.BytesIO(debug_bytes))
    assert debug_img.size == (1080, 1350)


def test_all_ten_content_categories_safezone_enforcement():
    """
    Tests full generation across all 10 Editorial Categories:
    Verifies 100% Critical Element Safezone Pass and Profile Grid Resilience.
    """
    agent = ContentGenerationAgent()
    
    test_briefs = [
        # 1. Problem
        UserBriefInput(topic="Leads iklan masuk, tapi sales lambat follow-up?"),
        # 2. Education
        UserBriefInput(topic="Kenapa properti di lokasi bagus belum tentu cepat laku?"),
        # 3. Insight
        UserBriefInput(topic="Harga rumah naik, tapi daya beli tidak ikut naik"),
        # 4. Listicle / Number List
        UserBriefInput(topic="3 Kesalahan Saat Membeli Properti Pertama"),
        # 5. Case Study
        UserBriefInput(topic="Bagaimana satu properti meningkatkan conversion rate 300%"),
        # 6. Data Editorial
        UserBriefInput(topic="Data & Statistik yield sewa properti komersial 2026"),
        # 7. Opinion
        UserBriefInput(topic="Developer properti yang menolak otomasi akan tertinggal"),
        # 8. Property Showcase
        UserBriefInput(topic="Rumah Premium Dekat Kota Baru Parahyangan"),
        # 9. Soft Selling
        UserBriefInput(topic="Gaya hidup asri residensial hijau dengan clubhouse modern"),
        # 10. Direct Offer
        UserBriefInput(topic="Daftar audit funnel marketing properti slot terbatas konsultasi gratis")
    ]

    for brief in test_briefs:
        pkg = agent.generate_full_package(brief=brief, image_provider_type="mock")
        qa: VisualQAResult = pkg.visual_qa

        assert qa.safezone_pass is True, f"Failed safezone_pass for topic: {brief.topic} (Issues: {qa.issues})"
        assert qa.safezone_critical_element_pass is True
        assert qa.text_bounding_box_pass is True
        assert qa.profile_grid_pass is True
        assert qa.non_regression_pass is True
        assert qa.technical_pass is True
        assert qa.design_pass is True
        assert qa.editorial_pass is True
        assert qa.brand_pass is True
        assert qa.score >= 90


def test_headline_length_variations_and_safezone_bounds():
    """Tests short, medium, and long headlines with adaptive layout wrapping."""
    engine = ProfessionalCompositingEngine()
    
    variations = [
        ("HEADLINE SINGKAT", ["SINGKAT"]),
        ("TIGA KATA HEADLINE", ["HEADLINE"]),
        ("LEADS IKLAN MASUK, TAPI SALES LAMBAT FOLLOW-UP?", ["LAMBAT FOLLOW-UP?"]),
        ("BAGAIMANA SATU PROPERTI BISA MENINGKATKAN CONVERSION RATE CLOSING SALES HINGGA TIGA RATUS PERSEN", ["CONVERSION RATE"])
    ]

    for hl, hw in variations:
        spec = DesignSpecification(
            headline=hl,
            subheadline="Penjelasan konteks strategi editorial untuk audiens developer.",
            highlight_words=hw,
            badge_text="INSIGHT",
            cta_strategy=CTAStrategy.CTA_NONE,
            width=1080,
            height=1350
        )
        _, meta = engine.composite_full_artwork(design_spec=spec)
        qa = VisualQAService.evaluate_design(spec, meta)

        assert qa.safezone_pass is True, f"Headline variation failed: {hl} (Issues: {qa.issues})"
        assert "headline_block" in meta["critical_element_bounding_boxes"]
        assert "highlight_pill" in meta["critical_element_bounding_boxes"]
        
        # Verify pill is within [76..1004, 135..1215]
        pill_box = meta["critical_element_bounding_boxes"]["highlight_pill"]
        assert pill_box["left"] >= SAFEZONE_CONTENT_LEFT
        assert pill_box["right"] <= SAFEZONE_CONTENT_RIGHT
        assert pill_box["top"] >= SAFEZONE_TOP
        assert pill_box["bottom"] <= SAFEZONE_BOTTOM
