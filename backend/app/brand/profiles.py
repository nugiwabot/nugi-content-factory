from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from app.brand.tokens import (
    ColorSystem,
    TypographySystem,
    SpacingSystem,
    LogoConfiguration,
    LayoutRules
)


class BrandProfileSpec(BaseModel):
    """
    Configurable brand profile schema capable of driving the entire design brain.
    """
    brand_name: str = Field(default="NugiProperti")
    brand_tagline: str = Field(default="Sistem Pemasaran & Pertumbuhan Properti Modern")
    brand_description: str = Field(
        default="Otoritas strategi pemasaran digital dan sistem konversi leads untuk pengembang properti dan kantor agen."
    )
    brand_personality: str = Field(
        default="PREMIUM, MODERN, CINEMATIC, TRUSTWORTHY, BUSINESS, TECHNOLOGY, PROPERTY"
    )
    target_audience: str = Field(
        default="Developer Property, Owner Developer, Principal Agen, Sales Manager, Marketing Lead"
    )
    visual_personality: str = Field(
        default="Dark cinematic atmosphere, high contrast, bold headline typography, key phrase highlights, clean negative space, editorial authority."
    )
    
    # Semantic Systems
    colors: ColorSystem = Field(default_factory=ColorSystem)
    typography: TypographySystem = Field(default_factory=TypographySystem)
    spacing: SpacingSystem = Field(default_factory=SpacingSystem)
    logo: LogoConfiguration = Field(default_factory=LogoConfiguration)
    layout: LayoutRules = Field(default_factory=LayoutRules)

    metadata: Dict[str, Any] = Field(default_factory=dict)


# Official Singleton Profile for NugiProperti
NUGI_PROPERTI_BRAND_PROFILE = BrandProfileSpec(
    brand_name="NugiProperti",
    brand_tagline="Sistem Pemasaran & Pertumbuhan Properti Modern",
    brand_description="Sistem otomasi dan otoritas konten edukasi konversi tinggi untuk developer dan agen properti.",
    brand_personality="PREMIUM, MODERN, CINEMATIC, TRUSTWORTHY, BUSINESS, TECHNOLOGY, PROPERTY",
    target_audience="Developer Property, Owner Developer, Principal Agen, Sales Manager",
    visual_personality="Dark luxury cinematic aesthetic, electric sky cyan accent, gold yield highlights, crisp typography, clean glassmorphism.",
    colors=ColorSystem(
        background_dark="#070b14",
        surface_dark="#0c1220",
        surface_card="#0f172a",
        surface_elevated="#162238",
        text_primary="#ffffff",
        text_secondary="#cbd5e1",
        text_muted="#94a3b8",
        accent_primary="#38bdf8",
        accent_secondary="#6366f1",
        accent_gold="#f59e0b",
        accent_emerald="#10b981",
        accent_rose="#f43f5e"
    ),
    typography=TypographySystem(),
    spacing=SpacingSystem(),
    logo=LogoConfiguration(
        placement="top_left",
        fallback_text="NugiProperti",
        fallback_symbol="⚡"
    ),
    layout=LayoutRules(
        primary_width=1080,
        primary_height=1350
    )
)
