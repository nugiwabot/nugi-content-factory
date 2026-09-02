import time
from fastapi import APIRouter, HTTPException
from typing import Dict, Any

from app.core.config import settings
from app.core.logging import logger
from app.schemas.provider_settings import (
    ProviderSettingsResponse,
    ProviderSettingsUpdateRequest,
    TestProviderRequest,
    TestProviderResponse,
    LLMConfigSchema,
    ImageConfigSchema,
    ComputeConfigSchema
)
from app.providers.factory import ProviderFactory

router = APIRouter(prefix="/settings", tags=["Settings & Provider Configuration"])


def _mask_key(key: str | None) -> str | None:
    if not key:
        return None
    if len(key) <= 8:
        return "****"
    return f"{key[:4]}...{key[-4:]}"


def _looks_masked(key: str) -> bool:
    """Heuristic: a masked/echoed key should never overwrite a stored secret."""
    return key.startswith("****") or "..." in key


def _resolve_api_key(new_key: str | None, current_key: str | None) -> str | None:
    """Returns current_key when new_key is empty or masked; otherwise the new secret."""
    if not new_key or _looks_masked(new_key):
        return current_key
    return new_key


@router.get("/providers", response_model=ProviderSettingsResponse)
def get_provider_settings():
    """Returns current active provider configurations with masked secret keys."""
    # Active LLM config
    active_llm_key = settings.LLM_API_KEY
    active_llm_url = settings.LLM_BASE_URL
    active_llm_model = settings.LLM_MODEL

    if settings.LLM_PROVIDER == "openrouter":
        active_llm_key = active_llm_key or settings.OPENROUTER_API_KEY
        active_llm_url = active_llm_url or settings.OPENROUTER_BASE_URL
        active_llm_model = active_llm_model or settings.OPENROUTER_MODEL
    elif settings.LLM_PROVIDER == "openai":
        active_llm_key = active_llm_key or settings.OPENAI_API_KEY
        active_llm_url = active_llm_url or settings.OPENAI_BASE_URL
        active_llm_model = active_llm_model or settings.OPENAI_MODEL
    elif settings.LLM_PROVIDER == "anthropic":
        active_llm_key = active_llm_key or settings.ANTHROPIC_API_KEY
        active_llm_url = active_llm_url or settings.ANTHROPIC_BASE_URL
        active_llm_model = active_llm_model or settings.ANTHROPIC_MODEL
    elif settings.LLM_PROVIDER == "google":
        active_llm_key = active_llm_key or settings.GOOGLE_API_KEY
        active_llm_model = active_llm_model or settings.GOOGLE_MODEL

    # Active Image config
    active_img_key = settings.IMAGE_API_KEY
    active_img_url = settings.IMAGE_BASE_URL or settings.IMAGE_ENDPOINT
    active_img_model = settings.IMAGE_MODEL

    if settings.IMAGE_PROVIDER == "flux":
        active_img_key = active_img_key or settings.FLUX_API_KEY
        active_img_url = active_img_url or settings.FLUX_BASE_URL
        active_img_model = active_img_model or settings.FLUX_MODEL

    # Active Compute config
    active_comp_key = settings.COMPUTE_API_KEY or settings.RUNPOD_API_KEY
    active_comp_endpoint = settings.COMPUTE_ENDPOINT_ID or settings.RUNPOD_ENDPOINT_ID

    return ProviderSettingsResponse(
        llm=LLMConfigSchema(
            provider=settings.LLM_PROVIDER,
            base_url=active_llm_url,
            api_key=_mask_key(active_llm_key),
            model=active_llm_model
        ),
        image=ImageConfigSchema(
            provider=settings.IMAGE_PROVIDER,
            endpoint_url=active_img_url,
            api_key=_mask_key(active_img_key),
            model=active_img_model
        ),
        compute=ComputeConfigSchema(
            provider=settings.COMPUTE_PROVIDER,
            endpoint_id=active_comp_endpoint,
            api_key=_mask_key(active_comp_key)
        )
    )


