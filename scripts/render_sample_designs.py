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
                topic="Kenapa leads iklan properti banyak tapi closing tetap rendah?",
                target_audience="Developer & Sales Manager Properti"
            )
        },
        # 2. Numbered Listicle (NUMBER_LIST)
        {
            "filename": "sample_02_editorial_dna_number_list_1080x1350.png",
            "brief": UserBriefInput(
                topic="3 kesalahan fatal follow-up yang membuat calon pembeli properti hilang",
                target_audience="Tim Sales & Marketing Properti"
            )
        },
        # 3. Market Insight (PROPERTY_INSIGHT)
        {
            "filename": "sample_03_editorial_dna_market_insight_1080x1350.png",
            "brief": UserBriefInput(
                topic="Kenapa harga rumah di dekat akses tol bisa naik lebih cepat?",
                target_audience="Investor & Calon Pembeli Properti"
            )
        },
        # 4. Empirical Case Study (CASE_STUDY)
        {
            "filename": "sample_04_editorial_dna_case_study_1080x1350.png",
            "brief": UserBriefInput(
                topic="Studi kasus hasil transformasi response time tim sales properti",
                target_audience="Principal Agen & Direktur Marketing"
            )
        },
        # 5. Authoritative Opinion Column (OPINION)
        {
            "filename": "sample_05_editorial_dna_opinion_column_1080x1350.png",
            "brief": UserBriefInput(
                topic="Developer properti yang menolak otomasi pemasaran akan tertinggal",
                target_audience="Owner & Direktur Developer Properti"
            )
        },
        # 6. Architectural Unit Showcase (PROPERTY_SHOWCASE)
        {
            "filename": "sample_06_editorial_dna_rukost_showcase_1080x1350.png",
            "brief": UserBriefInput(
                topic="Unit rukost premium dekat kampus UNPAD Jatinangor siap sewa",
                target_audience="Investor Passive Income"
            )
        }
    ]

    print("=======================================================================")
    print("  RENDERING 6 PHASE 3D-1 EDITORIAL DESIGN DNA SAMPLES (1080x1350)")
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
        print(f"     Size: {img.size} | Archetype: {pkg.art_direction_spec.archetype.value} | CTA: {pkg.editorial_spec.cta_policy.value} | QA Score: {pkg.visual_qa.score}/100")
        assert img.size == (1080, 1350)
        assert pkg.visual_qa.score >= 85

    print("\n[SUCCESS] All 6 Phase 3D-1 Editorial Design DNA visual samples rendered and verified successfully!")


if __name__ == "__main__":
    run_sample_renders()
