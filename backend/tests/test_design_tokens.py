from app.brand.tokens import ColorSystem, TypographySystem, SpacingSystem
from app.rendering.layout import LayoutEngine


def test_color_tokens_rgb_conversion():
    colors = ColorSystem()
    rgb = colors.get_rgb(colors.background_dark)
    assert rgb == (7, 11, 20)
    
    cyan_rgb = colors.get_rgb(colors.accent_primary)
    assert cyan_rgb == (56, 189, 248)


def test_typography_hierarchy_tokens():
    typo = TypographySystem()
    assert typo.display.font_size > typo.h1.font_size
    assert typo.h1.font_size > typo.h2.font_size
    assert typo.h2.font_size > typo.body.font_size
    assert typo.body.font_size > typo.caption.font_size


def test_contrast_ratio_on_dark_surface():
    colors = ColorSystem()
    white_rgb = (255, 255, 255)
    bg_rgb = colors.get_rgb(colors.background_dark)
    contrast = LayoutEngine.calculate_contrast_ratio(white_rgb, bg_rgb)
    assert contrast >= 15.0 # Well above WCAG AAA (7.0)
