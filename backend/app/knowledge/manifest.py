"""
Knowledge manifest: allow-list classification of the business knowledge
repository (freelance-nugi-software-engineer).

Categories:
- CORE       -> always included as brand/positioning context
- SUPPORTING -> included only when topic/pillar matches its tags
- REFERENCE  -> never auto-included in prompts (internal ops/dev docs)
- EXCLUDE    -> never even read (sales scripts, finance, prospect/PII data)
"""

CORE = "CORE"
SUPPORTING = "SUPPORTING"
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
    # SUPPORTING: topic-matched context
    # ---------------------------------------------------------------
    ("docs/CLIENT_READINESS.md", SUPPORTING, ["audience", "value proposition", "positioning", "klien"],
     "Readiness & value proposition untuk konten sales."),
    ("docs/PRODUCT.md", SUPPORTING, ["layanan", "harga", "produk"],
     "Daftar produk/jasa nyata dan harga publik."),
    ("business/strategy/PROPERTY_MARKET_SEGMENTATION.md", SUPPORTING, ["segment", "market", "budget", "developer", "agen"],
     "Segmentasi pasar properti dan pengambil keputusan."),
    ("business/marketing/PORTFOLIO_ASSET_AUDIT.md", SUPPORTING, ["portofolio", "case study", "bukti", "proyek"],
     "Riset portofolio dan studi kasus."),
    ("business/marketing/META_ADS_TESTING_PLAN.md", SUPPORTING, ["iklan", "meta ads", "angle", "hook", "kreatif"],
     "Angle kreatif iklan dan hook."),
]

# Paths that must NEVER be read into generation context (PII/financial/sales).
EXCLUDE_PATHS = [
    "business/sales/",
    "business/finance/",
    "business/growth/",
    "business/NOW.md",
    "business/BUSINESS_DASHBOARD.md",
    "business/products/UNIT_ECONOMICS.md",
    "BUSINESS_BLUEPRINT_GAP_ANALYSIS.md",
]

CORE_REL_PATHS = {entry[0] for entry in MANIFEST if entry[1] == CORE}
SUPPORTING_REL_PATHS = {entry[0] for entry in MANIFEST if entry[1] == SUPPORTING}


def category_for(rel_path: str) -> str:
    """Returns the manifest category for a repository-relative markdown path."""
    normalized = rel_path.replace("\\", "/")
    if normalized in CORE_REL_PATHS:
        return CORE
    if normalized in SUPPORTING_REL_PATHS:
        return SUPPORTING
    if normalized.startswith(tuple(EXCLUDE_PATHS)) or normalized in EXCLUDE_PATHS:
        return EXCLUDE
    return REFERENCE


def tags_for(rel_path: str) -> list:
    for entry in MANIFEST:
        if entry[0] == rel_path.replace("\\", "/"):
            return entry[2]
    return []
