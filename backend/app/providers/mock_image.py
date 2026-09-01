import io
import time
from typing import Optional
from PIL import Image, ImageDraw
from app.providers.base import ImageProvider, ImageGenerationOutput


class MockImageProvider(ImageProvider):
    """
    Deterministic Mock Image provider creating aesthetic visual background canvases
    via Pillow without external network or GPU overhead.
    """
    @property
    def provider_name(self) -> str:
        return "MockImageProvider"

    def generate_background(
        self,
        prompt: str,
        width: int = 1080,
        height: int = 1080,
        style_preset: Optional[str] = None
    ) -> ImageGenerationOutput:
        start_time = time.time()

        # Create base canvas with deep obsidian/navy background
        img = Image.new("RGB", (width, height), color=(10, 16, 26))
        draw = ImageDraw.Draw(img)

        # Generate smooth modern gradient overlay
        for y in range(height):
            # Gradient transition from deep slate to deep blue
            r = int(10 + (y / height) * 15)
            g = int(16 + (y / height) * 25)
            b = int(26 + (y / height) * 45)
            draw.line([(0, y), (width, y)], fill=(r, g, b))

        # Add subtle architectural grid accents (deterministic geometric lines)
        accent_color = (30, 45, 70)
        grid_step = width // 10
        for x in range(0, width, grid_step):
            draw.line([(x, 0), (x, height)], fill=accent_color, width=1)
        for y in range(0, height, grid_step):
            draw.line([(0, y), (width, y)], fill=accent_color, width=1)

        # Add modern soft lighting sphere in top corner
        glow_center = (int(width * 0.75), int(height * 0.25))
        glow_radius = int(width * 0.35)
        # Inner subtle aura
        draw.ellipse(
            [
                (glow_center[0] - glow_radius, glow_center[1] - glow_radius),
                (glow_center[0] + glow_radius, glow_center[1] + glow_radius)
            ],
            fill=(24, 40, 68),
            outline=(45, 75, 120),
            width=1
        )

        # Export to PNG bytes in memory
        buffer = io.BytesIO()
        img.save(buffer, format="PNG", optimize=True)
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
