from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
from app.core.config import settings
from app.providers.factory import ProviderFactory

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
            "image": img.provider_name
        }
    }
