# 🏛️ System Architecture: Nugi Content Factory

## 1. High-Level Architectural Diagram

```
┌────────────────────────────────────────────────────────┐
│               Frontend Layer (React + Vite)            │
│         [Brief Creator]  [Studio]  [Projects]          │
└───────────────────────────┬────────────────────────────┘
                            │ REST / JSON (HTTP)
┌───────────────────────────▼────────────────────────────┐
│            Application API Layer (FastAPI)             │
│   /health   /projects   /briefs   /content   /jobs     │
└───────────────────────────┬────────────────────────────┘
                            │ Service Invocations
┌───────────────────────────▼────────────────────────────┐
│                  Application Services                  │
│       [Orchestration]   [JobService]   [QAService]     │
└─────────────┬──────────────────┬─────────────────┬─────┘
              │                  │                 │
┌─────────────▼──────┐ ┌─────────▼──────┐ ┌────────▼─────┐
│  AI Provider Layer │ │ Image Provider │ │ Deterministic│
│   (LLMProvider)    │ │(ImageProvider) │ │Render Engine │
│  • MockLLMProvider │ │• MockImageGen  │ │(Pillow Engine│
│  • (Future OpenAI) │ │• (Future Flux) │ │& Layout)     │
└─────────────┬──────┘ └─────────┬──────┘ └────────┬─────┘
              │                  │                 │
┌─────────────▼──────────────────▼─────────────────▼─────┐
│                 Persistence & Storage                  │
│   • Database (SQLAlchemy / SQLite / PostgreSQL)        │
│   • StorageProvider (LocalStorageProvider -> ./storage)│
└────────────────────────────────────────────────────────┘
```

## 2. Layer Responsibilities

### A. Presentation Layer (Frontend)
- React 18 SPA dengan Vite 5.
- Dark-mode responsive UI tanpa dependensi CSS framework berat.
- Axios client dengan error handling otomatis dan interaktif.

### B. API Layer (FastAPI Backend)
- Validasi data ketat menggunakan Pydantic v2.
- Routing RESTful berbasis modul (`/api/v1/*`).
- Dependency injection untuk database session dan provider factory.

### C. Services & Orchestration
- `OrchestrationService`: Mengatur alur: Brief ➔ LLM Reasoning ➔ Background Generation ➔ Deterministic Graphic Rendering ➔ QA Evaluation ➔ DB Persistence.
- `JobService`: Mengelola siklus status job (`QUEUED`, `RUNNING`, `COMPLETED`, `FAILED`).
- `QAService`: Memeriksa kepatuhan panjang teks, kontras WCAG, dan guardrail klaim properti.

### D. Provider Abstraction Layer
- Mengisolasi panggilan AI pihak ketiga dari logika bisnis.
- Memungkinkan pengujian otomatis (*automated testing*) berjalan 100% offline dengan `MockLLMProvider` dan `MockImageProvider`.

### E. Deterministic Rendering Engine
- Menjamin hasil visual akhir (*final graphic*) selalu tajam, bebas halusinasi tipografi, dan sesuai spesifikasi layout 1080x1080.
