from app.services.visual_qa import VisualQAService
from app.schemas.design_spec import DesignSpecification


def test_visual_qa_perfect_score():
    spec = DesignSpecification(
        template_id="01_PROPERTY_PROBLEM",
        width=1080,
        height=1350,
        headline="LEADS IKLAN MASUK, TAPI SALES LAMBAT FOLLOW-UP?",
        highlight_words=["LAMBAT FOLLOW-UP"],
        subheadline="Setiap menit keterlambatan bisa membuat prospek berpindah ke kompetitor.",
        badge_text="DILEMA SALES PROPERTI",
        cta_text="Pelajari Solusinya →"
    )

    qa = VisualQAService.evaluate_design(spec)
    assert qa.score >= 90
    assert qa.readability == "EXCELLENT"
    assert qa.safe_area_compliant is True
    assert len(qa.issues) == 0


def test_visual_qa_detects_invalid_dimension_and_short_headline():
    spec = DesignSpecification(
        template_id="01_PROPERTY_PROBLEM",
        width=800,
        height=600, # Invalid dimensions
        headline="Pendek" # Too short
    )

    qa = VisualQAService.evaluate_design(spec)
    assert qa.score < 70
    assert any("Dimensi canvas" in issue for issue in qa.issues)
    assert any("terlalu pendek" in issue for issue in qa.issues)
