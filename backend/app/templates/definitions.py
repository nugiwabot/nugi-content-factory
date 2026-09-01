from typing import List
from app.templates.spec import TemplateSpecification, SemanticZone, CanvasSpec, BackgroundRule


def build_template_01_problem() -> TemplateSpecification:
    return TemplateSpecification(
        template_id="01_PROPERTY_PROBLEM",
        name="Property Problem & Dilemma",
        purpose="Mengangkat masalah nyata dan friksi yang dihadapi developer / sales manager.",
        target_audience="Developer & Sales Manager Properti",
        content_type="problem_agitation",
        accent_scheme="rose", # Rose/Red accent for warning & tension
        canvas=CanvasSpec(width=1080, height=1350, aspect_ratio="4:5"),
        zones=[
            SemanticZone(zone_id="badge", semantic_position="top_left", style_variant="warning_pill", default_text="DILEMA SALES PROPERTI"),
            SemanticZone(zone_id="logo", semantic_position="top_right", style_variant="logo"),
            SemanticZone(zone_id="headline", semantic_position="center_top", style_variant="display", max_lines=4),
            SemanticZone(zone_id="subheadline", semantic_position="center", style_variant="body", max_lines=3),
            SemanticZone(zone_id="cta", semantic_position="bottom_center", style_variant="cta_pill", default_text="Pelajari Solusinya →"),
            SemanticZone(zone_id="brand_footer", semantic_position="bottom_left", style_variant="caption", default_text="NugiProperti • Authority System")
        ],
        background_rules=BackgroundRule(type="gradient", scrim_opacity=0.88, overlay_color="#070b14")
    )


def build_template_02_insight() -> TemplateSpecification:
    return TemplateSpecification(
        template_id="02_PROPERTY_INSIGHT",
        name="Market Authority & Educational Insight",
        purpose="Memberikan insight mendalam dan analisis edukatif pasar properti.",
        target_audience="Principal Agen & Property Investors",
        content_type="market_insight",
        accent_scheme="cyan", # Electric cyan for tech & intelligence
        canvas=CanvasSpec(width=1080, height=1350, aspect_ratio="4:5"),
        zones=[
            SemanticZone(zone_id="badge", semantic_position="top_left", style_variant="accent_pill", default_text="MARKET INSIGHT"),
            SemanticZone(zone_id="logo", semantic_position="top_right", style_variant="logo"),
            SemanticZone(zone_id="headline", semantic_position="center_top", style_variant="display", max_lines=4),
            SemanticZone(zone_id="takeaway_card", semantic_position="center_bottom", style_variant="card", max_lines=4),
            SemanticZone(zone_id="cta", semantic_position="bottom_center", style_variant="cta_pill", default_text="Simpan Postingan Ini ↗"),
            SemanticZone(zone_id="brand_footer", semantic_position="bottom_left", style_variant="caption", default_text="NugiProperti • Growth Intelligence")
        ],
        background_rules=BackgroundRule(type="gradient", scrim_opacity=0.85, overlay_color="#070b14")
    )


def build_template_03_number_list() -> TemplateSpecification:
    return TemplateSpecification(
        template_id="03_NUMBER_LIST",
        name="Listicle & Crucial Points",
        purpose="Menyajikan poin-poin kesalahan fatal atau langkah taktis terstruktur.",
        target_audience="Marketing Lead & Sales Executive Properti",
        content_type="listicle",
        accent_scheme="gold", # Amber/Gold accent for numbered items
        canvas=CanvasSpec(width=1080, height=1350, aspect_ratio="4:5"),
        zones=[
            SemanticZone(zone_id="badge", semantic_position="top_left", style_variant="gold_pill", default_text="5 POIN KRUSIAL"),
            SemanticZone(zone_id="logo", semantic_position="top_right", style_variant="logo"),
            SemanticZone(zone_id="headline", semantic_position="top_center", style_variant="h1", max_lines=3),
            SemanticZone(zone_id="bullet_list", semantic_position="center", style_variant="bullet_points", max_lines=5),
            SemanticZone(zone_id="cta", semantic_position="bottom_center", style_variant="cta_pill", default_text="Baca Selengkapnya di Caption ↓"),
            SemanticZone(zone_id="brand_footer", semantic_position="bottom_left", style_variant="caption", default_text="NugiProperti • Actionable Playbook")
        ],
        background_rules=BackgroundRule(type="gradient", scrim_opacity=0.88, overlay_color="#070b14")
    )


