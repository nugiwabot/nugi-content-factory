import time
from typing import Dict, Any, Optional
from app.providers.base import LLMProvider, LLMContentOutput


class MockLLMProvider(LLMProvider):
    """
    Deterministic Mock LLM provider producing structured property marketing copy
    without requiring external network requests or API credits.
    """
    @property
    def provider_name(self) -> str:
        return "MockLLMProvider"

    def generate_content(
        self,
        topic: str,
        target_audience: str,
        content_pillar: str,
        tone_of_voice: str,
        brand_context: Optional[Dict[str, Any]] = None
    ) -> LLMContentOutput:
        start_time = time.time()

        # Clean strings
        clean_topic = topic.strip()
        topic_lower = clean_topic.lower()

        # Deterministic generation tailored to property marketing
        if "follow" in topic_lower or "lead" in topic_lower or "iklan" in topic_lower:
            headline = "3 Alasan Kenapa Leads Iklan Properti Sering Dingin"
            hook_text = "Bukan iklannya yang salah, tapi cara responnya yang terlambat."
            body_caption = (
                "Banyak developer & agen properti mengeluh leads iklan Meta atau Google boncos. "
                "Padahal saat dicek di lapangan:\n\n"
                "1. Respon lead baru lebih dari 15 menit.\n"
                "2. Sales langsung kirim brosur PDF berat tanpa menyapa kebutuhan prospek.\n"
                "3. Tidak ada reminder otomatis untuk follow-up survey lokasi.\n\n"
                "Gunakan sistem automasi alur leads agar tim sales Anda merespon dalam hitungan detik saat calon pembeli masih hangat!"
            )
            hashtags = "#BisnisProperti #DeveloperProperti #MarketingProperti #LeadAutomation #NugiProperti"
            call_to_action = "Klik link di bio untuk konsultasi automasi alur leads properti Anda!"
            visual_prompt = "Modern minimalist property marketing dashboard, dark navy gradient, sleek typography, ultra clean architectural aesthetics"
        elif "kost" in topic_lower or "rukos" in topic_lower or "investasi" in topic_lower:
            headline = "Strategi Passive Income Stabil dari Rumah Kost Mahasiswa"
            hook_text = "Yield sewa hingga 12% per tahun di kawasan kampus premium."
            body_caption = (
                "Investasi properti bukan cuma soal beli tanah dan bangunan, tapi bagaimana cashflow operasionalnya berjalan otomatis.\n\n"
                "Kunci sukses bisnis rukos modern:\n"
                "• Lokasi strategis < 5 menit ke kampus utama.\n"
                "• Fasilitas all-in (WiFi, furnish lengkap, water heater).\n"
                "• Manajemen penghuni & tagihan sewa berbasis sistem digital.\n\n"
                "Investasi cerdas, aset berkembang, passive income mengalir lancar setiap bulan."
            )
            hashtags = "#InvestasiProperti #RumahKost #PassiveIncome #PropertyYield #RukosModern"
            call_to_action = "Dapatkan e-brochure dan simulasi ROI lengkap via DM!"
            visual_prompt = "Luxury modern property architectural unit, golden hour warm lighting, elegant clean lines, photorealistic high quality"
        else:
            # General fallback deterministic output based on input topic
            headline = f"Strategi Efektif: {clean_topic[:45]}"
            hook_text = f"Panduan praktis untuk {target_audience} dalam mengoptimalkan hasil."
            body_caption = (
                f"Membahas topik penting seputar {clean_topic}.\n\n"
                f"Dalam industri properti yang kompetitif, {target_audience} memerlukan pendekatan terstruktur "
                f"dan sistematis agar setiap peluang konversi tidak terbuang sia-sia.\n\n"
                f"Fokus pada proses yang jelas, alat kerja yang tepat, dan tindak lanjut yang konsisten."
            )
            hashtags = "#PropertiIndonesia #MarketingProperti #DigitalProperty #PropertyStrategy"
            call_to_action = "Bagikan postingan ini ke tim Anda dan diskusikan langkah perbaikannya!"
            visual_prompt = f"Abstract property architectural concept, dark slate theme with cyan accents, modern geometric composition for {clean_topic}"

        latency_ms = int((time.time() - start_time) * 1000)

        return LLMContentOutput(
            headline=headline,
            hook_text=hook_text,
            body_caption=body_caption,
            hashtags=hashtags,
            call_to_action=call_to_action,
            visual_concept_prompt=visual_prompt,
            raw_response={
                "mock_generated": True,
                "pillar": content_pillar,
                "tone": tone_of_voice,
                "audience": target_audience
            },
            provider=self.provider_name,
            model="mock-llm-v1",
            tokens_used=240,
            tokens_in=120,
            tokens_out=120,
            estimated_cost=0.0,
            latency_ms=max(latency_ms, 12)
        )
