# 🪟 Windows Desktop Packaging Plan: Nugi Content Factory

Rencana strategis pengemasan aplikasi menjadi installer mandiri Windows (`Setup.exe`) agar dapat di-install dan dijalankan oleh pengguna awam tanpa CLI.

---

## 1. Target Pengalaman Pengguna (End-User UX)
1. Pengguna men-download file installer: `Nugi_Content_Factory_Setup.exe`.
2. Pengguna menjalankan installer (Next ➔ Install ➔ Finish).
3. Ikon shortcut muncul di Desktop & Start Menu.
4. Pengguna melakukan double click pada ikon aplikasi.
5. Aplikasi terbuka dalam jendela desktop native (Electron / Tauri window).
6. Pengguna memasukkan API key (jika beralih dari Mock ke Live) di menu Pengaturan UI.
7. Pengguna dapat langsung membuat konten dan mengekspor hasilnya.

**User TIDAK BOLEH diwajibkan memahami:**
- Python runtime
- Node.js / npm
- Docker
- Git
- Command Prompt / Terminal
- Virtual Environment

---

## 2. Arsitektur Packaging Desktop

```
┌────────────────────────────────────────────────────────┐
│        Desktop Shell (Electron / Tauri / PyWebView)    │
│  • Window Management                                   │
│  • Native File Dialogs (Save Image to Desktop/Folder)  │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│      Bundled Single-Binary Backend (PyInstaller)       │
│  • Embedded Python Runtime + FastAPI                   │
│  • Embedded SQLite Engine (`nugi_content_factory.db`)  │
│  • Pillow Imaging Engine                               │
└────────────────────────────────────────────────────────┘
```

---

## 3. Komponen & Alur Bundling

### A. Backend Packaging (PyInstaller)
- Mengemas seluruh backend FastAPI dan dependensi Python ke dalam file executable binary mandiri (`engine.exe`).
- Menggunakan database SQLite lokal bawaan yang otomatis terbuat di direktori `AppData/Local/NugiContentFactory/`.

### B. Frontend Packaging (Vite Static Build)
- Menjalankan `npm run build` yang menghasilkan bundle HTML/CSS/JS statis di folder `dist/`.
- Frontend statis di-load langsung oleh shell desktop atau di-serve melalui engine lokal.

### C. Desktop Wrapper (Tauri / Electron)
- Mengawali lifecycle: Saat aplikasi dibuka, background engine otomatis dijalankan di port lokal dinamis.
- Saat aplikasi ditutup oleh user, proses engine otomatis dimatikan (*graceful shutdown*) tanpa proses zombie.

### D. Windows Installer (Inno Setup / NSIS)
- Menghasilkan installer executable Windows tunggal (`.exe`) yang terkompresi.
- Menangani instalasi file, shortcut desktop, asosiasi file, dan uninstaller bersih.
