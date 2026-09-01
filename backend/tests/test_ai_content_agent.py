import pytest
from app.schemas.editorial_agent import (
    ContentType,
    TextSafeRegion,
    UserBriefInput,
    EditorialContentSpecification,
    VisualArtDirectionSpecification,
    ContentPackage
)
from app.schemas.design_spec import CompositionType, CTAStrategy
from app.services.content_strategy_service import ContentStrategyService
from app.services.headline_service import HeadlineGenerationService
from app.services.caption_service import CaptionGenerationService
from app.services.creative_director_service import CreativeDirectorService
from app.services.content_generation_agent import ContentGenerationAgent


def test_content_type_classification_and_cta_policy():
    # 1. Problem
    res_prob = ContentStrategyService.classify_and_strategize(
        UserBriefInput(topic="Kenapa leads iklan properti banyak tapi closing tetap rendah?")
    )
    assert res_prob["content_type"] == ContentType.PROPERTY_PROBLEM
    assert res_prob["cta_policy"] == CTAStrategy.CTA_NONE
    assert res_prob["suggested_archetype"] == CompositionType.HERO_IMAGE_EDITORIAL

    # 2. Listicle
    res_list = ContentStrategyService.classify_and_strategize(
        UserBriefInput(topic="5 Kesalahan fatal follow up leads properti")
    )
    assert res_list["content_type"] == ContentType.PROPERTY_LISTICLE
    assert res_list["cta_policy"] == CTAStrategy.CTA_NONE
    assert res_list["suggested_archetype"] == CompositionType.LIST_EDITORIAL

    # 3. Case study
    res_cs = ContentStrategyService.classify_and_strategize(
        UserBriefInput(topic="Studi kasus hasil transformasi response time tim sales kost")
    )
    assert res_cs["content_type"] == ContentType.PROPERTY_CASE_STUDY
    assert res_cs["cta_policy"] == CTAStrategy.CTA_NONE
    assert res_cs["suggested_archetype"] == CompositionType.DATA_EDITORIAL

    # 4. Property showcase
    res_show = ContentStrategyService.classify_and_strategize(
        UserBriefInput(topic="Unit rukost mahasiswa jatinangor siap huni")
    )
    assert res_show["content_type"] == ContentType.PROPERTY_SHOWCASE
    assert res_show["cta_policy"] == CTAStrategy.CTA_OPTIONAL
    assert res_show["suggested_archetype"] == CompositionType.PROPERTY_SHOWCASE

    # 5. Sales offer
    res_offer = ContentStrategyService.classify_and_strategize(
        UserBriefInput(topic="Daftar audit funnel marketing properti slot terbatas")
    )
    assert res_offer["content_type"] == ContentType.PROPERTY_SALES_OFFER
    assert res_offer["cta_policy"] == CTAStrategy.CTA_REQUIRED


def test_headline_generation_and_highlights():
    head_pkg = HeadlineGenerationService.generate_headline_package(
        topic="Kenapa leads properti lambat di follow up?",
        content_type=ContentType.PROPERTY_PROBLEM,
        editorial_angle="Membongkar kebocoran alur leads",
        target_audience="Developer Properti"
    )
    assert "headline" in head_pkg
    assert "highlight_words" in head_pkg
    assert len(head_pkg["highlight_words"]) >= 1
    # Verify highlight word exists in headline
    for hw in head_pkg["highlight_words"]:
        assert hw.upper() in head_pkg["headline"].upper()


def test_caption_structure_and_no_forced_cta():
    caption = CaptionGenerationService.generate_caption(
        topic="Kenapa harga rumah dekat tol naik cepat?",
        content_type=ContentType.PROPERTY_INSIGHT,
        headline="KENAPA HARGA RUMAH DI DEKAT TOL BISA NAIK LEBIH CEPAT?",
        core_insight="Konektivitas tol melipatgandakan apresiasi lahan.",
        target_audience="Developer & Investor",
        cta_policy=CTAStrategy.CTA_NONE # Strictly NO CTA
    )
    assert "DATA & FAKTA" in caption
    assert "KESIMPULAN" in caption
    assert "Hubungi kami sekarang" not in caption
    assert "DM kami" not in caption


