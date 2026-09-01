from app.schemas.design_spec import DesignSpecification


def test_design_spec_defaults():
    spec = DesignSpecification(
        headline="LEADS IKLAN MASUK, TAPI SALES LAMBAT FOLLOW-UP?",
        highlight_words=["LAMBAT FOLLOW-UP"]
    )
    assert spec.template_id == "01_PROPERTY_PROBLEM"
    assert spec.width == 1080
    assert spec.height == 1350
    assert spec.brand_name == "NugiProperti"
    assert "LAMBAT FOLLOW-UP" in spec.highlight_words


def test_design_spec_custom_dimensions():
    spec = DesignSpecification(
        template_id="02_PROPERTY_INSIGHT",
        width=1080,
        height=1080,
        headline="Mengapa Biaya Iklan Properti Naik Setiap Tahun?",
        cta_text="Simpan Postingan Ini"
    )
    assert spec.height == 1080
    assert spec.template_id == "02_PROPERTY_INSIGHT"
