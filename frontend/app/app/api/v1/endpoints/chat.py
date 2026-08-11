import logging
import traceback

from fastapi import APIRouter, HTTPException, status, Request
from app.models.schemas import ChatRequest, SahayResponse
from app.services.ai_orchestrator import ai_orchestrator

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/chat", response_model=SahayResponse)
async def chat_endpoint(request: ChatRequest) -> SahayResponse:
    try:
        response = ai_orchestrator.process_request(request)
        return response
    except Exception as e:
        logger.error(
            "Chat processing failed for conversation_id=%s: %s\n%s",
            request.conversation_id,
            str(e),
            traceback.format_exc(),
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal error occurred while processing your request. Please try again.",
        )
