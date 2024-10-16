import sys
import os
from fastapi.testclient import TestClient
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app

client = TestClient(app)

@pytest.fixture(scope="module")
def access_token():
    guest_token_response = client.get("/guestToken/create")
    guest_token = guest_token_response.json()["guest_token"]

    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword123A"
    }
    client.post(
        "/user/register",
        json=user_data,
        headers={"Authorization": f"Bearer {guest_token}"}
    )

    login_data = {
        "email": "testuser@example.com",
        "password": "testpassword123A"
    }
    login_response = client.post(
        "/user/login",
        json=login_data,
        headers={"Authorization": f"Bearer {guest_token}"}
    )

    assert login_response.status_code == 200
    assert "access_token" in login_response.json()
    
    return login_response.json()["access_token"]

def test_create_song_success(access_token):
    song_data = {
        "name": "Test Song",
        "tone": "C Major",
        "author": "Test Author",
        "notes": [
            {"note": "C4", "time": 0.0, "velocity": 1.0, "duration": 0.5},
            {"note": "E4", "time": 1.0, "velocity": 0.9, "duration": 0.5},
            {"note": "G4", "time": 2.0, "velocity": 0.8, "duration": 0.5}
        ]
    }

    response = client.post(
        "/song/create",
        json=song_data,
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Song created successfully"

def test_create_song_invalid_token(access_token):
    song_data = {
        "name": "Test Song",
        "tone": "C Major",
        "author": "Test Author",
        "notes": [
            {"note": "C4", "time": 0.0, "velocity": 1.0, "duration": 0.5}
        ]
    }

    invalid_access_token = 'asdf123'

    response = client.post(
        "/song/create",
        json=song_data,
        headers={"Authorization": f"Bearer {invalid_access_token}"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid access token"
