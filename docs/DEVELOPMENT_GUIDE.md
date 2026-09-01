# 🛠️ Development Guide: Nugi Content Factory

Panduan instalasi, konfigurasi, dan alur kerja pengembangan harian.

## 1. Prasyarat Sistem
* **Python:** 3.10 atau 3.11+
* **Node.js:** v18+ atau v20+ (dengan `npm`)
* **Git**

---

## 2. Instalasi Langkah demi Langkah

### Langkah A: Setup Backend
```bash
cd backend
python -m pip install -r requirements.txt
```

### Langkah B: Setup Frontend
```bash
cd frontend
npm install
```

---

## 3. Menjalankan Server Pengembangan

### Opsi 1: One-Click Starter (PowerShell)
Di root direktori project:
```powershell
.\scripts\start_dev.ps1
```

### Opsi 2: Manual Terminal

**Terminal 1 (Backend FastAPI):**
```bash
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
* API Server: `http://127.0.0.1:8000`
* Swagger Interactive Docs: `http://127.0.0.1:8000/docs`

**Terminal 2 (Frontend React):**
```bash
cd frontend
npm run dev
```
* Frontend UI: `http://localhost:5173`

---

## 4. Menjalankan Automated Test Suite
```bash
cd backend
python -m pytest -v
```
Atau menggunakan helper script:
```powershell
.\scripts\run_tests.ps1
```
