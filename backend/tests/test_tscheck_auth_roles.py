import pytest

@pytest.mark.parametrize("role", ["trainee", "trainer", "admin"])
def test_demo_login_returns_matching_role(client, role):
    response = client.post("/auth/login", json={"email": f"{role}@capacityconnect.gov.in", "password": "Demo@123"})
    assert response.status_code == 200, response.text
    assert response.json()["role"] == role
    me = client.get("/auth/me")
    assert me.status_code == 200
    assert me.json()["role"] == role
