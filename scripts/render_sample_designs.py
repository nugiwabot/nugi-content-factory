import os
import sys
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

from app.schemas.editorial_agent import UserBriefInput, ContentType
from app.services.content_generation_agent import ContentGenerationAgent
from app.providers.factory import ProviderFactory
from PIL import Image
import io


def run_sample_renders():
    output_dir = Path(__file__).resolve().parent.parent / "assets" / "generated"
    output_dir.mkdir(parents=True, exist_ok=True)
    agent = ContentGenerationAgent()

    briefs = [
        # 1. Problem Scene
        {
            "filename": "sample_01_composite_leads_problem_1080x1350.png",
            "brief": UserBriefInput(
                topic="Kenapa leads iklan properti banyak tapi closing tetap rendah?",
                target_audience="Developer & Sales Manager Properti"
            )
        },
        # 2. Listicle
        {
            "filename": "sample_02_composite_followup_mistakes_1080x1350.png",
            "brief": UserBriefInput(
                topic="3 kesalahan follow-up yang membuat calon pembeli hilang",
                target_audience="Tim Sales & Marketing Properti"
            )
        },
        # 3. Market Insight & Infrastructure
        {
            "filename": "sample_03_composite_housing_price_trend_1080x1350.png",
            "brief": UserBriefInput(
                topic="Apakah harga rumah akan terus naik?",
                target_audience="Investor & Calon Pembeli Properti"
            )
        },
        # 4. Education: Location vs Size
        {
            "filename": "sample_04_composite_location_vs_size_1080x1350.png",
            "brief": UserBriefInput(
                topic="Kenapa lokasi lebih penting daripada luas bangunan?",
                target_audience="Pembeli Rumah Pertama & Investor"
            )
        },
        # 5. Case Study: Automated Routing
        {
            "filename": "sample_05_composite_auto_leads_routing_1080x1350.png",
            "brief": UserBriefInput(
                topic="Bagaimana sistem otomatis membagi leads ke sales?",
                target_audience="Principal Agen & Direktur Marketing"
            )
        },
        # 6. Showcase & Investment Cashflow
        {
            "filename": "sample_06_composite_cashflow_vs_capital_gain_1080x1350.png",
            "brief": UserBriefInput(
                topic="Property investment: cash flow vs capital gain",
                target_audience="Investor Rukost Mahasiswa"
            )
        }
    ]

    print("==================================================================")
    print("  RENDERING 6 PHASE 3C COMPOSITE EDITORIAL SAMPLES (1080x1350)")
    print("==================================================================")

    for item in briefs:
        brief = item["brief"]
        pkg = agent.generate_full_package(brief=brief)

        # Read rendered bytes from storage provider
        storage = ProviderFactory.get_storage_provider()
        png_bytes = storage.read(pkg.rendered_asset_path)

        out_path = output_dir / item["filename"]
        with open(out_path, "wb") as f:
            f.write(png_bytes)

        img = Image.open(io.BytesIO(png_bytes))
        print(f"[OK] [{pkg.content_type.value}] -> {item['filename']}")
        print(f"     Size: {img.size} | Archetype: {pkg.art_direction_spec.archetype.value} | CTA: {pkg.editorial_spec.cta_policy.value} | QA Score: {pkg.visual_qa.score}/100")
        assert img.size == (1080, 1350)
        assert pkg.visual_qa.score >= 85

    print("\n[SUCCESS] All 6 Phase 3C Layered Composite visual samples rendered and verified successfully!")


if __name__ == "__main__":
    run_sample_renders()
