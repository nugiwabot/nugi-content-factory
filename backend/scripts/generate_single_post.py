import os
import sys
import shutil
from pathlib import Path

backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from app.core.config import settings
from app.schemas.editorial_agent import UserBriefInput, ContentType
from app.services.content_generation_agent import ContentGenerationAgent
from app.providers.factory import ProviderFactory

def main():
    print("==================================================")
    print("NUGI CONTENT FACTORY — LIVE EDITORIAL GENERATION")
    print("==================================================")
    print(f"LLM Provider   : {settings.LLM_PROVIDER}")
    print(f"Image Provider : {settings.IMAGE_PROVIDER}")
    print(f"OpenRouter URL : {settings.OPENROUTER_BASE_URL}")
    print(f"Flux Endpoint  : {settings.FLUX_BASE_URL}")
    print("--------------------------------------------------")

    # Property topic for live generation
    brief = UserBriefInput(
        topic="5 Kesalahan Fatal Follow-Up Leads Properti",
        target_audience="Tim sales properti & koordinator marketing",
        content_type_override=ContentType.PROPERTY_PROBLEM,
        key_information="Hindari pola komunikasi kaku, keterlambatan first response >10 menit, dan follow-up tanpa penawaran solusi spesifik.",
        brand_name="NugiProperti"
    )

    print(f"Generating content for topic: '{brief.topic}'...")
    agent = ContentGenerationAgent()

    # Generate full package
    package = agent.generate_full_package(
        brief=brief,
        db=None,
        image_provider_type=settings.IMAGE_PROVIDER,
        debug_safezone=False
    )

    print("\n--------------------------------------------------")
    print("GENERATION SUCCESSFUL!")
    print("--------------------------------------------------")
    print(f"Headline      : {package.editorial_spec.headline}")
    print(f"Subheadline   : {package.editorial_spec.subheadline}")
    print(f"Content Type  : {package.editorial_spec.content_type}")
    print(f"Highlight Word: {package.editorial_spec.highlight_words}")
    print(f"Visual Concept: {package.concept_spec.get('concept_title', 'N/A') if package.concept_spec else 'N/A'}")
    print(f"Image Prompt  : {package.art_direction_spec.image_prompt[:120]}...")
    if package.visual_qa:
        print(f"Visual QA     : Score {package.visual_qa.score}/100 | Safezone Pass: {package.visual_qa.safezone_pass}")

    # Output file paths
    output_dir = Path("C:/Users/Nugi/Documents/nugi-content-factory/assets/generated")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    scratch_dir = Path("C:/Users/Nugi/.gemini/antigravity-ide/brain/b80f175e-f63e-4113-aca5-af8b92fed644/scratch")
    scratch_dir.mkdir(parents=True, exist_ok=True)

    filename = "nugi_properti_live_generated_rumah_hook_1080x1350.png"
    out_path = output_dir / filename
    scratch_path = scratch_dir / filename

    storage = ProviderFactory.get_storage_provider()
    if package.rendered_asset_path:
        data = storage.read(package.rendered_asset_path)
        with open(out_path, "wb") as f:
            f.write(data)
        with open(scratch_path, "wb") as f:
            f.write(data)
        print(f"\nSaved live generated image to:")
        print(f"- {out_path}")
        print(f"- {scratch_path}")
    else:
        print("ERROR: No rendered asset path returned.")

if __name__ == "__main__":
    main()
