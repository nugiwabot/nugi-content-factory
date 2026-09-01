import os
import sys
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

from app.rendering.template_renderer import TemplateRenderer
from app.schemas.design_spec import DesignSpecification
from app.services.visual_qa import VisualQAService
from PIL import Image
import io

def run_sample_renders():
    output_dir = Path(__file__).resolve().parent.parent / "assets" / "generated"
    output_dir.mkdir(parents=True, exist_ok=True)
    renderer = TemplateRenderer()

    samples = [
        {
            "template_id": "01_PROPERTY_PROBLEM",
            "filename": "sample_01_property_problem_1080x1350.png",
            "spec": DesignSpecification(
                template_id="01_PROPERTY_PROBLEM",
                width=1080,
                height=1350,
                headline="LEADS IKLAN MASUK, TAPI SALES LAMBAT FOLLOW-UP?",
                highlight_words=["LAMBAT FOLLOW-UP"],
                subheadline="Setiap menit keterlambatan bisa membuat prospek berpindah ke kompetitor.",
                badge_text="DILEMA SALES PROPERTI",
                cta_text="Pelajari Solusinya →"
            )
        },
        {
            "template_id": "02_PROPERTY_INSIGHT",
            "filename": "sample_02_property_insight_1080x1350.png",
            "spec": DesignSpecification(
                template_id="02_PROPERTY_INSIGHT",
                width=1080,
                height=1350,
                headline="KENAPA BIAYA IKLAN PROPERTI MAHAL TAPI CLOSING RENDAH?",
                highlight_words=["CLOSING RENDAH"],
                subheadline="Bukan iklannya yang salah, tapi funnel konversi WhatsApp yang bocor tanpa SLA follow-up.",
                badge_text="MARKET INSIGHT",
                cta_text="Simpan Postingan Ini ↗"
            )
        },
        {
            "template_id": "03_NUMBER_LIST",
            "filename": "sample_03_number_list_1080x1350.png",
            "spec": DesignSpecification(
                template_id="03_NUMBER_LIST",
                width=1080,
                height=1350,
                headline="5 KESALAHAN FATAL FOLLOW-UP LEADS PROPERTI",
                highlight_words=["KESALAHAN FATAL"],
                bullet_points=[
                    "Respon di atas 15 menit menurunkan closing 80%",
                    "Template chat kaku tanpa menyebut nama prospek",
                    "Tidak membuat janji temu survey yang spesifik",
                    "Menyerah setelah hanya satu kali follow up"
                ],
                badge_text="5 POIN KRUSIAL",
                cta_text="Baca Selengkapnya di Caption ↓"
            )
        },
        {
            "template_id": "04_CASE_STUDY",
            "filename": "sample_04_case_study_1080x1350.png",
            "spec": DesignSpecification(
                template_id="04_CASE_STUDY",
                width=1080,
                height=1350,
                headline="TRANSFORMASI RESPONSE TIME LEADS GREN PROPERTYKOST",
                highlight_words=["TRANSFORMASI RESPONSE TIME"],
                metric_value="+300% Speed",
                metric_label="Waktu Respon & Janji Survey Prospek",
                badge_text="STUDI KASUS & HASIL",
                cta_text="Konsultasi Strategi →"
            )
        },
        {
            "template_id": "05_PRODUCT_SOLUTION",
            "filename": "sample_05_product_solution_1080x1350.png",
            "spec": DesignSpecification(
                template_id="05_PRODUCT_SOLUTION",
                width=1080,
                height=1350,
                headline="OTOMASI DISTRIBUSI LEADS PROPERTI LANGSUNG KE SALES",
                highlight_words=["OTOMASI DISTRIBUSI LEADS"],
                subheadline="Sistem routing cerdas mencegah leads terabaikan dan meningkatkan closing tim sales.",
                badge_text="SOLUSI SISTEM",
                cta_text="Lihat Demo Sistem →"
            )
        },
        {
            "template_id": "06_CALL_TO_ACTION",
            "filename": "sample_06_call_to_action_1080x1350.png",
            "spec": DesignSpecification(
                template_id="06_CALL_TO_ACTION",
                width=1080,
                height=1350,
                headline="KONSULTASI AUDIT SISTEM MARKETING PROPERTI ANDA",
                highlight_words=["AUDIT SISTEM MARKETING"],
                subheadline="Dapatkan roadmap perbaikan funnel iklan properti dalam sesi 45 menit bersama tim kami.",
                badge_text="SLOT TERBATAS",
                cta_text="HUBUNGI VIA WHATSAPP ➔"
            )
        }
    ]

    print("==================================================")
    print("  RENDERING 6 SAMPLE DESIGNS (1080x1350)")
    print("==================================================")

    for item in samples:
        spec = item["spec"]
        png_bytes, meta = renderer.render_spec(spec)
        out_path = output_dir / item["filename"]
        with open(out_path, "wb") as f:
            f.write(png_bytes)

        qa = VisualQAService.evaluate_design(spec, meta)
        
        # Verify image properties with Pillow
        img = Image.open(io.BytesIO(png_bytes))
        print(f"[OK] [{spec.template_id}] -> {item['filename']}")
        print(f"     Size: {img.size} (Expected 1080x1350) | Latency: {meta['render_latency_ms']}ms | QA Score: {qa.score}/100 ({qa.readability})")
        assert img.size == (1080, 1350)
        assert qa.score >= 85

    print("\n[SUCCESS] All 6 sample designs rendered and verified successfully!")

if __name__ == "__main__":
    run_sample_renders()
