from enum import Enum
from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class FlowType(str, Enum):
    CRISIS = "CRISIS"
    PUBLIC_SERVICE = "PUBLIC_SERVICE"
    ELIGIBILITY_CHECK = "ELIGIBILITY_CHECK"
    DOCUMENT_GUIDANCE = "DOCUMENT_GUIDANCE"
    GENERAL_INFORMATION = "GENERAL_INFORMATION"
    WEB_SEARCH_REQUIRED = "WEB_SEARCH_REQUIRED"
    AMBIGUOUS = "AMBIGUOUS"

class UrgencyLevel(str, Enum):
    CRISIS = "CRISIS"
    HIGH = "HIGH"
    NORMAL = "NORMAL"
    INFORMATIONAL = "INFORMATIONAL"

class EligibilityStatus(str, Enum):
    LIKELY_ELIGIBLE = "LIKELY_ELIGIBLE"
    POTENTIALLY_ELIGIBLE = "POTENTIALLY_ELIGIBLE"
    INELIGIBLE = "INELIGIBLE"
    UNCERTAIN = "UNCERTAIN"

class TTEProposalStatus(str, Enum):
    PROPOSED = "PROPOSED"
    VALIDATED = "VALIDATED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

# ---------------------------------------------------------------------------
# Nested Sub-Models
# ---------------------------------------------------------------------------

class Situation(BaseModel):
    summary: str = Field(..., description="Brief natural language summary of detected context")
    extracted_facts: Dict[str, Any] = Field(default_factory=dict, description="Facts extracted from input (income, employment, location, etc.)")
    primary_intent: Optional[str] = Field(None, description="Classified primary intent taxonomy")
    weather_data: Optional[Dict[str, Any]] = Field(None, description="Live weather payload from Open-Meteo")


class Urgency(BaseModel):
    level: UrgencyLevel = Field(..., description="Assessed urgency rating")
    score: float = Field(..., ge=0.0, le=1.0, description="Confidence/severity score between 0.0 and 1.0")
    reasoning: str = Field(..., description="Justification for the urgency rating")

class MissingInfoItem(BaseModel):
    field: str = Field(..., description="Key identifier for missing attribute")
    question: str = Field(..., description="User-facing prompt question to clarify the missing fact")
    importance: str = Field(default="high", description="Priority level: high, medium, low")

class RecommendationItem(BaseModel):
    scheme_id: str = Field(..., description="Unique scheme identifier")
    title: str = Field(..., description="Name of public service / assistance program")
    issuing_authority: str = Field(..., description="Official government department or agency")
    country: Optional[str] = "IN"
    jurisdiction_level: Optional[str] = "NATIONAL"
    region: Optional[str] = None
    category: str = Field(..., description="Service domain / category")
    summary: str = Field(..., description="Concise explanation of assistance provided")
    match_confidence: str = Field(default="HIGH", description="Confidence level: HIGH, MEDIUM, LOW")

class EligibilityItem(BaseModel):
    scheme_id: str = Field(..., description="Target scheme identifier")
    status: EligibilityStatus = Field(..., description="Evaluated eligibility status")
    matching_criteria: List[str] = Field(default_factory=list, description="Criteria satisfied by user facts")
    unmet_criteria: List[str] = Field(default_factory=list, description="Criteria failed or unsatisfied")
    reasoning: str = Field(..., description="Deterministic explanation of evaluation result")

class DocumentItem(BaseModel):
    document_name: str = Field(..., description="Official title of document")
    purpose: str = Field(..., description="Why this document is required")
    how_to_obtain: str = Field(..., description="Step-by-step guidance on acquiring the document")
    is_mandatory: bool = Field(default=True, description="Whether application fails without it")

class DocumentRequirement(BaseModel):
    document_name: str
    purpose: str
    how_to_obtain: str
    is_mandatory: bool = True

class ActionStep(BaseModel):
    step_number: int = Field(..., ge=1, description="Sequence order of action step")
    title: str = Field(..., description="Short action summary")
    description: str = Field(..., description="Detailed instructions for the user")
    estimated_time: Optional[str] = Field(default=None, description="Expected duration (e.g. 15 mins, 2 days)")

class SourceItem(BaseModel):
    title: str = Field(..., description="Title of official source or portal")
    url: str = Field(..., description="Verified direct web link")
    issuing_authority: str = Field(..., description="Official issuing authority")
    last_verified: Optional[str] = Field(default=None, description="ISO date when link was verified")

