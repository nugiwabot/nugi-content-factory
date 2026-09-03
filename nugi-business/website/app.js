/* ==========================================================================
   NUGI PROPERTI - JAVASCRIPT INTERACTIVE LOGIC
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  // 1. WhatsApp Configuration (Founder Direct Contact)
  const FOUNDER_WA = '6287747584665'; // Nomor WhatsApp Founder Nugi

  // 2. Navbar Scroll Blur Effect
  const navbar = document.getElementById('navbar');
  window.addEventListener('scroll', () => {
    if (window.scrollY > 30) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
  });

  // 3. Mobile Navigation Menu Toggle
  const mobileToggle = document.getElementById('mobileToggle');
  const navMenu = document.getElementById('navMenu');
  let isMobileMenuOpen = false;

  const applyMobileMenuStyles = () => {
    navMenu.style.display = 'flex';
    navMenu.style.flexDirection = 'column';
    navMenu.style.position = 'absolute';
    navMenu.style.top = '100%';
    navMenu.style.left = '0';
    navMenu.style.width = '100%';
    navMenu.style.background = 'rgba(12, 18, 32, 0.96)';
    navMenu.style.padding = '20px';
    navMenu.style.borderBottom = '1px solid rgba(255, 255, 255, 0.1)';
  };

  const resetMobileMenuStyles = () => {
    navMenu.style.display = '';
    navMenu.style.flexDirection = '';
    navMenu.style.position = '';
    navMenu.style.top = '';
    navMenu.style.left = '';
    navMenu.style.width = '';
    navMenu.style.background = '';
    navMenu.style.padding = '';
    navMenu.style.borderBottom = '';
  };

  const closeMobileMenu = () => {
    if (!navMenu || !isMobileMenuOpen) return;
    isMobileMenuOpen = false;
    navMenu.style.display = 'none';
  };

  if (mobileToggle && navMenu) {
    mobileToggle.addEventListener('click', () => {
      if (window.innerWidth > 900) return;
      if (isMobileMenuOpen) {
        closeMobileMenu();
      } else {
        isMobileMenuOpen = true;
        applyMobileMenuStyles();
      }
    });

    // Bersihkan inline style saat kembali ke viewport desktop (>=901px)
    // agar aturan CSS desktop kembali berlaku.
    window.addEventListener('resize', () => {
      if (window.innerWidth > 900) {
        isMobileMenuOpen = false;
        resetMobileMenuStyles();
      }
    });
  }

  // 4. FAQ Accordion Logic
  const faqItems = document.querySelectorAll('.faq-item');
  faqItems.forEach(item => {
    const questionBtn = item.querySelector('.faq-question');
    questionBtn.addEventListener('click', () => {
      const isActive = item.classList.contains('active');
      
      // Close all
      faqItems.forEach(otherItem => otherItem.classList.remove('active'));
      
      // Toggle clicked
      if (!isActive) {
        item.classList.add('active');
      }
    });
  });

  // 5. Interactive Pre-Filled Consultation Generator
  const btnKirimKonsultasi = document.getElementById('btnKirimKonsultasi');
  const selectKebutuhan = document.getElementById('selectKebutuhan');
  const inputNama = document.getElementById('inputNama');

  if (btnKirimKonsultasi) {
    btnKirimKonsultasi.addEventListener('click', () => {
      const kebutuhan = selectKebutuhan.value || 'kendala alur kerja tim properti';
      const nama = inputNama.value.trim() || 'Saya';

      const customMessage = `Halo Mas Nugi, nama saya ${nama}. Saya ingin ngobrol dan konsultasi santai mengenai: ${kebutuhan}. Apakah ada waktu senggang untuk diskusi?`;
      const waUrl = `https://wa.me/${FOUNDER_WA}?text=${encodeURIComponent(customMessage)}`;

      window.open(waUrl, '_blank');
    });
  }

  // 6. Cinematic Full-View Authority Showcase Controller
  const featuredMainImg = document.getElementById('featuredMainImg');
  const featuredBadge = document.getElementById('featuredBadge');
  const slideCounter = document.getElementById('slideCounter');
  const featuredTitle = document.getElementById('featuredTitle');
  const featuredDesc = document.getElementById('featuredDesc');
  const cinematicPrevBtn = document.getElementById('cinematicPrevBtn');
  const cinematicNextBtn = document.getElementById('cinematicNextBtn');
  const thumbBtns = document.querySelectorAll('.thumbnail-selector-strip .thumb-btn');

  const slidesData = [
    {
      image: 'assets/authority_full/wisuda_singapura.webp',
      badge: 'PENDIDIKAN PROPERTI',
      counter: '01 / 08',
      title: 'Wisuda BSP di Singapura',
      desc: 'Menyelesaikan program intensif 12 bulan di Boarding School Property (BSP) dan mengikuti prosesi wisuda kelulusan resmi di Singapura. Memahami proses bisnis properti secara komprehensif dari hulu ke hilir.'
    },
    {
      image: 'assets/authority_full/sertifikat_bsp.webp',
      badge: 'SERTIFIKASI RESMI',
      counter: '02 / 08',
      title: 'Sertifikat Kelulusan 12 Bulan BSP Bandung',
      desc: 'Sertifikasi kelulusan resmi 12 bulan dari Boarding School Property. Membedah aspek legalitas tanah, perizinan perumahan, analisis siteplan, manajemen cashflow proyek, dan strategi promosi.'
    },
    {
      image: 'assets/authority_full/mc_gathering.webp',
      badge: 'EVENT & GATHERING',
      counter: '03 / 08',
      title: 'Gathering Penjualan Properti',
      desc: 'Memandu acara gathering penjualan langsung di hadapan puluhan calon pembeli unit rukost & perumahan komersial, mengawal antusiasme prospek hingga proses booking unit di tempat.'
    },
    {
      image: 'assets/authority_full/pelatihan_sales.webp',
      badge: 'TRAINING MARKETING',
      counter: '04 / 08',
      title: 'Training Tim Sales Lapangan',
      desc: 'Memberikan pembekalan strategi respon cepat leads iklan, simulasi presentasi ke calon pembeli, dan optimasi alur follow-up tim marketing hingga penjadwalan survey lokasi.'
    },
    {
      image: 'assets/authority_full/proyek_lahan.webp',
      badge: 'PRAKTISI LAPANGAN',
      counter: '05 / 08',
      title: 'Pematangan Lahan & Lokasi Proyek',
      desc: 'Terjun langsung memantau proses cut & fill, pengukuran siteplan batas kavling, dan kesiapan infrastruktur proyek sebelum dipasarkan secara massal ke calon pembeli.'
    },
    {
      image: 'assets/authority_full/unit_properti.webp',
      badge: 'SHOWCASE PRODUK',
      counter: '06 / 08',
      title: 'Showcase Unit Properti & Rukost',
      desc: 'Mendampingi persiapan materi visual promosi, spesifikasi bangunan, denah tipe unit, dan kelengkapan fasilitas perumahan untuk kebutuhan tim pemasaran.'
    },
    {
      image: 'assets/authority_full/workshop_tim.webp',
      badge: 'WORKSHOP SISTEM',
      counter: '07 / 08',
      title: 'Workshop Alur Kerja Tim Properti',
      desc: 'Membedah kendala operasional harian bersama tim pemasaran dan merancang sistem digital praktis yang mempermudah pencatatan prospek serta follow-up harian.'
    },
    {
      image: 'assets/authority_full/diskusi_rekanan.webp',
      badge: 'NETWORKING & RELASI',
      counter: '08 / 08',
      title: 'Kolaborasi Rekanan Bisnis Properti',
      desc: 'Menjalin sinergi aktif dengan sesama praktisi, agen kantor properti, dan pengembang di berbagai kota untuk berbagi wawasan pasar terkini.'
    }
  ];

  if (featuredMainImg && slidesData.length > 0) {
    let currentSlideIdx = 0;
    const thumbnailStrip = document.getElementById('thumbnailStrip');

    const renderSlide = (idx) => {
      if (idx < 0) idx = slidesData.length - 1;
      if (idx >= slidesData.length) idx = 0;
      currentSlideIdx = idx;

      const data = slidesData[idx];

      // Smooth Fade Image Transition
      featuredMainImg.style.opacity = '0';
      featuredMainImg.style.transform = 'scale(0.98)';

      setTimeout(() => {
        featuredMainImg.src = data.image;
        featuredBadge.textContent = data.badge;
        slideCounter.textContent = data.counter;
        featuredTitle.textContent = data.title;
        featuredDesc.textContent = data.desc;

        featuredMainImg.style.opacity = '1';
        featuredMainImg.style.transform = 'scale(1)';
      }, 120);

      // Update Active Thumbnail State (No Page Auto-Scroll)
      thumbBtns.forEach((btn, bIdx) => {
        if (bIdx === idx) {
          btn.classList.add('active');
        } else {
          btn.classList.remove('active');
        }
      });
    };

    const nextSlide = () => renderSlide(currentSlideIdx + 1);
    const prevSlide = () => renderSlide(currentSlideIdx - 1);

    let isPaused = false;
    let autoPlayInterval = null;

    // Auto Play Functions (Slide berganti otomatis tanpa menggeser posisi halaman)
    const startAutoPlay = () => {
      stopAutoPlay();
      autoPlayInterval = setInterval(() => {
        if (!isPaused) {
          nextSlide();
        }
      }, 4000); // Berganti setiap 4 detik
    };

    const stopAutoPlay = () => {
      if (autoPlayInterval) {
        clearInterval(autoPlayInterval);
        autoPlayInterval = null;
      }
    };

    startAutoPlay();

    // Pause saat mouse kursor diarahkan ke area slide
    const showcaseContainer = document.querySelector('.cinematic-showcase-container');
    if (showcaseContainer) {
      showcaseContainer.addEventListener('mouseenter', () => { isPaused = true; });
      showcaseContainer.addEventListener('mouseleave', () => { isPaused = false; });
      showcaseContainer.addEventListener('touchstart', () => { isPaused = true; }, { passive: true });
      showcaseContainer.addEventListener('touchend', () => { isPaused = false; });
    }

    // Button Events
    if (cinematicNextBtn) {
      cinematicNextBtn.addEventListener('click', (e) => {
        e.preventDefault();
        isPaused = true;
        nextSlide();
        startAutoPlay();
        setTimeout(() => { isPaused = false; }, 3000);
      });
    }

    if (cinematicPrevBtn) {
      cinematicPrevBtn.addEventListener('click', (e) => {
        e.preventDefault();
        isPaused = true;
        prevSlide();
        startAutoPlay();
        setTimeout(() => { isPaused = false; }, 3000);
      });
    }

    // Thumbnail Clicks
    thumbBtns.forEach((btn) => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        isPaused = true;
        const targetIdx = parseInt(btn.getAttribute('data-index'), 10) || 0;
        renderSlide(targetIdx);
        startAutoPlay();
        setTimeout(() => { isPaused = false; }, 3000);
      });
    });
  }

  // 7. Smooth Scroll for Internal Anchors
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      const targetId = this.getAttribute('href');
      if (targetId === '#') return;
      
      const targetElement = document.querySelector(targetId);
      if (targetElement) {
        e.preventDefault();
        targetElement.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
        // Auto close mobile menu if opened
        if (window.innerWidth <= 900) {
          closeMobileMenu();
        }
      }
    });
  });

  // 8. Conversion Tracking — klik WhatsApp (semua tombol wa.me)
  const TRACKING = window.NUGI_TRACKING || {};

  function trackNugiEvent(eventName, params) {
    params = params || {};
    if (typeof window.gtag === 'function') {
      window.gtag('event', eventName, params);
    }
    if (typeof window.fbq === 'function') {
      window.fbq('trackCustom', eventName, params);
    }
    if (window.dataLayer && Array.isArray(window.dataLayer)) {
      window.dataLayer.push({ event: eventName, ...params });
    }
  }
  window.trackNugiEvent = trackNugiEvent;

  document.addEventListener('click', function (e) {
    const link = e.target.closest('a[href*="wa.me"]');
    if (link) {
      const cta = link.getAttribute('data-cta') || link.id || 'wa-click';
      trackNugiEvent('whatsapp_click', { cta_label: cta });
    }
  });

  // 9. Konsultasi button → track klik saat buka WhatsApp
  if (btnKirimKonsultasi) {
    btnKirimKonsultasi.addEventListener('click', function () {
      trackNugiEvent('consultation_click', { kebutuhan: selectKebutuhan.value || 'umum' });
    });
  }
});
