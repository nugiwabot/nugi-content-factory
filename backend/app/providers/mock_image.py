import io
import time
from typing import Optional
from PIL import Image, ImageDraw, ImageFilter
from app.providers.base import ImageProvider, ImageGenerationOutput


class MockImageProvider(ImageProvider):
    """
    Deterministic Mock Image provider generating aesthetic cinematic architectural
    visual canvases via Pillow without external network or GPU overhead.
    """
    @property
    def provider_name(self) -> str:
        return "MockImageProvider"

    def generate_background(
        self,
        prompt: str,
        width: int = 1080,
        height: int = 1350,
        style_preset: Optional[str] = None
    ) -> ImageGenerationOutput:
        start_time = time.time()

        # 1. Base dark obsidian canvas
        img = Image.new("RGBA", (width, height), color=(7, 11, 20, 255))
        draw = ImageDraw.Draw(img)

        # 2. Rich atmospheric sky gradient (deep navy to twilight indigo/amber)
        for y in range(height):
            ratio = y / height
            r = int(7 + ratio * 18)
            g = int(11 + ratio * 24)
            b = int(20 + ratio * 42)
            draw.line([(0, y), (width, y)], fill=(r, g, b, 255))

        # 3. Modern Architectural Silhouettes & Facade Grid (Top/Center portion)
        # Building blocks with warm illuminated window textures
        arch_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        arch_draw = ImageDraw.Draw(arch_layer)

        # Building 1 (Left background tower)
        b1_box = [int(width * 0.08), int(height * 0.15), int(width * 0.42), int(height * 0.72)]
        arch_draw.rectangle(b1_box, fill=(16, 24, 40, 240), outline=(40, 60, 90, 180), width=2)
        
        # Illuminated glass window grid in Building 1
        for wy in range(b1_box[1] + 30, b1_box[3] - 40, 45):
            for wx in range(b1_box[0] + 25, b1_box[2] - 25, 35):
                arch_draw.rectangle([wx, wy, wx + 18, wy + 24], fill=(245, 158, 11, 140)) # Warm amber window

        # Building 2 (Right hero tower with glass facade)
        b2_box = [int(width * 0.45), int(height * 0.08), int(width * 0.92), int(height * 0.75)]
        arch_draw.rectangle(b2_box, fill=(22, 34, 56, 250), outline=(56, 189, 248, 160), width=2)

        for wy in range(b2_box[1] + 35, b2_box[3] - 40, 40):
            for wx in range(b2_box[0] + 30, b2_box[2] - 30, 42):
                arch_draw.rectangle([wx, wy, wx + 26, wy + 20], fill=(56, 189, 248, 120)) # Sky cyan glass light

        # 4. Cinematic Golden Hour Radial Lighting (Warm Sunset Accent)
        sun_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        sun_draw = ImageDraw.Draw(sun_layer)
        sun_center = (int(width * 0.5), int(height * 0.35))
        sun_radius = int(width * 0.4)
        sun_draw.ellipse(
            [sun_center[0] - sun_radius, sun_center[1] - sun_radius, sun_center[0] + sun_radius, sun_center[1] + sun_radius],
            fill=(245, 158, 11, 60)
        )
        sun_layer = sun_layer.filter(ImageFilter.GaussianBlur(radius=60))

        # 5. Composite Layers
        composite = Image.alpha_composite(img, sun_layer)
        composite = Image.alpha_composite(composite, arch_layer)

        # 6. Directional Bottom Scrim / Negative Space Gradient (Darkens bottom 50% for high contrast text)
        dark_scrim = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        scrim_draw = ImageDraw.Draw(dark_scrim)
        start_scrim_y = int(height * 0.35)
        for y in range(start_scrim_y, height):
            alpha = int(((y - start_scrim_y) / (height - start_scrim_y)) ** 1.5 * 245)
            scrim_draw.line([(0, y), (width, y)], fill=(7, 11, 20, alpha))

        final_composite = Image.alpha_composite(composite, dark_scrim)

        # Export to PNG bytes
        buffer = io.BytesIO()
        final_rgb = final_composite.convert("RGB")
        final_rgb.save(buffer, format="PNG", optimize=True)
        img_bytes = buffer.getvalue()

        latency_ms = int((time.time() - start_time) * 1000)
        return ImageGenerationOutput(
            image_bytes=img_bytes,
            format="PNG",
            width=width,
            height=height,
            prompt_used=prompt,
            latency_ms=max(latency_ms, 15)
        )
