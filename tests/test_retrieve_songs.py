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

def test_retrieve_all_songs(guest_token, access_token):
    song_data = {
        "name": "Test Song All",
        "tone": "G Major",
        "author": "Test Author All",
        "notes": [
            {"note": "D4", "time": 0.0, "velocity": 1.0, "duration": 0.5}
        ]
    }

    client.post(
        "/song/create",
        json=song_data,
        headers={"Authorization": f"Bearer {access_token}"}
    )

    retrieve_response = client.get(
        "/song/retrieve_songs",
        headers={"Authorization": f"Bearer {guest_token}"}
    )

    assert retrieve_response.status_code == 400

    assert retrieve_response.json()["detail"] == 'At least one search parameter is required'

def test_retrieve_songs_by_name(guest_token, access_token):
    song_data = {
        "name": "Unique Name Song",
        "tone": "A Minor",
        "author": "Author1",
        "notes": [
            {"note": "C4", "time": 0.0, "velocity": 1.0, "duration": 0.5}
        ]
    }

    client.post(
        "/song/create",
        json=song_data,
        headers={"Authorization": f"Bearer {access_token}"}
    )

    retrieve_response = client.get(
        "/song/retrieve_songs?name=Unique Name Song",
        headers={"Authorization": f"Bearer {guest_token}"}
    )

    assert retrieve_response.status_code == 200

    retrieved_songs = retrieve_response.json()["songs"]

    assert len(retrieved_songs) >= 1
    assert retrieved_songs[0]["name"] == "Unique Name Song"

def test_retrieve_songs_by_author(guest_token, access_token):
    song_data = {
        "name": "Author Specific Song",
        "tone": "B Major",
        "author": "Unique Author",
        "notes": [
            {"note": "E4", "time": 0.0, "velocity": 1.0, "duration": 0.5}
        ]
    }

    client.post(
        "/song/create",
        json=song_data,
        headers={"Authorization": f"Bearer {access_token}"}
    )

    retrieve_response = client.get(
        "/song/retrieve_songs?author=Unique Author",
        headers={"Authorization": f"Bearer {guest_token}"}
    )

    assert retrieve_response.status_code == 200
    retrieved_songs = retrieve_response.json()["songs"]

    assert len(retrieved_songs) >= 1
    assert retrieved_songs[0]["author"] == "Unique Author"

def test_retrieve_songs_by_tone(guest_token, access_token):
    song_data = {
        "name": "Tone Specific Song",
        "tone": "D Minor",
        "author": "Author2",
        "notes": [
            {"note": "F4", "time": 0.0, "velocity": 1.0, "duration": 0.5}
        ]
    }

    client.post(
        "/song/create",
        json=song_data,
        headers={"Authorization": f"Bearer {access_token}"}
    )

    retrieve_response = client.get(
        "/song/retrieve_songs?tone=D Minor",
        headers={"Authorization": f"Bearer {guest_token}"}
    )

    assert retrieve_response.status_code == 200
    retrieved_songs = retrieve_response.json()["songs"]

    assert len(retrieved_songs) >= 1
    assert retrieved_songs[0]["tone"] == "D Minor"

def test_retrieve_songs_not_found(guest_token):
    retrieve_response = client.get(
        "/song/retrieve_songs?name=NonExistentSong",
        headers={"Authorization": f"Bearer {guest_token}"}
    )

    assert retrieve_response.status_code == 404
    assert retrieve_response.json()["detail"] == "No songs found"
