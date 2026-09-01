def test_create_and_list_projects(client):
    # 1. Create Brand Profile
    brand_res = client.post("/api/v1/brand-profiles", json={
        "name": "Nugi Properti Studio",
        "primary_color": "#0a101d",
        "secondary_color": "#38bdf8"
    })
    assert brand_res.status_code == 201
    brand_id = brand_res.json()["id"]

    # 2. Create Project
    proj_res = client.post("/api/v1/projects", json={
        "name": "GREN Propertykost Jatinangor",
        "description": "Proyek Rukos Premium Dekat Kampus UNPAD",
        "brand_profile_id": brand_id
    })
    assert proj_res.status_code == 201
    proj_data = proj_res.json()
    assert proj_data["name"] == "GREN Propertykost Jatinangor"
    assert proj_data["slug"] == "gren-propertykost-jatinangor"
    assert proj_data["id"] is not None

    # 3. List Projects
    list_res = client.get("/api/v1/projects")
    assert list_res.status_code == 200
    projects = list_res.json()
    assert len(projects) == 1
    assert projects[0]["id"] == proj_data["id"]


def test_get_project_not_found(client):
    res = client.get("/api/v1/projects/non-existent-uuid")
    assert res.status_code == 404
    data = res.json()
    assert data["success"] is False
