def test_admin_overview_contains_intelligence_and_impact(client):
    login = client.post("/auth/login", json={"email": "admin@capacityconnect.gov.in", "password": "Demo@123"})
    assert login.status_code == 200, login.text
    response = client.get("/demo/overview")
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["role"] == "admin"
    assert any(row["competency"] == "Cybersecurity" for row in body["heatmap"])
    assert body["impact"]
