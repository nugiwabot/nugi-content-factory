from typing import List, Optional
from app.schemas.editorial_agent import ContentType
from app.schemas.design_spec import CTAStrategy


class CaptionGenerationService:
    """
    Generates comprehensive, high-value Instagram article captions
    structured into Hook, Problem, Explanation, Why it happens, Practical solution, and Key takeaway.
    """
    @staticmethod
    def generate_caption(
        topic: str,
        content_type: ContentType,
        headline: str,
        core_insight: str,
        target_audience: str,
        cta_policy: CTAStrategy = CTAStrategy.CTA_NONE,
        cta_text: Optional[str] = None
    ) -> str:
        clean_topic = topic.strip()

        if content_type == ContentType.PROPERTY_PROBLEM:
            caption = (
                f"Pernahkah Anda menghitung berapa banyak leads iklan properti yang masuk ke WhatsApp, "
                f"tetapi berhenti di percakapan pertama tanpa pernah datang survey lokasi?\n\n"
                f"📌 MASALAH NYATA DI LAPANGAN:\n"
                f"Sebagian besar developer menyalahkan tim digital ads saat angka closing rendah. "
                f"Padahal ketika kami mengaudit data percakapan WhatsApp:\n"
                f"1. Rata-rata waktu respons sales berkisar antara 45 menit hingga 3 jam.\n"
                f"2. Pesan pertama yang dikirimkan seringkali berupa file brosur PDF berat tanpa menyapa kebutuhan spesifik prospek.\n"
                f"3. Tidak ada tindak lanjut kedua jika calon pembeli hanya membaca pesan.\n\n"
                f"💡 KENAPA INI TERJADI?\n"
                f"Calon pembeli properti yang mengklik iklan berada pada fase minat tertinggi dalam 5-15 menit pertama. "
                f"Ketika respons lambat, momentum emosional mereka mendingin, dan perhatian mereka teralihkan oleh iklan developer lain yang merespons lebih cepat.\n\n"
                f"🛠️ SOLUSI PRAKTIS:\n"
                f"• Terapkan SLA respons maksimal 5 menit untuk leads baru.\n"
                f"• Gunakan pesan pembuka personal yang fokus mengajukan 1 pertanyaan kualifikasi sederhana (misal: budget atau rencana huni).\n"
                f"• Selalu kunci janji temu survey lokasi dengan opsi tanggal dan jam yang spesifik.\n\n"
                f"✨ KESIMPULAN:\n"
                f"{core_insight}"
            )

        elif content_type == ContentType.PROPERTY_INSIGHT:
            caption = (
                f"Banyak orang beranggapan bahwa kenaikan harga properti semata-mata dipicu oleh inflasi dan bahan bangunan. "
                f"Kenyataannya, faktor pendorong terbesar adalah konektivitas infrastruktur.\n\n"
                f"📊 DATA & FAKTA:\n"
                f"Kawasan hunian yang terhubung langsung dengan akses tol baru rata-rata mengalami lonjakan capital gain 15-25% lebih tinggi "
                f"dibandingkan kawasan sekitarnya yang terisolasi dari akses cepat.\n\n"
                f"💡 ANALISIS PASAR:\n"
                f"Akses jalan tol bukan hanya memangkas waktu tempuh perjalanan harian, melainkan memicu masuknya pusat komersial, "
                f"sekolah unggulan, dan fasilitas publik baru yang secara otomatis mendongkrak permintaan hunian di radius 3-5 km.\n\n"
                f"🛠️ REKOMENDASI STRATEGIS:\n"
                f"Bagi pengembang properti maupun investor, identifikasi koridor rencana tata ruang kota sebelum pembangunan fisik tol rampung. "
                f"Di titik itulah peluang akumulasi lahan dan peluncuran proyek memiliki margin apresiasi tertinggi.\n\n"
                f"✨ KESIMPULAN:\n"
                f"{core_insight}"
            )

        elif content_type == ContentType.PROPERTY_LISTICLE:
            caption = (
                f"Berikut adalah 5 kesalahan mendasar yang paling sering menggagalkan konversi leads properti:\n\n"
                f"1️⃣ Respon di Atas 15 Menit\n"
                f"Setiap menit keterlambatan menurunkan probabilitas janji survey hingga 80%.\n\n"
                f"2️⃣ Template Pesan Chat Kaku\n"
                f"Mengirimkan broadcast copy-paste panjang tanpa menyebut nama prospek menciptakan kesan robotik.\n\n"
                f"3️⃣ Terlalu Cepat Menjual Sebelum Memahami Kebutuhan\n"
                f"Langsung menawarkan unit termahal sebelum mengetahui apakah prospek mencari rumah tinggal atau investasi.\n\n"
                f"4️⃣ Tidak Menetapkan Jadwal Survey Spesifik\n"
                f"Menutup percakapan dengan 'kapan-kapan mampir ya' alih-alih 'apakah hari Sabtu jam 10 pagi atau Minggu jam 2 siang yang lebih cocok?'.\n\n"
                f"5️⃣ Menyerah Setelah Satu Kali Follow-Up\n"
                f"Faktanya, 60% closing properti baru terjadi pada follow-up ke-3 hingga ke-5.\n\n"
                f"✨ KESIMPULAN:\n"
                f"{core_insight}"
            )

        elif content_type == ContentType.PROPERTY_CASE_STUDY:
            caption = (
                f"Bagaimana sistem respon cerdas mentransformasi kinerja penjualan proyek hunian mahasiswa?\n\n"
                f"📈 LATAR BELAKANG:\n"
                f"Sebelumnya, leads iklan yang masuk ke nomor sales sering terlambat dibalas hingga 2 jam. "
                f"Tingkat konversi leads menjadi janji temu survey lokasi stagnan di bawah 8%.\n\n"
                f"⚙️ INTERVENSI SISTEM:\n"
                f"1. Otomasi alur pesan instan terintegrasi dengan kualifikasi awal nama dan budget.\n"
                f"2. Routing otomatis leads ke sales yang sedang aktif secara bergantian (round-robin).\n"
                f"3. Reminder otomatis 24 jam sebelum jadwal survey lokasi.\n\n"
                f"🏆 HASIL:\n"
                f"• Waktu respons rata-rata turun dari 120 menit menjadi < 2 menit.\n"
                f"• Janji temu survey lokasi melonjak +300% dalam periode 60 hari.\n"
                f"• Biaya per closing turun signifikan karena minimnya prospek yang terbuang sia-sia.\n\n"
                f"✨ KESIMPULAN:\n"
                f"{core_insight}"
            )

        elif content_type == ContentType.PROPERTY_SHOWCASE:
            caption = (
                f"Mencari aset properti dengan cashflow sewa stabil dan potensi capital gain tinggi?\n\n"
                f"🏢 DETAIL UNIT:\n"
                f"• Tipe: Rumah Kost (Rukost) Eksklusif Modern\n"
                f"• Lokasi: Jatinangor, Sumedang (Radius dekat Kampus UNPAD & ITB)\n"
                f"• Kapasitas: 16 Kamar Kost Full Furnished\n"
                f"• Legalitas: Sertifikat Hak Milik (SHM) & IMB Lengkap\n"
                f"• Estimasi Yield: 10% - 14% per tahun dari pendapatan sewa mahasiswa\n\n"
                f"💡 KEUNGGULAN UTAMA:\n"
                f"Dilengkapi sistem manajemen properti terpadu sehingga pemilik tidak perlu repot mengurus tagihan sewa bulanan dan perawatan gedung.\n\n"
                f"✨ INFORMASI:\n"
                f"Unit siap survei dengan slot kepemilikan terbatas."
            )

        else: # PROPERTY_OPINION & PROPERTY_EDUCATION
            caption = (
                f"Dalam era digital hari ini, ekspektasi pembeli properti telah berubah secara fundamental.\n\n"
                f"Calon konsumen tidak lagi memiliki kesabaran menunggu balasan pesan berjam-jam hanya untuk mengetahui harga atau tipe unit yang tersedia.\n\n"
                f"Developer dan agensi properti yang mampu menyediakan informasi transparan, cepat, dan profesional sejak detik pertama "
                f"adalah yang akan mendominasi pangsa pasar penjualan properti ke depan.\n\n"
                f"Pemasaran properti bukan lagi soal siapa yang memasang baliho terbesar, melainkan siapa yang memiliki ekosistem tindak lanjut digital yang paling presisi.\n\n"
                f"✨ KESIMPULAN:\n"
                f"{core_insight}"
            )

        # Append CTA ONLY if required or optional
        if cta_policy == CTAStrategy.CTA_REQUIRED and cta_text:
            caption += f"\n\n👉 {cta_text}"
        elif cta_policy == CTAStrategy.CTA_OPTIONAL and cta_text:
            caption += f"\n\n📍 Ingin survey lokasi? {cta_text}"

        # Brand Hashtags
        caption += "\n\n#BisnisProperti #DeveloperProperti #MarketingProperti #InvestasiProperti #NugiProperti"

        return caption
