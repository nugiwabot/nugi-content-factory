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
        # 1. Problem Scene (PROPERTY_PROBLEM)
        {
            "filename": "sample_01_editorial_dna_leads_problem_1080x1350.png",
            "brief": UserBriefInput(
                topic="Leads iklan masuk, tapi sales lambat follow-up?",
                target_audience="Developer & Sales Manager Properti"
            )
        },
        # 2. Educational Scene (PROPERTY_EDUCATION)
        {
            "filename": "sample_02_editorial_dna_location_education_1080x1350.png",
            "brief": UserBriefInput(
                topic="Kenapa properti di lokasi bagus belum tentu cepat laku?",
                target_audience="Developer & Tim Marketing Properti"
            )
        },
        # 3. Market Insight (PROPERTY_INSIGHT)
        {
            "filename": "sample_03_editorial_dna_market_insight_1080x1350.png",
            "brief": UserBriefInput(
                topic="Harga rumah naik, tapi daya beli tidak ikut naik.",
                target_audience="Investor & Pengamat Properti"
            )
        },
        # 4. Numbered Listicle (NUMBER_LIST)
        {
            "filename": "sample_04_editorial_dna_number_list_1080x1350.png",
            "brief": UserBriefInput(
                topic="3 Kesalahan Saat Membeli Properti Pertama",
                target_audience="First Time Home Buyers & Investor Pemula"
            )
        },
        # 5. Empirical Case Study (CASE_STUDY)
        {
            "filename": "sample_05_editorial_dna_case_study_1080x1350.png",
            "brief": UserBriefInput(
                topic="Bagaimana satu properti meningkatkan conversion rate 300%",
                target_audience="Principal Agen & Direktur Marketing"
            )
        },
        # 6. Architectural Unit Showcase (PROPERTY_SHOWCASE)
        {
            "filename": "sample_06_editorial_dna_showcase_parahyangan_1080x1350.png",
            "brief": UserBriefInput(
                topic="Rumah Premium Dekat Kota Baru Parahyangan",
                target_audience="Calon Pembeli Rumah Mewah Bandung"
            )
        }
    ]

    print("=======================================================================")
    print("  RENDERING 6 PHASE 3D-2 EDITORIAL SAFEZONE SAMPLES (1080x1350)")
    print("=======================================================================")

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
        print(f"     Size: {img.size} | Quality: {pkg.visual_qa.overall_quality} | Tech: {pkg.visual_qa.technical_pass} | Design: {pkg.visual_qa.design_pass} | Editorial: {pkg.visual_qa.editorial_pass} | Brand: {pkg.visual_qa.brand_pass} | Score: {pkg.visual_qa.score}/100")
        assert img.size == (1080, 1350)
        assert pkg.visual_qa.score >= 85
        assert pkg.visual_qa.safe_area_compliant is True

    print("\n[SUCCESS] All 6 Phase 3D-2 Editorial Safezone visual samples rendered and verified successfully!")


if __name__ == "__main__":
    run_sample_renders()
