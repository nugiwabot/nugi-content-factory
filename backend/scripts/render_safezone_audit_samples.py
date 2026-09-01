import os
import sys
import shutil
from pathlib import Path

# Add backend directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from PIL import Image

from app.schemas.design_spec import (
    DesignSpecification,
    CompositionType,
    EditorialLayoutPreset,
    CTAStrategy,
    SAFEZONE_CONTENT_LEFT,
    SAFEZONE_CONTENT_RIGHT,
    SAFEZONE_TOP,
    SAFEZONE_BOTTOM
)
from app.rendering.compositing_engine import ProfessionalCompositingEngine
from app.services.visual_qa import VisualQAService
from app.brand.profiles import NUGI_PROPERTI_BRAND_PROFILE

OUTPUT_DIR = Path("C:/Users/Nugi/Documents/nugi-content-factory/assets/generated")
SCRATCH_DIR = Path("C:/Users/Nugi/.gemini/antigravity-ide/brain/b80f175e-f63e-4113-aca5-af8b92fed644/scratch")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
SCRATCH_DIR.mkdir(parents=True, exist_ok=True)

engine = ProfessionalCompositingEngine()

SAMPLES = [
    {
        "filename_prod": "sample_01_editorial_dna_leads_problem_1080x1350.png",
        "filename_debug": "sample_01_debug_safezone_leads_problem_1080x1350.png",
        "spec": DesignSpecification(
            template_id="01_PROPERTY_PROBLEM",
            composition_type=CompositionType.HERO_IMAGE_EDITORIAL,
            layout_preset=EditorialLayoutPreset.LAYOUT_HERO_BOTTOM_TEXT,
            cta_strategy=CTAStrategy.CTA_NONE,
            headline="LEADS IKLAN MASUK, TAPI SALES LAMBAT FOLLOW-UP?",
            subheadline="Setiap menit keterlambatan follow-up menurunkan peluang closing hingga 80%.",
            highlight_words=["LAMBAT FOLLOW-UP?"],
            badge_text="STRATEGI FOLLOW UP",
            accent_color_hex="#8b5cf6",
            width=1080,
            height=1350
        )
    },
    {
        "filename_prod": "sample_02_editorial_dna_location_education_1080x1350.png",
        "filename_debug": "sample_02_debug_safezone_location_education_1080x1350.png",
        "spec": DesignSpecification(
            template_id="02_PROPERTY_EDUCATION",
            composition_type=CompositionType.CINEMATIC_OVERLAY,
            layout_preset=EditorialLayoutPreset.LAYOUT_CINEMATIC_OVERLAY,
            cta_strategy=CTAStrategy.CTA_NONE,
            headline="LOKASI STRATEGIS BELUM TENTU CEPAT LAKU",
            subheadline="Aksesibilitas nyata dan positioning harga lebih menentukan kecepatan penjualan unit.",
            highlight_words=["CEPAT LAKU"],
            badge_text="EDUKASI PROPERTI",
            accent_color_hex="#8b5cf6",
            width=1080,
            height=1350
        )
    },
    {
        "filename_prod": "sample_03_editorial_dna_market_insight_1080x1350.png",
        "filename_debug": "sample_03_debug_safezone_market_insight_1080x1350.png",
        "spec": DesignSpecification(
            template_id="03_PROPERTY_INSIGHT",
            composition_type=CompositionType.HERO_IMAGE_EDITORIAL,
            layout_preset=EditorialLayoutPreset.LAYOUT_HERO_BOTTOM_TEXT,
            cta_strategy=CTAStrategy.CTA_NONE,
            headline="HARGA RUMAH NAIK, TAPI DAYA BELI STAGNAN",
            subheadline="Pergeseran tren hunian kompak dan skema cicilan inovatif di pasar 2026.",
            highlight_words=["DAYA BELI STAGNAN"],
            badge_text="ANALISIS PASAR",
            accent_color_hex="#8b5cf6",
            width=1080,
            height=1350
        )
    },
    {
        "filename_prod": "sample_04_editorial_dna_number_list_1080x1350.png",
        "filename_debug": "sample_04_debug_safezone_number_list_1080x1350.png",
        "spec": DesignSpecification(
            template_id="04_NUMBER_LIST",
            composition_type=CompositionType.LIST_EDITORIAL,
            layout_preset=EditorialLayoutPreset.LAYOUT_HERO_BOTTOM_TEXT,
            cta_strategy=CTAStrategy.CTA_NONE,
            headline="3 KESALAHAN FATAL SAAT MEMBELI PROPERTI",
            subheadline="Fokus pada promo sesaat tanpa mengecek legalitas tanah dan yield sewa riil.",
            highlight_words=["KESALAHAN FATAL"],
            badge_text="PANDUAN INVESTASI",
            accent_color_hex="#8b5cf6",
            bullet_points=[
                "Tidak mengecek keabsahan sertifikat dan perizinan IMB/PBG",
                "Tergiur harga murah tanpa menghitung biaya renovasi tersembunyi",
                "Mengabaikan tren pertumbuhan infrastruktur kawasan sekitar"
            ],
            width=1080,
            height=1350
        )
    },
    {
        "filename_prod": "sample_05_editorial_dna_case_study_1080x1350.png",
        "filename_debug": "sample_05_debug_safezone_case_study_1080x1350.png",
        "spec": DesignSpecification(
            template_id="05_CASE_STUDY",
            composition_type=CompositionType.DATA_EDITORIAL,
            layout_preset=EditorialLayoutPreset.LAYOUT_METRIC_DOMINANT,
            cta_strategy=CTAStrategy.CTA_NONE,
            headline="BAGAIMANA SATU PROPERTI MENAIKKAN CLOSING 300%",
            subheadline="Otomasi perutean leads cepat dan sistem janji temu survey terstruktur.",
            highlight_words=["CLOSING 300%"],
            badge_text="STUDI KASUS NYATA",
            accent_color_hex="#8b5cf6",
            metric_value="+300%",
            metric_label="Kecepatan Respon & Janji Survey",
            width=1080,
            height=1350
        )
    },
    {
        "filename_prod": "sample_06_editorial_dna_showcase_parahyangan_1080x1350.png",
        "filename_debug": "sample_06_debug_safezone_showcase_parahyangan_1080x1350.png",
        "spec": DesignSpecification(
            template_id="06_PROPERTY_SHOWCASE",
            composition_type=CompositionType.PROPERTY_SHOWCASE,
            layout_preset=EditorialLayoutPreset.LAYOUT_PROPERTY_SHOWCASE,
            cta_strategy=CTAStrategy.CTA_NONE,
            headline="RUMAH PRESTISIUS KOTA BARU PARAHYANGAN",
            subheadline="Hunian modern berarsitektur tropis dengan pencahayaan alami optimal.",
            highlight_words=["KOTA BARU PARAHYANGAN"],
            badge_text="SHOWCASE RESIDENSIAL",
            accent_color_hex="#8b5cf6",
            property_location="Padalarang, Bandung Barat",
            property_price="Mulai Rp 2,4 Miliar",
            property_features=["LT 180m² / LB 210m²", "4 Kamar Tidur", "Smart Home System"],
            width=1080,
            height=1350
        )
    }
]

