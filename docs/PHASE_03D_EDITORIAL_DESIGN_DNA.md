# 🏛️ NugiProperti Editorial Design DNA & Visual Benchmark Specification
**Phase 3D-1 — Professional Editorial Visual Standards**

Dokumen ini adalah standar visual resmi dan sistem aturan yang mengatur seluruh produksi kreatif visual pada **Nugi Content Factory** untuk brand **NugiProperti**.

---

## 1. Visi & Persepsi Brand (Target Perception)

Ketika audiens melihat postingan Instagram NugiProperti tanpa melihat username atau watermark, audiens harus langsung mempersepsikan:
> *"Ini adalah media publikasi properti dan teknologi bisnis level institusional yang berwibawa, tajam, dan berkelas dunia."*

Bukan template Canva biasa. Bukan gambar AI murahan dengan teks yang sekadar ditempelkan.

---

## 2. Definisi Konkret Aturan Desain (Sections A – R)

### A. Brand Visual DNA
* **Primary Background Canvas:** Obsidian Navy (`#070B14`, RGB: `7, 11, 20`) dan Deep Slate (`#0F172A`, RGB: `15, 23, 42`).
* **Text Hierarchy Colors:**
  - Headline Primary: Pure White (`#FFFFFF`, RGB: `255, 255, 255`).
  - Subheadline / Supporting: Slate Silver (`#CBD5E1`, RGB: `203, 213, 225`).
  - Eyebrow / Metadata: Slate Muted (`#94A3B8`, RGB: `148, 163, 184`).
* **Signature Accent Palette:**
  - Electric Sky Cyan (`#38BDF8`): Digunakan untuk edukasi, teknologi, dan infrastruktur.
  - Warm Champagne Gold (`#F59E0B`): Digunakan untuk showcase aset, listicle, dan investasi yield.
  - Emerald Growth Green (`#10B981`): Digunakan untuk studi kasus empiris, kenaikan profit, dan ROI.
  - Alert Rose Red (`#F43F5E`): Digunakan khusus untuk konten friksi/masalah sales (*Property Problem*).
  - Deep Indigo (`#6366F1`): Digunakan untuk opini dan editorial kepemimpinan.

---

### B. Art Direction Principles
1. **Visual Story First:** Setiap visual harus menceritakan sebuah narasi nyata (misal: "Leads masuk banyak tapi respon sales lambat" vs "Akselerasi jalan tol melipatgandakan capital gain").
2. **Single Focal Anchor:** Maksimal satu subjek utama yang dominan pada frame (fasad arsitektural, jalur tol layang, manajer sales, atau maket proyek).
3. **Intentional Tension:** Komposisi harus memiliki kontras visual antara ruang gelap bernapas (*negative space*) dan objek yang teriluminasi tajam.

---

### C. Editorial Composition Principles
1. **Rule of Thirds & Golden Ratio:** Penempatan subjek fokus pada sepertiga atas atau kanan canvas (antara Y: 15% hingga 60%), membiarkan sepertiga bawah atau kiri untuk tipografi.
2. **Asymmetric Balance:** Hindari penempatan simetris kartu di tengah. Gunakan tata letak asimetris yang dinamis.
3. **Multi-Plane Layering:** Setiap komposisi wajib memiliki 3 bidang kedalaman:
   - *Foreground:* Scrim gelap pelindung teks dan elemen framing.
   - *Midground:* Subjek fokus tajam dan detail arsitektural.
   - *Background:* Lanskap kota / lingkungan dengan *atmospheric perspective* lembut.

---

### D. Image Manipulation & Cutout Principles
1. **Edge Antialiasing & Alpha Masking:** Objek cutout tidak boleh memiliki pinggiran pixel kasar atau halo putih.
2. **Depth-of-Field Simulation:** Elemen latar belakang jauh diberi sedikit *soft atmospheric blur* (radius 2–4px) agar fokus mata langsung menuju subjek dan judul.
3. **Ground Contact Occlusion:** Setiap subjek yang berpijak wajib memiliki bayangan kontak (*contact shadow*) gelap dengan gaussian blur 18px di dasarnya.

---

### E. Typography Principles
* **3-Tier Hierarchy Strict Rule:**
  1. **Tier 1 (Eyebrow Badge):** Ukuran font 20–22px, Huruf Besar, beraksen simbol `✦`, dilengkapi garis aksen rambut (*hairline*).
  2. **Tier 2 (Primary Headline):** Ukuran font 42–56px tebal, 2–4 baris, *leading* proporsional, dengan kata kunci spesifik diberi warna aksen (*highlight words*).
  3. **Tier 3 (Subheadline Body):** Ukuran font 22–26px reguler, warna Slate Silver, maksimal 2–3 baris kalimat padat.
* **Zero Overflow Guarantee:** Teks wajib dibungkus secara deterministik menggunakan `LayoutEngine` dengan batas lebar maksimal 920px (margin aman 80px).

---

