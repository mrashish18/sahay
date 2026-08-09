from typing import List
from fastapi import APIRouter, HTTPException, status
from app.models.schemas import ToolDefinition, TTEProposal, TTEApproveRequest
from app.services.tool_registry import tool_registry_service
from app.services.tte_engine import tte_engine

router = APIRouter()

@router.get("/tools", response_model=List[ToolDefinition])
async def list_tools() -> List[ToolDefinition]:
    return tool_registry_service.list_tools()

@router.post("/tte/propose", response_model=TTEProposal)
async def propose_tte_tool(tool_name: str, problem_context: str, generated_code: str) -> TTEProposal:
    try:
        proposal = tte_engine.propose_tool(
            tool_name=tool_name,
            problem_context=problem_context,
            generated_code=generated_code
        )
        return proposal
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to propose TTE tool: {str(e)}"
        )

@router.post("/tte/approve", response_model=ToolDefinition)
async def approve_tte_tool(req: TTEApproveRequest) -> ToolDefinition:
    try:
        tool = tte_engine.approve_proposal(
            proposal_id=req.proposal_id,
            approved_by=req.approved_by
        )
        if not tool:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Approval failed.")
        return tool
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
