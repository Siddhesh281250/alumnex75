def test_trainee_priority_actions(client):
    login = client.post("/auth/login", json={"email": "trainee@capacityconnect.gov.in", "password": "Demo@123"})
    assert login.status_code == 200, login.text
    overview = client.get("/demo/overview")
    assert overview.status_code == 200
    data = overview.json()
    assert any(item["name"] == "Cybersecurity" for item in data["competencies"])
    path = client.post("/demo/learning-path", json={"focus": "Cybersecurity and Data Analytics"})
    assert path.status_code == 200, path.text
    enroll = client.post("/demo/enroll", json={"course_id": "course-nwp"})
    assert enroll.status_code == 200, enroll.text
    submit = client.post("/demo/assessment/submit", json={"assessment_id": "nwp-checkpoint", "answers": {"q-12": "A"}})
    assert submit.status_code == 200, submit.text
    assert submit.json()["score"] == 78
