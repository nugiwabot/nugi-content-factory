import os
from pathlib import Path
from fastapi import APIRouter, HTTPException, Query, Response
from fastapi.responses import FileResponse
from app.core.config import settings
from app.providers.factory import ProviderFactory
from app.core.errors import NotFoundError
from app.core.logging import logger

router = APIRouter(prefix="/assets", tags=["Assets"])


@router.get("/download")
def download_asset(path: str = Query(..., description="Relative or canonical asset path")):
    """Streams asset file from local storage provider with robust path fallback."""
    # Clean incoming path
    raw_path = path.strip().lstrip("/").lstrip("\\")
    target_file = Path(raw_path)

    if not target_file.is_absolute():
        candidates = [
            (settings.storage_path / raw_path).resolve(),
            (settings.storage_path.parent / raw_path).resolve(),
            (settings.user_data_dir / raw_path).resolve(),
            (settings.user_data_dir / "storage" / "assets" / raw_path).resolve(),
            (Path(settings.STORAGE_BASE_DIR) / raw_path).resolve(),
            (Path.cwd() / raw_path).resolve(),
            (Path(__file__).resolve().parent.parent.parent.parent / raw_path).resolve()
        ]
        found = False
        for c in candidates:
            if c.is_file():
                target_file = c
                found = True
                break
        if not found:
            logger.warning(f"Asset not found on disk for query '{path}'. Looked in candidates: {[str(c) for c in candidates]}")
            raise HTTPException(status_code=404, detail=f"Asset file not found on disk: {path}")

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
