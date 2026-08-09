import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.services.knowledge_base import knowledge_base_service

def test_knowledge_base_loading():
    schemes = knowledge_base_service.list_schemes()
    assert len(schemes) >= 4
    scheme_ids = [s["id"] for s in schemes]
    assert "SCH-GOV-001" in scheme_ids
    assert "SCH-GOV-002" in scheme_ids

def test_scheme_document_retrieval():
    docs = knowledge_base_service.get_documents_for_scheme("SCH-GOV-001")
    assert len(docs) > 0
    doc_names = [d.document_name for d in docs]
    assert any("Photo ID" in name for name in doc_names)

@pytest.mark.anyio
async def test_get_schemes_endpoint():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/v1/schemes")
    assert response.status_code == 200
    schemes = response.json()
    assert len(schemes) >= 4

@pytest.mark.anyio
async def test_get_specific_scheme_endpoint():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/v1/schemes/SCH-GOV-001")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "SCH-GOV-001"
    assert "FEMA" in data["issuing_authority"]
