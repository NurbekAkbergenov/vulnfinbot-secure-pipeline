"""Automated unit tests for Mini-VulnFinBot."""

import pytest
from app import create_app


@pytest.fixture
def app():
    app = create_app({"TESTING": True})
    return app


@pytest.fixture
def client(app):
    return app.test_client()


def test_health_check(client):
    """Test GET /health returns status healthy."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data == {"status": "healthy"}


def test_chat_success(client):
    """Test POST /api/chat with a valid message returns an assistant response."""
    response = client.post(
        "/api/chat",
        json={"message": "How can I manage my monthly budget?"}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert "response" in data
    assert len(data["response"]) > 0


def test_chat_missing_content_type(client):
    """Test POST /api/chat without application/json Content-Type is rejected (415)."""
    response = client.post("/api/chat", data="not json")
    assert response.status_code == 415
    data = response.get_json()
    assert "error" in data


def test_chat_invalid_json(client):
    """Test POST /api/chat with invalid JSON object body is rejected (400)."""
    response = client.post(
        "/api/chat",
        json=["not", "a", "dict"]
    )
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data


def test_chat_missing_message(client):
    """Test POST /api/chat without 'message' key is rejected (400)."""
    response = client.post(
        "/api/chat",
        json={"query": "hello"}
    )
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data


def test_chat_empty_message(client):
    """Test POST /api/chat with an empty or whitespace-only message is rejected (400)."""
    response = client.post(
        "/api/chat",
        json={"message": "   "}
    )
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data


def test_chat_unexpected_input_type(client):
    """Test POST /api/chat where 'message' is not a string is rejected (400)."""
    response = client.post(
        "/api/chat",
        json={"message": 12345}
    )
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data


def test_chat_excessively_long_message(client):
    """Test POST /api/chat with a message exceeding MAX_MESSAGE_LENGTH is rejected (400)."""
    long_msg = "a" * 1500  # Default MAX_MESSAGE_LENGTH is 1000
    response = client.post(
        "/api/chat",
        json={"message": long_msg}
    )
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