def build_template_04_case_study() -> TemplateSpecification:
    return TemplateSpecification(
        template_id="04_CASE_STUDY",
        name="Case Study & Proof Metrics",
        purpose="Membuktikan hasil nyata transformasi strategi penjualan/konversi.",
        target_audience="Owner Developer & Marketing Directors",
        content_type="social_proof",
        accent_scheme="emerald", # Emerald Green for metric growth & success
        canvas=CanvasSpec(width=1080, height=1350, aspect_ratio="4:5"),
        zones=[
            SemanticZone(zone_id="badge", semantic_position="top_left", style_variant="emerald_pill", default_text="STUDI KASUS & HASIL"),
            SemanticZone(zone_id="logo", semantic_position="top_right", style_variant="logo"),
            SemanticZone(zone_id="headline", semantic_position="top_center", style_variant="h1", max_lines=3),
            SemanticZone(zone_id="metric_card", semantic_position="center", style_variant="metric_highlight", max_lines=3),
            SemanticZone(zone_id="cta", semantic_position="bottom_center", style_variant="cta_pill", default_text="Konsultasi Strategi →"),
            SemanticZone(zone_id="brand_footer", semantic_position="bottom_left", style_variant="caption", default_text="NugiProperti • Proven Systems")
        ],
        background_rules=BackgroundRule(type="gradient", scrim_opacity=0.86, overlay_color="#070b14")
    )


def build_template_05_product_solution() -> TemplateSpecification:
    return TemplateSpecification(
        template_id="05_PRODUCT_SOLUTION",
        name="Tech & Automation Solution",
        purpose="Menjelaskan fitur software, automasi, atau sistem terpadu properti.",
        target_audience="Property Operations & Tech-driven Agency Leaders",
        content_type="product_solution",
        accent_scheme="indigo", # Indigo & Sky Cyan for Technology & Software
        canvas=CanvasSpec(width=1080, height=1350, aspect_ratio="4:5"),
        zones=[
            SemanticZone(zone_id="badge", semantic_position="top_left", style_variant="accent_pill", default_text="SOLUSI SISTEM"),
            SemanticZone(zone_id="logo", semantic_position="top_right", style_variant="logo"),
            SemanticZone(zone_id="headline", semantic_position="top_center", style_variant="h1", max_lines=3),
            SemanticZone(zone_id="feature_pills", semantic_position="center", style_variant="card", max_lines=4),
            SemanticZone(zone_id="cta", semantic_position="bottom_center", style_variant="cta_pill", default_text="Lihat Demo Sistem →"),
            SemanticZone(zone_id="brand_footer", semantic_position="bottom_left", style_variant="caption", default_text="NugiProperti • Automation Suite")
        ],
        background_rules=BackgroundRule(type="gradient", scrim_opacity=0.88, overlay_color="#070b14")
    )


def build_template_06_call_to_action() -> TemplateSpecification:
    return TemplateSpecification(
        template_id="06_CALL_TO_ACTION",
        name="Direct Conversion & Call to Action",
        purpose="Mendorong konversi langsung, pendaftaran survey, atau konsultasi eksklusif.",
        target_audience="High-intent Buyers & Investor Prospects",
        content_type="direct_conversion",
        accent_scheme="cyan", # Glowing high-contrast CTA
        canvas=CanvasSpec(width=1080, height=1350, aspect_ratio="4:5"),
        zones=[
            SemanticZone(zone_id="badge", semantic_position="top_left", style_variant="warning_pill", default_text="SLOT TERBATAS"),
            SemanticZone(zone_id="logo", semantic_position="top_right", style_variant="logo"),
            SemanticZone(zone_id="headline", semantic_position="center_top", style_variant="display", max_lines=3),
            SemanticZone(zone_id="value_prop", semantic_position="center", style_variant="body", max_lines=3),
            SemanticZone(zone_id="cta", semantic_position="center_bottom", style_variant="hero_button", default_text="HUBUNGI VIA WHATSAPP ➔"),
            SemanticZone(zone_id="brand_footer", semantic_position="bottom_center", style_variant="caption", default_text="Klik Link di Bio Profil Instagram")
        ],
        background_rules=BackgroundRule(type="gradient", scrim_opacity=0.90, overlay_color="#070b14")
    )


ALL_TEMPLATES: List[TemplateSpecification] = [
    build_template_01_problem(),
    build_template_02_insight(),
    build_template_03_number_list(),
    build_template_04_case_study(),
    build_template_05_product_solution(),
    build_template_06_call_to_action()
]
