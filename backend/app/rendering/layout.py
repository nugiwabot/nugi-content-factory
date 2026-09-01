import re
import textwrap
from typing import List, Tuple, Dict, Any, Optional
from PIL import ImageFont, ImageDraw, Image, ImageFilter
from app.schemas.design_spec import (
    SAFEZONE_TOP,
    SAFEZONE_BOTTOM,
    SAFEZONE_HEIGHT,
    SAFEZONE_LEFT,
    SAFEZONE_RIGHT,
    SAFEZONE_CONTENT_LEFT,
    SAFEZONE_CONTENT_RIGHT
)


class LayoutEngine:
    """
    Layout & Typography Engine (Phase 3D-3).
    Implements Safezone-Enforced Editorial Composition:
    - Seamless dark gradient scrim across lower canvas.
    - Solid vibrant highlight strips/pills directly behind punchline lines (mathematically centered).
    - Massive bold white typography (72–104px) with maximum contrast.
    - Precise text bounding-box measurement and safezone validation.
    - Optional debug visual overlay (strictly disabled in production).
    """
    @staticmethod
    def wrap_text(text: str, max_chars_per_line: int = 26) -> List[str]:
        """Wraps text into clean, visually balanced lines."""
        if not text:
            return []
        lines = textwrap.wrap(text.strip(), width=max_chars_per_line, break_long_words=False)
        return lines

    @staticmethod
    def wrap_headline_punchy(text: str, max_chars_per_line: int = 22) -> List[str]:
        """
        Wraps headlines into short, punchy 2-4 lines (Akademi Kripto style).
        Avoids single-word orphan lines.
        """
        if not text:
            return []
        
        cleaned = text.strip()
        words = cleaned.split()
        if len(words) <= 3:
            return [cleaned]
        
        raw_lines = textwrap.wrap(cleaned, width=max_chars_per_line, break_long_words=False)
        
        # Balance orphan words on last line
        if len(raw_lines) > 1 and len(raw_lines[-1].split()) == 1 and len(raw_lines[-2].split()) > 2:
            prev_words = raw_lines[-2].split()
            last_word_of_prev = prev_words.pop()
            raw_lines[-2] = " ".join(prev_words)
            raw_lines[-1] = f"{last_word_of_prev} {raw_lines[-1]}"

        return raw_lines[:4]

    @staticmethod
    def segment_highlighted_line(line: str, highlight_terms: List[str]) -> List[Tuple[str, bool]]:
        """
        Splits a single line into sequential segments of (text_chunk, is_highlighted).
        Handles multi-word phrases, single words, and markup like *text* or {text}.
        """
        if not line:
            return []

        spans: List[Tuple[int, int]] = []

        # 1. Regex markers: *phrase* or {phrase}
        for match in re.finditer(r"\*([^*]+)\*|\{([^}]+)\}", line):
            spans.append((match.start(), match.end()))

        # 2. Case-insensitive term search for multi-word or single-word phrases
        line_upper = line.upper()
        for term in (highlight_terms or []):
            term_clean = term.strip().upper()
            if not term_clean:
                continue
            start_idx = 0
            while True:
                idx = line_upper.find(term_clean, start_idx)
                if idx == -1:
                    break
                spans.append((idx, idx + len(term_clean)))
                start_idx = idx + len(term_clean)

        if not spans:
            return [(line, False)]

        # Sort and merge overlapping spans
        spans.sort(key=lambda s: s[0])
        merged_spans: List[Tuple[int, int]] = []
        for s_start, s_end in spans:
            if not merged_spans:
                merged_spans.append((s_start, s_end))
            else:
                prev_start, prev_end = merged_spans[-1]
                if s_start <= prev_end:
                    merged_spans[-1] = (prev_start, max(prev_end, s_end))
                else:
                    merged_spans.append((s_start, s_end))

        # Slice line into sequential segments
        segments: List[Tuple[str, bool]] = []
        curr = 0
        for s_start, s_end in merged_spans:
            if s_start > curr:
                segments.append((line[curr:s_start], False))

            raw_hl_text = line[s_start:s_end]
            if (raw_hl_text.startswith("*") and raw_hl_text.endswith("*")) or \
               (raw_hl_text.startswith("{") and raw_hl_text.endswith("}")):
                raw_hl_text = raw_hl_text[1:-1]

            segments.append((raw_hl_text, True))
            curr = s_end

        if curr < len(line):
            segments.append((line[curr:], False))

        return [seg for seg in segments if seg[0]]

    @staticmethod
    def draw_highlighted_line(
        draw: ImageDraw.ImageDraw,
        x: int,
        y: int,
        segments: List[Tuple[str, bool]],
        font: ImageFont.ImageFont,
        primary_color: Tuple[int, int, int, int] = (255, 255, 255, 255),
        highlight_color: Tuple[int, int, int, int] = (56, 189, 248, 255),
        with_shadow: bool = True
    ) -> int:
        """Renders a line with mixed highlight words and drop shadow."""
        curr_x = x
        line_height = 0

        for text_chunk, is_hl in segments:
            color = highlight_color if is_hl else primary_color
            bbox = draw.textbbox((0, 0), text_chunk, font=font)
            chunk_width = bbox[2] - bbox[0]
            chunk_height = bbox[3] - bbox[1]
            line_height = max(line_height, chunk_height)

            if with_shadow:
                draw.text((curr_x + 2, y + 2), text_chunk, fill=(0, 0, 0, 190), font=font)
            draw.text((curr_x, y), text_chunk, fill=color, font=font)
            curr_x += chunk_width

        return line_height

    @staticmethod
    def calculate_text_bounding_box(
        draw: ImageDraw.ImageDraw,
        text_lines: List[str],
        font: ImageFont.ImageFont,
        line_spacing: int = 12
    ) -> Tuple[int, int]:
        """Calculates total width and height of multi-line text block."""
        max_width = 0
        total_height = 0
        for i, line in enumerate(text_lines):
            bbox = draw.textbbox((0, 0), line, font=font)
            line_w = bbox[2] - bbox[0]
            line_h = bbox[3] - bbox[1]
            max_width = max(max_width, line_w)
            total_height += line_h
            if i < len(text_lines) - 1:
                total_height += line_spacing
        return max_width, total_height

    @staticmethod
    def get_fitted_font(
        text_lines: List[str],
        max_width: int,
        max_height: int,
        initial_size: int = 74,
        min_size: int = 44,
        bold: bool = True
    ) -> Tuple[ImageFont.ImageFont, int]:
        """
        Dynamically calculates font size to ensure headline is BIG, BOLD, and fits within max boundaries.
        Prefers extra-bold weights.
        """
        dummy_img = Image.new("RGBA", (1, 1))
        draw = ImageDraw.Draw(dummy_img)

        font_files = ["arialbd.ttf" if bold else "arial.ttf", "arial.ttf", "DejaVuSans-Bold.ttf", "DejaVuSans.ttf"]

        current_size = initial_size
        while current_size >= min_size:
            font = None
            for fn in font_files:
                try:
                    font = ImageFont.truetype(fn, current_size)
                    break
                except IOError:
                    continue
            if not font:
                font = ImageFont.load_default()
                return font, current_size

            w, h = LayoutEngine.calculate_text_bounding_box(draw, text_lines, font, line_spacing=int(current_size * 0.22))
            if w <= max_width and h <= max_height:
                return font, current_size
            current_size -= 2

        # Min size fallback
        for fn in font_files:
            try:
                return ImageFont.truetype(fn, min_size), min_size
            except IOError:
                continue
        return ImageFont.load_default(), min_size

    @staticmethod
    def draw_editorial_headline_with_strips(
        canvas: Image.Image,
        lines: List[str],
        highlight_terms: List[str],
        start_x: int,
        start_y: int,
        font: ImageFont.ImageFont,
        font_size: int,
        accent_rgb: Tuple[int, int, int]
    ) -> Tuple[int, Dict[str, Dict[str, int]]]:
        """
        Renders headline with Akademi Kripto aesthetic:
        - Regular lines in pure bold white.
        - Highlight line on top of a solid vibrant neon background strip/pill.
        - Perfectly centered mathematically.
        - Returns (end_y, measured_bboxes).
        """
        draw = ImageDraw.Draw(canvas)
        curr_y = start_y
        line_spacing = int(font_size * 0.22)
        pad_h = 16  # Horizontal padding inside highlight strip
        pad_v = 10  # Vertical padding inside highlight strip

        highlight_line_indices = set()
        hl_terms_upper = [t.strip().upper() for t in (highlight_terms or []) if t.strip()]

        for idx, line in enumerate(lines):
            line_up = line.upper()
            if any(term in line_up for term in hl_terms_upper):
                highlight_line_indices.add(idx)

        if not highlight_line_indices and len(lines) > 0:
            highlight_line_indices.add(len(lines) - 1)

        measured_bboxes = {}
        min_left = start_x
        max_right = start_x
        start_block_y = curr_y

        for idx, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=font)
            offset_x = bbox[0]
            offset_y = bbox[1]
            actual_w = bbox[2] - bbox[0]
            actual_h = bbox[3] - bbox[1]

            is_highlighted = (idx in highlight_line_indices)

            strip_y1 = curr_y
            strip_y2 = curr_y + actual_h + (pad_v * 2)
            draw_text_x = (start_x + pad_h) - offset_x
            draw_text_y = (curr_y + pad_v) - offset_y

            if is_highlighted:
                # Solid vibrant highlight strip behind the text
                strip_x1 = start_x
                strip_x2 = start_x + actual_w + (pad_h * 2)

                draw.rounded_rectangle(
                    [strip_x1, strip_y1, strip_x2, strip_y2],
                    radius=4,
                    fill=(accent_rgb[0], accent_rgb[1], accent_rgb[2], 255)
                )

                # Pure white bold text inside the strip (perfectly centered)
                draw.text(
                    (draw_text_x, draw_text_y),
                    line,
                    fill=(255, 255, 255, 255),
                    font=font
                )

                max_right = max(max_right, strip_x2)
                measured_bboxes["highlight_pill"] = {
                    "left": strip_x1,
                    "top": strip_y1,
                    "right": strip_x2,
                    "bottom": strip_y2
                }
            else:
                # Regular line: Pure white text with soft dark drop shadow
                draw.text((draw_text_x + 2, draw_text_y + 2), line, fill=(0, 0, 0, 220), font=font)
                draw.text((draw_text_x, draw_text_y), line, fill=(255, 255, 255, 255), font=font)
                max_right = max(max_right, start_x + pad_h + actual_w)

            curr_y += actual_h + (pad_v * 2) + line_spacing

        measured_bboxes["headline_block"] = {
            "left": min_left,
            "top": start_block_y,
            "right": max_right,
            "bottom": curr_y - line_spacing
        }

        return curr_y, measured_bboxes

    @staticmethod
    def draw_bottom_gradient_scrim(
        canvas: Image.Image,
        start_y: int = 650,
        end_y: int = 1350,
        dark_rgb: Tuple[int, int, int] = (4, 7, 17)
    ) -> Image.Image:
        """
        Creates a seamless, silky dark gradient scrim across the lower canvas (Akademi Kripto style).
        Fades from 0% opacity to 100% solid dark at the bottom.
        """
        width, height = canvas.size
        scrim_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(scrim_layer)

        span = float(end_y - start_y)
        for y in range(start_y, end_y):
            ratio = (y - start_y) / span
            alpha = int((ratio ** 1.8) * 255)
            draw.line([(0, y), (width, y)], fill=(dark_rgb[0], dark_rgb[1], dark_rgb[2], min(alpha, 255)), width=1)

        if end_y < height:
            draw.rectangle([0, end_y, width, height], fill=(dark_rgb[0], dark_rgb[1], dark_rgb[2], 255))

        return Image.alpha_composite(canvas, scrim_layer)

    @staticmethod
    def validate_element_bounding_box(
        bbox: Dict[str, int],
        safezone_bounds: Optional[Dict[str, Any]] = None
    ) -> Tuple[bool, List[str]]:
        """
        Validates if a critical element bounding box is 100% within safe content boundaries.
        Safe content area: [76..1004, 135..1215].
        """
        bounds = safezone_bounds or {
            "safezone_content_left": SAFEZONE_CONTENT_LEFT,
            "safezone_content_right": SAFEZONE_CONTENT_RIGHT,
            "top": SAFEZONE_TOP,
            "bottom": SAFEZONE_BOTTOM
        }
        
        min_x = bounds.get("safezone_content_left", SAFEZONE_CONTENT_LEFT)
        max_x = bounds.get("safezone_content_right", SAFEZONE_CONTENT_RIGHT)
        min_y = bounds.get("top", SAFEZONE_TOP)
        max_y = bounds.get("bottom", SAFEZONE_BOTTOM)

        l = bbox.get("left", 0)
        t = bbox.get("top", 0)
        r = bbox.get("right", 0)
        b = bbox.get("bottom", 0)

        violations = []
        if l < min_x:
            violations.append(f"Left bound ({l}px) < Safe Content Left ({min_x}px)")
        if r > max_x:
            violations.append(f"Right bound ({r}px) > Safe Content Right ({max_x}px)")
        if t < min_y:
            violations.append(f"Top bound ({t}px) < Safezone Top ({min_y}px)")
        if b > max_y:
            violations.append(f"Bottom bound ({b}px) > Safezone Bottom ({max_y}px)")

        return (len(violations) == 0), violations

    @staticmethod
    def draw_debug_safezone_overlay(
        canvas: Image.Image,
        critical_bboxes: Dict[str, Dict[str, int]],
        safezone_bounds: Optional[Dict[str, Any]] = None
    ) -> Image.Image:
        """
        Renders an explicit diagnostic overlay for debugging safezones (Phase 3D-3).
        - Cyan rectangle: Master Safe Content Area [76..1004, 135..1215]
        - Magenta lines: Instagram 3:4 Profile Grid crop (x=34, x=1046)
        - Yellow lines: Instagram 1:1 Square Feed crop (y=135, y=1215)
        - Green bounding boxes: Inside Safezone
        - Red bounding boxes: Overflowing Elements
        NOTE: Disabled in production.
        """
        debug_img = canvas.copy().convert("RGBA")
        overlay = Image.new("RGBA", debug_img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        width, height = debug_img.size

        # 1. 3:4 Profile Grid Crop Lines (x=34, x=1046)
        draw.line([(34, 0), (34, height)], fill=(236, 72, 153, 200), width=2)
        draw.line([(1046, 0), (1046, height)], fill=(236, 72, 153, 200), width=2)

        # 2. 1:1 Square Feed Crop Lines (y=135, y=1215)
        draw.line([(0, 135), (width, 135)], fill=(234, 179, 8, 200), width=2)
        draw.line([(0, 1215), (width, 1215)], fill=(234, 179, 8, 200), width=2)

        # 3. Master Content Safezone Box (Cyan [76, 135, 1004, 1215])
        draw.rectangle([76, 135, 1004, 1215], outline=(6, 182, 212, 220), width=2)

        # 4. Critical Element Bounding Boxes
        for elem_name, box in (critical_bboxes or {}).items():
            l, t, r, b = box.get("left", 0), box.get("top", 0), box.get("right", 0), box.get("bottom", 0)
            is_valid, _ = LayoutEngine.validate_element_bounding_box(box, safezone_bounds)
            outline_color = (34, 197, 94, 240) if is_valid else (239, 68, 68, 255)
            draw.rectangle([l, t, r, b], outline=outline_color, width=2)

        return Image.alpha_composite(debug_img, overlay)

    @staticmethod
    def calculate_luminance(color_rgb: Tuple[int, int, int]) -> float:
        """Calculates relative luminance for WCAG contrast ratio."""
        r, g, b = [x / 255.0 for x in color_rgb[:3]]
        r = r / 12.92 if r <= 0.03928 else ((r + 0.055) / 1.055) ** 2.4
        g = g / 12.92 if g <= 0.03928 else ((g + 0.055) / 1.055) ** 2.4
        b = b / 12.92 if b <= 0.03928 else ((b + 0.055) / 1.055) ** 2.4
        return 0.2126 * r + 0.7152 * g + 0.0722 * b

    @staticmethod
    def calculate_contrast_ratio(rgb1: Tuple[int, int, int], rgb2: Tuple[int, int, int]) -> float:
        """Returns contrast ratio between two colors (1.0 to 21.0)."""
        l1 = LayoutEngine.calculate_luminance(rgb1)
        l2 = LayoutEngine.calculate_luminance(rgb2)
        bright = max(l1, l2)
        dark = min(l1, l2)
        return (bright + 0.05) / (dark + 0.05)
