import pytest 
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

test_email = "test@gmail.com"
test_password = "test_123456"

@pytest.fixture(scope="module")
def setup_user():
    yield

def test_register_user(setup_user):
    response = client.post("/auth/register", json={"email": test_email, "password": test_password})
    assert response.status_code == 200
    assert response.json()["message"] == "User created successfully"

def test_login_user():
    response = client.post("/auth/login", json={"email": test_email, "password": test_password})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()

def test_refresh_token():
    login_response = client.post("/auth/login", json={"email": test_email, "password": test_password})
    refresh_token = login_response.json()["refresh_token"]

    response = client.post("/auth/refresh-token", json={"refresh_token": refresh_token})
    assert response.status_code == 200
    assert "access_token" in response.json()