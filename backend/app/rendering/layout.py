import re
import textwrap
from typing import List, Tuple, Dict, Any, Optional
from PIL import ImageFont, ImageDraw, Image


class LayoutEngine:
    """
    Computes deterministic layout geometries, font wrapping, word highlighting, and bounding boxes.
    """
    @staticmethod
    def wrap_text(text: str, max_chars_per_line: int = 24) -> List[str]:
        """Wraps text into clean, visually balanced lines."""
        if not text:
            return []
        lines = textwrap.wrap(text.strip(), width=max_chars_per_line, break_long_words=False)
        return lines

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
        for term in highlight_terms:
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
        initial_size: int = 64,
        min_size: int = 26
    ) -> Tuple[ImageFont.ImageFont, int]:
        """
        Dynamically calculates font size to ensure text fits strictly within max boundaries.
        """
        dummy_img = Image.new("RGBA", (1, 1))
        draw = ImageDraw.Draw(dummy_img)

        current_size = initial_size
        while current_size >= min_size:
            try:
                font = ImageFont.truetype("arial.ttf", current_size)
            except IOError:
                font = ImageFont.load_default()
                return font, current_size

            w, h = LayoutEngine.calculate_text_bounding_box(draw, text_lines, font)
            if w <= max_width and h <= max_height:
                return font, current_size
            current_size -= 2

        try:
            return ImageFont.truetype("arial.ttf", min_size), min_size
        except IOError:
            return ImageFont.load_default(), min_size

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
        """
        Renders a line with mixed highlight words and drop shadow.
        Returns the rendered line height.
        """
        curr_x = x
        line_height = 0

        for text_chunk, is_hl in segments:
            color = highlight_color if is_hl else primary_color
            
            # Shadow
            if with_shadow:
                draw.text((curr_x + 2, y + 2), text_chunk, fill=(0, 0, 0, 190), font=font)
            
            # Main Text
            draw.text((curr_x, y), text_chunk, fill=color, font=font)
            
            bbox = draw.textbbox((0, 0), text_chunk, font=font)
            chunk_width = bbox[2] - bbox[0]
            chunk_height = bbox[3] - bbox[1]
            line_height = max(line_height, chunk_height)
            curr_x += chunk_width

        return line_height

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
