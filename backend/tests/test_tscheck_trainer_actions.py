def test_trainer_generate_and_publish_assessment(client):
    login = client.post("/auth/login", json={"email": "trainer@capacityconnect.gov.in", "password": "Demo@123"})
    assert login.status_code == 200, login.text
    generated = client.post("/demo/assessment/generate", json={"subject": "Numerical Weather Prediction", "topic": "Model validation and forecast verification", "questions": 5, "difficulty": "Intermediate"})
    assert generated.status_code == 200, generated.text
    body = generated.json()
    assert body["status"] == "Needs trainer review"
    assert len(body["questions"]) >= 3
    published = client.post("/demo/assessment/publish", json={})
    assert published.status_code == 200, published.text
