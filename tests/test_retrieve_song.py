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

def test_retrieve_song_success(access_token, guest_token):
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

    create_response = client.post(
        "/song/create",
        json=song_data,
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert create_response.status_code == 200
    created_song = create_response.json()

    song_id = created_song.get("id")

    retrieve_response = client.get(
        f"/song/retrieve/{song_id}",
        headers={"Authorization": f"Bearer {guest_token}"}
    )

    assert retrieve_response.status_code == 200
    retrieved_song = retrieve_response.json()

    assert retrieved_song["song_data"]["name"] == song_data["name"]
    assert retrieved_song["song_data"]["tone"] == song_data["tone"]
    assert retrieved_song["song_data"]["author"] == song_data["author"]
    assert retrieved_song["song_data"]["notes"] == song_data["notes"]

def test_retrieve_song_not_found(guest_token):
    non_existing_song_id = "60f7c4e6d3b8a422b8b1d3b5"

    retrieve_response = client.get(
        f"/song/retrieve/{non_existing_song_id}",
        headers={"Authorization": f"Bearer {guest_token}"}
    )

    assert retrieve_response.status_code == 404
    assert retrieve_response.json()["detail"] == "Song not found"

def test_retrieve_invalid_song_id(guest_token):
    invalid_song_id = "123invalid"

    retrieve_response = client.get(
        f"/song/retrieve/{invalid_song_id}",
        headers={"Authorization": f"Bearer {guest_token}"}
    )

    assert retrieve_response.status_code == 400
    assert retrieve_response.json()["detail"] == "Invalid song ObjectId"
