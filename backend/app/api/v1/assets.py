import os
from pathlib import Path
from fastapi import APIRouter, HTTPException, Query, Response
from fastapi.responses import FileResponse
from app.core.config import settings
from app.providers.factory import ProviderFactory
from app.core.errors import NotFoundError

router = APIRouter(prefix="/assets", tags=["Assets"])


@router.get("/download")
def download_asset(path: str = Query(..., description="Relative or canonical asset path")):
    """Streams asset file from local storage provider."""
    storage = ProviderFactory.get_storage_provider()
    
    # Resolve file path
    target_file = Path(path)
    if not target_file.is_absolute():
        target_file = (settings.storage_path.parent / path).resolve()

    if not target_file.is_file():
        raise HTTPException(status_code=404, detail="Asset file not found on disk.")

    media_type = "image/png"
    if target_file.suffix.lower() in [".jpg", ".jpeg"]:
        media_type = "image/jpeg"
    elif target_file.suffix.lower() == ".webp":
        media_type = "image/webp"

    return FileResponse(
        path=str(target_file),
        media_type=media_type,
        filename=target_file.name
    )
