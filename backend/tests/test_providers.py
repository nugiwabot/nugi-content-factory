import pytest
from app.providers.mock_llm import MockLLMProvider
from app.providers.mock_image import MockImageProvider
from app.providers.local_storage import LocalStorageProvider
from app.providers.factory import ProviderFactory
from app.core.errors import ProviderError


def test_mock_llm_provider():
    provider = MockLLMProvider()
    output = provider.generate_content(
        topic="3 Kesalahan Fatal Follow Up Leads Iklan Properti",
        target_audience="Sales Manager & Agent Properti",
        content_pillar="educational",
        tone_of_voice="professional_authoritative"
    )
    assert output.headline is not None
    assert len(output.headline) > 5
    assert output.body_caption is not None
    assert "#" in output.hashtags
    assert output.visual_concept_prompt is not None
    assert output.latency_ms is not None


def test_mock_image_provider():
    provider = MockImageProvider()
    output = provider.generate_background(
        prompt="Modern luxury architectural background",
        width=500,
        height=500
    )
    assert output.image_bytes is not None
    assert len(output.image_bytes) > 100
    assert output.width == 500
    assert output.height == 500


def test_local_storage_provider(tmp_path):
    storage = LocalStorageProvider(base_dir=str(tmp_path))
    data = b"test asset binary content"
    saved_path = storage.save(data, "test.txt", subfolder="unit_test")
    
    assert storage.exists(saved_path)
    read_data = storage.read(saved_path)
    assert read_data == data

    storage.delete(saved_path)
    assert not storage.exists(saved_path)


def test_provider_factory_mock():
    llm = ProviderFactory.get_llm_provider("mock")
    assert llm.provider_name == "MockLLMProvider"

    img = ProviderFactory.get_image_provider("mock")
    assert img.provider_name == "MockImageProvider"

    storage = ProviderFactory.get_storage_provider("local")
    assert isinstance(storage, LocalStorageProvider)


def test_provider_factory_invalid():
    with pytest.raises(ProviderError):
        ProviderFactory.get_llm_provider("unsupported_ai")
