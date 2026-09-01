import pytest
from app.templates.registry import TemplateRegistry
from app.core.errors import NotFoundError


def test_six_templates_registered():
    templates = TemplateRegistry.list_all()
    assert len(templates) == 6
    
    expected_ids = [
        "01_PROPERTY_PROBLEM",
        "02_PROPERTY_INSIGHT",
        "03_NUMBER_LIST",
        "04_CASE_STUDY",
        "05_PRODUCT_SOLUTION",
        "06_CALL_TO_ACTION"
    ]
    for tid in expected_ids:
        assert TemplateRegistry.exists(tid)
        tmpl = TemplateRegistry.get(tid)
        assert tmpl.template_id == tid
        assert len(tmpl.zones) >= 4
        assert tmpl.canvas.width == 1080
        assert tmpl.canvas.height == 1350


def test_get_invalid_template():
    with pytest.raises(NotFoundError):
        TemplateRegistry.get("INVALID_TEMPLATE_99")
