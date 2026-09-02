from pathlib import Path
from fastapi.testclient import TestClient

import app.main as main_module


def test_spa_index_served(client, tmp_path, monkeypatch):
    dist = tmp_path / "frontend_dist"
    dist.mkdir(parents=True)
    (dist / "index.html").write_text("<html>index</html>")
    (dist / "app.js").write_text("console.log(1)")

    monkeypatch.setattr(main_module, "find_frontend_dist", lambda: dist)
    test_app = main_module.create_app()
    with TestClient(test_app) as c:
        # Real static file served directly.
        r2 = c.get("/app.js")
        assert r2.status_code == 200
        assert "console.log" in r2.text

        # Unknown client-side route falls back to index.html.
        r3 = c.get("/some/spa/route")
        assert r3.status_code == 200
        assert "index" in r3.text


def test_spa_rejects_path_traversal(client, tmp_path, monkeypatch):
    dist = tmp_path / "frontend_dist"
    dist.mkdir(parents=True)
    (dist / "index.html").write_text("<html>index</html>")
    # Secret file OUTSIDE the served frontend dist directory.
    secret = tmp_path / "secret.txt"
    secret.write_text("TOP-SECRET")

    monkeypatch.setattr(main_module, "find_frontend_dist", lambda: dist)
    test_app = main_module.create_app()
    with TestClient(test_app) as c:
        r = c.get("/%2e%2e/secret.txt")
        assert r.status_code == 404
        assert "TOP-SECRET" not in r.text

        # Backslash variant
        r2 = c.get("/..%5c..%5csecret.txt")
        assert r2.status_code == 404
        assert "TOP-SECRET" not in r2.text
