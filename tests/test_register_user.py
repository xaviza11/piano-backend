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

def test_register_user_success(guest_token):
    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword123A"
    }

    response = client.post(
        "/auth/register", 
        json=user_data,
        headers={"Authorization": f"Bearer {guest_token}"}
    )

    assert response.status_code == 200
    assert response.json() == {"message": "User registered successfully"}

def test_register_user_already_exists(guest_token):
    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword123A"
    }

    client.post(
        "/auth/register", 
        json=user_data,
        headers={"Authorization": f"Bearer {guest_token}"}
    )

    response = client.post(
        "/auth/register", 
        json=user_data,
        headers={"Authorization": f"Bearer {guest_token}"}
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "User already exists"}

def test_register_user_invalid_token():
    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword123A"
    }

    invalid_token = "Bearer invalid_token"

    response = client.post(
        "/auth/register", 
        json=user_data,
        headers={"Authorization": invalid_token}
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid guest token"}

def test_register_user_undefined_token():
    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword123A"
    }

    response = client.post(
        "/auth/register", 
        json=user_data,
        headers={"Authorization": ''}
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid authorization header"}

def test_register_user_not_contain_authorization():
    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword123A"
    }

    response = client.post(
        "/auth/register", 
        json=user_data,
    )

    assert response.status_code == 422
    assert "detail" in response.json() 
    assert any("missing" in str(detail) for detail in response.json()["detail"])
