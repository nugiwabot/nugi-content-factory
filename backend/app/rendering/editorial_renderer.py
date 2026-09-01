import io
import time
from typing import Dict, Any, Tuple, Optional, List
from PIL import Image, ImageDraw, ImageFont, ImageFilter

from app.brand.profiles import NUGI_PROPERTI_BRAND_PROFILE
from app.brand.tokens import ColorSystem
from app.schemas.design_spec import (
    DesignSpecification,
    CompositionType,
    CTAStrategy,
    ImageStrategy,
    OverlayStrategy
)
from app.rendering.layout import LayoutEngine
from app.core.errors import RenderingError
from app.core.logging import logger


class EditorialRenderer:
    """
    Professional Editorial Visual Composition Engine for NugiProperti.
    Transforms raw content into high-end social media editorial layouts
    (1080x1350 Portrait Feed 4:5 and 1080x1080 Square).
    """
    def __init__(self):
        self.colors = NUGI_PROPERTI_BRAND_PROFILE.colors

    def _hex_to_rgb(self, hex_code: str, fallback: Tuple[int, int, int] = (15, 23, 42)) -> Tuple[int, int, int]:
        try:
            h = hex_code.lstrip("#")
            if len(h) == 6:
                return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
            elif len(h) == 3:
                return tuple(int(h[i]*2, 16) for i in range(3))
        except Exception:
            pass
        return fallback

    def _load_font(self, size: int, bold: bool = False) -> ImageFont.ImageFont:
        font_names = ["arialbd.ttf" if bold else "arial.ttf", "arial.ttf", "DejaVuSans-Bold.ttf", "DejaVuSans.ttf"]
        for fn in font_names:
            try:
                return ImageFont.truetype(fn, size)
            except IOError:
                continue
        return ImageFont.load_default()

    def _apply_directional_gradient(
        self,
        base_img: Image.Image,
        overlay_strategy: OverlayStrategy,
        scrim_color: Tuple[int, int, int] = (7, 11, 20)
    ) -> Image.Image:
        """Applies smooth cinematic gradient overlays for high text contrast."""
        width, height = base_img.size
        gradient_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(gradient_layer)

        if overlay_strategy == OverlayStrategy.cinematic_gradient_bottom:
            start_y = int(height * 0.30)
            for y in range(start_y, height):
                alpha = int(((y - start_y) / (height - start_y)) ** 1.35 * 248)
                draw.line([(0, y), (width, y)], fill=(scrim_color[0], scrim_color[1], scrim_color[2], min(alpha, 252)))

        elif overlay_strategy == OverlayStrategy.cinematic_gradient_top:
            end_y = int(height * 0.70)
            for y in range(0, end_y):
                alpha = int(((end_y - y) / end_y) ** 1.35 * 248)
                draw.line([(0, y), (width, y)], fill=(scrim_color[0], scrim_color[1], scrim_color[2], min(alpha, 252)))

        elif overlay_strategy == OverlayStrategy.directional_vignette:
            # Full dark vignette with strong edge falloff
            for y in range(height):
                for x in (0, width - 1):
                    pass
            # General scrim + bottom boost
            for y in range(height):
                alpha = int(90 + (y / height) * 155)
                draw.line([(0, y), (width, y)], fill=(scrim_color[0], scrim_color[1], scrim_color[2], alpha))

        else: # subtle_scrim or default
            for y in range(height):
                alpha = int(120 + (y / height) * 125)
                draw.line([(0, y), (width, y)], fill=(scrim_color[0], scrim_color[1], scrim_color[2], alpha))

        return Image.alpha_composite(base_img.convert("RGBA"), gradient_layer)

    def render(
        self,
        spec: DesignSpecification,
        background_bytes: Optional[bytes] = None
    ) -> Tuple[bytes, Dict[str, Any]]:
        """
        Renders an editorial composition according to the composition archetype.
        """
        start_time = time.time()
        try:
            width = spec.width or 1080
            height = spec.height or 1350
            comp_type = spec.composition_type

            # Determine Accent Color
            accent_hex = spec.accent_color_hex or self.colors.accent_primary
            if comp_type == CompositionType.DATA_EDITORIAL or comp_type == CompositionType.PROPERTY_SHOWCASE:
                accent_hex = spec.accent_color_hex or self.colors.accent_gold
            elif comp_type == CompositionType.MINIMAL_EDITORIAL:
                accent_hex = spec.accent_color_hex or self.colors.accent_secondary

            accent_rgb = self._hex_to_rgb(accent_hex)

            # 1. Base Photographic Canvas Setup
            if background_bytes and len(background_bytes) > 0:
                base_img = Image.open(io.BytesIO(background_bytes)).convert("RGBA")
                if base_img.size != (width, height):
                    base_img = base_img.resize((width, height), Image.Resampling.LANCZOS)
            else:
                from app.providers.mock_image import MockImageProvider
                mock_gen = MockImageProvider()
                mock_out = mock_gen.generate_background(spec.headline, width, height)
                base_img = Image.open(io.BytesIO(mock_out.image_bytes)).convert("RGBA")

            # 2. Composition Specific Rendering Branch
            if comp_type == CompositionType.SPLIT_EDITORIAL:
                rendered_img = self._render_split_editorial(base_img, spec, width, height, accent_rgb)
            elif comp_type == CompositionType.CINEMATIC_OVERLAY:
                rendered_img = self._render_cinematic_overlay(base_img, spec, width, height, accent_rgb)
            elif comp_type == CompositionType.DATA_EDITORIAL:
                rendered_img = self._render_data_editorial(base_img, spec, width, height, accent_rgb)
            elif comp_type == CompositionType.LIST_EDITORIAL:
                rendered_img = self._render_list_editorial(base_img, spec, width, height, accent_rgb)
            elif comp_type == CompositionType.MINIMAL_EDITORIAL:
                rendered_img = self._render_minimal_editorial(base_img, spec, width, height, accent_rgb)
            elif comp_type == CompositionType.PROPERTY_SHOWCASE:
                rendered_img = self._render_property_showcase(base_img, spec, width, height, accent_rgb)
            else: # HERO_IMAGE_EDITORIAL (Default)
                rendered_img = self._render_hero_image_editorial(base_img, spec, width, height, accent_rgb)

            # 3. Export to PNG
            buffer = io.BytesIO()
            final_rgb = rendered_img.convert("RGB")
            final_rgb.save(buffer, format="PNG", optimize=True)
            rendered_bytes = buffer.getvalue()

            latency_ms = int((time.time() - start_time) * 1000)
            render_metadata = {
                "composition_type": comp_type.value,
                "width": width,
                "height": height,
                "aspect_ratio": "4:5" if height == 1350 else "1:1",
                "cta_strategy": spec.cta_strategy.value,
                "accent_color": accent_hex,
                "highlight_words": spec.highlight_words,
                "render_latency_ms": max(latency_ms, 12),
                "engine": "EditorialRenderer_v3A"
            }
            return rendered_bytes, render_metadata

        except Exception as e:
            logger.exception(f"Editorial visual rendering failed: {str(e)}")
            raise RenderingError(f"Failed to render editorial visual: {str(e)}")

    # --------------------------------------------------------------------------
    # ARCHETYPE 1: HERO IMAGE EDITORIAL (60-80% Visual Dominance + Deep Gradient)
    # --------------------------------------------------------------------------
    def _render_hero_image_editorial(self, base_img: Image.Image, spec: DesignSpecification, width: int, height: int, accent_rgb: Tuple[int, int, int]) -> Image.Image:
        img = self._apply_directional_gradient(base_img, spec.overlay_strategy)
        draw = ImageDraw.Draw(img)

        pad_x = int(width * 0.075) # 80px safe margin
        curr_y = int(height * 0.44) # Text placed on the bottom 56%

        # Eyebrow Category Pill
        badge_text = (spec.badge_text or "MARKET INSIGHT").upper().strip()
        badge_font = self._load_font(22, bold=True)
        draw.text((pad_x, curr_y), f"✦ {badge_text}", fill=accent_rgb, font=badge_font)
        curr_y += 38

        # Primary Display Headline with Word Highlights
        max_headline_w = width - (pad_x * 2)
        wrapped_headline = LayoutEngine.wrap_text(spec.headline, max_chars_per_line=19)
        headline_font, font_size = LayoutEngine.get_fitted_font(
            wrapped_headline,
            max_width=max_headline_w,
            max_height=int(height * 0.32),
            initial_size=58,
            min_size=32
        )

        for line in wrapped_headline:
            segments = LayoutEngine.segment_highlighted_line(line, spec.highlight_words)
            lh = LayoutEngine.draw_highlighted_line(
                draw=draw,
                x=pad_x,
                y=curr_y,
                segments=segments,
                font=headline_font,
                primary_color=(255, 255, 255, 255),
                highlight_color=(accent_rgb[0], accent_rgb[1], accent_rgb[2], 255),
                with_shadow=True
            )
            curr_y += lh + int(font_size * 0.24)

        curr_y += 18

        # Supporting Editorial Subheadline
        if spec.subheadline:
            sub_font = self._load_font(25, bold=False)
            wrapped_sub = LayoutEngine.wrap_text(spec.subheadline, max_chars_per_line=36)
            for s_line in wrapped_sub[:3]:
                draw.text((pad_x, curr_y), s_line, fill=(203, 213, 225, 255), font=sub_font)
                s_bbox = draw.textbbox((0, 0), s_line, font=sub_font)
                curr_y += (s_bbox[3] - s_bbox[1]) + 8

        # Render CTA ONLY if explicitly required
        if spec.cta_strategy == CTAStrategy.CTA_REQUIRED and spec.cta_text:
            cta_font = self._load_font(22, bold=True)
            cta_y = height - 140
            cta_rect = [pad_x, cta_y, pad_x + 320, cta_y + 54]
            draw.rounded_rectangle(cta_rect, radius=14, fill=accent_rgb)
            draw.text((pad_x + 24, cta_y + 14), spec.cta_text, fill=(7, 11, 20, 255), font=cta_font)

        # Brand Footer & Separator Line
        footer_y = height - 64
        draw.line([(pad_x, footer_y - 12), (width - pad_x, footer_y - 12)], fill=(255, 255, 255, 35), width=1)
        footer_font = self._load_font(18, bold=True)
        draw.text((pad_x, footer_y), f"⚡ {spec.brand_name.upper()}", fill=(148, 163, 184, 240), font=footer_font)
        draw.text((width - pad_x - 160, footer_y), "Property Editorial", fill=(100, 116, 139, 240), font=footer_font)

        return img

    # --------------------------------------------------------------------------
    # ARCHETYPE 2: SPLIT EDITORIAL (50/50 Image Top, Typography Bottom)
    # --------------------------------------------------------------------------
    def _render_split_editorial(self, base_img: Image.Image, spec: DesignSpecification, width: int, height: int, accent_rgb: Tuple[int, int, int]) -> Image.Image:
        img = Image.new("RGBA", (width, height), (7, 11, 20, 255))
        
        # Crop & place hero image in top 48%
        split_h = int(height * 0.48)
        top_visual = base_img.crop((0, 0, width, split_h))
        img.paste(top_visual, (0, 0))

        # Dividing gradient scrim
        draw = ImageDraw.Draw(img)
        for y in range(split_h - 80, split_h):
            alpha = int(((y - (split_h - 80)) / 80) * 255)
            draw.line([(0, y), (width, y)], fill=(7, 11, 20, alpha))

        # Thin accent hairline
        draw.line([(0, split_h), (width, split_h)], fill=(accent_rgb[0], accent_rgb[1], accent_rgb[2], 180), width=2)

        # Typography bottom half
        pad_x = int(width * 0.075)
        curr_y = split_h + 36

        badge_text = (spec.badge_text or "ANALISIS").upper().strip()
        badge_font = self._load_font(20, bold=True)
        draw.text((pad_x, curr_y), f"● {badge_text}", fill=accent_rgb, font=badge_font)
        curr_y += 36

        wrapped_headline = LayoutEngine.wrap_text(spec.headline, max_chars_per_line=20)
        headline_font, font_size = LayoutEngine.get_fitted_font(
            wrapped_headline,
            max_width=width - (pad_x * 2),
            max_height=int(height * 0.28),
            initial_size=52,
            min_size=28
        )

        for line in wrapped_headline:
            segments = LayoutEngine.segment_highlighted_line(line, spec.highlight_words)
            lh = LayoutEngine.draw_highlighted_line(
                draw=draw,
                x=pad_x,
                y=curr_y,
                segments=segments,
                font=headline_font,
                primary_color=(255, 255, 255, 255),
                highlight_color=(accent_rgb[0], accent_rgb[1], accent_rgb[2], 255),
                with_shadow=True
            )
            curr_y += lh + int(font_size * 0.22)

        curr_y += 16
        if spec.subheadline:
            sub_font = self._load_font(24, bold=False)
            for s_line in LayoutEngine.wrap_text(spec.subheadline, max_chars_per_line=36)[:3]:
                draw.text((pad_x, curr_y), s_line, fill=(148, 163, 184, 255), font=sub_font)
                curr_y += 34

        # Footer
        footer_y = height - 54
        draw.text((pad_x, footer_y), f"{spec.brand_name} • Intelligence", fill=(100, 116, 139, 255), font=self._load_font(18, bold=True))

        return img

    # --------------------------------------------------------------------------
    # ARCHETYPE 3: CINEMATIC OVERLAY (Full-bleed Image + Central Dark Scrim)
    # --------------------------------------------------------------------------
    def _render_cinematic_overlay(self, base_img: Image.Image, spec: DesignSpecification, width: int, height: int, accent_rgb: Tuple[int, int, int]) -> Image.Image:
        img = self._apply_directional_gradient(base_img, OverlayStrategy.directional_vignette)
        draw = ImageDraw.Draw(img)

        pad_x = int(width * 0.08)
        curr_y = int(height * 0.38)

        # Center Eyebrow
        badge_text = (spec.badge_text or "OPINI & PERSPEKTIF").upper().strip()
        draw.text((pad_x, curr_y), f"✦ {badge_text}", fill=accent_rgb, font=self._load_font(22, bold=True))
        curr_y += 42

        # Display Headline
        wrapped_headline = LayoutEngine.wrap_text(spec.headline, max_chars_per_line=18)
        headline_font, font_size = LayoutEngine.get_fitted_font(
            wrapped_headline,
            max_width=width - (pad_x * 2),
            max_height=int(height * 0.35),
            initial_size=60,
            min_size=32
        )

        for line in wrapped_headline:
            segments = LayoutEngine.segment_highlighted_line(line, spec.highlight_words)
            lh = LayoutEngine.draw_highlighted_line(
                draw=draw,
                x=pad_x,
                y=curr_y,
                segments=segments,
                font=headline_font,
                primary_color=(255, 255, 255, 255),
                highlight_color=(accent_rgb[0], accent_rgb[1], accent_rgb[2], 255),
                with_shadow=True
            )
            curr_y += lh + int(font_size * 0.24)

        if spec.subheadline:
            curr_y += 20
            sub_font = self._load_font(25, bold=False)
            for s_line in LayoutEngine.wrap_text(spec.subheadline, max_chars_per_line=34)[:3]:
                draw.text((pad_x, curr_y), s_line, fill=(203, 213, 225, 255), font=sub_font)
                curr_y += 36

        # Footer
        footer_y = height - 60
        draw.line([(pad_x, footer_y - 10), (width - pad_x, footer_y - 10)], fill=(255, 255, 255, 30), width=1)
        draw.text((pad_x, footer_y), f"⚡ {spec.brand_name.upper()}", fill=(148, 163, 184, 255), font=self._load_font(18, bold=True))

        return img

    # --------------------------------------------------------------------------
    # ARCHETYPE 4: DATA EDITORIAL (Large Prominent Number + Metric Callout)
    # --------------------------------------------------------------------------
    def _render_data_editorial(self, base_img: Image.Image, spec: DesignSpecification, width: int, height: int, accent_rgb: Tuple[int, int, int]) -> Image.Image:
        img = self._apply_directional_gradient(base_img, OverlayStrategy.cinematic_gradient_bottom)
        draw = ImageDraw.Draw(img)

        pad_x = int(width * 0.075)
        curr_y = int(height * 0.28)

        # Eyebrow
        badge_text = (spec.badge_text or "DATA & STATISTIK PROPERTI").upper().strip()
        draw.text((pad_x, curr_y), f"📊 {badge_text}", fill=accent_rgb, font=self._load_font(22, bold=True))
        curr_y += 44

        # Massive Numeric Callout (e.g. 85%, +300%, Rp 2,4 M)
        metric_val = spec.metric_value or "85%"
        metric_font = self._load_font(96, bold=True)
        draw.text((pad_x, curr_y), metric_val, fill=accent_rgb, font=metric_font)
        m_bbox = draw.textbbox((0, 0), metric_val, font=metric_font)
        curr_y += (m_bbox[3] - m_bbox[1]) + 14

        if spec.metric_label:
            draw.text((pad_x, curr_y), spec.metric_label.upper(), fill=(203, 213, 225, 255), font=self._load_font(22, bold=True))
            curr_y += 38

        # Main Headline
        wrapped_headline = LayoutEngine.wrap_text(spec.headline, max_chars_per_line=20)
        headline_font, font_size = LayoutEngine.get_fitted_font(
            wrapped_headline,
            max_width=width - (pad_x * 2),
            max_height=int(height * 0.24),
            initial_size=46,
            min_size=28
        )

        for line in wrapped_headline:
            segments = LayoutEngine.segment_highlighted_line(line, spec.highlight_words)
            lh = LayoutEngine.draw_highlighted_line(
                draw=draw,
                x=pad_x,
                y=curr_y,
                segments=segments,
                font=headline_font,
                primary_color=(255, 255, 255, 255),
                highlight_color=(accent_rgb[0], accent_rgb[1], accent_rgb[2], 255),
                with_shadow=True
            )
            curr_y += lh + 10

        # Subtitle Takeaway
        if spec.subheadline:
            curr_y += 14
            for s_line in LayoutEngine.wrap_text(spec.subheadline, max_chars_per_line=36)[:2]:
                draw.text((pad_x, curr_y), s_line, fill=(148, 163, 184, 255), font=self._load_font(22, bold=False))
                curr_y += 32

        # Footer
        draw.text((pad_x, height - 60), f"{spec.brand_name} • Market Data Desk", fill=(100, 116, 139, 255), font=self._load_font(18, bold=True))
        return img

    # --------------------------------------------------------------------------
    # ARCHETYPE 5: LIST EDITORIAL (Structured Numbered Points)
    # --------------------------------------------------------------------------
    def _render_list_editorial(self, base_img: Image.Image, spec: DesignSpecification, width: int, height: int, accent_rgb: Tuple[int, int, int]) -> Image.Image:
        img = self._apply_directional_gradient(base_img, OverlayStrategy.cinematic_gradient_bottom)
        draw = ImageDraw.Draw(img)

        pad_x = int(width * 0.075)
        curr_y = int(height * 0.22)

        badge_text = (spec.badge_text or "POIN UTAMA").upper().strip()
        draw.text((pad_x, curr_y), f"✦ {badge_text}", fill=accent_rgb, font=self._load_font(22, bold=True))
        curr_y += 38

        wrapped_headline = LayoutEngine.wrap_text(spec.headline, max_chars_per_line=20)
        headline_font, font_size = LayoutEngine.get_fitted_font(
            wrapped_headline,
            max_width=width - (pad_x * 2),
            max_height=int(height * 0.22),
            initial_size=48,
            min_size=30
        )

        for line in wrapped_headline:
            segments = LayoutEngine.segment_highlighted_line(line, spec.highlight_words)
            lh = LayoutEngine.draw_highlighted_line(
                draw=draw,
                x=pad_x,
                y=curr_y,
                segments=segments,
                font=headline_font,
                primary_color=(255, 255, 255, 255),
                highlight_color=(accent_rgb[0], accent_rgb[1], accent_rgb[2], 255),
                with_shadow=True
            )
            curr_y += lh + 10

        curr_y += 24

        # Numbered Pill Items
        pts = spec.bullet_points if spec.bullet_points else [
            "Respon prospek di atas 15 menit menurunkan closing 80%",
            "Template chat kaku tanpa personalisasi nama calon pembeli",
            "Tidak membuat janji temu survey yang spesifik"
        ]

        num_font = self._load_font(22, bold=True)
        item_font = self._load_font(23, bold=False)

        for i, pt in enumerate(pts[:4]):
            # Pill Number Badge
            pill_rect = [pad_x, curr_y, pad_x + 48, curr_y + 36]
            draw.rounded_rectangle(pill_rect, radius=10, fill=accent_rgb)
            draw.text((pad_x + 12, curr_y + 6), f"0{i+1}", fill=(7, 11, 20, 255), font=num_font)

            # Item Text
            wrapped_pt = LayoutEngine.wrap_text(pt, max_chars_per_line=30)
            pt_y = curr_y + 2
            for p_line in wrapped_pt[:2]:
                draw.text((pad_x + 64, pt_y), p_line, fill=(226, 232, 240, 255), font=item_font)
                pt_y += 30
            
            curr_y = max(pt_y + 16, curr_y + 54)

        # Footer
        draw.text((pad_x, height - 60), f"⚡ {spec.brand_name.upper()} • Editorial Playbook", fill=(100, 116, 139, 255), font=self._load_font(18, bold=True))
        return img

    # --------------------------------------------------------------------------
    # ARCHETYPE 6: MINIMAL EDITORIAL (Quote / Opinion on Dark Obsidian Canvas)
    # --------------------------------------------------------------------------
    def _render_minimal_editorial(self, base_img: Image.Image, spec: DesignSpecification, width: int, height: int, accent_rgb: Tuple[int, int, int]) -> Image.Image:
        img = Image.new("RGBA", (width, height), (7, 11, 20, 255))
        draw = ImageDraw.Draw(img)

        # Subtle ambient glow in center
        glow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        glow_draw = ImageDraw.Draw(glow)
        glow_draw.ellipse(
            [int(width * 0.2), int(height * 0.3), int(width * 0.8), int(height * 0.7)],
            fill=(accent_rgb[0], accent_rgb[1], accent_rgb[2], 25)
        )
        img = Image.alpha_composite(img, glow.filter(ImageFilter.GaussianBlur(radius=70)))
        draw = ImageDraw.Draw(img)

        pad_x = int(width * 0.08)
        curr_y = int(height * 0.28)

        # Giant quotation mark accent
        quote_font = self._load_font(110, bold=True)
        draw.text((pad_x - 10, curr_y - 40), "“", fill=(accent_rgb[0], accent_rgb[1], accent_rgb[2], 120), font=quote_font)
        curr_y += 60

        wrapped_headline = LayoutEngine.wrap_text(spec.headline, max_chars_per_line=17)
        headline_font, font_size = LayoutEngine.get_fitted_font(
            wrapped_headline,
            max_width=width - (pad_x * 2),
            max_height=int(height * 0.38),
            initial_size=56,
            min_size=32
        )

        for line in wrapped_headline:
            segments = LayoutEngine.segment_highlighted_line(line, spec.highlight_words)
            lh = LayoutEngine.draw_highlighted_line(
                draw=draw,
                x=pad_x,
                y=curr_y,
                segments=segments,
                font=headline_font,
                primary_color=(255, 255, 255, 255),
                highlight_color=(accent_rgb[0], accent_rgb[1], accent_rgb[2], 255),
                with_shadow=True
            )
            curr_y += lh + int(font_size * 0.24)

        if spec.subheadline:
            curr_y += 24
            for s_line in LayoutEngine.wrap_text(spec.subheadline, max_chars_per_line=34)[:3]:
                draw.text((pad_x, curr_y), s_line, fill=(148, 163, 184, 255), font=self._load_font(24, bold=False))
                curr_y += 36

        # Author attribution
        auth_name = spec.author_name or f"Tim Riset {spec.brand_name}"
        draw.text((pad_x, height - 100), f"— {auth_name}", fill=accent_rgb, font=self._load_font(22, bold=True))
        draw.text((pad_x, height - 64), f"{spec.brand_name} Editorial Column", fill=(100, 116, 139, 255), font=self._load_font(18, bold=False))

        return img

    # --------------------------------------------------------------------------
    # ARCHETYPE 7: PROPERTY SHOWCASE (Hero Photo + Location + Specs + Price)
    # --------------------------------------------------------------------------
    def _render_property_showcase(self, base_img: Image.Image, spec: DesignSpecification, width: int, height: int, accent_rgb: Tuple[int, int, int]) -> Image.Image:
        img = Image.new("RGBA", (width, height), (7, 11, 20, 255))

        # Hero photo top 52%
        photo_h = int(height * 0.52)
        top_photo = base_img.crop((0, 0, width, photo_h))
        img.paste(top_photo, (0, 0))

        draw = ImageDraw.Draw(img)
        # Smooth photo fade at bottom
        for y in range(photo_h - 90, photo_h):
            alpha = int(((y - (photo_h - 90)) / 90) * 255)
            draw.line([(0, y), (width, y)], fill=(7, 11, 20, alpha))

        pad_x = int(width * 0.075)

        # Location Badge on Photo
        loc_text = spec.property_location or "Jatinangor, Sumedang"
        loc_font = self._load_font(20, bold=True)
        loc_rect = [pad_x, photo_h - 64, pad_x + 280, photo_h - 18]
        draw.rounded_rectangle(loc_rect, radius=12, fill=(12, 18, 32, 220), outline=accent_rgb, width=1)
        draw.text((pad_x + 16, photo_h - 56), f"📍 {loc_text}", fill=(255, 255, 255, 255), font=loc_font)

        curr_y = photo_h + 24

        # Property Name / Headline
        wrapped_headline = LayoutEngine.wrap_text(spec.headline, max_chars_per_line=20)
        headline_font, font_size = LayoutEngine.get_fitted_font(
            wrapped_headline,
            max_width=width - (pad_x * 2),
            max_height=int(height * 0.18),
            initial_size=46,
            min_size=28
        )

        for line in wrapped_headline:
            segments = LayoutEngine.segment_highlighted_line(line, spec.highlight_words)
            lh = LayoutEngine.draw_highlighted_line(
                draw=draw,
                x=pad_x,
                y=curr_y,
                segments=segments,
                font=headline_font,
                primary_color=(255, 255, 255, 255),
                highlight_color=(accent_rgb[0], accent_rgb[1], accent_rgb[2], 255),
                with_shadow=True
            )
            curr_y += lh + 8

        curr_y += 16

        # Architectural Specs Pills Row
        features = spec.property_features if spec.property_features else ["16 Kamar Kost", "Yield 12%/thn", "SHM Siap", "Dekat UNPAD"]
        feat_font = self._load_font(20, bold=False)
        pill_x = pad_x
        for f_text in features[:3]:
            f_bbox = draw.textbbox((0, 0), f_text, font=feat_font)
            f_w = f_bbox[2] - f_bbox[0]
            draw.rounded_rectangle([pill_x, curr_y, pill_x + f_w + 24, curr_y + 36], radius=10, fill=(22, 34, 56, 200), outline=(56, 189, 248, 80))
            draw.text((pill_x + 12, curr_y + 7), f_text, fill=(203, 213, 225, 255), font=feat_font)
            pill_x += f_w + 36

        curr_y += 56

        # Price Highlight Box
        price_val = spec.property_price or "Mulai Rp 1,85 Miliar"
        draw.text((pad_x, curr_y), "HARGA UNIT:", fill=(148, 163, 184, 255), font=self._load_font(18, bold=True))
        draw.text((pad_x, curr_y + 24), price_val, fill=accent_rgb, font=self._load_font(38, bold=True))

        # Optional CTA Button for Showcase
        if spec.cta_strategy in (CTAStrategy.CTA_REQUIRED, CTAStrategy.CTA_OPTIONAL) and spec.cta_text:
            cta_font = self._load_font(20, bold=True)
            cta_btn_rect = [width - pad_x - 260, curr_y + 14, width - pad_x, curr_y + 64]
            draw.rounded_rectangle(cta_btn_rect, radius=12, fill=accent_rgb)
            draw.text((width - pad_x - 240, curr_y + 27), spec.cta_text, fill=(7, 11, 20, 255), font=cta_font)

        # Footer
        draw.text((pad_x, height - 48), f"{spec.brand_name} • Verified Property Portfolio", fill=(100, 116, 139, 255), font=self._load_font(16, bold=False))

        return img
