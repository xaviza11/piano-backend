import sys
import os
from fastapi.testclient import TestClient
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app

client = TestClient(app)

@pytest.fixture(scope="module")
def guest_token():
    guest_token_response = client.get("/guestToken/create")
    assert guest_token_response.status_code == 200
    return guest_token_response.json()["guest_token"]

@pytest.fixture(scope="module")
def access_token(guest_token):
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

def test_generate_melody_success(guest_token):
    tone = "A Major" 

    response = client.get(
        f"/song/generate_song?tone=A%23%20Minor",
        headers={"Authorization": f"Bearer {guest_token}"}
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["message"] == "Melody generated successfully"

    assert "notes" in response_data
    assert isinstance(response_data["notes"], list)

    for note_data in response_data["notes"]:
        assert "note" in note_data
        assert "time" in note_data
        assert "velocity" in note_data
        assert "duration" in note_data
        assert isinstance(note_data["note"], str)
        assert isinstance(note_data["time"], float)
        assert isinstance(note_data["velocity"], float)
        assert isinstance(note_data["duration"], float)
