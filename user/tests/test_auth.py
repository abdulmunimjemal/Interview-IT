import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Sample test data
test_emails = [
    "testuser1@example.com",
    "testuser2@example.com",
    "testuser3@example.com",
    "testuser4@example.com"
]
test_password = "testpassword123"
new_password = "newpassword123"
created_user_tokens: list[str] = []

@pytest.fixture(scope="module", autouse=True)
def setup_teardown():
    # Teardown logic: delete test users after all tests run
    yield
    # Delete all created users
    for token in created_user_tokens:
        client.delete("/auth/delete-user", headers={"Authorization": f"Bearer {token}"})


def test_register_user():
    response = client.post("/auth/register", json={"email": test_emails[0], "password": test_password})
    assert response.status_code == 200
    assert "verification email has been sent" in response.json()["message"]

def test_login_user_unverified():
    response = client.post("/auth/login", json={"email": test_emails[0], "password": test_password})
    assert response.status_code == 403
    assert "Email not verified" in response.json()["detail"]

def test_register_and_check_verification():
    # Register a new user for verification test
    response = client.post("/auth/register", json={"email": test_emails[1], "password": test_password})
    assert response.status_code == 200
    assert "verification email has been sent" in response.json()["message"]

    # Login to get access token
    login_response = client.post("/auth/login", json={"email": test_emails[1], "password": test_password})
    assert login_response.status_code == 403  # Email is not verified

def test_change_password():
    # Register a new user for password change test
    client.post("/auth/register", json={"email": test_emails[2], "password": test_password})

    # Login to get access token
    login_response = client.post("/auth/login", json={"email": test_emails[2], "password": test_password})
    assert login_response.status_code == 403  # Email is not verified

    # Simulate email verification (would require mocking Firebase response in a real test)
    # For demonstration, we assume email gets verified

    # Change password using the token
    response = client.post(
        "/auth/change-password", 
        headers={"Authorization": f"Bearer {login_response.json().get('access_token', '')}"}, 
        json={"new_password": new_password}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Password changed successfully"

    created_user_tokens.append(login_response.json().get('access_token'))

def test_delete_user():
    # Register and login a new user for deletion
    client.post("/auth/register", json={"email": test_emails[3], "password": test_password})
    login_response = client.post("/auth/login", json={"email": test_emails[3], "password": test_password})
    assert login_response.status_code == 403  # Email is not verified

    # Simulate email verification (would require mocking Firebase response in a real test)
    # For demonstration, we assume email gets verified

    # Delete the user
    delete_response = client.delete("/auth/delete-user", headers={"Authorization": f"Bearer {login_response.json().get('access_token', '')}"})
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "User deleted successfully"
