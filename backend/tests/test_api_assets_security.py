import os
from pathlib import Path

from app.core.config import settings
from app.providers.factory import ProviderFactory


def _write_sample_asset() -> str:
    """Writes a real asset via LocalStorageProvider and returns its stored relative path."""
    storage = ProviderFactory.get_storage_provider()
    # Provider returns the path relative to the storage base parent.
    stored = storage.save(b"\x89PNG\r\n\x1a\nfake-image-data", "sample_asset.png", subfolder="security_test")
    return stored


def test_download_valid_asset_returns_file(client):
    stored = _write_sample_asset()
    response = client.get("/api/v1/assets/download", params={"path": stored})
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("image/")


def test_download_relative_path_inside_storage(client):
    # A path given as relative to the storage root itself must also work.
    p = Path(settings.storage_path) / "security_test" / "sample_asset.png"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(b"\x89PNG\r\n\x1a\nfake2")
    response = client.get("/api/v1/assets/download", params={"path": "security_test/sample_asset.png"})
    assert response.status_code == 200


def test_download_rejects_absolute_path(client):
    evil = str(Path("C:/Windows/win.ini")) if os.name == "nt" else "/etc/passwd"
    response = client.get("/api/v1/assets/download", params={"path": evil})
    assert response.status_code == 404


def test_download_rejects_parent_traversal(client):
    # backend/app/core/config.py physically exists outside the storage root
    # and was reachable via ../ under the old resolver; must now 404.
    response = client.get("/api/v1/assets/download", params={"path": "../app/core/config.py"})
    assert response.status_code == 404


def test_download_rejects_deep_traversal(client):
    response = client.get("/api/v1/assets/download", params={"path": "../../../../../../Windows/win.ini"})
    assert response.status_code == 404


def test_download_rejects_backslash_traversal(client):
    response = client.get("/api/v1/assets/download", params={"path": "..\\..\\..\\pyproject.toml"})
    assert response.status_code == 404


def test_download_missing_asset(client):
    response = client.get("/api/v1/assets/download", params={"path": "does_not_exist/x.png"})
    assert response.status_code == 404
