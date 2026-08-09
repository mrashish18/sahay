import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.anyio
async def test_chat_crisis_flow():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        payload = {
            "message": "My house was damaged by flooding and we have nowhere to stay."
        }
        response = await ac.post("/api/v1/chat", json=payload)
        
    assert response.status_code == 200
    data = response.json()
    assert data["flow"] == "CRISIS"
    assert data["urgency"]["level"] == "CRISIS"
    assert data["urgency"]["score"] > 0.8
    assert len(data["recommendations"]) > 0
    assert len(data["documents"]) > 0
    assert len(data["action_plan"]) > 0
    assert len(data["sources"]) > 0
    assert "DISCLAIMER" in data["disclaimer"]

@pytest.mark.anyio
async def test_chat_public_service_flow():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        payload = {
            "message": "I lost my job and my family income is very low. What government support might I qualify for?"
        }
        response = await ac.post("/api/v1/chat", json=payload)
        
    assert response.status_code == 200
    data = response.json()
    assert data["flow"] == "PUBLIC_SERVICE" or data["flow"] == "ELIGIBILITY_CHECK"
    assert data["urgency"]["level"] in ["HIGH", "NORMAL"]
    assert len(data["recommendations"]) > 0
    assert "DISCLAIMER" in data["disclaimer"]
