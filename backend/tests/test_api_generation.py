def test_end_to_end_generation_pipeline(client):
    # 1. Create Project
    proj_res = client.post("/api/v1/projects", json={
        "name": "NugiProperti Internal Content"
    })
    assert proj_res.status_code == 201
    project_id = proj_res.json()["id"]

    # 2. Trigger Generation Pipeline
    gen_res = client.post("/api/v1/content/generate", json={
        "project_id": project_id,
        "topic": "3 Trik Mengubah Leads Dingin Menjadi Janji Survey Lokasi",
        "target_audience": "Leader Sales & Agent Properti",
        "content_pillar": "educational",
        "tone_of_voice": "professional_authoritative"
    })
    assert gen_res.status_code == 201
    gen_data = gen_res.json()

    assert gen_data["success"] is True
    assert gen_data["content_id"] is not None
    assert gen_data["job_id"] is not None
    assert gen_data["headline"] is not None
    assert gen_data["body_caption"] is not None
    assert gen_data["asset_path"] is not None
    assert gen_data["qa_result"]["status"] in ["PASSED", "WARNING"]

    # 3. Verify Content in Content List API
    content_list_res = client.get(f"/api/v1/content?project_id={project_id}")
    assert content_list_res.status_code == 200
    items = content_list_res.json()
    assert len(items) == 1
    assert items[0]["id"] == gen_data["content_id"]
    assert len(items[0]["assets"]) >= 1

    # 4. Verify Job Status API
    job_res = client.get(f"/api/v1/jobs/{gen_data['job_id']}")
    assert job_res.status_code == 200
    job_data = job_res.json()
    assert job_data["status"] == "COMPLETED"
    assert job_data["progress_percentage"] == 100
