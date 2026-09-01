# 🖼️ Phase 03C: Composition, Lighting, Depth & Color Grading System

## 1. Realistic Lighting Match

To prevent the common "cheap pasted AI sticker" look, the compositing engine simulates coherent lighting interaction:
1. **Directional Ambient Glow:** Projected from the dominant light source (e.g. upper right) with soft gaussian diffusion.
2. **Subject Rim Light Simulation:** Accentuates bright edge contours along the subject's boundary.
3. **Contact Occlusion Shadow:** Renders soft contact shadows at the base of the subject onto the scene floor.

---

## 2. Multi-Plane Depth System

* **Foreground:** Scrim gradient ensuring WCAG AAA typography contrast without completely obscuring scene details.
* **Midground:** Sharp focal point containing the subject and key architectural features.
* **Background:** Soft contrast attenuation (*atmospheric haze*) providing realistic perspective depth.

---

## 3. Color Grading Presets

* `CINEMATIC_TWILIGHT`: Cool navy shadows with balanced exposure and subtle amber warmth.
* `PREMIUM_GOLD`: Warm champagne temperature shift (+0.20 Kelvin) for luxury showcase content.
* `DEEP_OBSIDIAN`: High-contrast monochrome slate styling for authoritative opinion pieces.
