import io
from PIL import Image
from app.rendering.layout import LayoutEngine
from app.rendering.engine import DeterministicRenderingEngine
from app.providers.mock_image import MockImageProvider


def test_layout_text_wrap():
    text = "Cara Cepat Menangani Leads Properti dari Iklan Meta Agar Tidak Boncos dan Langsung Closing"
    wrapped = LayoutEngine.wrap_text(text, max_chars_per_line=20)
    assert len(wrapped) > 1
    for line in wrapped:
        assert len(line) <= 25


def test_layout_contrast_calculation():
    white = (255, 255, 255)
    black = (0, 0, 0)
    ratio = LayoutEngine.calculate_contrast_ratio(white, black)
    assert ratio >= 20.0 # Standard maximum contrast


def test_deterministic_rendering_engine():
    img_provider = MockImageProvider()
    bg_output = img_provider.generate_background("Modern test background", 500, 500)
    
    engine = DeterministicRenderingEngine()
    rendered_bytes, meta = engine.render(
        background_bytes=bg_output.image_bytes,
        headline="Strategi Efektif Follow Up Leads",
        category_badge="MARKETING PROPERTI",
        hook_text="Respon cepat di bawah 15 menit meningkatkan closing 300%.",
        brand_name="NugiProperti Studio",
        width=500,
        height=500
    )

    assert rendered_bytes is not None
    assert len(rendered_bytes) > 500
    assert meta["width"] == 500
    assert meta["height"] == 500

    # Verify Pillow can open the generated image
    img = Image.open(io.BytesIO(rendered_bytes))
    assert img.size == (500, 500)
