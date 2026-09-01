import os
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

DIR_FREELANCE = Path("C:/Users/Nugi/Documents/Freelance Nugi jasa software engginer/assets/logo")
DIR_CONTENT_FACTORY = Path("C:/Users/Nugi/Documents/nugi-content-factory/assets/brand")
DIR_SCRATCH = Path("C:/Users/Nugi/.gemini/antigravity-ide/brain/b80f175e-f63e-4113-aca5-af8b92fed644/scratch")

for d in [DIR_FREELANCE, DIR_CONTENT_FACTORY, DIR_SCRATCH]:
    d.mkdir(parents=True, exist_ok=True)

# Color Palette
C_WHITE = (255, 255, 255, 255)
C_DARK_SLATE = (15, 23, 42, 255)       # #0F172A Dark Slate
C_CYAN = (56, 189, 248, 255)          # #38BDF8 Electric Sky Cyan
C_CYAN_DARK = (2, 132, 199, 255)      # #0284C7 Sky 600
C_VIOLET = (139, 92, 246, 255)        # #8B5CF6 Neon Violet
C_VIOLET_DARK = (124, 58, 237, 255)   # #7C3AED Violet 600
C_SLATE_MUTED = (148, 163, 184, 255)  # #94A3B8 Secondary
C_BG_OBSIDIAN = (7, 11, 20, 255)      # #070B14

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
# HELPER: DRAW 3D MODERN ISOMETRIC BUILDING ICON
# ------------------------------------------------------------------------------
def draw_3d_building_icon(draw, cx, cy, scale=1.0, accent_color=C_CYAN):
    # Main Tower
    tw = int(140 * scale)
    th = int(240 * scale)
    
    # Left Facade (3D depth / shading)
    draw.polygon([
        (cx - tw, cy + th // 2),
        (cx - tw, cy - th // 2),
        (cx - tw // 4, cy - th // 2 - int(40 * scale)),
        (cx - tw // 4, cy + th // 2 - int(40 * scale))
    ], fill=(71, 85, 105, 255))

    # Right / Front Facade
    draw.polygon([
        (cx - tw // 4, cy + th // 2 - int(40 * scale)),
        (cx - tw // 4, cy - th // 2 - int(40 * scale)),
        (cx + tw, cy - th // 2 + int(20 * scale)),
        (cx + tw, cy + th // 2 + int(20 * scale))
    ], fill=(148, 163, 184, 255))

    # Roof Slab
    draw.polygon([
        (cx - tw, cy - th // 2),
        (cx - tw // 4, cy - th // 2 - int(40 * scale)),
        (cx + int(30 * scale), cy - th // 2 - int(65 * scale)),
        (cx - int(45 * scale), cy - th // 2 - int(25 * scale))
    ], fill=(226, 232, 240, 255))

    # Left Facade Illuminated Windows
    for r in range(4):
        wy = cy - int(90 * scale) + int(r * 50 * scale)
        draw.polygon([
            (cx - int(120 * scale), wy),
            (cx - int(50 * scale), wy - int(25 * scale)),
            (cx - int(50 * scale), wy - int(5 * scale)),
            (cx - int(120 * scale), wy + int(20 * scale))
        ], fill=accent_color)

    # Right Facade Windows (2 Columns)
    for r in range(4):
        wy = cy - int(130 * scale) + int(r * 60 * scale)
        # Col 1
        draw.polygon([
            (cx - int(10 * scale), wy),
            (cx + int(35 * scale), wy + int(20 * scale)),
            (cx + int(35 * scale), wy + int(40 * scale)),
            (cx - int(10 * scale), wy + int(20 * scale))
        ], fill=accent_color)
        # Col 2
        draw.polygon([
            (cx + int(50 * scale), wy + int(30 * scale)),
            (cx + int(90 * scale), wy + int(50 * scale)),
            (cx + int(90 * scale), wy + int(70 * scale)),
            (cx + int(50 * scale), wy + int(50 * scale))
        ], fill=(186, 230, 253, 255) if accent_color == C_CYAN else (221, 214, 254, 255))

    # Modern Entrance Doorway
    draw.polygon([
        (cx + int(10 * scale), cy + int(115 * scale)),
        (cx + int(55 * scale), cy + int(138 * scale)),
        (cx + int(55 * scale), cy + int(175 * scale)),
        (cx + int(10 * scale), cy + int(152 * scale))
    ], fill=(15, 23, 42, 255))

# ------------------------------------------------------------------------------
# 1. OPTION 1A: NUGIPROPERTI — 3D BUILDING (Dark Canvas / Transparent for Instagram & Dark UI)
# ------------------------------------------------------------------------------
def generate_option1_dark(width=2400, height=600):
    canvas = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)

    draw_3d_building_icon(draw, cx=260, cy=300, scale=1.0, accent_color=C_CYAN)

    font_main = load_font(210, bold=True)
    text_x = 480
    text_y = 195

    draw.text((text_x, text_y), "NUGI", fill=C_WHITE, font=font_main)
    w_nugi = draw.textlength("NUGI", font=font_main)
    draw.text((text_x + w_nugi + 10, text_y), "PROPERTI", fill=C_CYAN, font=font_main)

    return canvas

# ------------------------------------------------------------------------------
# 2. OPTION 1B: NUGIPROPERTI — 3D BUILDING (Light Canvas / Transparent for Invoices & Docs)
# ------------------------------------------------------------------------------
def generate_option1_light(width=2400, height=600):
    canvas = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)

    draw_3d_building_icon(draw, cx=260, cy=300, scale=1.0, accent_color=C_CYAN_DARK)

    font_main = load_font(210, bold=True)
    text_x = 480
    text_y = 195

    draw.text((text_x, text_y), "NUGI", fill=C_DARK_SLATE, font=font_main)
    w_nugi = draw.textlength("NUGI", font=font_main)
    draw.text((text_x + w_nugi + 10, text_y), "PROPERTI", fill=C_CYAN_DARK, font=font_main)

    return canvas

# ------------------------------------------------------------------------------
# 3. OPTION 2: EDITORIAL CHEVRON APEX (Signature Violet & White — Design DNA)
# ------------------------------------------------------------------------------
def generate_option2_violet(width=2500, height=650):
    canvas = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)

    cx = 260
    cy = 320

    # Geometric Chevron / Apex Shield
    draw.polygon([
        (cx - 130, cy - 110),
        (cx, cy + 130),
        (cx + 130, cy - 110),
        (cx + 70, cy - 110),
        (cx, cy + 35),
        (cx - 70, cy - 110)
    ], fill=C_VIOLET)

    # Modern Central Skyscraper Spire
    draw.polygon([
        (cx - 30, cy - 140),
        (cx + 30, cy - 140),
        (cx + 30, cy - 15),
        (cx, cy + 25),
        (cx - 30, cy - 15)
    ], fill=C_WHITE)

    font_main = load_font(210, bold=True)
    font_sub = load_font(38, bold=True)
    text_x = 480
    text_y = 190

    draw.text((text_x, text_y), "NUGI", fill=C_WHITE, font=font_main)
    w_nugi = draw.textlength("NUGI", font=font_main)
    draw.text((text_x + w_nugi + 12, text_y), "PROPERTI", fill=C_VIOLET, font=font_main)

    draw.text((text_x + 6, text_y + 240), "PROPERTY MARKETING & AUTOMATION SYSTEM", fill=C_SLATE_MUTED, font=font_sub)

    return canvas

# ------------------------------------------------------------------------------
# 4. OPTION 3: HYBRID TECH & PROPERTY MONOGRAM (Cyan + Violet)
# ------------------------------------------------------------------------------
def generate_option3_monogram(width=2500, height=650):
    canvas = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)

    cx = 260
    cy = 320

    # Left Skyscraper Pillar (Cyan)
    draw.rounded_rectangle([cx - 120, cy - 130, cx - 55, cy + 130], radius=10, fill=C_CYAN)
    
    # Diagonal Software / Speed Bridge (Gradient violet)
    draw.polygon([
        (cx - 55, cy - 130),
        (cx + 55, cy + 70),
        (cx + 55, cy + 130),
        (cx - 55, cy - 70)
    ], fill=C_VIOLET)

    # Right Skyscraper Tower (White)
    draw.rounded_rectangle([cx + 55, cy - 170, cx + 120, cy + 130], radius=10, fill=C_WHITE)

    # Windows
    for y in range(cy - 100, cy + 110, 40):
        draw.rectangle([cx - 105, y, cx - 75, y + 18], fill=(12, 74, 110, 220))
        draw.rectangle([cx + 75, y, cx + 105, y + 18], fill=(148, 163, 184, 220))

    font_main = load_font(210, bold=True)
    font_sub = load_font(38, bold=True)
    text_x = 480
    text_y = 190

    draw.text((text_x, text_y), "NUGI", fill=C_WHITE, font=font_main)
    w_nugi = draw.textlength("NUGI", font=font_main)
    draw.text((text_x + w_nugi + 12, text_y), "PROPERTI", fill=C_CYAN, font=font_main)

    draw.text((text_x + 6, text_y + 240), "AI SOFTWARE & CONVERSION INTELLIGENCE", fill=C_SLATE_MUTED, font=font_sub)

    return canvas

# ------------------------------------------------------------------------------
# 5. OPTION 4: FREELANCE AI SOFTWARE STUDIO (For B2B Tech Entity)
# ------------------------------------------------------------------------------
def generate_option4_studio(width=2600, height=650):
    canvas = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)

    cx = 260
    cy = 320

    # Hexagonal Node
    r = 135
    pts = [
        (cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)))
        for a in range(30, 390, 60)
    ]
    draw.polygon(pts, outline=C_CYAN, width=10)

    # Code Brackets
    f_sym = load_font(150, bold=True)
    draw.text((cx - 85, cy - 115), "{", fill=C_VIOLET, font=f_sym)
    draw.text((cx + 35, cy - 115), "}", fill=C_CYAN, font=f_sym)
    draw.rectangle([cx - 18, cy - 50, cx + 18, cy + 50], fill=C_WHITE)

    font_main = load_font(190, bold=True)
    font_sub = load_font(38, bold=True)
    text_x = 480
    text_y = 190

    draw.text((text_x, text_y), "NUGI", fill=C_WHITE, font=font_main)
    w_nugi = draw.textlength("NUGI", font=font_main)
    draw.text((text_x + w_nugi + 15, text_y), "SOFTWARE", fill=C_CYAN, font=font_main)

    draw.text((text_x + 6, text_y + 230), "AI AUTOMATION • WHATSAPP SYSTEMS • PROPERTY CRM", fill=C_SLATE_MUTED, font=font_sub)

    return canvas

# ------------------------------------------------------------------------------
# 6. OPTION 5: HIGH-RES 1:1 SQUARE APP ICON / PROFILE AVATAR (1024x1024)
# ------------------------------------------------------------------------------
def generate_option5_avatar(size=1024):
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)

    cx, cy = size // 2, size // 2

    # Obsidian Rounded Shield
    pad = 60
    draw.rounded_rectangle([pad, pad, size - pad, size - pad], radius=180, fill=C_BG_OBSIDIAN, outline=C_VIOLET, width=12)

    # 3D Building Tower Center
    draw_3d_building_icon(draw, cx=cx, cy=cy, scale=2.0, accent_color=C_CYAN)

    return canvas

# ------------------------------------------------------------------------------
# 7. SHOWCASE PRESENTATION CARD (Dark Studio Canvas for Comparison)
# ------------------------------------------------------------------------------
def generate_showcase_sheet():
    w, h = 2400, 3200
    card = Image.new("RGBA", (w, h), (7, 11, 20, 255))
    draw = ImageDraw.Draw(card)

    # Header
    f_title = load_font(84, bold=True)
    f_sub = load_font(40, bold=False)
    f_label = load_font(36, bold=True)
    f_desc = load_font(28, bold=False)

    draw.text((120, 90), "NUGIPROPERTI & NUGI STUDIO — BRAND LOGO SUITE", fill=C_WHITE, font=f_title)
    draw.text((120, 195), "Transparent PNG Assets • Matching Nugi Content Factory Editorial Design DNA", fill=C_CYAN, font=f_sub)
    draw.line([(120, 260), (w - 120, 260)], fill=(255, 255, 255, 30), width=2)

    # Master full options
    opt1 = generate_option1_dark()
    opt2 = generate_option2_violet()
    opt3 = generate_option3_monogram()
    opt4 = generate_option4_studio()
    opt5 = generate_option5_avatar()

    sections = [
        ("OPSI 1: MODERN ISOMETRIC PROPERTY (Exact Reference Upgraded)",
         "Ideal untuk Brand Properti, Instagram Feed, Header Editorial, & Banner Iklan.",
         opt1, 300),

        ("OPSI 2: EDITORIAL CYBER-CHEVRON (Nugi Content Factory Design DNA)",
         "Matching 100% dengan style Akademi Kripto / Neon Violet highlight strip & header chevron.",
         opt2, 850),

        ("OPSI 3: HYBRID MONOGRAM 'N' + SKYLINE (Dual Cyan & Violet)",
         "Kombinasi otoritas properti (gedung) dan kecerdasan software AI (jembatan data diagonal).",
         opt3, 1400),

        ("OPSI 4: NUGI SOFTWARE STUDIO (B2B Tech Consulting & CRM Automation)",
         "Khusus untuk portofolio freelance, penawaran jasa custom software, WhatsApp bot, & web apps.",
         opt4, 1950),

        ("OPSI 5: SQUARE APP ICON / AVATAR (1024x1024 Profile Picture)",
         "Format 1:1 siap pakai untuk Foto Profil Instagram, WhatsApp Business, dan Website Favicon.",
         opt5, 2500)
    ]

    for title, desc, img, y_pos in sections[:4]:
        # Glass card backing
        draw.rounded_rectangle([120, y_pos, w - 120, y_pos + 500], radius=24, fill=(15, 23, 42, 220), outline=(255, 255, 255, 30), width=2)
        draw.text((160, y_pos + 35), title, fill=C_WHITE, font=f_label)
        draw.text((160, y_pos + 85), desc, fill=C_SLATE_MUTED, font=f_desc)
        
        # Scale to fit width 1900 while maintaining aspect ratio
        scale = 1900 / img.width
        target_w = 1900
        target_h = int(img.height * scale)
        scaled_img = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
        
        card.paste(scaled_img, (160, y_pos + 135), scaled_img)

    # Option 5 at bottom
    y_pos = 2500
    draw.rounded_rectangle([120, y_pos, w - 120, y_pos + 500], radius=24, fill=(15, 23, 42, 220), outline=(255, 255, 255, 30), width=2)
    draw.text((160, y_pos + 35), sections[4][0], fill=C_WHITE, font=f_label)
    draw.text((160, y_pos + 85), sections[4][1], fill=C_SLATE_MUTED, font=f_desc)
    
    scaled_av = opt5.resize((320, 320), Image.Resampling.LANCZOS)
    card.paste(scaled_av, (160, y_pos + 140), scaled_av)
    
    # Text beside avatar
    draw.text((540, y_pos + 170), "NUGIPROPERTI APP ICON & AVATAR", fill=C_WHITE, font=f_label)
    draw.text((540, y_pos + 225), "High-res 1024x1024 PNG dengan rounded obsidian shield & neon border.", fill=C_CYAN, font=f_desc)
    draw.text((540, y_pos + 270), "Dirancang tahan terhadap circular crop Instagram & WhatsApp.", fill=C_SLATE_MUTED, font=f_desc)

    return card

# ------------------------------------------------------------------------------
# SAVE ALL ASSETS
# ------------------------------------------------------------------------------
files = {
    "01_nugi_properti_logo_transparent_dark_bg.png": generate_option1_dark(),
    "01_nugi_properti_logo_transparent_light_bg.png": generate_option1_light(),
    "02_nugi_properti_logo_editorial_violet.png": generate_option2_violet(),
    "03_nugi_properti_logo_hybrid_monogram.png": generate_option3_monogram(),
    "04_nugi_software_studio_logo_tech.png": generate_option4_studio(),
    "05_nugi_brand_avatar_1024x1024.png": generate_option5_avatar(),
    "nugi_brand_logo_suite_showcase.png": generate_showcase_sheet()
}

for name, img in files.items():
    for target in [DIR_FREELANCE, DIR_CONTENT_FACTORY, DIR_SCRATCH]:
        p = target / name
        img.save(p, format="PNG", optimize=True)
    print(f"Exported: {name}")

print("\nAll brand logo variations saved successfully.")
