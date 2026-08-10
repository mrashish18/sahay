import logging
import traceback
from typing import List

from fastapi import APIRouter, HTTPException, status
from app.models.schemas import ToolDefinition, TTEProposal, TTEApproveRequest
from app.services.tool_registry import tool_registry_service
from app.services.tte_engine import tte_engine

logger = logging.getLogger(__name__)

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
    except ValueError as ve:
        # ValueError from TTE validation is safe to surface (e.g. "static analysis failed")
        logger.warning("TTE proposal validation rejected for tool '%s': %s", tool_name, str(ve))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tool proposal was rejected due to validation failure.",
        )
    except Exception as e:
        logger.error(
            "TTE proposal failed for tool '%s': %s\n%s",
            tool_name, str(e), traceback.format_exc(),
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal error occurred while processing the tool proposal.",
        )

@router.post("/tte/approve", response_model=ToolDefinition)
async def approve_tte_tool(req: TTEApproveRequest) -> ToolDefinition:
    try:
        tool = tte_engine.approve_proposal(
            proposal_id=req.proposal_id,
            approved_by=req.approved_by
        )
        if not tool:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tool approval could not be completed. Verify the proposal ID and try again.",
            )
        return tool
    except HTTPException:
        raise  # Re-raise our own HTTPExceptions as-is
    except ValueError as ve:
        logger.warning("TTE approval rejected for proposal '%s': %s", req.proposal_id, str(ve))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Approval request was rejected. Verify the proposal ID is valid.",
        )
    except Exception as e:
        logger.error(
            "TTE approval failed for proposal '%s': %s\n%s",
            req.proposal_id, str(e), traceback.format_exc(),
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal error occurred while processing the approval.",
        )
