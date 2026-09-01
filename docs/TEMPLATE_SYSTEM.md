# 📐 Data-Driven Template System: Nugi Content Factory

Sistem template dibangun secara *data-driven* menggunakan spesifikasi JSON/Pydantic (`TemplateSpecification`) yang dapat diidentifikasi dan dieksekusi secara otomatis oleh AI reasoning engine maupun deterministic rendering engine.

---

## 1. Daftar 6 Template Spesifikasi

### Template 01: `01_PROPERTY_PROBLEM`
* **Tujuan:** Mengangkat friksi/masalah akut yang dialami developer atau sales manager (misal: leads lambat difollow-up).
* **Skema Aksen:** Rose Red (`#f43f5e`) & Cyan.
* **Zona Semantik:** Badge Peringatan (`DILEMA SALES PROPERTI`), Headline Pertanyaan, Subjudul Dampak Keterlambatan, Tombol Solusi CTA.

### Template 02: `02_PROPERTY_INSIGHT`
* **Tujuan:** Edukasi mendalam analisis pasar properti dan strategi marketing berbobot.
* **Skema Aksen:** Electric Sky Cyan (`#38bdf8`).
* **Zona Semantik:** Badge `MARKET INSIGHT`, Headline Analitis, Takeaway Card, Tombol Simpan Postingan.

### Template 03: `03_NUMBER_LIST`
* **Tujuan:** Menyajikan poin-poin kesalahan fatal atau langkah taktis terstruktur.
* **Skema Aksen:** Warm Amber Gold (`#f59e0b`).
* **Zona Semantik:** Badge `5 POIN KRUSIAL`, Headline Listicle, 3-5 Numbered Bullet Items, CTA Baca Caption.

### Template 04: `04_CASE_STUDY`
* **Tujuan:** Pembuktian hasil nyata transformasi sistem (before vs after).
* **Skema Aksen:** Emerald Green (`#10b981`).
* **Zona Semantik:** Badge `STUDI KASUS & HASIL`, Headline Transformasi, Metric Highlight Box (`+300% Speed`), CTA Konsultasi.

### Template 05: `05_PRODUCT_SOLUTION`
* **Tujuan:** Menjelaskan fitur software, automasi, atau sistem terpadu properti.
* **Skema Aksen:** Deep Indigo (`#6366f1`) & Cyan.
* **Zona Semantik:** Badge `SOLUSI SISTEM`, Headline Solusi, Feature Breakdown Box, CTA Demo Sistem.

### Template 06: `06_CALL_TO_ACTION`
* **Tujuan:** Konversi langsung berurgensi tinggi (misal: pendaftaran survey / slot audit terbatas).
* **Skema Aksen:** Glowing Sky Cyan (`#38bdf8`) & Rose.
* **Zona Semantik:** Badge Urgensi `SLOT TERBATAS`, Headline Penawaran, Deskripsi Nilai, Tombol Hero CTA WhatsApp.

---

## 2. Struktur Schema `TemplateSpecification`
```json
{
  "template_id": "01_PROPERTY_PROBLEM",
  "name": "Property Problem & Dilemma",
  "purpose": "Mengangkat masalah nyata dan friksi sales",
  "target_audience": "Developer & Sales Manager Properti",
  "accent_scheme": "rose",
  "canvas": {
    "width": 1080,
    "height": 1350,
    "aspect_ratio": "4:5"
  },
  "zones": [
    { "zone_id": "badge", "semantic_position": "top_left", "required": true },
    { "zone_id": "headline", "semantic_position": "center_top", "required": true },
    { "zone_id": "subheadline", "semantic_position": "center", "required": false },
    { "zone_id": "cta", "semantic_position": "bottom_center", "required": true }
  ]
}
```
