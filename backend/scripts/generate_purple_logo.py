import os
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

DIR_FREELANCE = Path("C:/Users/Nugi/Documents/Freelance Nugi jasa software engginer/assets/logo")
DIR_CONTENT_FACTORY = Path("C:/Users/Nugi/Documents/nugi-content-factory/assets/brand")
DIR_SCRATCH = Path("C:/Users/Nugi/.gemini/antigravity-ide/brain/b80f175e-f63e-4113-aca5-af8b92fed644/scratch")

for d in [DIR_FREELANCE, DIR_CONTENT_FACTORY, DIR_SCRATCH]:
    d.mkdir(parents=True, exist_ok=True)

# Color Palette Matching Nugi Editorial Design DNA (Akademi Kripto standard)
C_WHITE = (255, 255, 255, 255)
C_DARK_SLATE = (15, 23, 42, 255)          # #0F172A
C_NEON_VIOLET = (139, 92, 246, 255)       # #8B5CF6 (Exact Signature Violet)
C_DEEP_VIOLET = (109, 40, 217, 255)       # #6D28D9 (Violet 700)
C_LIGHT_VIOLET = (196, 181, 253, 255)     # #C4B5FD (Violet 300)
C_ICE_VIOLET = (245, 243, 255, 255)       # #F5F3FF
C_SLATE_400 = (148, 163, 184, 255)
C_SLATE_800 = (30, 41, 59, 255)

