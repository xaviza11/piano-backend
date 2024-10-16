import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app

client = TestClient(app)

@pytest.fixture(scope="module")
def guest_token():
    response = client.get("/guestToken/create")
    return response.json()["guest_token"]

@pytest.fixture(scope='module')
def register_user():
    guest_token = client.get("/guestToken/create")
    token = guest_token.json()["guest_token"]

    user_data = {
        "username": "testuser",
        "email": "newemail@example.com",
        "password": "testpassword123A"
    }

    client.post(
        "/user/register", 
        json=user_data,
        headers={"Authorization": f"Bearer {token}"}
    )

@pytest.fixture
def access_token(guest_token, register_user):
    response = client.post(
        "/user/login",
        json={
            "email": "newemail@example.com",
            "password": "testpassword123A"
        },
        headers={"Authorization": f"Bearer {guest_token}"}
    )
    
    assert "access_token" in response.json()
    assert response.status_code == 200
    return response.json()["access_token"]

def test_update_user_success(access_token):
    user_data = {
        "email": "newemail@example.com",
        "password": "testpassword123A",
        "new_email": "newemail@example.com",
        "new_password": "newpassword123A",
        "new_user_name": "newusername"
    }

    response = client.put(
        "/user/update",
        json=user_data,
        headers={"Authorization": f"Bearer {access_token}"}
    )
    
    assert response.status_code == 200
    assert response.json() == {"message": "User updated successfully"}

def test_update_user_not_found(access_token):
    user_data = {
        "email": "nonexistentemail@example.com",
        "password": "testpassword123A",
        "new_email": "newemailASD@example.com",
        "new_password": "newpassword123A",
        "new_user_name": "newusername"
    }

    response = client.put(
        "/user/update",
        json=user_data,
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_update_user_wrong_password(access_token):
    user_data = {
        "email": "newemail@example.com",
        "password": "wrongpasswordA123",
        "new_email": "newemail@example.com",
        "new_password": "newpassword123ASDA",
        "new_user_name": "newusername"
    }

    response = client.put(
        "/user/update",
        json=user_data,
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Wrong password"}
