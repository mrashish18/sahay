from enum import Enum
from typing import List, Dict, Any, Optional, Union
from pydantic import BaseModel, Field

class CriterionStatus(str, Enum):
    SATISFIED = "SATISFIED"
    NOT_SATISFIED = "NOT_SATISFIED"
    MISSING = "MISSING"
    UNCERTAIN = "UNCERTAIN"
    NOT_APPLICABLE = "NOT_APPLICABLE"

class RuleOperator(str, Enum):
    EQ = "=="
    NE = "!="
    GT = ">"
    GTE = ">="
    LT = "<"
    LTE = "<="
    IN = "in"
    NOT_IN = "not_in"

class LogicalOperator(str, Enum):
    AND = "AND"
    OR = "OR"
    NOT = "NOT"

class PeriodType(str, Enum):
    MONTHLY = "monthly"
    ANNUAL = "annual"
    ONE_TIME = "one_time"
    UNKNOWN = "unknown"

class RuleCondition(BaseModel):
    field: str = Field(..., description="Target user fact field name")
    operator: RuleOperator = Field(..., description="Comparison operator")
    value: Any = Field(..., description="Target threshold or value")
    description: str = Field(..., description="Human-readable condition description from scheme data")
    period: PeriodType = Field(default=PeriodType.UNKNOWN, description="Monetary or temporal period if applicable")
    currency: Optional[str] = Field(default=None, description="Currency code (e.g. INR, USD)")
    is_mandatory: bool = Field(default=True, description="Whether failure of this condition invalidates eligibility")

class RuleGroup(BaseModel):
    logical_operator: LogicalOperator = Field(default=LogicalOperator.AND, description="AND / OR connector")
    conditions: List[RuleCondition] = Field(default_factory=list, description="List of simple conditions")
    subgroups: List['RuleGroup'] = Field(default_factory=list, description="Nested rule groups")

# Enable self-referencing model for nested RuleGroup
RuleGroup.model_rebuild()

class CriterionTrace(BaseModel):
    criterion: str = Field(..., description="Condition description")
    field: str = Field(..., description="Evaluated field")
    status: CriterionStatus = Field(..., description="Evaluation result: SATISFIED, NOT_SATISFIED, MISSING, UNCERTAIN")
    user_value: Optional[Any] = Field(default=None, description="User value extracted")
    required_value: Any = Field(..., description="Required threshold or value")
    reason: str = Field(..., description="Detailed explanation of evaluation")

class DetailedEligibilityTrace(BaseModel):
    scheme_id: str = Field(..., description="Evaluated scheme identifier")
    status: str = Field(..., description="Evaluated eligibility state (LIKELY_ELIGIBLE, POTENTIALLY_ELIGIBLE, INELIGIBLE, UNCERTAIN)")
    criteria_evaluated: List[CriterionTrace] = Field(default_factory=list, description="Transparent trace of all evaluated criteria")
    matched_count: int = Field(default=0)
    failed_count: int = Field(default=0)
    missing_count: int = Field(default=0)
