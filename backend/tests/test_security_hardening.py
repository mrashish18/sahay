import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings

client = TestClient(app)

def test_oversized_chat_message_rejected():
    """Verify that payloads exceeding max_length (10,000 chars) return HTTP 422 Unprocessable Entity."""
    oversized_message = "A" * 10001
    response = client.post(
        "/api/v1/chat",
        json={"message": oversized_message}
    )
    assert response.status_code == 422

def test_empty_chat_message_rejected():
    """Verify empty chat message returns HTTP 422."""
    response = client.post(
        "/api/v1/chat",
        json={"message": ""}
    )
    assert response.status_code == 422

def test_health_endpoint_response():
    """Verify health endpoint returns clean status without internal information leakage."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_config_security_defaults():
    """Verify configuration settings contain non-empty security keys and configurable OpenAI base URL."""
    assert hasattr(settings, "SECRET_KEY")
    assert hasattr(settings, "OPENAI_BASE_URL")
    assert settings.SECRET_KEY != ""
    assert settings.OPENAI_BASE_URL != ""
