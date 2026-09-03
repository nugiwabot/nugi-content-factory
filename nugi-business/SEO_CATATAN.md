# Catatan Perbaikan Lanjutan — Website NUGIPROPERTI (nugi.biz.id)

Dokumen ini berisi pekerjaan yang **belum selesai / menyusul**, dikumpulkan agar
bisa dikerjakan bertahap. Semua hal teknis yang sudah live ada di commit git.

---

## A. SUDAH SELESAI (live di www.nugi.biz.id)
- [x] 9 halaman (Home, 4 layanan, /artikel + 3 artikel) — deploy Vercel
- [x] SEO meta lengkap: title 53-64 karakter, description, canonical, OG, Twitter Card
- [x] JSON-LD: ProfessionalService, Person, Service, Article, FAQPage, BreadcrumbList
- [x] favicon + apple-touch-icon + og:image 1024x1024 (semua halaman)
- [x] robots.txt + sitemap.xml (10 URL)
- [x] Canonical domain diseragamkan ke https://www.nugi.biz.id (ikuti redirect Vercel)
- [x] Tracking siap-pakai: slot Meta Pixel / GA4 / Google Ads (kosong = aman)
- [x] Event tracking klik WhatsApp (label data-cta) + konsultasi
- [x] CTA WhatsApp per kartu solusi & portofolio (pesan pre-filled)

## B. PERLU DATA DARI ANDA (agar bisa dikerjakan)
1. **Isi ID tracking di semua halaman** (cari `window.NUGI_TRACKING`):
   - `metaPixelId` (Meta/Facebook Pixel)
   - `ga4Id` (Google Analytics 4)
   - `googleAdsId` (Google Ads)
   - Simpan juga di `website/index.html` + `app.js` (fungsi `trackNugiEvent` sudah siap).
2. **Nama bisnis resmi & logo final** — saat ini memakai "NUGIPROPERTI" + logo yang ada.
   Jika ada logo/avatar baru, ganti file di `website/assets/brand/`.
3. **1-3 studi kasus nyata** (boleh anonim) dengan angka hasil — untuk mengganti
   portofolio yang masih deskriptif agar lebih meyakinkan.
4. **Testimoni klien** — belum ada; setelah klien pertama, tambahkan ke Home
   (+ schema Review bila perlu).

## C. OFF-PAGE / INDEXING (perlu akses akun Anda)
- [ ] **Google Search Console**: verifikasi domain `www.nugi.biz.id` (metode DNS/TXT),
      lalu submit `https://www.nugi.biz.id/sitemap.xml`.
- [ ] **Bing Webmaster Tools**: import dari GSC atau verifikasi langsung + submit sitemap.
- [ ] **Yandex Webmaster**: verifikasi + submit sitemap (bisa taruh file `yandex_*.html`
      di folder `website/` lalu commit, atau metode meta tag/DNS).
- [ ] **Google Business Profile** "NUGIPROPERTI" (Bandung) — wajib untuk pencarian
      lokal & Google Maps. Minta review dari klien.
- [ ] **Backlink awal**: LinkedIn pribadi, direktori bisnis Bandung, media/link building
      lokal properti, artikel tamu.
- [ ] **Sinyal sosial**: YouTube/TikTok/IG yang menaut ke website.

## D. IDE KONTEN & FITUR MENYUSUL (prioritas sedang)
- [ ] 2 artikel tambahan: "Sistem Custom untuk UMKM/Jasa" dan "Tips Follow-Up Sales".
- [ ] Halaman `/kontak` atau blok alamat/iframe Google Maps di footer.
- [ ] Struktur data `Review` + `AggregateRating` setelah ada testimoni.
- [ ] `hreflang` tidak diperlukan (satu bahasa). Tidak perlu.
- [ ] Optimasi gambar asli (webp) untuk portofolio bila ada foto baru.
- [ ] Google Business Profile listing link bisa ditambah ke footer/sitemap.

## E. CATATAN TEKNIS
- Folder deploy: `website/` (lihat `vercel.json`: outputDirectory=website, cleanUrls=true).
- Halaman baru: buat folder `website/<slug>/index.html`, tambahkan ke `sitemap.xml`,
  dan link dari Home/footer.
- Artikel baru: pakai template di `website/artikel/<slug>/index.html` (salin artikel
  yang ada), penulis "Tim NUGIPROPERTI".
- Semua halaman: wajib memuat `../style.css`, `../app.js`, tracking config,
  canonical `https://www.nugi.biz.id/<path>`, dan JSON-LD.