def test_creative_director_art_direction_and_negative_space():
    editorial_spec = EditorialContentSpecification(
        content_type=ContentType.PROPERTY_INSIGHT,
        target_audience="Investor Properti",
        audience_problem="Kurang paham faktor apresiasi",
        core_insight="Infrastruktur memicu pertumbuhan ekonomi",
        editorial_angle="Analisis koridor tol",
        headline="KENAPA HARGA RUMAH DI DEKAT TOL BISA NAIK LEBIH CEPAT?",
        subheadline="Aksesibilitas mempercepat pertumbuhan modal properti.",
        highlight_words=["NAIK LEBIH CEPAT"],
        caption="Full editorial caption article...",
        suggested_archetype=CompositionType.CINEMATIC_OVERLAY,
        cta_policy=CTAStrategy.CTA_NONE
    )

    art = CreativeDirectorService.create_art_direction(editorial_spec)
    assert art.archetype == CompositionType.CINEMATIC_OVERLAY
    assert art.negative_space_location == TextSafeRegion.FULL_BOTTOM
    assert "no text" in art.image_prompt
    assert "no watermark" in art.image_prompt
    assert "no logo" in art.image_prompt


def test_end_to_end_agent_generation():
    agent = ContentGenerationAgent()
    brief = UserBriefInput(
        topic="Kenapa leads iklan properti banyak tapi closing tetap rendah?",
        target_audience="Developer Properti"
    )

    pkg = agent.generate_full_package(brief=brief)
    assert isinstance(pkg, ContentPackage)
    assert pkg.content_type == ContentType.PROPERTY_PROBLEM
    assert pkg.editorial_spec.cta_policy == CTAStrategy.CTA_NONE
    assert pkg.rendered_asset_path is not None
    assert pkg.visual_qa is not None
    assert pkg.visual_qa.score >= 85


def test_modular_regenerations():
    agent = ContentGenerationAgent()
    brief = UserBriefInput(
        topic="5 Kesalahan fatal follow up leads properti",
        target_audience="Sales Manager Properti"
    )
    pkg = agent.generate_full_package(brief=brief)

    # 1. Regenerate Headline
    old_headline = pkg.editorial_spec.headline
    pkg_new_head = agent.regenerate_headline(pkg, custom_topic="3 Kesalahan fatal follow up leads")
    assert pkg_new_head.editorial_spec.headline is not None
    assert pkg_new_head.visual_qa.score >= 85

    # 2. Regenerate Caption
    pkg_new_cap = agent.regenerate_caption(pkg)
    assert len(pkg_new_cap.editorial_spec.caption) > 50

    # 3. Regenerate Visual
    pkg_new_vis = agent.regenerate_visual_art(pkg, archetype_override=CompositionType.HERO_IMAGE_EDITORIAL)
    assert pkg_new_vis.art_direction_spec.archetype == CompositionType.HERO_IMAGE_EDITORIAL


def test_ai_studio_api_endpoints(client):
    # 1. Generate Full Package
    gen_res = client.post("/api/v1/ai-studio/generate", json={
        "topic": "Kenapa harga rumah di dekat tol bisa naik lebih cepat?",
        "target_audience": "Investor Properti"
    })
    assert gen_res.status_code == 200
    pkg_data = gen_res.json()
    assert pkg_data["content_type"] == "PROPERTY_INSIGHT"
    assert pkg_data["editorial_spec"]["cta_policy"] == "CTA_NONE"
    assert pkg_data["visual_qa"]["score"] >= 85

    # 2. Regenerate Headline Endpoint
    rehead_res = client.post("/api/v1/ai-studio/regenerate/headline", json={
        "package": pkg_data,
        "custom_topic": "Strategi kenaikan harga rumah koridor tol"
    })
    assert rehead_res.status_code == 200
    assert rehead_res.json()["editorial_spec"]["headline"] is not None

    # 3. Regenerate Caption Endpoint
    recap_res = client.post("/api/v1/ai-studio/regenerate/caption", json={
        "package": pkg_data
    })
    assert recap_res.status_code == 200
    assert "DATA & FAKTA" in recap_res.json()["editorial_spec"]["caption"]
