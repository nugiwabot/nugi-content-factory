# 🎨 Semantic Design Tokens: Nugi Content Factory

Sistem token semantik menjamin tidak ada kode warna HEX atau ukuran sembarangan yang tersebar secara *hardcoded* di engine rendering.

---

## 1. Color System (Semantic Color Tokens)

| Token Semantik | Nilai HEX | Nilai RGB | Fungsi & Penggunaan |
| :--- | :--- | :--- | :--- |
| `background_dark` | `#070b14` | `(7, 11, 20)` | Latar belakang canvas gelap utama (*Obsidian Navy*). |
| `surface_dark` | `#0c1220` | `(12, 18, 32)` | Latar belakang container pendukung. |
| `surface_card` | `#0f172a` | `(15, 23, 42)` | Kartu glassmorphism utama dengan opacity 85%. |
| `surface_elevated` | `#162238` | `(22, 34, 56)` | Kartu elevated dan box metrik hasil. |
| `text_primary` | `#ffffff` | `(255, 255, 255)` | Teks headline dan display kontras tinggi. |
| `text_secondary` | `#cbd5e1` | `(203, 213, 225)` | Teks subjudul dan nilai metrik sekunder. |
| `text_muted` | `#94a3b8` | `(148, 163, 184)` | Deskripsi penjelas dan body copywriting. |
| `text_dim` | `#64748b` | `(100, 116, 139)` | Metadata, timestamp, dan teks watermark footer. |
| `accent_primary` | `#38bdf8` | `(56, 189, 248)` | *Electric Sky Cyan* — Aksen teknologi, otoritas, tombol CTA. |
| `accent_secondary` | `#6366f1` | `(99, 102, 241)` | *Deep Indigo* — Aksen bisnis & solusi sistem software. |
| `accent_gold` | `#f59e0b` | `(245, 158, 11)` | *Warm Amber/Gold* — Aksen listicle, yield investasi, & keuangan. |
| `accent_emerald` | `#10b981` | `(16, 185, 129)` | *Emerald Green* — Aksen pertumbuhan, conversion speed, studi kasus. |
| `accent_rose` | `#f43f5e` | `(244, 63, 94)` | *Rose Red* — Aksen peringatan masalah, friksi sales, & urgensi. |

---

## 2. Typography System (Mobile-First Hierarchy)

| Level Token | Ukuran Standar | Line Height | Max Karakter / Baris | Max Baris Aman |
| :--- | :--- | :--- | :--- | :--- |
| **Display** | 64pt (Auto-fit 58-28) | 1.18x | 18-20 karakter | 3-4 baris |
| **H1** | 52pt | 1.22x | 22-24 karakter | 3-4 baris |
| **H2** | 38pt | 1.26x | 28 karakter | 4 baris |
| **Body** | 24-26pt | 1.35x | 34-38 karakter | 4 baris |
| **Label / Badge** | 20-22pt | 1.20x | 30 karakter | 1 baris |
| **Caption** | 18pt | 1.20x | 45 karakter | 2 baris |
| **CTA Button** | 24pt | 1.10x | 24 karakter | 1 baris |

---

## 3. Spacing System (8pt Grid)
* `xs`: 4px
* `sm`: 8px
* `md`: 16px
* `lg`: 24px
* `xl`: 32px
* `xxl`: 48px
* `xxxl`: 64px
* `huge`: 80px
