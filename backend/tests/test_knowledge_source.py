import pytest

from app.core.config import settings
from app.knowledge import source as knowledge_source_module
from app.knowledge.source import KnowledgeSource

from app.services.knowledge_service import KnowledgeService


def _write_tree(root):
    (root / "docs").mkdir(parents=True)
    (root / "business" / "strategy").mkdir(parents=True)
    (root / "business" / "sales").mkdir(parents=True)
    (root / "business" / "finance").mkdir(parents=True)
    (root / "business" / "marketing").mkdir(parents=True)

    (root / "DESIGN_SYSTEM.md").write_text("# Design System\nWarna utama violet #8b5cf6.", encoding="utf-8")
    (root / "docs" / "BUSINESS.md").write_text("# Business\nICP Developer Properti, hero offer Lead-Engine.", encoding="utf-8")
    (root / "business" / "strategy" / "CUSTOMER_PROBLEMS.md").write_text("# Pain\nLeads dibagi manual lambat.", encoding="utf-8")
    (root / "business" / "marketing" / "SOCIAL_MEDIA_STRATEGY.md").write_text(
        "# Sosmed\nKontak nugifathulfalah04@gmail.com WA 6287747584665 proyek GREN Propertykost Jatinangor.", encoding="utf-8"
    )
    (root / "docs" / "PRODUCT.md").write_text("# Product\nLayanan CRM Properti harga mulai 7.5jt.", encoding="utf-8")
    (root / "README.md").write_text("# Internal readme\nStrategi internal rahasia.", encoding="utf-8")
    (root / "business" / "sales" / "WARM_OUTREACH_EXECUTION.md").write_text("# Sales script\nTemplate WA rahasia untuk prospek hangat.", encoding="utf-8")
    (root / "business" / "finance" / "REVENUE_LEDGER.md").write_text("# Finance\nPendapatan Rp 0.", encoding="utf-8")


@pytest.fixture()
def knowledge_tree(tmp_path, monkeypatch):
    _write_tree(tmp_path)
    monkeypatch.setattr(settings, "KNOWLEDGE_SOURCE_PATH", str(tmp_path))
    KnowledgeSource.refresh()
    yield tmp_path
    KnowledgeSource.clear()


def test_core_context_loaded_from_manifest(knowledge_tree):
    core = KnowledgeSource.core_context()
    assert "Design System" in core
    assert "Business" in core
    assert "CUSTOMER_PROBLEMS" in core
    # REFERENCE and EXCLUDE files must not appear.
    assert "Internal readme" not in core
    assert "sales script" not in core.lower()
    assert "REVENUE_LEDGER" not in core
    assert "Pendapatan" not in core


def test_core_context_pii_scrubbed(knowledge_tree):
    core = KnowledgeSource.core_context()
    assert "nugifathulfalah04@gmail.com" not in core
    assert "6287747584665" not in core
    assert "[phone]" in core
    assert "GREN" not in core


def test_supporting_retrieval_only_matches_topic(knowledge_tree):
    match = KnowledgeSource.supporting_for_topic("berapa biaya bikin crm properti")
    assert "CRM Properti" in match
    assert "PRODUCT" in match or "Product" in match

    no_match = KnowledgeSource.supporting_for_topic("template outreach whatsapp sales")
    assert no_match == ""


def test_status_reports_source(knowledge_tree):
    status = KnowledgeSource.status()
    assert status["active"] is True
    assert status["core_docs"] >= 4
    assert "supporting_docs" in status
    assert "private_docs" in status


def test_assistant_context_includes_private_but_not_exclude(knowledge_tree):
    context = KnowledgeSource.assistant_context("outreach whatsapp ke prospek hangat")
    assert "Sales script" in context
    assert "KONTEKS INTERNAL PRIVAT" in context
    # EXCLUDE (finance ledger) must never appear anywhere.
    assert "REVENUE_LEDGER" not in context
    assert "Pendapatan" not in context


def test_core_and_supporting_never_leak_private(knowledge_tree):
    core = KnowledgeSource.core_context()
    supporting = KnowledgeSource.supporting_for_topic("outreach whatsapp sales properti")
    assert "rahasia untuk prospek hangat" not in core
    assert "rahasia untuk prospek hangat" not in supporting


def test_knowledge_service_merges_external_context(db_session, knowledge_tree):
    brand = KnowledgeService.get_brand_context(db_session)
    assert "Design System" in brand
    assert "SUMBER PENGETAHUAN BISNIS" in brand

    skills = KnowledgeService.retrieve_relevant_skills(db_session, "biaya crm properti")
    assert "CRM Properti" in skills
