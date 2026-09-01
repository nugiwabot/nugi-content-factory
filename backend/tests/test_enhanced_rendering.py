import io
from PIL import Image
from app.rendering.template_renderer import TemplateRenderer
from app.schemas.design_spec import DesignSpecification
from app.rendering.layout import LayoutEngine


def test_word_highlighting_segmentation():
    line = "LEADS IKLAN MASUK, TAPI SALES LAMBAT FOLLOW-UP?"
    segments = LayoutEngine.segment_highlighted_line(line, ["LAMBAT FOLLOW-UP"])
    
    has_highlight = any(is_hl for _, is_hl in segments)
    assert has_highlight is True


def test_template_renderer_1080x1350():
    renderer = TemplateRenderer()
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

    rendered_bytes, meta = renderer.render_spec(spec)
    assert rendered_bytes is not None
    assert len(rendered_bytes) > 1000
    assert meta["width"] == 1080
    assert meta["height"] == 1350
    assert meta["aspect_ratio"] == "4:5"

    img = Image.open(io.BytesIO(rendered_bytes))
    assert img.size == (1080, 1350)


def test_template_renderer_square_1080x1080():
    renderer = TemplateRenderer()
    spec = DesignSpecification(
        template_id="03_NUMBER_LIST",
        width=1080,
        height=1080,
        headline="5 Kesalahan Follow-Up yang Bikin Leads Hilang",
        bullet_points=[
            "Menghubungi lebih dari 30 menit",
            "Template chat kaku tanpa personalisasi",
            "Tidak follow up kedua kalinya"
        ],
        badge_text="5 POIN KRUSIAL",
        cta_text="Simpan Panduan Ini"
    )

    rendered_bytes, meta = renderer.render_spec(spec)
    assert meta["width"] == 1080
    assert meta["height"] == 1080
    assert meta["aspect_ratio"] == "1:1"

    img = Image.open(io.BytesIO(rendered_bytes))
    assert img.size == (1080, 1080)
