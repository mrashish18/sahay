from typing import Dict, Any, Tuple, List, Optional
from app.models.schemas import FlowType, UrgencyLevel, Urgency
from app.services.semantic_understanding import semantic_engine, SemanticQueryResult

class ConversationRouter:
    """
    Intelligent Conversation Router for Sahay 2.0.
    Delegates to Semantic Understanding Engine & Multi-Turn Conversation Memory.
    No longer relies solely on keyword lists!
    """

    def route(
        self,
        user_message: str,
        user_context: Optional[Dict[str, Any]] = None,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> Tuple[FlowType, str, Dict[str, Any], Urgency, SemanticQueryResult]:
        
        user_context = user_context or {}
        conversation_history = conversation_history or []

        res: SemanticQueryResult = semantic_engine.understand_and_normalize(
            user_message=user_message,
            conversation_history=conversation_history,
            user_context=user_context
        )

        extracted_facts = dict(user_context)
        extracted_facts.update(res.entities)

        return res.flow, res.primary_intent, extracted_facts, res.urgency, res

conversation_router = ConversationRouter()
