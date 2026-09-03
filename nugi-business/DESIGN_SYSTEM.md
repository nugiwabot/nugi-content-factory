# 🎨 DESIGN SYSTEM — NUGIPROPERTI

Identitas visual resmi untuk seluruh aset NUGIPROPERTI (website, file markdown, materi promosi).
Token di bawah ini **harus** dipakai di semua permukaan brand agar warna selalu matching dengan
Nugi Content Factory (`nugi-content-factory/frontend/src/styles/index.css` dan `docs/DESIGN_TOKENS.md`).

---

## 1. Sumber Kebenaran

- UI aplikasi & engine render: `nugi-content-factory/frontend/src/styles/index.css`
- Token semantik poster: `nugi-content-factory/docs/DESIGN_TOKENS.md`
- Dokumen ini: ringkasan kanonikal untuk repo freelance.

## 2. Color System

### Background (Obsidian Navy)
| Token | HEX / RGB | Fungsi |
| :--- | :--- | :--- |
| `bg_dark` | `#070b14` `(7,11,20)` | Latar utama |
| `bg_surface` | `#0c1220` `(12,18,32)` | Panel/navbar |
| `bg_card` | `rgba(15,23,42,0.75)` | Kartu glassmorphism |
| `bg_card_hover` | `rgba(22,34,60,0.85)` | Kartu hover |

### Teks
| Token | HEX | Fungsi |
| :--- | :--- | :--- |
| `text_main` | `#f8fafc` | Headline |
| `text_muted` | `#94a3b8` | Body |
| `text_dim` | `#64748b` | Metadata |

### Aksen (Semantik)
| Token | HEX | Fungsi |
| :--- | :--- | :--- |
| `accent_violet` | `#8b5cf6` | **Primer — AI / teknologi canggih** |
| `accent_violet_light` | `#a855f7` | Hover/glow violet |
| `accent_violet_soft` | `#c084fc` | Label & badge AI-tech |
| `accent_cyan` | `#38bdf8` | **Sekunder — sistem / properti-tech** |
| `accent_indigo` | `#6366f1` | Aksen bisnis/sistem |
| `accent_emerald` | `#10b981` | Pertumbuhan, closing, studi kasus |
| `accent_amber` | `#f59e0b` | Yield investasi & keuangan |
| `accent_rose` | `#f43f5e` | Peringatan, friksi, urgensi |

### Gradient Identitas Brand
- `gradient_primary: linear-gradient(135deg, #8b5cf6 0%, #38bdf8 100%)`
- `gradient_ambient_hero: radial-gradient(circle at 50% 0%, rgba(139,92,246,0.16), transparent 60%)`

### Pengecualian Fungsional
- `wa_green: #25d366` — **hanya** untuk tombol/float WhatsApp.

## 3. Radius & Shadow
- Radius: `sm 6px` · `md 12px` · `lg 18px` · `full 9999px`
- Shadow: `sm/md/lg` mengikuti Nugi Content Factory.

## 4. Tipografi
- Utama: **Plus Jakarta Sans** (400/500/600/700/800)
- Teknis: **JetBrains Mono** untuk section-badge, step-number, code-preview, counter slide.

## 5. Aturan Pemakaian Warna
1. Gradient violet→cyan dipakai untuk tombol CTA utama & elemen signature brand.
2. Violet `#8b5cf6` dipakai untuk elemen AI/teknologi; cyan `#38bdf8` untuk elemen sistem/properti.
3. Hijau WhatsApp `#25d366` HANYA di tombol WhatsApp.
4. Emerald untuk angka pertumbuhan, amber untuk yield/keuangan, rose untuk masalah/urgensi.

## 6. Larangan (Anti "AI-Generated Look")
- ❌ Jangan gunakan emoji sebagai ikon — pakai SVG inline stroke 24×24.
- ❌ Jangan aksen cyan-only (tanpa violet).
- ❌ Jangan biru lama `#3b82f6` / `#2563eb` / `#0ea5e9`.
- ❌ Jangan `--accent-red: #ef4444`; gunakan `#f43f5e`.
- ❌ Jangan gradient hijau-ungu / warna pelangi acak.

## 7. Rujukan
- `nugi-content-factory/docs/DESIGN_TOKENS.md`
- `nugi-content-factory/docs/BRAND_DESIGN_SYSTEM.md`
