import httpx
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
from app.core.config import settings
from app.providers.factory import ProviderFactory
from app.core.logging import logger

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("")
def health_check(db: Session = Depends(get_db)):
    """
    Verifies service health, database connectivity, and provider readiness.
    """
    # 1. DB Connectivity Check
    db_status = "healthy"
    try:
        db.execute(text("SELECT 1"))
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    # 2. Storage Check
    storage = ProviderFactory.get_storage_provider()
    storage_status = "ready" if settings.storage_path.exists() else "unhealthy"

    # 3. Providers Check
    llm = ProviderFactory.get_llm_provider()
    img = ProviderFactory.get_image_provider()

    # 4. Flux Configuration Status (Safe boolean, never exposes secret)
    flux_configured = bool(settings.FLUX_API_KEY and len(settings.FLUX_API_KEY.strip()) > 0)

    return {
        "status": "online",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.APP_ENV,
        "database": db_status,
        "storage": {
            "status": storage_status,
            "provider": settings.STORAGE_PROVIDER,
            "path": str(settings.storage_path)
        },
        "providers": {
            "llm": llm.provider_name,
            "image": img.provider_name,
            "flux_configured": flux_configured
        }
    }


@router.get("/flux")
def test_flux_connection():
    """
    Safely tests Flux / Black Forest Labs API readiness and connectivity without exposing API keys.
    """
    api_key = settings.FLUX_API_KEY
    if not api_key or len(api_key.strip()) == 0:
        return {
            "status": "NOT_CONFIGURED",
            "configured": False,
            "provider": "FluxImageProvider",
            "model": settings.FLUX_MODEL,
            "endpoint": settings.FLUX_BASE_URL,
            "message": "FLUX_API_KEY is empty in .env. Application is safely using MockImageProvider fallback with 100% functionality."
        }

    try:
        # Ping the Flux API endpoint safely with headers
        headers = {
            "Authorization": f"Bearer {api_key.strip()}",
            "Content-Type": "application/json"
        }
        test_url = f"{settings.FLUX_BASE_URL.rstrip('/')}/models"
        
        with httpx.Client(timeout=10.0) as client:
            resp = client.get(test_url, headers=headers)
            if resp.status_code in (200, 201):
                return {
                    "status": "SUCCESS",
                    "configured": True,
                    "provider": "FluxImageProvider",
                    "model": settings.FLUX_MODEL,
                    "endpoint": settings.FLUX_BASE_URL,
                    "message": "Flux API connection verified successfully."
                }
            elif resp.status_code == 401 or resp.status_code == 403:
                return {
                    "status": "FAILED",
                    "configured": True,
                    "provider": "FluxImageProvider",
                    "model": settings.FLUX_MODEL,
                    "endpoint": settings.FLUX_BASE_URL,
                    "message": "Authentication failed. Please verify your FLUX_API_KEY in .env."
                }
            else:
                return {
                    "status": "FAILED",
                    "configured": True,
                    "provider": "FluxImageProvider",
                    "model": settings.FLUX_MODEL,
                    "endpoint": settings.FLUX_BASE_URL,
                    "message": f"Flux API returned status code {resp.status_code}."
                }
    except httpx.RequestError as req_err:
        logger.warning(f"Flux API connection check encountered network error: {type(req_err).__name__}")
        return {
            "status": "FAILED",
            "configured": True,
            "provider": "FluxImageProvider",
            "model": settings.FLUX_MODEL,
            "endpoint": settings.FLUX_BASE_URL,
            "message": "Network error reaching Flux API endpoint. Check internet connection or base URL."
        }
    except Exception as e:
        logger.warning(f"Flux API test error: {type(e).__name__}")
        return {
            "status": "FAILED",
            "configured": True,
            "provider": "FluxImageProvider",
            "model": settings.FLUX_MODEL,
            "endpoint": settings.FLUX_BASE_URL,
            "message": f"Error testing Flux API: {type(e).__name__}"
        }
