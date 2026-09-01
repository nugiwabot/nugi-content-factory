import io
import time
from typing import Dict, Any, Tuple, Optional, List
from PIL import Image, ImageDraw, ImageFont, ImageFilter

from app.brand.profiles import NUGI_PROPERTI_BRAND_PROFILE
from app.brand.tokens import ColorSystem
from app.templates.registry import TemplateRegistry
from app.templates.spec import TemplateSpecification
from app.schemas.design_spec import DesignSpecification
from app.rendering.layout import LayoutEngine
from app.core.errors import RenderingError
from app.core.logging import logger


class TemplateRenderer:
    """
    Data-Driven Deterministic Template Renderer.
    Renders high-conversion 1080x1350 (4:5 portrait) and 1080x1080 property marketing graphics
    strictly following Brand DNA & Template Specifications.
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

    def _create_cinematic_gradient_canvas(self, width: int, height: int, accent_hex: str) -> Image.Image:
        """Generates a rich dark luxury gradient background with subtle accent glow."""
        img = Image.new("RGBA", (width, height), (7, 11, 20, 255)) # Obsidian Navy
        draw = ImageDraw.Draw(img)

        # Subtle dark gradient overlay
        for y in range(height):
            ratio = y / height
            r = int(7 + ratio * 8)
            g = int(11 + ratio * 12)
            b = int(20 + ratio * 20)
            draw.line([(0, y), (width, y)], fill=(r, g, b, 255))

        # Radial accent ambient glow at bottom-right or top-left
        accent_rgb = self._hex_to_rgb(accent_hex, (56, 189, 248))
        glow_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        glow_draw = ImageDraw.Draw(glow_layer)
        glow_draw.ellipse(
            [int(width * 0.5), int(height * 0.6), int(width * 1.3), int(height * 1.3)],
            fill=(accent_rgb[0], accent_rgb[1], accent_rgb[2], 25)
        )
        glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(radius=80))

        return Image.alpha_composite(img, glow_layer)

    def render_spec(
        self,
        spec: DesignSpecification,
        background_bytes: Optional[bytes] = None
    ) -> Tuple[bytes, Dict[str, Any]]:
        """
        Renders a full DesignSpecification into a pixel-perfect PNG asset.
        """
        start_time = time.time()
        try:
            # 1. Fetch Template Definition
            template_id = spec.template_id
            if TemplateRegistry.exists(template_id):
                tmpl = TemplateRegistry.get(template_id)
            else:
                tmpl = TemplateRegistry.get("01_PROPERTY_PROBLEM")

            width = spec.width or tmpl.canvas.width
            height = spec.height or tmpl.canvas.height

            # Determine Accent Color
            accent_hex = spec.accent_color_hex
            if not accent_hex:
                if tmpl.accent_scheme == "rose":
                    accent_hex = self.colors.accent_rose
                elif tmpl.accent_scheme == "gold":
                    accent_hex = self.colors.accent_gold
                elif tmpl.accent_scheme == "emerald":
                    accent_hex = self.colors.accent_emerald
                elif tmpl.accent_scheme == "indigo":
                    accent_hex = self.colors.accent_secondary
                else:
                    accent_hex = self.colors.accent_primary
            
            accent_rgb = self._hex_to_rgb(accent_hex)

            # 2. Base Canvas / Background Visual
            if background_bytes and len(background_bytes) > 0:
                base_img = Image.open(io.BytesIO(background_bytes)).convert("RGBA")
                if base_img.size != (width, height):
                    base_img = base_img.resize((width, height), Image.Resampling.LANCZOS)
                
                # Apply dark scrim for contrast
                scrim = Image.new("RGBA", (width, height), (7, 11, 20, int(tmpl.background_rules.scrim_opacity * 255)))
                base_canvas = Image.alpha_composite(base_img, scrim)
            else:
                base_canvas = self._create_cinematic_gradient_canvas(width, height, accent_hex)

            # 3. Main Glassmorphic Card Container
            overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
            draw_overlay = ImageDraw.Draw(overlay)

            margin_x = int(width * 0.065) # 70px
            margin_y = int(height * 0.065) # 88px
            card_box = [margin_x, margin_y, width - margin_x, height - margin_y]

            draw_overlay.rounded_rectangle(
                card_box,
                radius=28,
                fill=(12, 18, 32, 220), # Sleek dark slate
                outline=(accent_rgb[0], accent_rgb[1], accent_rgb[2], 65),
                width=2
            )

            composite = Image.alpha_composite(base_canvas, overlay)
            draw = ImageDraw.Draw(composite)

            card_inner_x = margin_x + 40
            card_inner_w = (width - margin_x * 2) - 80
            curr_y = margin_y + 40

            # 4. Top Header Row: Category Badge Pill (Left) & Brand Watermark / Logo (Right)
            badge_text = (spec.badge_text or "PROPERTI STRATEGY").upper().strip()
            badge_font = self._load_font(22, bold=True)
            badge_bbox = draw.textbbox((0, 0), badge_text, font=badge_font)
            badge_w = badge_bbox[2] - badge_bbox[0]
            badge_h = badge_bbox[3] - badge_bbox[1]

            badge_pad_x = 16
            badge_pad_y = 8
            badge_rect = [
                card_inner_x,
                curr_y,
                card_inner_x + badge_w + (badge_pad_x * 2),
                curr_y + badge_h + (badge_pad_y * 2)
            ]
            draw.rounded_rectangle(
                badge_rect,
                radius=14,
                fill=(accent_rgb[0], accent_rgb[1], accent_rgb[2], 35),
                outline=accent_rgb,
                width=1
            )
            draw.text(
                (card_inner_x + badge_pad_x, curr_y + badge_pad_y - 2),
                badge_text,
                fill=accent_rgb,
                font=badge_font
            )

            # Logo / Brand at Top Right
            if spec.show_logo:
                brand_font = self._load_font(20, bold=True)
                logo_text = f"⚡ {spec.brand_name.upper()}"
                logo_bbox = draw.textbbox((0, 0), logo_text, font=brand_font)
                logo_w = logo_bbox[2] - logo_bbox[0]
                draw.text(
                    (card_box[2] - 40 - logo_w, curr_y + 6),
                    logo_text,
                    fill=(203, 213, 225, 230),
                    font=brand_font
                )

            curr_y = badge_rect[3] + 36

            # 5. Headline Rendering with Word Highlighting & Dynamic Auto-Fit
            headline_max_h = int(height * 0.38)
            wrapped_headline = LayoutEngine.wrap_text(spec.headline, max_chars_per_line=20)
            
            headline_font, font_size = LayoutEngine.get_fitted_font(
                wrapped_headline,
                max_width=card_inner_w,
                max_height=headline_max_h,
                initial_size=58,
                min_size=28
            )

            line_spacing = int(font_size * 0.28)
            for line in wrapped_headline:
                segments = LayoutEngine.segment_highlighted_line(line, spec.highlight_words)
                lh = LayoutEngine.draw_highlighted_line(
                    draw=draw,
                    x=card_inner_x,
                    y=curr_y,
                    segments=segments,
                    font=headline_font,
                    primary_color=(255, 255, 255, 255),
                    highlight_color=(accent_rgb[0], accent_rgb[1], accent_rgb[2], 255),
                    with_shadow=True
                )
                curr_y += lh + line_spacing

            curr_y += 12

            # 6. Template Specific Zone Elements
            # A. Subheadline / Insight description
            if spec.subheadline:
                sub_font = self._load_font(26, bold=False)
                wrapped_sub = LayoutEngine.wrap_text(spec.subheadline, max_chars_per_line=34)
                for s_line in wrapped_sub[:4]:
                    draw.text((card_inner_x, curr_y), s_line, fill=(148, 163, 184, 255), font=sub_font)
                    s_bbox = draw.textbbox((0, 0), s_line, font=sub_font)
                    curr_y += (s_bbox[3] - s_bbox[1]) + 10
                curr_y += 14

            # B. Numbered Bullet Points (Template 03)
            if spec.bullet_points and len(spec.bullet_points) > 0:
                bp_font = self._load_font(24, bold=False)
                bp_num_font = self._load_font(24, bold=True)
                for idx, pt in enumerate(spec.bullet_points[:4]):
                    num_str = f"0{idx+1}."
                    draw.text((card_inner_x, curr_y), num_str, fill=accent_rgb, font=bp_num_font)
                    draw.text((card_inner_x + 50, curr_y), pt[:44], fill=(226, 232, 240, 255), font=bp_font)
                    curr_y += 38
                curr_y += 10

            # C. Metric Card Highlight (Template 04)
            if spec.metric_value:
                metric_font = self._load_font(46, bold=True)
                metric_label_font = self._load_font(22, bold=False)
                
                # Metric highlight box
                m_box = [card_inner_x, curr_y, card_inner_x + card_inner_w, curr_y + 80]
                draw.rounded_rectangle(
                    m_box,
                    radius=16,
                    fill=(accent_rgb[0], accent_rgb[1], accent_rgb[2], 20),
                    outline=(accent_rgb[0], accent_rgb[1], accent_rgb[2], 90),
                    width=1
                )
                draw.text((card_inner_x + 20, curr_y + 16), spec.metric_value, fill=accent_rgb, font=metric_font)
                if spec.metric_label:
                    draw.text((card_inner_x + 220, curr_y + 26), spec.metric_label, fill=(203, 213, 225, 255), font=metric_label_font)
                curr_y += 100

            # 7. Bottom CTA Button & Footer
            cta_text = spec.cta_text or "Pelajari Solusinya →"
            cta_font = self._load_font(24, bold=True)
            cta_bbox = draw.textbbox((0, 0), cta_text, font=cta_font)
            cta_w = cta_bbox[2] - cta_bbox[0]
            cta_h = cta_bbox[3] - cta_bbox[1]

            cta_button_y = card_box[3] - 90
            cta_btn_rect = [
                card_inner_x,
                cta_button_y,
                card_inner_x + cta_w + 48,
                cta_button_y + cta_h + 24
            ]
            draw.rounded_rectangle(
                cta_btn_rect,
                radius=16,
                fill=accent_rgb,
                outline=(255, 255, 255, 120),
                width=1
            )
            draw.text(
                (card_inner_x + 24, cta_button_y + 12),
                cta_text,
                fill=(7, 11, 20, 255), # Dark text for high contrast on glowing button
                font=cta_font
            )

            # Bottom subtle separator line & footer note
            draw.line(
                [(card_inner_x, card_box[3] - 36), (card_box[2] - 40, card_box[3] - 36)],
                fill=(255, 255, 255, 25),
                width=1
            )
            footer_font = self._load_font(18, bold=False)
            draw.text(
                (card_inner_x, card_box[3] - 28),
                f"{spec.brand_name} • Property Growth & Marketing Intelligence",
                fill=(100, 116, 139, 230),
                font=footer_font
            )

            # 8. Encode to PNG
            output_buffer = io.BytesIO()
            final_rgb = composite.convert("RGB")
            final_rgb.save(output_buffer, format="PNG", optimize=True)
            rendered_bytes = output_buffer.getvalue()

            latency_ms = int((time.time() - start_time) * 1000)
            render_metadata = {
                "template_id": template_id,
                "width": width,
                "height": height,
                "aspect_ratio": "4:5" if height == 1350 else "1:1",
                "font_size_used": font_size,
                "lines_rendered": len(wrapped_headline),
                "highlight_words": spec.highlight_words,
                "accent_color": accent_hex,
                "render_latency_ms": max(latency_ms, 10),
                "engine": "TemplateRenderer_v2"
            }
            return rendered_bytes, render_metadata

        except Exception as e:
            logger.exception(f"Template rendering failed: {str(e)}")
            raise RenderingError(f"Failed to render template graphic: {str(e)}")
