import sys
import os
from fastapi.testclient import TestClient
import pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app 

client = TestClient(app)

def test_create_guest_token():
    response = client.get("/guestToken/create")

    assert response.status_code == 200
    assert "guest_token" in response.json()
    assert isinstance(response.json()["guest_token"], str)
    assert len(response.json()["guest_token"]) > 0
