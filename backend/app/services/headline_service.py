from typing import Dict, Any, List
from app.schemas.editorial_agent import ContentType


class HeadlineGenerationService:
    """
    Generates high-impact, editorial Indonesian headlines (2-4 lines),
    concise supporting subheadlines, and extracts exact highlight words for accent styling.
    """
    @staticmethod
    def generate_headline_package(
        topic: str,
        content_type: ContentType,
        editorial_angle: str,
        target_audience: str,
        highlight_override: List[str] = None
    ) -> Dict[str, Any]:
        clean_topic = topic.strip()
        topic_lower = clean_topic.lower()

        if content_type == ContentType.PROPERTY_PROBLEM:
            if "follow" in topic_lower or "lambat" in topic_lower:
                headline = "LEADS IKLAN MASUK, TAPI SALES LAMBAT FOLLOW-UP?"
                highlight_words = ["LAMBAT FOLLOW-UP"]
                subheadline = "Setiap menit keterlambatan membuat calon pembeli beralih ke developer kompetitor."
            else:
                headline = "IKLAN PROPERTI BONCOS, TAPI CLOSING TETAP NOL?"
                highlight_words = ["CLOSING TETAP NOL"]
                subheadline = "Masalahnya bukan pada budget iklan, tapi pada funnel respon WhatsApp yang bocor."

        elif content_type == ContentType.PROPERTY_INSIGHT:
            if "tol" in topic_lower or "lokasi" in topic_lower:
                headline = "KENAPA HARGA RUMAH DI DEKAT TOL BISA NAIK LEBIH CEPAT?"
                highlight_words = ["NAIK LEBIH CEPAT"]
                subheadline = "Aksesibilitas dan percepatan infrastruktur melipatgandakan capital gain kawasan."
            else:
                headline = "BIAYA IKLAN PROPERTI MAHAL BUKAN KARENA ALGORITMA"
                highlight_words = ["BUKAN KARENA ALGORITMA"]
                subheadline = "Penyebab utama CPA membengkak adalah penawaran unit generik dan respons sales yang lambat."

        elif content_type == ContentType.PROPERTY_LISTICLE:
            headline = "5 KESALAHAN FATAL FOLLOW-UP LEADS PROPERTI"
            highlight_words = ["KESALAHAN FATAL"]
            subheadline = "Hindari pola komunikasi kaku yang membuat prospek hangat menghilang tanpa kabar."

        elif content_type == ContentType.PROPERTY_CASE_STUDY:
            headline = "TRANSFORMASI RESPONSE TIME LEADS GREN PROPERTYKOST"
            highlight_words = ["TRANSFORMASI RESPONSE TIME"]
            subheadline = "Penerapan sistem routing pesan instan meningkatkan janji survey lokasi hingga 300%."

        elif content_type == ContentType.PROPERTY_SHOWCASE:
            headline = "RUKOST PREMIUM DEKAT KAMPUS UNPAD JATINANGOR"
            highlight_words = ["RUKOST PREMIUM"]
            subheadline = "Pilihan aset investasi properti dengan yield sewa tinggi dan manajemen profesional."

        elif content_type == ContentType.PROPERTY_OPINION:
            headline = "DEVELOPER YANG MENOLAK OTOMASI AKAN TERTINGGAL"
            highlight_words = ["MENOLAK OTOMASI"]
            subheadline = "Generasi pembeli properti hari ini menuntut respons dalam hitungan menit, bukan jam."

        elif content_type == ContentType.PROPERTY_SALES_OFFER:
            headline = "AUDIT SISTEM MARKETING & FUNNEL PROPERTI ANDA"
            highlight_words = ["AUDIT SISTEM MARKETING"]
            subheadline = "Petakan kebocoran leads iklan dan dapatkan roadmap perbaikan dalam sesi konsultasi 45 menit."

        else: # PROPERTY_EDUCATION
            headline = f"STRATEGI FUNDAMENTAL PEMASARAN PROPERTI MODERN"
            highlight_words = ["PEMASARAN PROPERTI MODERN"]
            subheadline = "Membangun kepercayaan dan mengedukasi prospek sebelum menawarkan unit proyek."

        # If user provided explicit highlight overrides
        if highlight_override and len(highlight_override) > 0:
            highlight_words = highlight_override

        return {
            "headline": headline,
            "subheadline": subheadline,
            "highlight_words": highlight_words
        }
