# 🪟 Phase Windows Desktop & GitHub Actions Release Pipeline Implementation Plan

## 1. Executive Summary & Objective
Transform **Nugi Content Factory** into a production-grade, portable Windows x64 desktop application (`Setup.exe` installer + portable `.zip`) built autonomously through **GitHub Actions**.

### Non-Regression Absolute Rules:
- **Locked Visual DNA**: Dark obsidian palette (`#040711`), Electric neon violet (`#8B5CF6`), high-contrast typography, and Akademi Kripto editorial standards remain 100% untouched.
- **Locked Safezone**: Master canvas `1080 × 1350 px` with 3:4 profile grid resilience (`1012 × 1350 px`) and 1:1 square feed resilience strictly preserved.
- **Decoupled AI Providers**: LLM, Image, Compute, and Storage remain modular. RunPod is strictly **optional** (heavy workloads only) and **never** invoked for standard image generation.
- **Zero Developer PC Dependency**: All builds, dependencies, and packaging steps are reproducible inside GitHub Actions runner (`windows-latest`).

---

## 2. Desktop Shell Architecture & Rationale

```
┌────────────────────────────────────────────────────────┐
│   Desktop Shell (PyWebView with Edge WebView2 Runtime) │
│   • Native Windows 10/11 frame with NugiProperti Icon  │
│   • Dark theme background (#040711)                    │
│   • Single-process lifecycle & auto clean shutdown     │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│         FastAPI Embedded Engine (PyInstaller)          │
│   • Embedded Python 3.11 Runtime + Uvicorn Localhost   │
│   • Embedded Vite Static UI Mount (`/dist`)            │
│   • Pillow 13-Layer Compositing Engine                 │
│   • Modular Provider Engine (OpenRouter, Flux, etc.)   │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│      Persistent User Data (%LOCALAPPDATA%/...)         │
│   • `%LOCALAPPDATA%/Nugi Content Factory/config/`      │
│   • `%LOCALAPPDATA%/Nugi Content Factory/storage/`     │
│   • `%LOCALAPPDATA%/Nugi Content Factory/logs/`        │
│   • `%LOCALAPPDATA%/Nugi Content Factory/database.db`  │
└────────────────────────────────────────────────────────┘
```

### Technology Choice & Rationale:
- **Desktop Shell**: **PyWebView (Edge WebView2)**
  - *Why not Electron?* Electron bundles a ~180MB Chromium browser, requires Node runtime orchestration, and creates complex child-process IPC.
  - *Why PyWebView?* Uses Windows 10/11 pre-installed Microsoft Edge WebView2, produces a lightweight single-process binary (~35MB), has instant startup, and zero zombie process risk.
  - *Fallback*: If WebView2 is absent, automatically opens the local default browser tab seamlessly.

---

## 3. Persistent User Configuration & Security Strategy

### Directory Separation:
- **Application Binaries**: `C:\Program Files\Nugi Content Factory\` (Read-Only).
- **User Data & Settings**: `%LOCALAPPDATA%\Nugi Content Factory\` (Read/Write, survives application updates).
  - `config/provider_settings.json`: User AI API keys, base URLs, and model configurations.
  - `storage/assets/`: Rendered 1080x1350 editorial posters.
  - `logs/app.log`: Production diagnostics (API keys strictly masked).
  - `nugi_content_factory.db`: SQLite project & content metadata.

### API Key Protection:
- Zero hardcoded keys in source code or Git.
- Keys masked in API responses (`****...1234`).
- Frontend never embeds secret credentials.
- `SettingsModal.jsx` allows users to enter their own credentials and test connectivity.

---

## 4. Packaging & Distribution Pipeline

### Outputs:
1. **`Nugi-Content-Factory-Windows-x64-Setup.exe`**: Inno Setup installer supporting desktop shortcut, start menu entry, custom install path, and clean uninstallation.
2. **`Nugi-Content-Factory-Windows-x64-Portable.zip`**: Self-contained zip archive for zero-install execution.
3. **`SHA256SUMS.txt`**: Cryptographic integrity checksums.

---

## 5. GitHub Actions Release Workflow (`.github/workflows/build-release.yml`)

1. **Trigger**: Tag push (`v*`) or manual `workflow_dispatch`.
2. **Environment**: `windows-latest`.
3. **Build Steps**:
   - `actions/checkout@v4`
   - `actions/setup-python@v5` (Python 3.11)
   - `actions/setup-node@v4` (Node 20)
   - Install dependencies (`requirements.txt`, `npm ci`).
   - Run backend tests: `pytest` (Quality Gate).
   - Build frontend: `npm run build` in `frontend/`.
   - Build PyInstaller executable (`pyinstaller desktop.spec`).
   - Build Inno Setup installer (`iscc packaging/installer.iss`).
   - Package portable zip archive.
   - Run automated smoke test on packaged artifact.
   - Compute SHA256 checksums.
   - Upload GitHub Release assets.

---

## 6. Implementation Checklist & Work Breakdown

- [x] **Audit**: Codebase inspected, existing assets and paths mapped.
- [ ] **Data Directory Hardening**: Update `config.py` to use `%LOCALAPPDATA%` for storage, DB, logs, and config.
- [ ] **Static Frontend Mounting**: Update `backend/app/main.py` to serve Vite static files from `frontend/dist`.
- [ ] **Desktop Launcher**: Create `desktop_app.py` orchestrating background server and PyWebView desktop window.
- [ ] **Windows Icon Asset**: Generate `.ico` icon from official purple logo for Windows executable & installer.
- [ ] **PyInstaller Spec**: Create `packaging/desktop.spec` with all dependencies and asset bundling.
- [ ] **Inno Setup Script**: Create `packaging/installer.iss` for professional Windows installer.
- [ ] **Packaging Smoke Test**: Create `backend/tests/test_packaging_smoke.py` validating packaged readiness.
- [ ] **GitHub Actions Workflow**: Create `.github/workflows/build-release.yml`.
- [ ] **Documentation**: Create user & developer packaging guide in `docs/WINDOWS_DISTRIBUTION_GUIDE.md`.
- [ ] **Verification**: Run all 70+ tests and build verification.
