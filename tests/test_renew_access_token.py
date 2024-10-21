import sys
import os
from fastapi.testclient import TestClient
import pytest
from datetime import datetime, timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app

client = TestClient(app)

@pytest.fixture(scope="module")
def guest_token():
    response = client.get("/guestToken/create")
    return response.json()["guest_token"]


def test_renew_access_token_success(guest_token):
    user_data = {
        "username": "testuser",
        "email": "renewTokenUser@example.com",
        "password": "testpassword123A"
    }

    login_data = {
        "email": "renewTokenUser@example.com",
        "password": "testpassword123A"
    }

    client.post(
        "/user/register", 
        json=user_data,
        headers={"Authorization": f"Bearer {guest_token}"}
    )

    login_response = client.post("/user/login", json=login_data, headers={"Authorization": f"Bearer {guest_token}"})

    access_token = login_response.json()["access_token"]
    
    response = client.post("/accessToken/renew", headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == 200
    assert response.json()["message"] == "Token renewed successfully"
    assert "token" in response.json()

def test_renew_access_token_invalid_token():
    invalid_token = "Bearer invalid_token"
    
    response = client.post("/accessToken/renew", headers={"Authorization": invalid_token})
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token"}

def test_renew_access_token_no_authorization_header():
    response = client.post("/accessToken/renew", headers={})
    assert response.status_code == 422
