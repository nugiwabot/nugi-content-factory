import os
from pathlib import Path
from PIL import Image

def generate_ico():
    brand_dir = Path("c:/Users/Nugi/Documents/nugi-content-factory/assets/brand")
    brand_dir.mkdir(parents=True, exist_ok=True)
    
    avatar_path = brand_dir / "nugi_properti_avatar_purple_1024x1024.png"
    if not avatar_path.exists():
        # Fallback to scratch or logo
        avatar_path = Path("c:/Users/Nugi/.gemini/antigravity-ide/brain/b80f175e-f63e-4113-aca5-af8b92fed644/scratch/nugi_properti_avatar_purple_1024x1024.png")
    
    img = Image.open(avatar_path).convert("RGBA")
    
    ico_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    target_ico = brand_dir / "app.ico"
    
    img.save(
        target_ico,
        format="ICO",
        sizes=ico_sizes
    )
    print(f"Generated multi-resolution Windows Icon at: {target_ico}")

if __name__ == "__main__":
    generate_ico()
