from typing import Dict, Any, List
from app.schemas.editorial_agent import ContentType


class HeadlineGenerationService:
    """
    Generates high-impact, editorial Indonesian headlines (2-3 lines, NugiProperti Editorial style),
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

        if "leads" in topic_lower and "lambat" in topic_lower:
            headline = "LEADS IKLAN MASUK, TAPI SALES LAMBAT FOLLOW-UP?"
            highlight_words = ["LAMBAT FOLLOW-UP?"]
            subheadline = "Setiap menit keterlambatan membuat calon pembeli beralih ke developer lain."

        elif "lokasi bagus" in topic_lower or "cepat laku" in topic_lower:
            headline = "LOKASI BAGUS, TAPI PROPERTI BELUM TENTU CEPAT LAKU?"
            highlight_words = ["BELUM TENTU CEPAT LAKU?"]
            subheadline = "Faktor penawaran dan kecepatan respon seringkali lebih menentukan konversi."

        elif "daya beli" in topic_lower or "harga rumah" in topic_lower:
            headline = "HARGA RUMAH NAIK, DAYA BELI TIDAK IKUT NAIK"
            highlight_words = ["DAYA BELI TIDAK IKUT NAIK"]
            subheadline = "Dinamika pasar properti menghadapi tantangan gap likuiditas konsumen baru."

        elif "membeli properti" in topic_lower or "pertama" in topic_lower:
            headline = "3 KESALAHAN SAAT MEMBELI PROPERTI PERTAMA"
            highlight_words = ["3 KESALAHAN"]
            subheadline = "Hindari jebakan legalitas dan perhitungan cashflow yang merugikan."

        elif "conversion rate" in topic_lower or "300%" in topic_lower or "bagaimana satu" in topic_lower:
            headline = "CARA SATU PROPERTI NAIKKAN CONVERSION RATE 300%"
            highlight_words = ["CONVERSION RATE 300%"]
            subheadline = "Studi kasus optimasi funnel respon cepat melipatgandakan closing."

        elif "parahyangan" in topic_lower or "rumah premium" in topic_lower:
            headline = "RUMAH PREMIUM DEKAT KOTA BARU PARAHYANGAN"
            highlight_words = ["RUMAH PREMIUM"]
            subheadline = "Unit hunian eksklusif dengan fasilitas lengkap dan nilai investasi tinggi."

        elif content_type == ContentType.PROPERTY_PROBLEM:
            headline = "IKLAN PROPERTI BONCOS, TAPI CLOSING TETAP NOL?"
            highlight_words = ["CLOSING TETAP NOL?"]
            subheadline = "Masalahnya bukan pada budget iklan, tapi pada funnel respon WhatsApp yang bocor."

        elif content_type == ContentType.PROPERTY_INSIGHT:
            headline = "BIAYA IKLAN PROPERTI MAHAL BUKAN KARENA ALGORITMA"
            highlight_words = ["BUKAN KARENA ALGORITMA"]
            subheadline = "Penyebab utama CPA membengkak adalah penawaran unit generik."

        elif content_type in (ContentType.PROPERTY_LISTICLE, ContentType.NUMBER_LIST):
            headline = "5 KESALAHAN FATAL FOLLOW-UP LEADS PROPERTI"
            highlight_words = ["5 KESALAHAN FATAL"]
            subheadline = "Hindari pola komunikasi kaku yang membuat prospek hangat menghilang."

        elif content_type in (ContentType.PROPERTY_CASE_STUDY, ContentType.CASE_STUDY):
            headline = "TRANSFORMASI RESPONSE TIME MENINGKATKAN CLOSING 300%"
            highlight_words = ["MENINGKATKAN CLOSING 300%"]
            subheadline = "Penerapan sistem routing pesan instan meningkatkan janji survey lokasi."

        elif content_type == ContentType.PROPERTY_SHOWCASE:
            headline = "RUKOST PREMIUM DEKAT KAMPUS UNPAD JATINANGOR"
            highlight_words = ["RUKOST PREMIUM"]
            subheadline = "Pilihan aset investasi properti dengan yield sewa tinggi dan manajemen siap kelola."

        elif content_type in (ContentType.PROPERTY_OPINION, ContentType.OPINION):
            headline = "DEVELOPER YANG MENOLAK OTOMASI AKAN TERTINGGAL"
            highlight_words = ["MENOLAK OTOMASI"]
            subheadline = "Generasi pembeli properti hari ini menuntut respons dalam hitungan menit."

        else:
            # Fallback direct uppercase conversion of topic
            headline = clean_topic.upper()
            words = headline.split()
            highlight_words = [" ".join(words[-2:])] if len(words) >= 2 else [headline]
            subheadline = "Editorial insight strategi pemasaran dan kepemimpinan properti modern."

        if highlight_override:
            highlight_words = highlight_override

        return {
            "headline": headline,
            "highlight_words": highlight_words,
            "subheadline": subheadline
        }
