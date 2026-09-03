from app.core.pricing import estimate_llm_cost, estimate_image_cost
from app.providers.mock_llm import MockLLMProvider
from app.providers.mock_image import MockImageProvider
from app.services.content_generation_agent import ContentGenerationAgent
from app.schemas.editorial_agent import UserBriefInput


def test_pricing_known_llm_model():
    cost = estimate_llm_cost("google/gemini-2.5-flash-lite", tokens_in=1000, tokens_out=500)
    assert cost is not None
    assert abs(cost - 0.00155) < 1e-6


def test_pricing_unknown_llm_model_returns_none():
    assert estimate_llm_cost("custom-model-xyz", 100, 100) is None
    assert estimate_llm_cost("flux", None, 10) is None


def test_pricing_image_models():
    assert estimate_image_cost("flux-2-klein-9b") == 0.04
    assert estimate_image_cost("dall-e-3") == 0.08
    assert estimate_image_cost("totally-unknown-model") is None
    assert estimate_image_cost("flux-pro-1.1") == 0.04


def test_pricing_real_live_models():
    # Models actually used in acceptance testing (sumopod gemini + BFL flux-pro-1.1).
    llm = estimate_llm_cost("gemini/gemini-3.5-flash-lite", tokens_in=1000, tokens_out=500)
    assert llm is not None and llm > 0
    assert estimate_image_cost("flux-pro-1.1") == 0.04


def test_mock_providers_report_zero_cost():
    out = MockLLMProvider().generate_content(topic="x", target_audience="a", content_pillar="p", tone_of_voice="v")
    assert out.estimated_cost == 0.0
    assert out.model == "mock-llm-v1"

    img = MockImageProvider().generate_background(prompt="p", width=256, height=256)
    assert img.estimated_cost == 0.0
    assert img.model == "mock-image-v1"


def test_mock_generation_reports_no_cost():
    agent = ContentGenerationAgent()
    pkg = agent.generate_full_package(
        brief=UserBriefInput(topic="Kenapa leads properti dingin?"),
        image_provider_type="mock"
    )
    # Mock providers produce no real spend -> cost is None, but never fabricated.
    assert pkg.estimated_cost_usd in (None, 0.0)
    assert pkg.usage is not None
