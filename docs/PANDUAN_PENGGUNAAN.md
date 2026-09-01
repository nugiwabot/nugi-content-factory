# 📖 Panduan Penggunaan — Nugi Content Factory
### Platform Produksi Konten Pemasaran Properti Berbasis AI & 13-Layer Compositing Engine

Selamat datang di **Nugi Content Factory**! Aplikasi ini dirancang khusus untuk memproduksi konten pemasaran properti berkonversi tinggi secara otomatis, estetik, dan konsisten dengan standar editorial modern.

---

## 🚀 1. Cara Menggunakan AI Agent Copilot (Chat Mode)

Antarmuka utama aplikasi ini menggunakan **Conversational AI Agent**. Anda tidak perlu mengisi formulir yang rumit, cukup ajak AI berdiskusi seperti asisten pribadi Anda.

### A. Memulai Sapaan & Diskusi Strategi
Ketik di kolom chat bawah:
> *"Halo, kamu bisa bantu saya apa saja?"*  
> *"Saya mau buat konten edukasi untuk investor pemula, ada ide angle yang menarik?"*

**AI Agent akan:**
1. Membalas obrolan Anda dengan analisis strategi pemasaran properti.
2. Memberikan 3–4 rekomendasi topik siap generate yang bisa Anda klik langsung.

### B. Meminta AI Membuat Konten Otomatis
Ketik instruksi atau topik apa saja yang ingin Anda buat:
> *"Bikinkan konten edukasi tentang bahaya beli tanah tanpa sertifikat SHM di Bandung"*  
> *"Buatkan postingan kenapa rukost dekat kampus selalu cepat tersewa"*  
> *"Bahas 3 kesalahan tim sales saat follow up leads iklan properti"*

**AI Agent akan secara otomatis:**
1. 🧠 **Menganalisis Target Audiens & Market Friction**
2. ✍️ **Merumuskan Headline Hook (PAS/AIDA) & Caption Lengkap**
3. 🎨 **Mengarahkan Art Direction Visual & Konsep Pencahayaan 3D**
4. 📐 **Merender Poster 1080x1350 dengan 13-Layer Compositing & Safezone Instagram**

### C. Melakukan Revisi Lewat Chat
Setelah poster selesai di-render, Anda bisa meminta revisi langsung di chat:
* *"Ubah headline-nya jadi lebih provokatif"*
* *"Ganti visualnya jadi ruko modern 3 lantai"*
* *"Tulis ulang captionnya dengan gaya yang lebih santai"*

---

## ⚡ 2. Fitur Quick Action & Export

Di setiap kartu hasil poster yang muncul di dalam chat, tersedia tombol cepat:

1. **📥 Unduh HD**: Mengunduh poster resolusi penuh 1080x1350 langsung ke komputer Anda (folder *Downloads*).
2. **📋 Salin Caption**: Menyalin teks caption Instagram lengkap dengan format rapi dan hashtag yang relevan.
3. **🛡️ Audit Safezone**: Menampilkan garis panduan batas aman Instagram (4:5) agar teks dan logo tidak terpotong di feed.
4. **🔄 Variasi Headline Lain**: Membuat alternatif judul visual baru tanpa mengubah gambar.
5. **🎨 Regenerate Visual**: Merender ulang konsep gambar arsitektur baru.

---

## ⚙️ 3. Konfigurasi AI Provider (OpenRouter & Flux)

Aplikasi ini mendukung multi-provider AI yang dapat diatur melalui file `.env` atau tombol **Settings (⚙️)** di pojok kanan atas aplikasi:

### Konfigurasi `.env`:
* **OpenRouter LLM**:
  ```env
  LLM_PROVIDER=openrouter
  OPENROUTER_API_KEY=sk-or-v1-...
  OPENROUTER_MODEL=gemini-2.5-flash-lite
  ```
* **Flux Image Generation**:
  ```env
  IMAGE_PROVIDER=flux
  FLUX_API_KEY=bfl_...
  FLUX_MODEL=flux-2-klein-9b
  ```

---

## 📚 4. Indeks Lengkap Dokumentasi Teknis

Seluruh dokumentasi teknis mendalam tersedia di dalam folder `docs/`:

| Nama File Dokumentasi | Deskripsi Isi |
| :--- | :--- |
| **[ARCHITECTURE.md](file:///c:/Users/Nugi/Documents/nugi-content-factory/docs/ARCHITECTURE.md)** | Arsitektur menyeluruh sistem, service orchestration, & data flow |
| **[BRAND_DESIGN_SYSTEM.md](file:///c:/Users/Nugi/Documents/nugi-content-factory/docs/BRAND_DESIGN_SYSTEM.md)** | DNA visual brand NugiProperti, palet warna ungu obsidian, & tipografi |
| **[DATA_MODEL.md](file:///c:/Users/Nugi/Documents/nugi-content-factory/docs/DATA_MODEL.md)** | Skema database SQLite/PostgreSQL (Briefs, Content, Assets, Jobs) |
| **[DESIGN_SPECIFICATION.md](file:///c:/Users/Nugi/Documents/nugi-content-factory/docs/DESIGN_SPECIFICATION.md)** | Spesifikasi struktur 13-layer compositing engine & koordinat visual |
| **[FLUX_SETUP.md](file:///c:/Users/Nugi/Documents/nugi-content-factory/docs/FLUX_SETUP.md)** | Panduan integrasi Black Forest Labs (BFL) Flux API |
| **[PHASE_03D_EDITORIAL_DESIGN_DNA.md](file:///c:/Users/Nugi/Documents/nugi-content-factory/docs/PHASE_03D_EDITORIAL_DESIGN_DNA.md)** | Formula 8 Arketipe Editorial properti & Safezone Enforcement |
| **[TECH_STACK.md](file:///c:/Users/Nugi/Documents/nugi-content-factory/docs/TECH_STACK.md)** | Daftar teknologi lengkap (FastAPI, React, Vite, PyInstaller, Inno Setup) |
| **[WINDOWS_DISTRIBUTION_GUIDE.md](file:///c:/Users/Nugi/Documents/nugi-content-factory/docs/WINDOWS_DISTRIBUTION_GUIDE.md)** | Panduan kompilasi installer `.exe`, CI/CD GitHub Actions, & portable zip |

---

*Dokumentasi ini diperbarui secara otomatis seiring perkembangan versi Nugi Content Factory.*
