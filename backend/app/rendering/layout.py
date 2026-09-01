import textwrap
from typing import List, Tuple, Dict, Any, Optional
from PIL import ImageFont, ImageDraw, Image


class LayoutEngine:
    """
    Computes deterministic layout geometries, font wrapping, and bounding boxes.
    """
    @staticmethod
    def wrap_text(text: str, max_chars_per_line: int = 24) -> List[str]:
        """Wraps text into clean, visually balanced lines."""
        if not text:
            return []
        lines = textwrap.wrap(text.strip(), width=max_chars_per_line, break_long_words=False)
        return lines

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
        min_size: int = 28
    ) -> Tuple[ImageFont.ImageFont, int]:
        """
        Dynamically calculates font size to ensure text fits strictly within max boundaries.
        """
        # Create dummy image to measure
        dummy_img = Image.new("RGBA", (1, 1))
        draw = ImageDraw.Draw(dummy_img)

        current_size = initial_size
        while current_size >= min_size:
            try:
                # Try loading standard truetype or fallback to default
                font = ImageFont.truetype("arial.ttf", current_size)
            except IOError:
                font = ImageFont.load_default()
                return font, current_size

            w, h = LayoutEngine.calculate_text_bounding_box(draw, text_lines, font)
            if w <= max_width and h <= max_height:
                return font, current_size
            current_size -= 4

        try:
            return ImageFont.truetype("arial.ttf", min_size), min_size
        except IOError:
            return ImageFont.load_default(), min_size

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