def load_font(size: int, bold: bool = True):
    font_paths = [
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "arialbd.ttf" if bold else "arial.ttf",
        "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    ]
    for fp in font_paths:
        try:
            return ImageFont.truetype(fp, size)
        except Exception:
            continue
    return ImageFont.load_default()

# ------------------------------------------------------------------------------
# 1. ICON VARIANT A: SLEEK MONOGRAM 'N' SKYSCRAPER (PURPLE)
# ------------------------------------------------------------------------------
def draw_monogram_n_icon(draw, cx, cy, scale=1.0, is_dark_mode=True):
    col_w = int(52 * scale)
    span = int(70 * scale)
    h_left = int(220 * scale)
    h_right = int(270 * scale)
    rad = int(10 * scale)

    x1 = cx - span - col_w // 2
    x2 = x1 + col_w
    y1_top = cy - h_left // 2
    y1_bot = cy + h_left // 2

    x3 = cx + span - col_w // 2
    x4 = x3 + col_w
    y2_top = cy - h_right // 2
    y2_bot = cy + h_right // 2

    # 1. Diagonal Bridge ('N' connecting beam)
    beam_th = int(44 * scale)
    draw.polygon([
        (x2, y1_top + int(10 * scale)),
        (x3, y2_bot - int(25 * scale)),
        (x3, y2_bot),
        (x2, y1_top + beam_th + int(10 * scale))
    ], fill=C_DEEP_VIOLET)

    # 2. Left Tower (Electric Neon Violet)
    draw.rounded_rectangle([x1, y1_top, x2, y1_bot], radius=rad, fill=C_NEON_VIOLET)

    # 3. Right Tower (Pure White on Dark / Deep Slate on Light)
    r_fill = C_WHITE if is_dark_mode else C_DARK_SLATE
    draw.rounded_rectangle([x3, y2_top, x4, y2_bot], radius=rad, fill=r_fill)

    # 4. Architectural Windows on Left Tower
    win_left = (76, 29, 149, 255) if is_dark_mode else (221, 214, 254, 255)
    for i in range(4):
        wy = y1_top + int(28 * scale) + int(i * 44 * scale)
        draw.rectangle([x1 + int(12 * scale), wy, x2 - int(12 * scale), wy + int(18 * scale)], fill=win_left)

    # 5. Architectural Windows on Right Tower
    win_right = (148, 163, 184, 255) if is_dark_mode else (100, 116, 139, 255)
    for i in range(5):
        wy = y2_top + int(28 * scale) + int(i * 44 * scale)
        draw.rectangle([x3 + int(12 * scale), wy, x4 - int(12 * scale), wy + int(18 * scale)], fill=win_right)


# ------------------------------------------------------------------------------
# 2. ICON VARIANT B: ISOMETRIC 3D SKYSCRAPER IN ALL-PURPLE & WHITE
# ------------------------------------------------------------------------------
def draw_isometric_purple_building(draw, cx, cy, scale=1.0, is_dark_mode=True):
    tw = int(120 * scale)
    th = int(220 * scale)
    
    # Left Facade (Deep Royal Violet)
    draw.polygon([
        (cx - tw, cy + th // 2),
        (cx - tw, cy - th // 2),
        (cx - tw // 4, cy - th // 2 - int(35 * scale)),
        (cx - tw // 4, cy + th // 2 - int(35 * scale))
    ], fill=C_DEEP_VIOLET)

    # Right Facade (Electric Neon Violet)
    draw.polygon([
        (cx - tw // 4, cy + th // 2 - int(35 * scale)),
        (cx - tw // 4, cy - th // 2 - int(35 * scale)),
        (cx + tw, cy - th // 2 + int(18 * scale)),
        (cx + tw, cy + th // 2 + int(18 * scale))
    ], fill=C_NEON_VIOLET)

    # Roof Slab (Pure Ice White)
    draw.polygon([
        (cx - tw, cy - th // 2),
        (cx - tw // 4, cy - th // 2 - int(35 * scale)),
        (cx + int(25 * scale), cy - th // 2 - int(60 * scale)),
        (cx - int(40 * scale), cy - th // 2 - int(25 * scale))
    ], fill=C_ICE_VIOLET)

    # Windows on Left Facade (Glowing Violet)
    for r in range(4):
        wy = cy - int(80 * scale) + int(r * 45 * scale)
        draw.polygon([
            (cx - int(105 * scale), wy),
            (cx - int(45 * scale), wy - int(22 * scale)),
            (cx - int(45 * scale), wy - int(5 * scale)),
            (cx - int(105 * scale), wy + int(18 * scale))
        ], fill=(167, 139, 250, 255))

    # Windows on Right Facade (Crisp White / Ice)
    for r in range(4):
        wy = cy - int(115 * scale) + int(r * 55 * scale)
        # Col 1
        draw.polygon([
            (cx - int(8 * scale), wy),
            (cx + int(32 * scale), wy + int(18 * scale)),
            (cx + int(32 * scale), wy + int(36 * scale)),
            (cx - int(8 * scale), wy + int(18 * scale))
        ], fill=C_WHITE)
        # Col 2
        draw.polygon([
            (cx + int(45 * scale), wy + int(26 * scale)),
            (cx + int(80 * scale), wy + int(45 * scale)),
            (cx + int(80 * scale), wy + int(63 * scale)),
            (cx + int(45 * scale), wy + int(45 * scale))
        ], fill=C_ICE_VIOLET)


# ------------------------------------------------------------------------------
# 3. HORIZONTAL MASTER LOGOS (DARK & LIGHT) — 2800 x 500 px
# ------------------------------------------------------------------------------
def generate_horizontal_logo_dark(width=2800, height=500, use_monogram=True):
    canvas = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)

    icon_cx = 240
    icon_cy = height // 2
    
    if use_monogram:
        draw_monogram_n_icon(draw, cx=icon_cx, cy=icon_cy, scale=1.0, is_dark_mode=True)
        text_x = 440
    else:
        draw_isometric_purple_building(draw, cx=icon_cx, cy=icon_cy, scale=0.9, is_dark_mode=True)
        text_x = 440

    font_main = load_font(180, bold=True)
    text_y = height // 2 - 100

    draw.text((text_x, text_y), "NUGI", fill=C_WHITE, font=font_main)
    w_nugi = draw.textlength("NUGI", font=font_main)
    draw.text((text_x + w_nugi + 18, text_y), "PROPERTI", fill=C_NEON_VIOLET, font=font_main)

    return canvas

def generate_horizontal_logo_light(width=2800, height=500, use_monogram=True):
    canvas = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)

    icon_cx = 240
    icon_cy = height // 2
    
    if use_monogram:
        draw_monogram_n_icon(draw, cx=icon_cx, cy=icon_cy, scale=1.0, is_dark_mode=False)
        text_x = 440
    else:
        draw_isometric_purple_building(draw, cx=icon_cx, cy=icon_cy, scale=0.9, is_dark_mode=False)
        text_x = 440

    font_main = load_font(180, bold=True)
    text_y = height // 2 - 100

    draw.text((text_x, text_y), "NUGI", fill=C_DARK_SLATE, font=font_main)
    w_nugi = draw.textlength("NUGI", font=font_main)
    draw.text((text_x + w_nugi + 18, text_y), "PROPERTI", fill=C_DEEP_VIOLET, font=font_main)

    return canvas


# ------------------------------------------------------------------------------
# 4. SQUARE APP ICON / PROFILE AVATAR (1024x1024)
# ------------------------------------------------------------------------------
def generate_square_avatar(size=1024, use_monogram=True):
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)

    cx, cy = size // 2, size // 2

    # Obsidian Rounded Shield with Neon Violet Glow Border
    pad = int(70 * (size / 1024.0))
    rad = int(200 * (size / 1024.0))
    border_w = int(18 * (size / 1024.0))
    draw.rounded_rectangle([pad, pad, size - pad, size - pad], radius=rad, fill=(7, 11, 20, 255), outline=C_NEON_VIOLET, width=border_w)

    scale_factor = 2.1 * (size / 1024.0)

    if use_monogram:
        draw_monogram_n_icon(draw, cx=cx, cy=cy, scale=scale_factor, is_dark_mode=True)
    else:
        draw_isometric_purple_building(draw, cx=cx, cy=cy, scale=scale_factor, is_dark_mode=True)

    return canvas


# ------------------------------------------------------------------------------
# 5. MASTER PRESENTATION SHOWCASE
# ------------------------------------------------------------------------------
def generate_master_showcase():
    w, h = 2400, 2200
    sheet = Image.new("RGBA", (w, h), (4, 7, 17, 255)) # Obsidian Dark Canvas
    draw = ImageDraw.Draw(sheet)

    f_title = load_font(76, bold=True)
    f_sub = load_font(36, bold=False)
    f_label = load_font(34, bold=True)
    f_desc = load_font(26, bold=False)

    # Title
    draw.text((100, 70), "NUGIPROPERTI — OFFICIAL PURPLE BRAND LOGO SUITE", fill=C_WHITE, font=f_title)
    draw.text((100, 160), "Monogram 'N' Skyscraper • #8B5CF6 Electric Neon Violet • 100% Transparent PNG", fill=C_NEON_VIOLET, font=f_sub)
    draw.line([(100, 220), (w - 100, 220)], fill=(255, 255, 255, 30), width=2)

    # Section 1: Dark Mode Version (Monogram N)
    y1 = 260
    draw.rounded_rectangle([100, y1, w - 100, y1 + 500], radius=24, fill=(15, 23, 42, 220), outline=C_NEON_VIOLET, width=2)
    draw.text((140, y1 + 35), "1. VERSI DARK MODE (INSTAGRAM FEED, COVER, EDITORIAL HEADER)", fill=C_WHITE, font=f_label)
    draw.text((140, y1 + 80), "Background Transparan PNG • NUGI (Putih) + PROPERTI (Ungu Neon #8B5CF6) • Clean & Bold", fill=C_SLATE_400, font=f_desc)
    
    logo_dark = generate_horizontal_logo_dark(2800, 500, use_monogram=True)
    scale = 2000 / logo_dark.width
    scaled_d = logo_dark.resize((2000, int(logo_dark.height * scale)), Image.Resampling.LANCZOS)
    sheet.paste(scaled_d, (140, y1 + 120), scaled_d)

    # Section 2: Light Mode Version (Monogram N)
    y2 = 800
    draw.rounded_rectangle([100, y2, w - 100, y2 + 500], radius=24, fill=(248, 250, 252, 255), outline=(226, 232, 240, 255), width=2)
    draw.text((140, y2 + 35), "2. VERSI LIGHT MODE (INVOICE, PROPOSAL PDF, DOKUMEN CETAK & WEB TERANG)", fill=C_DARK_SLATE, font=f_label)
    draw.text((140, y2 + 80), "Background Transparan PNG • NUGI (Dark Slate #0F172A) + PROPERTI (Ungu #6D28D9)", fill=(100, 116, 139, 255), font=f_desc)
    
    logo_light = generate_horizontal_logo_light(2800, 500, use_monogram=True)
    scaled_l = logo_light.resize((2000, int(logo_light.height * scale)), Image.Resampling.LANCZOS)
    sheet.paste(scaled_l, (140, y2 + 120), scaled_l)

    # Section 3: Profile Avatar & 3D Building Alt
    y3 = 1340
    draw.rounded_rectangle([100, y3, w - 100, y3 + 740], radius=24, fill=(15, 23, 42, 220), outline=C_NEON_VIOLET, width=2)
    draw.text((140, y3 + 35), "3. FOTO PROFIL (1:1 AVATAR) & ALTERNATIF GEDUNG 3D ISOMETRIC UNGU", fill=C_WHITE, font=f_label)
    draw.text((140, y3 + 80), "Format 1024x1024 siap pakai untuk Instagram @nugiproperti, WhatsApp Business & Favicon", fill=C_SLATE_400, font=f_desc)
    
    avatar = generate_square_avatar(520, use_monogram=True)
    sheet.paste(avatar, (140, y3 + 140), avatar)
    
    # Building alt on right side
    b_dark = generate_horizontal_logo_dark(2800, 500, use_monogram=False)
    b_scale = 1450 / b_dark.width
    b_scaled = b_dark.resize((1450, int(b_dark.height * b_scale)), Image.Resampling.LANCZOS)
    sheet.paste(b_scaled, (720, y3 + 220), b_scaled)
    
    draw.text((740, y3 + 160), "ALTERNATIF GEDUNG 3D ISOMETRIC FULL UNGU:", fill=C_NEON_VIOLET, font=f_label)
    draw.text((740, y3 + 520), "Tersedia juga varian gedung 3D full ungu dalam resolusi 2800px transparan.", fill=C_SLATE_400, font=f_desc)

    return sheet

# ------------------------------------------------------------------------------
# SAVE ALL ASSETS
# ------------------------------------------------------------------------------
files = {
    # Primary Monogram N Logos (Clean No Subtitle, Purple)
    "nugi_properti_logo_purple_transparent_dark_bg.png": generate_horizontal_logo_dark(use_monogram=True),
    "nugi_properti_logo_purple_transparent_light_bg.png": generate_horizontal_logo_light(use_monogram=True),
    
    # Isometric 3D Building Purple Variant
    "nugi_properti_logo_3d_building_purple_dark.png": generate_horizontal_logo_dark(use_monogram=False),
    "nugi_properti_logo_3d_building_purple_light.png": generate_horizontal_logo_light(use_monogram=False),

    # Square Profile Avatars (Monogram and 3D Building)
    "nugi_properti_avatar_purple_1024x1024.png": generate_square_avatar(use_monogram=True),
    "nugi_properti_avatar_3d_building_1024x1024.png": generate_square_avatar(use_monogram=False),

    # Showcase Sheet
    "nugi_properti_purple_logo_mockup.png": generate_master_showcase()
}

for name, img in files.items():
    for target in [DIR_FREELANCE, DIR_CONTENT_FACTORY, DIR_SCRATCH]:
        p = target / name
        img.save(p, format="PNG", optimize=True)
    print(f"Exported: {name} ({img.size[0]}x{img.size[1]} px)")

print("\nAll refined purple NugiProperti logo assets exported successfully.")
