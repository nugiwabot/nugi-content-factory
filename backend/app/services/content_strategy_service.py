from typing import Optional, Dict, Any
from app.schemas.editorial_agent import ContentType, UserBriefInput, EditorialContentSpecification
from app.schemas.design_spec import CompositionType, CTAStrategy


class ContentStrategyService:
    """
    Analyzes raw user briefs, classifies property content types,
    identifies audience friction, and determines the editorial strategy and CTA policy.
    """
    @staticmethod
    def classify_and_strategize(brief: UserBriefInput) -> Dict[str, Any]:
        topic = brief.topic.strip()
        topic_lower = topic.lower()
        audience = brief.target_audience or "Developer & Tim Marketing Properti"

        # 1. Determine Content Type
        if brief.content_type_override:
            content_type = brief.content_type_override
        elif any(k in topic_lower for k in ["kesalahan", "tips", "langkah", "alasan", "5 ", "3 ", "7 "]):
            content_type = ContentType.PROPERTY_LISTICLE
        elif any(k in topic_lower for k in ["studi kasus", "hasil transformasi", "closing naik", "roi"]):
            content_type = ContentType.PROPERTY_CASE_STUDY
        elif any(k in topic_lower for k in ["rukost", "kavling", "unit", "villa", "apartemen", "showcase"]):
            content_type = ContentType.PROPERTY_SHOWCASE
        elif any(k in topic_lower for k in ["promo", "daftar audit", "konsultasi gratis", "slot terbatas"]):
            content_type = ContentType.PROPERTY_SALES_OFFER
        elif any(k in topic_lower for k in ["tol", "infrastruktur", "tren", "pasar", "naik lebih cepat", "kenaikan harga", "data & statistik"]):
            content_type = ContentType.PROPERTY_INSIGHT
        elif any(k in topic_lower for k in ["opini", "menolak otomasi", "masa depan pemasaran"]):
            content_type = ContentType.PROPERTY_OPINION
        elif any(k in topic_lower for k in ["masalah", "lambat", "dingin", "boncos", "gagal", "bocor", "kenapa"]):
            content_type = ContentType.PROPERTY_PROBLEM
        else:
            content_type = ContentType.PROPERTY_EDUCATION

        # 2. Strict CTA Business Rule
        if content_type == ContentType.PROPERTY_SALES_OFFER:
            cta_policy = CTAStrategy.CTA_REQUIRED
            default_cta = "Jadwalkan Sesi Audit Gratis →"
        elif content_type == ContentType.PROPERTY_SHOWCASE:
            cta_policy = CTAStrategy.CTA_OPTIONAL
            default_cta = "Jadwalkan Survey Lokasi →"
        else: # PROPERTY_EDUCATION, PROPERTY_PROBLEM, PROPERTY_INSIGHT, PROPERTY_LISTICLE, PROPERTY_CASE_STUDY, PROPERTY_OPINION
            cta_policy = CTAStrategy.CTA_NONE
            default_cta = None

        # 3. Map Suggested Archetype
        archetype_map = {
            ContentType.PROPERTY_EDUCATION: CompositionType.HERO_IMAGE_EDITORIAL,
            ContentType.PROPERTY_PROBLEM: CompositionType.HERO_IMAGE_EDITORIAL,
            ContentType.PROPERTY_INSIGHT: CompositionType.CINEMATIC_OVERLAY,
            ContentType.PROPERTY_LISTICLE: CompositionType.LIST_EDITORIAL,
            ContentType.PROPERTY_CASE_STUDY: CompositionType.DATA_EDITORIAL,
            ContentType.PROPERTY_OPINION: CompositionType.MINIMAL_EDITORIAL,
            ContentType.PROPERTY_SHOWCASE: CompositionType.PROPERTY_SHOWCASE,
            ContentType.PROPERTY_SALES_OFFER: CompositionType.HERO_IMAGE_EDITORIAL,
        }
        suggested_archetype = archetype_map.get(content_type, CompositionType.HERO_IMAGE_EDITORIAL)

        # 4. Formulate Problem, Core Insight, and Editorial Angle
        if content_type == ContentType.PROPERTY_PROBLEM:
            audience_problem = "Leads properti masuk dari iklan berbayar tetapi tingkat konversi closing ke survey sangat rendah."
            core_insight = "Masalah bukan pada algoritma iklan, melainkan waktu respons follow-up tim sales yang lambat dan tanpa skrip kualifikasi terstruktur."
            editorial_angle = "Membongkar kebocoran alur follow-up leads properti setelah prospek menekan tombol iklan."
        elif content_type == ContentType.PROPERTY_INSIGHT:
            audience_problem = "Ketidakpastian arah pasar properti dan faktor pendorong kenaikan nilai tanah yang belum dipahami secara mendalam."
            core_insight = "Aksesibilitas infrastruktur dan sentra ekonomi baru melipatgandakan capital gain jauh lebih cepat daripada faktor fisik bangunan."
            editorial_angle = "Analisis mendalam data apresiasi properti berbasis kedekatan infrastruktur strategis."
        elif content_type == ContentType.PROPERTY_LISTICLE:
            audience_problem = "Tim marketing dan sales mengulangi kesalahan operasional yang sama saat memproses prospek properti."
            core_insight = "Menghilangkan kesalahan elementer dalam follow-up meningkatkan peluang closing hingga 3x lipat."
            editorial_angle = "Daftar kesalahan fatal yang harus segera dihentikan oleh developer dan agensi properti."
        elif content_type == ContentType.PROPERTY_CASE_STUDY:
            audience_problem = "Keraguan apakah digitalisasi dan automasi leads benar-benar menghasilkan closing nyata."
            core_insight = "Sistem routing pesan instan terbukti memotong response time dari 45 menit menjadi 2 menit dan melipatgandakan janji survey."
            editorial_angle = "Bukti empiris transformasi kinerja penjualan properti melalui sistem automasi respon."
        elif content_type == ContentType.PROPERTY_SHOWCASE:
            audience_problem = "Investor properti mencari aset dengan cashflow sewa stabil dan legalitas aman."
            core_insight = "Rumah Kost (Rukost) modern di kawasan kampus unggulan memberikan yield tahunan 10-14% dengan okupansi tinggi."
            editorial_angle = "Showcase aset investasi properti siap huni berdaya hasil tinggi."
        elif content_type == ContentType.PROPERTY_OPINION:
            audience_problem = "Kecenderungan bertahan pada metode konvensional yang mulai ditinggalkan pembeli generasi muda."
            core_insight = "Developer yang lambat mengadopsi otomasi digital akan tergerus oleh kompetitor yang responsif dalam hitungan detik."
            editorial_angle = "Sikap tegas mengenai masa depan pemasaran properti modern di Indonesia."
        elif content_type == ContentType.PROPERTY_SALES_OFFER:
            audience_problem = "Biaya iklan properti tinggi tetapi funnel penjualan belum diaudit secara profesional."
            core_insight = "Audit menyeluruh selama 45 menit dapat memetakan titik kebocoran leads iklan dan roadmap perbaikannya."
            editorial_angle = "Penawaran sesi konsultasi dan audit sistem pemasaran properti."
        else: # PROPERTY_EDUCATION
            audience_problem = "Kurangnya pemahaman mengenai mekanisme dasar penilaian dan pemasaran properti modern."
            core_insight = "Pemasaran properti yang berkelanjutan dibangun di atas edukasi nilai, bukan sekadar broadcast harga."
            editorial_angle = "Panduan edukatif memahami faktor kunci pertumbuhan bisnis properti."

        return {
            "content_type": content_type,
            "target_audience": audience,
            "audience_problem": audience_problem,
            "core_insight": core_insight,
            "editorial_angle": editorial_angle,
            "suggested_archetype": suggested_archetype,
            "cta_policy": cta_policy,
            "cta_text": default_cta
        }