### F. Image-to-Text Ratio (60:40 Rule)
* **60% s.d. 70% Luas Canvas:** Didedikasikan untuk aset visual fotografi arsitektur dan kedalaman atmosfer.
* **30% s.d. 40% Luas Canvas:** Didedikasikan untuk hierarki tipografi editorial, badge kategori, dan signature footer.

---

### G. Negative Space Rules
* Jangan pernah mengisi seluruh canvas dengan teks atau kotak grafis padat.
* Wilayah aman teks (*text-safe regions*):
  - `FULL_BOTTOM`: Area Y 42% hingga 88% canvas untuk headline vertikal.
  - `SPLIT_LEFT`: Area X 7% hingga 50% canvas untuk layout kolom ganda.
  - `CENTER_TOP`: Area Y 8% hingga 35% canvas untuk minimal editorial quote.

---

### H. Depth & Layering Rules (13-Layer Stack)
```
Layer 0:  Canvas Base (Obsidian Navy #070B14)
Layer 1:  Background Asset (Pure Architectural Photography)
Layer 2:  Atmosphere & Haze (Ambient Twilight Gradient)
Layer 3:  Architecture Scene (Midground Facade Geometry)
Layer 4:  Main Focal Subject (Alpha-Masked Focal Subject)
Layer 5:  Supporting Objects (Metric Pills & Icons)
Layer 6:  Foreground Scrim (Negative Space Scrim for Contrast)
Layer 7:  Lighting Effects (Directional Side Light & Rim Light)
Layer 8:  Shadows (Ground Contact Occlusion & Drop Shadow)
Layer 9:  Depth Effects (Tone Mapping & Corner Vignette)
Layer 10: Graphic Elements (Category Eyebrow & Hairlines)
Layer 11: Deterministic Typography (Fitted Headline & Highlighting)
Layer 12: Brand Identity (NugiProperti Signature Watermark)
```

---

### I. Lighting Rules
* **Directional Key Light:** Cahaya utama jatuh dari sudut diagonal (45° dari atas kanan atau atas kiri).
* **Subject Rim Light:** Simulasi pantulan cahaya lembut pada kontur subjek untuk memisahkan subjek dari latar belakang gelap.
* **Ambient Lighting Glow:** Pendaran cahaya hangat (gold/cyan) dengan opacity 20–35% yang menyatu secara plausibel dengan pencahayaan lingkungan.

---

### J. Shadow Rules
* Bayangan harus bersifat directional sesuai arah cahaya utama.
* **Contact Shadow:** Berwarna `#04070E` dengan opacity 75%, radius blur 18px.
* **Drop Shadow pada Teks:** Offset Y +3px, X +2px, opacity 85% untuk menjamin keterbacaan 100% pada latar belakang apa pun (WCAG AAA).

---

### K. Color Grading Rules
* **`CINEMATIC_TWILIGHT`:** Contrast 1.14x, Saturation 0.95x, Cool Twilight tone bias (-0.05).
* **`PREMIUM_GOLD`:** Contrast 1.15x, Warm Amber tone bias (+0.18), Vignette 0.35x.
* **`DEEP_OBSIDIAN`:** Contrast 1.25x, Saturation 0.85x, Monochrome charcoal mood.
* **`TECH_CYAN`:** Contrast 1.12x, Electric cyan highlight boost (+0.12).

---

### L. Headline Treatment
* Maksimal 18–20 karakter per baris.
* Maksimal 2–4 baris total.
* Seluruh baris judul berada dalam safe zone margin (minimal 80px dari tepi kiri/kanan).
* Highlight kata kunci langsung menggunakan warna aksen brand yang relevan.

---

### M. Information Hierarchy
1. **Category Eyebrow:** `✦ EDUKASI PROPERTI`
2. **Main Headline:** `KENAPA LEADS BANYAK TAPI CLOSING RENDAH?`
3. **Subheadline Context:** `Masalah bukan pada biaya iklan, melainkan waktu respon tim sales.`
4. **Data Callout (Jika ada):** `[ +300% Kecepatan Respon ]`
5. **Brand Signature:** `⚡ NUGIPROPERTI | Editorial Art Direction`

---

### N. Visual Rhythm
* Elemen grafis aksen harus minimalis dan fungsional (garis pemisah 1px, badge pill halus, titik data grid).
* Hindari penumpukan elemen berat di satu sisi (*visual clutter*).

---

### O. Premium Quality Checklist (10 Aturan Uji)
1. [ ] Apakah visual terlihat seperti karya art director, bukan template instan?
2. [ ] Apakah rasio kontras teks terhadap latar belakang memenuhi standar WCAG AAA (> 7:1)?
3. [ ] Apakah subjek visual dan teks memiliki hierarki yang jelas?
4. [ ] Apakah pencahayaan subjek konsisten dengan latar belakang?
5. [ ] Apakah margin aman 80px terpenuhi tanpa teks terpotong?
6. [ ] Apakah aturan CTA terpenuhi (tidak ada tombol sales pada artikel edukasi)?
7. [ ] Apakah color grading terasa sinematik dan tidak oversaturated?
8. [ ] Apakah kata sorotan (*highlight words*) tepat dan bermakna?
9. [ ] Apakah resolusi kanvas tepat 1080 × 1350 piksel (4:5 rasio potret Instagram)?
10. [ ] Apakah signature watermark NugiProperti terpasang elegan di bagian bawah?

