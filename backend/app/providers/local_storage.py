import os
from pathlib import Path
from typing import Optional
from app.providers.base import StorageProvider
from app.core.config import settings
from app.core.errors import StorageError
from app.core.logging import logger


class LocalStorageProvider(StorageProvider):
    """
    Local filesystem storage provider for saving and retrieving rendered assets.
    """
    def __init__(self, base_dir: Optional[str] = None):
        self.base_path = Path(base_dir) if base_dir else settings.storage_path
        self.base_path.mkdir(parents=True, exist_ok=True)

    def save(self, data: bytes, filename: str, subfolder: str = "") -> str:
        try:
            target_dir = self.base_path / subfolder if subfolder else self.base_path
            target_dir.mkdir(parents=True, exist_ok=True)

            # Sanitize filename
            safe_filename = Path(filename).name
            file_path = target_dir / safe_filename

            with open(file_path, "wb") as f:
                f.write(data)

            # Return relative or canonical path string
            rel_path = file_path.relative_to(self.base_path.parent).as_posix()
            logger.debug(f"Saved asset to local storage: {rel_path} ({len(data)} bytes)")
            return rel_path
        except Exception as e:
            raise StorageError(f"Failed to save asset '{filename}': {str(e)}")

    def read(self, file_path: str) -> bytes:
        try:
            # Resolve relative to base_path or project root
            target_file = Path(file_path)
            if not target_file.is_absolute():
                target_file = (self.base_path.parent / file_path).resolve()

            if not target_file.exists():
                raise StorageError(f"Asset file '{file_path}' does not exist.")

            with open(target_file, "rb") as f:
                return f.read()
        except Exception as e:
            raise StorageError(f"Failed to read asset '{file_path}': {str(e)}")

    def exists(self, file_path: str) -> bool:
        target_file = Path(file_path)
        if not target_file.is_absolute():
            target_file = (self.base_path.parent / file_path).resolve()
        return target_file.is_file()

    def delete(self, file_path: str) -> bool:
        try:
            target_file = Path(file_path)
            if not target_file.is_absolute():
                target_file = (self.base_path.parent / file_path).resolve()

            if target_file.exists():
                target_file.unlink()
                logger.debug(f"Deleted asset from local storage: {file_path}")
                return True
            return False
        except Exception as e:
            logger.warning(f"Error deleting asset '{file_path}': {str(e)}")
            return False
