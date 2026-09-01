def test_health_endpoint(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert data["database"] == "healthy"
    assert "MockLLMProvider" in data["providers"]["llm"]
    assert "MockImageProvider" in data["providers"]["image"]
    assert "flux_configured" in data["providers"]


def test_flux_health_endpoint_safe(client):
    response = client.get("/api/v1/health/flux")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ("NOT_CONFIGURED", "SUCCESS", "FAILED")
    assert "api_key" not in data  # Never expose secrets
    assert "FLUX_API_KEY" not in str(data.get("message", "")) or "not set" in str(data.get("message", "")) or "empty" in str(data.get("message", ""))


def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "operational"
