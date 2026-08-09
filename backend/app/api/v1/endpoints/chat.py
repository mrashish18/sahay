from fastapi import APIRouter, HTTPException, status
from app.models.schemas import ChatRequest, SahayResponse
from app.services.ai_orchestrator import ai_orchestrator

router = APIRouter()

@router.post("/chat", response_model=SahayResponse)
async def chat_endpoint(request: ChatRequest) -> SahayResponse:
    try:
        response = ai_orchestrator.process_request(request)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing your request: {str(e)}"
        )
