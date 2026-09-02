from pathlib import Path
from fastapi import APIRouter, HTTPException, Query, Response
from fastapi.responses import FileResponse
from app.core.config import settings
from app.core.logging import logger

router = APIRouter(prefix="/assets", tags=["Assets"])


def _resolve_asset_path(raw_path: str) -> Path | None:
    """
    Resolves a stored relative asset path strictly inside the allowed storage
    roots. Absolute paths and any path that escapes containment are rejected.
    """
    cleaned = raw_path.strip().lstrip("/").lstrip("\\")
    candidate = Path(cleaned)

    # Never trust absolute paths supplied over HTTP.
    if candidate.is_absolute():
        return None

    allowed_roots = [
        settings.storage_path.resolve(),
        settings.storage_path.parent.resolve(),
    ]

    for root in allowed_roots:
        resolved = (root / candidate).resolve()
        try:
            resolved.relative_to(root)
        except ValueError:
            # Path escaped the allowed root (e.g. via .. traversal).
            continue
        if resolved.is_file():
            return resolved
    return None


@router.get("/download")
def download_asset(path: str = Query(..., description="Relative or canonical asset path")):
    """Streams an asset file strictly from the local storage directory tree."""
    target_file = _resolve_asset_path(path)
    if target_file is None:
        logger.warning(f"Asset not found or outside storage root: '{path}'")
        raise HTTPException(status_code=404, detail=f"Asset file not found on disk: {path}")

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
