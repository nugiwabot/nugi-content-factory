# ⚡ Nugi Content Factory

**Internal AI Content Production System for High-Conversion Property Marketing**

---

## 1. Apa Itu Nugi Content Factory?
**Nugi Content Factory** adalah platform modular produksi konten pemasaran berbasis AI yang dirancang khusus untuk memproduksi materi promosi berkonversi tinggi, konsisten, dan scalable bagi industri properti (Developer, Principal Agen, Marketing Manager, dan Tim Sales).

### 🎯 Prinsip Utama Produk
* **LLM is a Reasoning Engine:** AI digunakan untuk menyusun sudut pandang (*angle*), *headline*, *hook*, dan *caption* — bukan sebagai renderer gambar.
* **Image Model for Backgrounds:** Model visual hanya menghasilkan latar belakang grafis tanpa teks atau logo.
* **Deterministic Rendering:** Tipografi, badge kategori, padding, dan penempatan logo dirender secara pasti (*pixel-perfect*) menggunakan Python Pillow.
* **Zero API Cost for Tests:** Menggunakan layer abstraksi provider (`MockLLMProvider`, `MockImageProvider`) sehingga pengujian otomatis 100% gratis dan offline-ready.

---

## 2. Arsitektur Singkat

```
Frontend (React + Vite) 
        ↓  REST API (HTTP/JSON)
Application API (FastAPI)
        ↓
Application Services (Orchestration, Job, QA)
        ↓
AI & Rendering Layer (LLMProvider, ImageProvider, Deterministic Pillow Engine)
        ↓
Persistence Layer (SQLAlchemy 2.0 / SQLite / PostgreSQL & Local Storage)
```

---

## 3. Prasyarat Sistem (Developer Requirements)
* **Python:** 3.10 atau 3.11+
* **Node.js:** v18+ atau v20+
* **npm:** v9+ atau v10+

---

## 4. Instalasi & Setup Lingkungan Bersih

### Backend Setup
```bash
cd backend
python -m pip install -r requirements.txt
```

### Frontend Setup
```bash
cd frontend
npm install
```

---

## 5. Konfigurasi (`.env`)
Salin file template konfigurasi:
```bash
cp .env.example .env
```
Variabel konfigurasi utama:
* `APP_ENV`: `development` | `testing` | `production`
* `DATABASE_URL`: `sqlite:///./nugi_content_factory.db` (Default SQLite, siap PostgreSQL)
* `LLM_PROVIDER`: `mock` (Default Phase 1)
* `IMAGE_PROVIDER`: `mock` (Default Phase 1)
* `STORAGE_BASE_DIR`: `./storage/assets`

---

## 6. Cara Menjalankan Aplikasi

### Opsi 1: One-Click PowerShell Script (Disarankan di Windows)
Di root folder project, jalankan:
```powershell
.\scripts\start_dev.ps1
```

### Opsi 2: Manual Terminal

**Terminal 1 — Backend API (FastAPI):**
```bash
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
* Backend API: `http://127.0.0.1:8000`
* Swagger Interactive Docs: `http://127.0.0.1:8000/docs`

**Terminal 2 — Frontend UI (React + Vite):**
```bash
cd frontend
npm run dev
```
* Frontend Dashboard: `http://localhost:5173`

---

## 7. Cara Menjalankan Automated Test Suite
Di folder `backend/`:
```bash
python -m pytest -v
```
Atau jalankan script:
```powershell
.\scripts\run_tests.ps1
```
*Semua 17 unit test & integration test akan berjalan dan memvalidasi seluruh pipeline tanpa memerlukan kuota API berbayar.*

---

## 8. Struktur Direktori Repository

```
nugi-content-factory/
├── backend/
│   ├── app/
│   │   ├── api/v1/         # REST API route handlers (projects, briefs, content, jobs, assets, health)
│   │   ├── core/           # Config (Pydantic Settings), Logging, Error handlers
│   │   ├── models/         # SQLAlchemy 2.0 ORM models
│   │   ├── schemas/        # Pydantic v2 validation schemas
│   │   ├── providers/      # LLMProvider, ImageProvider, StorageProvider abstractions & Mocks
│   │   ├── rendering/      # Deterministic Pillow Rendering Engine & Layout calculations
│   │   ├── services/       # OrchestrationService, JobService, QAService
│   │   ├── database.py     # Database engine & session dependency
│   │   └── main.py         # FastAPI application entrypoint
│   ├── tests/              # 17 Unit & Integration test suites
│   ├── requirements.txt    # Backend dependencies
│   └── pyproject.toml      # Pytest & package configuration
├── frontend/
│   ├── src/
│   │   ├── components/     # UI Components (Header, Sidebar, BriefCreator, ContentStudio, etc.)
│   │   ├── services/       # Axios API client
│   │   ├── styles/         # Ultra-clean Dark Theme CSS Design Tokens
│   │   ├── App.jsx         # Root React component
│   │   └── main.jsx        # React entrypoint
│   ├── package.json        # Frontend dependencies
│   └── vite.config.js      # Vite proxy configuration
├── docs/                   # Full documentation suite (Vision, Architecture, Data Model, etc.)
├── scripts/                # Helper PowerShell scripts (start_dev.ps1, run_tests.ps1)
├── storage/assets/         # Rendered image assets directory
├── .env.example            # Environment configuration template
├── .gitignore              # Standard git exclusion rules
└── README.md               # Main documentation
```

---

## 9. Troubleshooting Dasar

1. **Port 8000 atau 5173 sudah digunakan:**
   Ubah port di file `.env` untuk backend (`PORT=8001`) atau di `vite.config.js` untuk frontend.
2. **Database Schema Reset:**
   Jika ingin mereset data lokal, cukup hapus file `nugi_content_factory.db` di folder `backend/`. Aplikasi akan otomatis membuat ulang skema bersih saat dijalankan kembali.
3. **Module Not Found saat menjalankan pytest:**
   Pastikan menjalankan pytest dengan perintah `python -m pytest -v` dari dalam direktori `backend/`.

---

## 10. Roadmap & Status
* **Phase 1: Foundation Architecture:** ✅ **COMPLETED (17/17 Tests Passed)**
* **Phase 2: Brand & Design Intelligence:** ✅ **COMPLETED (35/35 Tests Passed)**
* **Phase 3A: Professional Editorial Visual Engine:** ✅ **COMPLETED (41/41 Tests Passed)**
  - Content -> Art Direction -> Visual Composition -> Render
  - 7 Editorial Archetypes (`HERO_IMAGE_EDITORIAL`, `SPLIT_EDITORIAL`, `CINEMATIC_OVERLAY`, `DATA_EDITORIAL`, `LIST_EDITORIAL`, `MINIMAL_EDITORIAL`, `PROPERTY_SHOWCASE`)
  - Strict CTA Business Rules (`CTA_NONE`, `CTA_OPTIONAL`, `CTA_REQUIRED`)
  - Flux Provider Architecture with Graceful Mock Fallback
  - Visual Prompt Specification with Negative Space Awareness
  - Extended Editorial Visual QA Engine (41/41 Tests Passing)
* **Phase 3B: Content & Art Direction AI Agent:** *Pending Next Phase*
* **Phase 4: Windows Desktop Packaging (`Setup.exe`):** *Documented in `docs/WINDOWS_PACKAGING_PLAN.md`*
