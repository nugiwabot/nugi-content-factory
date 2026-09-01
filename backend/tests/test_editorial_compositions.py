import io
from PIL import Image
from app.schemas.design_spec import DesignSpecification, CompositionType, CTAStrategy, ImageStrategy, OverlayStrategy
from app.schemas.visual_prompt import VisualPromptSpecification
from app.providers.flux_image import FluxImageProvider
from app.providers.factory import ProviderFactory
from app.rendering.editorial_renderer import EditorialRenderer
from app.services.visual_qa import VisualQAService


def test_visual_prompt_specification():
    spec = VisualPromptSpecification(
        subject="Modern Indonesian luxury villa architecture",
        focal_point_position="right",
        time_of_day="Sunset golden hour"
    )
    prompt = spec.build_flux_prompt(negative_space_bias="bottom")
    assert "Modern Indonesian luxury villa architecture" in prompt
    assert "Sunset golden hour" in prompt
    assert "negative space on the bottom" in prompt
    assert "no text" in prompt


def test_flux_image_provider_fallback():
    # Without FLUX_API_KEY, provider should gracefully fall back to MockImageProvider
    provider = FluxImageProvider(api_key=None)
    assert "FluxImageProvider" in provider.provider_name
    
    out = provider.generate_background(prompt="Contemporary property", width=1080, height=1350)
    assert out.image_bytes is not None
    assert len(out.image_bytes) > 500
    assert out.width == 1080
    assert out.height == 1350


def test_provider_factory_flux_resolution():
    provider = ProviderFactory.get_image_provider("flux")
    assert isinstance(provider, FluxImageProvider)


def test_render_all_seven_composition_archetypes():
    renderer = EditorialRenderer()
    archetypes = [
        CompositionType.HERO_IMAGE_EDITORIAL,
        CompositionType.SPLIT_EDITORIAL,
        CompositionType.CINEMATIC_OVERLAY,
        CompositionType.DATA_EDITORIAL,
        CompositionType.LIST_EDITORIAL,
        CompositionType.MINIMAL_EDITORIAL,
        CompositionType.PROPERTY_SHOWCASE
    ]

    for arch in archetypes:
        spec = DesignSpecification(
            composition_type=arch,
            width=1080,
            height=1350,
            headline="KENAPA HARGA RUMAH DI DEKAT TOL BISA NAIK LEBIH CEPAT?",
            highlight_words=["HARGA RUMAH"],
            subheadline="Aksesibilitas dan aktivitas ekonomi mempercepat pertumbuhan nilai investasi properti.",
            badge_text="EDUKASI PROPERTI",
            cta_strategy=CTAStrategy.CTA_NONE, # Article content: NO CTA
            metric_value="+300%",
            metric_label="Pertumbuhan Nilai Kawasan",
            bullet_points=["Akses gerbang tol < 5 menit", "Pusat bisnis terpadu", "Kawasan bebas banjir"],
            property_location="Jatinangor, Sumedang",
            property_price="Mulai Rp 1,85 Miliar",
            property_features=["16 Kamar Kost", "Yield 12%/thn", "SHM Siap"]
        )

        rendered_bytes, meta = renderer.render(spec)
        assert rendered_bytes is not None
        assert meta["composition_type"] == arch.value
        assert meta["width"] == 1080
        assert meta["height"] == 1350
        assert meta["cta_strategy"] == "CTA_NONE"

        img = Image.open(io.BytesIO(rendered_bytes))
        assert img.size == (1080, 1350)

        # Visual QA verification
        qa = VisualQAService.evaluate_design(spec, meta)
        assert qa.score >= 85


def test_cta_business_rules():
    renderer = EditorialRenderer()

    # 1. Educational Article: CTA_NONE -> No CTA button
    spec_article = DesignSpecification(
        composition_type=CompositionType.HERO_IMAGE_EDITORIAL,
        headline="Strategi Evaluasi Legalitas Tanah Sebelum Membeli Lahan Properti",
        cta_strategy=CTAStrategy.CTA_NONE
    )
    bytes_art, meta_art = renderer.render(spec_article)
    assert meta_art["cta_strategy"] == "CTA_NONE"
    qa_art = VisualQAService.evaluate_design(spec_article, meta_art)
    assert qa_art.score >= 85

    # 2. Direct Offer: CTA_REQUIRED -> Requires CTA text
    spec_offer_valid = DesignSpecification(
        composition_type=CompositionType.HERO_IMAGE_EDITORIAL,
        headline="Daftar Survey Rumah Kost Mahasiswa Jatinangor Hari Ini",
        cta_strategy=CTAStrategy.CTA_REQUIRED,
        cta_text="Daftar Survey Sekarang →"
    )
    bytes_off, meta_off = renderer.render(spec_offer_valid)
    assert meta_off["cta_strategy"] == "CTA_REQUIRED"
    qa_off = VisualQAService.evaluate_design(spec_offer_valid, meta_off)
    assert qa_off.score >= 85

    # 3. Direct Offer missing CTA text -> Penalized in QA
    spec_offer_missing = DesignSpecification(
        composition_type=CompositionType.HERO_IMAGE_EDITORIAL,
        headline="Daftar Survey Rumah Kost Mahasiswa Jatinangor Hari Ini",
        cta_strategy=CTAStrategy.CTA_REQUIRED,
        cta_text=None # Missing CTA
    )
    qa_missing = VisualQAService.evaluate_design(spec_offer_missing)
    assert qa_missing.score < 90
    assert any("CTA_REQUIRED" in issue for issue in qa_missing.issues)


def test_editorial_api_endpoints(client):
    # 1. List compositions
    list_res = client.get("/api/v1/editorial/compositions")
    assert list_res.status_code == 200
    comps = list_res.json()
    assert len(comps) == 7

    # 2. Render editorial visual
    render_payload = {
        "composition_type": "HERO_IMAGE_EDITORIAL",
        "width": 1080,
        "height": 1350,
        "headline": "KENAPA HARGA RUMAH DI DEKAT TOL BISA NAIK LEBIH CEPAT?",
        "highlight_words": ["HARGA RUMAH"],
        "subheadline": "Aksesibilitas dan pertumbuhan kawasan mempercepat apresiasi modal.",
        "badge_text": "MARKET INSIGHT",
        "cta_strategy": "CTA_NONE"
    }
    render_res = client.post("/api/v1/editorial/render", json=render_payload)
    assert render_res.status_code == 200
    data = render_res.json()
    assert data["success"] is True
    assert data["composition_type"] == "HERO_IMAGE_EDITORIAL"
    assert data["asset_path"] is not None
    assert data["visual_qa"]["score"] >= 85
