import logging
from typing import List, Optional, Dict, Any

from fastapi import APIRouter, HTTPException, status, Query
from app.services.knowledge_base import knowledge_base_service

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/schemes", response_model=List[Dict[str, Any]])
async def list_public_schemes(category: Optional[str] = Query(None, description="Filter schemes by category")) -> List[Dict[str, Any]]:
    return knowledge_base_service.list_schemes(category=category)

@router.get("/schemes/{scheme_id}", response_model=Dict[str, Any])
async def get_public_scheme(scheme_id: str) -> Dict[str, Any]:
    scheme = knowledge_base_service.get_scheme(scheme_id)
    if not scheme:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The requested public assistance scheme was not found.",
        )
    return scheme
