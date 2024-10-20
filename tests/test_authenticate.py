import sys
import os
from fastapi.testclient import TestClient
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app

client = TestClient(app)

@pytest.fixture(scope="module")
def guest_token():
    response = client.get("/guestToken/create")
    return response.json()["guest_token"]

def test_authenticate_user_success(guest_token):
    user_data = {
        "email": "testuserAuth@example.com",
        "password": "testpassword123A"
    }

    client.post(
        "/auth/register", 
        json=user_data,
        headers={"Authorization": f"Bearer {guest_token}"}
    )

    response = client.post(
        "/user/login",
        json={
            "email": "testuserAuth@example.com",
            "password": "testpassword123A"
        },
        headers={"Authorization": f"Bearer {guest_token}"}
    )
    
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_authenticate_user_invalid_password(guest_token):
    response = client.post(
        "/user/login",
        json={
            "email": "testuserAuth@example.com",
            "password": "wrongpassword1A"
        },
        headers={"Authorization": f"Bearer {guest_token}"}
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Wrong password"}

def test_authenticate_user_not_found(guest_token):
    response = client.post(
        "/user/login",
        json={
            "email": "testuserAuthaasd@example.com",
            "password": "testpassword123A"
        },
        headers={"Authorization": f"Bearer {guest_token}"}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_authenticate_user_invalid_token():
    invalid_token = "Bearer invalid_token"

    response = client.post(
        "/user/login",
        json={
            "email": "testuserAuth@example.com",
            "password": "testpassword123A"
        },
        headers={"Authorization": f"Bearer {guest_token}"}
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid guest token"}

def test_authenticate_user_undefined_token():
    response = client.post(
        "/user/login",
        json={
            "email": "testuserAuth@example.com",
            "password": "testpassword123A"
        },
        headers={"Authorization": ''}
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid authorization header"}

def test_authenticate_user_not_contain_authorization():
    response = client.post(
        "/user/login",
        json={
            "email": "testuserAuth@example.com",
            "password": "testpassword123A"
        }
    )

    assert response.status_code == 422
    assert "detail" in response.json()
    assert any("missing" in str(detail) for detail in response.json()["detail"])