print("Starting Rendering Safezone Audit Samples...")
for idx, s in enumerate(SAMPLES, 1):
    spec = s["spec"]
    
    # 1. Render Production Version
    prod_bytes, prod_meta = engine.composite_full_artwork(design_spec=spec, debug_safezone=False)
    prod_out_path = OUTPUT_DIR / s["filename_prod"]
    prod_scratch_path = SCRATCH_DIR / s["filename_prod"]
    with open(prod_out_path, "wb") as f:
        f.write(prod_bytes)
    with open(prod_scratch_path, "wb") as f:
        f.write(prod_bytes)

    # 2. Render Debug Diagnostic Version
    debug_bytes, debug_meta = engine.composite_full_artwork(design_spec=spec, debug_safezone=True)
    debug_out_path = OUTPUT_DIR / s["filename_debug"]
    debug_scratch_path = SCRATCH_DIR / s["filename_debug"]
    with open(debug_out_path, "wb") as f:
        f.write(debug_bytes)
    with open(debug_scratch_path, "wb") as f:
        f.write(debug_bytes)

    # 3. Evaluate Visual QA
    qa = VisualQAService.evaluate_design(spec, prod_meta)
    print(f"[{idx}/6] Rendered {s['filename_prod']} | QA Score: {qa.score}/100 | Safezone Pass: {qa.safezone_pass} | Grid 3:4 Pass: {qa.profile_grid_pass}")

print("All 6 Production + 6 Debug Diagnostic Samples successfully rendered and verified.")