class EvidenceItem(BaseModel):
    chunk_id: str
    scheme_id: str
    title: str
    section_type: str = "OVERVIEW"
    content: str
    country: Optional[str] = "IN"
    jurisdiction_level: Optional[str] = "NATIONAL"
    region: Optional[str] = None
    source_url: str = Field(..., description="Verified direct government portal URL")
    issuing_authority: str = Field(..., description="Official government department")
    similarity_score: float = Field(..., ge=0.0, le=1.0, description="Cosine similarity score")
    last_verified: Optional[str] = Field(default=None, description="Verification date")

class SchemeBase(BaseModel):
    title: str = Field(..., description="Official title of the scheme")
    issuing_authority: str = Field(..., description="Government department or agency issuing the scheme")
    country: str = Field(default="IN", description="ISO country code (e.g. IN, US)")
    jurisdiction_level: str = Field(default="NATIONAL", description="Jurisdiction level: NATIONAL, STATE, FEDERAL")
    region: Optional[str] = Field(default=None, description="State or region name (e.g. Bihar, Delhi)")
    jurisdiction: str = Field(..., description="Formatted jurisdiction label")
    category: str = Field(..., description="Assistance category")
    summary: str = Field(..., description="Brief summary")
    description: str = Field(..., description="Detailed description")
    eligibility_rules: Dict[str, Any] = Field(default_factory=dict)
    document_requirements: List[DocumentRequirement] = Field(default_factory=list)
    source_url: str = Field(..., description="Authoritative government source URL")
    effective_date: Optional[str] = Field(default=None)
    last_verified: Optional[str] = Field(default=None)

class SchemeCreate(SchemeBase):
    id: str

class Scheme(SchemeBase):
    id: str

    model_config = ConfigDict(from_attributes=True)

# ---------------------------------------------------------------------------
# Primary Backend Response Contract: SahayResponse
# ---------------------------------------------------------------------------

class SahayResponse(BaseModel):
    request_id: str = Field(..., description="Unique UUID for tracing request")
    timestamp: str = Field(..., description="ISO 8601 timestamp")
    flow: FlowType = Field(..., description="Detected workflow route")
    situation: Situation = Field(..., description="Extracted situation details")
    urgency: Urgency = Field(..., description="Urgency assessment")
    missing_information: List[MissingInfoItem] = Field(default_factory=list, description="Clarification items needed")
    recommendations: List[RecommendationItem] = Field(default_factory=list, description="Matching assistance programs")
    eligibility: List[EligibilityItem] = Field(default_factory=list, description="Evaluated eligibility rules")
    documents: List[DocumentItem] = Field(default_factory=list, description="Required documents checklist")
    action_plan: List[ActionStep] = Field(default_factory=list, description="Ordered step-by-step next steps")
    sources: List[SourceItem] = Field(default_factory=list, description="Verified authoritative evidence links")
    evidence: List[EvidenceItem] = Field(default_factory=list, description="Retrieved RAG evidence chunks")
    disclaimer: str = Field(
        default="DISCLAIMER: Sahay is an independent public-service navigator and does not guarantee official legal eligibility. Please verify all requirements directly with the issuing government authority.",
        description="Non-hallucinatory legal disclaimer"
    )

# Alias for backward compatibility
SahayAIResponse = SahayResponse

# ---------------------------------------------------------------------------
# Request Payloads
# ---------------------------------------------------------------------------

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=10000, description="Natural language situation description")
    conversation_id: Optional[str] = Field(default=None, max_length=100, description="Optional session conversation identifier")
    user_context: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Optional extra user facts")
    location: Optional[str] = Field(default=None, max_length=200, description="Optional state / district / region")

# ---------------------------------------------------------------------------
# Tool Registry & TTE Schemas
# ---------------------------------------------------------------------------

class ToolDefinition(BaseModel):
    name: str
    version: str
    category: str
    description: str
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]
    permissions: List[str]
    reliability_score: float = 1.0
    status: str = "ACTIVE"
    created_at: str
    approved_by: Optional[str] = None

class TTEProposal(BaseModel):
    proposal_id: str
    tool_name: str
    problem_context: str
    generated_code: str
    test_results: Dict[str, Any] = Field(default_factory=dict)
    static_analysis_passed: bool = False
    security_audit_passed: bool = False
    status: TTEProposalStatus = TTEProposalStatus.PROPOSED
    created_at: str

class TTEApproveRequest(BaseModel):
    proposal_id: str
    approved_by: str = "ADMIN"
