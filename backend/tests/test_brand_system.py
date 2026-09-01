from app.brand.profiles import NUGI_PROPERTI_BRAND_PROFILE, BrandProfileSpec
from app.brand.tokens import ColorSystem, TypographySystem, LayoutRules


def test_nugi_properti_brand_profile():
    profile = NUGI_PROPERTI_BRAND_PROFILE
    assert profile.brand_name == "NugiProperti"
    assert "PREMIUM" in profile.brand_personality
    assert "CINEMATIC" in profile.brand_personality
    assert profile.layout.primary_width == 1080
    assert profile.layout.primary_height == 1350
    assert profile.colors.accent_primary == "#38bdf8"
    assert profile.colors.accent_gold == "#f59e0b"
    assert profile.typography.display.font_size >= 60


def test_custom_brand_profile_creation():
    custom_profile = BrandProfileSpec(
        brand_name="Custom Real Estate Client",
        colors=ColorSystem(accent_primary="#10b981")
    )
    assert custom_profile.brand_name == "Custom Real Estate Client"
    assert custom_profile.colors.accent_primary == "#10b981"
