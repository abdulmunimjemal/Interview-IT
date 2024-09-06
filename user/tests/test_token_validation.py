import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@pytest.fixture(scope="module")
def get_access_token():
    # Register a test user
    test_email = "testuser2@example.com"
    test_password = "testpassword123"
    client.post("/auth/register", json={"email": test_email, "password": test_password})

    # Login to get the access token
    login_response = client.post("/auth/login", json={"email": test_email, "password": test_password})
    access_token = login_response.json()["access_token"]
    return access_token


def test_validate_token(get_access_token):
    response = client.post("/validate/", json={"token": get_access_token})
    assert response.status_code == 200
    assert response.json()["status"] == "success"


def test_invalid_token():
    invalid_token = "invalidtoken123"
    response = client.post("/validate/", json={"token": invalid_token})
    assert response.status_code == 200
    assert response.json()["status"] == "error"
    assert "Invalid credentials" in response.json()["detail"]
