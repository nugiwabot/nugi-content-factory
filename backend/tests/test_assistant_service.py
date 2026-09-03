from app.schemas.editorial_agent import AgentChatRequest
from app.services.assistant_service import AssistantService


def _req(message, project_id=None, active_package=None):
    return AgentChatRequest(
        message=message,
        project_id=project_id,
        active_package=active_package,
    )


def test_welcome_greeting_returns_capability_intro():
    resp = AssistantService.respond(_req("halo"))
    assert resp.action_type == "CHAT"
    assert "Asisten Nugi" in resp.reply
    assert resp.quick_suggestions is not None
    assert len(resp.quick_suggestions) >= 4


def test_empty_message_returns_welcome():
    resp = AssistantService.respond(_req("   "))
    assert resp.action_type == "CHAT"
    assert "Asisten Nugi" in resp.reply


def test_bulk_request_guides_to_bulk_tab_when_no_live_llm():
    # With the default (mock) provider, the deterministic path must explain
    # how to generate mass content instead of pretending it created 30 posts.
    resp = AssistantService._deterministic_answer("buat 30 konten tentang leads properti")
    assert resp.action_type == "CHAT"
    assert "Bulk" in resp.reply


def test_offline_generate_like_message_produces_package():
    resp = AssistantService._deterministic_answer("buat konten tentang kenapa leads properti lambat direspon")
    assert resp.action_type == "GENERATE"
    assert resp.content_package is not None
    assert resp.content_package.topic != ""


def test_unknown_non_generate_message_returns_welcome_when_offline():
    resp = AssistantService._deterministic_answer("cara bikin ayam goreng crispy")
    assert resp.action_type == "CHAT"
    assert "Asisten Nugi" in resp.reply


def test_chat_endpoint_greeting(client):
    resp = client.post("/api/v1/ai-studio/chat", json={"message": "halo"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["action_type"] == "CHAT"
    assert "Asisten Nugi" in data["reply"]


def test_chat_endpoint_offline_generate(client):
    resp = client.post("/api/v1/ai-studio/chat", json={"message": "buat konten tentang leads properti lambat direspon"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["action_type"] == "GENERATE"
    assert data["content_package"] is not None
