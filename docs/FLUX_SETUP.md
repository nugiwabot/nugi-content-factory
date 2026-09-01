# ⚡ Panduan Konfigurasi & Setup Flux API (Black Forest Labs)
**Nugi Content Factory**

Panduan resmi untuk menghubungkan API Image Generation **Flux** (Black Forest Labs) secara aman tanpa risiko kebocoran secret key.

---

## 1. Konfigurasi Environment Variable

Sistem Nugi Content Factory menggunakan konfigurasi 12-factor application melalui file `.env` di root direktori project (`c:\Users\Nugi\Documents\nugi-content-factory\.env`).

Variabel resmi yang digunakan:

```env
# 1. Aktifkan Image Provider ke Flux
IMAGE_PROVIDER=flux

# 2. Masukkan API Key Black Forest Labs Anda
FLUX_API_KEY=your_actual_bfl_api_key_here

# 3. Model Identifier (Default: flux-1.1-pro)
FLUX_MODEL=flux-1.1-pro

# 4. Base Gateway URL (Default: https://api.bfl.ml/v1)
FLUX_BASE_URL=https://api.bfl.ml/v1
```

> [!NOTE]
> Pilihan model yang didukung:
> - `flux-1.1-pro` (Kualitas fotografi tertinggi & resolusi 8k - Direkomendasikan)
> - `flux-dev` (Development & high aesthetic quality)
> - `flux-schnell` (Ultra-fast generation)

---

## 2. Cara Memasukkan API Key

1. Buka file `.env` di root repository:
   ```
   c:\Users\Nugi\Documents\nugi-content-factory\.env
   ```
2. Isi nilai `FLUX_API_KEY=` dengan API key Anda dari [Black Forest Labs (api.bfl.ml)](https://api.bfl.ml/).
3. Ubah `IMAGE_PROVIDER=mock` menjadi `IMAGE_PROVIDER=flux`.
4. Simpan file `.env`.

> [!IMPORTANT]
> File `.env` **TIDAK AKAN PERNAH** ter-commit ke Git karena sudah diproteksi secara ketat di `.gitignore`.

---

## 3. Cara Menjalankan Aplikasi

Jalankan backend server:
```powershell
# Dari direktori root project
cd c:\Users\Nugi\Documents\nugi-content-factory
.\scripts\run_backend.ps1
```

Jalankan frontend UI:
```powershell
# Dari direktori frontend
cd c:\Users\Nugi\Documents\nugi-content-factory\frontend
npm run dev
```
Buka browser di: `http://localhost:5173`.

---

## 4. Cara Mengetes Koneksi Flux (Test Connection)

Anda dapat mengetes koneksi Flux melalui 2 cara:

### Cara A: Melalui UI (Settings Modal)
1. Buka aplikasi di browser (`http://localhost:5173`).
2. Klik ikon ⚙️ **Settings** di header kanan atas.
3. Pada kartu **Flux Image Provider**, klik tombol **Test Connection**.
4. Sistem akan menampilkan status real-time:
   - 🟢 `SUCCESS`: API Key valid dan koneksi berhasil.
   - 🔵 `NOT_CONFIGURED`: API Key belum diisi (menggunakan Mock fallback).
   - 🔴 `FAILED`: API Key salah atau terjadi gangguan jaringan.

### Cara B: Melalui Endpoint REST API / Terminal
```powershell
curl -X GET http://127.0.0.1:8000/api/v1/health/flux
```
Response aman (tanpa menampilkan secret):
```json
{
  "status": "SUCCESS",
  "configured": true,
  "provider": "FluxImageProvider",
  "model": "flux-1.1-pro",
  "endpoint": "https://api.bfl.ml/v1",
  "message": "Flux API connection verified successfully."
}
```

---

## 5. Cara Mengetahui Apakah Flux Sedang Aktif

Ketika Anda melakukan generate visual di **AI Content Studio**:
- Jika `IMAGE_PROVIDER=flux` dan `FLUX_API_KEY` valid: Log backend akan mencatat pemanggilan ke endpoint Flux dan menghasilkan background murni fotografi real-time.
- Jika `FLUX_API_KEY` kosong atau terjadi timeout/error: Sistem secara otomatis beralih ke `MockImageProvider` tanpa menyebabkan aplikasi crash (*zero downtime fallback*).

---

## 6. Troubleshooting & Pertanyaan Umum

| Kendala | Penyebab | Solusi |
| :--- | :--- | :--- |
| **Status: NOT_CONFIGURED** | `FLUX_API_KEY` masih kosong di `.env`. | Buka `.env` dan masukkan API key Anda, lalu restart backend. |
| **Status: FAILED (Authentication failed)** | API Key salah / expired / kredit habis. | Periksa saldo akun di portal api.bfl.ml dan update key di `.env`. |
| **Gambar masih bernuansa mock** | `IMAGE_PROVIDER` masih bernilai `mock`. | Ubah `IMAGE_PROVIDER=flux` pada `.env`. |
| **Network Timeout** | Koneksi internet lambat / endpoint terblokir. | Pastikan `FLUX_BASE_URL=https://api.bfl.ml/v1` dapat diakses dari jaringan Anda. |

---

## 7. Aturan Keamanan (Security Rules)

1. **Never Commit Secrets:** Jangan pernah menulis API key asli ke file `.env.example`, kode Python, file JavaScript/React, atau commit Git.
2. **Backend-Only Access:** Kunci API Flux hanya dibaca oleh backend (`FluxImageProvider`). Frontend tidak pernah menerima atau menyimpan kunci API.
3. **No Key in Logs:** Log aplikasi hanya menampilkan endpoint dan status HTTP tanpa mencetak token otentikasi.
