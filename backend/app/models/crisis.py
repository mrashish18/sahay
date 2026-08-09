from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from app.models.schemas import UrgencyLevel, SourceItem, ActionStep, MissingInfoItem

class CrisisType(str, Enum):
    DISASTER = "DISASTER"
    FLOOD = "FLOOD"
    FIRE = "FIRE"
    EARTHQUAKE = "EARTHQUAKE"
    CYCLONE = "CYCLONE"
    STORM = "STORM"
    LANDSLIDE = "LANDSLIDE"
    DISPLACEMENT = "DISPLACEMENT"
    HOMELESSNESS = "HOMELESSNESS"
    FOOD_INSECURITY = "FOOD_INSECURITY"
    MEDICAL_EMERGENCY = "MEDICAL_EMERGENCY"
    SAFETY_THREAT = "SAFETY_THREAT"
    LOST_DOCUMENTS = "LOST_DOCUMENTS"
    OTHER = "OTHER"

class ResourceType(str, Enum):
    EMERGENCY = "EMERGENCY"
    SHELTER = "SHELTER"
    FOOD = "FOOD"
    MEDICAL = "MEDICAL"
    DISASTER_RELIEF = "DISASTER_RELIEF"
    HOUSING = "HOUSING"
    DOCUMENT_REPLACEMENT = "DOCUMENT_REPLACEMENT"
    COUNSELLING = "COUNSELLING"
    PUBLIC_SERVICE = "PUBLIC_SERVICE"

class SafetyStep(BaseModel):
    priority: int = Field(..., description="1 = Highest Immediate Priority")
    title: str = Field(..., description="Action title")
    description: str = Field(..., description="Detailed safety instruction")
    reason: str = Field(..., description="Rationale for safety instruction")

class CrisisResource(BaseModel):
    name: str = Field(..., description="Name of verified emergency resource")
    resource_type: ResourceType = Field(..., description="Type of crisis resource")
    description: str = Field(..., description="Resource details")
    jurisdiction: str = Field(..., description="Jurisdiction scope (e.g. National, Bihar, State)")
    availability: str = Field(..., description="Operating hours / availability")
    source_url: str = Field(..., description="Authoritative source URL")
    issuing_authority: str = Field(..., description="Issuing authority")
    last_verified: Optional[str] = Field(default=None, description="Verification date")
    verified: bool = Field(default=True, description="Whether resource is verified in knowledge base")

class CrisisAssessment(BaseModel):
    crisis_detected: bool = Field(..., description="Whether urgent crisis workflow is active")
    crisis_type: CrisisType = Field(default=CrisisType.OTHER, description="Specific crisis category")
    severity: UrgencyLevel = Field(..., description="Urgency level")
    signals: Dict[str, Any] = Field(default_factory=dict, description="Structured crisis signals")
    immediate_safety_steps: List[SafetyStep] = Field(default_factory=list, description="Prioritized safety actions")
    emergency_resources: List[CrisisResource] = Field(default_factory=list, description="Verified emergency resources")
    assistance_options: List[Dict[str, Any]] = Field(default_factory=list, description="Public assistance schemes")
    missing_information: List[MissingInfoItem] = Field(default_factory=list)
    action_plan: List[ActionStep] = Field(default_factory=list)
    sources: List[SourceItem] = Field(default_factory=list)
