import os
from pathlib import Path
from PIL import Image

def generate_ico():
    root_dir = Path(__file__).resolve().parent.parent.parent
    brand_dir = root_dir / "assets" / "brand"
    brand_dir.mkdir(parents=True, exist_ok=True)
    
    avatar_path = brand_dir / "nugi_properti_avatar_purple_1024x1024.png"
    if not avatar_path.exists():
        avatar_path = brand_dir / "nugi_properti_logo.png"
    
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