---

### P. Anti-Template Rules
* ❌ DILARANG menggunakan bingkai kartu rounded card putih/terang di atas background gelap.
* ❌ DILARANG menggunakan shape acak seperti lingkaran warna-warni, ombak (waves), atau ornamen Canva murahan.
* ❌ DILARANG membuat visual yang simetris kaku seperti slide presentasi biasa.

---

### Q. Anti-Generic-AI-Visual Rules
* ❌ DILARANG membiarkan model AI (Flux) menggambar teks, huruf, atau logo sembarangan.
* ❌ DILARANG menghasilkan gambar gedung dengan proporsi cacat atau surrealistik yang tidak masuk akal dalam arsitektur nyata.
* ✅ Seluruh teks dan tipografi WAJIB dirender 100% secara deterministik oleh engine Pillow Python.

---

### R. NugiProperti Signature Elements
1. **Eyebrow Prefix:** Simbol `✦` diikuti nama kategori huruf kapital.
2. **Precision Hairline:** Garis aksen tipis horizontal di samping badge kategori.
3. **Signature Watermark Footer:** `⚡ NUGIPROPERTI` di sudut kiri bawah dan `Editorial Art Direction` di sudut kanan bawah.

---

## 3. Spesifikasi Visual untuk 10 Tipe Konten Properti

| Tipe Konten | Nuansa Visual (*Visual Mood*) | Warna Aksen | Treatment Tipografi & Layout | CTA Policy |
| :--- | :--- | :--- | :--- | :---: |
| **`PROPERTY_PROBLEM`** | Chiaroscuro senja, sales gallery, maket arsitektur | Rose Alert (`#F43F5E`) | Headline diagnosis tajam, scrim asimetris gelap | `CTA_NONE` |
| **`PROPERTY_EDUCATION`** | Arsitektur modern, kaca bersih, pencahayaan alami | Sky Cyan (`#38BDF8`) | Penjelasan terstruktur, subheadline kontekstual | `CTA_NONE` |
| **`PROPERTY_INSIGHT`** | Infrastruktur jalan tol layang, senja keemasan | Sunset Gold (`#F59E0B`) | Headline makro ekonomi, garis tren pasar | `CTA_NONE` |
| **`NUMBER_LIST`** | Fasad ritmis bertingkat dengan kisi-kisi arsitektur | Amber Gold (`#F59E0B`) | Nomor indeks `01`, `02`, `03` dengan layout rapi | `CTA_NONE` |
| **`CASE_STUDY`** | Kawasan hunian rukost beroperasi penuh | Emerald Green (`#10B981`) | Box metrik data empiris `[ +300% ]` | `CTA_NONE` |
| **`DATA_EDITORIAL`** | Masterplan proyek, diagram yield keuangan | Cyan & Gold | Grid data institucional, pembagian kolom bersih | `CTA_NONE` |
| **`OPINION`** | Monokrom obsidian, teras penthouse malam hari | Indigo (`#6366F1`) | Tanda kutip raksasa `“`, tipografi berani | `CTA_NONE` |
| **`PROPERTY_SHOWCASE`** | Fasad unit rukost tropis modern, cahaya matahari | Champagne Gold (`#F59E0B`) | Pill spesifikasi unit, lokasi, dan harga | `CTA_OPTIONAL` |
| **`SOFT_SELLING`** | Gaya hidup residensial prestisius | Sky Cyan (`#38BDF8`) | Cerita naratif aspiratif, tanpa tombol jualan paksa | `CTA_NONE` |
| **`DIRECT_OFFER`** | Ruang konsultasi eksekutif modern | Emerald / Gold | Action card dengan tombol CTA konsultasi/audit | `CTA_REQUIRED` |

---

## 4. Protokol Pembuatan Visual Asset pada Flux

Prompt ke Flux diformulasikan dengan struktur fotografi arsitektur profesional murni:
```
[Shot Type & Camera Lens] + [Architectural Subject & Spatial Layout] + [Surrounding Environment & Context] + [Lighting Direction & Quality] + [Atmosphere & Color Palette] + [Negative Space Preservation Directive] + [Pure Photographic Quality Tokens]
```

**Contoh Prompt Standar:**
> *"Cinematic 35mm architectural low-angle photography of modern tropical student residential building facade with glass balconies, located in tranquil university township. Lighting: Golden hour late afternoon sun with warm natural shadows. Atmosphere: Prestigious, crisp architectural geometry. Preserve clean uncluttered dark negative space on the bottom half for editorial typography. 8k resolution, authentic concrete and timber textures, no text, no letters, no words, no watermark, no logo, pure photographic background asset."*
