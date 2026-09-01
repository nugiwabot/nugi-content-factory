# 🛡️ Visual Quality Assurance (Visual QA): Nugi Content Factory

Sistem Visual QA melakukan validasi otomatis berbasis aturan (*deterministic validation*) terhadap parameter desain dan hasil render untuk memastikan kepatuhan visual sebelum materi dipublikasikan.

---

## 1. Aturan Validasi Otomatis (Rules & Scoring)

1. **Dimensi Canvas (Bobot: 20 poin):**
   * Validasi ukuran: wajib `1080x1350` (Portrait 4:5) atau `1080x1080` (Square 1:1).
2. **Template ID Terdaftar (Bobot: 15 poin):**
   * Validasi bahwa `template_id` ada dalam registri sistem.
3. **Panjang Headline & Keterbacaan Mobile (Bobot: 25 poin):**
   * Panjang karakter headline ideal: 15–120 karakter.
   * Auto-fit font minimal 28pt (mencegah teks mengecil berlebihan).
4. **Validasi Highlight Words (Bobot: 10 poin):**
   * Memastikan setiap kata/frasa dalam `highlight_words` benar-benar ada dalam teks headline.
5. **Kelengkapan Zona Semantik (Bobot: 20 poin):**
   * Memverifikasi zona wajib per template (misal: badge kategori, tombol CTA, daftar bullet points).
6. **Rasio Kontras Warna WCAG (Bobot: 30 poin):**
   * Memastikan teks utama di atas surface card memiliki rasio kontras > 7.0:1 (WCAG AAA).

---

## 2. Struktur Output `VisualQAResult`
```json
{
  "score": 100,
  "readability": "EXCELLENT",
  "hierarchy": "STRONG",
  "composition": "BALANCED",
  "branding": "COMPLIANT",
  "safe_area_compliant": true,
  "contrast_ratio_compliant": true,
  "issues": [],
  "recommendations": []
}
```
Jika ditemukan ketidakpatuhan, skor akan berkurang secara otomatis dan daftar `issues` serta `recommendations` akan terisi untuk memandu AI reasoning maupun pengguna.
