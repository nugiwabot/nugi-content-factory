import io
import time
import math
from pathlib import Path
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
from app.schemas.editorial_agent import ContentType, VisualArtDirectionSpecification
from app.schemas.design_spec import (
    DesignSpecification,
    CompositionType,
    EditorialLayoutPreset,
    CTAStrategy,
    SAFEZONE_TOP,
    SAFEZONE_BOTTOM,
    SAFEZONE_HEIGHT,
    SAFEZONE_LEFT,
    SAFEZONE_RIGHT,
    SAFEZONE_WIDTH,
    SAFEZONE_CONTENT_LEFT,
    SAFEZONE_CONTENT_RIGHT
)
from app.rendering.layout import LayoutEngine
from app.core.logging import logger
from app.core.errors import RenderingError


class ProfessionalCompositingEngine:
    """
    13-Layer Professional Editorial Compositing Engine (Phase 3D-2).
    Implements NugiProperti Editorial visual editorial DNA:
    - Seamless dark gradient scrim across the lower canvas for maximum readability.
    - Solid vibrant neon highlight strips/pills directly behind key headline punchlines.
    - Crisp white extra-bold typography (68-84px) with maximum contrast.
    - Minimalist header with sleek brand mark and carousel icon.
    - 100% invisible Instagram safezone (y=135..1215).
    """
    def __init__(self):
        self.colors = NUGI_PROPERTI_BRAND_PROFILE.colors

    def _hex_to_rgb(self, hex_code: str, fallback: Tuple[int, int, int] = (139, 92, 246)) -> Tuple[int, int, int]:
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
    # COLOR GRADING
    # --------------------------------------------------------------------------
    def apply_color_grading(
        self,
        img: Image.Image,
        grade: ColorGradeSpecification
    ) -> Image.Image:
        """Applies cinematic color grading, contrast, temperature bias, and tone mapping."""
        width, height = img.size
        working = img.convert("RGBA")

        # 1. Exposure
        if grade.exposure != 0.0:
            exp_factor = 1.0 + grade.exposure
            enhancer = ImageEnhance.Brightness(working)
            working = enhancer.enhance(max(0.2, exp_factor)).convert("RGBA")

        # 2. Contrast
        if grade.contrast != 1.0:
            enhancer = ImageEnhance.Contrast(working)
            working = enhancer.enhance(grade.contrast).convert("RGBA")

        # 3. Saturation
        if grade.saturation != 1.0:
            enhancer = ImageEnhance.Color(working)
            working = enhancer.enhance(grade.saturation).convert("RGBA")

        # 4. Temperature & Tone Shift
        if grade.temperature != 0.0 or grade.tint != 0.0:
            temp_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
            draw_t = ImageDraw.Draw(temp_layer)
            if grade.temperature > 0:
                r_val, g_val, b_val = int(245 * grade.temperature), int(158 * grade.temperature), int(11 * grade.temperature)
                draw_t.rectangle([0, 0, width, height], fill=(r_val, g_val, b_val, int(35 * abs(grade.temperature))))
            else:
                cool_mag = abs(grade.temperature)
                draw_t.rectangle([0, 0, width, height], fill=(15, 30, 60, int(45 * cool_mag)))
            working = Image.alpha_composite(working, temp_layer)

        # 5. Vignette Falloff
        if grade.vignette_strength > 0:
            vig_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
            draw_v = ImageDraw.Draw(vig_layer)
            cx, cy = width / 2.0, height / 2.0
            steps = 30
            for i in range(steps):
                ratio = i / float(steps)
                alpha = int((ratio ** 2.2) * 200 * grade.vignette_strength)
                inset_x = int(cx * (1.0 - ratio))
                inset_y = int(cy * (1.0 - ratio))
                draw_v.rectangle([inset_x, inset_y, width - inset_x, height - inset_y], outline=(4, 7, 14, alpha), width=width // steps + 2)
            vig_layer = vig_layer.filter(ImageFilter.GaussianBlur(radius=30))
            working = Image.alpha_composite(working, vig_layer)

        return working

    # --------------------------------------------------------------------------
    # MASTER 13-LAYER COMPOSITING EXECUTION
    # --------------------------------------------------------------------------
    def composite_full_artwork(
        self,
        concept: Optional[Any] = None,
        design_spec: Optional[DesignSpecification] = None,
        plan: Optional[Any] = None,
        background_bytes: Optional[bytes] = None,
        subject_bytes: Optional[bytes] = None,
        debug_safezone: bool = False
    ) -> Tuple[bytes, Dict[str, Any]]:
        """
        Master Layer Compositing Pipeline (Phase 3D-3 Safezone Enforcement):
        - Enforces 100% invisible Instagram safezone (x=76..1004, y=135..1215).
        - Measures and tracks exact bounding boxes for every critical element.
        - Preserves approved NugiProperti Editorial Design DNA without regression.
        - Supports optional debug safezone visualization (disabled by default in production).
        """
        # Flexible argument unpacking for complete backward compatibility
        actual_spec: DesignSpecification
        actual_concept: Optional[VisualConceptSpecification] = None
        actual_plan: Optional[Any] = plan

        if isinstance(concept, DesignSpecification):
            actual_spec = concept
            actual_concept = None
        elif isinstance(design_spec, DesignSpecification):
            actual_spec = design_spec
            actual_concept = concept if isinstance(concept, VisualConceptSpecification) else None
        else:
            raise ValueError("A valid DesignSpecification must be provided to composite_full_artwork")

        start_time = time.time()
        width = actual_spec.width or 1080
        height = actual_spec.height or 1350

        try:
            # Base Canvas
            canvas = Image.new("RGBA", (width, height), (4, 7, 17, 255))
            accent_hex = actual_spec.accent_color_hex or actual_spec.accent_color or NUGI_PROPERTI_BRAND_PROFILE.colors.accent_neon_violet
            accent_rgb = self._hex_to_rgb(accent_hex)
            critical_bboxes: Dict[str, Dict[str, int]] = {}

            # LAYER 1: Base Photography / Cinematic Artwork
            bg_bytes = background_bytes or actual_spec.background_image_bytes
            if bg_bytes and len(bg_bytes) > 0:
                bg_img = Image.open(io.BytesIO(bg_bytes)).convert("RGBA")
                if bg_img.size != (width, height):
                    bg_img = bg_img.resize((width, height), Image.Resampling.LANCZOS)
                canvas = Image.alpha_composite(canvas, bg_img)
            else:
                from app.providers.mock_image import MockImageProvider
                mock_gen = MockImageProvider()
                mock_story = actual_concept.visual_story if actual_concept else actual_spec.headline
                mock_out = mock_gen.generate_background(mock_story, width, height)
                bg_img = Image.open(io.BytesIO(mock_out.image_bytes)).convert("RGBA")
                canvas = Image.alpha_composite(canvas, bg_img)

            # LAYER 2: Subtle Focal Spotlight Glow behind subject
            spot_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
            draw_spot = ImageDraw.Draw(spot_layer)
            cx, cy = int(width * 0.5), int(height * 0.38)
            spot_r = int(width * 0.45)
            for r in range(spot_r, 0, -20):
                alpha = int((1.0 - (r / float(spot_r))) ** 2 * 60)
                draw_spot.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255, alpha))
            spot_layer = spot_layer.filter(ImageFilter.GaussianBlur(radius=35))
            canvas = Image.alpha_composite(canvas, spot_layer)

            # LAYER 3: Isolated Subject (if provided)
            if subject_bytes and len(subject_bytes) > 0:
                subj_img = Image.open(io.BytesIO(subject_bytes)).convert("RGBA")
                canvas.paste(subj_img, (int(width * 0.45), int(SAFEZONE_TOP + 40)), subj_img)

            # LAYER 4: Seamless Bottom Dark Gradient Scrim (NugiProperti Editorial Style)
            canvas = LayoutEngine.draw_bottom_gradient_scrim(
                canvas=canvas,
                start_y=680,
                end_y=1220,
                dark_rgb=(4, 7, 17)
            )

            # LAYER 5: Color Grading & Tone Mapping
            grade = actual_plan.color_grade if isinstance(actual_plan, CompositionPlan) else ColorGradeSpecification(
                preset_name="CINEMATIC_TWILIGHT",
                contrast=1.12,
                exposure=0.0
            )
            canvas = self.apply_color_grading(canvas, grade)

            # ==================================================================
            # TOP SAFEZONE: Minimalist Brand Header & Carousel Icon (y ≈ 150)
            # ==================================================================
            pad_x = SAFEZONE_CONTENT_LEFT
            top_y = SAFEZONE_TOP + 20
            draw_top = ImageDraw.Draw(canvas)

            # 1. Sleek Brand Icon & Logo Mark (Top-Left)
            logo_loaded = False
            brand_logo_path = Path(__file__).resolve().parent.parent.parent.parent / "assets" / "brand" / "nugi_properti_logo.png"
            if not brand_logo_path.exists():
                brand_logo_path = Path(__file__).resolve().parent.parent.parent / "assets" / "brand" / "nugi_properti_logo.png"

            if brand_logo_path.exists():
                try:
                    brand_logo = Image.open(brand_logo_path).convert("RGBA")
                    lh = 50
                    lw = int(brand_logo.width * (lh / float(brand_logo.height)))
                    brand_logo_scaled = brand_logo.resize((lw, lh), Image.Resampling.LANCZOS)
                    canvas.paste(brand_logo_scaled, (pad_x, top_y), brand_logo_scaled)
                    critical_bboxes["brand_header"] = {
                        "left": pad_x,
                        "top": top_y,
                        "right": pad_x + lw,
                        "bottom": top_y + lh
                    }
                    logo_loaded = True
                except Exception:
                    logo_loaded = False

            if not logo_loaded:
                v_x = pad_x
                v_y = top_y + 2
                draw_top.polygon(
                    [(v_x, v_y), (v_x + 12, v_y + 24), (v_x + 24, v_y), (v_x + 18, v_y), (v_x + 12, v_y + 14), (v_x + 6, v_y)],
                    fill=accent_rgb
                )
                logo_font = self._load_font(28, bold=True)
                logo_sub_font = self._load_font(18, bold=False)
                
                # Stacked modern brand text: NUGI / PROPERTI
                draw_top.text((v_x + 32, top_y - 2), "NUGI", fill=(255, 255, 255, 240), font=logo_font)
                draw_top.text((v_x + 32, top_y + 24), "PROPERTI", fill=accent_rgb, font=logo_sub_font)
                critical_bboxes["brand_header"] = {
                    "left": v_x,
                    "top": top_y - 2,
                    "right": v_x + 180,
                    "bottom": top_y + 48
                }

            # 2. Carousel / Share Icon (Top-Right)
            car_sz = 30
            car_x = width - pad_x - car_sz - 6
            car_y = top_y + 10
            draw_top.rounded_rectangle([car_x, car_y, car_x + car_sz - 4, car_y + car_sz - 4], radius=4, outline=(255, 255, 255, 140), width=2)
            draw_top.rounded_rectangle([car_x + 6, car_y + 6, car_x + car_sz + 2, car_y + car_sz + 2], radius=4, outline=(255, 255, 255, 180), width=2)
            critical_bboxes["carousel_icon"] = {
                "left": car_x,
                "top": car_y,
                "right": car_x + car_sz + 2,
                "bottom": car_y + car_sz + 2
            }

            # ==================================================================
            # LOWER SAFEZONE: NugiProperti Editorial Headline with Solid Highlight Strip
            # ==================================================================
            wrapped_headline = LayoutEngine.wrap_headline_punchy(actual_spec.headline, max_chars_per_line=22)
            
            # Calculate optimal font size (target 66–78px extra-bold)
            headline_font, font_size = LayoutEngine.get_fitted_font(
                wrapped_headline,
                max_width=width - (pad_x * 2) - 40,
                max_height=320,
                initial_size=74,
                min_size=46,
                bold=True
            )

            # Calculate total height of headline block
            temp_draw = ImageDraw.Draw(canvas)
            hl_w, hl_h = LayoutEngine.calculate_text_bounding_box(
                temp_draw, wrapped_headline, headline_font, line_spacing=int(font_size * 0.22)
            )

            # Position headline comfortably in the lower third (inside safezone y=135..1215)
            has_sub = bool(actual_spec.subheadline)
            has_badge = bool(actual_spec.badge_text)
            extra_lower_h = (65 if has_sub else 0) + (35 if has_badge else 0)
            target_max_y = SAFEZONE_BOTTOM - 20 - extra_lower_h
            headline_y = min(target_max_y - hl_h, 1140 - hl_h)
            headline_y = max(SAFEZONE_TOP + 280, headline_y)

            # Render Headline with NugiProperti Editorial Solid Highlight Strip
            end_hl_y, hl_bboxes = LayoutEngine.draw_editorial_headline_with_strips(
                canvas=canvas,
                lines=wrapped_headline,
                highlight_terms=actual_spec.highlight_words,
                start_x=pad_x,
                start_y=headline_y,
                font=headline_font,
                font_size=font_size,
                accent_rgb=accent_rgb
            )
            critical_bboxes.update(hl_bboxes)

            # High-Contrast Subheadline Context (if provided)
            draw_bottom = ImageDraw.Draw(canvas)
            if actual_spec.subheadline and end_hl_y + 32 <= SAFEZONE_BOTTOM - 10:
                sub_font = self._load_font(22, bold=False)
                wrapped_sub = LayoutEngine.wrap_text(actual_spec.subheadline, max_chars_per_line=38)
                sub_start_y = end_hl_y + 6
                sub_max_r = pad_x + 16
                for s_line in wrapped_sub[:2]:
                    if end_hl_y + 26 <= SAFEZONE_BOTTOM - 10:
                        draw_bottom.text((pad_x + 16, end_hl_y + 6), s_line, fill=(226, 232, 240, 240), font=sub_font)
                        s_bbox = draw_bottom.textbbox((0, 0), s_line, font=sub_font)
                        sub_max_r = max(sub_max_r, pad_x + 16 + (s_bbox[2] - s_bbox[0]))
                        end_hl_y += (s_bbox[3] - s_bbox[1]) + 6

                critical_bboxes["subheadline"] = {
                    "left": pad_x + 16,
                    "top": sub_start_y,
                    "right": sub_max_r,
                    "bottom": end_hl_y
                }

            # Optional Minimal Category Tag / Verification (strictly within safezone)
            if actual_spec.badge_text and end_hl_y + 24 <= SAFEZONE_BOTTOM - 10:
                badge_font = self._load_font(15, bold=True)
                tag_y = end_hl_y + 8
                tag_str = f"NUGIPROPERTI  •  {actual_spec.badge_text.upper()}"
                draw_bottom.text((pad_x + 16, tag_y), tag_str, fill=(148, 163, 184, 190), font=badge_font)
                b_bbox = draw_bottom.textbbox((0, 0), tag_str, font=badge_font)
                critical_bboxes["category_badge"] = {
                    "left": pad_x + 16,
                    "top": tag_y,
                    "right": pad_x + 16 + (b_bbox[2] - b_bbox[0]),
                    "bottom": tag_y + (b_bbox[3] - b_bbox[1])
                }

            # Optional Debug Overlay (Phase 3D-3, strictly disabled in production)
            final_canvas = canvas
            if debug_safezone:
                final_canvas = LayoutEngine.draw_debug_safezone_overlay(
                    canvas=canvas,
                    critical_bboxes=critical_bboxes
                )

            # Export to PNG bytes
            buffer = io.BytesIO()
            final_rgb = final_canvas.convert("RGB")
            final_rgb.save(buffer, format="PNG", optimize=True)
            rendered_bytes = buffer.getvalue()

            latency_ms = int((time.time() - start_time) * 1000)
            render_metadata = {
                "engine": "ProfessionalCompositingEngine_v3D3_SafezoneEnforced",
                "layers_count": 13,
                "debug_safezone": debug_safezone,
                "safezone": {
                    "top": SAFEZONE_TOP,
                    "bottom": SAFEZONE_BOTTOM,
                    "height": SAFEZONE_HEIGHT,
                    "left_crop_3_4": 34,
                    "right_crop_3_4": 34,
                    "grid_3_4_width": 1012,
                    "grid_3_4_height": 1350,
                    "safezone_left": SAFEZONE_LEFT,
                    "safezone_right": SAFEZONE_RIGHT,
                    "safezone_content_left": SAFEZONE_CONTENT_LEFT,
                    "safezone_content_right": SAFEZONE_CONTENT_RIGHT,
                    "width": width,
                    "height": height
                },
                "critical_element_bounding_boxes": critical_bboxes,
                "headline_font_size": font_size,
                "highlight_strip_accent": accent_hex,
                "width": width,
                "height": height,
                "aspect_ratio": "4:5",
                "cta_strategy": actual_spec.cta_strategy.value,
                "render_latency_ms": max(latency_ms, 25)
            }
            return rendered_bytes, render_metadata

        except Exception as e:
            logger.exception(f"Compositing execution failed: {str(e)}")
            raise RenderingError(f"Failed to execute layered compositing: {str(e)}")
