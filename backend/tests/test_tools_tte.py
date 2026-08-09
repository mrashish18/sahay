import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.anyio
async def test_list_tools():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/v1/tools")
    assert response.status_code == 200
    tools = response.json()
    assert len(tools) >= 2
    tool_names = [t["name"] for t in tools]
    assert "knowledge_search" in tool_names
    assert "eligibility_evaluator" in tool_names

@pytest.mark.anyio
async def test_tte_proposal_and_approval_flow():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Step 1: Propose valid safe tool
        params = {
            "tool_name": "custom_housing_calculator",
            "problem_context": "Calculate income threshold ratio for housing vouchers",
            "generated_code": "def calculate_ratio(income, threshold):\n    return income / threshold\n"
        }
        prop_res = await ac.post("/api/v1/tte/propose", params=params)
        assert prop_res.status_code == 200
        proposal = prop_res.json()
        assert proposal["static_analysis_passed"] is True
        assert proposal["security_audit_passed"] is True
        prop_id = proposal["proposal_id"]
        
        # Step 2: Approve proposal
        app_res = await ac.post("/api/v1/tte/approve", json={"proposal_id": prop_id, "approved_by": "TEST_ADMIN"})
        assert app_res.status_code == 200
        approved_tool = app_res.json()
        assert approved_tool["name"] == "custom_housing_calculator"
        assert approved_tool["approved_by"] == "TEST_ADMIN"

@pytest.mark.anyio
async def test_tte_unsafe_code_rejection():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Propose unsafe tool attempting forbidden import
        params = {
            "tool_name": "malicious_tool",
            "problem_context": "Attempt system execution",
            "generated_code": "import os\nos.system('echo hacked')\n"
        }
        prop_res = await ac.post("/api/v1/tte/propose", params=params)
        assert prop_res.status_code == 200
        proposal = prop_res.json()
        assert proposal["static_analysis_passed"] is False
        assert proposal["security_audit_passed"] is False
        prop_id = proposal["proposal_id"]
        
        # Attempt approval should fail with 400
        app_res = await ac.post("/api/v1/tte/approve", json={"proposal_id": prop_id, "approved_by": "TEST_ADMIN"})
        assert app_res.status_code == 400
