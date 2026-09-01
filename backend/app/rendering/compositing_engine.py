import io
import time
import math
from typing import Dict, Any, Tuple, Optional, List
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageChops

from app.brand.profiles import NUGI_PROPERTI_BRAND_PROFILE
from app.brand.tokens import ColorSystem
from app.schemas.compositing import (
    CompositionPlan,
    LayerSpecification,
    LayerType,
    BlendMode,
    ColorGradeSpecification,
    VisualConceptSpecification
)
from app.schemas.editorial_agent import ContentType
from app.schemas.design_spec import DesignSpecification, CompositionType, CTAStrategy
from app.rendering.layout import LayoutEngine
from app.core.logging import logger
from app.core.errors import RenderingError


class ProfessionalCompositingEngine:
    """
    13-Layer Professional AI Visual Compositing Engine for Nugi Content Factory (Phase 3D-1).
    Executes layered alpha compositing, lighting matching, contact/drop shadows,
    atmospheric depth, content-type-specific editorial layouts, and deterministic typography.
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

    # --------------------------------------------------------------------------
    # BLEND MODES ENGINE
    # --------------------------------------------------------------------------
    def apply_blend_mode(
        self,
        base_img: Image.Image,
        overlay_img: Image.Image,
        mode: BlendMode,
        opacity: float = 1.0
    ) -> Image.Image:
        """Applies advanced blend modes between two RGBA images."""
        if opacity < 1.0:
            r, g, b, a = overlay_img.split()
            a = a.point(lambda p: int(p * opacity))
            overlay_img = Image.merge("RGBA", (r, g, b, a))

        if mode == BlendMode.NORMAL:
            return Image.alpha_composite(base_img, overlay_img)

        base_rgb = base_img.convert("RGB")
        over_rgb = overlay_img.convert("RGB")
        over_alpha = overlay_img.split()[3]

        if mode == BlendMode.MULTIPLY:
            blended_rgb = ImageChops.multiply(base_rgb, over_rgb)
        elif mode == BlendMode.SCREEN:
            blended_rgb = ImageChops.screen(base_rgb, over_rgb)
        elif mode == BlendMode.ADD:
            blended_rgb = ImageChops.add(base_rgb, over_rgb)
        elif mode == BlendMode.OVERLAY:
            blended_rgb = ImageChops.overlay(base_rgb, over_rgb)
        elif mode == BlendMode.SOFT_LIGHT:
            blended_rgb = ImageChops.soft_light(base_rgb, over_rgb)
        else:
            return Image.alpha_composite(base_img, overlay_img)

        blended_rgba = blended_rgb.convert("RGBA")
        blended_rgba.putalpha(over_alpha)
        return Image.alpha_composite(base_img, blended_rgba)

    # --------------------------------------------------------------------------
    # COLOR GRADING & CINEMATIC TONE MAPPING
    # --------------------------------------------------------------------------
    def apply_color_grading(
        self,
        img: Image.Image,
        grade: ColorGradeSpecification
    ) -> Image.Image:
        """Applies cinematic color grading, contrast, temperature bias, and corner vignette."""
        width, height = img.size
        working = img.convert("RGBA")

        # 1. Exposure Adjustment
        if grade.exposure != 0.0:
            exp_factor = 1.0 + grade.exposure
            enhancer = ImageEnhance.Brightness(working)
            working = enhancer.enhance(max(0.2, exp_factor)).convert("RGBA")

        # 2. Contrast Multiplier
        if grade.contrast != 1.0:
            enhancer = ImageEnhance.Contrast(working)
            working = enhancer.enhance(grade.contrast).convert("RGBA")

        # 3. Saturation Multiplier
        if grade.saturation != 1.0:
            enhancer = ImageEnhance.Color(working)
            working = enhancer.enhance(grade.saturation).convert("RGBA")

        # 4. Temperature & Tone Shift (Warm Amber vs Cool Twilight Tint)
        if grade.temperature != 0.0 or grade.tint != 0.0:
            temp_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
            draw_t = ImageDraw.Draw(temp_layer)
            if grade.temperature > 0:
                # Warm champagne gold tint
                r_val, g_val, b_val = int(245 * grade.temperature), int(158 * grade.temperature), int(11 * grade.temperature)
                draw_t.rectangle([0, 0, width, height], fill=(r_val, g_val, b_val, int(35 * abs(grade.temperature))))
            else:
                # Cool obsidian twilight tint
                cool_mag = abs(grade.temperature)
                draw_t.rectangle([0, 0, width, height], fill=(15, 30, 60, int(45 * cool_mag)))
            
            working = Image.alpha_composite(working, temp_layer)

        # 5. Vignette Falloff
        if grade.vignette_strength > 0:
            vignette_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
            draw_v = ImageDraw.Draw(vignette_layer)
            
            cx, cy = width / 2.0, height / 2.0
            steps = 40
            for i in range(steps):
                ratio = i / float(steps)
                alpha = int((ratio ** 2.2) * 220 * grade.vignette_strength)
                inset_x = int(cx * (1.0 - ratio))
                inset_y = int(cy * (1.0 - ratio))
                draw_v.rectangle([inset_x, inset_y, width - inset_x, height - inset_y], outline=(4, 7, 14, alpha), width=width // steps + 2)

            vignette_layer = vignette_layer.filter(ImageFilter.GaussianBlur(radius=35))
            working = Image.alpha_composite(working, vignette_layer)

        return working

    # --------------------------------------------------------------------------
    # REALISTIC LIGHTING MATCH & SHADOWS
    # --------------------------------------------------------------------------
    def apply_lighting_and_shadows(
        self,
        canvas: Image.Image,
        subject_box: Tuple[int, int, int, int],
        accent_rgb: Tuple[int, int, int]
    ) -> Image.Image:
        """Simulates directional lighting match, rim lighting on subject, and soft contact shadow."""
        width, height = canvas.size
        x1, y1, x2, y2 = subject_box

        # 1. Soft Ground Contact Shadow (Occlusion at subject base)
        shadow_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw_s = ImageDraw.Draw(shadow_layer)
        contact_y = y2 - 10
        contact_rx = (x2 - x1) // 2 + 30
        contact_ry = 28
        draw_s.ellipse(
            [((x1 + x2)//2) - contact_rx, contact_y - contact_ry, ((x1 + x2)//2) + contact_rx, contact_y + contact_ry],
            fill=(4, 7, 14, 185)
        )
        shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(radius=18))
        canvas = Image.alpha_composite(canvas, shadow_layer)

        # 2. Directional Ambient Lighting Glow (Warm golden/cyan highlight)
        glow_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw_g = ImageDraw.Draw(glow_layer)
        glow_cx = x2 + 40
        glow_cy = y1 + 60
        glow_r = int((x2 - x1) * 0.75)
        draw_g.ellipse(
            [glow_cx - glow_r, glow_cy - glow_r, glow_cx + glow_r, glow_cy + glow_r],
            fill=(accent_rgb[0], accent_rgb[1], accent_rgb[2], 55)
        )
        glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(radius=50))
        canvas = Image.alpha_composite(canvas, glow_layer)

        return canvas

    # --------------------------------------------------------------------------
    # MASTER 13-LAYER COMPOSITING EXECUTION
    # --------------------------------------------------------------------------
    def composite_full_artwork(
        self,
        concept: Optional[VisualConceptSpecification],
        design_spec: DesignSpecification,
        plan: Optional[CompositionPlan] = None,
        background_bytes: Optional[bytes] = None,
        subject_bytes: Optional[bytes] = None
    ) -> Tuple[bytes, Dict[str, Any]]:
        """
        Executes the 13-layer compositing stack adhering to NugiProperti Editorial Design DNA:
        L0: Canvas -> L1: Background -> L2: Atmosphere -> L3: Architecture ->
        L4: Subject -> L5: Supporting -> L6: Dynamic Scrim -> L7: Lighting ->
        L8: Shadows -> L9: Depth/Color Grade -> L10: Graphics -> L11: Typography -> L12: Brand Signature.
        """
        start_time = time.time()
        try:
            width = design_spec.width or 1080
            height = design_spec.height or 1350
            accent_hex = design_spec.accent_color_hex or self.colors.accent_primary
            accent_rgb = self._hex_to_rgb(accent_hex)

            # LAYER 0: Canvas Base (Obsidian Navy #070B14)
            canvas = Image.new("RGBA", (width, height), (7, 11, 20, 255))

            # LAYER 1: Background Asset (Photographic 8k Asset)
            if background_bytes and len(background_bytes) > 0:
                bg_img = Image.open(io.BytesIO(background_bytes)).convert("RGBA")
                if bg_img.size != (width, height):
                    bg_img = bg_img.resize((width, height), Image.Resampling.LANCZOS)
                canvas = Image.alpha_composite(canvas, bg_img)
            else:
                from app.providers.mock_image import MockImageProvider
                mock_gen = MockImageProvider()
                mock_story = concept.visual_story if concept else design_spec.headline
                mock_out = mock_gen.generate_background(mock_story, width, height)
                bg_img = Image.open(io.BytesIO(mock_out.image_bytes)).convert("RGBA")
                canvas = Image.alpha_composite(canvas, bg_img)

            # LAYER 2: Atmosphere & Twilight Haze
            atmo_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
            draw_atmo = ImageDraw.Draw(atmo_layer)
            for y in range(int(height * 0.18), int(height * 0.65)):
                alpha = int(((y - height * 0.18) / (height * 0.47)) * 45)
                draw_atmo.line([(0, y), (width, y)], fill=(15, 23, 42, alpha))
            canvas = Image.alpha_composite(canvas, atmo_layer)

            # LAYER 3 & 4 & 5: Architectural Scene & Main Subject Isolation
            subject_box = (int(width * 0.45), int(height * 0.10), int(width * 0.95), int(height * 0.72))
            if subject_bytes and len(subject_bytes) > 0:
                subj_img = Image.open(io.BytesIO(subject_bytes)).convert("RGBA")
                canvas.paste(subj_img, (subject_box[0], subject_box[1]), subj_img)
            
            # LAYER 7 & 8: Lighting Match & Contact Shadows
            canvas = self.apply_lighting_and_shadows(canvas, subject_box, accent_rgb)

            # LAYER 6: Dynamic Asymmetric Scrim Gradient (60:40 Editorial Ratio)
            scrim_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
            draw_scrim = ImageDraw.Draw(scrim_layer)
            scrim_start_y = int(height * 0.38) # Darkens bottom 62% for headline legibility
            for y in range(scrim_start_y, height):
                progress = (y - scrim_start_y) / (height - scrim_start_y)
                alpha = int((progress ** 1.35) * 252)
                draw_scrim.line([(0, y), (width, y)], fill=(7, 11, 20, min(alpha, 254)))
            canvas = Image.alpha_composite(canvas, scrim_layer)

            # LAYER 9: Depth & Color Grading Tone Mapping
            grade = plan.color_grade if plan else ColorGradeSpecification(
                preset_name=concept.color_mood[:20] if concept else "CINEMATIC_TWILIGHT"
            )
            canvas = self.apply_color_grading(canvas, grade)

            # LAYER 10: Editorial Graphic Design Accents
            draw = ImageDraw.Draw(canvas)
            pad_x = int(width * 0.075) # 80px safe margin
            curr_y = int(height * 0.44)

            # Check content archetype specifics
            is_opinion = "OPINION" in str(design_spec.badge_text).upper() or (concept and concept.content_type in (ContentType.PROPERTY_OPINION, ContentType.OPINION))
            
            # Category Eyebrow Badge
            badge_text = (design_spec.badge_text or "EDUKASI PROPERTI").upper().strip()
            badge_font = self._load_font(22, bold=True)
            draw.text((pad_x, curr_y), f"✦ {badge_text}", fill=accent_rgb, font=badge_font)
            
            # Subtle precision hairline next to badge
            b_bbox = draw.textbbox((0, 0), f"✦ {badge_text}", font=badge_font)
            badge_w = b_bbox[2] - b_bbox[0]
            draw.line([(pad_x + badge_w + 18, curr_y + 12), (pad_x + badge_w + 120, curr_y + 12)], fill=(accent_rgb[0], accent_rgb[1], accent_rgb[2], 140), width=2)
            curr_y += 44

            # Giant editorial quotation mark for Opinion pieces
            if is_opinion:
                quote_font = self._load_font(72, bold=True)
                draw.text((pad_x, curr_y - 20), "“", fill=(accent_rgb[0], accent_rgb[1], accent_rgb[2], 120), font=quote_font)
                curr_y += 36

            # LAYER 11: Deterministic Typography (Headline + Word Highlights)
            max_headline_w = width - (pad_x * 2)
            wrapped_headline = LayoutEngine.wrap_text(design_spec.headline, max_chars_per_line=19)
            headline_font, font_size = LayoutEngine.get_fitted_font(
                wrapped_headline,
                max_width=max_headline_w,
                max_height=int(height * 0.28),
                initial_size=54,
                min_size=32
            )

            for line in wrapped_headline:
                segments = LayoutEngine.segment_highlighted_line(line, design_spec.highlight_words)
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
                curr_y += lh + int(font_size * 0.20)

            curr_y += 16

            # Supporting Subheadline
            if design_spec.subheadline:
                sub_font = self._load_font(24, bold=False)
                wrapped_sub = LayoutEngine.wrap_text(design_spec.subheadline, max_chars_per_line=36)
                for s_line in wrapped_sub[:3]:
                    draw.text((pad_x, curr_y), s_line, fill=(203, 213, 225, 255), font=sub_font)
                    s_bbox = draw.textbbox((0, 0), s_line, font=sub_font)
                    curr_y += (s_bbox[3] - s_bbox[1]) + 8

            # Empirical Metric Pill Callout (Case Study & Data Editorial)
            if design_spec.metric_value:
                curr_y += 12
                m_font = self._load_font(22, bold=True)
                m_label = design_spec.metric_label or "Pertumbuhan Efisiensi"
                m_text = f"✦ {design_spec.metric_value}  |  {m_label}"
                m_bbox = draw.textbbox((0, 0), m_text, font=m_font)
                m_w = m_bbox[2] - m_bbox[0] + 32
                m_h = 38
                draw.rounded_rectangle([pad_x, curr_y, pad_x + m_w, curr_y + m_h], radius=8, fill=(16, 185, 129, 35), outline=(16, 185, 129, 140), width=1)
                draw.text((pad_x + 16, curr_y + 8), m_text, fill=(16, 185, 129, 255), font=m_font)
                curr_y += m_h + 12

            # Numbered Index Listicle Items (01, 02, 03)
            elif design_spec.bullet_points and len(design_spec.bullet_points) > 0:
                curr_y += 10
                pt_font = self._load_font(21, bold=False)
                idx_font = self._load_font(20, bold=True)
                for i, pt in enumerate(design_spec.bullet_points[:3]):
                    num_str = f"0{i+1}"
                    draw.text((pad_x, curr_y), num_str, fill=accent_rgb, font=idx_font)
                    draw.text((pad_x + 36, curr_y), pt, fill=(226, 232, 240, 255), font=pt_font)
                    curr_y += 32

            # Property Showcase Location & Price Badge
            elif design_spec.property_location or design_spec.property_price:
                curr_y += 10
                spec_font = self._load_font(21, bold=True)
                loc_text = f"📍 {design_spec.property_location or 'Bandung'}"
                price_text = f"🏷️ {design_spec.property_price or 'Yield 12%'}"
                draw.text((pad_x, curr_y), loc_text, fill=(203, 213, 225, 255), font=spec_font)
                draw.text((pad_x + 280, curr_y), price_text, fill=accent_rgb, font=spec_font)
                curr_y += 34

            # CTA Button ONLY if CTA_REQUIRED or CTA_OPTIONAL with valid text
            if design_spec.cta_strategy in (CTAStrategy.CTA_REQUIRED, CTAStrategy.CTA_OPTIONAL) and design_spec.cta_text:
                cta_font = self._load_font(20, bold=True)
                cta_y = height - 135
                cta_rect = [pad_x, cta_y, pad_x + 310, cta_y + 50]
                draw.rounded_rectangle(cta_rect, radius=12, fill=accent_rgb)
                draw.text((pad_x + 22, cta_y + 13), design_spec.cta_text, fill=(7, 11, 20, 255), font=cta_font)

            # LAYER 12: Brand Identity & Signature Watermark Footer
            footer_y = height - 60
            draw.line([(pad_x, footer_y - 12), (width - pad_x, footer_y - 12)], fill=(255, 255, 255, 30), width=1)
            footer_font = self._load_font(18, bold=True)
            draw.text((pad_x, footer_y), f"⚡ {design_spec.brand_name.upper()}", fill=(148, 163, 184, 255), font=footer_font)
            draw.text((width - pad_x - 170, footer_y), "Editorial Art Direction", fill=(100, 116, 139, 255), font=footer_font)

            # Export to PNG bytes
            buffer = io.BytesIO()
            final_rgb = canvas.convert("RGB")
            final_rgb.save(buffer, format="PNG", optimize=True)
            rendered_bytes = buffer.getvalue()

            latency_ms = int((time.time() - start_time) * 1000)
            render_metadata = {
                "engine": "ProfessionalCompositingEngine_v3D",
                "layers_count": 13,
                "color_grade_preset": grade.preset_name,
                "width": width,
                "height": height,
                "aspect_ratio": "4:5" if height == 1350 else "1:1",
                "cta_strategy": design_spec.cta_strategy.value,
                "accent_color": accent_hex,
                "render_latency_ms": max(latency_ms, 25)
            }
            return rendered_bytes, render_metadata

        except Exception as e:
            logger.exception(f"Professional compositing failed: {str(e)}")
            raise RenderingError(f"Failed to execute layered compositing: {str(e)}")
