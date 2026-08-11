from typing import Dict, List, Optional
from datetime import datetime
from app.models.schemas import ToolDefinition

class ToolRegistryService:
    """
    Central registry for versioned AI tools with permission management and status tracking.
    """
    
    def __init__(self):
        self._tools: Dict[str, ToolDefinition] = {}
        # Seed default built-in tools
        self._seed_default_tools()
        
    def _seed_default_tools(self):
        default_tools = [
            ToolDefinition(
                name="knowledge_search",
                version="1.0.0",
                category="knowledge_search",
                description="Search authoritative public service knowledge base chunks using hybrid RAG.",
                input_schema={"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]},
                output_schema={"type": "array", "items": {"type": "object"}},
                permissions=["READ_ONLY", "PUBLIC_LOOKUP"],
                reliability_score=0.98,
                status="ACTIVE",
                created_at=datetime.utcnow().isoformat(),
                approved_by="SYSTEM"
            ),
            ToolDefinition(
                name="eligibility_evaluator",
                version="1.0.0",
                category="eligibility_check",
                description="Evaluate structured rule criteria against user facts deterministically.",
                input_schema={"type": "object", "properties": {"scheme_id": {"type": "string"}, "user_facts": {"type": "object"}}, "required": ["scheme_id", "user_facts"]},
                output_schema={"type": "object"},
                permissions=["READ_ONLY", "DETERMINISTIC_RULES"],
                reliability_score=0.99,
                status="ACTIVE",
                created_at=datetime.utcnow().isoformat(),
                approved_by="SYSTEM"
            )
        ]
        for t in default_tools:
            self.register_tool(t)

    def register_tool(self, tool: ToolDefinition) -> ToolDefinition:
        key = f"{tool.name}:{tool.version}"
        self._tools[key] = tool
        return tool

    def get_tool(self, name: str, version: str = "1.0.0") -> Optional[ToolDefinition]:
        return self._tools.get(f"{name}:{version}")

    def list_tools(self) -> List[ToolDefinition]:
        return list(self._tools.values())

tool_registry_service = ToolRegistryService()
