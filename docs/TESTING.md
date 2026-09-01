# 🧪 Testing Strategy: Nugi Content Factory

Sistem pengujian otomatis (*automated testing*) dirancang agar dapat dijalankan secara mandiri tanpa membutuhkan koneksi internet atau saldo API berbayar.

## 1. Lingkup Pengujian (17 Test Suites)

### A. Provider Tests (`test_providers.py`)
- Memvalidasi `MockLLMProvider` menghasilkan struktur copy (headline, hook, caption, hashtags) yang lengkap.
- Memvalidasi `MockImageProvider` menghasilkan canvas visual binary PNG dengan dimensi tepat.
- Memvalidasi `LocalStorageProvider` dapat menyimpan, membaca, memeriksa keberadaan, dan menghapus file secara aman.
- Memvalidasi `ProviderFactory` menginjeksi provider yang sesuai dan menolak tipe provider tidak valid.

### B. Deterministic Rendering Tests (`test_rendering.py`)
- Memvalidasi `LayoutEngine.wrap_text` membagi headline panjang menjadi baris-baris berimbang.
- Memvalidasi kalkulasi kontras warna WCAG.
- Memvalidasi `DeterministicRenderingEngine` menggabungkan background + tipografi + badge menjadi gambar PNG valid yang dapat dibuka oleh Pillow.

### C. Quality Assurance Tests (`test_qa_service.py`)
- Memvalidasi evaluasi panjang karakter headline dan caption.
- Memvalidasi *guardrail policy* pendeteksian klaim garansi keuntungan properti yang dilarang (misal: "pasti untung 100%").

### D. API Integration Tests (`test_api_health.py`, `test_api_projects.py`, `test_api_generation.py`)
- Menguji endpoint `GET /api/v1/health`.
- Menguji siklus CRUD Project dan Brand Profile.
- Menguji alur lengkap *end-to-end* (`POST /api/v1/content/generate`), pembuatan record `Content`, penyimpanan `Asset`, pembuatan `QAResult`, dan penyelesaian `GenerationJob`.

---

## 2. Cara Menjalankan Test
```bash
cd backend
python -m pytest -v --tb=short
```
Hasil yang diharapkan: **17 passed** dengan status hijau.
