import os
import sys
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

from app.rendering.editorial_renderer import EditorialRenderer
from app.schemas.design_spec import (
    DesignSpecification,
    CompositionType,
    CTAStrategy,
    ImageStrategy,
    OverlayStrategy
)
from app.services.visual_qa import VisualQAService
from PIL import Image
import io


def run_sample_renders():
    output_dir = Path(__file__).resolve().parent.parent / "assets" / "generated"
    output_dir.mkdir(parents=True, exist_ok=True)
    renderer = EditorialRenderer()

    samples = [
        # 1. Property Educational Article (HERO_IMAGE_EDITORIAL, CTA_NONE)
        {
            "filename": "sample_01_property_education_hero_1080x1350.png",
            "spec": DesignSpecification(
                composition_type=CompositionType.HERO_IMAGE_EDITORIAL,
                width=1080,
                height=1350,
                headline="KENAPA HARGA RUMAH DI DEKAT TOL BISA NAIK LEBIH CEPAT?",
                highlight_words=["HARGA RUMAH", "NAIK LEBIH CEPAT"],
                subheadline="Lokasi bukan hanya soal jarak. Aksesibilitas, aktivitas ekonomi, dan perkembangan kawasan ikut memengaruhi nilai apresiasi properti.",
                badge_text="EDUKASI PROPERTI",
                cta_strategy=CTAStrategy.CTA_NONE # Strictly NO CTA for Educational Articles
            )
        },
        # 2. Property Market Insight (CINEMATIC_OVERLAY, CTA_NONE)
        {
            "filename": "sample_02_property_insight_overlay_1080x1350.png",
            "spec": DesignSpecification(
                composition_type=CompositionType.CINEMATIC_OVERLAY,
                width=1080,
                height=1350,
                headline="BIAYA IKLAN PROPERTI MAHAL BUKAN KARENA ALGORITMA META",
                highlight_words=["BUKAN KARENA ALGORITMA"],
                subheadline="Penyebab utama CPA membengkak adalah penawaran unit yang generik dan respons follow-up tim sales yang lambat di atas 30 menit.",
                badge_text="MARKET INTELLIGENCE",
                cta_strategy=CTAStrategy.CTA_NONE
            )
        },
        # 3. Property Listicle (LIST_EDITORIAL, CTA_NONE)
        {
            "filename": "sample_03_property_listicle_1080x1350.png",
            "spec": DesignSpecification(
                composition_type=CompositionType.LIST_EDITORIAL,
                width=1080,
                height=1350,
                headline="5 KESALAHAN FATAL FOLLOW-UP LEADS PROPERTI",
                highlight_words=["KESALAHAN FATAL"],
                bullet_points=[
                    "Respon di atas 15 menit menurunkan closing hingga 80%",
                    "Template pesan chat kaku tanpa personalisasi nama calon pembeli",
                    "Tidak mengunci janji temu survey lokasi yang spesifik",
                    "Menyerah setelah hanya satu kali follow up tanpa follow up kedua"
                ],
                badge_text="POIN KRUSIAL",
                cta_strategy=CTAStrategy.CTA_NONE
            )
        },
        # 4. Property Case Study / Data (DATA_EDITORIAL, CTA_NONE)
        {
            "filename": "sample_04_property_case_study_data_1080x1350.png",
            "spec": DesignSpecification(
                composition_type=CompositionType.DATA_EDITORIAL,
                width=1080,
                height=1350,
                headline="HASIL TRANSFORMASI RESPONSE TIME GREN PROPERTYKOST",
                highlight_words=["TRANSFORMASI RESPONSE TIME"],
                metric_value="+300%",
                metric_label="Kecepatan Respon & Janji Survey Prospek",
                subheadline="Penerapan sistem routing pesan instan berhasil meningkatkan konversi janji survey mahasiswa sebesar 300% dalam 60 hari.",
                badge_text="STUDI KASUS & HASIL",
                cta_strategy=CTAStrategy.CTA_NONE
            )
        },
        # 5. Property Showcase (PROPERTY_SHOWCASE, CTA_OPTIONAL)
        {
            "filename": "sample_05_property_showcase_1080x1350.png",
            "spec": DesignSpecification(
                composition_type=CompositionType.PROPERTY_SHOWCASE,
                width=1080,
                height=1350,
                headline="RUKOST PREMIUM DEKAT KAMPUS UNPAD JATINANGOR",
                highlight_words=["RUKOST PREMIUM", "UNPAD JATINANGOR"],
                property_location="Jatinangor, Sumedang",
                property_price="Mulai Rp 1,85 Miliar",
                property_features=["16 Kamar Kost", "Yield 12%/thn", "SHM Siap", "Full Furnished"],
                badge_text="PORTFOLIO UNIT",
                cta_strategy=CTAStrategy.CTA_OPTIONAL,
                cta_text="Jadwalkan Survey →"
            )
        },
        # 6. Property Opinion & Perspective (MINIMAL_EDITORIAL, CTA_NONE)
        {
            "filename": "sample_06_property_opinion_minimal_1080x1350.png",
            "spec": DesignSpecification(
                composition_type=CompositionType.MINIMAL_EDITORIAL,
                width=1080,
                height=1350,
                headline="DEVELOPER YANG MENOLAK OTOMASI MARKETING AKAN TERGANTIKAN OLEH YANG MEMANFAATKANNYA",
                highlight_words=["OTOMASI MARKETING"],
                subheadline="Pasar properti generasi baru membutuhkan respons instan, transparansi data, dan pengalaman digital yang mulus sejak detik pertama.",
                author_name="Tim Riset NugiProperti",
                badge_text="PERSPEKTIF",
                cta_strategy=CTAStrategy.CTA_NONE
            )
        }
    ]

    print("==================================================")
    print("  RENDERING 6 EDITORIAL VISUAL SAMPLES (1080x1350)")
    print("==================================================")

    for item in samples:
        spec = item["spec"]
        png_bytes, meta = renderer.render(spec)
        out_path = output_dir / item["filename"]
        with open(out_path, "wb") as f:
            f.write(png_bytes)

        qa = VisualQAService.evaluate_design(spec, meta)

        # Verify image properties with Pillow
        img = Image.open(io.BytesIO(png_bytes))
        print(f"[OK] [{spec.composition_type.value}] -> {item['filename']}")
        print(f"     Size: {img.size} (1080x1350) | CTA: {spec.cta_strategy.value} | Latency: {meta['render_latency_ms']}ms | QA Score: {qa.score}/100 ({qa.readability})")
        assert img.size == (1080, 1350)
        assert qa.score >= 85

    print("\n[SUCCESS] All 6 Phase 3A Editorial samples rendered and verified successfully!")


if __name__ == "__main__":
    run_sample_renders()
