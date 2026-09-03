"""
Knowledge manifest: allow-list classification of the business knowledge
repository (freelance-nugi-software-engineer).

Categories:
- CORE       -> always included as brand/positioning context
- SUPPORTING -> included only when topic/pillar matches its tags
- PRIVATE    -> assistant-only context (sales scripts, pricing, internal ops);
                NEVER injected into published content prompts
- REFERENCE  -> never auto-included in prompts (internal ops/dev docs)
- EXCLUDE    -> never even read (finance ledger, prospect database, PII data)
"""

CORE = "CORE"
SUPPORTING = "SUPPORTING"
PRIVATE = "PRIVATE"
REFERENCE = "REFERENCE"
EXCLUDE = "EXCLUDE"

# Ordered (relative_path, category, tags, purpose)
MANIFEST = [
    # ---------------------------------------------------------------
    # CORE: always-on business identity, brand, offer, audience, voice
    # ---------------------------------------------------------------
    ("DESIGN_SYSTEM.md", CORE, ["brand", "design", "warna", "font", "visual"],
     "Warna, font, dan aturan visual brand."),
    ("PHASE_00_BUSINESS_ASSET_AUDIT.md", CORE, ["identitas", "layanan", "penawaran", "founder"],
     "Identitas founder, katalog layanan, dan aset bisnis."),
    ("docs/BUSINESS.md", CORE, ["positioning", "icp", "offer", "pricing"],
     "Arah bisnis, ICP, hero offer, dan skema harga."),
    ("business/strategy/POSITIONING.md", CORE, ["positioning", "audiens", "icp"],
     "Positioning (April Dunford) dan persona ICP."),
    ("business/strategy/CUSTOMER_PROBLEMS.md", CORE, ["pain", "problem", "audience"],
     "Database pain point calon klien untuk angle konten."),
    ("business/knowledge/CUSTOMER_LANGUAGE.md", CORE, ["bahasa", "customer", "voice", "quote"],
     "Kutipan bahasa asli calon klien."),
    ("business/products/PRODUCT_01_DEFINITION.md", CORE, ["offer", "produk", "fitur", "harga"],
     "Definisi hero offer dan tier-nya."),
    ("business/marketing/BRAND_POSITIONING.md", CORE, ["brand", "voice", "messaging", "claim"],
     "Posisi brand, pilar pesan, dan klaim terlarang."),
    ("business/marketing/SOCIAL_MEDIA_STRATEGY.md", CORE, ["instagram", "rasio", "hook", "bio", "konten"],
     "Strategi konten Instagram 60-25-15 dan struktur bio."),

    # ---------------------------------------------------------------
    # SUPPORTING: topic-matched context for content & assistant
    # ---------------------------------------------------------------
    ("docs/PRODUCT.md", SUPPORTING, ["layanan", "harga", "produk"],
     "Daftar produk/jasa nyata dan harga publik."),
    ("business/strategy/PROPERTY_MARKET_SEGMENTATION.md", SUPPORTING, ["segment", "market", "budget", "developer", "agen"],
     "Segmentasi pasar properti dan pengambil keputusan."),
    ("business/marketing/PORTFOLIO_ASSET_AUDIT.md", SUPPORTING, ["portofolio", "case study", "bukti", "proyek"],
     "Riset portofolio dan studi kasus."),
    ("business/marketing/META_ADS_TESTING_PLAN.md", SUPPORTING, ["iklan", "meta ads", "angle", "hook", "kreatif"],
     "Angle kreatif iklan dan hook."),

    # ---------------------------------------------------------------
    # PRIVATE: assistant-only. Read for chat/sales/productivity help,
    # but NEVER injected into generated content that will be published.
    # ---------------------------------------------------------------
    ("docs/CLIENT_READINESS.md", PRIVATE, ["readiness", "positioning", "pricing", "sow", "legal", "scope"],
     "Audit internal kesiapan jual & legal (candid)."),
    ("business/products/UNIT_ECONOMICS.md", PRIVATE, ["biaya", "margin", "pricing", "finansial"],
     "Unit economics riil dan simulasi pendapatan."),
    ("business/products/PAID_PILOT.md", PRIVATE, ["pilot", "paid", "pricing", "offer"],
     "Struktur paid pilot / penawaran awal."),
    ("business/sales/WARM_OUTREACH_SYSTEM.md", PRIVATE, ["outreach", "warm", "sales", "prospek"],
     "Sistem outreach santai ke warm network."),
    ("business/sales/WARM_OUTREACH_EXECUTION.md", PRIVATE, ["outreach", "execution", "follow", "template"],
     "Template & eksekusi pesan outreach."),
    ("business/sales/OBJECTION_HANDLING.md", PRIVATE, ["keberatan", "negosiasi", "harga", "rebuttal"],
     "Playbook menangani keberatan & negosiasi."),
    ("business/sales/DISCOVERY_INTERVIEW_SYSTEM.md", PRIVATE, ["discovery", "interview", "kebutuhan", "kualifikasi"],
     "Pertanyaan discovery non-leading."),
    ("business/NOW.md", PRIVATE, ["now", "status", "prioritas", "target"],
     "Status dan prioritas operasional saat ini."),
    ("business/BUSINESS_DASHBOARD.md", PRIVATE, ["dashboard", "pipeline", "revenue", "target"],
     "Progress pipeline dan tracker finansial."),
    ("business/FOUNDER_ROLE_ARCHITECTURE.md", PRIVATE, ["peran", "founder", "stack", "arsitektur"],
     "Pembagian peran founder vs AI."),
    ("business/PHASE_01_MARKET_VALIDATION.md", PRIVATE, ["validasi", "riset", "market", "discovery"],
     "Hasil validasi pasar."),
    ("business/growth/FIRST_15M_PLAN.md", PRIVATE, ["target", "first 15m", "klien", "rencana"],
     "Rencana mencapai Rp15jt pertama."),
    ("business/growth/SCALE_100M.md", PRIVATE, ["skala", "pertumbuhan", "100m", "rencana"],
     "Rencana penskalaan ke Rp100jt/bulan."),
]

# Paths that must NEVER be read into ANY prompt (finance ledger, live
# prospect database with contact/PII, internal gap analysis).
EXCLUDE_PATHS = [
    "business/finance/",
    "business/sales/PROSPECT_DATABASE.md",
    "BUSINESS_BLUEPRINT_GAP_ANALYSIS.md",
]

CORE_REL_PATHS = {entry[0] for entry in MANIFEST if entry[1] == CORE}
SUPPORTING_REL_PATHS = {entry[0] for entry in MANIFEST if entry[1] == SUPPORTING}
PRIVATE_REL_PATHS = {entry[0] for entry in MANIFEST if entry[1] == PRIVATE}


def category_for(rel_path: str) -> str:
    """Returns the manifest category for a repository-relative markdown path."""
    normalized = rel_path.replace("\\", "/")
    if normalized in CORE_REL_PATHS:
        return CORE
    if normalized in SUPPORTING_REL_PATHS:
        return SUPPORTING
    if normalized in PRIVATE_REL_PATHS:
        return PRIVATE
    if normalized.startswith(tuple(EXCLUDE_PATHS)) or normalized in EXCLUDE_PATHS:
        return EXCLUDE
    return REFERENCE


def tags_for(rel_path: str) -> list:
    for entry in MANIFEST:
        if entry[0] == rel_path.replace("\\", "/"):
            return entry[2]
    return []
