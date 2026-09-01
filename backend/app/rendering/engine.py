import io
import time
from typing import Dict, Any, Optional, Tuple
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from app.rendering.layout import LayoutEngine
from app.core.errors import RenderingError
from app.core.logging import logger


class DeterministicRenderingEngine:
    """
    Deterministic rendering engine: converts background visual + marketing copy
    into publication-grade 1080x1080 social media graphic assets.
    """
    def __init__(self):
        self.default_width = 1080
        self.default_height = 1080
        from app.rendering.template_renderer import TemplateRenderer
        from app.rendering.editorial_renderer import EditorialRenderer
        self.template_renderer = TemplateRenderer()
        self.editorial_renderer = EditorialRenderer()

    def render_from_spec(
        self,
        spec,
        background_bytes: Optional[bytes] = None
    ) -> Tuple[bytes, Dict[str, Any]]:
        """Renders graphic from a formal DesignSpecification object."""
        if hasattr(spec, "composition_type") and spec.composition_type:
            return self.editorial_renderer.render(spec, background_bytes)
        return self.template_renderer.render_spec(spec, background_bytes)

    def hex_to_rgb(self, hex_code: str, fallback: Tuple[int, int, int] = (15, 23, 42)) -> Tuple[int, int, int]:
        try:
            h = hex_code.lstrip("#")
            if len(h) == 6:
                return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
            elif len(h) == 3:
                return tuple(int(h[i]*2, 16) for i in range(3))
        except Exception:
            pass
        return fallback

    def render(
        self,
        background_bytes: bytes,
        headline: str,
        category_badge: str = "PROPERTI STRATEGY",
        hook_text: Optional[str] = None,
        brand_name: str = "NugiProperti Studio",
        primary_color_hex: str = "#0f172a",
        accent_color_hex: str = "#38bdf8",
        width: int = 1080,
        height: int = 1080
    ) -> Tuple[bytes, Dict[str, Any]]:
        start_time = time.time()
        try:
            # 1. Load Background Image
            bg_stream = io.BytesIO(background_bytes)
            base_image = Image.open(bg_stream).convert("RGBA")
            if base_image.size != (width, height):
                base_image = base_image.resize((width, height), Image.Resampling.LANCZOS)

            # 2. Add Dark Scrim / Glassmorphism Container for High Contrast
            overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
            draw_overlay = ImageDraw.Draw(overlay)

            # Semi-transparent dark card in center
            card_margin_x = int(width * 0.08)
            card_margin_y = int(height * 0.12)
            card_box = [
                card_margin_x,
                card_margin_y,
                width - card_margin_x,
                height - card_margin_y
            ]
            
            # Draw sleek glass card
            draw_overlay.rounded_rectangle(
                card_box,
                radius=24,
                fill=(8, 14, 24, 210), # Dark slate with high opacity
                outline=(56, 189, 248, 80), # Subtle cyan border
                width=2
            )

            # Composite base with card overlay
            composite = Image.alpha_composite(base_image, overlay)
            draw = ImageDraw.Draw(composite)

            # 3. Render Category Badge Pill at Top of Card
            badge_font_size = 22
            try:
                badge_font = ImageFont.truetype("arial.ttf", badge_font_size)
            except IOError:
                badge_font = ImageFont.load_default()

            badge_text = category_badge.upper().strip()
            badge_bbox = draw.textbbox((0, 0), badge_text, font=badge_font)
            badge_w = badge_bbox[2] - badge_bbox[0]
            badge_h = badge_bbox[3] - badge_bbox[1]

            badge_pad_x = 16
            badge_pad_y = 8
            badge_x = card_margin_x + 36
            badge_y = card_margin_y + 36

            badge_rect = [
                badge_x,
                badge_y,
                badge_x + badge_w + (badge_pad_x * 2),
                badge_y + badge_h + (badge_pad_y * 2)
            ]
            accent_rgb = self.hex_to_rgb(accent_color_hex, (56, 189, 248))
            draw.rounded_rectangle(
                badge_rect,
                radius=14,
                fill=(accent_rgb[0], accent_rgb[1], accent_rgb[2], 40),
                outline=accent_rgb,
                width=1
            )
            draw.text(
                (badge_x + badge_pad_x, badge_y + badge_pad_y - 2),
                badge_text,
                fill=accent_rgb,
                font=badge_font
            )

            # 4. Render Main Headline with Dynamic Auto-Fitting
            headline_max_width = width - (card_margin_x * 2) - 72
            headline_max_height = int(height * 0.40)
            wrapped_headline = LayoutEngine.wrap_text(headline, max_chars_per_line=22)

            headline_font, font_size = LayoutEngine.get_fitted_font(
                wrapped_headline,
                max_width=headline_max_width,
                max_height=headline_max_height,
                initial_size=56,
                min_size=28
            )

            headline_y = badge_rect[3] + 28
            curr_y = headline_y
            line_spacing = int(font_size * 0.28)

            for line in wrapped_headline:
                # Text Shadow for maximum readability
                draw.text(
                    (card_margin_x + 36 + 2, curr_y + 2),
                    line,
                    fill=(0, 0, 0, 180),
                    font=headline_font
                )
                # Crisp White Text
                draw.text(
                    (card_margin_x + 36, curr_y),
                    line,
                    fill=(255, 255, 255, 255),
                    font=headline_font
                )
                bbox = draw.textbbox((0, 0), line, font=headline_font)
                curr_y += (bbox[3] - bbox[1]) + line_spacing

            # 5. Render Hook Text / Subtitle if provided
            if hook_text:
                try:
                    hook_font = ImageFont.truetype("arial.ttf", 26)
                except IOError:
                    hook_font = ImageFont.load_default()

                wrapped_hook = LayoutEngine.wrap_text(hook_text, max_chars_per_line=36)
                curr_y += 16
                for h_line in wrapped_hook[:3]: # Max 3 lines
                    draw.text(
                        (card_margin_x + 36, curr_y),
                        h_line,
                        fill=(148, 163, 184, 255), # Slate text
                        font=hook_font
                    )
                    h_bbox = draw.textbbox((0, 0), h_line, font=hook_font)
                    curr_y += (h_bbox[3] - h_bbox[1]) + 8

            # 6. Render Brand Name & Watermark at Bottom of Card
            try:
                brand_font = ImageFont.truetype("arial.ttf", 20)
            except IOError:
                brand_font = ImageFont.load_default()

            brand_y = card_box[3] - 44
            draw.line(
                [(card_margin_x + 36, brand_y - 12), (card_box[2] - 36, brand_y - 12)],
                fill=(255, 255, 255, 30),
                width=1
            )
            draw.text(
                (card_margin_x + 36, brand_y),
                f"⚡ {brand_name.upper()}",
                fill=(148, 163, 184, 230),
                font=brand_font
            )

            # Export final image
            output_buffer = io.BytesIO()
            final_rgb = composite.convert("RGB")
            final_rgb.save(output_buffer, format="PNG", optimize=True)
            rendered_bytes = output_buffer.getvalue()

            latency_ms = int((time.time() - start_time) * 1000)
            render_metadata = {
                "width": width,
                "height": height,
                "font_size_used": font_size,
                "lines_rendered": len(wrapped_headline),
                "badge": badge_text,
                "render_latency_ms": max(latency_ms, 10),
                "engine": "DeterministicPillowEngine"
            }
            return rendered_bytes, render_metadata

        except Exception as e:
            logger.exception(f"Rendering engine failed: {str(e)}")
            raise RenderingError(f"Failed to render deterministic graphic: {str(e)}")
