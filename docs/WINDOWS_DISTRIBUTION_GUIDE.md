# 📦 Nugi Content Factory: Windows Distribution & Release Guide

Panduan lengkap instalasi, packaging Windows desktop, konfigurasi provider, dan pipeline rilis otomatis GitHub Actions untuk **Nugi Content Factory**.

---

## 1. 🚀 Ringkasan Arsitektur Desktop

Nugi Content Factory didistribusikan sebagai aplikasi desktop mandiri Windows 64-bit (`Setup.exe` dan portable `.zip`).

```
┌────────────────────────────────────────────────────────┐
│   Desktop Shell (PyWebView with Edge WebView2)         │
│   • Frameless / Modern Window dengan Icon NugiProperti │
│   • Dark Theme Background (#040711)                    │
│   • Auto-launch backend & graceful process shutdown    │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│         FastAPI Engine (PyInstaller Bundled)           │
│   • Python 3.11 Runtime + SQLite Embedded Engine       │
│   • Vite Frontend UI Mount (/dist)                     │
│   • Pillow 13-Layer Compositing Engine                 │
│   • Modular Provider Architecture (OpenRouter, Flux)   │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│      Persistent User Data (%LOCALAPPDATA%/...)         │
│   • %LOCALAPPDATA%\Nugi Content Factory\config\        │
│   • %LOCALAPPDATA%\Nugi Content Factory\storage\       │
│   • %LOCALAPPDATA%\Nugi Content Factory\logs\          │
│   • %LOCALAPPDATA%\Nugi Content Factory\database.db    │
└────────────────────────────────────────────────────────┘
```

---

## 2. 💻 Pengalaman Pengguna Akhir (*End-User Experience*)

1. Download **`Nugi-Content-Factory-Windows-x64-Setup.exe`**.
2. Jalankan installer (Next ➔ Install ➔ Finish).
3. Buka **Nugi Content Factory** dari Desktop Shortcut atau Start Menu.
4. Klik tombol **Pengaturan (⚙️)** di pojok kanan atas untuk memasukkan API Key OpenRouter / Flux sesuai kebutuhan.
5. Klik **Test Connection** ➔ Simpan Pengaturan.
6. Mulai membuat konten visual editorial beresolusi tinggi 1080 × 1350 px.

---

## 3. 🛡️ Keamanan & Lokasi Penyimpanan Konfigurasi

- **File Executable Aplikasi**: `C:\Program Files\Nugi Content Factory\` *(Read-Only)*
- **Data Konfigurasi & Asset Pengguna**: `%LOCALAPPDATA%\Nugi Content Factory\` *(Read/Write)*
  - `config/provider_settings.json`: Menyimpan API keys dan model yang dikonfigurasi user.
  - `storage/assets/`: Menyimpan hasil render gambar visual 1080x1350 px.
  - `logs/app.log`: Log diagnostik sistem (API Key disensor/dimask otomatis).
  - `nugi_content_factory.db`: Database SQLite lokal untuk riwayat konten dan brief.

> **PENTING**: Saat aplikasi diupdate ke versi baru, konfigurasi API Key dan asset yang digenerate **TIDAK AKAN HILANG** karena disimpan di direktori data pengguna.

---

## 4. 🤖 Konfigurasi Provider AI

### A. LLM Provider (Copywriting & Strategy)
Dapat dikonfigurasi langsung dari UI Settings:
- **OpenRouter Gateway (Default)**: Model `google/gemini-2.5-flash-lite`, Claude 3.5, dll.
- **OpenAI / OpenAI-Compatible**: Untuk endpoint kustom, Ollama, vLLM, DeepSeek, Groq.
- **Anthropic Messages API**: Untuk Claude direct.
- **Google Gemini Direct API**: Untuk Gemini direct.
- **Mock Provider**: Untuk pengujian offline tanpa kuota.

### B. Image Provider (Fotografi Arsitektural)
- **Flux / Black Forest Labs (Default)**: Model `flux-2-klein-9b`, `flux-1.1-pro`.
- **OpenAI DALL-E / OpenRouter Image**: Model `dall-e-3`.
- **Custom SD WebUI / ComfyUI**: Endpoint lokal `http://localhost:7860`.
- **Mock Provider**: Generator gambar placeholder lokal untuk pengujian.

### C. Compute Provider (RunPod)
- **RunPod bersifat OPSIONAL** dan hanya digunakan untuk tugas komputasi berat (video rendering, heavy local model inference).
- **Pembuatan gambar standar TIDAK MEMERLUKAN RunPod.**

---

## 5. 🏗️ Cara Build Lokal (Developer Workflow)

### Menjalankan Mode Development:
```powershell
# Terminal 1: Backend
cd backend
python -m uvicorn app.main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend
npm run dev
```

### Membangun Paket Distribusi Windows Lokal:
```powershell
# Jalankan script otomasi packaging
python packaging/build_windows_dist.py
```
Hasil output akan berada di folder `release/`:
- `Nugi-Content-Factory-Windows-x64-Setup.exe`
- `Nugi-Content-Factory-Windows-x64-Portable.zip`
- `SHA256SUMS.txt`

---

## 6. 🌐 Pipeline Rilis Otomatis GitHub Actions

Workflow GitHub Actions (`.github/workflows/build-release.yml`) berjalan secara otomatis di runner `windows-latest`:

1. **Membuat Rilis Baru**:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```
2. **Proses yang Dijalankan GitHub Actions**:
   - Menjalankan seluruh test backend (`pytest`).
   - Melakukan build frontend production (`npm run build`).
   - Melakukan smoke testing packaging.
   - Meng-compile executable PyInstaller.
   - Meng-compile installer Inno Setup.
   - Mengompresi arsip ZIP portabel.
   - Menghitung checksum SHA-256.
   - Mempublikasikan **GitHub Release** lengkap dengan file binary `.exe` dan `.zip`.

---

## 7. 🔧 Troubleshooting

| Kendala | Penyebab | Solusi |
| :--- | :--- | :--- |
| **Port 8000 sudah digunakan** | Ada aplikasi lain yang memakai port 8000. | Launcher otomatis mendeteksi dan beralih ke port 8001–8050. |
| **Gagal generate gambar** | API Key Flux belum diisi atau kuota habis. | Buka menu Pengaturan (⚙️), masukkan API Key Flux, klik *Test Image Connection*. |
| **Gagal generate copywriting** | API Key OpenRouter belum diisi. | Masukkan API Key OpenRouter di menu Pengaturan, klik *Test LLM Connection*. |
| **Antivirus memblokir .exe** | Binary baru belum memiliki sertifikat code-signing komersial. | Pilih *Run Anyway* atau *Allow on Device*. |
