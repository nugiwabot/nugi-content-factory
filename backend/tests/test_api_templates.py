def test_list_templates_api(client):
    res = client.get("/api/v1/templates")
    assert res.status_code == 200
    templates = res.json()
    assert len(templates) == 6
    assert any(t["template_id"] == "01_PROPERTY_PROBLEM" for t in templates)


def test_get_template_by_id_api(client):
    res = client.get("/api/v1/templates/02_PROPERTY_INSIGHT")
    assert res.status_code == 200
    data = res.json()
    assert data["template_id"] == "02_PROPERTY_INSIGHT"
    assert data["accent_scheme"] == "cyan"


def test_render_template_api(client):
    payload = {
        "template_id": "01_PROPERTY_PROBLEM",
        "width": 1080,
        "height": 1350,
        "headline": "LEADS IKLAN MASUK, TAPI SALES LAMBAT FOLLOW-UP?",
        "highlight_words": ["LAMBAT FOLLOW-UP"],
        "subheadline": "Setiap menit keterlambatan bisa membuat prospek berpindah ke kompetitor.",
        "badge_text": "DILEMA SALES PROPERTI",
        "cta_text": "Pelajari Solusinya"
    }
    res = client.post("/api/v1/templates/render", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert data["asset_path"] is not None
    assert data["render_metadata"]["width"] == 1080
    assert data["render_metadata"]["height"] == 1350
    assert data["visual_qa"]["score"] >= 85


def test_get_brand_nugi_properti_api(client):
    res = client.get("/api/v1/brand/nugi-properti")
    assert res.status_code == 200
    data = res.json()
    assert data["brand_name"] == "NugiProperti"
    assert data["colors"]["accent_primary"] == "#38bdf8"
