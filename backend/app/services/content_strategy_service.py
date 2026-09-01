from typing import Optional, Dict, Any
from app.schemas.editorial_agent import ContentType, UserBriefInput, EditorialContentSpecification
from app.schemas.design_spec import CompositionType, CTAStrategy


class ContentStrategyService:
    """
    Analyzes raw user briefs, classifies property content types,
    identifies audience friction, and determines the editorial strategy and CTA policy (Phase 3D-1).
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
        elif any(k in topic_lower for k in ["studi kasus", "hasil transformasi", "closing naik", "efisiensi"]):
            content_type = ContentType.PROPERTY_CASE_STUDY
        elif any(k in topic_lower for k in ["data & statistik", "diagram yield", "data pasar", "grafik"]):
            content_type = ContentType.DATA_EDITORIAL
        elif any(k in topic_lower for k in ["rukost", "kavling", "unit", "villa", "apartemen", "showcase"]):
            content_type = ContentType.PROPERTY_SHOWCASE
        elif any(k in topic_lower for k in ["promo", "daftar audit", "konsultasi gratis", "slot terbatas"]):
            content_type = ContentType.PROPERTY_SALES_OFFER
        elif any(k in topic_lower for k in ["lifestyle", "gaya hidup", "clubhouse", "residensial asri"]):
            content_type = ContentType.SOFT_SELLING
        elif any(k in topic_lower for k in ["tol", "infrastruktur", "tren", "pasar", "naik lebih cepat", "kenaikan harga"]):
            content_type = ContentType.PROPERTY_INSIGHT
        elif any(k in topic_lower for k in ["opini", "menolak otomasi", "masa depan pemasaran"]):
            content_type = ContentType.PROPERTY_OPINION
        elif any(k in topic_lower for k in ["masalah", "lambat", "dingin", "boncos", "gagal", "bocor", "kenapa"]):
            content_type = ContentType.PROPERTY_PROBLEM
        else:
            content_type = ContentType.PROPERTY_EDUCATION

        # 2. Strict CTA Business Rule
        if content_type in (ContentType.PROPERTY_SALES_OFFER, ContentType.DIRECT_OFFER):
            cta_policy = CTAStrategy.CTA_REQUIRED
            default_cta = "Jadwalkan Sesi Audit Gratis →"
        elif content_type == ContentType.PROPERTY_SHOWCASE:
            cta_policy = CTAStrategy.CTA_OPTIONAL
            default_cta = "Jadwalkan Survey Lokasi →"
        else: # PROPERTY_EDUCATION, PROPERTY_PROBLEM, PROPERTY_INSIGHT, NUMBER_LIST, CASE_STUDY, DATA_EDITORIAL, OPINION, SOFT_SELLING
            cta_policy = CTAStrategy.CTA_NONE
            default_cta = None

        # 3. Map Suggested Archetype
        archetype_map = {
            ContentType.PROPERTY_EDUCATION: CompositionType.HERO_IMAGE_EDITORIAL,
            ContentType.PROPERTY_PROBLEM: CompositionType.HERO_IMAGE_EDITORIAL,
            ContentType.PROPERTY_INSIGHT: CompositionType.CINEMATIC_OVERLAY,
            ContentType.PROPERTY_LISTICLE: CompositionType.LIST_EDITORIAL,
            ContentType.NUMBER_LIST: CompositionType.LIST_EDITORIAL,
            ContentType.PROPERTY_CASE_STUDY: CompositionType.DATA_EDITORIAL,
            ContentType.CASE_STUDY: CompositionType.DATA_EDITORIAL,
            ContentType.DATA_EDITORIAL: CompositionType.DATA_EDITORIAL,
            ContentType.PROPERTY_OPINION: CompositionType.MINIMAL_EDITORIAL,
            ContentType.OPINION: CompositionType.MINIMAL_EDITORIAL,
            ContentType.PROPERTY_SHOWCASE: CompositionType.PROPERTY_SHOWCASE,
            ContentType.SOFT_SELLING: CompositionType.HERO_IMAGE_EDITORIAL,
            ContentType.PROPERTY_SALES_OFFER: CompositionType.HERO_IMAGE_EDITORIAL,
            ContentType.DIRECT_OFFER: CompositionType.HERO_IMAGE_EDITORIAL,
        }
        suggested_archetype = archetype_map.get(content_type, CompositionType.HERO_IMAGE_EDITORIAL)

        # 4. Formulate Problem, Angle, and Core Insight
        if content_type == ContentType.PROPERTY_PROBLEM:
            problem = "Leads iklan masuk dalam jumlah banyak tetapi tingkat closing penjualan tetap rendah."
            angle = "Masalah bukan pada platform iklan, melainkan bottleneck di kecepatan dan kualitas follow-up tim sales."
            insight = "Kecepatan respon di bawah 5 menit melipatgandakan peluang closing hingga 391% dibandingkan respon di atas 30 menit."
        elif content_type in (ContentType.PROPERTY_LISTICLE, ContentType.NUMBER_LIST):
            problem = "Tim sales melakukan kesalahan berulang saat menghubungi prospek properti baru."
            angle = "Menghindari 3 kesalahan fatal follow-up akan langsung menyelamatkan anggaran iklan developer."
            insight = "Follow-up yang berfokus pada konsultasi kebutuhan menghasilkan konversi survey 3x lebih tinggi daripada langsung mengirim brosur PDF."
        elif content_type in (ContentType.PROPERTY_CASE_STUDY, ContentType.CASE_STUDY, ContentType.DATA_EDITORIAL):
            problem = "Developer kesulitan mengukur ROI implementasi digitalisasi dan respon cepat leads."
            angle = "Data empiris transformasi waktu respon menunjukkan peningkatan langsung pada janji temu survey lokasi."
            insight = "Sistem otomatisasi alur leads terbukti menaikkan volume survey hingga 300% dalam waktu 60 hari."
        elif content_type in (ContentType.PROPERTY_OPINION, ContentType.OPINION):
            problem = "Banyak pelaku industri properti masih meragukan efektivitas automasi pemasaran digital."
            angle = "Developer yang menolak transformasi digital dan respon instan akan ditinggalkan oleh generasi pembeli modern."
            insight = "Keputusan membeli properti kini dimulai dari pengalaman digital pertama yang cepat dan transparan."
        elif content_type == ContentType.PROPERTY_INSIGHT:
            problem = "Investor properti bingung memprediksi akselerasi pertumbuhan harga tanah dan properti."
            angle = "Infrastruktur tol dan konektivitas transportasi modern adalah katalis utama percepatan capital gain."
            insight = "Kawasan yang terhubung pintu tol baru mencatat pertumbuhan harga tanah 25-40% lebih cepat dibandingkan area tanpa akses tol."
        elif content_type == ContentType.PROPERTY_SHOWCASE:
            problem = "Investor mencari aset properti dengan yield riil tinggi dan bebas repot manajemen operasional."
            angle = "Showcase unit rukost premium dengan potensi passive income konsisten dan okupansi mahasiswa terjamin."
            insight = "Rumah kost modern dengan fasilitas lengkap di dekat kampus utama memberikan yield sewa 10-14% per tahun."
        else: # PROPERTY_EDUCATION, SOFT_SELLING, DIRECT_OFFER
            problem = "Kurangnya pemahaman mengenai pondasi sistem marketing properti yang terukur."
            angle = "Membangun sistem pemasaran yang terintegrasi dari traffic iklan, filter leads, hingga closing."
            insight = "Pemasaran properti yang sukses bertumpu pada konsistensi pesan, diferensiasi produk, dan kecepatan eksekusi tim."

        return {
            "content_type": content_type,
            "target_audience": audience,
            "audience_problem": problem,
            "editorial_angle": angle,
            "core_insight": insight,
            "suggested_archetype": suggested_archetype,
            "cta_policy": cta_policy,
            "cta_text": default_cta
        }
