def test_trainee_can_request_matching_mentor(client):
    login = client.post("/auth/login", json={"email": "trainee@capacityconnect.gov.in", "password": "Demo@123"})
    assert login.status_code == 200, login.text
    response = client.post("/demo/mentorship", json={"trainer_id": "trainer-arjun"})
    assert response.status_code == 200, response.text
    assert response.json()["message"] == "Mentorship request sent. The trainer will respond through Capacity Connect."
