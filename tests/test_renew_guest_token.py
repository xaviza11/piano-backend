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

def test_renew_guest_token_success(guest_token):
    response = client.get("/guestToken/create")
    token = response.json()["guest_token"]
    
    response = client.post("/guestToken/renew", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json()["message"] == "Guest token renewed successfully"
    assert "token" in response.json()

def test_renew_guest_token_no_renewal_needed(guest_token):
    response = client.post("/guestToken/renew", headers={"Authorization": f"Bearer {guest_token}"})

    assert response.status_code == 200
    assert response.json()["message"] == "Guest token does not need renewal yet"
    assert response.json()["token"] == guest_token

def test_renew_guest_token_invalid(guest_token):
    invalid_token = "invalid.token.here"

    response = client.post("/guestToken/renew", headers={"Authorization": f"Bearer {invalid_token}"})

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid guest token"
