import os
import shutil
from pathlib import Path

# Paths
FREELANCE_LOGO_DIR = Path("C:/Users/Nugi/Documents/Freelance Nugi jasa software engginer/assets/logo")
FREELANCE_WEBSITE_ASSETS = Path("C:/Users/Nugi/Documents/Freelance Nugi jasa software engginer/website/assets")
CONTENT_FACTORY_BRAND_DIR = Path("C:/Users/Nugi/Documents/nugi-content-factory/assets/brand")
CONTENT_FACTORY_FRONTEND_PUBLIC = Path("C:/Users/Nugi/Documents/nugi-content-factory/frontend/public")
CONTENT_FACTORY_FRONTEND_ASSETS = Path("C:/Users/Nugi/Documents/nugi-content-factory/frontend/src/assets")

for d in [FREELANCE_LOGO_DIR, FREELANCE_WEBSITE_ASSETS, CONTENT_FACTORY_BRAND_DIR, CONTENT_FACTORY_FRONTEND_PUBLIC, CONTENT_FACTORY_FRONTEND_ASSETS]:
    d.mkdir(parents=True, exist_ok=True)

# The Chosen Master Logo Source
MASTER_LOGO_SOURCE = FREELANCE_LOGO_DIR / "nugi_properti_logo_purple_transparent_dark_bg.png"
if not MASTER_LOGO_SOURCE.exists():
    MASTER_LOGO_SOURCE = Path("C:/Users/Nugi/.gemini/antigravity-ide/brain/b80f175e-f63e-4113-aca5-af8b92fed644/scratch/nugi_properti_logo_purple_transparent_dark_bg.png")

print(f"Master logo source: {MASTER_LOGO_SOURCE}")

# Target destinations for the chosen logo
targets = [
    FREELANCE_LOGO_DIR / "nugi_properti_logo_purple_transparent_dark_bg.png",
    FREELANCE_LOGO_DIR / "nugi_properti_logo.png",
    FREELANCE_WEBSITE_ASSETS / "nugi_properti_logo.png",
    CONTENT_FACTORY_BRAND_DIR / "nugi_properti_logo_purple_transparent_dark_bg.png",
    CONTENT_FACTORY_BRAND_DIR / "nugi_properti_logo.png",
    CONTENT_FACTORY_FRONTEND_PUBLIC / "nugi_properti_logo.png",
    CONTENT_FACTORY_FRONTEND_PUBLIC / "logo.png",
    CONTENT_FACTORY_FRONTEND_ASSETS / "nugi_properti_logo.png"
]

for t in targets:
    if MASTER_LOGO_SOURCE.resolve() != t.resolve():
        shutil.copy2(MASTER_LOGO_SOURCE, t)
        print(f"Copied master logo to: {t}")
    else:
        print(f"Master logo already at: {t}")

# Allowed files to keep in Freelance logo folder
allowed_freelance = {
    "nugi_properti_logo_purple_transparent_dark_bg.png",
    "nugi_properti_logo.png",
    "nugi_properti_avatar_purple_1024x1024.png" # Profile avatar
}

for f in FREELANCE_LOGO_DIR.iterdir():
    if f.is_file() and f.name not in allowed_freelance:
        f.unlink()
        print(f"Removed unused logo: {f.name} from Freelance logo folder")

# Allowed files to keep in Content Factory brand folder
allowed_factory = {
    "nugi_properti_logo_purple_transparent_dark_bg.png",
    "nugi_properti_logo.png",
    "nugi_properti_avatar_purple_1024x1024.png"
}

for f in CONTENT_FACTORY_BRAND_DIR.iterdir():
    if f.is_file() and f.name not in allowed_factory:
        f.unlink()
        print(f"Removed unused logo: {f.name} from Content Factory brand folder")

print("\nCleanup and distribution complete!")