@router.post("/providers", response_model=ProviderSettingsResponse)
def update_provider_settings(payload: ProviderSettingsUpdateRequest):
    """Updates provider configuration at runtime."""
    if payload.llm:
        if payload.llm.provider:
            settings.LLM_PROVIDER = payload.llm.provider
        if payload.llm.base_url:
            settings.LLM_BASE_URL = payload.llm.base_url
        resolved_llm_key = _resolve_api_key(payload.llm.api_key, settings.LLM_API_KEY)
        if resolved_llm_key != settings.LLM_API_KEY:
            settings.LLM_API_KEY = resolved_llm_key
            if payload.llm.provider == "openrouter":
                settings.OPENROUTER_API_KEY = resolved_llm_key
            elif payload.llm.provider == "openai":
                settings.OPENAI_API_KEY = resolved_llm_key
            elif payload.llm.provider == "anthropic":
                settings.ANTHROPIC_API_KEY = resolved_llm_key
            elif payload.llm.provider == "google":
                settings.GOOGLE_API_KEY = resolved_llm_key
        if payload.llm.model:
            settings.LLM_MODEL = payload.llm.model
            if payload.llm.provider == "openrouter":
                settings.OPENROUTER_MODEL = payload.llm.model
            elif payload.llm.provider == "openai":
                settings.OPENAI_MODEL = payload.llm.model
            elif payload.llm.provider == "anthropic":
                settings.ANTHROPIC_MODEL = payload.llm.model
            elif payload.llm.provider == "google":
                settings.GOOGLE_MODEL = payload.llm.model

    if payload.image:
        if payload.image.provider:
            settings.IMAGE_PROVIDER = payload.image.provider
        if payload.image.endpoint_url:
            settings.IMAGE_BASE_URL = payload.image.endpoint_url
            settings.IMAGE_ENDPOINT = payload.image.endpoint_url
            if payload.image.provider == "flux":
                settings.FLUX_BASE_URL = payload.image.endpoint_url
        resolved_img_key = _resolve_api_key(payload.image.api_key, settings.IMAGE_API_KEY)
        if resolved_img_key != settings.IMAGE_API_KEY:
            settings.IMAGE_API_KEY = resolved_img_key
            if payload.image.provider == "flux":
                settings.FLUX_API_KEY = resolved_img_key
        if payload.image.model:
            settings.IMAGE_MODEL = payload.image.model
            if payload.image.provider == "flux":
                settings.FLUX_MODEL = payload.image.model

    if payload.compute:
        if payload.compute.provider:
            settings.COMPUTE_PROVIDER = payload.compute.provider
        if payload.compute.endpoint_id:
            settings.COMPUTE_ENDPOINT_ID = payload.compute.endpoint_id
            settings.RUNPOD_ENDPOINT_ID = payload.compute.endpoint_id
        if payload.compute.api_key and not payload.compute.api_key.startswith("****") and not "..." in payload.compute.api_key:
            settings.COMPUTE_API_KEY = payload.compute.api_key
            settings.RUNPOD_API_KEY = payload.compute.api_key

    # Save to persistent storage file
    settings.save_persistent_settings({
        "llm": {
            "provider": settings.LLM_PROVIDER,
            "base_url": settings.LLM_BASE_URL,
            "api_key": settings.LLM_API_KEY,
            "model": settings.LLM_MODEL
        },
        "image": {
            "provider": settings.IMAGE_PROVIDER,
            "endpoint_url": settings.IMAGE_BASE_URL or settings.IMAGE_ENDPOINT,
            "api_key": settings.IMAGE_API_KEY,
            "model": settings.IMAGE_MODEL
        },
        "compute": {
            "provider": settings.COMPUTE_PROVIDER,
            "endpoint_id": settings.COMPUTE_ENDPOINT_ID or settings.RUNPOD_ENDPOINT_ID,
            "api_key": settings.COMPUTE_API_KEY or settings.RUNPOD_API_KEY
        }
    })

    logger.info(f"Updated Provider Settings: LLM={settings.LLM_PROVIDER}, Image={settings.IMAGE_PROVIDER}, Compute={settings.COMPUTE_PROVIDER}")
    return get_provider_settings()


@router.post("/providers/test", response_model=TestProviderResponse)
def test_provider_connection(payload: TestProviderRequest):
    """Tests connectivity and credentials for a specified provider category."""
    cat = payload.category.lower()
    start_t = time.time()

    try:
        if cat == "llm":
            p_name = payload.provider or settings.LLM_PROVIDER
            inst = ProviderFactory.get_llm_provider(
                provider_type=p_name,
                config={
                    "api_key": payload.api_key if (payload.api_key and not payload.api_key.startswith("****")) else settings.LLM_API_KEY,
                    "base_url": payload.base_url,
                    "model": payload.model
                }
            )
            res = inst.test_connection()
            latency = int((time.time() - start_t) * 1000)
            return TestProviderResponse(
                status=res.get("status", "SUCCESS"),
                category="llm",
                provider=inst.provider_name,
                latency_ms=res.get("latency_ms", latency),
                message=res.get("message", "LLM Provider connection successful.")
            )

        elif cat == "image":
            p_name = payload.provider or settings.IMAGE_PROVIDER
            inst = ProviderFactory.get_image_provider(
                provider_type=p_name,
                config={
                    "api_key": payload.api_key if (payload.api_key and not payload.api_key.startswith("****")) else settings.IMAGE_API_KEY,
                    "endpoint_url": payload.endpoint_url or payload.base_url,
                    "model": payload.model
                }
            )
            res = inst.test_connection()
            latency = int((time.time() - start_t) * 1000)
            return TestProviderResponse(
                status=res.get("status", "SUCCESS"),
                category="image",
                provider=inst.provider_name,
                latency_ms=res.get("latency_ms", latency),
                message=res.get("message", "Image Provider connection successful.")
            )

        elif cat == "compute":
            p_name = payload.provider or settings.COMPUTE_PROVIDER
            inst = ProviderFactory.get_compute_provider(
                provider_type=p_name,
                config={
                    "api_key": payload.api_key if (payload.api_key and not payload.api_key.startswith("****")) else settings.COMPUTE_API_KEY,
                    "endpoint_id": payload.endpoint_id,
                    "base_url": payload.base_url
                }
            )
            res = inst.test_connection()
            latency = int((time.time() - start_t) * 1000)
            return TestProviderResponse(
                status=res.get("status", "SUCCESS"),
                category="compute",
                provider=inst.provider_name,
                latency_ms=latency,
                message=res.get("message", "Compute Provider ready.")
            )

        raise HTTPException(status_code=400, detail=f"Invalid category '{payload.category}'. Use 'llm', 'image', or 'compute'.")

    except Exception as e:
        latency = int((time.time() - start_t) * 1000)
        return TestProviderResponse(
            status="FAILED",
            category=cat,
            provider=payload.provider or "unknown",
            latency_ms=latency,
            message=f"Connection test failed: {str(e)}"
        )
