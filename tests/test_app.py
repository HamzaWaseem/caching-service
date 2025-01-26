import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_valid_payload():
    response = client.post(
        "/payload",
        json={
            "list_1": ["first string", "second string"],
            "list_2": ["other string", "another string"]
        }
    )
    assert response.status_code == 200
    assert "payload_id" in response.json()

def test_payload_with_empty_lists():
    response = client.post(
        "/payload",
        json={
            "list_1": [],
            "list_2": []
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Both input lists are empty."

def test_payload_missing_list():
    response = client.post(
        "/payload",
        json={
            "list_1": ["first string"]
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Both 'list_1' and 'list_2' must be provided."

def test_payload_with_extra_param():
    response = client.post(
        "/payload",
        json={
            "list_1": ["first string"],
            "list_2": ["other string"],
            "extra_param": "not allowed"
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Only 'list_1' and 'list_2' are allowed in the request body."
