import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Basketball" in data
    assert "Volleyball" in data
    assert isinstance(data["Basketball"]["participants"], list)

def test_signup_for_activity():
    # Test successful signup
    response = client.post("/activities/Basketball/signup?email=test@example.com")
    assert response.status_code == 200
    data = response.json()
    assert "Signed up test@example.com for Basketball" in data["message"]

    # Verify the participant was added
    response = client.get("/activities")
    data = response.json()
    assert "test@example.com" in data["Basketball"]["participants"]

def test_signup_for_nonexistent_activity():
    response = client.post("/activities/NonExistent/signup?email=test@example.com")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Activity not found"

def test_signup_duplicate():
    # First signup
    client.post("/activities/Volleyball/signup?email=duplicate@example.com")
    # Try to signup again
    response = client.post("/activities/Volleyball/signup?email=duplicate@example.com")
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Student already signed up for this activity"

def test_unregister_participant():
    # First signup
    client.post("/activities/Art%20Club/signup?email=unregister@example.com")
    # Then unregister
    response = client.delete("/activities/Art%20Club/participants/unregister@example.com")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Participant unregistered successfully"

    # Verify the participant was removed
    response = client.get("/activities")
    data = response.json()
    assert "unregister@example.com" not in data["Art Club"]["participants"]

def test_unregister_nonexistent_activity():
    response = client.delete("/activities/NonExistent/participants/test@example.com")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Activity not found"

def test_unregister_nonexistent_participant():
    response = client.delete("/activities/Basketball/participants/nonexistent@example.com")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Participant not found"