from typing import Dict, Any, Tuple
from pydantic import BaseModel, Field


class ColorSystem(BaseModel):
    """
    Semantic Design Color Tokens for NugiProperti.
    No raw hex codes should be scattered across the rendering engine.
    """
    # Backgrounds & Surfaces (Dark & Cinematic atmosphere)
    background_dark: str = Field(default="#070b14", description="Deep cinematic obsidian navy canvas background")
    surface_dark: str = Field(default="#0c1220", description="Secondary dark background container")
    surface_card: str = Field(default="#0f172a", description="Glassmorphic card surface")
    surface_elevated: str = Field(default="#162238", description="Elevated card or active section")
    surface_overlay: str = Field(default="rgba(7, 11, 20, 0.85)", description="Scrim overlay for high background contrast")

    # Typography & Text hierarchy
    text_primary: str = Field(default="#ffffff", description="Crisp high-contrast pure white for display & headlines")
    text_secondary: str = Field(default="#cbd5e1", description="Soft off-white for subheadings and key takeaways")
    text_muted: str = Field(default="#94a3b8", description="Slate gray for body copy and supporting descriptions")
    text_dim: str = Field(default="#64748b", description="Dark slate for metadata and timestamps")

    # Accents (Business, Tech, Property authority)
    accent_primary: str = Field(default="#38bdf8", description="Electric Sky Cyan — Tech & Innovation")
    accent_secondary: str = Field(default="#6366f1", description="Deep Indigo — Business Authority")
    accent_gold: str = Field(default="#f59e0b", description="Warm Amber/Gold — High-yield Investment & Wealth")
    accent_emerald: str = Field(default="#10b981", description="Emerald Green — Growth & Success Metrics")
    accent_rose: str = Field(default="#f43f5e", description="Rose Red — High-urgency Warnings & Critical Errors")

    # Borders & Lines
    border_subtle: str = Field(default="rgba(255, 255, 255, 0.08)", description="Very subtle division line")
    border_card: str = Field(default="rgba(255, 255, 255, 0.12)", description="Standard card boundary")
    border_highlight: str = Field(default="rgba(56, 189, 248, 0.45)", description="Cyan accent border")

    def get_rgb(self, hex_code: str, fallback: Tuple[int, int, int] = (255, 255, 255)) -> Tuple[int, int, int]:
        try:
            h = hex_code.lstrip("#")
            if len(h) == 6:
                return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
            elif len(h) == 3:
                return tuple(int(h[i]*2, 16) for i in range(3))
        except Exception:
            pass
        return fallback


class TypographyToken(BaseModel):
    font_size: int
    line_height_multiplier: float
    max_chars_per_line: int
    font_weight: str = "bold"
    letter_spacing: int = 0
    safe_max_lines: int = 4


class TypographySystem(BaseModel):
    """
    Mobile-first Typography hierarchy ensuring maximum readability on smartphones.
    """
    font_family_primary: str = "sans-serif" # Plus Jakarta Sans / Inter / Arial
    font_family_mono: str = "monospace"     # JetBrains Mono / Courier

    display: TypographyToken = Field(
        default=TypographyToken(font_size=64, line_height_multiplier=1.18, max_chars_per_line=18, font_weight="800", safe_max_lines=3)
    )
    h1: TypographyToken = Field(
        default=TypographyToken(font_size=52, line_height_multiplier=1.22, max_chars_per_line=22, font_weight="700", safe_max_lines=4)
    )
    h2: TypographyToken = Field(
        default=TypographyToken(font_size=38, line_height_multiplier=1.26, max_chars_per_line=28, font_weight="700", safe_max_lines=4)
    )
    body: TypographyToken = Field(
        default=TypographyToken(font_size=24, line_height_multiplier=1.35, max_chars_per_line=38, font_weight="normal", safe_max_lines=5)
    )
    label: TypographyToken = Field(
        default=TypographyToken(font_size=20, line_height_multiplier=1.2, max_chars_per_line=30, font_weight="700", safe_max_lines=1)
    )
    caption: TypographyToken = Field(
        default=TypographyToken(font_size=18, line_height_multiplier=1.2, max_chars_per_line=45, font_weight="normal", safe_max_lines=2)
    )
    cta: TypographyToken = Field(
        default=TypographyToken(font_size=24, line_height_multiplier=1.1, max_chars_per_line=24, font_weight="800", safe_max_lines=1)
    )


class SpacingSystem(BaseModel):
    """Consistent 8pt-based spacing scale."""
    xs: int = 4
    sm: int = 8
    md: int = 16
    lg: int = 24
    xl: int = 32
    xxl: int = 48
    xxxl: int = 64
    huge: int = 80


class LogoConfiguration(BaseModel):
    """Rules and placement for brand logos."""
    placement: str = "top_left" # top_left, top_center, bottom_left, bottom_right
    max_width: int = 220
    max_height: int = 64
    safe_margin_x: int = 64
    safe_margin_y: int = 64
    opacity: float = 1.0
    fallback_text: str = "NugiProperti"
    fallback_symbol: str = "⚡"


class LayoutRules(BaseModel):
    """Grid and canvas dimensions rules for Instagram formats."""
    primary_width: int = 1080
    primary_height: int = 1350 # 4:5 Instagram Portrait Feed (Optimal Mobile Viewport)
    secondary_width: int = 1080
    secondary_height: int = 1080 # 1:1 Instagram Square Feed

    safe_area_margin_x: int = 64
    safe_area_margin_y: int = 80
    card_padding_x: int = 44
    card_padding_y: int = 48
    card_radius: int = 24
    negative_space_min_ratio: float = 0.25
